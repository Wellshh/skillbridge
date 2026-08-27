# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from allegrobridge.client.base import SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectPins'
_OptionalFloat = float | None
_OptionalString = str | None


class PinInfo(SessionRecord):
    refdes: str
    number: str
    net: _OptionalString
    padstack: _OptionalString
    placement: Literal['placed', 'unplaced']
    x: _OptionalFloat
    y: _OptionalFloat
    rotation: _OptionalFloat
    start_layer: _OptionalString
    end_layer: _OptionalString


_PinList = list[PinInfo]
_PINS = TypeAdapter(_PinList)


@_core_api
class PinsApi(SessionApi):
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

    def __getitem__(self, key: tuple[str, str]) -> PinInfo:
        component, number = key
        pins = self._project(component, number, None)
        if not pins:
            raise KeyError(key)
        return pins[0]
