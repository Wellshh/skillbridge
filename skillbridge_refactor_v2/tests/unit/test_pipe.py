from __future__ import annotations

import threading
import time
from queue import Queue

import pytest

from skillbridge.pipe import (
    SkillExecutionError,
    SkillPipe,
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeState,
    SkillPipeTimeoutError,
)
from skillbridge.response_protocol import FramedResponseProtocol, LineResponseProtocol
from ..helpers import BlockingTextReader, FailingWriter, RecordingWriter


def framed_pipe(
    *,
    drain_timeout: float | None = 1.0,
) -> tuple[SkillPipe, BlockingTextReader, RecordingWriter]:
    reader = BlockingTextReader()
    writer = RecordingWriter()
    pipe = SkillPipe(
        reader,
        writer,
        response_protocol=FramedResponseProtocol(),
        drain_timeout=drain_timeout,
        owns_streams=True,
    )
    return pipe, reader, writer


def test_framed_success_and_multiline_payload() -> None:
    pipe, reader, writer = framed_pipe()

    def respond() -> None:
        assert writer.write_event.wait(1.0)
        reader.feed_success("line one\nline two")

    thread = threading.Thread(target=respond)
    thread.start()
    try:
        assert pipe.execute("cmd()", timeout=1.0) == "line one\nline two"
        assert writer.text == "cmd()\n"
        assert pipe.state is SkillPipeState.READY
        assert pipe.snapshot().successful_requests == 1
    finally:
        pipe.close()
        thread.join(1.0)
        pipe.join_reader(1.0)


def test_framed_error_raises_without_poisoning_channel() -> None:
    pipe, reader, writer = framed_pipe()

    def respond_error() -> None:
        assert writer.write_event.wait(1.0)
        reader.feed_error("bad expression")

    thread = threading.Thread(target=respond_error)
    thread.start()
    try:
        with pytest.raises(SkillExecutionError) as caught:
            pipe.execute("bad()", timeout=1.0)
        assert caught.value.payload == "bad expression"
        assert pipe.state is SkillPipeState.READY
        assert pipe.snapshot().remote_errors == 1
    finally:
        pipe.close()
        thread.join(1.0)
        pipe.join_reader(1.0)


def test_framed_timeout_drains_late_response_and_recovers() -> None:
    pipe, reader, writer = framed_pipe(drain_timeout=1.0)
    try:
        with pytest.raises(SkillPipeTimeoutError) as caught:
            pipe.execute("slow()", timeout=0.03)
        assert caught.value.phase == "SKILL response"
        assert pipe.state is SkillPipeState.DRAINING

        reader.feed_success("late result")
        assert pipe.wait_until_ready(1.0)
        assert pipe.state is SkillPipeState.READY
        assert pipe.snapshot().recovered_timeouts == 1
        assert pipe.snapshot().failure is None

        writer.write_event.clear()

        def respond_next() -> None:
            assert writer.write_event.wait(1.0)
            reader.feed_success("next result")

        thread = threading.Thread(target=respond_next)
        thread.start()
        assert pipe.execute("next()", timeout=1.0) == "next result"
        thread.join(1.0)
        assert writer.lines() == ["slow()", "next()"]
    finally:
        pipe.close()
        pipe.join_reader(1.0)


def test_next_request_waits_for_drain_before_writing() -> None:
    pipe, reader, writer = framed_pipe(drain_timeout=1.0)
    result: Queue[str | BaseException] = Queue()
    try:
        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("slow()", timeout=0.03)

        writer.write_event.clear()

        def next_request() -> None:
            try:
                result.put(pipe.execute("next()", timeout=1.0))
            except BaseException as exc:
                result.put(exc)

        thread = threading.Thread(target=next_request)
        thread.start()
        time.sleep(0.03)
        assert writer.lines() == ["slow()"]

        reader.feed_success("stale")
        assert writer.write_event.wait(1.0)
        assert writer.lines() == ["slow()", "next()"]
        reader.feed_success("fresh")
        thread.join(1.0)
        assert result.get_nowait() == "fresh"
    finally:
        pipe.close()
        pipe.join_reader(1.0)


def test_drain_watchdog_eventually_desynchronizes() -> None:
    pipe, _reader, _writer = framed_pipe(drain_timeout=0.05)
    try:
        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("never_returns()", timeout=0.02)
        assert pipe.state is SkillPipeState.DRAINING

        deadline = time.monotonic() + 1.0
        while pipe.state is SkillPipeState.DRAINING and time.monotonic() < deadline:
            time.sleep(0.005)
        assert pipe.state is SkillPipeState.DESYNCHRONIZED
        with pytest.raises(SkillPipeDesynchronizedError):
            pipe.execute("next()", timeout=1.0)
    finally:
        pipe.close()
        pipe.join_reader(1.0)


def test_request_deadline_can_expire_while_waiting_for_recovery() -> None:
    pipe, _reader, writer = framed_pipe(drain_timeout=None)
    try:
        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("slow()", timeout=0.02)
        with pytest.raises(SkillPipeTimeoutError) as caught:
            pipe.execute("next()", timeout=0.03)
        assert caught.value.phase == "timeout recovery"
        assert pipe.state is SkillPipeState.DRAINING
        assert writer.lines() == ["slow()"]
    finally:
        pipe.close()
        pipe.join_reader(1.0)


