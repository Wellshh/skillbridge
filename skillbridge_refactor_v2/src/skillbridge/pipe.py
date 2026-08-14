"""Serialized, cross-platform access to a SKILL IPC pipe.

A daemon reader thread owns the blocking read side.  Request threads never call
``select(stdin, ...)``; they wait on thread primitives whose timeouts work on
Windows, macOS, and Linux.

Only one command may be in flight.  In the legacy line protocol, a response
timeout permanently desynchronizes the channel.  With explicit framed
responses, the channel can enter ``DRAINING`` and safely discard exactly one
late response before returning to ``READY``.
"""

from __future__ import annotations

import math
import queue
import threading
import time
from dataclasses import asdict, dataclass
from enum import Enum, auto
from types import TracebackType
from typing import Any, TextIO

from .response_protocol import (
    LineResponseProtocol,
    SkillResponse,
    SkillResponseProtocol,
)


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


class SkillExecutionError(SkillPipeError):
    """SKILL returned a framed error response while the channel stayed valid."""

    def __init__(self, payload: str) -> None:
        self.payload = payload
        super().__init__(payload or "SKILL execution failed")


class SkillPipeState(Enum):
    READY = auto()
    EXECUTING = auto()
    DRAINING = auto()
    DESYNCHRONIZED = auto()
    BROKEN = auto()
    CLOSED = auto()


@dataclass(frozen=True, slots=True)
class SkillPipeSnapshot:
    state: str
    protocol: str
    recover_after_timeout: bool
    total_requests: int
    successful_requests: int
    remote_errors: int
    response_timeouts: int
    serialization_timeouts: int
    recovery_wait_timeouts: int
    recovered_timeouts: int
    failure: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class _ResponseEnvelope:
    request_id: int
    value: SkillResponse | BaseException


