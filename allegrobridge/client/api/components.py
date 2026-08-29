# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.base import KeyedCollection, SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read, write

_PROCEDURE = '__abProjectComponents'
_MOVE_PROCEDURE = '__abMoveComponent'
_OptionalFloat = float | None


class ComponentInfo(SessionRecord):
    refdes: str
    device_type: str
    package: str
    component_class: str
    placement: Literal['placed', 'unplaced']
    x: _OptionalFloat
    y: _OptionalFloat
    rotation: _OptionalFloat


_ComponentList = list[ComponentInfo]
_COMPONENTS = TypeAdapter(_ComponentList)
_COMPONENT = TypeAdapter(ComponentInfo)


@_core_api
class ComponentsApi(KeyedCollection[str, ComponentInfo]):
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
        return refdes, x, y, rotation
