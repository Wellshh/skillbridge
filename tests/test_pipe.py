"""Test framework for Pipe; see ``skillbridge/server/SECRET.md`` for its design."""

from __future__ import annotations

import threading
from collections.abc import Iterator
from io import TextIOWrapper
from os import fdopen, pipe
from queue import Queue

from pytest import fixture

from skillbridge.protocol.response import Response, RespStatus
from skillbridge.server._pipe import Pipe  # ruff: ignore[import-private-name]

TEST_TIMEOUT = 1.0
_EOF = object()


class SkillServer:
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
def skill_pipe() -> Iterator[tuple[Pipe, SkillServer]]:
    command_read_fd, command_write_fd = pipe()
    response_read_fd, response_write_fd = pipe()
    command_reader = fdopen(command_read_fd, encoding='utf-8', newline='')
    command_writer = fdopen(command_write_fd, 'w', encoding='utf-8', newline='')
    response_reader = fdopen(response_read_fd, encoding='utf-8', newline='')
    response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')
    server = SkillServer(command_reader, response_writer)
    channel = Pipe(response_reader, command_writer)

    try:
        yield channel, server
    finally:
        command_writer.close()
        try:
            server.close()
        finally:
            channel._thread.join(TEST_TIMEOUT)
            response_reader.close()
