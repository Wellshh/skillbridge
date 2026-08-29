# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""AllegroBridge Client Base Infrastructure."""

from __future__ import annotations

from allegrobridge.client.base._datastructure import (
    _Collection as Collection,
)
from allegrobridge.client.base._datastructure import (
    _KeyedCollection as KeyedCollection,
)
from allegrobridge.client.base._extensions import SkillModule, extension
from allegrobridge.client.base._extensions import _Extensions as Extensions
from allegrobridge.client.base._future import Cmd, CmdResult
from allegrobridge.client.base._record import (
    _ID,
    BaseRecord,
    SessionRecord,
)
from allegrobridge.client.base._rpc import (
    Batch,
    RpcArgs,
    RpcDef,
    SessionApi,
    direct,
    read,
    write,
)

__all__ = [
    '_ID',
    'BaseRecord',
    'Batch',
    'Cmd',
    'CmdResult',
    'Collection',
    'Extensions',
    'KeyedCollection',
    'RpcArgs',
    'RpcDef',
    'SessionApi',
    'SessionRecord',
    'SkillModule',
    'direct',
    'extension',
    'read',
    'write',
]
