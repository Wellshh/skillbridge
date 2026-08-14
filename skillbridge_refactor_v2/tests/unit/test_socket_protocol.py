from __future__ import annotations

from collections import deque

import pytest

from skillbridge.socket_protocol import (
    FrameTooLargeError,
    PeerClosedError,
    ProtocolError,
    decode_header,
    encode_header,
    recv_exactly,
    recv_frame,
    send_frame,
)


class FakeSocket:
    def __init__(self, chunks: list[bytes] | None = None) -> None:
        self.chunks = deque(chunks or [])
        self.sent = bytearray()

    def recv(self, size: int) -> bytes:
        if not self.chunks:
            return b""
        chunk = self.chunks.popleft()
        if len(chunk) <= size:
            return chunk
        self.chunks.appendleft(chunk[size:])
        return chunk[:size]

    def sendall(self, data: bytes) -> None:
        self.sent.extend(data)


def test_header_round_trip() -> None:
    assert encode_header(9) == b"         9"
    assert decode_header(encode_header(123456)) == 123456


def test_decode_header_rejects_invalid_data() -> None:
    with pytest.raises(ProtocolError):
        decode_header(b"abcdefg123")
    with pytest.raises(ProtocolError):
        decode_header(b"\xff        1")


def test_recv_exactly_reassembles_fragmented_stream() -> None:
    assert recv_exactly(FakeSocket([b"a", b"bc", b"def"]), 6) == b"abcdef"


def test_recv_exactly_reports_truncation() -> None:
    with pytest.raises(PeerClosedError) as caught:
        recv_exactly(FakeSocket([b"abc", b""]), 5)
    assert caught.value.received == 3


def test_recv_frame_handles_fragmented_header_and_payload() -> None:
    payload = b"hello"
    wire = encode_header(len(payload)) + payload
    assert recv_frame(FakeSocket([wire[:2], wire[2:9], wire[9:12], wire[12:]])) == payload


def test_size_limits_apply_to_receive_and_send() -> None:
    with pytest.raises(FrameTooLargeError):
        recv_frame(FakeSocket([encode_header(100)]), max_payload_size=10)
    with pytest.raises(FrameTooLargeError):
        send_frame(FakeSocket(), b"abc", max_payload_size=2)


def test_send_frame_writes_one_complete_frame() -> None:
    sock = FakeSocket()
    send_frame(sock, b"abc")
    assert bytes(sock.sent) == b"         3abc"
