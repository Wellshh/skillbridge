from __future__ import annotations

from typing import List

from pydantic import NonNegativeInt, PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, read

_PROCEDURE = '__abProjectNets'


class NetInfo(_Record):
    name: str
    branch_count: NonNegativeInt
    unconnected_count: NonNegativeInt
    unplaced_pin_count: NonNegativeInt
    session_generation: PositiveInt


_NetList = List[NetInfo]
_NETS = TypeAdapter(_NetList)


class NetsApi(SessionApi):
    @read(_PROCEDURE, _NETS, none_as_empty=True)
    def _project(self, name: str | None) -> RpcArgs:
        return (name,)

    def __call__(self) -> list[NetInfo]:
        return self._project(None)

    def __getitem__(self, name: str) -> NetInfo:
        nets = self._project(name)
        if not nets:
            raise KeyError(name)
        return nets[0]
