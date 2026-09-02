# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import Padstack
from allegrobridge.client.base import KeyedCollection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read

_PROCEDURE = '__abProjectPadstacks'

_PadstackList = list[Padstack]
_PADSTACKS = TypeAdapter(_PadstackList)


@_core_api
class PadstacksApi(KeyedCollection[str, Padstack]):
    _key_type = str

    @read(_PROCEDURE, _PADSTACKS)
    def _project(self, name: str | None) -> RpcArgs:
        return (name,)

    def __call__(self) -> list[Padstack]:
        return self.snapshot()

    def _snapshot(self) -> list[Padstack]:
        return self._project(None)

    def _query_key(self, key: str) -> list[Padstack]:
        return self._project(key)
