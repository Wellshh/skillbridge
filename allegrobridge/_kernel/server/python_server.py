#!/usr/bin/env python3
# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import os
import socket
import stat
from argparse import ArgumentParser
from contextlib import suppress
from errno import EACCES, EADDRINUSE, EAGAIN, ECONNREFUSED
from io import BufferedIOBase
from logging import getLogger
from os import getenv
from pathlib import Path
from socketserver import (
    StreamRequestHandler,
    TCPServer,
    ThreadingMixIn,
)
from threading import Condition, Thread

try:
    from socketserver import UnixStreamServer
except ImportError:  # pragma: no cover - Windows: unix domain sockets unavailable
    UnixStreamServer = None  # type: ignore[assignment,misc]
from sys import platform, stdin, stdout
from typing import cast

from allegrobridge._kernel.exception import (
    FrameTooLargeError,
    PeerClosedError,
    SkillPipeError,
    SkillPipeTimeoutError,
)
from allegrobridge._kernel.protocol.response import SkillResp
from allegrobridge._kernel.protocol.socket import DEFAULT_MAX_PAYLOAD_SIZE, Socket
from allegrobridge._kernel.server._pipe import Pipe
from allegrobridge._logging import setup_logging

LOG_DIRECTORY = Path(getenv('ALLEGROBRIDGE_LOG_DIRECTORY', '.'))
LOG_FILE = LOG_DIRECTORY / 'allegrobridge_server.log'
logger = getLogger("allegrobridge.server")
_SHUTDOWN_GRACE_SECONDS = 1.0

# payload size should at least be capable of reporting back error
MIN_MAX_PAYLOAD_SIZE = 28


class _RequestTracker:
    """Thread-safe counter tracking in-flight requests for graceful shutdown.

    Coordinates request execution with server shutdown by gating new requests
    and allowing active handlers to finish sending responses (such as ACK frames)
    before the process exits.

    Attributes:
        _active: Number of currently in-flight requests being processed.
        _stopping: Flag indicating whether new requests are being rejected.
        _sync: Condition variable synchronizing active counter updates and drain waits.
    """

    def __init__(self) -> None:
        self._active = 0
        self._stopping = False
        self._sync = Condition()

    def start(self) -> bool:
        with self._sync:
            if self._stopping:
                return False
            self._active += 1
            return True

    def finish(self) -> None:
        with self._sync:
            self._active -= 1
            self._sync.notify_all()

    def stop_and_wait(self, timeout: float) -> bool:
        with self._sync:
            self._stopping = True
            return self._sync.wait_for(lambda: self._active == 0, timeout)


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
        self._requests = _RequestTracker()
        self.max_payload_size = max_payload_size
        super().__init__(("localhost", int(port)), handler)

    @property
    def request_tracker(self) -> _RequestTracker:
        return self._requests

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
    import fcntl

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
            self.lock_path = Path(f"{path}.lock")
            self._lock_fd: int | None = None
            self._owned_identity: tuple[int, int] | None = None
            self.pipe = pipe
            self.timeout = timeout
            self._requests = _RequestTracker()
            self.max_payload_size = max_payload_size

            super().__init__(path, handler)

        def _acquire_lock(self) -> None:
            flags = os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW
            self._lock_fd = os.open(self.lock_path, flags, 0o600)
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                if exc.errno in {EACCES, EAGAIN}:
                    raise OSError(EADDRINUSE, f"Unix endpoint is busy: {self.path}") from exc
                raise

        def _prepare_socket_path(self) -> None:
            try:
                identity = self.path.lstat()
            except FileNotFoundError:
                return
            if stat.S_ISLNK(identity.st_mode) or not stat.S_ISSOCK(identity.st_mode):
                raise OSError(EADDRINUSE, f"Unix endpoint is not a stale socket: {self.path}")

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe:
                probe.settimeout(0.1)
                try:
                    probe.connect(str(self.path))
                except FileNotFoundError:
                    return
                except OSError as exc:
                    if exc.errno != ECONNREFUSED:
                        raise OSError(EADDRINUSE, f"Unix endpoint is busy: {self.path}") from exc
                    current = self.path.lstat()
                    if not stat.S_ISSOCK(current.st_mode) or (
                        current.st_dev,
                        current.st_ino,
                    ) != (identity.st_dev, identity.st_ino):
                        raise OSError(EADDRINUSE, f"Unix endpoint changed: {self.path}") from exc
                    self.path.unlink()
                else:
                    raise OSError(EADDRINUSE, f"Unix endpoint is busy: {self.path}")

        def server_bind(self) -> None:
            self._acquire_lock()
            self._prepare_socket_path()
            super().server_bind()
            identity = self.path.lstat()
            self._owned_identity = (identity.st_dev, identity.st_ino)

        def _release_lock(self) -> None:
            fd, self._lock_fd = self._lock_fd, None
            if fd is not None:
                os.close(fd)

        def _unlink_owned_path(self) -> None:
            identity, self._owned_identity = self._owned_identity, None
            if identity is None:
                return
            try:
                current = self.path.lstat()
            except FileNotFoundError:
                return
            if stat.S_ISSOCK(current.st_mode) and (current.st_dev, current.st_ino) == identity:
                self.path.unlink(missing_ok=True)

        @property
        def request_tracker(self) -> _RequestTracker:
            return self._requests

        def server_close(self) -> None:
            try:
                super().server_close()
            finally:
                try:
                    self._unlink_owned_path()
                finally:
                    self._release_lock()

    class ThreadingUnixServer(ThreadingMixIn, SingleUnixServer):
        daemon_threads = True


def _respond_to_client(sock: Socket, response: SkillResp) -> None:
    status = 'success' if response.status == 'restart' else response.status

    payload = response.payload.encode()
    sock.send_frame(payload, prefix=f'{status} '.encode())
    logger.debug("sent response to client")


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
        if not server.request_tracker.start():
            return False
        try:
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
            return response.status != 'restart'
        finally:
            server.request_tracker.finish()

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


def _watch_pipe_death(
    pipe: Pipe,
    tracker: _RequestTracker,
    *,
    grace: float = _SHUTDOWN_GRACE_SECONDS,
) -> None:
    if pipe.wait_peer_closed():
        logger.info("SKILL IPC reader stopped; stopping request intake")
        if not tracker.stop_and_wait(grace):
            logger.warning("SKILL IPC shutdown grace expired with active requests")
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
    setup_logging(level=log_level, console=False, file=LOG_FILE)
    with (
        Pipe(
            cast("BufferedIOBase", stdin.buffer),
            stdout,
            reader_encoding=stdin.encoding,
        ) as pipe,
        create_server(
            id_,
            pipe=pipe,
            single=single,
            timeout=timeout,
            force_tcp=force_tcp,
            max_payload_size=max_payload_size,
        ) as server,
    ):
        Thread(
            target=_watch_pipe_death,
            args=(pipe, server.request_tracker),
            name="allegrobridge-pipe-watcher",
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
