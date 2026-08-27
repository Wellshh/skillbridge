# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.api.routes import Point
from allegrobridge.client.base import BaseRecord, SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, read

_PROJECT_PROCEDURE = '__abProjectShapes'
_OptionalString = str | None


class BBox(BaseRecord):
    lower_left: Point
    upper_right: Point


class ShapeInfo(SessionRecord):
    net: _OptionalString
    layer: str
    dynamic: Literal['dynamic', 'static']
    bbox: BBox


_ShapeList = list[ShapeInfo]
_SHAPES = TypeAdapter(_ShapeList)


class ShapesApi(SessionApi):
    @read(_PROJECT_PROCEDURE, _SHAPES)
    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        dynamic: bool | None = None,
    ) -> RpcArgs:
        state = None if dynamic is None else 'dynamic' if dynamic else 'static'
        return net, layer, state
