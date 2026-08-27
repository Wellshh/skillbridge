# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, _core_api, read, write

_PROCEDURE = '__abProjectComponents'
_MOVE_PROCEDURE = '__abMoveComponent'
_OptionalFloat = float | None


class ComponentInfo(_Record):
    refdes: str
    device_type: str
    package: str
    component_class: str
    placement: Literal['placed', 'unplaced']
    x: _OptionalFloat
    y: _OptionalFloat
    rotation: _OptionalFloat
    session_generation: PositiveInt


_ComponentList = list[ComponentInfo]
_COMPONENTS = TypeAdapter(_ComponentList)
_COMPONENT = TypeAdapter(ComponentInfo)


@_core_api
class ComponentsApi(SessionApi):
    @read(_PROCEDURE, _COMPONENTS, none_as_empty=True)
    def _project(self, refdes: str | None, include_unplaced: bool) -> RpcArgs:
        return refdes, include_unplaced

    def __call__(self, *, include_unplaced: bool = True) -> list[ComponentInfo]:
        return self._project(None, include_unplaced)

    def __getitem__(self, refdes: str) -> ComponentInfo:
        include_unplaced = True
        components = self._project(refdes, include_unplaced)
        if not components:
            raise KeyError(refdes)
        return components[0]

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
