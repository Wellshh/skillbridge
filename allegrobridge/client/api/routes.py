# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from threading import Lock
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

if TYPE_CHECKING:
    from allegrobridge.client.session.session import Session

from allegrobridge._kernel.client.hints import Skill, SkillCode
from allegrobridge.client.api.geometry import (
    ArcTo,
    LineTo,
    PathStep,
    Point,
    finite,
)
from allegrobridge.client.api.record import Route, RouteConnectResult
from allegrobridge.client.base import Collection, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, direct, read, write

_PROJECT_PROCEDURE = '__abProjectRoutes'
_CREATE_PATH_PROCEDURE = '__abCreatePath'
_CONNECT_PROCEDURE = '__abConnectRoutes'
_POINT_SIZE = 2
_ASCII_CONTROL_LIMIT = 32
_ASCII_DELETE = 127

_RouteList = list[Route]
_ROUTES = TypeAdapter(_RouteList)


def _route_key(route: Route) -> tuple[object, ...]:
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


def _added_routes(before: list[Route], after: list[Route]) -> list[Route]:
    """Multiset difference: rows of ``after`` beyond their multiplicity in ``before``.

    Called with swapped arguments it yields the removed rows, preserving duplicate
    segments in both directions.
    """
    remaining = Counter(_route_key(route) for route in before)
    added: list[Route] = []
    for route in after:
        key = _route_key(route)
        if remaining[key]:
            remaining[key] -= 1
        else:
            added.append(route)
    return added


def _rejects_name_char(char: str, *, allow_space: bool) -> bool:
    return (
        char in ';\'"'
        or ord(char) < _ASCII_CONTROL_LIMIT
        or ord(char) == _ASCII_DELETE
        or (char.isspace() and not (allow_space and char == ' '))
    )


def _validated_net_name(value: str) -> str:
    # The CLI receives the net through SKILL %L quoting, so inner ASCII spaces
    # survive verbatim (probe-verified). Edge whitespace stays rejected: quoted or
    # not, it is indistinguishable from token padding.
    if (
        not isinstance(value, str)
        or not value.strip()
        or value != value.strip()
        or any(_rejects_name_char(char, allow_space=True) for char in value)
    ):
        raise ValueError(
            'net must be a non-empty name without command syntax, '
            'control characters, or edge whitespace'
        )
    return value


def _validated_layer_name(value: str) -> str:
    # The layer token reaches the CLI unquoted (%s); quoted layer names are
    # unprobed, so any whitespace remains rejected.
    if (
        not isinstance(value, str)
        or not value
        or any(_rejects_name_char(char, allow_space=False) for char in value)
    ):
        raise ValueError('layer must be a non-empty name without whitespace or command syntax')
    return value


class RoutesApi(Collection[Route]):
    module = SkillModule('allegrobridge.server', 'extensions/routes.il')
    _connect_lock: Lock

    def __init__(self, session: Session) -> None:
        super().__init__(session)
        object.__setattr__(self, '_connect_lock', Lock())

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
    ) -> list[Route]:
        return self._project(net=net, layer=layer)

    def _snapshot(self) -> list[Route]:
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
    ) -> RouteConnectResult:
        """Execute a structured ``add connect`` command and report the delta on ``net``.

        Immediate CLI-only operation: no preview or batch semantics, and *not*
        idempotent - repeated calls on the same coordinates may re-route existing
        copper or silently change nothing. ``layer`` and ``width`` are hints; the
        authoritative values are whatever the returned :class:`Route` rows carry.

        The result reports projection differences on the target net only (cross-net
        collateral is excluded) and promises nothing about Allegro DBID identity.
        ``added`` and ``removed`` both being empty is a legal outcome; a non-empty
        ``added`` does not prove the two requested coordinates became electrically
        connected.
        """
        if self._session.mode != 'cli':
            raise RuntimeError("routes.connect() requires Allegro.open(mode='cli')")
        net = _validated_net_name(net)
        layer = _validated_layer_name(layer)
        start = Point.of(start)
        end = Point.of(end)
        width = finite(width)
        if width <= 0:
            raise ValueError('route width must be positive')

        with self._connect_lock:
            try:
                before = self._connect(net, start, end, layer, width)
            finally:
                # whether success or not, the dbid in allegro database might be invalidated
                # we manually refresh the session id here, leaving all queried
                # local variables dangling
                self._session.refresh()
            self._session.workspace.transaction(SkillCode('t'))
            after = self._project(net=net, layer=None)
            # removed rows come from the pre-refresh snapshot, so they keep the
            # previous generation id and are stale by construction
            return RouteConnectResult(
                added=_added_routes(before, after),
                removed=_added_routes(after, before),
            )

    @write(_CREATE_PATH_PROCEDURE, _ROUTES)
    def create(
        self,
        net: str,
        path: Sequence[Point | tuple[float, float] | LineTo | ArcTo],
        layer: str,
        width: float,
    ) -> RpcArgs:
        """Create a path and return :class:`Route` projections of the created segments.

        The first element of ``path`` is the start coordinate (``Point`` or plain
        ``(x, y)``); later elements are ``LineTo``/``ArcTo`` steps, or plain
        coordinates treated as ``LineTo``. Adjacent duplicate points are rejected
        before the RPC: a zero-length segment is a caller bug, and Allegro itself
        silently drops it (probe-verified), hiding the mistake.

        Net contract (probe-verified on Allegro 17.2, ``axlDBCreatePath``):

        - a net name that does not exist fails with ``ROUTE_CREATE_FAILED`` and
          the transaction is rolled back;
        - ``net=''`` creates unassigned copper (Allegro's dummy net);
        - even with an existing net, Allegro attaches the net name only to etch
          connected to a pin, via, or shape - isolated new segments come back as
          rows with ``net=None``.
        """
        if len(path) < _POINT_SIZE:
            raise ValueError('a route requires at least two points')
        width = finite(width)
        if width <= 0:
            raise ValueError('route width must be positive')
        first = path[0]
        if isinstance(first, (LineTo, ArcTo)):
            raise ValueError(
                'the first path element must be a plain coordinate, not a LineTo/ArcTo step'
            )
        start = Point.of(first)
        # declared as list[Skill] because list is invariant: a list[LineTo | ArcTo]
        # variable would not satisfy the RpcArgs tuple[Skill, ...] return type
        steps: list[Skill] = []
        previous = start
        for index, item in enumerate(path[1:], start=1):
            step = PathStep.of(item)
            if step.end == previous:
                raise ValueError(
                    f'adjacent path points must differ: zero-length segment at index {index}'
                )
            steps.append(step)
            previous = step.end
        return net, start, steps, layer, width
