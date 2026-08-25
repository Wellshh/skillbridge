"""Wrapped around higher-level api of allegro, different from `:class.RemoteObject`."""

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
from allegrobridge.client.api.nets import NetInfo, NetsApi

__all__ = [
    'Batch',
    'BoardApi',
    'BoardInfo',
    'Command',
    'CommandResult',
    'ComponentInfo',
    'ComponentsApi',
    'NetInfo',
    'NetsApi',
    'RpcArgs',
    'SessionApi',
    'extension',
    'read',
    'write',
]
