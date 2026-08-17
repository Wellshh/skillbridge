from __future__ import annotations

from contextlib import suppress
from select import select
from socket import AF_INET, SOCK_STREAM, socket
from sys import platform
from typing import Any, TextIO

from skillbridge.exception import PeerClosedError
from skillbridge.protocol.socket import Socket

PORT_RANGE_MIN = 0
PORT_RANGE_MAX = 0xFFFF


class Channel:
    def __init__(self, max_transmission_length: int) -> None:
        self._max_transmission_length = max_transmission_length

    def send(self, data: str) -> str:
        raise NotImplementedError  # pragma: no cover

    def close(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def flush(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def try_repair(self) -> Any:
        raise NotImplementedError  # pragma: no cover

    @property
    def max_transmission_length(self) -> int:
        return self._max_transmission_length

    @max_transmission_length.setter
    def max_transmission_length(self, value: int) -> None:
        self._max_transmission_length = value

    def __del__(self) -> None:
        with suppress(Exception):
            self.close()

    @staticmethod
    def decode_response(response: str) -> str:
        status, response = response.split(' ', maxsplit=1)

        if status == 'failure':
            if response == '<timeout>':
                raise RuntimeError(
                    "Timeout: you should restart the skill server and "
                    "increase the timeout `pyStartServer ?timeout X`.",
                )
            raise RuntimeError(response)
        return response


class DirectChannel(Channel):
    def __init__(self, stdout: TextIO) -> None:
        super().__init__(10_000)
        self.stdout = stdout

    def send(self, data: str) -> str:
        print(data.replace('\n', '\\n'), file=self.stdout, flush=True)
        return self.decode_response(input())

    def close(self) -> None:
        pass

    def flush(self) -> None:
        pass

    def try_repair(self) -> Any:
        pass


class TcpChannel(Channel):
    address_family = AF_INET
    socket_kind = SOCK_STREAM

    def __init__(self, address: Any) -> None:
        super().__init__(1_000_000)

        self.connected = False
        self.address = self.create_address(address)
        self.socket = self.start()
        self._socket = Socket(self.socket, max_payload_size=self._max_transmission_length)

    @staticmethod
    def create_address(id_: Any) -> Any:
        raise NotImplementedError  # pragma: no cover

    def start(self) -> socket:
        sock = self.create_socket()
        self.configure(sock)
        return self.connect(sock)

    def create_socket(self) -> socket:
        return socket(self.address_family, self.socket_kind)

    def configure(self, sock: socket) -> None:
        _ = sock

    def connect(self, sock: socket) -> socket:
        sock.settimeout(1)
        sock.connect(self.address)
        sock.settimeout(None)
        self.connected = True
        return sock

    def reconnect(self) -> None:
        self.socket.close()
        self.socket = self.start()
        self._socket = Socket(self.socket, max_payload_size=self._max_transmission_length)

    def _send_only(self, data: str) -> None:
        byte = data.encode()
        try:
            self._socket.send_frame(byte, max_size=self._max_transmission_length)
        except (BrokenPipeError, OSError):
            print("attempting to reconnect")
            self.reconnect()
            self._socket.send_frame(byte, max_size=self._max_transmission_length)

    def _receive_only(self) -> str:
        try:
            payload = self._socket.recv_frame(max_size=self._max_transmission_length)
        except KeyboardInterrupt:
            raise RuntimeError(
                "Receive aborted, you should restart the skill server or"
                " call `ws.try_repair()` if you are sure that the response"
                " will arrive.",
            ) from None
        except (PeerClosedError, OSError) as e:
            raise RuntimeError("The server unexpectedly died") from e

        return self.decode_response(payload.decode())

    def send(self, data: str) -> str:
        try:
            self._send_only(data)
            return self._receive_only()
        except RuntimeError as e:
            # On some platforms (notably macOS) a dead TCP peer may not be
            # detected during sendall; the failure only surfaces when reading
            # the response.
            if "The server unexpectedly died" not in str(e):
                raise
            print("attempting to reconnect")
            self.reconnect()
            self._send_only(data)
            return self._receive_only()

    def try_repair(self) -> Exception | str:
        try:
            payload = self._socket.recv_frame(max_size=self._max_transmission_length)
        except Exception as e:  # ruff: ignore[blind-except]
            return e
        return payload.decode()

    def close(self) -> None:
        if self.connected:
            try:
                with suppress(ConnectionError):
                    self._socket.send_frame(b'$close')
            finally:
                try:
                    self.socket.close()
                finally:
                    self.connected = False

    def flush(self) -> None:
        while True:
            read, _, _ = select([self.socket], [], [], 0.1)
            if read:
                self._socket.recv_frame()
            else:
                break


def create_channel_class(force_tcp: bool = False) -> type[TcpChannel]:
    if platform == 'win32' or force_tcp:

        class CustomTcpChannel(TcpChannel):
            def configure(self, sock: socket) -> None:
                try:
                    from socket import (  # type: ignore[attr-defined]  # ruff: ignore[import-outside-top-level]
                        SIO_LOOPBACK_FAST_PATH,
                    )

                    sock.ioctl(  # type: ignore[attr-defined]
                        SIO_LOOPBACK_FAST_PATH,
                        True,  # ruff: ignore[boolean-positional-value-in-call]
                    )
                except ImportError:
                    pass

            @staticmethod
            def create_address(id_: str | None) -> tuple[str, int]:
                if id_ is None:
                    return 'localhost', 7777

                if not (id_.isnumeric() and PORT_RANGE_MIN <= int(id_) <= PORT_RANGE_MAX):
                    raise ValueError(
                        f"TCP server requires a numeric id in range 0-65535 (given=`{id_}`)"
                    )

                return 'localhost', int(id_)

        return CustomTcpChannel

    from socket import AF_UNIX  # ruff: ignore[import-outside-top-level]

    class CustomUnixChannel(TcpChannel):
        address_family = AF_UNIX

        @staticmethod
        def create_address(id_: Any) -> Any:
            id_ = 'default' if id_ is None else id_
            return f'/tmp/skill-server-{id_}.sock'

    return CustomUnixChannel
