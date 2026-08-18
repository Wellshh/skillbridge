#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import logging
import os
from argparse import ArgumentParser
from collections.abc import Callable, Generator
from functools import partial
from logging import WARNING, basicConfig, getLogger
from os import getenv
from pathlib import Path
from select import select
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
from typing import Any

from skillbridge.exception import PeerClosedError
from skillbridge.protocol.socket import Socket

LOG_DIRECTORY = Path(getenv('SKILLBRIDGE_LOG_DIRECTORY', '.'))
LOG_FILE = LOG_DIRECTORY / 'skillbridge_server.log'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_LEVEL = WARNING

basicConfig(filename=LOG_FILE, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = getLogger("python-server")


def send_to_skill(data: str) -> None:
    stdout.write(data)
    stdout.write("\n")
    stdout.flush()


def read_from_skill(data_ready: Callable[[], bool]) -> str:

    readable = data_ready()

    if readable:
        return stdin.readline()

    logger.debug("timeout")
    return 'failure <timeout>'


class SingleTcpServer(TCPServer):
    request_queue_size: int = 0
    allow_reuse_address: bool = True
    active: bool = False

    def __init__(self, port: str | int, handler: type[StreamRequestHandler]) -> None:
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

    def verify_request(self, request: Any, client_address: Any) -> bool:
        _ = request, client_address
        if self.active:
            return False

        self.active = True
        return True

    def finish_request(self, request: Any, client_address: Any) -> None:
        super().finish_request(request, client_address)
        self.active = False


class ThreadingTcpServer(ThreadingMixIn, SingleTcpServer):
    pass


def create_tcp_server_class(single: bool) -> type[SingleTcpServer]:
    return SingleTcpServer if single else ThreadingTcpServer


if UnixStreamServer is not None:

    class SingleUnixServer(UnixStreamServer):
        request_queue_size: int = 0
        allow_reuse_address: bool = True

        def __init__(self, file: str, handler: type[StreamRequestHandler]) -> None:

            path = f"/tmp/skill-server-{file}.sock"
            Path(path).unlink(missing_ok=True)

            super().__init__(path, handler)

    class ThreadingUnixServer(ThreadingMixIn, SingleUnixServer):
        pass


def create_unix_server_class(single: bool) -> type[SingleUnixServer]:
    if UnixStreamServer is None:  # pragma: no cover - Windows
        msg = "Unix domain sockets are unavailable on this platform"  # type: ignore[unreachable]
        raise RuntimeError(msg)
    return SingleUnixServer if single else ThreadingUnixServer


def unix_data_ready(timeout: float | None) -> bool:
    readable, _, _ = select([stdin], [], [], timeout)

    return bool(readable)


def win_data_ready() -> bool:
    return True


def _respond_to_client(request: Any, result: str) -> None:
    restarting = result.startswith('restart ')
    if restarting:
        result = 'success ' + result[len('restart ') :]

    payload = result.encode()
    Socket(request).send_frame(payload)
    logger.debug("sent response to client")

    if restarting:
        logger.info("graceful restart requested; exiting daemon")
        os._exit(0)


def create_handler(
    data_ready: Callable[[], bool],
) -> type[StreamRequestHandler]:

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
            logger.debug(f"got data {command[:1000].decode()}")

            send_to_skill(command.decode())
            logger.debug("sent data to skill")
            result = read_from_skill(data_ready)
            logger.debug(f"got response from skill {result[:1000]!r}")

            _respond_to_client(self.request, result)

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

    return Handler


@contextlib.contextmanager
def create_server(
    id_: str,
    log_level: str,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
) -> Generator[SingleTcpServer | SingleUnixServer, Any, None]:
    logger.setLevel(getattr(logging, log_level))

    serv_cls: type[SingleUnixServer | SingleTcpServer]

    if platform == "win32":
        serv_cls = create_tcp_server_class(single)
        data_ready = win_data_ready
    elif force_tcp:
        serv_cls = create_tcp_server_class(single)
        data_ready = partial(unix_data_ready, timeout)
    else:
        serv_cls = create_unix_server_class(single)
        data_ready = partial(unix_data_ready, timeout)

    yield serv_cls(id_, create_handler(data_ready))


def main(
    id_: str,
    log_level: str,
    notify: bool,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
) -> None:

    with create_server(id_, log_level, single, timeout, force_tcp) as server:
        logger.info(
            f"starting server id={id_} log={log_level} {notify=} {single=} {timeout=} {force_tcp=}",
        )
        if notify:
            send_to_skill('running')
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

    with contextlib.suppress(KeyboardInterrupt):
        main(ns.id, ns.log_level, ns.notify, ns.single, ns.timeout, ns.force_tcp)
