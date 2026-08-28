# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Sequence

from pydantic import PositiveFloat, TypeAdapter

from allegrobridge.client.base import BaseRecord, SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, read, write

_PROJECT_PROCEDURE = '__abProjectRoutes'
_CREATE_PROCEDURE = '__abCreateRoute'
_POINT_SIZE = 2
_OptionalString = str | None


class Point(BaseRecord):
    x: float
    y: float


class RouteInfo(SessionRecord):
    net: _OptionalString
    layer: str
    start: Point
    end: Point
    width: PositiveFloat


_RouteList = list[RouteInfo]
_ROUTES = TypeAdapter(_RouteList)


class RoutesApi(SessionApi):
    @read(_PROJECT_PROCEDURE, _ROUTES)
    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
    ) -> RpcArgs:
        return net, layer

    @write(_CREATE_PROCEDURE, _ROUTES)
    def create(
        self,
        net: str,
        points: Sequence[tuple[float, float]],
        layer: str,
        width: float,
    ) -> RpcArgs:
        if len(points) < _POINT_SIZE:
            raise ValueError('a route requires at least two points')
        if any(len(point) != _POINT_SIZE for point in points):
            raise ValueError('route points must contain exactly two coordinates')
        if width <= 0:
            raise ValueError('route width must be positive')
        return net, list(points), layer, width
