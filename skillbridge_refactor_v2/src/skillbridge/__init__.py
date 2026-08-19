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
    NAK,
    RS,
    STX,
    FramedResponseProtocol,
    SkillResponse,
    SkillResponseProtocolError,
)

__all__ = [
    "NAK",
    "RS",
    "STX",
    "FramedResponseProtocol",
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
