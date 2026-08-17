from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from socket import SHUT_WR, socket, socketpair

from pytest import fixture, mark, raises

from skillbridge.exception import FrameTooLargeError, PeerClosedError, ProtocolError
from skillbridge.protocol.socket import Socket

SOCKET_TIMEOUT_SECONDS = 1.0

# For socket test, we always use socket.socketpaire instead of
# mocking it for behavioural tests


@fixture(scope="function")
def raw_socket_pair() -> Iterator[tuple[socket, socket]]:
    sender, receiver = socketpair()
    sender.settimeout(SOCKET_TIMEOUT_SECONDS)
    receiver.settimeout(SOCKET_TIMEOUT_SECONDS)
    try:
        yield sender, receiver
    finally:
        sender.close()
        receiver.close()


class FragmentedSocket:
    def __init__(self, *chunks: bytes) -> None:
        self._chunks = deque(chunks)

    def recv_into(self, buffer: memoryview) -> int:
        if not self._chunks:
            return 0

        chunk = self._chunks.popleft()
        received = min(len(buffer), len(chunk))
        buffer[:received] = chunk[:received]
        if received < len(chunk):
            self._chunks.appendleft(chunk[received:])
        return received


class TestHeader:
    @mark.parametrize(
        ('size', 'encoded'),
        [
            (0, b'         0'),
            (123, b'       123'),
            (9_999_999_999, b'9999999999'),
        ],
    )
    def test_roundtrip(self, size: int, encoded: bytes) -> None:
        assert Socket.encode_header(size) == encoded
        assert Socket.decode_header(encoded) == size

    def test_encode_rejects_more_than_ten_digits(self) -> None:
        with raises(FrameTooLargeError) as caught:
            Socket.encode_header(10_000_000_000)

        assert caught.value.size == 10_000_000_000

    @mark.parametrize(
        'header',
        [
            b'        1',
            b'          1',
            b'abcdefg123',
            b'\t        1',
            b'123       ',
            b'\xff        1',
        ],
    )
    def test_decode_rejects_malformed_header(self, header: bytes) -> None:
        with raises(ProtocolError):
            Socket.decode_header(header)


class TestReceive:
    def test_collects_fragmented_data(self) -> None:
        connection = Socket(FragmentedSocket(b'a', b'bc', b'def'))

        assert connection.recv(6) == b'abcdef'

    def test_reports_peer_closed_from_fake(self) -> None:
        connection = Socket(FragmentedSocket(b'ab', b'c'))

        with raises(PeerClosedError) as caught:
            connection.recv(5)

        assert caught.value.expected == 5
        assert caught.value.received == 3

    def test_reports_peer_closed_from_real_socket(
        self,
        raw_socket_pair: tuple[socket, socket],
    ) -> None:
        sender, receiver = raw_socket_pair
        sender.sendall(b'abc')
        sender.shutdown(SHUT_WR)

        with raises(PeerClosedError) as caught:
            Socket(receiver).recv(5)

        assert caught.value.expected == 5
        assert caught.value.received == 3


class TestFrame:
    @mark.parametrize('payload', [b'', b'hello'])
    def test_roundtrip(
        self,
        raw_socket_pair: tuple[socket, socket],
        payload: bytes,
    ) -> None:
        sender, receiver = raw_socket_pair

        Socket(sender).send_frame(payload)

        assert Socket(receiver).recv_frame() == payload

    def test_consecutive_frames_do_not_consume_each_other(
        self,
        raw_socket_pair: tuple[socket, socket],
    ) -> None:
        sender, receiver = raw_socket_pair
        sending = Socket(sender)
        receiving = Socket(receiver)

        sending.send_frame(b'first')
        sending.send_frame(b'second')

        assert receiving.recv_frame() == b'first'
        assert receiving.recv_frame() == b'second'

    def test_properties_expose_wrapped_socket_and_default_limit(
        self,
        raw_socket_pair: tuple[socket, socket],
    ) -> None:
        sender, _ = raw_socket_pair
        connection = Socket(sender)

        assert connection.sock is sender
        assert connection.max_payload_size == Socket.DEFAULT_MAX_PAYLOAD_SIZE_

    def test_send_uses_instance_limit(
        self,
        raw_socket_pair: tuple[socket, socket],
    ) -> None:
        sender, _ = raw_socket_pair

        with raises(FrameTooLargeError) as caught:
            Socket(sender, max_payload_size=3).send_frame(b'four')

        assert caught.value.size == 4
        assert caught.value.max_size == 3

    def test_send_allows_per_call_limit_override(
        self,
        raw_socket_pair: tuple[socket, socket],
    ) -> None:
        sender, receiver = raw_socket_pair

        Socket(sender, max_payload_size=3).send_frame(b'four', max_size=4)

        assert Socket(receiver).recv_frame() == b'four'

    def test_receive_rejects_declared_size_above_limit(
        self,
        raw_socket_pair: tuple[socket, socket],
    ) -> None:
        sender, receiver = raw_socket_pair
        sender.sendall(Socket.encode_header(4))

        with raises(FrameTooLargeError) as caught:
            Socket(receiver).recv_frame(max_size=3)

        assert caught.value.size == 4
        assert caught.value.max_size == 3
