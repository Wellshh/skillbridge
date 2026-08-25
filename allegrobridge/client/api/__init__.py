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

__all__ = [
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
    'RpcArgs',
    'SessionApi',
    'extension',
    'read',
    'write',
]
