"""Wrapped around higher-level api of allegro, different from `:class.RemoteObject`."""

from __future__ import annotations

from allegrobridge.client.api._record import AllegroProtocolError
from allegrobridge.client.api.board import BoardApi, BoardInfo

__all__ = ['AllegroProtocolError', 'BoardApi', 'BoardInfo']
