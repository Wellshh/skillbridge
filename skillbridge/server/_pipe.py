# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import logging
import math
import threading
import time
from collections.abc import Callable
from contextlib import suppress
from enum import Enum, auto
from types import TracebackType
from typing import TextIO, cast

from skillbridge.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeTimeoutError,
)
from skillbridge.protocol.response import Response, SkillResp

logger = logging.getLogger(__name__)

_MISSING = object()
_PREVIEW_CHARS = 100


def _remaining(deadline: float | None) -> float | None:
    if deadline is None:
        return None
    return max(0.0, deadline - time.monotonic())


class _DrainTimer:
    """Watchdog timer for pipe drain state."""

    __slots__ = ("_timeout", "_timer")

    _timeout: float | None
    _timer: threading.Timer | None

    def __init__(self, timeout: float | None = 30.0) -> None:
        self._timeout = timeout
        self._timer = None

    @property
    def timeout(self) -> float | None:
        return self._timeout

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


class _StateMachine:
    __slots__ = (
        "_cause",
        "_drain",
        "_resp",
        "_state",
        "_sync",
    )

    _cause: Exception | None
    _drain: _DrainTimer
    _resp: SkillResp | object
    _state: _PipeState
    _sync: threading.Condition

    def __init__(self, drain_timeout: float | None) -> None:
        self._cause = None
        self._drain = _DrainTimer(drain_timeout)
        self._resp = _MISSING
        self._state = _PipeState.READY
        self._sync = threading.Condition(threading.Lock())

    @property
    def state(self) -> _PipeState:
        with self._sync:
            return self._state

    def wait_until_ready(self, timeout: float | None) -> bool:
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._sync:
            while self._state is _PipeState.DRAINING:
                remaining = _remaining(deadline)
                if remaining is not None and remaining <= 0.0:
                    return False
                self._sync.wait(remaining)
            return self._state is _PipeState.READY

    def close(self) -> bool:
        with self._sync:
            if self._state is _PipeState.CLOSED:
                return False
            self._state = _PipeState.CLOSED
            self._drain.cancel()
            self._sync.notify_all()
            return True

    def begin(self, *, timeout: float | None, deadline: float | None) -> None:
        with self._sync:
            while self._state is _PipeState.DRAINING:
                remaining = _remaining(deadline)
                if remaining is not None and remaining <= 0.0:
                    raise SkillPipeTimeoutError(
                        timeout if timeout is not None else 0.0,
                        phase="timeout recovery",
                    )
                self._sync.wait(remaining)

            if self._state is _PipeState.CLOSED:
                raise SkillPipeClosedError("SKILL pipe is closed")
            if self._state is _PipeState.DESYNCHRONIZED:
                desync_error = SkillPipeDesynchronizedError(
                    "SKILL pipe is desynchronized; "
                    "restart the bridge before sending another request"
                )
                raise desync_error from self._cause
            if self._state is _PipeState.BROKEN:
                broken_error = SkillPipeBrokenError("SKILL IPC pipe is broken")
                raise broken_error from self._cause

            self._state = _PipeState.EXECUTING

    def write_failed(self, failure: Exception) -> bool:
        with self._sync:
            if self._state is _PipeState.CLOSED:
                return False
            self._cause = failure
            self._state = _PipeState.BROKEN
            self._sync.notify_all()
            return True

    def wait_response(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> SkillResp:
        with self._sync:

            def is_waiting() -> bool:
                return (
                    self._resp is _MISSING
                    and self._cause is None
                    and self._state is _PipeState.EXECUTING
                )

            while is_waiting():
                remaining = _remaining(deadline)
                if remaining is not None and remaining <= 0.0:
                    break
                self._sync.wait(remaining)

            if is_waiting():
                self._state = _PipeState.DRAINING
                self._drain.start(self._expire_drain)
                self._sync.notify_all()
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0, phase="SKILL response"
                )

            if self._state is _PipeState.CLOSED:
                raise SkillPipeClosedError("SKILL pipe was closed during execution")
            if self._state is _PipeState.DESYNCHRONIZED:
                failure = SkillPipeDesynchronizedError(
                    "SKILL pipe became desynchronized while reading a response"
                )
                raise failure from self._cause
            if self._resp is _MISSING and self._cause is not None:
                raise SkillPipeBrokenError("SKILL IPC reader failed") from self._cause

            resp = cast("SkillResp", self._resp)
            self._resp = _MISSING
            if self._state is not _PipeState.BROKEN:
                self._state = _PipeState.READY
                self._cause = None
            return resp

    def publish(self, event: SkillResp | Exception) -> None:
        with self._sync:
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
                assert isinstance(event, SkillResp)
                preview = (
                    event.payload[:_PREVIEW_CHARS] + "..."
                    if len(event.payload) > _PREVIEW_CHARS
                    else event.payload
                )
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
            if self._state not in {_PipeState.DESYNCHRONIZED, _PipeState.BROKEN}:
                self._desync(
                    SkillPipeDesynchronizedError(
                        "unexpected or additional response arrived while no frame was expected"
                    )
                )

    def _expire_drain(self) -> None:
        with self._sync:
            if self._state is not _PipeState.DRAINING:
                return
            timeout = self._drain.timeout
            timeout_str = f"{timeout:g}" if timeout is not None else "configured"
            self._desync(
                SkillPipeDesynchronizedError(
                    f"late SKILL response did not arrive within {timeout_str} seconds"
                )
            )

    def _desync(self, failure: Exception) -> None:
        self._cause = failure
        self._state = _PipeState.DESYNCHRONIZED
        self._resp = _MISSING
        self._drain.cancel()
        self._sync.notify_all()


