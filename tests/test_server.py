# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import io
import socket as socket_mod
import subprocess
import sys
import threading
from collections.abc import Iterator
from contextlib import nullcontext
from os import getpid
from queue import Empty, Queue
from socket import socketpair
from socketserver import BaseServer
from sys import platform
from types import SimpleNamespace
from typing import Any, cast

from pytest import FixtureRequest, MonkeyPatch, approx, fixture, mark, param, raises

from allegrobridge._kernel.client.channel import Channel, TcpChannel, create_channel_class
from allegrobridge._kernel.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeTimeoutError,
)
from allegrobridge._kernel.protocol.response import SkillResp
from allegrobridge._kernel.protocol.socket import DEFAULT_MAX_PAYLOAD_SIZE, Socket
from allegrobridge._kernel.server import python_server

TEST_TIMEOUT = 1.0
channel_class = create_channel_class()
tcp_channel_class = create_channel_class(force_tcp=True)
server_params = (
    [param(True, id='tcp')]
    if platform == 'win32'
    else [param(False, id='unix'), param(True, id='tcp')]
)


class Redirect:
    def __init__(self) -> None:
        self.written: Queue[str] = Queue()
        self.reading: Queue[SkillResp | Exception] = Queue()

    def prepare(self, response: SkillResp | Exception) -> None:
        self.reading.put(response)

    def pop(self, timeout: float = TEST_TIMEOUT) -> str:
        return self.written.get(timeout=timeout)

    def execute(self, command: str, timeout: float | None = None) -> SkillResp:
        del timeout
        self.written.put(command)
        response = self.reading.get(timeout=TEST_TIMEOUT)
        if isinstance(response, Exception):
            raise response
        return response


class Server(threading.Thread):
    def __init__(
        self,
        identifier: str,
        redirect: Redirect,
        use_tcp: bool = False,
        max_payload_size: int = DEFAULT_MAX_PAYLOAD_SIZE,
    ) -> None:
        super().__init__(daemon=True)
        self.identifier = identifier
        self.redirect = redirect
        self.use_tcp = use_tcp
        self.max_payload_size = max_payload_size
        self.server: BaseServer | None = None
        self.ready = threading.Event()
        self.failure: BaseException | None = None

    def run(self) -> None:
        try:
            server = python_server.create_server(
                self.identifier,
                pipe=cast('Any', self.redirect),
                single=False,
                timeout=None,
                force_tcp=self.use_tcp,
                max_payload_size=self.max_payload_size,
            )
            self.server = server
            with server:
                self.ready.set()
                server.serve_forever()
        except BaseException as exc:  # ruff: ignore[blind-except] - return to test thread
            self.failure = exc
            self.ready.set()

    def join(self, timeout: float | None = None) -> None:
        if self.server is not None:
            self.server.shutdown()
        super().join(timeout)

    def channel(self) -> Channel:
        if self.server is None:
            raise RuntimeError("Server hasn't started")
        if not self.use_tcp:
            return channel_class(self.identifier)
        address = cast("tuple[str, int]", self.server.server_address)
        return tcp_channel_class(str(address[1]))


@fixture
def redirect() -> Redirect:
    return Redirect()


@fixture(params=server_params)
def server(
    redirect: Redirect,
    request: FixtureRequest,
) -> Iterator[Server]:
    use_tcp = bool(request.param)
    identifier = '0' if use_tcp else f'server-{getpid()}'
    thread = Server(identifier, redirect, use_tcp=use_tcp)
    thread.start()
    try:
        assert thread.ready.wait(TEST_TIMEOUT), "Server didn't start in time"
        if thread.failure is not None:
            raise thread.failure
        yield thread
    finally:
        thread.join(TEST_TIMEOUT)
        assert not thread.is_alive(), "Server didn't stop in time"
        if thread.failure is not None:
            raise thread.failure


def test_one_request(redirect: Redirect, server: Server) -> None:
    redirect.prepare(SkillResp('success', 'pong'))
    channel = server.channel()
    try:
        assert channel.send('ping') == 'pong'
        assert redirect.pop() == 'ping'
    finally:
        channel.close()


def test_failed_request(redirect: Redirect, server: Server) -> None:
    redirect.prepare(SkillResp('failure', 'bad expression'))
    channel = server.channel()
    try:
        with raises(RuntimeError, match='bad expression'):
            channel.send('bad()')
        assert redirect.pop() == 'bad()'
    finally:
        channel.close()


