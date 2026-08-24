from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional

from pydantic import PositiveInt, TypeAdapter, ValidationError

from allegrobridge.client.api._record import AllegroProtocolError, _Record

if TYPE_CHECKING:
    from allegrobridge.client.session.session import Session

_PROCEDURE = '__abProjectComponents'
_OptionalFloat = Optional[float]


class ComponentInfo(_Record):
    refdes: str
    device_type: str
    package: str
    component_class: str
    placement: Literal['placed', 'unplaced']
    x: _OptionalFloat
    y: _OptionalFloat
    rotation: _OptionalFloat
    session_generation: PositiveInt


_ComponentList = List[ComponentInfo]
_COMPONENTS = TypeAdapter(_ComponentList)


class ComponentsApi:
    def __init__(self, session: Session) -> None:
        self._session = session

    def _validate(self, payload: object) -> list[ComponentInfo]:
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
            return _COMPONENTS.validate_python(candidate, strict=True)
        except ValidationError as error:
            raise AllegroProtocolError(f'{_PROCEDURE} returned an invalid payload') from error

    def __call__(self, *, include_unplaced: bool = True) -> list[ComponentInfo]:
        return self._validate(self._session.raw[_PROCEDURE](None, include_unplaced))

    def __getitem__(self, refdes: str) -> ComponentInfo:
        include_unplaced = True
        components = self._validate(self._session.raw[_PROCEDURE](refdes, include_unplaced))
        if not components:
            raise KeyError(refdes)
        return components[0]