class Pipe:
    __slots__ = (
        "_decoder",
        "_lock",
        "_machine",
        "_reader",
        "_thread",
        "_writer",
    )

    _decoder: Response
    _lock: threading.Lock
    _machine: _StateMachine
    _reader: TextIO
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
        self._lock = threading.Lock()
        self._machine = _StateMachine(drain_timeout)

        self._start()

    def __enter__(self) -> Pipe:  # ruff: ignore[non-self-return-type] - Python 3.8
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
        return self._machine.state

    def wait_until_ready(self, timeout: float | None = None) -> bool:
        """Wait until recovery finishes.

        Returns:
            Whether the pipe reached the ready state before the timeout.
        """
        return self._machine.wait_until_ready(timeout)

    def close(self) -> None:
        """Close the command stream; the reader exits after the peer closes its response."""
        if self._machine.close():
            with suppress(OSError):
                self._writer.close()

    def wait_closed(self, timeout: float | None = None) -> bool:
        """Wait for the reader thread.

        Returns:
            Whether the peer closed its response stream before the timeout.
        """
        self._thread.join(timeout)
        return not self._thread.is_alive()

    def wait_peer_closed(self, timeout: float | None = None) -> bool:
        """Wait for the reader thread and report whether the peer ended the pipe.

        Returns:
            Whether the reader thread exited without a prior local close.
        """
        if not self.wait_closed(timeout):
            return False
        return self._machine.state is not _PipeState.CLOSED

    def execute(
        self,
        cmd: str,
        *,
        timeout: float | None = None,
    ) -> SkillResp:
        """Execute one command and return its complete response object.

        Returns:
            The complete SKILL response.

        Raises:
            ValueError: If the timeout is negative or not finite.
            SkillPipeClosedError: If the pipe is closed.
            SkillPipeBrokenError: If the pipe broke while executing.
            SkillPipeTimeoutError: If the command did not finish in time.
        """
        if timeout is not None and (timeout < 0.0 or not math.isfinite(timeout)):
            raise ValueError("timeout must be None or a non-negative finite number")
        deadline = None if timeout is None else time.monotonic() + timeout

        if deadline is None:
            self._lock.acquire()
        else:
            remaining = _remaining(deadline)
            assert remaining is not None
            if not self._lock.acquire(timeout=remaining):
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0, phase="serialization"
                )

        try:
            remaining = _remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                raise SkillPipeTimeoutError(
                    timeout if timeout is not None else 0.0, phase="serialization"
                )

            self._machine.begin(timeout=timeout, deadline=deadline)
            try:
                self._writer.write(cmd)
                if not cmd.endswith("\n"):
                    self._writer.write("\n")
                self._writer.flush()
            except Exception as exc:
                if not self._machine.write_failed(exc):
                    raise SkillPipeClosedError(
                        "SKILL pipe was closed while writing a command"
                    ) from exc
                raise SkillPipeBrokenError("failed to write command to the SKILL IPC pipe") from exc

            response = self._machine.wait_response(timeout=timeout, deadline=deadline)
            if response.status == 'restart':
                self.close()
            return response
        finally:
            self._lock.release()

    def _start(self) -> None:
        def loop() -> None:
            try:
                while True:
                    resp = self._decoder.recv()
                    self._machine.publish(resp)
            except Exception as exc:  # ruff: ignore[blind-except] - publish reader failure
                self._machine.publish(exc)
            finally:
                with suppress(OSError):
                    self._reader.close()

        self._thread = threading.Thread(
            target=loop,
            name="skillbridge-pipe-reader",
            daemon=True,
        )
        self._thread.start()