def test_invalid_utf8_is_rejected_before_pipe(redirect: Redirect, server: Server) -> None:
    channel = cast("TcpChannel", server.channel())
    channel.socket.settimeout(TEST_TIMEOUT)
    try:
        Socket(channel.socket).send_frame(b'\xff')

        assert Socket(channel.socket).recv_frame() == b'failure <invalid-utf8>'
        with raises(ConnectionError):
            Socket(channel.socket).recv_frame()
        with raises(Empty):
            redirect.pop(0.01)
    finally:
        channel.close()


@mark.parametrize('use_tcp', server_params)
def test_oversized_request_is_rejected_before_pipe(
    redirect: Redirect,
    use_tcp: bool,
) -> None:
    limit = 64
    identifier = '0' if use_tcp else f'server-{getpid()}'
    thread = Server(identifier, redirect, use_tcp=use_tcp, max_payload_size=limit)
    thread.start()
    try:
        assert thread.ready.wait(TEST_TIMEOUT)
        redirect.prepare(SkillResp('success', 'unexpected'))
        channel = cast("TcpChannel", thread.channel())
        channel.socket.settimeout(TEST_TIMEOUT)
        try:
            Socket(channel.socket).send_frame(b'x' * (limit + 1), max_size=10_000)

            assert Socket(channel.socket).recv_frame() == b'failure <request-too-large>'
            with raises(ConnectionError):
                Socket(channel.socket).recv_frame()
            with raises(Empty):
                redirect.pop(0.01)
        finally:
            channel.close()
    finally:
        thread.join(TEST_TIMEOUT)
        assert not thread.is_alive()


@mark.parametrize('use_tcp', server_params)
def test_oversized_response_keeps_connection_for_next_request(
    redirect: Redirect,
    use_tcp: bool,
) -> None:
    limit = 64
    identifier = '0' if use_tcp else f'server-{getpid()}'
    thread = Server(identifier, redirect, use_tcp=use_tcp, max_payload_size=limit)
    thread.start()
    try:
        assert thread.ready.wait(TEST_TIMEOUT)
        redirect.prepare(SkillResp('success', 'x' * limit))
        channel = thread.channel()
        channel.max_transmission_length = 10_000
        try:
            with raises(RuntimeError, match='<response-too-large>'):
                channel.send('large()')
            assert redirect.pop() == 'large()'

            redirect.prepare(SkillResp('success', 'fresh'))
            assert channel.send('next()') == 'fresh'
            assert redirect.pop() == 'next()'
        finally:
            channel.close()
    finally:
        thread.join(TEST_TIMEOUT)
        assert not thread.is_alive()


@mark.parametrize(
    ('failure', 'message'),
    argvalues=[
        (SkillPipeTimeoutError(0.1, phase='SKILL response'), 'Timeout'),
        (SkillPipeDesynchronizedError(), '<desynchronized>'),
        (SkillPipeClosedError(), '<closed>'),
        (SkillPipeBrokenError(), '<pipe-error>'),
    ],
    ids=['timeout', 'desynchronized', 'closed', 'broken'],
)
def test_pipe_error_is_reported(
    redirect: Redirect,
    server: Server,
    failure: Exception,
    message: str,
) -> None:
    redirect.prepare(failure)
    channel = server.channel()
    try:
        with raises(RuntimeError, match=message):
            channel.send('bad()')
        assert redirect.pop() == 'bad()'
    finally:
        channel.close()


def test_timeout_keeps_connection_for_next_request(
    redirect: Redirect,
    server: Server,
) -> None:
    redirect.prepare(SkillPipeTimeoutError(0.1, phase='SKILL response'))
    channel = server.channel()
    try:
        with raises(RuntimeError, match='Timeout'):
            channel.send('slow()')
        assert redirect.pop() == 'slow()'

        redirect.prepare(SkillResp('success', 'fresh'))
        assert channel.send('next()') == 'fresh'
        assert redirect.pop() == 'next()'
    finally:
        channel.close()


