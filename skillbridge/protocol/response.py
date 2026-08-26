# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING, Final, Literal, NamedTuple

from skillbridge.exception import FrameTooLargeError, InvalidResponseError

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

    _reader: TextIO
    _max_payload_chars: int
    _ignore_preamble: bool
    _max_preamble_chars: int

    def __init__(
        self,
        reader: TextIO,
        *,
        max_payload_chars: int = DEFAULT_MAX_PAYLOAD_CHARS,
        ignore_preamble: bool = False,
        max_preamble_chars: int = DEFAULT_MAX_PREAMBLE_CHARS,
    ) -> None:
        self._reader = reader
        self._max_payload_chars = max_payload_chars
        self._ignore_preamble = ignore_preamble
        self._max_preamble_chars = max_preamble_chars

    @staticmethod
    def _read_char(reader: TextIO, context: str) -> str:
        char = reader.read(1)
        if not char:
            raise EOFError(f"SKILL IPC pipe closed {context}")
        return char

    def recv(self) -> SkillResp:
        # When ignore_preamble is True, gracefully skip noise characters
        # (e.g. Cadence logs/warnings) before the frame, bounded by
        # max_preamble_chars to prevent unbounded buffering.
        preamble_count = 0
        while True:
            marker = self._read_char(self._reader, "before response frame")
            if marker in {self.STX, self.NAK, self.RST}:
                break

            if not self._ignore_preamble:
                raise InvalidResponseError(
                    marker,
                    reason="unexpected character before response frame",
                )

            preamble_count += 1
            if preamble_count > self._max_preamble_chars:
                raise FrameTooLargeError(preamble_count, self._max_preamble_chars)

        status: RespStatus
        if marker == self.STX:
            status = "success"
        elif marker == self.NAK:
            status = "failure"
        else:
            status = "restart"

        payload: list[str] = []
        while True:
            char = self._read_char(self._reader, "inside response frame")
            if char == self.RS:
                return SkillResp(status, "".join(payload))

            payload.append(char)
            if len(payload) > self._max_payload_chars:
                raise FrameTooLargeError(len(payload), self._max_payload_chars)
