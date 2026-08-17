from __future__ import annotations

from typing import TYPE_CHECKING, Final, NewType

from skillbridge.exception import FrameTooLargeError, InvalidResponseError

if TYPE_CHECKING:
    from typing import TextIO

__all__ = [
    "Response",
    "SkillResp",
]

SkillResp = NewType("SkillResp", tuple[bool, str])


class Response:
    __slots__ = (
        "_ignore_preamble",
        "_max_payload_chars",
        "_max_preamble_chars",
        "_reader",
    )

    STX_: Final[str] = "\x02"
    NAK_: Final[str] = "\x15"
    RS_: Final[str] = "\x1e"
    DEFAULT_MAX_PAYLOAD_CHARS_: Final[int] = 16 * 1024 * 1024
    DEFAULT_MAX_PREAMBLE_CHARS_: Final[int] = 4096

    _reader: TextIO
    _max_payload_chars: int
    _ignore_preamble: bool
    _max_preamble_chars: int

    def __init__(
        self,
        reader: TextIO,
        *,
        max_payload_chars: int = DEFAULT_MAX_PAYLOAD_CHARS_,
        ignore_preamble: bool = False,
        max_preamble_chars: int = DEFAULT_MAX_PREAMBLE_CHARS_,
    ) -> None:
        self._reader = reader
        self._max_payload_chars = max_payload_chars
        self._ignore_preamble = ignore_preamble
        self._max_preamble_chars = max_preamble_chars

    @property
    def reader(self) -> TextIO:
        return self._reader

    @property
    def max_payload_chars(self) -> int:
        return self._max_payload_chars

    @property
    def max_preamble_chars(self) -> int:
        return self._max_preamble_chars

    @staticmethod
    def _read_char(reader: TextIO, context: str) -> str:
        char = reader.read(1)
        if not char:
            raise EOFError(f"SKILL IPC pipe closed {context}")
        return char

    def recv(self) -> SkillResp:
        # Scan for the start marker (STX for success, NAK for failure).
        # When ignore_preamble is True, gracefully skip noise characters
        # (e.g. Cadence logs/warnings) before the frame, bounded by
        # max_preamble_chars to prevent unbounded buffering.
        preamble_count = 0
        while True:
            marker = self._read_char(self._reader, "before response frame")
            if marker in {self.STX_, self.NAK_}:
                break

            if not self._ignore_preamble:
                raise InvalidResponseError(
                    marker,
                    reason="unexpected character before response frame",
                )

            preamble_count += 1
            if preamble_count > self._max_preamble_chars:
                raise FrameTooLargeError(preamble_count, self._max_preamble_chars)

        payload: list[str] = []
        while True:
            char = self._read_char(self._reader, "inside response frame")
            if char == self.RS_:
                return SkillResp((marker == self.STX_, "".join(payload)))

            payload.append(char)
            if len(payload) > self._max_payload_chars:
                raise FrameTooLargeError(len(payload), self._max_payload_chars)
