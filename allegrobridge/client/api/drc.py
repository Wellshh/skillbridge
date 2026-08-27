# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, direct, read, write
from allegrobridge.client.api.routes import Point
from allegrobridge.client.api.shapes import BBox

if TYPE_CHECKING:  # pragma: no cover
    from allegrobridge.client.api.components import ComponentInfo
    from allegrobridge.client.api.nets import NetInfo
    from allegrobridge.client.api.pins import PinInfo

_PROCEDURE = '__abProjectDrcs'
_UPDATE_PROCEDURE = '__abUpdateDrcs'
_CHECK_PROCEDURE = '__abCheckDrcs'


class ComponentRef(_Record):
    kind: Literal['component']
    refdes: str


class NetRef(_Record):
    kind: Literal['net']
    name: str


class PinRef(_Record):
    kind: Literal['pin']
    refdes: str
    number: str


DrcObjectRef = ComponentRef | NetRef | PinRef
_DrcObjectList = list[DrcObjectRef]


class DrcInfo(_Record):
    name: str
    category: str
    source: str
    expected: str
    actual: str
    layer: str
    location: Point
    bbox: BBox
    objects: _DrcObjectList
    session_generation: PositiveInt


_DrcList = list[DrcInfo]
_DRCS = TypeAdapter(_DrcList)


class DrcApi(SessionApi):
    @read(_PROCEDURE, _DRCS)
    def __call__(self) -> RpcArgs:
        return ()

    @write(_UPDATE_PROCEDURE, _DRCS)
    def update(self) -> RpcArgs:
        return ()

    # axlDRCItem mutates marker state that database rollback does not reliably restore.
    # Keep check as one direct RPC: no preview, command, or Batch affordances.
    @direct(_CHECK_PROCEDURE, _DRCS)
    def check(self, target: ComponentInfo | NetInfo | PinInfo) -> RpcArgs:
        # Keep these lazy so importing DRC cannot reorder core readiness registration.
        from allegrobridge.client.api.components import (  # ruff: ignore[import-outside-top-level]
            ComponentInfo,
        )
        from allegrobridge.client.api.nets import NetInfo  # ruff: ignore[import-outside-top-level]
        from allegrobridge.client.api.pins import PinInfo  # ruff: ignore[import-outside-top-level]

        if isinstance(target, ComponentInfo):
            return 'component', target.refdes, None
        if isinstance(target, NetInfo):
            return 'net', target.name, None
        if isinstance(target, PinInfo):
            return 'pin', target.refdes, target.number
        raise TypeError('target must be ComponentInfo, NetInfo, or PinInfo')
