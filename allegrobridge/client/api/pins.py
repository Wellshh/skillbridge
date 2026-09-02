# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import Component, Net, Pin
from allegrobridge.client.base import KeyedCollection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read

_PROCEDURE = '__abProjectPins'

_PinList = list[Pin]
_PINS = TypeAdapter(_PinList)


@_core_api
class PinsApi(KeyedCollection[tuple[str, str], Pin]):
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
        component: str | Component | None = None,
        net: str | Net | None = None,
    ) -> list[Pin]:
        refdes = component.refdes if isinstance(component, Component) else component
        net_name = net.name if isinstance(net, Net) else net
        return self._project(refdes, None, net_name)

    def _snapshot(self) -> list[Pin]:
        return self._project(None, None, None)

    def _query_key(self, key: tuple[str, str]) -> list[Pin]:
        component, number = key
        return self._project(component, number, None)
