from __future__ import annotations

from typing import List, Optional, Sequence

from pydantic import PositiveFloat, PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, read, write
from skillbridge import SkillList, SkillTuple

_PROJECT_PROCEDURE = '__abProjectRoutes'
_CREATE_PROCEDURE = '__abCreateRoute'
_POINT_SIZE = 2
_OptionalString = Optional[str]


class Point(_Record):
    x: float
    y: float


class RouteInfo(_Record):
    net: _OptionalString
    layer: str
    start: Point
    end: Point
    width: PositiveFloat
    session_generation: PositiveInt


_RouteList = List[RouteInfo]
_ROUTES = TypeAdapter(_RouteList)


class RoutesApi(SessionApi):
    @read(_PROJECT_PROCEDURE, _ROUTES, none_as_empty=True)
    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
    ) -> RpcArgs:
        return net, layer

    @write(_CREATE_PROCEDURE, _ROUTES, none_as_empty=True)
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
        return net, SkillList(SkillTuple(point) for point in points), layer, width
