"""Test framework for Pipe; see ``skillbridge/server/SECRET.md`` for its design."""

from __future__ import annotations

import threading
from collections.abc import Callable, Iterator
from io import StringIO, TextIOWrapper
from os import fdopen, pipe
from queue import Queue

from pytest import fixture, raises

from skillbridge.exception import SkillPipeClosedError
from skillbridge.protocol.response import Response, RespStatus, SkillResp
from skillbridge.server._pipe import Pipe  # ruff: ignore[import-private-name]

TEST_TIMEOUT = 1.0
_EOF = object()


class Client(threading.Thread):
    def __init__(
        self,
        request: Callable[[], SkillResp],
        *,
        gate: threading.Barrier | None = None,
        name: str = 'mock-client',
    ) -> None:
        super().__init__(name=name, daemon=True)
        self._request = request
        self._gate = gate
        self._outcome: Queue[SkillResp | Exception] = Queue(maxsize=1)
        self.started = threading.Event()

    def run(self) -> None:
        self.started.set()
        try:
            if self._gate is not None:
                self._gate.wait(TEST_TIMEOUT)
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
        self._commands: Queue[str | object] = Queue()
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
            self._commands.put(_EOF)
            self._response_writer.close()

    def recv(self, timeout: float = TEST_TIMEOUT) -> str:
        command = self._commands.get(timeout=timeout)
        if command is _EOF:
            raise EOFError("Pipe closed its command stream")
        assert isinstance(command, str)
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

    def close(self) -> None:
        self._response_writer.close()
        self._thread.join(TEST_TIMEOUT)
        if self._thread.is_alive():
            raise RuntimeError("mock SKILL server did not stop")
        self._command_reader.close()


@fixture
def skill_pipe() -> Iterator[tuple[Pipe, Server]]:
    command_read_fd, command_write_fd = pipe()
    response_read_fd, response_write_fd = pipe()
    command_reader = fdopen(command_read_fd, encoding='utf-8', newline='')
    command_writer = fdopen(command_write_fd, 'w', encoding='utf-8', newline='')
    response_reader = fdopen(response_read_fd, encoding='utf-8', newline='')
    response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')
    server = Server(command_reader, response_writer)
    channel = Pipe(response_reader, command_writer)

    try:
        yield channel, server
    finally:
        channel.close()
        try:
            server.close()
        finally:
            channel._thread.join(TEST_TIMEOUT)
            response_reader.close()


def test_owned_close_stops_reader_after_peer_eof(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, _ = skill_pipe

    channel.close()

    assert channel.wait_closed(TEST_TIMEOUT)


def test_close_wakes_executing_client(skill_pipe: tuple[Pipe, Server]) -> None:
    channel, server = skill_pipe
    client = Client(lambda: channel.execute('wait()', timeout=None))
    client.start()
    assert server.recv() == 'wait()'

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
