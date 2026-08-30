# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.api.geometry import _OptionalLocated
from allegrobridge.client.base import KeyedCollection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read

_PROCEDURE = '__abProjectPins'
_OptionalString = str | None


class PinInfo(_OptionalLocated):
    refdes: str
    number: str
    net: _OptionalString
    padstack: _OptionalString
    placement: Literal['placed', 'unplaced']
    start_layer: _OptionalString
    end_layer: _OptionalString


_PinList = list[PinInfo]
_PINS = TypeAdapter(_PinList)


@_core_api
class PinsApi(KeyedCollection[tuple[str, str], PinInfo]):
    def _is_key(self, key: object) -> bool:
        match key:
            case (str(), str()) if isinstance(key, tuple):
                return True
            case _:
                return False

    @read(_PROCEDURE, _PINS)
    def _project(
        self,
        component: str | None,
        number: str | None,
        net: str | None,
    ) -> RpcArgs:
        return component, number, net

    def __call__(
        self,
        *,
        component: str | None = None,
        net: str | None = None,
    ) -> list[PinInfo]:
        return self._project(component, None, net)

    def _snapshot(self) -> list[PinInfo]:
        return self._project(None, None, None)

    def _query_key(self, key: tuple[str, str]) -> list[PinInfo]:
        component, number = key
        return self._project(component, number, None)
