from __future__ import annotations
from types import TracebackType

import logging
import threading
from enum import Enum, auto
from typing import TextIO

from skillbridge.protocol.response import Response, SkillResp

logger = logging.getLogger(__name__)


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
        "_condition",
        "_drain_deadline",
        "_drain_timeout",
        "_reader",
        "_request_lock",
        "_response",
        "_response_reader",
        "_state",
        "_writer",
    )

    _cause: Exception | None
    """The exception cause of reader and its downstream."""

    _drain_deadline: float | None
    _drain_timeout: float | None
    _reader: TextIO
    _response: SkillResp | None
    _response_reader: Response
    _state: _PipeState
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
        self._response_reader = Response(
            reader,
            max_payload_chars=max_payload_chars,
            ignore_preamble=ignore_preamble,
            max_preamble_chars=max_preamble_chars,
        )
        self._drain_timeout = drain_timeout
        self._drain_deadline = None

        self._request_lock = threading.Lock()
        self._condition = threading.Condition()

        self._state = _PipeState.READY
        self._response = None
        self._cause = None

    def __enter__(self) -> Pipe:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ...

    def _loop(self) -> None:
