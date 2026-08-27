# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from weakref import ReferenceType

from pydantic import BaseModel, ConfigDict, PrivateAttr

from allegrobridge.exceptions import RecordIDError

if TYPE_CHECKING:
    from allegrobridge.client.session.session import Session


class BaseRecord(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid', frozen=True)


@dataclass(frozen=True, slots=True)
class _ID:
    """An implicit id binded to each record fetched from allegro database,
    associated with session and object query turns."""

    token: ReferenceType[Session]
    generation: int

    def check(self, session: Session, name: str) -> None:
        owner = self.token()
        if owner is None:
            raise RecordIDError(f'{name} Session is no longer available')
        if owner is not session:
            raise RecordIDError(f'{name} belongs to another Session')
        if self.generation != session.generation:
            raise RecordIDError(f'{name} is stale for this Session')


class SessionRecord(BaseRecord):
    _id: _ID | None = PrivateAttr(default=None)

    def model_post_init(self, context: object, /) -> None:
        if isinstance(context, _ID):
            # avoid pyright type lint error
            object.__setattr__(self, '_id', context)  # ruff: ignore[unnecessary-dunder-call]

    def _check_id(self, session: Session) -> None:
        name = type(self).__name__
        if self._id is None:
            raise RecordIDError(f'{name} is not bound to a Session')
        self._id.check(session, name)
