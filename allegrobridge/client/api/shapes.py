# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import Shape
from allegrobridge.client.base import Collection, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, read

_PROJECT_PROCEDURE = '__abProjectShapes'

_ShapeList = list[Shape]
_SHAPES = TypeAdapter(_ShapeList)


class ShapesApi(Collection[Shape]):
    module = SkillModule('allegrobridge.server', 'extensions/shapes.il')

    @read(_PROJECT_PROCEDURE, _SHAPES)
    def _project(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        dynamic: bool | None = None,
    ) -> RpcArgs:
        state = None if dynamic is None else 'dynamic' if dynamic else 'static'
        return net, layer, state

    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        dynamic: bool | None = None,
    ) -> list[Shape]:
        return self._project(net=net, layer=layer, dynamic=dynamic)

    def _snapshot(self) -> list[Shape]:
        return self._project(net=None, layer=None, dynamic=None)
