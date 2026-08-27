# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectPadstacks'
_OptionalString = str | None


class PadstackInfo(_Record):
    name: str
    type: str
    usage: str
    start_layer: _OptionalString
    end_layer: _OptionalString
    session_generation: PositiveInt


_PadstackList = list[PadstackInfo]
_PADSTACKS = TypeAdapter(_PadstackList)


@_core_api
class PadstacksApi(SessionApi):
    @read(_PROCEDURE, _PADSTACKS)
    def _project(self, name: str | None) -> RpcArgs:
        return (name,)

    def __call__(self) -> list[PadstackInfo]:
        return self._project(None)

    def __getitem__(self, name: str) -> PadstackInfo:
        padstacks = self._project(name)
        if not padstacks:
            raise KeyError(name)
        return padstacks[0]
