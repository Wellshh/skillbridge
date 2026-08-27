# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass
from weakref import ReferenceType

from pydantic import BaseModel, ConfigDict, PrivateAttr


class BaseRecord(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid', frozen=True)


@dataclass(frozen=True, slots=True)
class _ID:
    """An implicit id binded to each record fetched from allegro database,
    associated with session and object query turns."""

    token: ReferenceType[object]
    generation: int


class SessionRecord(BaseRecord):
    _id: _ID | None = PrivateAttr(default=None)

    def model_post_init(self, context: object, /) -> None:
        if isinstance(context, _ID):
            object.__setattr__(self, '_id', context)  # ruff: ignore[unnecessary-dunder-call]
