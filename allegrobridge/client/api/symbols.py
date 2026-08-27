# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.base import SessionRecord
from allegrobridge.client.base._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectSymbols'
_OptionalString = str | None


class SymbolInfo(SessionRecord):
    name: str
    type: str
    refdes: _OptionalString
    x: float
    y: float
    rotation: float


_SymbolList = list[SymbolInfo]
_SYMBOLS = TypeAdapter(_SymbolList)


@_core_api
class SymbolsApi(SessionApi):
    @read(_PROCEDURE, _SYMBOLS)
    def __call__(
        self,
        *,
        type: str | None = None,  # ruff: ignore[builtin-argument-shadowing]
    ) -> RpcArgs:
        return (type,)
