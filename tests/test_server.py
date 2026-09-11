# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import errno
import io
import socket as socket_mod
import subprocess
import sys
import textwrap
import threading
from collections.abc import Callable, Iterator
from contextlib import ExitStack, nullcontext
from os import fdopen, getpid, pipe
from pathlib import Path
from queue import Empty, Queue
from socket import socketpair
from socketserver import BaseServer
from sys import platform
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

from pytest import FixtureRequest, MonkeyPatch, approx, fixture, mark, param, raises

from allegrobridge._kernel.client.channel import Channel, TcpChannel, create_channel_class
from allegrobridge._kernel.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeInvalidCommandError,
    SkillPipeTimeoutError,
)
from allegrobridge._kernel.protocol.response import Response, SkillResp
from allegrobridge._kernel.protocol.socket import DEFAULT_MAX_PAYLOAD_SIZE, Socket
from allegrobridge._kernel.server import python_server
from allegrobridge._kernel.server._pipe import Pipe

TEST_TIMEOUT = 1.0
channel_class = create_channel_class()
tcp_channel_class = create_channel_class(force_tcp=True)
server_params = (
    [param(True, id='tcp')]
    if platform == 'win32'
    else [param(False, id='unix'), param(True, id='tcp')]
)
unix_server_classes = tuple(
    cls
    for cls in (
        getattr(python_server, 'SingleUnixServer', None),
        getattr(python_server, 'ThreadingUnixServer', None),
    )
    if cls is not None
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


@fixture
def unix_endpoint() -> Iterator[tuple[str, Path]]:
    identifier = f'u{uuid4().hex[:10]}'
    path = Path(f'/tmp/skill-server-{identifier}.sock')
    lock_path = Path(f'{path}.lock')
    try:
        yield identifier, path
    finally:
        path.unlink(missing_ok=True)
        lock_path.unlink(missing_ok=True)


@fixture(params=unix_server_classes, ids=lambda cls: cls.__name__)
def unix_server_cls(request: FixtureRequest) -> type[BaseServer]:
    return request.param


@fixture
def managed_unix_server(
    unix_endpoint: tuple[str, Path],
) -> Iterator[Callable[[type[BaseServer]], BaseServer]]:
    identifier, _ = unix_endpoint
    with ExitStack() as stack:

        def create(server_cls: type[BaseServer]) -> BaseServer:
            server = cast('Any', server_cls)(
                identifier, python_server.Handler, pipe=cast('Pipe', Redirect()), timeout=None
            )
            stack.callback(server.server_close)
            return server

        yield create


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
        if not use_tcp:
            Path(f'/tmp/skill-server-{thread.identifier}.sock.lock').unlink(missing_ok=True)
        if thread.failure is not None:
            raise thread.failure


@mark.skipif(not unix_server_classes, reason='Unix domain sockets unavailable')
class TestUnixOwnership:
    def test_unix_active_endpoint_is_not_unlinked(
        self,
        unix_server_cls: type[BaseServer],
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        _, path = unix_endpoint
        first = managed_unix_server(unix_server_cls)
        try:
            with raises(OSError) as caught:
                managed_unix_server(unix_server_cls)
            assert caught.value.errno == errno.EADDRINUSE
            assert path.exists()
            with socket_mod.socket(socket_mod.AF_UNIX, socket_mod.SOCK_STREAM) as probe:
                probe.settimeout(TEST_TIMEOUT)
                probe.connect(str(path))
        finally:
            first.server_close()

        assert not path.exists()

    def test_unix_foreign_active_listener_is_not_unlinked(
        self,
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        _, path = unix_endpoint
        with socket_mod.socket(socket_mod.AF_UNIX, socket_mod.SOCK_STREAM) as listener:
            listener.bind(str(path))
            listener.listen(1)
            with raises(OSError) as caught:
                managed_unix_server(python_server.SingleUnixServer)
            assert caught.value.errno == errno.EADDRINUSE
            assert path.exists()

    def test_unix_stale_socket_is_reclaimed(
        self,
        unix_server_cls: type[BaseServer],
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        _, path = unix_endpoint
        with socket_mod.socket(socket_mod.AF_UNIX, socket_mod.SOCK_STREAM) as stale:
            stale.bind(str(path))
            stale.listen(1)

        server = managed_unix_server(unix_server_cls)
        try:
            assert path.exists()
            with socket_mod.socket(socket_mod.AF_UNIX, socket_mod.SOCK_STREAM) as probe:
                probe.settimeout(TEST_TIMEOUT)
                probe.connect(str(path))
        finally:
            server.server_close()
        assert not path.exists()

    @mark.parametrize('kind', ['file', 'symlink'])
    def test_unix_non_socket_path_is_preserved(
        self,
        kind: str,
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        _, path = unix_endpoint
        target = path.with_name(f'{path.name}-target')
        if kind == 'file':
            path.write_text('owned by test')
        else:
            path.symlink_to(target)

        with raises(OSError) as caught:
            managed_unix_server(python_server.SingleUnixServer)
        assert caught.value.errno == errno.EADDRINUSE
        assert path.is_symlink() if kind == 'symlink' else path.read_text() == 'owned by test'

    def test_unix_old_close_preserves_replacement(
        self,
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        _, path = unix_endpoint
        replacement_path = path.with_name(f'{path.name}-replacement')
        first = managed_unix_server(python_server.SingleUnixServer)
        try:
            with socket_mod.socket(socket_mod.AF_UNIX, socket_mod.SOCK_STREAM) as replacement:
                replacement.bind(str(replacement_path))
                replacement.listen(1)
                Path(replacement_path).replace(path)
                replacement_identity = (path.stat().st_dev, path.stat().st_ino)
            first.server_close()
            current = path.stat()
            assert (current.st_dev, current.st_ino) == replacement_identity
            replacement_server = managed_unix_server(python_server.SingleUnixServer)
            assert path.exists()
            first.server_close()
            assert path.exists()
            replacement_server.server_close()
        finally:
            first.server_close()
            replacement_path.unlink(missing_ok=True)

    def test_unix_failed_activate_releases_lock(
        self,
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        _, path = unix_endpoint

        class FailingServer(python_server.SingleUnixServer):
            def server_activate(self) -> None:
                raise RuntimeError('activate failed')

        with raises(RuntimeError, match='activate failed'):
            managed_unix_server(FailingServer)

        server = managed_unix_server(python_server.SingleUnixServer)
        server.server_close()
        assert not path.exists()

    def test_unix_lock_covers_bind_before_listen(
        self,
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        identifier, path = unix_endpoint
        entered = threading.Event()
        release = threading.Event()
        created: list[BaseServer] = []
        failures: list[BaseException] = []

        class PausedServer(python_server.SingleUnixServer):
            def server_activate(self) -> None:
                entered.set()
                if not release.wait(TEST_TIMEOUT):
                    raise TimeoutError('activate was not released')
                super().server_activate()

        def create() -> None:
            try:
                created.append(
                    PausedServer(
                        identifier,
                        python_server.Handler,
                        pipe=cast('Pipe', Redirect()),
                        timeout=None,
                    )
                )
            except BaseException as exc:  # ruff: ignore[blind-except] - return to test thread
                failures.append(exc)

        thread = threading.Thread(target=create)
        thread.start()
        try:
            assert entered.wait(TEST_TIMEOUT)
            with raises(OSError) as caught:
                managed_unix_server(python_server.SingleUnixServer)
            assert caught.value.errno == errno.EADDRINUSE
        finally:
            release.set()
            thread.join(TEST_TIMEOUT)
            for server in created:
                server.server_close()
            assert not thread.is_alive()
            assert not failures
        assert not path.exists()

    def test_unix_crash_leaves_reclaimable_socket(
        self,
        unix_endpoint: tuple[str, Path],
        managed_unix_server: Callable[[type[BaseServer]], BaseServer],
    ) -> None:
        identifier, path = unix_endpoint
        script = textwrap.dedent(f"""\
        import os
        from allegrobridge._kernel.server import python_server
        from allegrobridge._kernel.server.python_server import Handler
        class P:
            def execute(self, command, timeout=None):
                return None
        python_server.SingleUnixServer({identifier!r}, Handler, pipe=P(), timeout=None)
        os._exit(0)
        """)
        result = subprocess.run([sys.executable, '-c', script], timeout=TEST_TIMEOUT, check=False)
        assert result.returncode == 0
        assert path.exists()

        server = managed_unix_server(python_server.SingleUnixServer)
        server.server_close()
        assert not path.exists()


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
        (SkillPipeInvalidCommandError(), '<invalid-command>'),
    ],
    ids=['timeout', 'desynchronized', 'closed', 'broken', 'invalid-command'],
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


def test_restart_acknowledges_client_without_exit_side_effect(
    monkeypatch: MonkeyPatch,
) -> None:
    server_socket, client_socket = socketpair()
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)
    try:
        python_server._respond_to_client(
            Socket(server_socket),
            SkillResp('restart', 'True'),
        )

        assert Socket(client_socket).recv_frame() == b'success True'
        assert exits == []
    finally:
        server_socket.close()
        client_socket.close()


def test_restart_acknowledgement_failure_propagates(monkeypatch: MonkeyPatch) -> None:
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
        assert exits == []
    finally:
        server_socket.close()
        client_socket.close()


def test_pipe_death_watcher_exits_process(monkeypatch: MonkeyPatch) -> None:
    pipe = SimpleNamespace(wait_peer_closed=lambda: True)
    tracker = python_server._RequestTracker()
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)

    python_server._watch_pipe_death(cast('Any', pipe), tracker)

    assert exits == [0]


def test_pipe_death_watcher_ignores_local_close(monkeypatch: MonkeyPatch) -> None:
    pipe = SimpleNamespace(wait_peer_closed=lambda: False)
    tracker = python_server._RequestTracker()
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)

    python_server._watch_pipe_death(cast('Any', pipe), tracker)

    assert exits == []


def test_request_tracker_waits_for_active_request() -> None:
    tracker = python_server._RequestTracker()
    assert tracker.start()
    assert not tracker.stop_and_wait(0.0)
    assert not tracker.start()

    tracker.finish()
    assert tracker.stop_and_wait(TEST_TIMEOUT)


@mark.parametrize(
    ('status', 'ack_fails'),
    [('success', False), ('restart', False), ('restart', True)],
    ids=['success', 'restart', 'restart-ack-failure'],
)
def test_watcher_waits_for_handler_ack_before_exit(
    monkeypatch: MonkeyPatch, status: str, ack_fails: bool
) -> None:
    case = _WatcherAckCase(monkeypatch, status, ack_fails)
    try:
        case.run()
    finally:
        case.close()


class _WatcherAckCase:
    def __init__(self, monkeypatch: MonkeyPatch, status: str, ack_fails: bool) -> None:
        self.status = status
        self.ack_fails = ack_fails
        self.response_read_fd, response_write_fd = pipe()
        self.response_reader = fdopen(self.response_read_fd, 'r', encoding='utf-8', newline='')
        self.response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')
        self.command_written = threading.Event()
        self.skill_pipe = Pipe(self.response_reader, self._command_writer())
        self.tracker = python_server._RequestTracker()
        self.server_socket, self.client_socket = socketpair()
        self.server_socket.settimeout(TEST_TIMEOUT)
        self.client_socket.settimeout(TEST_TIMEOUT)
        self.ack_entered = threading.Event()
        self.release_ack = threading.Event()
        self.stop_entered = threading.Event()
        self.handler_outcome: list[Exception | bool] = []
        self.exits: list[int] = []
        dummy_server = SimpleNamespace(
            max_payload_size=DEFAULT_MAX_PAYLOAD_SIZE,
            pipe=self.skill_pipe,
            timeout=TEST_TIMEOUT,
            request_tracker=self.tracker,
        )
        self.handler = python_server.Handler.__new__(python_server.Handler)
        self.handler.client_address = ('127.0.0.1', 12345)
        self.handler.request = self.server_socket
        self.handler.server = cast('python_server.SingleTcpServer', dummy_server)
        original_respond = python_server._respond_to_client

        def delayed_respond(sock: Socket, response: SkillResp) -> None:
            self.ack_entered.set()
            assert self.release_ack.wait(TEST_TIMEOUT)
            if self.ack_fails:
                raise OSError('acknowledgement send failed')
            original_respond(sock, response)

        monkeypatch.setattr(python_server, '_respond_to_client', delayed_respond)
        monkeypatch.setattr(python_server.os, '_exit', self.exits.append)
        original_stop = self.tracker.stop_and_wait
        monkeypatch.setattr(
            self.tracker,
            'stop_and_wait',
            lambda timeout: self._tracked_stop(original_stop, timeout),
        )
        self.request: threading.Thread | None = None
        self.watcher: threading.Thread | None = None

    def _command_writer(self) -> io.StringIO:
        case = self

        class CommandWriter(io.StringIO):
            def write(self, value: str) -> int:
                written = super().write(value)
                if value.endswith('\n'):
                    case.command_written.set()
                return written

        return CommandWriter()

    def _tracked_stop(self, original_stop: object, timeout: float) -> bool:
        self.stop_entered.set()
        return cast('Any', original_stop)(timeout)

    def run(self) -> None:
        def handle() -> None:
            try:
                self.handler_outcome.append(self.handler.handle_one_request())
            except OSError as exc:
                self.handler_outcome.append(exc)

        self.request = threading.Thread(target=handle)
        self.request.start()
        Socket(self.client_socket).send_frame(b'ping()')
        assert self.command_written.wait(TEST_TIMEOUT)
        marker = Response.RST if self.status == 'restart' else Response.STX
        payload = 'True' if self.status == 'restart' else 'pong'
        self.response_writer.write(marker + payload + Response.RS)
        self.response_writer.flush()
        assert self.ack_entered.wait(TEST_TIMEOUT)
        self.response_writer.close()
        self.watcher = threading.Thread(
            target=python_server._watch_pipe_death,
            args=(self.skill_pipe, self.tracker),
            kwargs={'grace': TEST_TIMEOUT},
        )
        self.watcher.start()
        assert self.stop_entered.wait(TEST_TIMEOUT)
        assert self.exits == []
        self.release_ack.set()
        self.request.join(TEST_TIMEOUT)
        self.watcher.join(TEST_TIMEOUT)
        assert not self.request.is_alive()
        assert not self.watcher.is_alive()
        assert self.exits == [0]
        if self.ack_fails:
            assert isinstance(self.handler_outcome[0], OSError)
        else:
            assert self.handler_outcome == [self.status != 'restart']
            assert Socket(self.client_socket).recv_frame() == f'success {payload}'.encode()

    def close(self) -> None:
        self.release_ack.set()
        self.response_writer.close()
        if self.request is not None:
            self.request.join(TEST_TIMEOUT)
        if self.watcher is not None:
            self.watcher.join(TEST_TIMEOUT)
        self.client_socket.close()
        self.server_socket.close()
        self.skill_pipe.close()
        assert self.request is None or not self.request.is_alive()
        assert self.watcher is None or not self.watcher.is_alive()
        assert self.skill_pipe.wait_closed(TEST_TIMEOUT)


def test_pipe_death_watcher_exits_after_grace(monkeypatch: MonkeyPatch) -> None:
    pipe = SimpleNamespace(wait_peer_closed=lambda: True)
    tracker = python_server._RequestTracker()
    assert tracker.start()
    exits: list[int] = []
    monkeypatch.setattr(python_server.os, '_exit', exits.append)

    python_server._watch_pipe_death(cast('Any', pipe), tracker, grace=0.0)

    assert exits == [0]
    tracker.finish()


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
    dummy_server = SimpleNamespace(
        serve_forever=lambda: served.append(True),
        request_tracker=python_server._RequestTracker(),
    )
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
    dummy_server = SimpleNamespace(
        serve_forever=lambda: None,
        request_tracker=python_server._RequestTracker(),
    )
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