def test_line_mode_timeout_remains_fail_closed() -> None:
    reader = BlockingTextReader()
    writer = RecordingWriter()
    pipe = SkillPipe(
        reader,
        writer,
        response_protocol=LineResponseProtocol(),
        owns_streams=True,
    )
    try:
        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("slow()", timeout=0.02)
        assert pipe.state is SkillPipeState.DESYNCHRONIZED
        reader.feed_line("late\n")
        time.sleep(0.01)
        with pytest.raises(SkillPipeDesynchronizedError):
            pipe.execute("next()", timeout=1.0)
    finally:
        pipe.close()
        pipe.join_reader(1.0)


def test_recovery_cannot_be_enabled_for_line_protocol() -> None:
    with pytest.raises(ValueError):
        SkillPipe(
            BlockingTextReader(),
            RecordingWriter(),
            response_protocol=LineResponseProtocol(),
            recover_after_timeout=True,
        )


def test_timeout_waiting_for_serializer_does_not_poison_channel() -> None:
    pipe, reader, writer = framed_pipe()
    first_result: Queue[str | BaseException] = Queue()

    def first_request() -> None:
        try:
            first_result.put(pipe.execute("first()", timeout=1.0))
        except BaseException as exc:
            first_result.put(exc)

    first = threading.Thread(target=first_request)
    first.start()
    assert writer.write_event.wait(1.0)
    try:
        with pytest.raises(SkillPipeTimeoutError) as caught:
            pipe.execute("second()", timeout=0.03)
        assert caught.value.phase == "serialization"
        assert pipe.state is SkillPipeState.EXECUTING
        assert writer.lines() == ["first()"]

        reader.feed_success("one")
        first.join(1.0)
        assert first_result.get_nowait() == "one"
        assert pipe.state is SkillPipeState.READY
    finally:
        pipe.close()
        first.join(1.0)
        pipe.join_reader(1.0)


def test_two_callers_are_serialized_across_response_boundary() -> None:
    pipe, reader, writer = framed_pipe()
    outputs: dict[str, str] = {}
    failures: list[BaseException] = []

    def call(name: str) -> None:
        try:
            outputs[name] = pipe.execute(name, timeout=2.0)
        except BaseException as exc:
            failures.append(exc)

    threads = [threading.Thread(target=call, args=(name,)) for name in ("A", "B")]
    for thread in threads:
        thread.start()
    try:
        deadline = time.monotonic() + 1.0
        while len(writer.lines()) < 1 and time.monotonic() < deadline:
            time.sleep(0.005)
        first = writer.lines()[0]
        time.sleep(0.03)
        assert writer.lines() == [first]
        reader.feed_success(f"response:{first}")

        deadline = time.monotonic() + 1.0
        while len(writer.lines()) < 2 and time.monotonic() < deadline:
            time.sleep(0.005)
        second = writer.lines()[1]
        reader.feed_success(f"response:{second}")

        for thread in threads:
            thread.join(1.0)
        assert not failures
        assert outputs[first] == f"response:{first}"
        assert outputs[second] == f"response:{second}"
    finally:
        pipe.close()
        for thread in threads:
            thread.join(1.0)
        pipe.join_reader(1.0)


def test_reader_eof_and_writer_failure_mark_broken() -> None:
    pipe, reader, writer = framed_pipe()

    def eof_after_write() -> None:
        assert writer.write_event.wait(1.0)
        reader.feed_eof()

    thread = threading.Thread(target=eof_after_write)
    thread.start()
    try:
        with pytest.raises(SkillPipeBrokenError):
            pipe.execute("cmd", timeout=1.0)
        assert pipe.state is SkillPipeState.BROKEN
    finally:
        pipe.close()
        thread.join(1.0)
        pipe.join_reader(1.0)

    reader2 = BlockingTextReader()
    pipe2 = SkillPipe(
        reader2,
        FailingWriter(),
        response_protocol=FramedResponseProtocol(),
        owns_streams=True,
    )
    try:
        with pytest.raises(SkillPipeBrokenError):
            pipe2.execute("cmd", timeout=1.0)
        assert pipe2.state is SkillPipeState.BROKEN
    finally:
        pipe2.close()
        pipe2.join_reader(1.0)


def test_close_wakes_request_with_no_deadline() -> None:
    pipe, _reader, writer = framed_pipe()
    result: Queue[str | BaseException] = Queue()

    def execute() -> None:
        try:
            result.put(pipe.execute("cmd", timeout=None))
        except BaseException as exc:
            result.put(exc)

    thread = threading.Thread(target=execute)
    thread.start()
    assert writer.write_event.wait(1.0)
    pipe.close()
    thread.join(1.0)
    assert isinstance(result.get_nowait(), SkillPipeClosedError)
    pipe.join_reader(1.0)


@pytest.mark.parametrize("timeout", [-1.0, float("inf"), float("nan")])
def test_invalid_timeout_is_rejected(timeout: float) -> None:
    pipe, _reader, _writer = framed_pipe()
    try:
        with pytest.raises(ValueError):
            pipe.execute("cmd", timeout=timeout)
    finally:
        pipe.close()
        pipe.join_reader(1.0)
