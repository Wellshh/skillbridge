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
3. Bundled & Custom Extensions:
   - Specialized, version-sensitive, or complex toolkits
     (e.g. `session.ext.rules`, `session.ext.autoplace`).
   - Lazily imported and isolated under `session.ext.<name>`.
"""

from __future__ import annotations

from allegrobridge.client.api._extensions import extension
from allegrobridge.client.api._rpc import (
    Batch,
    Command,
    CommandResult,
    RpcArgs,
    SessionApi,
    read,
    write,
)
from allegrobridge.client.api.board import BoardApi, BoardInfo
from allegrobridge.client.api.components import ComponentInfo, ComponentsApi
from allegrobridge.client.api.layers import LayerInfo, LayersApi
from allegrobridge.client.api.nets import NetInfo, NetsApi
from allegrobridge.client.api.padstacks import PadstackInfo, PadstacksApi
from allegrobridge.client.api.pins import PinInfo, PinsApi
from allegrobridge.client.api.routes import Point, RouteInfo, RoutesApi
from allegrobridge.client.api.shapes import BBox, ShapeInfo, ShapesApi
from allegrobridge.client.api.symbols import SymbolInfo, SymbolsApi
from allegrobridge.client.api.vias import ViaInfo, ViasApi

__all__ = [
    'BBox',
    'Batch',
    'BoardApi',
    'BoardInfo',
    'Command',
    'CommandResult',
    'ComponentInfo',
    'ComponentsApi',
    'LayerInfo',
    'LayersApi',
    'NetInfo',
    'NetsApi',
    'PadstackInfo',
    'PadstacksApi',
    'PinInfo',
    'PinsApi',
    'Point',
    'RouteInfo',
    'RoutesApi',
    'RpcArgs',
    'SessionApi',
    'ShapeInfo',
    'ShapesApi',
    'SymbolInfo',
    'SymbolsApi',
    'ViaInfo',
    'ViasApi',
    'extension',
    'read',
    'write',
]
