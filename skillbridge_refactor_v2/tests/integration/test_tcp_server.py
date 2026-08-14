from __future__ import annotations

import json
import socket
import threading
import time
from contextlib import contextmanager
from typing import Iterator

import pytest

from skillbridge.client import SkillBridgeClient
from skillbridge.pipe import SkillPipe, SkillPipeState
from skillbridge.response_protocol import FramedResponseProtocol
from skillbridge.server import Handler, ThreadingTcpServer
from skillbridge.socket_protocol import encode_header, recv_frame
from ..helpers import BlockingTextReader, RecordingWriter


@contextmanager
def running_server(
    *,
    timeout: float | None = 1.0,
    drain_timeout: float | None = 1.0,
) -> Iterator[tuple[ThreadingTcpServer, SkillPipe, BlockingTextReader, RecordingWriter]]:
    reader = BlockingTextReader()
    writer = RecordingWriter()
    pipe = SkillPipe(
        reader,
        writer,
        response_protocol=FramedResponseProtocol(),
        drain_timeout=drain_timeout,
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
def test_real_tcp_round_trip_multiline_error_and_health() -> None:
    with running_server() as (server, pipe, reader, writer):
        with SkillBridgeClient("127.0.0.1", port(server), timeout=2.0) as client:
            def success(expected: str, payload: str) -> None:
                deadline = time.monotonic() + 1.0
                while expected not in writer.lines() and time.monotonic() < deadline:
                    time.sleep(0.005)
                reader.feed_success(payload)

            thread = threading.Thread(target=success, args=("multi()", "one\ntwo"))
            thread.start()
            assert client.execute("multi()") == "one\ntwo"
            thread.join(1.0)

            writer.write_event.clear()

            def error() -> None:
                assert writer.write_event.wait(1.0)
                reader.feed_error("bad expression")

            thread = threading.Thread(target=error)
            thread.start()
            assert client.execute("bad()") == "failure <skill-error>\nbad expression"
            thread.join(1.0)
            assert pipe.state is SkillPipeState.READY

            health = json.loads(client.health())
            assert health["protocol"] == "framed"
            assert health["successful_requests"] == 1
            assert health["remote_errors"] == 1


@pytest.mark.integration
def test_fragmented_tcp_request_is_reassembled() -> None:
    with running_server() as (server, _pipe, reader, writer):
        sock = socket.create_connection(("127.0.0.1", port(server)), timeout=2.0)
        sock.settimeout(2.0)
        try:
            payload = b"fragmented()"
            wire = encode_header(len(payload)) + payload

            def respond() -> None:
                deadline = time.monotonic() + 1.0
                while "fragmented()" not in writer.lines() and time.monotonic() < deadline:
                    time.sleep(0.005)
                reader.feed_success("ok")

            responder = threading.Thread(target=respond)
            responder.start()
            for part in (wire[:1], wire[1:4], wire[4:10], wire[10:13], wire[13:]):
                sock.sendall(part)
            assert recv_frame(sock) == b"ok"
            responder.join(1.0)
        finally:
            sock.close()


@pytest.mark.integration
def test_concurrent_tcp_clients_are_serialized() -> None:
    with running_server(timeout=2.0) as (server, _pipe, reader, writer):
        outputs: dict[str, str] = {}
        failures: list[BaseException] = []
        barrier = threading.Barrier(3)

        def call(command: str) -> None:
            try:
                with SkillBridgeClient("127.0.0.1", port(server), timeout=3.0) as client:
                    barrier.wait()
                    outputs[command] = client.execute(command)
            except BaseException as exc:
                failures.append(exc)

        clients = [threading.Thread(target=call, args=(cmd,)) for cmd in ("A", "B")]
        for client in clients:
            client.start()
        barrier.wait()

        deadline = time.monotonic() + 1.0
        while len(writer.lines()) < 1 and time.monotonic() < deadline:
            time.sleep(0.005)
        first = writer.lines()[0]
        time.sleep(0.03)
        assert writer.lines() == [first]
        reader.feed_success(f"result:{first}")

        deadline = time.monotonic() + 1.0
        while len(writer.lines()) < 2 and time.monotonic() < deadline:
            time.sleep(0.005)
        second = writer.lines()[1]
        reader.feed_success(f"result:{second}")

        for client in clients:
            client.join(2.0)
        assert not failures
        assert outputs[first] == f"result:{first}"
        assert outputs[second] == f"result:{second}"


@pytest.mark.integration
def test_server_recovers_after_late_frame() -> None:
    with running_server(timeout=0.15, drain_timeout=1.0) as (
        server,
        pipe,
        reader,
        writer,
    ):
        first = SkillBridgeClient("127.0.0.1", port(server), timeout=2.0)
        try:
            assert first.execute("slow()") == "failure <timeout phase=SKILL response>"
        finally:
            first.close(notify_server=False)
        assert pipe.state is SkillPipeState.DRAINING

        result: list[str] = []

        def second_client() -> None:
            with SkillBridgeClient("127.0.0.1", port(server), timeout=2.0) as client:
                result.append(client.execute("next()"))

        thread = threading.Thread(target=second_client)
        thread.start()
        time.sleep(0.03)
        assert writer.lines() == ["slow()"]

        reader.feed_success("late")
        deadline = time.monotonic() + 1.0
        while len(writer.lines()) < 2 and time.monotonic() < deadline:
            time.sleep(0.005)
        assert writer.lines() == ["slow()", "next()"]
        reader.feed_success("fresh")
        thread.join(2.0)
        assert result == ["fresh"]
        assert pipe.state is SkillPipeState.READY
