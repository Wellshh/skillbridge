# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from math import isclose
from typing import Annotated, cast

from pydantic import Field, FiniteFloat, TypeAdapter

from allegrobridge._kernel.client.hints import SkillCode
from allegrobridge.client.api.geometry import (
    ArcTo,
    LineTo,
    PathStep,
    Point,
    finite,
)
from allegrobridge.client.base import Collection, SessionRecord, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, direct, read, write

# NOTE: DELETE this dangling projection
_PROJECT_PROCEDURE = '__abProjectRoutes'
_CREATE_PATH_PROCEDURE = '__abCreatePath'
_CONNECT_PROCEDURE = '__abConnectRoutes'
_POINT_SIZE = 2
_POINT_TOLERANCE = 1e-6
_ASCII_CONTROL_LIMIT = 32
_ASCII_DELETE = 127
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

    # optional Arc attributes
    radius: FiniteFloat | None
    is_clockwise: bool | None
    center: Point | None


_RouteList = list[RouteInfo]
_ROUTES = TypeAdapter(_RouteList)


def _route_key(route: RouteInfo) -> tuple[object, ...]:
    return (
        route.net,
        route.layer,
        route.obj_type,
        route.start,
        route.end,
        route.width,
        route.length,
        route.radius,
        route.is_clockwise,
        route.center,
    )


def _added_routes(before: list[RouteInfo], after: list[RouteInfo]) -> list[RouteInfo]:
    remaining = Counter(_route_key(route) for route in before)
    added: list[RouteInfo] = []
    for route in after:
        key = _route_key(route)
        if remaining[key]:
            remaining[key] -= 1
        else:
            added.append(route)
    return added


def _same_point(first: Point, second: Point) -> bool:
    return isclose(first.x, second.x, abs_tol=_POINT_TOLERANCE) and isclose(
        first.y,
        second.y,
        abs_tol=_POINT_TOLERANCE,
    )


def _is_single_change_chain(routes: list[RouteInfo], start: Point, end: Point) -> bool:
    reached = [start]
    pending = routes.copy()
    while pending:
        for index, route in enumerate(pending):
            if any(
                _same_point(route.start, point) or _same_point(route.end, point)
                for point in reached
            ):
                reached.extend((route.start, route.end))
                pending.pop(index)
                break
        else:
            return False
    return any(_same_point(point, end) for point in reached)


def _validated_name(value: str, field: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or any(
            char.isspace()
            or char in ';\'"'
            or ord(char) < _ASCII_CONTROL_LIMIT
            or ord(char) == _ASCII_DELETE
            for char in value
        )
    ):
        raise ValueError(f'{field} must be a non-empty name without command syntax')
    return value


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

    @direct(_CONNECT_PROCEDURE, _ROUTES)
    def _connect(
        self,
        net: str,
        start: Point,
        end: Point,
        layer: str,
        width: float,
    ) -> RpcArgs:
        return net, start, end, layer, width

    def connect(
        self,
        net: str,
        start: Point | tuple[float, float],
        end: Point | tuple[float, float],
        layer: str,
        width: float,
    ) -> list[RouteInfo]:
        if self._session._allegro.mode != 'cli':  # ruff: ignore[private-member-access]
            raise RuntimeError("routes.connect() requires Allegro.open(mode='cli')")
        net = _validated_name(net, 'net')
        layer = _validated_name(layer, 'layer')
        start = Point.of(start)
        end = Point.of(end)
        width = finite(width)
        if width <= 0:
            raise ValueError('route width must be positive')

        with self._session._connect_lock:  # ruff: ignore[private-member-access]
            try:
                before = self._connect(net, start, end, layer, width)
            finally:
                self._session.refresh()
            self._session.workspace.transaction(SkillCode('t'))
            after = self._project(net=net, layer=None)
            added = _added_routes(before, after)
            if not added:
                raise RuntimeError('ROUTE_CONNECT_NO_CHANGE')
            if not _is_single_change_chain(added, start, end):
                raise RuntimeError('ROUTE_CONNECT_AMBIGUOUS')
            return added

    @write(_CREATE_PATH_PROCEDURE, _ROUTES)
    def create(
        self,
        net: str,
        path: Sequence[Point | tuple[float, float] | LineTo | ArcTo],
        layer: str,
        width: float,
    ) -> RpcArgs:
        if len(path) < _POINT_SIZE:
            raise ValueError('a route requires at least two points')
        width = finite(width)
        if width <= 0:
            raise ValueError('route width must be positive')
        return (
            net,
            Point.of(cast('Point | tuple[float, float]', path[0])),
            [PathStep.of(item) for item in path[1:]],
            layer,
            width,
        )