class SkillPipe:
    """Serialize complete command/response transactions over text streams.

    Parameters
    ----------
    reader:
        Responses from SKILL, normally ``sys.stdin``.
    writer:
        Commands sent to SKILL, normally ``sys.stdout``.
    response_protocol:
        ``LineResponseProtocol`` for compatibility, or an explicit framed
        protocol for multiline results and safe late-response draining.
    recover_after_timeout:
        ``None`` selects the protocol's safe default.  Enabling recovery for a
        protocol that cannot identify complete frames is rejected.
    drain_timeout:
        Maximum time to wait for the late framed response.  ``None`` leaves the
        channel in DRAINING indefinitely until a frame or I/O failure arrives.
    owns_streams:
        Close reader and writer from :meth:`close`; keep false for process-wide
        ``sys.stdin`` and ``sys.stdout``.
    """

    def __init__(
        self,
        reader: TextIO,
        writer: TextIO,
        *,
        response_protocol: SkillResponseProtocol | None = None,
        recover_after_timeout: bool | None = None,
        drain_timeout: float | None = 30.0,
        owns_streams: bool = False,
        thread_name: str = "skillbridge-pipe-reader",
    ) -> None:
        protocol = response_protocol or LineResponseProtocol()
        recovery = (
            protocol.recoverable_after_timeout
            if recover_after_timeout is None
            else recover_after_timeout
        )
        if recovery and not protocol.recoverable_after_timeout:
            raise ValueError(
                f"response protocol {protocol.name!r} cannot safely recover after a timeout"
            )
        self._validate_optional_timeout(drain_timeout, name="drain_timeout")

        self._reader = reader
        self._writer = writer
        self._protocol = protocol
        self._recover_after_timeout = recovery
        self._drain_timeout = drain_timeout
        self._owns_streams = owns_streams

        self._responses: queue.Queue[_ResponseEnvelope] = queue.Queue()
        self._request_lock = threading.Lock()
        self._condition = threading.Condition(threading.Lock())
        self._closed_event = threading.Event()

        self._state = SkillPipeState.READY
        self._failure: BaseException | None = None
        self._pending_request_id: int | None = None
        self._response_enqueued = False
        self._next_request_id = 1
        self._drain_timer: threading.Timer | None = None

        self._total_requests = 0
        self._successful_requests = 0
        self._remote_errors = 0
        self._response_timeouts = 0
        self._serialization_timeouts = 0
        self._recovery_wait_timeouts = 0
        self._recovered_timeouts = 0

        self._reader_thread = threading.Thread(
            target=self._reader_loop,
            name=thread_name,
            daemon=True,
        )
        self._reader_thread.start()

    @property
    def state(self) -> SkillPipeState:
        with self._condition:
            return self._state

    @property
    def protocol_name(self) -> str:
        return self._protocol.name

    @property
    def recover_after_timeout(self) -> bool:
        return self._recover_after_timeout

    @property
    def desynchronized(self) -> bool:
        return self.state is SkillPipeState.DESYNCHRONIZED

    @property
    def recovering(self) -> bool:
        return self.state is SkillPipeState.DRAINING

    @property
    def closed(self) -> bool:
        return self.state is SkillPipeState.CLOSED

    @property
    def reader_thread_alive(self) -> bool:
        return self._reader_thread.is_alive()

    def snapshot(self) -> SkillPipeSnapshot:
        with self._condition:
            return SkillPipeSnapshot(
                state=self._state.name,
                protocol=self._protocol.name,
                recover_after_timeout=self._recover_after_timeout,
                total_requests=self._total_requests,
                successful_requests=self._successful_requests,
                remote_errors=self._remote_errors,
                response_timeouts=self._response_timeouts,
                serialization_timeouts=self._serialization_timeouts,
                recovery_wait_timeouts=self._recovery_wait_timeouts,
                recovered_timeouts=self._recovered_timeouts,
                failure=None if self._failure is None else repr(self._failure),
            )

    def _reader_loop(self) -> None:
        try:
            while not self._closed_event.is_set():
                response = self._protocol.read_response(self._reader)
                self._publish_response(response)
        except BaseException as exc:
            self._publish_reader_failure(exc)

    def _publish_response(self, response: SkillResponse) -> None:
        with self._condition:
            if self._state is SkillPipeState.CLOSED:
                return

            if (
                self._state is SkillPipeState.EXECUTING
                and self._pending_request_id is not None
                and not self._response_enqueued
            ):
                request_id = self._pending_request_id
                self._responses.put(_ResponseEnvelope(request_id, response))
                self._response_enqueued = True
                self._condition.notify_all()
                return

            if self._state is SkillPipeState.DRAINING:
                # Exactly one complete framed response belongs to the timed-out
                # request.  Discard it, cancel the recovery watchdog, and reopen
                # the channel for the next transaction.
                self._cancel_drain_timer_locked()
                self._pending_request_id = None
                self._response_enqueued = False
                self._failure = None
                self._state = SkillPipeState.READY
                self._recovered_timeouts += 1
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

    def _publish_reader_failure(self, exc: BaseException) -> None:
        with self._condition:
            if self._state is SkillPipeState.CLOSED:
                return

            request_id = self._pending_request_id
            self._failure = exc
            self._state = SkillPipeState.BROKEN
            self._cancel_drain_timer_locked()

            if request_id is not None and not self._response_enqueued:
                self._responses.put(_ResponseEnvelope(request_id, exc))
                self._response_enqueued = True
            self._condition.notify_all()

    @staticmethod
    def _validate_optional_timeout(value: float | None, *, name: str) -> None:
        if value is None:
            return
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be None or a finite non-negative number")

    @classmethod
    def _validate_timeout(cls, timeout: float | None) -> None:
        cls._validate_optional_timeout(timeout, name="timeout")

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
            with self._condition:
                self._serialization_timeouts += 1
            raise SkillPipeTimeoutError(timeout, phase="serialization")

    def _wait_for_recovery_locked(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        while self._state is SkillPipeState.DRAINING:
            remaining = self._remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                self._recovery_wait_timeouts += 1
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0,
                    phase="timeout recovery",
                )
            self._condition.wait(remaining)

    def _raise_for_unusable_state_locked(self) -> None:
        if self._state is SkillPipeState.CLOSED:
            raise SkillPipeClosedError("SKILL pipe is closed")

        if self._state is SkillPipeState.DESYNCHRONIZED:
            error = SkillPipeDesynchronizedError(
                "SKILL pipe is desynchronized; restart the bridge before sending another request"
            )
            if self._failure is not None:
                raise error from self._failure
            raise error

        if self._state is SkillPipeState.BROKEN:
            error = SkillPipeBrokenError("SKILL IPC pipe is broken")
            if self._failure is not None:
                raise error from self._failure
            raise error

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

    def _mark_desynchronized_locked(self, failure: BaseException) -> None:
        self._failure = failure
        self._state = SkillPipeState.DESYNCHRONIZED
        self._pending_request_id = None
        self._response_enqueued = False
        self._cancel_drain_timer_locked()
        self._condition.notify_all()

    def _transition_after_response_timeout_locked(
        self,
        *,
        timeout: float,
    ) -> None:
        self._response_timeouts += 1
        failure = SkillPipeTimeoutError(timeout, phase="SKILL response")
        self._failure = failure
        self._response_enqueued = False

        if self._recover_after_timeout:
            self._state = SkillPipeState.DRAINING
            self._start_drain_timer_locked()
        else:
            self._mark_desynchronized_locked(failure)
        self._condition.notify_all()

    def execute(
        self,
        command: str,
        *,
        timeout: float | None,
    ) -> str:
        """Execute one command and return its payload.

        The timeout is one total deadline from method entry.  It includes
        serializer wait, timeout-recovery wait, write/flush, SKILL execution,
        and response delivery.
        """

        self._validate_timeout(timeout)
        deadline = None if timeout is None else time.monotonic() + timeout

        self._acquire_request_lock(timeout=timeout, deadline=deadline)
        try:
            if deadline is not None and self._remaining(deadline) <= 0.0:
                with self._condition:
                    self._serialization_timeouts += 1
                raise SkillPipeTimeoutError(timeout, phase="serialization")

            with self._condition:
                self._wait_for_recovery_locked(timeout=timeout, deadline=deadline)
                self._raise_for_unusable_state_locked()

                request_id = self._next_request_id
                self._next_request_id += 1
                self._pending_request_id = request_id
                self._response_enqueued = False
                self._failure = None
                self._state = SkillPipeState.EXECUTING
                self._total_requests += 1

                try:
                    self._writer.write(command)
                    if not command.endswith("\n"):
                        self._writer.write("\n")
                    self._writer.flush()
                except BaseException as exc:
                    self._failure = exc
                    self._state = SkillPipeState.BROKEN
                    self._pending_request_id = None
                    self._condition.notify_all()
                    raise SkillPipeBrokenError(
                        "failed to write command to the SKILL IPC pipe"
                    ) from exc

            remaining = self._remaining(deadline)
            try:
                if remaining is None:
                    envelope = self._responses.get()
                elif remaining <= 0.0:
                    envelope = self._responses.get_nowait()
                else:
                    envelope = self._responses.get(timeout=remaining)
            except queue.Empty as exc:
                with self._condition:
                    if (
                        self._state is SkillPipeState.EXECUTING
                        and self._pending_request_id == request_id
                    ):
                        self._transition_after_response_timeout_locked(
                            timeout=timeout if timeout is not None else 0.0
                        )
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0,
                    phase="SKILL response",
                ) from exc

            if envelope.request_id != request_id:
                with self._condition:
                    self._mark_desynchronized_locked(
                        SkillPipeDesynchronizedError("received a response for a different request")
                    )
                raise SkillPipeDesynchronizedError(
                    "received a response for a different request; restart the bridge"
                )

            if isinstance(envelope.value, BaseException):
                with self._condition:
                    if self._state is not SkillPipeState.CLOSED:
                        self._state = SkillPipeState.BROKEN
                        self._failure = envelope.value
                    self._pending_request_id = None
                    self._condition.notify_all()
                if isinstance(envelope.value, SkillPipeClosedError):
                    raise envelope.value
                raise SkillPipeBrokenError("SKILL IPC reader failed") from envelope.value

            with self._condition:
                if self._state is SkillPipeState.CLOSED:
                    self._pending_request_id = None
                    raise SkillPipeClosedError("SKILL pipe was closed during execution")

                if self._state is SkillPipeState.DESYNCHRONIZED:
                    self._pending_request_id = None
                    error = SkillPipeDesynchronizedError(
                        "SKILL pipe became desynchronized while reading a response"
                    )
                    if self._failure is not None:
                        raise error from self._failure
                    raise error

                if self._state is SkillPipeState.BROKEN:
                    self._pending_request_id = None
                    error = SkillPipeBrokenError("SKILL IPC pipe failed during execution")
                    if self._failure is not None:
                        raise error from self._failure
                    raise error

                if (
                    self._state is not SkillPipeState.EXECUTING
                    or self._pending_request_id != request_id
                    or not self._response_enqueued
                ):
                    self._mark_desynchronized_locked(
                        SkillPipeDesynchronizedError("SKILL pipe transaction state is inconsistent")
                    )
                    raise SkillPipeDesynchronizedError(
                        "SKILL pipe transaction state is inconsistent"
                    )

                response = envelope.value
                self._state = SkillPipeState.READY
                self._pending_request_id = None
                self._response_enqueued = False
                self._failure = None
                if response.ok:
                    self._successful_requests += 1
                else:
                    self._remote_errors += 1
                self._condition.notify_all()

            if not response.ok:
                raise SkillExecutionError(response.payload)
            return response.payload
        finally:
            self._request_lock.release()

    def wait_until_ready(self, timeout: float | None = None) -> bool:
        """Wait until recovery finishes; return false on timeout/unusable state."""

        self._validate_timeout(timeout)
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

            pending_request_id = self._pending_request_id
            should_wake = (
                self._state is SkillPipeState.EXECUTING
                and pending_request_id is not None
                and not self._response_enqueued
            )
            self._state = SkillPipeState.CLOSED
            self._closed_event.set()
            self._cancel_drain_timer_locked()

            if should_wake:
                self._responses.put(
                    _ResponseEnvelope(
                        pending_request_id,
                        SkillPipeClosedError("SKILL pipe was closed"),
                    )
                )
                self._response_enqueued = True
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
