# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.api.geometry import BBox
from allegrobridge.client.base import Collection, SessionRecord, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, read

_PROJECT_PROCEDURE = '__abProjectShapes'
_OptionalString = str | None


class ShapeInfo(SessionRecord):
    net: _OptionalString
    layer: str
    dynamic: Literal['dynamic', 'static']
    bbox: BBox


_ShapeList = list[ShapeInfo]
_SHAPES = TypeAdapter(_ShapeList)


class ShapesApi(Collection[ShapeInfo]):
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
    ) -> list[ShapeInfo]:
        return self._project(net=net, layer=layer, dynamic=dynamic)

    def _snapshot(self) -> list[ShapeInfo]:
        return self._project(net=None, layer=None, dynamic=None)
