# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import List, Optional

from pydantic import PositiveInt, TypeAdapter

from allegrobridge.client.api._record import _Record
from allegrobridge.client.api._rpc import RpcArgs, SessionApi, _core_api, read

_PROCEDURE = '__abProjectSymbols'
_OptionalString = Optional[str]


class SymbolInfo(_Record):
    name: str
    type: str
    refdes: _OptionalString
    x: float
    y: float
    rotation: float
    session_generation: PositiveInt


_SymbolList = List[SymbolInfo]
_SYMBOLS = TypeAdapter(_SymbolList)


@_core_api
class SymbolsApi(SessionApi):
    @read(_PROCEDURE, _SYMBOLS, none_as_empty=True)
    def __call__(
        self,
        *,
        type: str | None = None,  # ruff: ignore[builtin-argument-shadowing]
    ) -> RpcArgs:
        return (type,)
