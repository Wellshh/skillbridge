# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.base import Collection, SessionRecord, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, read, write

_PROJECT_PROCEDURE = '__abProjectVias'
_CREATE_PROCEDURE = '__abCreateVia'
_OptionalString = str | None


class ViaInfo(SessionRecord):
    padstack: str
    net: _OptionalString
    x: float
    y: float
    rotation: float
    mirroring: Literal['mirrored', 'unmirrored']
    start_layer: str
    end_layer: str


_ViaList = list[ViaInfo]
_VIAS = TypeAdapter(_ViaList)
_VIA = TypeAdapter(ViaInfo)


class ViasApi(Collection[ViaInfo]):
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
    ) -> list[ViaInfo]:
        return self._project(net=net, layer=layer, padstack=padstack)

    def _snapshot(self) -> list[ViaInfo]:
        return self._project(net=None, layer=None, padstack=None)

    @write(_CREATE_PROCEDURE, _VIA)
    def create(
        self,
        padstack: str,
        *,
        at: tuple[float, float],
        net: str | None = None,
        rotation: float = 0.0,
        mirrored: bool = False,
    ) -> RpcArgs:
        return padstack, at, net, mirrored, rotation
