"""Response framing between the Python daemon and the SKILL parent process."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO

STX = "\x02"  # successful response starts here
NAK = "\x15"  # failed response starts here
RS = "\x1e"  # response terminator


class SkillResponseProtocolError(RuntimeError):
    """The SKILL-side response stream violated its framing contract."""


@dataclass(frozen=True, slots=True)
class SkillResponse:
    """One decoded response from SKILL."""

    ok: bool
    payload: str


@dataclass(frozen=True, slots=True)
class FramedResponseProtocol:
    """Decode ``STX|NAK + payload + RS`` frames.

    The payload may contain newlines. Timeout recovery is safe because the
    reader can discard exactly one complete late frame before accepting another
    request.

    ``ignore_preamble`` mirrors the pragmatic behavior used by several Cadence
    bridges: characters before STX/NAK are ignored. Strict mode is preferable
    when the pipe is known to contain only protocol traffic.
    """

    max_payload_chars: int = 16 * 1024 * 1024
    ignore_preamble: bool = False
    max_preamble_chars: int = 4096

    def __post_init__(self) -> None:
        if self.max_payload_chars <= 0:
            raise ValueError("max_payload_chars must be positive")
        if self.max_preamble_chars < 0:
            raise ValueError("max_preamble_chars must be non-negative")

    @staticmethod
    def _read_char(reader: TextIO, *, context: str) -> str:
        char = reader.read(1)
        if char == "":
            raise EOFError(f"SKILL IPC pipe closed {context}")
        return char

    def read_response(self, reader: TextIO) -> SkillResponse:
        preamble: list[str] = []

        while True:
            char = self._read_char(reader, context="before response frame")
            if char in {STX, NAK}:
                start = char
                break

            if not self.ignore_preamble:
                raise SkillResponseProtocolError(
                    f"unexpected character before response frame: {char!r}"
                )

            preamble.append(char)
            if len(preamble) > self.max_preamble_chars:
                raise SkillResponseProtocolError("response preamble exceeded configured limit")

        payload: list[str] = []
        while True:
            char = self._read_char(reader, context="inside response frame")
            if char == RS:
                return SkillResponse(ok=start == STX, payload="".join(payload))

            payload.append(char)
            if len(payload) > self.max_payload_chars:
                raise SkillResponseProtocolError("SKILL response payload exceeded configured limit")
