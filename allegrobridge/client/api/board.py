# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import NonNegativeInt, TypeAdapter

from allegrobridge.client.base import SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectBoard'


class BoardInfo(SessionRecord):
    path: str
    units: str
    component_count: NonNegativeInt
    symbol_count: NonNegativeInt
    net_count: NonNegativeInt


_BOARD_INFO = TypeAdapter(BoardInfo)


@_core_api
class BoardApi(SessionApi):
    @read(_PROCEDURE, _BOARD_INFO)
    def __call__(self) -> RpcArgs:
        return ()
