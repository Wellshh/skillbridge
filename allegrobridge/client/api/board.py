# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import Board
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectBoard'

_BOARD_INFO = TypeAdapter(Board)


@_core_api
class BoardApi(SessionApi):
    @read(_PROCEDURE, _BOARD_INFO)
    def __call__(self) -> RpcArgs:
        return ()
