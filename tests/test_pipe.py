from __future__ import annotations

from collections.abc import Iterator
from io import TextIOWrapper
from os import fdopen, pipe

from pytest import fixture

from skillbridge.server._pipe import Pipe  # ruff: ignore[import-private-name]


@fixture
def skill_pipe() -> Iterator[tuple[Pipe, TextIOWrapper, TextIOWrapper]]:
    command_read_fd, command_write_fd = pipe()
    response_read_fd, response_write_fd = pipe()
    command_reader = fdopen(command_read_fd, encoding='utf-8', newline='')
    command_writer = fdopen(command_write_fd, 'w', encoding='utf-8', newline='')
    response_reader = fdopen(response_read_fd, encoding='utf-8', newline='')
    response_writer = fdopen(response_write_fd, 'w', encoding='utf-8', newline='')

    try:
        channel = Pipe(response_reader, command_writer)
        yield channel, command_reader, response_writer
    finally:
        command_reader.close()
        command_writer.close()
        response_reader.close()
        response_writer.close()
