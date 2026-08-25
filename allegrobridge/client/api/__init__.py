"""Wrapped around higher-level api of allegro, different from `:class.RemoteObject`."""

from __future__ import annotations

from allegrobridge.client.api._record import AllegroProtocolError, _Record
from allegrobridge.client.api._rpc import Command, RpcArgs, SessionApi, read, write
from allegrobridge.client.api.board import BoardApi, BoardInfo
from allegrobridge.client.api.components import ComponentInfo, ComponentsApi
from allegrobridge.client.api.nets import NetInfo, NetsApi

__all__ = [
    'AllegroProtocolError',
    'BoardApi',
    'BoardInfo',
    'Command',
    'ComponentInfo',
    'ComponentsApi',
    'NetInfo',
    'NetsApi',
    'RpcArgs',
    'SessionApi',
    '_Record',
    'read',
    'write',
]
