"""Cross-platform SKILL bridge primitives."""

from .client import SkillBridgeClient
from .pipe import (
    SkillExecutionError,
    SkillPipe,
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeError,
    SkillPipeSnapshot,
    SkillPipeState,
    SkillPipeTimeoutError,
)
from .response_protocol import (
    FramedResponseProtocol,
    LineResponseProtocol,
    NAK,
    RS,
    STX,
    SkillResponse,
    SkillResponseProtocolError,
)

__all__ = [
    "FramedResponseProtocol",
    "LineResponseProtocol",
    "NAK",
    "RS",
    "STX",
    "SkillBridgeClient",
    "SkillExecutionError",
    "SkillPipe",
    "SkillPipeBrokenError",
    "SkillPipeClosedError",
    "SkillPipeDesynchronizedError",
    "SkillPipeError",
    "SkillPipeSnapshot",
    "SkillPipeState",
    "SkillPipeTimeoutError",
    "SkillResponse",
    "SkillResponseProtocolError",
]
