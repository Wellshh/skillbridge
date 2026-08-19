"""Cross-platform SKILL bridge primitives."""

from .client import SkillBridgeClient
from .pipe import (
    SkillPipe,
    SkillPipeBrokenError,
    SkillPipeClosedError,
    SkillPipeDesynchronizedError,
    SkillPipeError,
    SkillPipeState,
    SkillPipeTimeoutError,
)
from .response_protocol import (
    FramedResponseProtocol,
    NAK,
    RS,
    STX,
    SkillResponse,
    SkillResponseProtocolError,
)

__all__ = [
    "FramedResponseProtocol",
    "NAK",
    "RS",
    "STX",
    "SkillBridgeClient",
    "SkillPipe",
    "SkillPipeBrokenError",
    "SkillPipeClosedError",
    "SkillPipeDesynchronizedError",
    "SkillPipeError",
    "SkillPipeState",
    "SkillPipeTimeoutError",
    "SkillResponse",
    "SkillResponseProtocolError",
]
