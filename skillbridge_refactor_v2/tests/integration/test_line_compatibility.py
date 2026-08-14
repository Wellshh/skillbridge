from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from typing import Iterator

import pytest

from skillbridge.client import SkillBridgeClient
from skillbridge.pipe import SkillPipe, SkillPipeState
from skillbridge.response_protocol import LineResponseProtocol
from skillbridge.server import Handler, ThreadingTcpServer
from ..helpers import BlockingTextReader, RecordingWriter


@contextmanager
def line_server(
    *, timeout: float | None = 1.0,
) -> Iterator[tuple[ThreadingTcpServer, SkillPipe, BlockingTextReader, RecordingWriter]]:
    reader = BlockingTextReader()
    writer = RecordingWriter()
    pipe = SkillPipe(
        reader,
        writer,
        response_protocol=LineResponseProtocol(),
        owns_streams=True,
    )
    server = ThreadingTcpServer(
        0,
        Handler,
        skill_pipe=pipe,
        skill_timeout=timeout,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, pipe, reader, writer
    finally:
        server.shutdown()
        server.server_close()
        thread.join(2.0)
        pipe.close()
        pipe.join_reader(2.0)


def port(server: ThreadingTcpServer) -> int:
    return int(server.server_address[1])


@pytest.mark.integration
def test_legacy_one_line_response_remains_compatible() -> None:
    with line_server() as (server, pipe, reader, writer):
        def respond() -> None:
            assert writer.write_event.wait(1.0)
            reader.feed_line("legacy-result\n")

        responder = threading.Thread(target=respond)
        responder.start()
        with SkillBridgeClient("127.0.0.1", port(server), timeout=2.0) as client:
            assert client.execute("legacy()") == "legacy-result\n"
        responder.join(1.0)
        assert pipe.state is SkillPipeState.READY


@pytest.mark.integration
def test_legacy_timeout_is_intentionally_fail_closed() -> None:
    with line_server(timeout=0.05) as (server, pipe, _reader, writer):
        client = SkillBridgeClient("127.0.0.1", port(server), timeout=2.0)
        try:
            assert client.execute("slow()") == "failure <timeout phase=SKILL response>"
        finally:
            client.close(notify_server=False)
        assert pipe.state is SkillPipeState.DESYNCHRONIZED
        assert writer.lines() == ["slow()"]

        second = SkillBridgeClient("127.0.0.1", port(server), timeout=2.0)
        try:
            assert second.execute("next()") == "failure <desynchronized>"
        finally:
            second.close(notify_server=False)
        time.sleep(0.01)
        assert writer.lines() == ["slow()"]
