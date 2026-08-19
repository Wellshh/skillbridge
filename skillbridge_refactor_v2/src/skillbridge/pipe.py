"""Serialized, cross-platform access to a SKILL IPC pipe.

A daemon reader thread owns the blocking read side.  Request threads wait on
thread synchronization primitives whose timeouts work on Windows, macOS, and Linux.

Only one command may be in flight at a time.  With framed responses, the channel
enters DRAINING on timeout to safely consume exactly one late response before
returning to READY.
"""

from __future__ import annotations

import logging
import threading
import time
from enum import Enum, auto
from types import TracebackType
from typing import TextIO

from .response_protocol import FramedResponseProtocol, SkillResponse

logger = logging.getLogger(__name__)

_MISSING = object()


class SkillPipeError(RuntimeError):
    """Base class for SKILL channel failures."""


class SkillPipeTimeoutError(SkillPipeError):
    """A request exceeded its total deadline."""

    def __init__(self, timeout: float, *, phase: str) -> None:
        self.timeout = timeout
        self.phase = phase
        super().__init__(
            f"SKILL request timed out after {timeout:g} seconds while waiting for {phase}"
        )


class SkillPipeDesynchronizedError(SkillPipeError):
    """The request/response association can no longer be trusted."""


class SkillPipeClosedError(SkillPipeError):
    """The channel was closed intentionally."""


class SkillPipeBrokenError(SkillPipeError):
    """The underlying reader, writer, or framing parser failed."""


class SkillPipeState(Enum):
    READY = auto()
    EXECUTING = auto()
    DRAINING = auto()
    DESYNCHRONIZED = auto()
    BROKEN = auto()
    CLOSED = auto()