def test_windows_factory_uses_tcp_and_preserves_timeout(
    monkeypatch: MonkeyPatch,
    redirect: Redirect,
) -> None:
    monkeypatch.setattr(python_server, 'platform', 'win32')
    server = python_server.create_server(
        '0',
        pipe=cast('Any', redirect),
        single=True,
        timeout=0.25,
        force_tcp=False,
    )
    try:
        assert isinstance(server, python_server.SingleTcpServer)
        assert server.timeout == approx(0.25)
    finally:
        server.server_close()


def test_server_startup_failure_propagates(monkeypatch: MonkeyPatch, redirect: Redirect) -> None:
    def fail_create(*args: object, **kwargs: object) -> None:
        raise OSError("failed to bind address")

    monkeypatch.setattr(python_server, "create_server", fail_create)
    thread = Server('0', redirect, use_tcp=True)
    thread.start()
    assert thread.ready.wait(TEST_TIMEOUT)
    thread.join(TEST_TIMEOUT)
    assert not thread.is_alive()
    assert isinstance(thread.failure, OSError)


def test_restart_acknowledges_client_before_exit(monkeypatch: MonkeyPatch) -> None:
    server_socket, client_socket = socketpair()
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)
    try:
        python_server._respond_to_client(
            Socket(server_socket),
            SkillResp('restart', 'True'),
        )

        assert Socket(client_socket).recv_frame() == b'success True'
        assert exits == [0]
    finally:
        server_socket.close()
        client_socket.close()


def test_restart_exits_when_acknowledgement_fails(monkeypatch: MonkeyPatch) -> None:
    server_socket, client_socket = socketpair()
    sock = Socket(server_socket)
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)

    # On POSIX a sendall() to a closed socketpair peer raises OSError on the
    # first write, but on Windows the first small write is buffered and
    # succeeds, so the failure cannot be induced by closing the peer alone.
    # Inject the failure deterministically: the contract under test is that
    # the daemon still exits even when the acknowledgement send fails.
    def fail_send(*args: object, **kwargs: object) -> None:
        raise OSError("acknowledgement send failed")

    monkeypatch.setattr(Socket, 'send_frame', fail_send)
    try:
        with raises(OSError):
            python_server._respond_to_client(sock, SkillResp('restart', 'True'))
        assert exits == [0]
    finally:
        server_socket.close()
        client_socket.close()


def test_pipe_death_watcher_exits_process(monkeypatch: MonkeyPatch) -> None:
    pipe = SimpleNamespace(wait_peer_closed=lambda: True)
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)

    python_server._watch_pipe_death(cast('Any', pipe))

    assert exits == [0]


def test_pipe_death_watcher_ignores_local_close(monkeypatch: MonkeyPatch) -> None:
    pipe = SimpleNamespace(wait_peer_closed=lambda: False)
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)

    python_server._watch_pipe_death(cast('Any', pipe))

    assert exits == []


def test_create_server_rejects_payload_size_smaller_than_minimum(
    redirect: Redirect,
) -> None:
    with raises(AssertionError, match='max_payload_size must be at least 28 bytes'):
        python_server.create_server(
            '0',
            pipe=cast('Any', redirect),
            single=True,
            timeout=None,
            force_tcp=True,
            max_payload_size=27,
        )


@mark.parametrize('use_tcp', server_params)
def test_close_command_disconnects_client(redirect: Redirect, use_tcp: bool) -> None:
    identifier = '0' if use_tcp else f'server-{getpid()}'
    thread = Server(identifier, redirect, use_tcp=use_tcp)
    thread.start()
    try:
        assert thread.ready.wait(TEST_TIMEOUT)
        channel = cast("TcpChannel", thread.channel())
        try:
            Socket(channel.socket).send_frame(b'$close')
            with raises((ConnectionError, OSError)):
                Socket(channel.socket).recv_frame()
        finally:
            channel.close()
    finally:
        thread.join(TEST_TIMEOUT)
        assert not thread.is_alive()


