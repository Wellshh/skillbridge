"""Small synchronous TCP client for the SkillBridge socket protocol."""

from __future__ import annotations

import socket
from types import TracebackType

from .socket_protocol import DEFAULT_MAX_PAYLOAD_SIZE, recv_frame, send_frame


class SkillBridgeClient:
    def __init__(
        self,
        host: str,
        port: int,
        *,
        timeout: float | None = None,
        max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
    ) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout
        self._max_payload_size = max_payload_size
        self._socket: socket.socket | None = None

    def connect(self) -> None:
        if self._socket is not None:
            return
        sock = socket.create_connection((self._host, self._port), self._timeout)
        sock.settimeout(self._timeout)
        self._socket = sock

    def execute(self, command: str) -> str:
        self.connect()
        assert self._socket is not None
        send_frame(
            self._socket,
            command.encode("utf-8"),
            max_payload_size=self._max_payload_size,
        )
        return recv_frame(
            self._socket,
            max_payload_size=self._max_payload_size,
        ).decode("utf-8")

    def health(self) -> str:
        return self.execute("$health")

    def close(self, *, notify_server: bool = True) -> None:
        sock, self._socket = self._socket, None
        if sock is None:
            return
        if notify_server:
            try:
                send_frame(sock, b"$close", max_payload_size=self._max_payload_size)
            except OSError:
                pass
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()

    def __enter__(self) -> SkillBridgeClient:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc, traceback
        self.close()
