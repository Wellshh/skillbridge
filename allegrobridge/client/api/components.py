# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.api.geometry import _coerce_finite_float, _OptionalLocated
from allegrobridge.client.base import KeyedCollection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read, write
from skillbridge.client.hints import Skill

_PROCEDURE = '__abProjectComponents'
_MOVE_PROCEDURE = '__abMoveComponent'
_MOVE_BY_PROCEDURE = '__abMoveComponentsBy'


class ComponentInfo(_OptionalLocated):
    refdes: str
    device_type: str
    package: str
    component_class: str
    placement: Literal['placed', 'unplaced']


_ComponentList = list[ComponentInfo]
_COMPONENTS = TypeAdapter(_ComponentList)
_COMPONENT = TypeAdapter(ComponentInfo)


@_core_api
class ComponentsApi(KeyedCollection[str, ComponentInfo]):
    _key_type = str

    @read(_PROCEDURE, _COMPONENTS)
    def _project(self, refdes: str | None, include_unplaced: bool) -> RpcArgs:
        return refdes, include_unplaced

    def __call__(self, *, include_unplaced: bool = True) -> list[ComponentInfo]:
        return self._project(None, include_unplaced)

    def _snapshot(self) -> list[ComponentInfo]:
        include_unplaced = True
        return self._project(None, include_unplaced)

    def _query_key(self, key: str) -> list[ComponentInfo]:
        include_unplaced = True
        return self._project(key, include_unplaced)

    @write(_MOVE_PROCEDURE, _COMPONENT)
    def move(
        self,
        refdes: str,
        *,
        x: float,
        y: float,
        rotation: float | None = None,
    ) -> RpcArgs:
        return (
            refdes,
            _coerce_finite_float(x),
            _coerce_finite_float(y),
            None if rotation is None else _coerce_finite_float(rotation),
        )

    @write(_MOVE_BY_PROCEDURE, _COMPONENTS)
    def move_by(
        self,
        components: Sequence[ComponentInfo],
        *,
        dx: float,
        dy: float,
    ) -> RpcArgs:
        refdeses: list[Skill] = []
        seen: set[str] = set()
        for component in components:
            component._check_id(self._session)  # ruff: ignore[private-member-access]
            if component.refdes in seen:
                raise ValueError(f'duplicate component refdes: {component.refdes!r}')
            seen.add(component.refdes)
            refdeses.append(component.refdes)
        return (
            refdeses,
            _coerce_finite_float(dx),
            _coerce_finite_float(dy),
        )
