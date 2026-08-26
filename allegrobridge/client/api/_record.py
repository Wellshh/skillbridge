# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _Record(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid', frozen=True)
