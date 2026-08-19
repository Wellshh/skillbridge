from __future__ import annotations

import threading
from queue import Queue

import pytest
from skillbridge.pipe import (
    SkillPipe,
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeState,
    SkillPipeTimeoutError,
)
from skillbridge.response_protocol import SkillResponse

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
        response = pipe.execute("cmd()", timeout=1.0)
        assert response.ok
        assert response.payload == "line one\nline two"
        assert writer.text == "cmd()\n"
        assert pipe.state is SkillPipeState.READY
    finally:
        pipe.close()
        thread.join(1.0)
        pipe.join_reader(1.0)


def test_framed_error_returns_failed_response_without_poisoning_channel() -> None:
    pipe, reader, writer = framed_pipe()

    def respond_error() -> None:
        assert writer.write_event.wait(1.0)
        reader.feed_error("bad expression")

    thread = threading.Thread(target=respond_error)
    thread.start()
    try:
        response = pipe.execute("bad()", timeout=1.0)
        assert not response.ok
        assert response.payload == "bad expression"
        assert pipe.state is SkillPipeState.READY
    finally:
        pipe.close()
        thread.join(1.0)
        pipe.join_reader(1.0)


def test_framed_timeout_drains_late_response_and_recovers() -> None:
    pipe, reader, writer = framed_pipe(drain_timeout=1.0)
    respond_thread: threading.Thread | None = None
    try:
        with pytest.raises(SkillPipeTimeoutError) as caught:
            pipe.execute("slow()", timeout=0.03)
        assert caught.value.phase == "SKILL response"
        assert pipe.state is SkillPipeState.DRAINING

        reader.feed_success("late result")
        assert pipe.wait_until_ready(1.0)
        assert pipe.state is SkillPipeState.READY

        writer.write_event.clear()

        def respond_next() -> None:
            assert writer.write_event.wait(1.0)
            reader.feed_success("next result")

        respond_thread = threading.Thread(target=respond_next)
        respond_thread.start()
        response = pipe.execute("next()", timeout=1.0)
        assert response.ok
        assert response.payload == "next result"
        assert writer.lines() == ["slow()", "next()"]
    finally:
        pipe.close()
        if respond_thread is not None:
            respond_thread.join(1.0)
        pipe.join_reader(1.0)


def test_next_request_waits_for_drain_before_writing() -> None:
    pipe, reader, writer = framed_pipe(drain_timeout=1.0)
    result: Queue[SkillResponse | BaseException] = Queue()
    next_entered = threading.Event()
    next_thread: threading.Thread | None = None
    try:
        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("slow()", timeout=0.03)

        assert pipe.state is SkillPipeState.DRAINING
        writer.write_event.clear()

        def next_request() -> None:
            next_entered.set()
            try:
                result.put(pipe.execute("next()", timeout=1.0))
            except BaseException as exc:
                result.put(exc)

        next_thread = threading.Thread(target=next_request)
        next_thread.start()
        assert next_entered.wait(1.0)
        assert writer.lines() == ["slow()"]

        reader.feed_success("stale")
        assert writer.write_event.wait(1.0)
        assert writer.lines() == ["slow()", "next()"]
        reader.feed_success("fresh")
        res = result.get(timeout=1.0)
        assert isinstance(res, SkillResponse)
        assert res.ok
        assert res.payload == "fresh"
    finally:
        pipe.close()
        if next_thread is not None:
            next_thread.join(1.0)
        pipe.join_reader(1.0)


def test_drain_watchdog_eventually_desynchronizes() -> None:
    pipe, _reader, _writer = framed_pipe(drain_timeout=0.05)
    try:
        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("never_returns()", timeout=0.02)
        assert pipe.state is SkillPipeState.DRAINING

        assert not pipe.wait_until_ready(0.5)
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


def test_timeout_waiting_for_serializer_does_not_poison_channel() -> None:
    pipe, reader, writer = framed_pipe()
    first_result: Queue[SkillResponse | BaseException] = Queue()

    def first_request() -> None:
        try:
            first_result.put(pipe.execute("first()", timeout=1.0))
        except BaseException as exc:
            first_result.put(exc)

    first = threading.Thread(target=first_request)
    first.start()
    try:
        assert writer.write_event.wait(1.0)
        with pytest.raises(SkillPipeTimeoutError) as caught:
            pipe.execute("second()", timeout=0.03)
        assert caught.value.phase == "serialization"
        assert pipe.state is SkillPipeState.EXECUTING
        assert writer.lines() == ["first()"]

        reader.feed_success("one")
        res = first_result.get(timeout=1.0)
        assert isinstance(res, SkillResponse)
        assert res.ok
        assert res.payload == "one"
        assert pipe.state is SkillPipeState.READY
    finally:
        pipe.close()
        first.join(1.0)
        pipe.join_reader(1.0)


