# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import NonNegativeInt, TypeAdapter

from allegrobridge.client.base import SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectNets'


class NetInfo(SessionRecord):
    name: str
    branch_count: NonNegativeInt
    unconnected_count: NonNegativeInt
    unplaced_pin_count: NonNegativeInt


_NetList = list[NetInfo]
_NETS = TypeAdapter(_NetList)


@_core_api
class NetsApi(SessionApi):
    @read(_PROCEDURE, _NETS)
    def _project(self, name: str | None) -> RpcArgs:
        return (name,)

    def __call__(self) -> list[NetInfo]:
        return self._project(None)

    def __getitem__(self, name: str) -> NetInfo:
        nets = self._project(name)
        if not nets:
            raise KeyError(name)
        return nets[0]
