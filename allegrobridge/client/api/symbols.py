# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import Symbol
from allegrobridge.client.base import Collection
from allegrobridge.client.base._rpc import RpcArgs, _core_api, read

_PROCEDURE = '__abProjectSymbols'

_SymbolList = list[Symbol]
_SYMBOLS = TypeAdapter(_SymbolList)


@_core_api
class SymbolsApi(Collection[Symbol]):
    @read(_PROCEDURE, _SYMBOLS)
    def _project(
        self,
        *,
        kind: str | None = None,
    ) -> RpcArgs:
        return (kind,)

    def __call__(
        self,
        *,
        kind: str | None = None,
        type: str | None = None,  # ruff: ignore[builtin-argument-shadowing]
    ) -> list[Symbol]:
        chosen = kind if kind is not None else type
        return self._project(kind=chosen)

    def _snapshot(self) -> list[Symbol]:
        return self._project(kind=None)
