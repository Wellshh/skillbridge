"""Socket-to-SKILL bridge server."""

from __future__ import annotations

import contextlib
import json
import logging
import os
import re
import sys
from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path
from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
from typing import Any

try:
    from socketserver import UnixStreamServer
except ImportError:  # pragma: no cover - unavailable on some Windows versions
    UnixStreamServer = None  # type: ignore[assignment,misc]

from .pipe import (
    SkillExecutionError,
    SkillPipe,
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeError,
    SkillPipeTimeoutError,
)
from .response_protocol import create_response_protocol
from .socket_protocol import (
    DEFAULT_MAX_PAYLOAD_SIZE,
    FrameTooLargeError,
    PeerClosedError,
    ProtocolError,
    recv_frame,
    send_frame,
)

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
LOG_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
logger = logging.getLogger("skillbridge.server")


class _BridgeServerMixin:
    skill_pipe: SkillPipe
    skill_timeout: float | None
    max_payload_size: int

    def _configure_bridge(
        self,
        *,
        skill_pipe: SkillPipe,
        skill_timeout: float | None,
        max_payload_size: int,
    ) -> None:
        self.skill_pipe = skill_pipe
        self.skill_timeout = skill_timeout
        self.max_payload_size = max_payload_size


class SingleTcpServer(_BridgeServerMixin, TCPServer):
    request_queue_size = 16
    allow_reuse_address = True

    def __init__(
        self,
        port: str | int,
        handler: type[StreamRequestHandler],
        *,
        skill_pipe: SkillPipe,
        skill_timeout: float | None,
        max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
    ) -> None:
        self._configure_bridge(
            skill_pipe=skill_pipe,
            skill_timeout=skill_timeout,
            max_payload_size=max_payload_size,
        )
        super().__init__(("127.0.0.1", int(port)), handler)

    def server_bind(self) -> None:
        try:
            from socket import SIO_LOOPBACK_FAST_PATH  # type: ignore[attr-defined]

            self.socket.ioctl(  # type: ignore[attr-defined]
                SIO_LOOPBACK_FAST_PATH,
                True,
            )
        except (ImportError, AttributeError, OSError):
            pass
        super().server_bind()


class ThreadingTcpServer(ThreadingMixIn, SingleTcpServer):
    daemon_threads = True
    block_on_close = True


def create_tcp_server_class(single: bool) -> type[SingleTcpServer]:
    return SingleTcpServer if single else ThreadingTcpServer


if UnixStreamServer is not None:

    class SingleUnixServer(_BridgeServerMixin, UnixStreamServer):
        request_queue_size = 16
        allow_reuse_address = True

        def __init__(
            self,
            file: str,
            handler: type[StreamRequestHandler],
            *,
            skill_pipe: SkillPipe,
            skill_timeout: float | None,
            max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
        ) -> None:
            self._configure_bridge(
                skill_pipe=skill_pipe,
                skill_timeout=skill_timeout,
                max_payload_size=max_payload_size,
            )
            self.socket_path = _unix_socket_path(file)
            self.socket_path.unlink(missing_ok=True)
            super().__init__(str(self.socket_path), handler)

        def server_close(self) -> None:
            try:
                super().server_close()
            finally:
                self.socket_path.unlink(missing_ok=True)

    class ThreadingUnixServer(ThreadingMixIn, SingleUnixServer):
        daemon_threads = True
        block_on_close = True


def _unix_socket_path(identifier: str) -> Path:
    safe_identifier = re.sub(r"[^A-Za-z0-9_.-]", "_", identifier)
    safe_identifier = safe_identifier[:64] or "default"
    # Keep the AF_UNIX path short on both Linux and macOS.  The environment
    # variable permits a controlled override without accepting path segments
    # from the client-visible identifier.
    socket_directory = Path(os.getenv("SKILLBRIDGE_SOCKET_DIRECTORY", "/tmp"))
    socket_directory.mkdir(parents=True, exist_ok=True)
    return socket_directory / f"skill-server-{safe_identifier}.sock"


def create_unix_server_class(single: bool) -> type[Any]:
    if UnixStreamServer is None:  # pragma: no cover - Windows
        raise RuntimeError("Unix domain sockets are unavailable on this platform")
    return SingleUnixServer if single else ThreadingUnixServer


