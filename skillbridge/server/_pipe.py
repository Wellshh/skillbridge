from __future__ import annotations

import logging
import threading
from collections.abc import Callable
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
    ) -> None: ...

    @property
    def state(self) -> _PipeState:
        with self._sync:
            return self._state

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
