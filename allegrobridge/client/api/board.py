from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import NonNegativeInt, PositiveInt, TypeAdapter, ValidationError

from allegrobridge.client.api._record import AllegroProtocolError, _Record

if TYPE_CHECKING:
    from allegrobridge.client.session.session import Session

_PROCEDURE = '__abProjectBoard'


class BoardInfo(_Record):
    path: str
    units: str
    component_count: NonNegativeInt
    symbol_count: NonNegativeInt
    net_count: NonNegativeInt
    session_generation: PositiveInt


_BOARD_INFO = TypeAdapter(BoardInfo)


class BoardApi:
    def __init__(self, session: Session) -> None:
        self._session = session

    def __call__(self) -> BoardInfo:
        payload = self._session.raw[_PROCEDURE]()
        candidate: object = payload
        if isinstance(payload, dict):
            candidate = {**payload, 'session_generation': self._session.generation}
        try:
            return _BOARD_INFO.validate_python(candidate, strict=True)
        except ValidationError as error:
            raise AllegroProtocolError(f'{_PROCEDURE} returned an invalid payload') from error
