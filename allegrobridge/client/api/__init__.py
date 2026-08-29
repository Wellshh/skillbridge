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

from allegrobridge.client.api.board import BoardApi, BoardInfo
from allegrobridge.client.api.components import ComponentInfo, ComponentsApi
from allegrobridge.client.api.drc import (
    ComponentRef,
    DrcApi,
    DrcInfo,
    DrcObjectRef,
    NetRef,
    PinRef,
)
from allegrobridge.client.api.layers import LayerInfo, LayersApi
from allegrobridge.client.api.nets import NetInfo, NetsApi
from allegrobridge.client.api.padstacks import PadstackInfo, PadstacksApi
from allegrobridge.client.api.pins import PinInfo, PinsApi
from allegrobridge.client.api.routes import Point, RouteInfo, RoutesApi
from allegrobridge.client.api.shapes import BBox, ShapeInfo, ShapesApi
from allegrobridge.client.api.symbols import SymbolInfo, SymbolsApi
from allegrobridge.client.api.vias import ViaInfo, ViasApi
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
    'BBox',
    'Batch',
    'BoardApi',
    'BoardInfo',
    'Cmd',
    'CmdResult',
    'Collection',
    'ComponentInfo',
    'ComponentRef',
    'ComponentsApi',
    'DrcApi',
    'DrcInfo',
    'DrcObjectRef',
    'KeyedCollection',
    'LayerInfo',
    'LayersApi',
    'NetInfo',
    'NetRef',
    'NetsApi',
    'PadstackInfo',
    'PadstacksApi',
    'PinInfo',
    'PinRef',
    'PinsApi',
    'Point',
    'RouteInfo',
    'RoutesApi',
    'RpcArgs',
    'RpcDef',
    'SessionApi',
    'ShapeInfo',
    'ShapesApi',
    'SkillModule',
    'SymbolInfo',
    'SymbolsApi',
    'ViaInfo',
    'ViasApi',
    'read',
    'write',
]
