# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, read, write
from skillbridge import SkillTuple

_PROJECT_PROCEDURE = '__abProjectVias'
_CREATE_PROCEDURE = '__abCreateVia'
_OptionalString = Optional[str]


class ViaInfo(_Record):
    padstack: str
    net: _OptionalString
    x: float
    y: float
    rotation: float
    mirroring: Literal['mirrored', 'unmirrored']
    start_layer: str
    end_layer: str
    session_generation: PositiveInt


_ViaList = List[ViaInfo]
_VIAS = TypeAdapter(_ViaList)
_VIA = TypeAdapter(ViaInfo)


class ViasApi(SessionApi):
    @read(_PROJECT_PROCEDURE, _VIAS, none_as_empty=True)
    def __call__(
        self,
        *,
        net: str | None = None,
        layer: str | None = None,
        padstack: str | None = None,
    ) -> RpcArgs:
        return net, layer, padstack

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
        return padstack, SkillTuple(at), net, mirrored, rotation
