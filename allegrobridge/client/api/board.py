from __future__ import annotations

from pydantic import NonNegativeInt, PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectBoard'


class BoardInfo(_Record):
    path: str
    units: str
    component_count: NonNegativeInt
    symbol_count: NonNegativeInt
    net_count: NonNegativeInt
    session_generation: PositiveInt


_BOARD_INFO = TypeAdapter(BoardInfo)


@_core_api
class BoardApi(SessionApi):
    @read(_PROCEDURE, _BOARD_INFO)
    def __call__(self) -> RpcArgs:
        return ()
