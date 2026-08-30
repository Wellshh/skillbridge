# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated, cast

from pydantic import Field, FiniteFloat, TypeAdapter

from allegrobridge.client.api.geometry import (
    ArcTo,
    LineTo,
    PathStep,
    Point,
    _coerce_finite_float,
    _coerce_point,
)
from allegrobridge.client.base import Collection, SessionRecord, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, read, write

# NOTE: DELETE this dangling projection
_PROJECT_PROCEDURE = '__abProjectRoutes'
_CREATE_PATH_PROCEDURE = '__abCreatePath'
_POINT_SIZE = 2
_OptionalString = str | None
_Width = Annotated[float, Field(gt=0, allow_inf_nan=False)]


class RouteInfo(SessionRecord):
    net: _OptionalString
    layer: str
    obj_type: str
    start: Point
    end: Point
    width: _Width
    length: FiniteFloat
    radius: FiniteFloat | None
    is_clockwise: bool | None
    center: Point | None


_RouteList = list[RouteInfo]
_ROUTES = TypeAdapter(_RouteList)


def _coerce_step(item: PathStep | Point | tuple[float, float]) -> PathStep:
    if isinstance(item, LineTo):
        return LineTo(_coerce_point(item.end))
    if isinstance(item, ArcTo):
        return ArcTo(_coerce_point(item.end), _coerce_point(item.center), item.clockwise)
    return LineTo(_coerce_point(item))


class RoutesApi(Collection[RouteInfo]):
    module = SkillModule('allegrobridge.server', 'extensions/routes.il')

    @read(_PROJECT_PROCEDURE, _ROUTES)
    def _project(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
    ) -> RpcArgs:
        return net, layer

    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
    ) -> list[RouteInfo]:
        return self._project(net=net, layer=layer)

    def _snapshot(self) -> list[RouteInfo]:
        return self._project(net=None, layer=None)

    @write(_CREATE_PATH_PROCEDURE, _ROUTES)
    def create(
        self,
        net: str,
        path: Sequence[Point | tuple[float, float] | PathStep],
        layer: str,
        width: float,
    ) -> RpcArgs:
        if len(path) < _POINT_SIZE:
            raise ValueError('a route requires at least two points')
        width = _coerce_finite_float(width)
        if width <= 0:
            raise ValueError('route width must be positive')
        return (
            net,
            _coerce_point(cast('Point | tuple[float, float]', path[0])),
            [_coerce_step(item) for item in path[1:]],
            layer,
            width,
        )
