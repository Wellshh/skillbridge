from __future__ import annotations

from typing import ClassVar

__all__ = [
    'FrameTooLargeError',
    'InvalidFrameError',
    'InvalidResponseError',
    'PeerClosedError',
    'ProtocolError',
    'SkillBridgeError',
]


class SkillBridgeError(Exception):
    code: ClassVar[str] = 'skillbridge_error'
    default_hint: ClassVar[str | None] = None

    def __init__(self, message: str, *, hint: str | None = None) -> None:
        self.message = message
        self.hint = self.default_hint if hint is None else hint
        super().__init__(message)

    def __str__(self) -> str:
        if self.hint is None:
            return self.message
        return f'{self.message}\nHint: {self.hint}'


class ProtocolError(SkillBridgeError):
    pass


class FrameTooLargeError(ProtocolError, ValueError):
    code = 'frame_too_large'

    def __init__(self, size: int, max_size: int) -> None:
        self.size = size
        self.max_size = max_size
        super().__init__(
            f'Data exceeds max transmission length: payload size {size} > limit {max_size} bytes.',
            hint='Reduce the payload or increase the configured max transmission limit.',
        )


class PeerClosedError(ProtocolError, ConnectionError):
    code = 'peer_closed'

    def __init__(self, expected: int, received: int) -> None:
        self.expected = expected
        self.received = received
        super().__init__(
            f'Peer closed the connection after {received} of {expected} expected bytes.',
            hint='Reconnect before sending another request.',
        )


class InvalidFrameError(ProtocolError):
    code = 'invalid_frame'

    def __init__(self, header: bytes) -> None:
        self.header = header
        super().__init__(f'Invalid SkillBridge frame header: {header!r}.')


class InvalidResponseError(ProtocolError):
    code = 'invalid_response'

    def __init__(self, response: str, *, reason: str) -> None:
        self.response = response
        self.reason = reason
        preview = response[:200]
        if len(response) > len(preview):
            preview += '...'
        super().__init__(f'Invalid SkillBridge response: {reason}. Response: {preview!r}.')
