from __future__ import annotations

import threading
from collections.abc import Iterator
from os import getpid
from queue import Queue
from socket import socketpair
from socketserver import BaseServer
from typing import cast

from pytest import FixtureRequest, MonkeyPatch, TempPathFactory, fixture, mark, raises

from skillbridge.client.channel import Channel, create_channel_class
from skillbridge.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeTimeoutError,
)
from skillbridge.protocol.response import SkillResp
from skillbridge.protocol.socket import Socket
from skillbridge.server import python_server

TEST_TIMEOUT = 1.0
channel_class = create_channel_class()
tcp_channel_class = create_channel_class(force_tcp=True)


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
    def __init__(self, identifier: str, redirect: Redirect, use_tcp: bool = False) -> None:
        super().__init__(daemon=True)
        self.identifier = identifier
        self.redirect = redirect
        self.use_tcp = use_tcp
        self.server: BaseServer | None = None
        self.ready = threading.Event()
        self.failure: BaseException | None = None

    def run(self) -> None:
        try:
            server = python_server.create_server(
                self.identifier,
                pipe=self.redirect,
                single=False,
                timeout=None,
                force_tcp=self.use_tcp,
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


@fixture(scope='session')
def unix_identifier(tmp_path_factory: TempPathFactory) -> str:
    return f"{tmp_path_factory.mktemp('server').name}-{getpid()}"


@fixture
def server(
    redirect: Redirect,
    request: FixtureRequest,
    unix_identifier: str,
) -> Iterator[Server]:
    use_tcp = bool(request.param)
    identifier = '0' if use_tcp else unix_identifier
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


@mark.parametrize('server', argvalues=[False, True], ids=['unix', 'tcp'], indirect=True)
def test_one_request(redirect: Redirect, server: Server) -> None:
    redirect.prepare(SkillResp('success', 'pong'))
    channel = server.channel()
    try:
        assert channel.send('ping') == 'pong'
        assert redirect.pop() == 'ping'
    finally:
        channel.close()


@mark.parametrize('server', argvalues=[False, True], ids=['unix', 'tcp'], indirect=True)
def test_failed_request(redirect: Redirect, server: Server) -> None:
    redirect.prepare(SkillResp('failure', 'bad expression'))
    channel = server.channel()
    try:
        with raises(RuntimeError, match='bad expression'):
            channel.send('bad()')
        assert redirect.pop() == 'bad()'
    finally:
        channel.close()


@mark.parametrize('server', argvalues=[False, True], ids=['unix', 'tcp'], indirect=True)
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
        python_server._respond_to_client(server_socket, SkillResp('restart', 'True'))

        assert Socket(client_socket).recv_frame() == b'success True'
        assert exits == [0]
    finally:
        server_socket.close()
        client_socket.close()


def test_restart_exits_when_acknowledgement_fails(monkeypatch: MonkeyPatch) -> None:
    server_socket, client_socket = socketpair()
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)
    client_socket.close()
    try:
        with raises(OSError):
            python_server._respond_to_client(server_socket, SkillResp('restart', 'True'))

        assert exits == [0]
    finally:
        server_socket.close()
