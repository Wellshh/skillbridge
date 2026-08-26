#!/usr/bin/env python3
# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import os
from argparse import ArgumentParser
from contextlib import suppress
from logging import basicConfig, getLogger
from os import getenv
from pathlib import Path
from socketserver import (
    StreamRequestHandler,
    TCPServer,
    ThreadingMixIn,
)
from threading import Thread

try:
    from socketserver import UnixStreamServer
except ImportError:  # pragma: no cover - Windows: unix domain sockets unavailable
    UnixStreamServer = None  # type: ignore[assignment,misc]
from sys import platform, stdin, stdout
from typing import cast

from skillbridge.exception import (
    FrameTooLargeError,
    PeerClosedError,
    SkillPipeError,
    SkillPipeTimeoutError,
)
from skillbridge.protocol.response import SkillResp
from skillbridge.protocol.socket import DEFAULT_MAX_PAYLOAD_SIZE, Socket
from skillbridge.server._pipe import Pipe

LOG_DIRECTORY = Path(getenv('SKILLBRIDGE_LOG_DIRECTORY', '.'))
LOG_FILE = LOG_DIRECTORY / 'skillbridge_server.log'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
basicConfig(filename=LOG_FILE, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = getLogger("python-server")

# payload size should at least be capable of reporting back error
MIN_MAX_PAYLOAD_SIZE = 28


class SingleTcpServer(TCPServer):
    request_queue_size: int = 0
    allow_reuse_address: bool = True

    def __init__(
        self,
        port: str | int,
        handler: type[StreamRequestHandler],
        *,
        pipe: Pipe,
        timeout: float | None,
        max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
    ) -> None:
        self.pipe = pipe
        self.timeout = timeout
        self.max_payload_size = max_payload_size
        super().__init__(("localhost", int(port)), handler)

    def server_bind(self) -> None:
        try:
            from socket import (  # type: ignore[attr-defined]  # ruff: ignore[import-outside-top-level]
                SIO_LOOPBACK_FAST_PATH,
            )

            self.socket.ioctl(  # type: ignore[attr-defined]
                SIO_LOOPBACK_FAST_PATH,
                True,  # ruff: ignore[boolean-positional-value-in-call]
            )
        except ImportError:
            pass
        super().server_bind()


class ThreadingTcpServer(ThreadingMixIn, SingleTcpServer):
    daemon_threads = True


if UnixStreamServer is not None:  # pragma: no branch

    class SingleUnixServer(UnixStreamServer):
        request_queue_size: int = 0
        allow_reuse_address: bool = True

        def __init__(
            self,
            file: str,
            handler: type[StreamRequestHandler],
            *,
            pipe: Pipe,
            timeout: float | None,
            max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
        ) -> None:
            path = f"/tmp/skill-server-{file}.sock"
            self.path = Path(path)
            self.path.unlink(missing_ok=True)
            self.pipe = pipe
            self.timeout = timeout
            self.max_payload_size = max_payload_size

            super().__init__(path, handler)

        def server_close(self) -> None:
            try:
                super().server_close()
            finally:
                self.path.unlink(missing_ok=True)

    class ThreadingUnixServer(ThreadingMixIn, SingleUnixServer):
        daemon_threads = True


def _respond_to_client(sock: Socket, response: SkillResp) -> None:
    restarting = response.status == 'restart'
    status = 'success' if restarting else response.status
    result = f'{status} {response.payload}'
    if restarting:
        logger.info("graceful restart requested; exiting daemon")

    payload = result.encode()
    try:
        sock.send_frame(payload)
        logger.debug("sent response to client")
    finally:
        if restarting:
            os._exit(0)


class Handler(StreamRequestHandler):
    def handle_one_request(self) -> bool:
        server = cast("SingleTcpServer | SingleUnixServer", self.server)
        sock = Socket(self.request, max_payload_size=server.max_payload_size)
        try:
            command = sock.recv_frame()
        except FrameTooLargeError:
            _respond_to_client(sock, SkillResp('failure', '<request-too-large>'))
            return False
        except PeerClosedError:
            logger.warning(f"client {self.client_address} lost connection")
            return False

        logger.debug(f"received {len(command)} bytes")

        if command.startswith(b'$close'):
            logger.debug(f"client {self.client_address} disconnected")
            return False

        try:
            decoded = command.decode()
        except UnicodeDecodeError:
            _respond_to_client(sock, SkillResp('failure', '<invalid-utf8>'))
            return False
        logger.debug(f"got data {decoded[:1000]}")
        try:
            response = server.pipe.execute(decoded, timeout=server.timeout)
        except SkillPipeTimeoutError as exc:
            _respond_to_client(sock, SkillResp('failure', exc.wire_payload))
            return True
        except SkillPipeError as exc:
            _respond_to_client(sock, SkillResp('failure', exc.wire_payload))
            return False
        logger.debug(f"got response from skill {response.payload[:1000]!r}")

        try:
            _respond_to_client(sock, response)
        except FrameTooLargeError:
            _respond_to_client(sock, SkillResp('failure', '<response-too-large>'))
        return True

    def handle(self) -> None:
        logger.info(f"client {self.client_address} connected")
        try:
            while self.handle_one_request():
                pass
        except Exception:
            logger.exception("Failed to handle request")


def create_server(
    id_: str,
    *,
    pipe: Pipe,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
    max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
) -> SingleTcpServer | SingleUnixServer:
    assert max_payload_size >= MIN_MAX_PAYLOAD_SIZE, (
        f"max_payload_size must be at least {MIN_MAX_PAYLOAD_SIZE} bytes"
    )
    serv_cls: type[SingleUnixServer | SingleTcpServer]

    if platform == "win32" or force_tcp:
        serv_cls = SingleTcpServer if single else ThreadingTcpServer
    else:
        if UnixStreamServer is None:  # pragma: no cover - Windows
            msg = "Unix domain sockets are unavailable on this platform"
            raise RuntimeError(msg)
        serv_cls = SingleUnixServer if single else ThreadingUnixServer
    return serv_cls(
        id_,
        Handler,
        pipe=pipe,
        timeout=timeout,
        max_payload_size=max_payload_size,
    )


def _watch_pipe_death(pipe: Pipe) -> None:
    if pipe.wait_peer_closed():
        logger.info("SKILL IPC pipe closed by peer; exiting")
        os._exit(0)


def main(
    id_: str,
    log_level: str,
    notify: bool,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
    max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
) -> None:
    logger.setLevel(log_level)
    with Pipe(stdin, stdout) as pipe, create_server(
        id_,
        pipe=pipe,
        single=single,
        timeout=timeout,
        force_tcp=force_tcp,
        max_payload_size=max_payload_size,
    ) as server:
        Thread(
            target=_watch_pipe_death,
            args=(pipe,),
            name="skillbridge-pipe-watcher",
            daemon=True,
        ).start()
        logger.info(
            f"starting server id={id_} log={log_level} {notify=} "
            f"{single=} {timeout=} {force_tcp=} {max_payload_size=}",
        )
        if notify:
            stdout.write('running\n')
            stdout.flush()
        server.serve_forever()


def build_parser() -> ArgumentParser:
    log_levels = ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL", "FATAL"]
    argument_parser = ArgumentParser()
    argument_parser.add_argument('id')
    argument_parser.add_argument('log_level', choices=log_levels)
    argument_parser.add_argument('--notify', action='store_true')
    argument_parser.add_argument('--single', action='store_true')
    argument_parser.add_argument('--timeout', type=float, default=None)
    argument_parser.add_argument('--force-tcp', action='store_true')
    argument_parser.add_argument(
        '--max-payload-size',
        type=int,
        default=DEFAULT_MAX_PAYLOAD_SIZE,
    )
    return argument_parser


def cli(args: list[str] | None = None) -> None:
    ns = build_parser().parse_args(args)
    with suppress(KeyboardInterrupt):
        main(
            ns.id,
            ns.log_level,
            ns.notify,
            ns.single,
            ns.timeout,
            ns.force_tcp,
            max_payload_size=ns.max_payload_size,
        )


if __name__ == '__main__':  # pragma: no cover
    cli()
