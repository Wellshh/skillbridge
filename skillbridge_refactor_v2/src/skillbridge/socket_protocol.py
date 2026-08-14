"""Length-prefixed socket protocol used by SkillBridge clients and servers."""

from __future__ import annotations

from socket import socket

HEADER_SIZE = 10
DEFAULT_MAX_PAYLOAD_SIZE = 64 * 1024 * 1024


class ProtocolError(RuntimeError):
    pass


class PeerClosedError(ProtocolError):
    def __init__(self, expected: int, received: int) -> None:
        self.expected = expected
        self.received = received
        super().__init__(
            f"peer closed connection after {received} of {expected} expected bytes"
        )


class FrameTooLargeError(ProtocolError):
    pass


def recv_exactly(sock: socket, size: int) -> bytes:
    if size < 0:
        raise ValueError("size must be non-negative")
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise PeerClosedError(size, len(data))
        data.extend(chunk)
    return bytes(data)


def encode_header(payload_size: int) -> bytes:
    if payload_size < 0:
        raise ValueError("payload_size must be non-negative")
    text = f"{payload_size:{HEADER_SIZE}d}"
    if len(text) != HEADER_SIZE:
        raise FrameTooLargeError(
            f"payload length {payload_size} does not fit in {HEADER_SIZE} bytes"
        )
    return text.encode("ascii")


def decode_header(header: bytes) -> int:
    if len(header) != HEADER_SIZE:
        raise ProtocolError(
            f"invalid header size: expected {HEADER_SIZE}, got {len(header)}"
        )
    try:
        text = header.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ProtocolError("length header is not ASCII") from exc
    stripped = text.strip()
    if not stripped or not stripped.isdecimal():
        raise ProtocolError(f"invalid length header: {header!r}")
    return int(stripped, 10)


def recv_frame(
    sock: socket,
    *,
    max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
) -> bytes:
    header = recv_exactly(sock, HEADER_SIZE)
    payload_size = decode_header(header)
    if payload_size > max_payload_size:
        raise FrameTooLargeError(
            f"payload length {payload_size} exceeds limit {max_payload_size}"
        )
    return recv_exactly(sock, payload_size)


def send_frame(
    sock: socket,
    payload: bytes,
    *,
    max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
) -> None:
    if len(payload) > max_payload_size:
        raise FrameTooLargeError(
            f"payload length {len(payload)} exceeds limit {max_payload_size}"
        )
    sock.sendall(encode_header(len(payload)) + payload)
