# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""AllegroBridge Domain API Layer.

API Layering & Loading Principles:
1. Core Runtime:
   - Fundamental kernel required by every Allegro connection
     (e.g. transaction, dry-run, batch kernel).
   - Loaded in `allegro_server.il` at connection time;
     failure blocks `Workspace.open()`.
2. First-Class Domain API:
   - Stable and frequent operations exposed directly on `Session`
     (e.g. `session.board`, `session.drc`).
   - May be eagerly verified or backed lazily by extensions;
     failure is isolated to the specific domain.
3. Custom APIs:
   - Third-party API classes declare a `SkillModule` and bind through `Session.bind()`.
"""

from __future__ import annotations

from allegrobridge.client.api.board import BoardApi
from allegrobridge.client.api.components import ComponentsApi
from allegrobridge.client.api.drc import DrcApi
from allegrobridge.client.api.geometry import ArcTo, BBox, LineTo, Point
from allegrobridge.client.api.layers import LayersApi
from allegrobridge.client.api.nets import NetsApi
from allegrobridge.client.api.padstacks import PadstacksApi
from allegrobridge.client.api.pins import PinsApi
from allegrobridge.client.api.record import (
    AbBoard,
    AbComponent,
    AbComponentRef,
    AbDrc,
    AbDrcObjectRef,
    AbLayer,
    AbNet,
    AbNetRef,
    AbPadstack,
    AbPin,
    AbPinRef,
    AbRoute,
    AbShape,
    AbSymbol,
    AbVia,
    Board,
    Component,
    ComponentRef,
    Drc,
    DrcObjectRef,
    Layer,
    Net,
    NetRef,
    Padstack,
    PcbSymbol,
    Pin,
    PinRef,
    Route,
    Shape,
    Symbol,
    Via,
)
from allegrobridge.client.api.routes import RoutesApi
from allegrobridge.client.api.shapes import ShapesApi
from allegrobridge.client.api.symbols import SymbolsApi
from allegrobridge.client.api.vias import ViasApi
from allegrobridge.client.base import (
    Batch,
    Cmd,
    CmdResult,
    Collection,
    KeyedCollection,
    RpcArgs,
    RpcDef,
    SessionApi,
    SkillModule,
    read,
    write,
)

__all__ = [
    'AbBoard',
    'AbComponent',
    'AbComponentRef',
    'AbDrc',
    'AbDrcObjectRef',
    'AbLayer',
    'AbNet',
    'AbNetRef',
    'AbPadstack',
    'AbPin',
    'AbPinRef',
    'AbRoute',
    'AbShape',
    'AbSymbol',
    'AbVia',
    'ArcTo',
    'BBox',
    'Batch',
    'Board',
    'BoardApi',
    'Cmd',
    'CmdResult',
    'Collection',
    'Component',
    'ComponentRef',
    'ComponentsApi',
    'Drc',
    'DrcApi',
    'DrcObjectRef',
    'KeyedCollection',
    'Layer',
    'LayersApi',
    'LineTo',
    'Net',
    'NetRef',
    'NetsApi',
    'Padstack',
    'PadstacksApi',
    'PcbSymbol',
    'Pin',
    'PinRef',
    'PinsApi',
    'Point',
    'Route',
    'RoutesApi',
    'RpcArgs',
    'RpcDef',
    'SessionApi',
    'Shape',
    'ShapesApi',
    'SkillModule',
    'Symbol',
    'SymbolsApi',
    'Via',
    'ViasApi',
    'read',
    'write',
]
