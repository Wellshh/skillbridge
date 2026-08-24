from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import NonNegativeInt, PositiveInt, TypeAdapter, ValidationError

from allegrobridge.client.api._record import AllegroProtocolError, _Record

if TYPE_CHECKING:
    from allegrobridge.client.session.session import Session

_PROCEDURE = '__abProjectNets'


class NetInfo(_Record):
    name: str
    branch_count: NonNegativeInt
    unconnected_count: NonNegativeInt
    unplaced_pin_count: NonNegativeInt
    session_generation: PositiveInt


_NetList = List[NetInfo]
_NETS = TypeAdapter(_NetList)


class NetsApi:
    def __init__(self, session: Session) -> None:
        self._session = session

    def _validate(self, payload: object) -> list[NetInfo]:
        if payload is None:
            payload = []
        candidate: object = payload
        if isinstance(payload, list):
            candidate = [
                {**item, 'session_generation': self._session.generation}
                if isinstance(item, dict)
                else item
                for item in payload
            ]
        try:
            return _NETS.validate_python(candidate, strict=True)
        except ValidationError as error:
            raise AllegroProtocolError(f'{_PROCEDURE} returned an invalid payload') from error

    def __call__(self) -> list[NetInfo]:
        return self._validate(self._session.raw[_PROCEDURE](None))

    def __getitem__(self, name: str) -> NetInfo:
        nets = self._validate(self._session.raw[_PROCEDURE](name))
        if not nets:
            raise KeyError(name)
        return nets[0]
