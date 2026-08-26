# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import List, Literal, Union

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, read
from allegrobridge.client.api.routes import Point
from allegrobridge.client.api.shapes import BBox

_PROCEDURE = '__abProjectDrcs'


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


DrcObjectRef = Union[ComponentRef, NetRef, PinRef]
_DrcObjectList = List[DrcObjectRef]


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


_DrcList = List[DrcInfo]
_DRCS = TypeAdapter(_DrcList)


class DrcApi(SessionApi):
    @read(_PROCEDURE, _DRCS, none_as_empty=True)
    def __call__(self) -> RpcArgs:
        return ()