class SkillPipe:
    """Serialize complete command/response transactions over text streams."""

    def __init__(
        self,
        reader: TextIO,
        writer: TextIO,
        *,
        drain_timeout: float | None = 30.0,
        owns_streams: bool = False,
        max_payload_chars: int = 16 * 1024 * 1024,
        ignore_preamble: bool = False,
        max_preamble_chars: int = 4096,
    ) -> None:
        self._validate_optional_timeout(drain_timeout, name="drain_timeout")

        self._reader = reader
        self._writer = writer
        self._protocol = FramedResponseProtocol(
            max_payload_chars=max_payload_chars,
            ignore_preamble=ignore_preamble,
            max_preamble_chars=max_preamble_chars,
        )
        self._drain_timeout = drain_timeout
        self._owns_streams = owns_streams

        self._request_lock = threading.Lock()
        self._condition = threading.Condition(threading.Lock())
        self._closed_event = threading.Event()

        self._state = SkillPipeState.READY
        self._response: SkillResponse | object = _MISSING
        self._reader_error: Exception | None = None
        self._failure: Exception | None = None
        self._drain_timer: threading.Timer | None = None

        self._reader_thread = threading.Thread(
            target=self._reader_loop,
            name="skillbridge-pipe-reader",
            daemon=True,
        )
        self._reader_thread.start()

    @property
    def state(self) -> SkillPipeState:
        with self._condition:
            return self._state

    def _reader_loop(self) -> None:
        try:
            while not self._closed_event.is_set():
                response = self._protocol.read_response(self._reader)
                self._publish_response(response)
        except Exception as exc:
            self._publish_reader_failure(exc)

    def _publish_response(self, response: SkillResponse) -> None:
        with self._condition:
            if self._state is SkillPipeState.CLOSED:
                return

            if self._state is SkillPipeState.EXECUTING and self._response is _MISSING:
                self._response = response
                self._condition.notify_all()
                return

            if self._state is SkillPipeState.DRAINING:
                preview = (
                    response.payload[:100] + "..."
                    if len(response.payload) > 100
                    else response.payload
                )
                logger.warning(
                    "late SKILL response after timeout: ok=%s size=%d preview=%r",
                    response.ok,
                    len(response.payload),
                    preview,
                )
                self._cancel_drain_timer_locked()
                self._response = _MISSING
                self._failure = None
                self._state = SkillPipeState.READY
                self._condition.notify_all()
                return

            if self._state in {
                SkillPipeState.DESYNCHRONIZED,
                SkillPipeState.BROKEN,
            }:
                return

            self._mark_desynchronized_locked(
                SkillPipeDesynchronizedError(
                    "unexpected or additional response arrived while no frame was expected"
                )
            )

    def _publish_reader_failure(self, exc: Exception) -> None:
        with self._condition:
            if self._state is SkillPipeState.CLOSED:
                return

            self._failure = exc
            self._reader_error = exc
            self._state = SkillPipeState.BROKEN
            self._cancel_drain_timer_locked()
            self._condition.notify_all()

    @staticmethod
    def _remaining(deadline: float | None) -> float | None:
        if deadline is None:
            return None
        return max(0.0, deadline - time.monotonic())

    def _acquire_request_lock(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        if deadline is None:
            self._request_lock.acquire()
            return

        remaining = self._remaining(deadline)
        assert remaining is not None
        if not self._request_lock.acquire(timeout=remaining):
            raise SkillPipeTimeoutError(
                timeout if timeout is not None else 0.0, phase="serialization"
            )

    def _wait_for_recovery_locked(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        while self._state is SkillPipeState.DRAINING:
            remaining = self._remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0,
                    phase="timeout recovery",
                )
            self._condition.wait(remaining)

    def _raise_for_unusable_state_locked(self) -> None:
        if self._state is SkillPipeState.CLOSED:
            raise SkillPipeClosedError("SKILL pipe is closed")

        if self._state is SkillPipeState.DESYNCHRONIZED:
            desync_error = SkillPipeDesynchronizedError(
                "SKILL pipe is desynchronized; restart the bridge before sending another request"
            )
            if self._failure is not None:
                raise desync_error from self._failure
            raise desync_error

        if self._state is SkillPipeState.BROKEN:
            broken_error = SkillPipeBrokenError("SKILL IPC pipe is broken")
            if self._failure is not None:
                raise broken_error from self._failure
            raise broken_error

        if self._state is not SkillPipeState.READY:
            raise SkillPipeError(
                f"invalid SKILL pipe state while starting request: {self._state.name}"
            )

    def _cancel_drain_timer_locked(self) -> None:
        timer, self._drain_timer = self._drain_timer, None
        if timer is not None:
            timer.cancel()

    def _start_drain_timer_locked(self) -> None:
        self._cancel_drain_timer_locked()
        if self._drain_timeout is None:
            return
        timer = threading.Timer(self._drain_timeout, self._expire_drain)
        timer.name = "skillbridge-drain-timeout"
        timer.daemon = True
        self._drain_timer = timer
        timer.start()

    def _expire_drain(self) -> None:
        with self._condition:
            if self._state is not SkillPipeState.DRAINING:
                return
            self._drain_timer = None
            self._mark_desynchronized_locked(
                SkillPipeDesynchronizedError(
                    f"late SKILL response did not arrive within {self._drain_timeout:g} seconds"
                )
            )

    def _mark_desynchronized_locked(self, failure: Exception) -> None:
        self._failure = failure
        self._state = SkillPipeState.DESYNCHRONIZED
        self._response = _MISSING
        self._cancel_drain_timer_locked()
        self._condition.notify_all()

    def _transition_after_response_timeout_locked(
        self,
        *,
        timeout: float,
    ) -> None:
        failure = SkillPipeTimeoutError(timeout, phase="SKILL response")
        self._failure = failure
        self._response = _MISSING
        self._state = SkillPipeState.DRAINING
        self._start_drain_timer_locked()
        self._condition.notify_all()

    def execute(
        self,
        command: str,
        *,
        timeout: float | None,
    ) -> SkillResponse:
        """Execute one command and return its complete response object."""
        deadline = None if timeout is None else time.monotonic() + timeout

        self._acquire_request_lock(timeout=timeout, deadline=deadline)
        try:
            remaining = self._remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0, phase="serialization"
                )

            with self._condition:
                self._wait_for_recovery_locked(timeout=timeout, deadline=deadline)
                self._raise_for_unusable_state_locked()

                self._response = _MISSING
                self._failure = None
                self._state = SkillPipeState.EXECUTING

                try:
                    self._writer.write(command)
                    if not command.endswith("\n"):
                        self._writer.write("\n")
                    self._writer.flush()
                except Exception as exc:
                    self._failure = exc
                    self._state = SkillPipeState.BROKEN
                    self._condition.notify_all()
                    raise SkillPipeBrokenError(
                        "failed to write command to the SKILL IPC pipe"
                    ) from exc

                while (
                    self._response is _MISSING
                    and self._reader_error is None
                    and self._state is SkillPipeState.EXECUTING
                ):
                    remaining = self._remaining(deadline)
                    if remaining is not None and remaining <= 0.0:
                        break
                    self._condition.wait(remaining)

                if (
                    self._response is _MISSING
                    and self._reader_error is None
                    and self._state is SkillPipeState.EXECUTING
                ):
                    self._transition_after_response_timeout_locked(
                        timeout=timeout if timeout is not None else 0.0
                    )
                    raise SkillPipeTimeoutError(
                        timeout if timeout is not None else 0.0,
                        phase="SKILL response",
                    )

                if self._state is SkillPipeState.CLOSED:
                    raise SkillPipeClosedError("SKILL pipe was closed during execution")

                if self._state is SkillPipeState.DESYNCHRONIZED:
                    desync_error = SkillPipeDesynchronizedError(
                        "SKILL pipe became desynchronized while reading a response"
                    )
                    if self._failure is not None:
                        raise desync_error from self._failure
                    raise desync_error

                if self._response is _MISSING and self._reader_error is not None:
                    if isinstance(self._reader_error, SkillPipeClosedError):
                        raise self._reader_error
                    raise SkillPipeBrokenError("SKILL IPC reader failed") from self._reader_error

                if not isinstance(self._response, SkillResponse):
                    self._mark_desynchronized_locked(
                        SkillPipeDesynchronizedError("SKILL pipe transaction state is inconsistent")
                    )
                    raise SkillPipeDesynchronizedError(
                        "SKILL pipe transaction state is inconsistent"
                    )

                response = self._response
                self._response = _MISSING
                if self._state is not SkillPipeState.BROKEN:
                    self._state = SkillPipeState.READY
                    self._failure = None
                self._condition.notify_all()
                return response
        finally:
            self._request_lock.release()

    def wait_until_ready(self, timeout: float | None = None) -> bool:
        """Wait until recovery finishes; return false on timeout/unusable state."""
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._condition:
            while self._state is SkillPipeState.DRAINING:
                remaining = self._remaining(deadline)
                if remaining is not None and remaining <= 0.0:
                    return False
                self._condition.wait(remaining)
            return self._state is SkillPipeState.READY

    def close(self) -> None:
        """Close the channel and wake any in-flight or recovery waiter."""
        with self._condition:
            if self._state is SkillPipeState.CLOSED:
                return

            self._state = SkillPipeState.CLOSED
            self._closed_event.set()
            self._cancel_drain_timer_locked()
            self._condition.notify_all()

        if self._owns_streams:
            for stream in (self._writer, self._reader):
                try:
                    stream.close()
                except Exception:
                    pass

    def join_reader(self, timeout: float | None = None) -> bool:
        self._reader_thread.join(timeout)
        return not self._reader_thread.is_alive()

    def __enter__(self) -> SkillPipe:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc, traceback
        self.close()
