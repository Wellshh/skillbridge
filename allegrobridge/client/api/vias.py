# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.geometry import (
    Point,
    finite,
)
from allegrobridge.client.api.record import Via
from allegrobridge.client.base import Collection, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, read, write

_PROJECT_PROCEDURE = '__abProjectVias'
_CREATE_PROCEDURE = '__abCreateVia'

_ViaList = list[Via]
_VIAS = TypeAdapter(_ViaList)
_VIA = TypeAdapter(Via)


class ViasApi(Collection[Via]):
    module = SkillModule('allegrobridge.server', 'extensions/vias.il')

    @read(_PROJECT_PROCEDURE, _VIAS)
    def _project(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        padstack: str | None = None,
    ) -> RpcArgs:
        return net, layer, padstack

    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        padstack: str | None = None,
    ) -> list[Via]:
        return self._project(net=net, layer=layer, padstack=padstack)

    def _snapshot(self) -> list[Via]:
        return self._project(net=None, layer=None, padstack=None)

    @write(_CREATE_PROCEDURE, _VIA)
    def create(
        self,
        padstack: str,
        *,
        at: Point | tuple[float, float],
        net: str | None = None,
        rotation: float = 0.0,
        mirrored: bool = False,
    ) -> RpcArgs:
        return padstack, Point.of(at), net, mirrored, finite(rotation)
