# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import codecs
from io import BufferedIOBase, StringIO
from typing import TYPE_CHECKING, Final, Literal, NamedTuple, cast

from allegrobridge._kernel.exception import FrameTooLargeError, InvalidResponseError

if TYPE_CHECKING:
    from typing import TextIO

__all__ = [
    "RespStatus",
    "Response",
    "SkillResp",
]

RespStatus = Literal['success', 'failure', 'restart']


class SkillResp(NamedTuple):
    status: RespStatus
    payload: str


class Response:
    __slots__ = (
        "_buffer",
        "_decoder",
        "_eof",
        "_ignore_preamble",
        "_max_payload_chars",
        "_max_preamble_chars",
        "_reader",
    )
    # frame protocol
    STX: Final[str] = "\x02"  # success: start of payload
    NAK: Final[str] = "\x15"  # failed: start of payload
    RST: Final[str] = "\x12"  # restart: start of payload
    RS: Final[str] = "\x1e"  # end of payload

    DEFAULT_MAX_PAYLOAD_CHARS: Final[int] = 16 * 1024 * 1024
    DEFAULT_MAX_PREAMBLE_CHARS: Final[int] = 4096
    _READ_SIZE: Final[int] = 64 * 1024  # buffer size: 64Kib

    _reader: TextIO | BufferedIOBase
    _buffer: str
    _decoder: codecs.IncrementalDecoder | None
    _eof: bool
    _max_payload_chars: int
    _ignore_preamble: bool
    _max_preamble_chars: int

    def __init__(
        self,
        reader: TextIO | BufferedIOBase,
        *,
        encoding: str = "utf-8",
        max_payload_chars: int = DEFAULT_MAX_PAYLOAD_CHARS,
        ignore_preamble: bool = False,
        max_preamble_chars: int = DEFAULT_MAX_PREAMBLE_CHARS,
    ) -> None:
        self._reader = reader
        self._buffer = ""
        self._decoder = (
            codecs.getincrementaldecoder(encoding)() if isinstance(reader, BufferedIOBase) else None
        )
        self._eof = False
        self._max_payload_chars = max_payload_chars
        self._ignore_preamble = ignore_preamble
        self._max_preamble_chars = max_preamble_chars

    def _fill(self, context: str) -> None:
        while not self._buffer:
            if self._eof:
                raise EOFError(f"SKILL IPC pipe closed {context}")

            if self._decoder is None:
                size = self._READ_SIZE if isinstance(self._reader, StringIO) else 1
                self._buffer = cast("TextIO", self._reader).read(size)
                self._eof = not self._buffer
                continue

            raw = cast("BufferedIOBase", self._reader).read1(self._READ_SIZE)
            self._eof = not raw
            self._buffer = self._decoder.decode(raw, final=self._eof)

    def recv(self) -> SkillResp:  # ruff: ignore[complex-structure] - framed stream parser
        # When ignore_preamble is True, gracefully skip noise characters
        # (e.g. Cadence logs/warnings) before the frame, bounded by
        # max_preamble_chars to prevent unbounded buffering.
        preamble_count = 0
        while True:
            self._fill("before response frame")
            marker_index = min(
                (
                    index
                    for marker in (self.STX, self.NAK, self.RST)
                    if (index := self._buffer.find(marker)) >= 0
                ),
                default=-1,
            )
            if marker_index >= 0:
                if marker_index and not self._ignore_preamble:
                    raise InvalidResponseError(
                        self._buffer[0],
                        reason="unexpected character before response frame",
                    )
                preamble_count += marker_index
                if preamble_count > self._max_preamble_chars:
                    raise FrameTooLargeError(self._max_preamble_chars + 1, self._max_preamble_chars)
                marker = self._buffer[marker_index]
                self._buffer = self._buffer[marker_index + 1 :]
                break

            if not self._ignore_preamble:
                raise InvalidResponseError(
                    self._buffer[0],
                    reason="unexpected character before response frame",
                )

            preamble_count += len(self._buffer)
            if preamble_count > self._max_preamble_chars:
                raise FrameTooLargeError(self._max_preamble_chars + 1, self._max_preamble_chars)
            self._buffer = ""

        status: RespStatus
        if marker == self.STX:
            status = "success"
        elif marker == self.NAK:
            status = "failure"
        else:
            status = "restart"

        payload: list[str] = []
        payload_size = 0
        while True:
            self._fill("inside response frame")
            marker_index = self._buffer.find(self.RS)
            chunk = self._buffer if marker_index < 0 else self._buffer[:marker_index]
            payload.append(chunk)
            payload_size += len(chunk)
            if payload_size > self._max_payload_chars:
                raise FrameTooLargeError(self._max_payload_chars + 1, self._max_payload_chars)

            if marker_index >= 0:
                self._buffer = self._buffer[marker_index + 1 :]
                return SkillResp(status, "".join(payload))

            self._buffer = ""
