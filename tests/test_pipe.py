"""Test framework for Pipe; see ``skillbridge/server/SECRET.md`` for its design."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Iterator
from io import StringIO, TextIOWrapper
from os import fdopen, pipe
from queue import Empty, Queue

from pytest import MonkeyPatch, fixture, mark, raises

from skillbridge.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeTimeoutError,
)
from skillbridge.protocol.response import Response, RespStatus, SkillResp
from skillbridge.server._pipe import (  # ruff: ignore[import-private-name]
    Pipe,
    _PipeState,
    _StateMachine,
)

TEST_TIMEOUT = 1.0


class Client(threading.Thread):
    def __init__(
        self,
        request: Callable[[], SkillResp],
        *,
        name: str = 'mock-client',
    ) -> None:
        super().__init__(name=name, daemon=True)
        self._request = request
        self._outcome: Queue[SkillResp | Exception] = Queue(maxsize=1)
        self.started = threading.Event()

    def run(self) -> None:
        self.started.set()
        try:
            outcome: SkillResp | Exception = self._request()
        except Exception as exc:  # ruff: ignore[blind-except] - propagate to test thread
            outcome = exc
        self._outcome.put(outcome)

    def result(self, timeout: float = TEST_TIMEOUT) -> SkillResp:
        self.join(timeout)
        if self.is_alive():
            raise TimeoutError("mock client did not stop")
        outcome = self._outcome.get_nowait()
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class Server:
    def __init__(self, command_reader: TextIOWrapper, response_writer: TextIOWrapper) -> None:
        self._command_reader = command_reader
        self._response_writer = response_writer
        self._commands: Queue[str | None] = Queue()
        self._write_lock = threading.Lock()
        self._thread = threading.Thread(
            target=self._collect_commands,
            name='mock-skill-server',
            daemon=True,
        )
        self._thread.start()

    def _collect_commands(self) -> None:
        try:
            for command in self._command_reader:
                self._commands.put(command[:-1] if command.endswith('\n') else command)
        finally:
            self._commands.put(None)
            self._response_writer.close()

    def recv(self, timeout: float = TEST_TIMEOUT) -> str:
        command = self._commands.get(timeout=timeout)
        if command is None:
            raise EOFError("Pipe closed its command stream")
        return command

    def respond(self, payload: str, *, status: RespStatus = 'success') -> None:
        marker = {
            'success': Response.STX,
            'failure': Response.NAK,
            'restart': Response.RST,
        }[status]
        with self._write_lock:
            self._response_writer.write(marker + payload + Response.RS)
            self._response_writer.flush()

    def respond_when(
        self,
        release: threading.Event,
        payload: str,
        *,
        status: RespStatus = 'success',
        timeout: float = TEST_TIMEOUT,
    ) -> None:
        # mock slow skill execution
        if not release.wait(timeout):
            raise TimeoutError("mock SKILL execution was not released")
        self.respond(payload, status=status)

    def disconnect_response(self) -> None:
        self._response_writer.close()

    def close(self) -> None:
        self._response_writer.close()
        self._thread.join(TEST_TIMEOUT)
        if self._thread.is_alive():
            raise RuntimeError("mock SKILL server did not stop")
        self._command_reader.close()


class FailingWriter(StringIO):
    def write(self, value: str) -> int:
        del value
        raise OSError('writer stopped')


class BlockingWriter(FailingWriter):
    def __init__(self) -> None:
        super().__init__()
        self.entered = threading.Event()
        self._release = threading.Event()

    def write(self, value: str) -> int:
        self.entered.set()
        if not self._release.wait(TEST_TIMEOUT):
            raise TimeoutError('writer was not released')
        return super().write(value)

    def close(self) -> None:
        self._release.set()
        super().close()


def assert_pipe_state(channel: Pipe, expected: _PipeState) -> None:
    assert channel.state is expected


@fixture
def skill_pipe_factory() -> Iterator[Callable[[float | None], tuple[Pipe, Server]]]:
    resources: list[tuple[Pipe, Server, TextIOWrapper]] = []

    def create(drain_timeout: float | None = 30.0) -> tuple[Pipe, Server]:
        command_read_fd, command_write_fd = pipe()
        response_read_fd, response_write_fd = pipe()
        command_reader = fdopen(command_read_fd, encoding='utf-8', newline='')
        command_writer = fdopen(command_write_fd, 'w', encoding='utf-8', newline='')
        response_reader = fdopen(response_read_fd, encoding='utf-8', newline='')
        response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')
        server = Server(command_reader, response_writer)
        channel = Pipe(response_reader, command_writer, drain_timeout=drain_timeout)
        resources.append((channel, server, response_reader))
        return channel, server

    try:
        yield create
    finally:
        for channel, server, response_reader in resources:
            channel.close()
            try:
                server.close()
            finally:
                assert channel.wait_closed(TEST_TIMEOUT)
                response_reader.close()


@fixture
def skill_pipe(
    skill_pipe_factory: Callable[[float | None], tuple[Pipe, Server]],
) -> tuple[Pipe, Server]:
    return skill_pipe_factory(30.0)


@fixture
def channel_factory() -> Iterator[Callable[[StringIO], Pipe]]:
    resources: list[tuple[Pipe, TextIOWrapper]] = []

    def create(writer: StringIO) -> Pipe:
        response_read_fd, response_write_fd = pipe()
        response_reader = fdopen(response_read_fd, encoding='utf-8', newline='')
        response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')
        channel = Pipe(response_reader, writer)
        resources.append((channel, response_writer))
        return channel

    try:
        yield create
    finally:
        for channel, response_writer in resources:
            channel.close()
            response_writer.close()
            assert channel.wait_closed(TEST_TIMEOUT)


class TestStateMachine:
    def test_delivers_response_and_returns_to_ready(self) -> None:
        machine = _StateMachine(drain_timeout=None)
        response = SkillResp('success', 'done')

        machine.begin(timeout=None, deadline=None)
        machine.publish(response)

        assert machine.wait_response(timeout=None, deadline=None) == response
        assert machine.state is _PipeState.READY

    def test_close_is_idempotent_and_rejects_requests(self) -> None:
        machine = _StateMachine(drain_timeout=None)

        assert machine.close()
        assert machine.state is _PipeState.CLOSED
        assert not machine.close()
        assert not machine.wait_until_ready(0.0)
        machine.publish(SkillResp('success', 'ignored'))
        with raises(SkillPipeClosedError):
            machine.begin(timeout=None, deadline=None)

    def test_unexpected_response_desynchronizes_pipe(self) -> None:
        machine = _StateMachine(drain_timeout=None)

        machine.publish(SkillResp('success', 'unexpected'))
        machine.publish(SkillResp('success', 'ignored'))

        assert machine.state is _PipeState.DESYNCHRONIZED
        with raises(SkillPipeDesynchronizedError) as caught:
            machine.begin(timeout=None, deadline=None)
        assert isinstance(caught.value.__cause__, SkillPipeDesynchronizedError)

    def test_additional_response_interrupts_current_request(self) -> None:
        machine = _StateMachine(drain_timeout=None)
        machine.begin(timeout=None, deadline=None)
        machine.publish(SkillResp('success', 'first'))

        machine.publish(SkillResp('success', 'additional'))

        with raises(SkillPipeDesynchronizedError):
            machine.wait_response(timeout=None, deadline=None)

    def test_late_response_restores_ready_state(self) -> None:
        machine = _StateMachine(drain_timeout=None)
        machine.begin(timeout=0.0, deadline=time.monotonic())

        with raises(SkillPipeTimeoutError):
            machine.wait_response(timeout=0.0, deadline=time.monotonic())

        assert not machine.wait_until_ready(0.0)
        machine.publish(SkillResp('success', 'late'))
        assert machine.wait_until_ready(TEST_TIMEOUT)

    def test_stale_drain_watchdog_does_not_change_ready_state(self) -> None:
        machine = _StateMachine(drain_timeout=None)

        machine._expire_drain()

        assert machine.state is _PipeState.READY


@mark.integration
def test_execute_roundtrip_with_multiline_payload(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute('ping()', timeout=TEST_TIMEOUT))
    client.start()

    assert server.recv() == 'ping()'
    server.respond('line one\nline two')

    assert client.result() == SkillResp('success', 'line one\nline two')
    assert channel.state is _PipeState.READY


@mark.integration
def test_execute_preserves_existing_newline(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute('ping()\n', timeout=TEST_TIMEOUT))
    client.start()

    assert server.recv() == 'ping()'
    server.respond('pong')

    assert client.result() == SkillResp('success', 'pong')


@mark.integration
def test_failure_response_does_not_poison_channel(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    failed_client = Client(lambda: channel.execute('bad()', timeout=TEST_TIMEOUT))
    failed_client.start()

    assert server.recv() == 'bad()'
    server.respond('bad expression', status='failure')

    assert failed_client.result() == SkillResp('failure', 'bad expression')
    assert channel.state is _PipeState.READY

    next_client = Client(lambda: channel.execute('good()', timeout=TEST_TIMEOUT))
    next_client.start()
    assert server.recv() == 'good()'
    server.respond('ok')

    assert next_client.result() == SkillResp('success', 'ok')
    assert channel.state is _PipeState.READY


@mark.integration
def test_execute_serializes_clients(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    first_client = Client(
        lambda: channel.execute('first()', timeout=TEST_TIMEOUT),
        name='mock-client-first',
    )
    second_client = Client(
        lambda: channel.execute('second()', timeout=TEST_TIMEOUT),
        name='mock-client-second',
    )

    first_client.start()
    assert server.recv() == 'first()'

    second_client.start()
    assert second_client.started.wait(TEST_TIMEOUT)
    with raises(Empty):
        server.recv(timeout=0.05)

    server.respond('response:first')
    assert first_client.result() == SkillResp('success', 'response:first')

    assert server.recv() == 'second()'
    server.respond('response:second')
    assert second_client.result() == SkillResp('success', 'response:second')


@mark.integration
def test_restart_closes_before_next_client_can_write(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    restarting = Client(lambda: channel.execute('restart()', timeout=TEST_TIMEOUT))
    waiting = Client(lambda: channel.execute('next()', timeout=TEST_TIMEOUT))

    restarting.start()
    assert server.recv() == 'restart()'

    waiting.start()
    assert waiting.started.wait(TEST_TIMEOUT)
    with raises(Empty):
        server.recv(timeout=0.05)

    server.respond('True', status='restart')

    assert restarting.result() == SkillResp('restart', 'True')
    with raises(SkillPipeClosedError):
        waiting.result()
    assert_pipe_state(channel, _PipeState.CLOSED)
    with raises(EOFError):
        server.recv()


@mark.integration
def test_serialization_timeout_does_not_send_command(
    skill_pipe: tuple[Pipe, Server],
) -> None:
    channel, server = skill_pipe
    first_client = Client(lambda: channel.execute('first()', timeout=TEST_TIMEOUT))
    first_client.start()
    assert server.recv() == 'first()'

    with raises(SkillPipeTimeoutError) as caught:
        channel.execute('blocked()', timeout=0.0)
    assert caught.value.phase == 'serialization'
    assert_pipe_state(channel, _PipeState.EXECUTING)
    with raises(Empty):
        server.recv(timeout=0.05)

    server.respond('done')
    assert first_client.result() == SkillResp('success', 'done')
    assert_pipe_state(channel, _PipeState.READY)


@mark.integration
def test_zero_timeout_does_not_send_command(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe

    with raises(SkillPipeTimeoutError):
        channel.execute('expired()', timeout=0.0)

    with raises(Empty):
        server.recv(timeout=0.05)


@mark.integration
def test_late_response_is_drained(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    slow_client = Client(lambda: channel.execute('slow()', timeout=0.05))
    slow_client.start()
    assert server.recv() == 'slow()'

    with raises(SkillPipeTimeoutError):
        slow_client.result()
    assert channel.state is _PipeState.DRAINING

    server.respond('late')
    assert channel.wait_until_ready(TEST_TIMEOUT)

    next_client = Client(lambda: channel.execute('next()', timeout=TEST_TIMEOUT))
    next_client.start()
    assert server.recv() == 'next()'
    server.respond('fresh')

    assert next_client.result() == SkillResp('success', 'fresh')


@mark.integration
def test_next_request_waits_for_late_response_before_writing(
    skill_pipe: tuple[Pipe, Server],
) -> None:
    channel, server = skill_pipe
    slow_client = Client(lambda: channel.execute('slow()', timeout=0.05))
    slow_client.start()
    assert server.recv() == 'slow()'
    with raises(SkillPipeTimeoutError):
        slow_client.result()

    next_client = Client(lambda: channel.execute('next()', timeout=TEST_TIMEOUT))
    next_client.start()
    assert next_client.started.wait(TEST_TIMEOUT)
    with raises(Empty):
        server.recv(timeout=0.05)

    server.respond('stale')
    assert server.recv() == 'next()'
    server.respond('fresh')

    assert next_client.result() == SkillResp('success', 'fresh')


@mark.integration
def test_request_deadline_can_expire_while_waiting_for_recovery(
    skill_pipe: tuple[Pipe, Server],
) -> None:
    channel, server = skill_pipe
    slow_client = Client(lambda: channel.execute('slow()', timeout=0.05))
    slow_client.start()
    assert server.recv() == 'slow()'
    with raises(SkillPipeTimeoutError):
        slow_client.result()

    with raises(SkillPipeTimeoutError) as caught:
        channel.execute('next()', timeout=0.05)

    assert caught.value.phase == 'timeout recovery'
    assert channel.state is _PipeState.DRAINING
    with raises(Empty):
        server.recv(timeout=0.05)


@mark.integration
def test_drain_watchdog_desynchronizes_future_requests(
    skill_pipe_factory: Callable[[float | None], tuple[Pipe, Server]],
) -> None:
    channel, server = skill_pipe_factory(0.0)
    client = Client(lambda: channel.execute('never_returns()', timeout=0.05))
    client.start()
    assert server.recv() == 'never_returns()'
    with raises(SkillPipeTimeoutError):
        client.result()

    assert not channel.wait_until_ready(TEST_TIMEOUT)
    assert channel.state is _PipeState.DESYNCHRONIZED
    with raises(SkillPipeDesynchronizedError):
        channel.execute('next()', timeout=TEST_TIMEOUT)


@mark.integration
def test_owned_close_stops_reader_after_peer_eof(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, _ = skill_pipe

    channel.close()

    assert channel.wait_closed(TEST_TIMEOUT)


@mark.integration
def test_close_wakes_executing_client(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute('wait()', timeout=None))
    client.start()
    assert server.recv() == 'wait()'

    channel.close()

    with raises(SkillPipeClosedError):
        client.result()


@mark.integration
def test_reader_eof_breaks_current_request(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute('read()', timeout=TEST_TIMEOUT))
    client.start()
    assert server.recv() == 'read()'

    server.disconnect_response()

    with raises(SkillPipeBrokenError):
        client.result()
    assert channel.state is _PipeState.BROKEN


@mark.integration
def test_response_before_reader_eof_is_delivered(
    skill_pipe: tuple[Pipe, Server],
) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute('first()', timeout=TEST_TIMEOUT))
    client.start()
    assert server.recv() == 'first()'

    server.respond('valid payload')
    server.disconnect_response()

    assert client.result() == SkillResp('success', 'valid payload')
    with raises(SkillPipeBrokenError):
        channel.execute('second()', timeout=TEST_TIMEOUT)
    assert channel.state is _PipeState.BROKEN


@mark.integration
def test_response_published_at_deadline_is_delivered(
    skill_pipe: tuple[Pipe, Server],
    monkeypatch: MonkeyPatch,
) -> None:
    channel, server = skill_pipe
    current_time = 100.0
    monkeypatch.setattr(time, 'monotonic', lambda: current_time)
    client = Client(lambda: channel.execute('race()', timeout=1.0))
    client.start()
    assert server.recv() == 'race()'

    current_time = 102.0
    server.respond('exact boundary')

    assert client.result() == SkillResp('success', 'exact boundary')
    assert channel.state is _PipeState.READY


@mark.parametrize('timeout', [-1.0, float('inf'), float('nan')])
def test_invalid_timeout_is_rejected(timeout: float) -> None:
    channel = Pipe(StringIO(), StringIO())
    assert channel.wait_closed(TEST_TIMEOUT)

    try:
        with raises(ValueError):
            channel.execute('invalid()', timeout=timeout)
    finally:
        channel.close()


def test_write_failure_breaks_pipe(channel_factory: Callable[[StringIO], Pipe]) -> None:
    channel = channel_factory(FailingWriter())

    with raises(SkillPipeBrokenError):
        channel.execute('fail()', timeout=TEST_TIMEOUT)

    assert channel.state is _PipeState.BROKEN


def test_close_interrupts_blocked_write(channel_factory: Callable[[StringIO], Pipe]) -> None:
    writer = BlockingWriter()
    channel = channel_factory(writer)
    client = Client(lambda: channel.execute('blocked()', timeout=None))
    client.start()
    assert writer.entered.wait(TEST_TIMEOUT)

    channel.close()

    with raises(SkillPipeClosedError):
        client.result()


def test_close_closes_streams() -> None:
    reader = StringIO()
    writer = StringIO()
    channel = Pipe(reader, writer)
    assert channel.wait_closed(TEST_TIMEOUT)

    channel.close()

    assert reader.closed
    assert writer.closed


def test_context_manager_closes_pipe() -> None:
    reader = StringIO()
    writer = StringIO()

    with Pipe(reader, writer) as channel:
        assert channel.state in {_PipeState.READY, _PipeState.BROKEN}

    assert channel.state is _PipeState.CLOSED
