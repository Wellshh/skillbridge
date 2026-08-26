# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING, Final

from skillbridge.exception import FrameTooLargeError, PeerClosedError, ProtocolError

if TYPE_CHECKING:
    from socket import socket

DEFAULT_MAX_PAYLOAD_SIZE: Final[int] = 64 * 1024 * 1024  # 64 MiB


class Socket:
    __slots__ = (
        "_max_payload_size",
        "_sock",
    )

    HEADER_SIZE_: Final[int] = 10
    _sock: socket
    _max_payload_size: int

    def __init__(
        self,
        sock: socket,
        *,
        max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
    ) -> None:
        self._sock = sock
        self._max_payload_size = max_payload_size

    @property
    def sock(self) -> socket:
        return self._sock

    @property
    def max_payload_size(self) -> int:
        return self._max_payload_size

    def recv(self, size: int) -> bytes:
        # The original TCP socket.recv does not guarantee to receive
        # set length of data, we chunk it to configured size mannually.
        buffer = bytearray(size)

        # For large payload,e.g. 10MB - assign memory in advance
        view = memoryview(buffer)
        offset = 0

        while offset < size:
            n = self._sock.recv_into(view[offset:])

            if not n:
                raise PeerClosedError(size, offset)

            offset += n

        return bytes(buffer)

    def recv_frame(self, *, max_size: int | None = None) -> bytes:
        limit = self._max_payload_size if max_size is None else max_size
        header_ = self.recv(self.HEADER_SIZE_)
        size = self.decode_header(header_)
        if size > limit:
            raise FrameTooLargeError(size, limit)
        return self.recv(size)

    def send_frame(
        self,
        payload: bytes,
        *,
        max_size: int | None = None,
    ) -> None:
        limit = self._max_payload_size if max_size is None else max_size
        if len(payload) > limit:
            raise FrameTooLargeError(len(payload), limit)
        # ALWAYS sendall to ensure data is sent out
        self._sock.sendall(self.encode_header(len(payload)) + payload)

    @classmethod
    def encode_header(cls, size: int) -> bytes:
        txt = f"{size:{cls.HEADER_SIZE_}d}"
        if len(txt) != cls.HEADER_SIZE_:
            raise FrameTooLargeError(size, DEFAULT_MAX_PAYLOAD_SIZE)
        return txt.encode("ascii")

    @classmethod
    def decode_header(cls, header: bytes) -> int:
        if len(header) != cls.HEADER_SIZE_:
            raise ProtocolError(
                "While decoding header, format is rejected. Expect right-aligned 10-bytes format.",
                hint="Check if the sender socket closed or sent corrupted frame bytes.",
            )

        try:
            txt = header.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ProtocolError("length header is not ASCII") from exc

        digits = txt.lstrip(" ")
        if not digits or not digits.isdecimal():
            raise ProtocolError(f"invalid length header: {header!r}")

        return int(digits)
