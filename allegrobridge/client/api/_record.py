from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _Record(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid', frozen=True)