class Handler(StreamRequestHandler):
    def _server(self) -> _BridgeServerMixin:
        return self.server  # type: ignore[return-value]

    def _send_text(self, text: str) -> None:
        server = self._server()
        send_frame(
            self.request,
            text.encode("utf-8"),
            max_payload_size=server.max_payload_size,
        )

    def handle_one_request(self) -> bool:
        server = self._server()
        try:
            command_bytes = recv_frame(
                self.request,
                max_payload_size=server.max_payload_size,
            )
        except PeerClosedError as exc:
            if exc.received:
                logger.warning(
                    "client %s closed during a frame: %s",
                    self.client_address,
                    exc,
                )
            return False

        if command_bytes == b"$close":
            return False
        if command_bytes == b"$health":
            self._send_text(json.dumps(server.skill_pipe.snapshot().to_dict()))
            return True

        try:
            command = command_bytes.decode("utf-8")
        except UnicodeDecodeError:
            self._send_text("failure <invalid-utf8>")
            return False

        try:
            result = server.skill_pipe.execute(command, timeout=server.skill_timeout)
        except SkillPipeTimeoutError as exc:
            logger.warning("SKILL request timeout in phase %s", exc.phase)
            self._send_text(f"failure <timeout phase={exc.phase}>")
            return False
        except SkillExecutionError as exc:
            self._send_text(f"failure <skill-error>\n{exc.payload}")
            return True
        except SkillPipeDesynchronizedError:
            self._send_text("failure <desynchronized>")
            return False
        except SkillPipeClosedError:
            self._send_text("failure <closed>")
            return False
        except SkillPipeBrokenError:
            logger.exception("SKILL IPC pipe failed")
            self._send_text("failure <pipe-error>")
            return False
        except SkillPipeError:
            logger.exception("SKILL transaction failed")
            self._send_text("failure <pipe-error>")
            return False

        try:
            self._send_text(result)
        except FrameTooLargeError:
            logger.error("SKILL response exceeded configured frame limit")
            self._send_text("failure <response-too-large>")
            return False
        return True

    def handle(self) -> None:
        logger.info("client %s connected", self.client_address)
        while True:
            try:
                if not self.handle_one_request():
                    break
            except (ProtocolError, OSError):
                logger.exception("failed to handle request from %s", self.client_address)
                break
            except Exception:
                logger.exception("unexpected request handler failure")
                break


def create_server(
    id_: str,
    *,
    skill_pipe: SkillPipe,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
    max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
) -> Any:
    if sys.platform == "win32" or force_tcp:
        server_class = create_tcp_server_class(single)
    else:
        server_class = create_unix_server_class(single)
    return server_class(
        id_,
        Handler,
        skill_pipe=skill_pipe,
        skill_timeout=timeout,
        max_payload_size=max_payload_size,
    )


def configure_logging(log_level: str) -> None:
    log_directory = Path(os.getenv("SKILLBRIDGE_LOG_DIRECTORY", "."))
    log_directory.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_directory / "skillbridge_server.log",
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        level=getattr(logging, log_level),
    )


def notify_skill(message: str) -> None:
    sys.stdout.write(message)
    if not message.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.flush()


def main(
    id_: str,
    log_level: str,
    notify: bool,
    single: bool,
    timeout: float | None,
    force_tcp: bool,
    max_payload_size: int,
    skill_protocol: str,
    recover_timeouts: bool | None,
    drain_timeout: float | None,
) -> None:
    configure_logging(log_level)
    protocol = create_response_protocol(skill_protocol)

    with SkillPipe(
        sys.stdin,
        sys.stdout,
        response_protocol=protocol,
        recover_after_timeout=recover_timeouts,
        drain_timeout=drain_timeout,
    ) as skill_pipe:
        with create_server(
            id_,
            skill_pipe=skill_pipe,
            single=single,
            timeout=timeout,
            force_tcp=force_tcp,
            max_payload_size=max_payload_size,
        ) as server:
            logger.info(
                "starting server id=%s protocol=%s recovery=%s timeout=%s",
                id_,
                skill_pipe.protocol_name,
                skill_pipe.recover_after_timeout,
                timeout,
            )
            if notify:
                notify_skill("running")
            server.serve_forever()


def build_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="skillbridge-server")
    parser.add_argument("id", help="TCP port or Unix-socket identifier")
    parser.add_argument(
        "log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"],
    )
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--single", action="store_true")
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("--force-tcp", action="store_true")
    parser.add_argument(
        "--max-payload-size",
        type=int,
        default=DEFAULT_MAX_PAYLOAD_SIZE,
    )
    parser.add_argument(
        "--skill-protocol",
        choices=["line", "framed"],
        default="line",
    )
    parser.add_argument(
        "--recover-timeouts",
        action=BooleanOptionalAction,
        default=None,
        help="default: enabled for framed, disabled for line",
    )
    parser.add_argument("--drain-timeout", type=float, default=30.0)
    return parser


def cli() -> None:
    ns = build_argument_parser().parse_args()
    for name in ("timeout", "drain_timeout"):
        value = getattr(ns, name)
        if value is not None and value < 0:
            raise SystemExit(f"--{name.replace('_', '-')} must be non-negative")
    if ns.max_payload_size <= 0:
        raise SystemExit("--max-payload-size must be positive")
    if ns.skill_protocol == "line" and ns.recover_timeouts is True:
        raise SystemExit("--recover-timeouts requires --skill-protocol framed")

    with contextlib.suppress(KeyboardInterrupt):
        main(
            ns.id,
            ns.log_level,
            ns.notify,
            ns.single,
            ns.timeout,
            ns.force_tcp,
            ns.max_payload_size,
            ns.skill_protocol,
            ns.recover_timeouts,
            ns.drain_timeout,
        )


if __name__ == "__main__":
    cli()
