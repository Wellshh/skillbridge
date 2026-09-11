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
from io import BufferedIOBase
from types import TracebackType
from typing import TextIO, cast

from allegrobridge._kernel.exception import (
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeInvalidCommandError,
    SkillPipeTimeoutError,
)
from allegrobridge._kernel.protocol.response import Response, SkillResp

logger = logging.getLogger(__name__)

_MISSING = object()
_PREVIEW_CHARS = 100


def _remaining(deadline: float | None) -> float | None:
    if deadline is None:
        return None
    return max(0.0, deadline - time.monotonic())


def _command_line(cmd: str) -> str:
    if cmd.endswith('\r\n'):
        cmd = cmd[:-2]
    elif cmd.endswith('\n'):
        cmd = cmd[:-1]
    if not cmd or cmd.isspace() or '\n' in cmd or '\r' in cmd:
        raise SkillPipeInvalidCommandError
    return cmd


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
        timer.name = "allegrobridge-drain-timeout"
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
    RESTARTING = auto()
    CLOSED = auto()


class _StateMachine:
    """Synchronization and lifecycle state machine for the serialized IPC pipe.

    State Transition Diagram:

                    +-------------------------+
                    |          READY          |<-----------------------+
                    +-------------------------+                        |
                       |                   |                           |
              begin()  |                   | close()                   |
                       v                   v                           |
           +-------------------+       +--------+                      |
           |     EXECUTING     |       | CLOSED |<----+                |
           +-------------------+       +--------+     |                |
             |       |       |            ^           |                |
     write   |       |       | resp       | close()   | close()        |
     timeout |       |       | timeout    |           |                |
     or fail |       |       v            |           |                |
             |       |   +----------+     |           |                |
             |       |   | DRAINING |-----+           |                |
             |       |   +----------+                 |                |
             |       |     |      |                   | late resp      |
             |       |     |      | watchdog          | (non-RST)      |
             |       |     |      | expired           |                |
             |       |     |      v                   |                |
             |       |     |   +----------------+     |                |
             |       |     |   | DESYNCHRONIZED |     |                |
             |       |     |   +----------------+     |                |
             |       |     |                          |                |
             |       |     | late RST                 |                |
             |       |     +--------------------+     |                |
             |       |                          |     |                |
             |       | resp (RST)               v     |                |
             |       +------------------->+------------+               |
             |                            | RESTARTING |               |
             |                            +------------+               |
             |                                                         |
             | resp (non-RST) consumed                                 |
             +---------------------------------------------------------+
             |
             v (writer/reader failure or write timeout)
       +------------+
       |   BROKEN   |
       +------------+
    """

    __slots__ = (
        "_cause",
        "_command",
        "_drain",
        "_drain_generation",
        "_resp",
        "_state",
        "_sync",
        "_writer_stopping",
        "_writing",
    )

    _cause: Exception | None
    _drain: _DrainTimer
    _drain_generation: int
    _command: str | None
    _writing: bool
    _writer_stopping: bool
    _resp: SkillResp | object
    _state: _PipeState
    _sync: threading.Condition

    def __init__(self, drain_timeout: float | None) -> None:
        self._cause = None
        self._drain = _DrainTimer(drain_timeout)
        self._drain_generation = 0
        self._command = None
        self._writing = False
        self._writer_stopping = False
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
            self._command = None
            self._writing = False
            self._writer_stopping = True
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
            if self._state is _PipeState.RESTARTING:
                raise SkillPipeClosedError("SKILL pipe is restarting")
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

    def queue_command(self, command: str) -> None:
        with self._sync:
            if self._state is _PipeState.CLOSED or self._state is _PipeState.RESTARTING:
                raise SkillPipeClosedError("SKILL pipe is closed")
            if self._state is _PipeState.BROKEN:
                raise SkillPipeBrokenError("SKILL IPC pipe is broken") from self._cause
            if self._state is _PipeState.DESYNCHRONIZED:
                raise SkillPipeDesynchronizedError(
                    "SKILL pipe is desynchronized; restart the bridge before "
                    "sending another request"
                ) from self._cause
            if self._state is not _PipeState.EXECUTING:
                raise SkillPipeBrokenError("SKILL pipe is not executing")
            self._command = command + '\n'
            self._writing = True
            self._sync.notify_all()

    def take_command(self) -> str | None:
        with self._sync:
            while self._command is None and not self._writer_stopping:
                self._sync.wait()
            command, self._command = self._command, None
            return command

    def write_completed(self, failure: Exception | None) -> None:
        with self._sync:
            if failure is not None and self._state is _PipeState.EXECUTING:
                self._state = _PipeState.BROKEN
                self._cause = failure
                self._resp = _MISSING
            self._writing = False
            self._sync.notify_all()

    def stop_writer(self) -> None:
        with self._sync:
            self._writer_stopping = True
            self._command = None
            self._sync.notify_all()

    def wait_response(
        self,
        *,
        timeout: float | None,
        deadline: float | None,
    ) -> SkillResp:
        with self._sync:
            while self._state is _PipeState.EXECUTING and self._writing:
                remaining = _remaining(deadline)
                if remaining is not None and remaining <= 0.0:
                    raise self._break_on_write_timeout(timeout)
                self._sync.wait(remaining)

            self._wait_for_response(timeout, deadline)

            if self._state is _PipeState.CLOSED:
                raise SkillPipeClosedError("SKILL pipe was closed during execution")
            if self._state is _PipeState.DESYNCHRONIZED:
                failure = SkillPipeDesynchronizedError(
                    "SKILL pipe became desynchronized while reading a response"
                )
                raise failure from self._cause
            if self._state is _PipeState.BROKEN and self._resp is _MISSING:
                raise SkillPipeBrokenError("SKILL IPC reader or writer failed") from self._cause

            resp = cast("SkillResp", self._resp)
            self._resp = _MISSING
            if self._state not in {_PipeState.BROKEN, _PipeState.RESTARTING}:
                self._state = _PipeState.READY
                self._cause = None
            return resp

    def _break_on_write_timeout(self, timeout: float | None) -> SkillPipeTimeoutError:
        failure = SkillPipeTimeoutError(
            timeout if timeout is not None else 0.0,
            phase="command write",
        )
        self._cause = failure
        self._state = _PipeState.BROKEN
        self._command = None
        self._resp = _MISSING
        self._writing = False
        self._writer_stopping = True
        self._sync.notify_all()
        return failure

    def _wait_for_response(self, timeout: float | None, deadline: float | None) -> None:
        while self._state is _PipeState.EXECUTING and self._resp is _MISSING:
            remaining = _remaining(deadline)
            if remaining is not None and remaining <= 0.0:
                break
            self._sync.wait(remaining)

        if self._state is _PipeState.EXECUTING and self._resp is _MISSING:
            self._state = _PipeState.DRAINING
            self._drain_generation += 1
            generation = self._drain_generation
            self._drain.start(lambda: self._expire_drain(generation))
            self._sync.notify_all()
            raise SkillPipeTimeoutError(
                timeout if timeout is not None else 0.0, phase="SKILL response"
            )

    def publish(self, event: SkillResp | Exception) -> None:
        with self._sync:
            if self._state is _PipeState.CLOSED:
                return
            if isinstance(event, Exception):
                if self._state not in {_PipeState.CLOSED, _PipeState.BROKEN}:
                    self._cause = event
                    self._state = _PipeState.BROKEN
                self._drain.cancel()
                self._sync.notify_all()
                return
            if self._state is _PipeState.EXECUTING and self._resp is _MISSING:
                self._resp = event
                if event.status == 'restart':
                    self._state = _PipeState.RESTARTING
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
                self._state = (
                    _PipeState.RESTARTING if event.status == 'restart' else _PipeState.READY
                )
                self._sync.notify_all()
                return
            if self._state not in {_PipeState.DESYNCHRONIZED, _PipeState.BROKEN}:
                self._desync(
                    SkillPipeDesynchronizedError(
                        "unexpected or additional response arrived while no frame was expected"
                    )
                )

    def _expire_drain(self, generation: int) -> None:
        with self._sync:
            if self._state is not _PipeState.DRAINING or generation != self._drain_generation:
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
        "_writer_start_lock",
        "_writer_thread",
    )

    _decoder: Response
    _lock: threading.Lock
    _machine: _StateMachine
    _reader: TextIO | BufferedIOBase
    _thread: threading.Thread
    _writer_start_lock: threading.Lock
    _writer_thread: threading.Thread | None
    _writer: TextIO

    def __init__(
        self,
        reader: TextIO | BufferedIOBase,
        writer: TextIO,
        *,
        reader_encoding: str = "utf-8",
        drain_timeout: float | None = 30.0,
        max_payload_chars: int = Response.DEFAULT_MAX_PAYLOAD_CHARS,
        ignore_preamble: bool = False,
        max_preamble_chars: int = Response.DEFAULT_MAX_PREAMBLE_CHARS,
    ) -> None:
        self._reader = reader
        self._writer = writer
        self._decoder = Response(
            reader,
            encoding=reader_encoding,
            max_payload_chars=max_payload_chars,
            ignore_preamble=ignore_preamble,
            max_preamble_chars=max_preamble_chars,
        )
        self._lock = threading.Lock()
        self._machine = _StateMachine(drain_timeout)
        self._writer_start_lock = threading.Lock()
        self._writer_thread = None

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
        return self._machine.wait_until_ready(timeout)

    def close(self) -> None:
        self._start_writer()
        self._machine.close()

    def wait_closed(self, timeout: float | None = None) -> bool:
        deadline = None if timeout is None else time.monotonic() + timeout
        self._thread.join(timeout)
        if self._thread.is_alive():
            return False
        with self._writer_start_lock:
            writer = self._writer_thread
        if writer is None:
            return True
        remaining = None if deadline is None else _remaining(deadline)
        writer.join(remaining)
        return not writer.is_alive()

    def wait_peer_closed(self, timeout: float | None = None) -> bool:
        """Wait for the reader thread and report whether the peer ended the pipe.

        Returns:
            Whether the reader thread exited without a prior local close.
        """
        self._thread.join(timeout)
        if self._thread.is_alive():
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
            SkillPipeInvalidCommandError: If the command is empty or multiline.
            SkillPipeClosedError: If the pipe is closed.
            SkillPipeBrokenError: If the pipe broke while executing.
            SkillPipeTimeoutError: If the command did not finish in time.
        """
        if timeout is not None and (timeout < 0.0 or not math.isfinite(timeout)):
            raise ValueError("timeout must be None or a non-negative finite number")

        cmd = _command_line(cmd)

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
            self._start_writer()
            self._machine.queue_command(cmd)

            return self._machine.wait_response(timeout=timeout, deadline=deadline)
        finally:
            self._lock.release()

    def _start_writer(self) -> None:
        with self._writer_start_lock:
            if self._writer_thread is not None:
                return
            self._writer_thread = threading.Thread(
                target=self._writer_loop,
                name="allegrobridge-pipe-writer",
                daemon=True,
            )
            self._writer_thread.start()

    def _writer_loop(self) -> None:
        try:
            while True:
                command = self._machine.take_command()
                if command is None:
                    return
                failure: Exception | None = None
                try:
                    self._writer.write(command)
                    self._writer.flush()
                except Exception as exc:  # ruff: ignore[blind-except] - poison writer
                    failure = exc
                self._machine.write_completed(failure)
        finally:
            with suppress(OSError):
                self._writer.close()

    def _start(self) -> None:
        def loop() -> None:
            try:
                while True:
                    resp = self._decoder.recv()
                    self._machine.publish(resp)
                    if resp.status == 'restart':
                        # Let the writer owner finish an in-flight flush before closing.
                        self._machine.stop_writer()
                        return
            except Exception as exc:  # ruff: ignore[blind-except] - publish reader failure
                self._machine.publish(exc)
            finally:
                with suppress(OSError):
                    self._reader.close()

        self._thread = threading.Thread(
            target=loop,
            name="allegrobridge-pipe-reader",
            daemon=True,
        )
        self._thread.start()
