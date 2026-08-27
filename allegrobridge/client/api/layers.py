# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.base import SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectLayers'


class LayerInfo(SessionRecord):
    name: str
    class_name: str
    subclass: str
    number: int

    @property
    def is_etch(self) -> bool:
        return self.class_name == 'ETCH'


_LayerList = list[LayerInfo]
_LAYERS = TypeAdapter(_LayerList)


@_core_api
class LayersApi(SessionApi):
    @read(_PROCEDURE, _LAYERS)
    def _project(self, name: str | None, etch_only: bool) -> RpcArgs:
        return name, etch_only

    def __call__(self, *, etch_only: bool = False) -> list[LayerInfo]:
        return self._project(None, etch_only)

    def __getitem__(self, name: str) -> LayerInfo:
        etch_only = False
        layers = self._project(name, etch_only)
        if not layers:
            raise KeyError(name)
        return layers[0]