def test_handler_logs_unexpected_exception(monkeypatch: MonkeyPatch) -> None:
    def raise_err(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(python_server.Handler, "handle_one_request", raise_err)
    logged: list[str] = []
    monkeypatch.setattr(python_server.logger, "exception", logged.append)

    handler = python_server.Handler.__new__(python_server.Handler)
    handler.client_address = ('127.0.0.1', 12345)
    handler.handle()
    assert logged == ["Failed to handle request"]


def test_tcp_server_bind_uses_fast_path_when_available(monkeypatch: MonkeyPatch) -> None:
    ioctls: list[tuple[object, object]] = []
    monkeypatch.setattr(socket_mod, "SIO_LOOPBACK_FAST_PATH", 0x9800001A, raising=False)
    monkeypatch.setattr(
        socket_mod.socket,
        "ioctl",
        lambda _self, cmd, val: ioctls.append((cmd, val)),
        raising=False,
    )
    redirect = Redirect()
    server = python_server.SingleTcpServer(
        '0',
        python_server.Handler,
        pipe=cast('Any', redirect),
        timeout=None,
    )
    try:
        assert (0x9800001A, True) in ioctls
    finally:
        server.server_close()


@mark.parametrize(
    ('cli_args', 'expected_output'),
    [
        (
            [
                "my_server",
                "DEBUG",
                "--notify",
                "--force-tcp",
                "--timeout",
                "1.5",
                "--single",
                "--max-payload-size",
                "1024",
            ],
            "running\n",
        ),
        (["my_server", "INFO"], ""),
    ],
    ids=["with_notify", "without_notify"],
)
def test_main_startup(
    monkeypatch: MonkeyPatch,
    cli_args: list[str],
    expected_output: str,
) -> None:
    served: list[bool] = []
    dummy_server = SimpleNamespace(serve_forever=lambda: served.append(True))
    dummy_pipe = SimpleNamespace(wait_peer_closed=lambda: False)
    monkeypatch.setattr(python_server, "Pipe", lambda *_a, **_kw: nullcontext(dummy_pipe))
    monkeypatch.setattr(
        python_server, "create_server", lambda *_a, **_kw: nullcontext(dummy_server)
    )

    out = io.StringIO()
    monkeypatch.setattr(python_server.stdout, "write", out.write)
    monkeypatch.setattr(python_server.stdout, "flush", lambda: None)

    python_server.cli(cli_args)
    assert served == [True]
    assert out.getvalue() == expected_output


def test_main_startup_configures_file_logging(monkeypatch: MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_setup_logging(*args: object, **kwargs: object) -> None:
        calls.append({'args': args, 'kwargs': kwargs})

    monkeypatch.setattr(python_server, "setup_logging", fake_setup_logging)
    dummy_server = SimpleNamespace(serve_forever=lambda: None)
    dummy_pipe = SimpleNamespace(wait_peer_closed=lambda: False)
    monkeypatch.setattr(python_server, "Pipe", lambda *_a, **_kw: nullcontext(dummy_pipe))
    monkeypatch.setattr(
        python_server, "create_server", lambda *_a, **_kw: nullcontext(dummy_server)
    )
    monkeypatch.setattr(python_server.stdout, "write", lambda _s: None)
    monkeypatch.setattr(python_server.stdout, "flush", lambda: None)

    python_server.cli(["my_server", "WARNING"])

    assert len(calls) == 1
    assert calls[0]['kwargs'] == {
        "level": "WARNING",
        "console": False,
        "file": python_server.LOG_FILE,
    }


def test_import_does_not_configure_root_logger() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import logging; import allegrobridge._kernel.server.python_server; "
                "root = logging.getLogger(); "
                "assert not any(isinstance(h, logging.FileHandler) for h in root.handlers)"
            ),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_cli_handles_keyboard_interrupt(monkeypatch: MonkeyPatch) -> None:
    def raise_keyboard_interrupt(*args: object, **kwargs: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(python_server, "main", raise_keyboard_interrupt)
    python_server.cli(["my_server", "INFO"])


def test_handler_handles_peer_closed(monkeypatch: MonkeyPatch) -> None:
    logged: list[str] = []
    monkeypatch.setattr(python_server.logger, "warning", logged.append)

    server_socket, client_socket = socketpair()
    client_socket.close()
    try:
        handler = python_server.Handler.__new__(python_server.Handler)
        handler.client_address = ('127.0.0.1', 12345)
        handler.request = server_socket
        dummy_server = type("DummyServer", (), {"max_payload_size": 1024})()
        handler.server = cast("python_server.SingleTcpServer", dummy_server)
        assert handler.handle_one_request() is False
        assert any("lost connection" in msg for msg in logged)
    finally:
        server_socket.close()
