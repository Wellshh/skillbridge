# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated

from pydantic import Field, TypeAdapter

from allegrobridge.client.api.geometry import Point, _coerce_finite_float, _coerce_point
from allegrobridge.client.base import Collection, SessionRecord, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, read, write

_PROJECT_PROCEDURE = '__abProjectRoutes'
_CREATE_PROCEDURE = '__abCreateRoute'
_POINT_SIZE = 2
_OptionalString = str | None
_Width = Annotated[float, Field(gt=0, allow_inf_nan=False)]


class RouteInfo(SessionRecord):
    net: _OptionalString
    layer: str
    start: Point
    end: Point
    width: _Width


_RouteList = list[RouteInfo]
_ROUTES = TypeAdapter(_RouteList)


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

    @write(_CREATE_PROCEDURE, _ROUTES)
    def create(
        self,
        net: str,
        points: Sequence[Point | tuple[float, float]],
        layer: str,
        width: float,
    ) -> RpcArgs:
        if len(points) < _POINT_SIZE:
            raise ValueError('a route requires at least two points')
        if any(len(point) != _POINT_SIZE for point in points):
            raise ValueError('route points must contain exactly two coordinates')
        width = _coerce_finite_float(width)
        if width <= 0:
            raise ValueError('route width must be positive')
        return net, [_coerce_point(point) for point in points], layer, width
