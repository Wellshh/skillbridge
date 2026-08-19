from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from contextlib import suppress
from enum import Enum, auto
from types import TracebackType
from typing import TextIO

from skillbridge.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeError,
    SkillPipeTimeoutError,
)
from skillbridge.protocol.response import Response, SkillResp

logger = logging.getLogger(__name__)

_MISSING = object()


class _DrainTimer:
    """Watch dog timer for pipe drain state."""

    __slots__ = ("_timeout", "_timer")

    _timeout: float | None
    _timer: threading.Timer | None

    def __init__(self, timeout: float | None = 30.0) -> None:
        self._timeout = timeout
        self._timer = None

    def start(self, on_expired: Callable[[], None]) -> None:
        self.cancel()
        if self._timeout is None:
            return
        timer = threading.Timer(self._timeout, on_expired)
        timer.name = "skillbridge-drain-timeout"
        timer.daemon = True
        self._timer = timer
        timer.start()

    def cancel(self) -> None:
        timer, self._timer = self._timer, None
        if timer is not None:
            timer.cancel()


class _PipeState(Enum):
    READY = auto()
    EXECUTING = auto()
    DRAINING = auto()
    DESYNCHRONIZED = auto()
    BROKEN = auto()
    CLOSED = auto()


class Pipe:
    __slots__ = (
        "_cause",
        "_decoder",
        "_drain",
        "_lock",
        "_reader",
        "_resp",
        "_state",
        "_sync",
        "_thread",
        "_writer",
    )

    _cause: Exception | None
    """The exception cause of reader and its downstream."""

    _decoder: Response
    _drain: _DrainTimer
    _lock: threading.Lock
    _reader: TextIO
    _resp: SkillResp | object
    _state: _PipeState
    _sync: threading.Condition
    _thread: threading.Thread
    _writer: TextIO

    def __init__(
        self,
        reader: TextIO,
        writer: TextIO,
        *,
        drain_timeout: float | None = 30.0,
        max_payload_chars: int = Response.DEFAULT_MAX_PAYLOAD_CHARS,
        ignore_preamble: bool = False,
        max_preamble_chars: int = Response.DEFAULT_MAX_PREAMBLE_CHARS,
    ) -> None:
        self._reader = reader
        self._writer = writer
        self._decoder = Response(
            reader,
            max_payload_chars=max_payload_chars,
            ignore_preamble=ignore_preamble,
            max_preamble_chars=max_preamble_chars,
        )
        self._drain = _DrainTimer(drain_timeout)

        self._lock = threading.Lock()
        self._sync = threading.Condition(threading.Lock())

        self._state = _PipeState.READY
        self._resp = _MISSING
        self._cause = None

        self._start()

    def __enter__(self) -> Pipe:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc, traceback
        self.close()

    @property
    def state(self) -> _PipeState:
        with self._sync:
            return self._state

    @staticmethod
    def _remaining(deadline: float | None) -> float | None:
        if deadline is None:
            return None
        return max(0.0, deadline - time.monotonic())

    def wait_until_ready(self, timeout: float | None = None) -> bool:
        """Wait until recovery finishes; return false on timeout/unusable state."""
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._sync:
            while self._state is _PipeState.DRAINING:
                remaining = self._remaining(deadline)
                if remaining is not None and remaining <= 0.0:
                    return False
                self._sync.wait(remaining)
            return self._state is _PipeState.READY

    def close(self) -> None:
        """Close the command stream; the reader exits after the peer closes its response."""
        with self._sync:
            if self._state is _PipeState.CLOSED:
                return

            self._state = _PipeState.CLOSED
            self._drain.cancel()
            self._sync.notify_all()

        with suppress(OSError):
            self._writer.close()

    def wait_closed(self, timeout: float | None = None) -> bool:
        """Wait for the reader thread; return false if the peer has not closed its response."""
        self._thread.join(timeout)
        return not self._thread.is_alive()

    def execute(
        self,
        cmd: str,
        *,
        timeout: float | None = None,
    ) -> SkillResp:
        """Execute one command and return its complete response object."""
        deadline = None if timeout is None else time.monotonic() + timeout

        self._acquire_lock(timeout=timeout, deadline=deadline)
        try:
            remaining = self._remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0, phase="serialization"
                )

            with self._sync:
                # Wait for stale frames to drain, ensure channel health, and dispatch command
                self._wait_draining(timeout=timeout, deadline=deadline)
                self._check_usable()

                self._resp = _MISSING
                self._cause = None
                self._state = _PipeState.EXECUTING

                try:
                    self._writer.write(cmd)
                    if not cmd.endswith("\n"):
                        self._writer.write("\n")
                    self._writer.flush()
                except Exception as exc:
                    self._cause = exc
                    self._state = _PipeState.BROKEN
                    self._sync.notify_all()
                    raise SkillPipeBrokenError(
                        "failed to write command to the SKILL IPC pipe"
                    ) from exc

                while (
                    self._resp is _MISSING
                    and self._cause is None
                    and self._state is _PipeState.EXECUTING
                ):
                    remaining = self._remaining(deadline)
                    if remaining is not None and remaining <= 0.0:
                        break
                    self._sync.wait(remaining)

                # Timeout on response triggers DRAINING watchdog to absorb late frames
                if (
                    self._resp is _MISSING
                    and self._cause is None
                    and self._state is _PipeState.EXECUTING
                ):
                    self._enter_draining(timeout=timeout if timeout is not None else 0.0)
                    raise SkillPipeTimeoutError(
                        timeout if timeout is not None else 0.0,
                        phase="SKILL response",
                    )

                if self._state is _PipeState.CLOSED:
                    raise SkillPipeClosedError("SKILL pipe was closed during execution")

                if self._state is _PipeState.DESYNCHRONIZED:
                    desync_error = SkillPipeDesynchronizedError(
                        "SKILL pipe became desynchronized while reading a response"
                    )
                    if self._cause is not None:
                        raise desync_error from self._cause
                    raise desync_error

                if self._resp is _MISSING and self._cause is not None:
                    raise SkillPipeBrokenError("SKILL IPC reader failed") from self._cause

                if not isinstance(self._resp, SkillResp):
                    self._desync(
                        SkillPipeDesynchronizedError("SKILL pipe transaction state is inconsistent")
                    )
                    raise SkillPipeDesynchronizedError(
                        "SKILL pipe transaction state is inconsistent"
                    )

                # Consume response and restore channel to READY state
                resp = self._resp
                self._resp = _MISSING
                if self._state is not _PipeState.BROKEN:
                    self._state = _PipeState.READY
                    self._cause = None
                self._sync.notify_all()
                return resp
        finally:
            self._lock.release()

    def _acquire_lock(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        if deadline is None:
            self._lock.acquire()
            return

        remaining = self._remaining(deadline)
        assert remaining is not None
        if not self._lock.acquire(timeout=remaining):
            raise SkillPipeTimeoutError(
                timeout if timeout is not None else 0.0, phase="serialization"
            )

    def _wait_draining(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> None:
        while self._state is _PipeState.DRAINING:
            remaining = self._remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0,
                    phase="timeout recovery",
                )
            self._sync.wait(remaining)

    def _check_usable(self) -> None:
        if self._state is _PipeState.CLOSED:
            raise SkillPipeClosedError("SKILL pipe is closed")

        if self._state is _PipeState.DESYNCHRONIZED:
            desync_error = SkillPipeDesynchronizedError(
                "SKILL pipe is desynchronized; restart the bridge before sending another request"
            )
            if self._cause is not None:
                raise desync_error from self._cause
            raise desync_error

        if self._state is _PipeState.BROKEN:
            broken_error = SkillPipeBrokenError("SKILL IPC pipe is broken")
            if self._cause is not None:
                raise broken_error from self._cause
            raise broken_error

        if self._state is not _PipeState.READY:
            raise SkillPipeError(
                f"invalid SKILL pipe state while starting request: {self._state.name}"
            )

    def _enter_draining(self, *, timeout: float) -> None:
        self._cause = SkillPipeTimeoutError(timeout, phase="SKILL response")
        self._resp = _MISSING
        self._state = _PipeState.DRAINING
        self._drain.start(self._expire_drain)
        self._sync.notify_all()

    def _expire_drain(self) -> None:
        with self._sync:
            if self._state is not _PipeState.DRAINING:
                return
            timeout = self._drain._timeout
            timeout_str = f"{timeout:g}" if timeout is not None else "configured"
            self._desync(
                SkillPipeDesynchronizedError(
                    f"late SKILL response did not arrive within {timeout_str} seconds"
                )
            )

    def _start(self) -> None:

        def loop() -> None:
            try:
                while True:
                    with self._sync:
                        if self._state is _PipeState.CLOSED:
                            break
                    resp = self._decoder.recv()
                    self._publish(resp)
            except Exception as exc:
                self._publish(exc)
            finally:
                with suppress(OSError):
                    self._reader.close()

        self._thread = threading.Thread(
            target=loop,
            name="skillbridge-pipe-reader",
            daemon=True,
        )
        self._thread.start()

    def _publish(self, event: SkillResp | Exception) -> None:
        with self._sync:
            # Deliver response when EXECUTING, discard stale frame to recover READY
            # when DRAINING, fail on stream error, and desync on unexpected idle frames.
            if self._state is _PipeState.CLOSED:
                return

            if isinstance(event, Exception):
                self._cause = event
                self._state = _PipeState.BROKEN
                self._drain.cancel()
                self._sync.notify_all()
                return

            if self._state is _PipeState.EXECUTING and self._resp is _MISSING:
                self._resp = event
                self._sync.notify_all()
                return

            if self._state is _PipeState.DRAINING:
                preview = event.payload[:100] + "..." if len(event.payload) > 100 else event.payload
                logger.warning(
                    "late SKILL response after timeout: status=%s size=%d preview=%r",
                    event.status,
                    len(event.payload),
                    preview,
                )
                self._drain.cancel()
                self._resp = _MISSING
                self._cause = None
                self._state = _PipeState.READY
                self._sync.notify_all()
                return

            if self._state in {_PipeState.DESYNCHRONIZED, _PipeState.BROKEN}:
                return

            self._desync(
                SkillPipeDesynchronizedError(
                    "unexpected or additional response arrived while no frame was expected"
                )
            )

    def _desync(self, failure: Exception) -> None:
        """Transition pipe into unrecoverable DESYNCHRONIZED state and wake all waiters."""
        self._cause = failure
        self._state = _PipeState.DESYNCHRONIZED
        self._resp = _MISSING
        self._drain.cancel()
        self._sync.notify_all()