def test_two_callers_are_serialized_across_response_boundary() -> None:
    pipe, reader, writer = framed_pipe()
    outputs: dict[str, SkillResponse] = {}
    failures: list[BaseException] = []
    second_started = threading.Event()

    def call_a() -> None:
        try:
            outputs["A"] = pipe.execute("A", timeout=2.0)
        except BaseException as exc:
            failures.append(exc)

    def call_b() -> None:
        second_started.set()
        try:
            outputs["B"] = pipe.execute("B", timeout=2.0)
        except BaseException as exc:
            failures.append(exc)

    t_a = threading.Thread(target=call_a)
    t_b = threading.Thread(target=call_b)

    t_a.start()
    try:
        assert writer.write_event.wait(1.0)
        assert writer.lines() == ["A"]

        writer.write_event.clear()
        t_b.start()
        assert second_started.wait(1.0)

        reader.feed_success("response:A")
        t_a.join(1.0)
        assert outputs["A"].ok
        assert outputs["A"].payload == "response:A"

        assert writer.write_event.wait(1.0)
        assert writer.lines() == ["A", "B"]

        reader.feed_success("response:B")
        t_b.join(1.0)
        assert outputs["B"].ok
        assert outputs["B"].payload == "response:B"
        assert not failures
    finally:
        pipe.close()
        t_a.join(1.0)
        t_b.join(1.0)
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
    result: Queue[SkillResponse | BaseException] = Queue()

    def execute() -> None:
        try:
            result.put(pipe.execute("cmd", timeout=None))
        except BaseException as exc:
            result.put(exc)

    thread = threading.Thread(target=execute)
    thread.start()
    try:
        assert writer.write_event.wait(1.0)
        pipe.close()
        res = result.get(timeout=1.0)
        assert isinstance(res, SkillPipeClosedError)
    finally:
        pipe.close()
        thread.join(1.0)
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


def test_deadline_race_response_published_at_exact_boundary(monkeypatch) -> None:
    """When time reaches the deadline just as reader publishes the response frame,
    the pipe must reliably return the response if it was published while EXECUTING,
    and state must remain READY without dropping into DRAINING."""
    pipe, reader, writer = framed_pipe(drain_timeout=1.0)
    current_time = 100.0

    def mock_time() -> float:
        return current_time

    monkeypatch.setattr("time.monotonic", mock_time)

    result_queue: Queue[SkillResponse | BaseException] = Queue()

    def caller() -> None:
        try:
            res = pipe.execute("race()", timeout=1.0)
            result_queue.put(res)
        except BaseException as exc:
            result_queue.put(exc)

    t = threading.Thread(target=caller)
    t.start()
    try:
        assert writer.write_event.wait(1.0)
        # Advance clock to simulate deadline boundary expiration
        current_time = 102.0
        # Publish response simultaneously
        reader.feed_success("exact_boundary")
        res = result_queue.get(timeout=1.0)
        assert isinstance(res, SkillResponse)
        assert res.ok
        assert res.payload == "exact_boundary"
        assert pipe.state is SkillPipeState.READY
    finally:
        pipe.close()
        t.join(1.0)
        pipe.join_reader(1.0)


def test_response_delivered_before_subsequent_reader_eof() -> None:
    """When a complete response frame is published and the reader encounters EOF
    on the next read, the current in-flight execute must return the complete response,
    and only the subsequent execute should report BROKEN."""
    pipe, reader, writer = framed_pipe()

    def feed_and_then_eof() -> None:
        assert writer.write_event.wait(1.0)
        reader.feed_success("valid payload")
        reader.feed_eof()

    feed_thread = threading.Thread(target=feed_and_then_eof)
    feed_thread.start()
    try:
        result = pipe.execute("first()", timeout=1.0)
        assert result.ok
        assert result.payload == "valid payload"

        with pytest.raises(SkillPipeBrokenError):
            pipe.execute("second()", timeout=1.0)
        assert pipe.state is SkillPipeState.BROKEN
    finally:
        pipe.close()
        feed_thread.join(1.0)
        pipe.join_reader(1.0)
