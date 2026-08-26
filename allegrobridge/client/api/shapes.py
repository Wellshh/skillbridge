# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, read
from allegrobridge.client.api.routes import Point

_PROJECT_PROCEDURE = '__abProjectShapes'
_OptionalString = Optional[str]


class BBox(_Record):
    lower_left: Point
    upper_right: Point


class ShapeInfo(_Record):
    net: _OptionalString
    layer: str
    dynamic: Literal['dynamic', 'static']
    bbox: BBox
    session_generation: PositiveInt


_ShapeList = List[ShapeInfo]
_SHAPES = TypeAdapter(_ShapeList)


class ShapesApi(SessionApi):
    @read(_PROJECT_PROCEDURE, _SHAPES, none_as_empty=True)
    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        dynamic: bool | None = None,
    ) -> RpcArgs:
        state = None if dynamic is None else 'dynamic' if dynamic else 'static'
        return net, layer, state
