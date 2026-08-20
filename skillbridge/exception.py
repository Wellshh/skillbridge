from __future__ import annotations

from typing import ClassVar

__all__ = [
    'FrameTooLargeError',
    'InvalidFrameError',
    'InvalidResponseError',
    'PeerClosedError',
    'ProtocolError',
    'SkillBridgeError',
    'SkillPipeBrokenError',
    'SkillPipeClosedError',
    'SkillPipeDesynchronizedError',
    'SkillPipeError',
    'SkillPipeTimeoutError',
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


class SkillPipeError(SkillBridgeError, RuntimeError):
    """Base class for SKILL channel failures."""

    code = 'pipe_error'
    wire_payload: ClassVar[str] = '<pipe-error>'


class SkillPipeTimeoutError(SkillPipeError, TimeoutError):
    """A request exceeded its total deadline."""

    code = 'pipe_timeout'
    wire_payload = '<timeout>'

    def __init__(self, timeout: float, *, phase: str) -> None:
        self.timeout = timeout
        self.phase = phase
        super().__init__(
            f'SKILL request timed out after {timeout:g} seconds while waiting for {phase}.',
            hint='Increase the timeout value or investigate slow SKILL execution.',
        )


class SkillPipeDesynchronizedError(SkillPipeError):
    """The request/response association can no longer be trusted."""

    code = 'pipe_desynchronized'
    wire_payload = '<desynchronized>'

    def __init__(
        self,
        message: str = (
            'SKILL pipe is desynchronized; restart the bridge before sending another request.'
        ),
    ) -> None:
        super().__init__(
            message,
            hint='Restart the server or subprocess to resynchronize IPC communication.',
        )


class SkillPipeClosedError(SkillPipeError):
    """The channel was closed intentionally."""

    code = 'pipe_closed'
    wire_payload = '<closed>'

    def __init__(self, message: str = 'SKILL pipe is closed.') -> None:
        super().__init__(message)


class SkillPipeBrokenError(SkillPipeError):
    """The underlying reader, writer, or framing parser failed."""

    code = 'pipe_broken'

    def __init__(self, message: str = 'SKILL IPC pipe is broken.') -> None:
        super().__init__(
            message,
            hint='Check that the Cadence process is still running and responsive.',
        )
