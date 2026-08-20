#!/usr/bin/env python3
from __future__ import annotations

import logging
import os
from argparse import ArgumentParser
from contextlib import suppress
from logging import WARNING, basicConfig, getLogger
from os import getenv
from pathlib import Path
from socketserver import (
    StreamRequestHandler,
    TCPServer,
    ThreadingMixIn,
)

try:
    from socketserver import UnixStreamServer
except ImportError:  # pragma: no cover - Windows: unix domain sockets unavailable
    UnixStreamServer = None  # type: ignore[assignment,misc]
from sys import argv, platform, stderr, stdin, stdout
from sys import exit as sys_exit
from typing import Any, cast

from skillbridge.exception import PeerClosedError, SkillPipeError
from skillbridge.protocol.response import SkillResp
from skillbridge.protocol.socket import Socket
from skillbridge.server._pipe import Pipe

LOG_DIRECTORY = Path(getenv('SKILLBRIDGE_LOG_DIRECTORY', '.'))
LOG_FILE = LOG_DIRECTORY / 'skillbridge_server.log'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_LEVEL = WARNING

basicConfig(filename=LOG_FILE, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = getLogger("python-server")


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
    ) -> None:
        self.pipe = pipe
        self.timeout = timeout
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


def create_tcp_server_class(single: bool) -> type[SingleTcpServer]:
    return SingleTcpServer if single else ThreadingTcpServer


if UnixStreamServer is not None:

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
        ) -> None:
            path = f"/tmp/skill-server-{file}.sock"
            self.path = Path(path)
            self.path.unlink(missing_ok=True)
            self.pipe = pipe
            self.timeout = timeout

            super().__init__(path, handler)

        def server_close(self) -> None:
            try:
                super().server_close()
            finally:
                self.path.unlink(missing_ok=True)

    class ThreadingUnixServer(ThreadingMixIn, SingleUnixServer):
        daemon_threads = True


def create_unix_server_class(single: bool) -> type[SingleUnixServer]:
    if UnixStreamServer is None:  # pragma: no cover - Windows
        msg = "Unix domain sockets are unavailable on this platform"
        raise RuntimeError(msg)
    return SingleUnixServer if single else ThreadingUnixServer


def _respond_to_client(request: Any, response: SkillResp) -> None:
    restarting = response.status == 'restart'
    status = 'success' if restarting else response.status
    result = f'{status} {response.payload}'
    if restarting:
        logger.info("graceful restart requested; exiting daemon")

    payload = result.encode()
    try:
        Socket(request).send_frame(payload)
        logger.debug("sent response to client")
    finally:
        if restarting:
            os._exit(0)


class Handler(StreamRequestHandler):
    def handle_one_request(self) -> bool:
        sock = Socket(self.request)
        try:
            command = sock.recv_frame()
        except PeerClosedError:
            logger.warning(f"client {self.client_address} lost connection")
            return False

        logger.debug(f"received {len(command)} bytes")

        if command.startswith(b'$close'):
            logger.debug(f"client {self.client_address} disconnected")
            return False

        decoded = command.decode()
        logger.debug(f"got data {decoded[:1000]}")
        server = cast("SingleTcpServer | SingleUnixServer", self.server)
        try:
            response = server.pipe.execute(decoded, timeout=server.timeout)
        except SkillPipeError as exc:
            _respond_to_client(self.request, SkillResp('failure', exc.wire_payload))
            return False
        logger.debug(f"got response from skill {response.payload[:1000]!r}")

        _respond_to_client(self.request, response)
        return True

    def try_handle_one_request(self) -> bool:
        try:
            return self.handle_one_request()
        except Exception:
            logger.exception("Failed to handle request")
            return False

    def handle(self) -> None:
        logger.info(f"client {self.client_address} connected")
        while self.try_handle_one_request():
            pass


def create_server(
    id_: str,
    *,
    pipe: Pipe,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
) -> SingleTcpServer | SingleUnixServer:
    serv_cls: type[SingleUnixServer | SingleTcpServer]

    if platform == "win32" or force_tcp:
        serv_cls = create_tcp_server_class(single)
    else:
        serv_cls = create_unix_server_class(single)
    return serv_cls(id_, Handler, pipe=pipe, timeout=timeout)


def main(
    id_: str,
    log_level: str,
    notify: bool,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
) -> None:
    logger.setLevel(getattr(logging, log_level))
    with Pipe(stdin, stdout) as pipe, create_server(
        id_,
        pipe=pipe,
        single=single,
        timeout=timeout,
        force_tcp=force_tcp,
    ) as server:
        logger.info(
            f"starting server id={id_} log={log_level} {notify=} {single=} {timeout=} {force_tcp=}",
        )
        if notify:
            stdout.write('running\n')
            stdout.flush()
        server.serve_forever()


if __name__ == '__main__':
    log_levels = ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL", "FATAL"]
    argument_parser = ArgumentParser(argv[0])
    argument_parser.add_argument('id')
    argument_parser.add_argument('log_level', choices=log_levels)
    argument_parser.add_argument('--notify', action='store_true')
    argument_parser.add_argument('--single', action='store_true')
    argument_parser.add_argument('--timeout', type=float, default=None)
    argument_parser.add_argument('--force-tcp', action='store_true')

    ns = argument_parser.parse_args()

    if platform == 'win32' and ns.timeout is not None:
        print("Timeout is not possible on Windows", file=stderr)
        sys_exit(1)

    with suppress(KeyboardInterrupt):
        main(ns.id, ns.log_level, ns.notify, ns.single, ns.timeout, ns.force_tcp)
