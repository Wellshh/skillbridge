# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Sequence

from pydantic import TypeAdapter

from allegrobridge._kernel.client.hints import Skill
from allegrobridge.client.api.geometry import finite
from allegrobridge.client.api.record import Component
from allegrobridge.client.base import KeyedCollection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read, write

_PROCEDURE = '__abProjectComponents'
_MOVE_PROCEDURE = '__abMoveComponent'
_MOVE_BY_PROCEDURE = '__abMoveComponentsBy'

_ComponentList = list[Component]
_COMPONENTS = TypeAdapter(_ComponentList)
_COMPONENT = TypeAdapter(Component)


def _to_refdes(target: str | Component) -> str:
    if isinstance(target, Component):
        return target.refdes
    if isinstance(target, str) and target:
        return target
    raise TypeError(f'expected component refdes or Component, got {type(target).__name__}')


@_core_api
class ComponentsApi(KeyedCollection[str, Component]):
    _key_type = str

    @read(_PROCEDURE, _COMPONENTS)
    def _project(self, refdes: str | None, include_unplaced: bool) -> RpcArgs:
        return refdes, include_unplaced

    def __call__(self, *, include_unplaced: bool = True) -> list[Component]:
        return self._project(None, include_unplaced)

    def _snapshot(self) -> list[Component]:
        include_unplaced = True
        return self._project(None, include_unplaced)

    def _query_key(self, key: str) -> list[Component]:
        include_unplaced = True
        return self._project(key, include_unplaced)

    @write(_MOVE_PROCEDURE, _COMPONENT)
    def move(
        self,
        component: str | Component,
        *,
        x: float,
        y: float,
        rotation: float | None = None,
    ) -> RpcArgs:
        return (
            _to_refdes(component),
            finite(x),
            finite(y),
            None if rotation is None else finite(rotation),
        )

    @write(_MOVE_BY_PROCEDURE, _COMPONENTS)
    def move_by(
        self,
        components: Sequence[str | Component],
        *,
        dx: float,
        dy: float,
    ) -> RpcArgs:
        refdeses: list[Skill] = []
        seen: set[str] = set()
        for component in components:
            refdes = _to_refdes(component)
            if refdes in seen:
                raise ValueError(f'duplicate component refdes: {refdes!r}')
            seen.add(refdes)
            refdeses.append(refdes)
        return (
            refdeses,
            finite(dx),
            finite(dy),
        )
