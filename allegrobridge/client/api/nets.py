# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import Net
from allegrobridge.client.base import KeyedCollection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read

_PROCEDURE = '__abProjectNets'

_NetList = list[Net]
_NETS = TypeAdapter(_NetList)


@_core_api
class NetsApi(KeyedCollection[str, Net]):
    _key_type = str

    @read(_PROCEDURE, _NETS)
    def _project(self, name: str | None) -> RpcArgs:
        return (name,)

    def __call__(self) -> list[Net]:
        return self.snapshot()

    def _snapshot(self) -> list[Net]:
        return self._project(None)

    def _query_key(self, key: str) -> list[Net]:
        return self._project(key)
