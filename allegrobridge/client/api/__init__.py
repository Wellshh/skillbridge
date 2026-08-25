"""Wrapped around higher-level api of allegro, different from `:class.RemoteObject`."""

from __future__ import annotations

from allegrobridge.client.api._extensions import Extensions, extension
from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import (
    Batch,
    Command,
    CommandResult,
    RpcArgs,
    SessionApi,
    core_api,
    read,
    write,
)
from allegrobridge.client.api.board import BoardApi, BoardInfo
from allegrobridge.client.api.components import ComponentInfo, ComponentsApi
from allegrobridge.client.api.nets import NetInfo, NetsApi
from allegrobridge.exceptions import AllegroProtocolError

__all__ = [
    'AllegroProtocolError',
    'Batch',
    'BoardApi',
    'BoardInfo',
    'Command',
    'CommandResult',
    'ComponentInfo',
    'ComponentsApi',
    'Extensions',
    'NetInfo',
    'NetsApi',
    'RpcArgs',
    'SessionApi',
    '_Record',
    'core_api',
    'extension',
    'read',
    'write',
]
