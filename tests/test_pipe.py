# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test framework for Pipe; see ``allegrobridge/_kernel/server/SECRET.md`` for its design."""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from io import BufferedWriter, StringIO, TextIOWrapper
from os import fdopen, pipe
from queue import Empty, Queue
from typing import BinaryIO

from pytest import MonkeyPatch, fixture, mark, raises

from allegrobridge._kernel.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeInvalidCommandError,
    SkillPipeTimeoutError,
)
from allegrobridge._kernel.protocol.response import Response, RespStatus, SkillResp
from allegrobridge._kernel.server._pipe import (
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
                self._commands.put(command.removesuffix('\n'))
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

    def release(self) -> None:
        self._release.set()

    def close(self) -> None:
        self.release()
        super().close()


class GatedPipeWriter(TextIOWrapper):
    def __init__(self, binary_writer: BufferedWriter, phase: str) -> None:
        super().__init__(binary_writer, encoding='utf-8', newline='')
        self.entered = threading.Event()
        self._phase = phase

    def write(self, value: str) -> int:
        if self._phase == 'write':
            self.entered.set()
        return super().write(value)

    def flush(self) -> None:
        if self._phase == 'flush':
            self.entered.set()
        super().flush()


@dataclass
class BlockedPipe:
    channel: Pipe
    command_writer: GatedPipeWriter
    command_reader: BinaryIO
    response_writer: TextIOWrapper
    threads: list[threading.Thread] = field(default_factory=list)
    errors: list[BaseException] = field(default_factory=list)


def assert_pipe_state(channel: Pipe, expected: _PipeState) -> None:
    assert channel.state is expected


def start_drainer(
    resource: BlockedPipe, expected: bytes
) -> tuple[threading.Thread, list[BaseException]]:
    errors = resource.errors

    def read_expected() -> None:
        chunks: list[bytes] = []
        remaining = len(expected)
        while remaining:
            chunk = resource.command_reader.read(remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        if b''.join(chunks) != expected:
            raise AssertionError('command stream was not drained exactly')

    def drain() -> None:
        try:
            read_expected()
        except BaseException as exc:  # ruff: ignore[blind-except] - propagate test thread failure
            errors.append(exc)

    thread = threading.Thread(target=drain, daemon=True)
    resource.threads.append(thread)
    thread.start()
    return thread, errors


def start_thread(resource: BlockedPipe, thread: threading.Thread) -> None:
    resource.threads.append(thread)
    thread.start()


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


@fixture
def blocked_pipe() -> Iterator[Callable[[str], BlockedPipe]]:
    resources: list[BlockedPipe] = []

    def create(phase: str) -> BlockedPipe:
        command_read_fd, command_write_fd = pipe()
        response_read_fd, response_write_fd = pipe()
        raw_writer = os.fdopen(command_write_fd, 'wb', buffering=0)
        command_writer = GatedPipeWriter(
            BufferedWriter(
                raw_writer,
                buffer_size=8192 if phase == 'write' else 16 * 1024 * 1024,
            ),
            phase,
        )
        command_reader = os.fdopen(command_read_fd, 'rb', buffering=0)
        response_reader = fdopen(response_read_fd, encoding='utf-8', newline='')
        response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')
        channel = Pipe(response_reader, command_writer)
        resource = BlockedPipe(channel, command_writer, command_reader, response_writer)
        resources.append(resource)
        return resource

    try:
        yield create
    finally:
        for resource in resources:
            resource.command_reader.close()
            channel = resource.channel
            command_writer = resource.command_writer
            response_writer = resource.response_writer
            if not response_writer.closed:
                response_writer.close()
            channel.close()
            assert channel.wait_closed(TEST_TIMEOUT)
            if not command_writer.closed:
                command_writer.close()
            for thread in resource.threads:
                thread.join(TEST_TIMEOUT)
                assert not thread.is_alive()
            assert not resource.errors


class TestStateMachine:
    def test_delivers_response_and_returns_to_ready(self) -> None:
        machine = _StateMachine(drain_timeout=None)
        response = SkillResp('success', 'done')

        machine.begin(timeout=None, deadline=None)
        machine.publish(response)

        assert machine.wait_response(timeout=None, deadline=None) == response
        assert machine.state is _PipeState.READY

    def test_write_failure_wins_over_early_response(self) -> None:
        machine = _StateMachine(drain_timeout=None)
        response = SkillResp('success', 'early')
        machine.begin(timeout=None, deadline=None)
        machine.queue_command('command')
        machine.publish(response)

        failure = OSError('flush failed')
        machine.write_completed(failure)

        with raises(SkillPipeBrokenError) as caught:
            machine.wait_response(timeout=None, deadline=None)
        assert caught.value.__cause__ is failure
        assert machine.state is _PipeState.BROKEN

    @mark.parametrize('write_failure', [None, OSError('late flush')])
    @mark.parametrize('event', [SkillResp('success', 'late'), OSError('late EOF')])
    def test_write_timeout_cause_survives_late_events(
        self, write_failure: Exception | None, event: SkillResp | Exception
    ) -> None:
        machine = _StateMachine(drain_timeout=None)
        machine.begin(timeout=0.1, deadline=time.monotonic() + 0.1)
        machine.queue_command('command')
        assert machine.take_command() == 'command\n'
        with machine._sync:
            timeout = machine._break_on_write_timeout(0.1)

        machine.write_completed(write_failure)
        machine.publish(event)

        with raises(SkillPipeBrokenError) as caught:
            machine.begin(timeout=0.1, deadline=time.monotonic() + 0.1)
        assert caught.value.__cause__ is timeout

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

        machine._expire_drain(0)

        assert machine.state is _PipeState.READY

    def test_stale_drain_watchdog_cannot_desynchronize_new_drain(self) -> None:
        class ControlledDrainTimer:
            timeout = 30.0

            def __init__(self) -> None:
                self.callbacks: list[Callable[[], None]] = []

            def start(self, callback: Callable[[], None]) -> None:
                self.callbacks.append(callback)

            def cancel(self) -> None:
                pass

        machine = _StateMachine(drain_timeout=30.0)
        timer = ControlledDrainTimer()
        machine._drain = timer  # type: ignore[assignment]

        machine.begin(timeout=0.0, deadline=time.monotonic())
        with raises(SkillPipeTimeoutError):
            machine.wait_response(timeout=0.0, deadline=time.monotonic())
        first_watchdog = timer.callbacks[0]

        machine.publish(SkillResp('success', 'late'))
        assert machine.state is _PipeState.READY

        machine.begin(timeout=0.0, deadline=time.monotonic())
        with raises(SkillPipeTimeoutError):
            machine.wait_response(timeout=0.0, deadline=time.monotonic())
        second_watchdog = timer.callbacks[1]

        first_watchdog()
        assert machine.state is _PipeState.DRAINING
        second_watchdog()
        assert machine.state is _PipeState.DESYNCHRONIZED


@mark.integration
@mark.parametrize(
    'command',
    ['', ' \t', 'ping()\nnext()', 'ping()\n\n', 'ping()\r', 'ping()\r\nnext()'],
    ids=['empty', 'whitespace', 'embedded-lf', 'extra-lf', 'bare-cr', 'embedded-crlf'],
)
def test_execute_rejects_invalid_command_without_writing(
    skill_pipe: tuple[Pipe, Server], command: str
) -> None:
    channel, server = skill_pipe

    with raises(SkillPipeInvalidCommandError):
        channel.execute(command, timeout=TEST_TIMEOUT)

    assert channel.state is _PipeState.READY
    with raises(Empty):
        server.recv(timeout=0.01)

    client = Client(lambda: channel.execute('good()', timeout=TEST_TIMEOUT))
    client.start()
    assert server.recv() == 'good()'
    server.respond('ok')
    assert client.result() == SkillResp('success', 'ok')


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
@mark.parametrize('command', ['ping()\n', 'ping()\r\n'], ids=['lf', 'crlf'])
def test_execute_preserves_existing_newline(skill_pipe: tuple[Pipe, Server], command: str) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute(command, timeout=TEST_TIMEOUT))
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
    assert_pipe_state(channel, _PipeState.RESTARTING)
    assert channel.wait_peer_closed(TEST_TIMEOUT)
    with raises(EOFError):
        server.recv()


@mark.integration
def test_late_restart_stops_pipe_without_next_request(
    skill_pipe: tuple[Pipe, Server],
) -> None:
    channel, server = skill_pipe

    requesting = Client(lambda: channel.execute('restart()', timeout=0.05))
    requesting.start()
    assert server.recv() == 'restart()'
    with raises(SkillPipeTimeoutError):
        requesting.result()

    server.respond('True', status='restart')

    assert channel.wait_peer_closed(TEST_TIMEOUT)
    assert_pipe_state(channel, _PipeState.RESTARTING)
    with raises(SkillPipeClosedError):
        channel.execute('next()', timeout=TEST_TIMEOUT)


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
def test_wait_peer_closed_detects_peer_eof(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe

    server.disconnect_response()

    assert channel.wait_peer_closed(TEST_TIMEOUT)


@mark.integration
def test_wait_peer_closed_distinguishes_local_close(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe

    channel.close()
    server.disconnect_response()

    assert not channel.wait_peer_closed(TEST_TIMEOUT)


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
    published = False
    monkeypatch.setattr(time, 'monotonic', lambda: 102.0 if published else 100.0)

    original_publish = _StateMachine.publish

    def publish_at_deadline(self: _StateMachine, event: SkillResp | Exception) -> None:
        nonlocal published
        original_publish(self, event)
        published = True

    monkeypatch.setattr(_StateMachine, 'publish', publish_at_deadline)

    client = Client(lambda: channel.execute('race()', timeout=1.0))
    client.start()
    assert server.recv() == 'race()'

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


def test_close_wakes_client_but_writer_owner_finishes(
    channel_factory: Callable[[StringIO], Pipe],
) -> None:
    writer = BlockingWriter()
    channel = channel_factory(writer)
    client = Client(lambda: channel.execute('blocked()', timeout=None))
    client.start()
    assert writer.entered.wait(TEST_TIMEOUT)

    channel.close()

    with raises(SkillPipeClosedError):
        client.result()
    writer.release()


def test_close_starts_owner_for_pre_execute_buffered_data(
    blocked_pipe: Callable[[str], BlockedPipe],
) -> None:
    resource = blocked_pipe('flush')
    payload = b'x' * (8 * 1024 * 1024) + b'\n'
    for offset in range(0, len(payload), 4096):
        resource.command_writer.buffer.write(payload[offset : offset + 4096])

    close_done = threading.Event()
    closer = threading.Thread(
        target=lambda: (resource.channel.close(), close_done.set()), daemon=True
    )
    start_thread(resource, closer)
    assert close_done.wait(TEST_TIMEOUT)
    drainer, errors = start_drainer(resource, payload)
    drainer.join(TEST_TIMEOUT)
    assert not drainer.is_alive()
    assert close_done.wait(TEST_TIMEOUT)
    assert not errors


@mark.parametrize('phase', ['write', 'flush'])
def test_real_pipe_write_deadline_poison_is_not_reusable(
    phase: str,
    blocked_pipe: Callable[[str], BlockedPipe],
) -> None:
    resource = blocked_pipe(phase)
    channel, command_writer = resource.channel, resource.command_writer
    client = Client(lambda: channel.execute('x' * (1024 * 1024), timeout=0.05))
    start_thread(resource, client)
    assert command_writer.entered.wait(TEST_TIMEOUT)
    with raises(SkillPipeTimeoutError) as caught:
        client.result(TEST_TIMEOUT)
    assert caught.value.phase == 'command write'
    timeout_cause = caught.value
    drainer, errors = start_drainer(resource, b'x' * (1024 * 1024) + b'\n')
    drainer.join(TEST_TIMEOUT)
    assert not drainer.is_alive()
    assert not errors
    assert_pipe_state(channel, _PipeState.BROKEN)
    with raises(SkillPipeBrokenError) as broken:
        channel.execute('next()', timeout=TEST_TIMEOUT)
    assert broken.value.__cause__ is timeout_cause


@mark.parametrize('phase', ['write', 'flush'])
def test_real_pipe_close_wakes_client_without_waiting_for_writer(
    phase: str,
    blocked_pipe: Callable[[str], BlockedPipe],
) -> None:
    resource = blocked_pipe(phase)
    channel, command_writer = resource.channel, resource.command_writer
    client = Client(lambda: channel.execute('x' * (1024 * 1024), timeout=None))
    start_thread(resource, client)
    assert command_writer.entered.wait(TEST_TIMEOUT)
    close_done = threading.Event()
    closer = threading.Thread(target=lambda: (channel.close(), close_done.set()), daemon=True)
    start_thread(resource, closer)
    assert close_done.wait(TEST_TIMEOUT)
    with raises(SkillPipeClosedError):
        client.result(TEST_TIMEOUT)


def test_real_pipe_eof_wakes_client_without_waiting_for_writer(
    blocked_pipe: Callable[[str], BlockedPipe],
) -> None:
    resource = blocked_pipe('flush')
    channel = resource.channel
    command_writer, response_writer = resource.command_writer, resource.response_writer
    client = Client(lambda: channel.execute('x' * (1024 * 1024), timeout=None))
    start_thread(resource, client)
    assert command_writer.entered.wait(TEST_TIMEOUT)
    response_writer.close()

    with raises(SkillPipeBrokenError):
        client.result(TEST_TIMEOUT)
    assert channel.wait_peer_closed(TEST_TIMEOUT)


def test_real_pipe_rst_delivers_without_waiting_for_writer(
    blocked_pipe: Callable[[str], BlockedPipe],
) -> None:
    resource = blocked_pipe('flush')
    channel = resource.channel
    command_writer, response_writer = resource.command_writer, resource.response_writer
    client = Client(lambda: channel.execute('x' * (1024 * 1024), timeout=None))
    start_thread(resource, client)
    assert command_writer.entered.wait(TEST_TIMEOUT)
    response_writer.write(Response.RST + 'restart' + Response.RS)
    response_writer.flush()

    assert client.result(TEST_TIMEOUT) == SkillResp('restart', 'restart')
    assert channel.state is _PipeState.RESTARTING
    assert channel.wait_peer_closed(TEST_TIMEOUT)


def test_real_pipe_response_waits_for_blocked_writer(
    blocked_pipe: Callable[[str], BlockedPipe],
) -> None:
    resource = blocked_pipe('flush')
    channel = resource.channel
    command_writer, response_writer = resource.command_writer, resource.response_writer
    client = Client(lambda: channel.execute('x' * (1024 * 1024), timeout=None))
    start_thread(resource, client)
    assert command_writer.entered.wait(TEST_TIMEOUT)
    response_writer.write(Response.STX + 'done' + Response.RS)
    response_writer.flush()

    client.join(0.05)
    assert client.is_alive()
    drainer, errors = start_drainer(resource, b'x' * (1024 * 1024) + b'\n')
    assert client.result(TEST_TIMEOUT) == SkillResp('success', 'done')
    drainer.join(TEST_TIMEOUT)
    assert not drainer.is_alive()
    assert not errors


def test_close_closes_streams() -> None:
    reader = StringIO()
    writer = StringIO()
    channel = Pipe(reader, writer)
    channel.close()
    assert channel.wait_closed(TEST_TIMEOUT)

    assert reader.closed
    assert writer.closed


def test_context_manager_closes_pipe() -> None:
    reader = StringIO()
    writer = StringIO()

    with Pipe(reader, writer) as channel:
        assert channel.state in {_PipeState.READY, _PipeState.BROKEN}

    assert channel.state is _PipeState.CLOSED
