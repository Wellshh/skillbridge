# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar, cast
from weakref import ref

from pydantic import TypeAdapter, ValidationError

from allegrobridge._kernel.client.hints import SkillCode
from allegrobridge.client.base._record import _ID
from allegrobridge.exceptions import AllegroProtocolError

if TYPE_CHECKING:  # pragma: no cover
    from allegrobridge.client.session.session import Session

T = TypeVar('T')

_PENDING = object()


class CmdResult(Generic[T]):
    """A promise-like handle for the result of a Command added to a Batch."""

    def __init__(self) -> None:
        self._value: object = _PENDING
        self._error: BaseException | None = None

    @property
    def value(self) -> T:
        if self._error is not None:
            raise self._error
        if self._value is _PENDING:
            raise RuntimeError('batch result is pending')
        return cast('T', self._value)

    def _resolve(self, value: T) -> None:
        self._value = value

    def _fail(self, error: BaseException) -> None:
        self._error = error


def _validate(
    payload: object,
    adapter: TypeAdapter[T],
    session: Session,
    proc: str,
) -> T:
    context = _ID(ref(session), session.generation)
    try:
        return adapter.validate_python(payload, strict=True, context=context)
    except ValidationError as error:
        if payload is None:
            # In SKILL, empty lists evaluate to nil (decoded as Python None).
            # Unwrap Pydantic core schema definitions to auto-coerce None -> [] for list targets.
            schema = adapter.core_schema
            if schema['type'] == 'definitions':
                schema = schema['schema']
            if schema['type'] == 'list':
                try:
                    return adapter.validate_python([], strict=True, context=context)
                except ValidationError:
                    pass
        raise AllegroProtocolError(f'{proc} returned an invalid payload') from error


@dataclass(frozen=True)
class Cmd(Generic[T]):
    """Deferred transactional write operation."""

    _session: Session
    expr: SkillCode
    proc: str
    _adapter: TypeAdapter[T]
    _id: _ID = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, '_id', _ID(ref(self._session), self._session.generation))

    def _execute(self, *, preview: bool = False) -> T:
        self._check_id(self._session)
        transaction = self._session.raw.transaction
        payload = transaction.preview(self.expr) if preview else transaction(self.expr)
        self._check_id(self._session)
        return self._validate(payload)

    def _check_id(self, session: Session) -> None:
        self._id.check(session, 'Command')

    def _validate(self, payload: object) -> T:
        return _validate(
            payload,
            self._adapter,
            self._session,
            self.proc,
        )
