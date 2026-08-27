# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Session management for a .brd in allegro."""

from __future__ import annotations

from functools import cached_property
from types import TracebackType
from typing import Protocol

from typing_extensions import Self

from allegrobridge.client.api import (
    Batch,
    BoardApi,
    ComponentsApi,
    DrcApi,
    LayersApi,
    NetsApi,
    PadstacksApi,
    PinsApi,
    RoutesApi,
    ShapesApi,
    SymbolsApi,
    ViasApi,
)
from allegrobridge.client.base import Extensions
from allegrobridge.client.base._rpc import _api_procedures
from allegrobridge.client.workspace import Workspace


class _Allegro(Protocol):
    @property
    def workspace(self) -> Workspace: ...

    def close(self) -> None: ...


class Session:
    def __init__(self, allegro: _Allegro) -> None:
        self._allegro = allegro
        self._generation = 1
        self._closed = False

    @property
    def raw(self) -> Workspace:
        return self._allegro.workspace

    @property
    def generation(self) -> int:
        return self._generation

    def batch(self, description: str = '', *, dry_run: bool = False) -> Batch:
        return Batch(self, description, dry_run=dry_run)

    # --- First-Class Domain APIs ---
    # Direct access on Session. Heavy or version-sensitive domains (e.g. DRC)
    # can delegate internally to lazy extension loaders to keep Workspace startup light.
    @cached_property
    def board(self) -> BoardApi:
        return BoardApi(self)

    @cached_property
    def components(self) -> ComponentsApi:
        return ComponentsApi(self)

    @cached_property
    def layers(self) -> LayersApi:
        return LayersApi(self)

    @cached_property
    def nets(self) -> NetsApi:
        return NetsApi(self)

    @cached_property
    def padstacks(self) -> PadstacksApi:
        return PadstacksApi(self)

    @cached_property
    def pins(self) -> PinsApi:
        return PinsApi(self)

    @cached_property
    def symbols(self) -> SymbolsApi:
        return SymbolsApi(self)

    @cached_property
    def vias(self) -> ViasApi:
        self.raw._ensure_extension(  # ruff: ignore[private-member-access]
            'vias',
            _api_procedures(ViasApi),
        )
        return ViasApi(self)

    @cached_property
    def routes(self) -> RoutesApi:
        self.raw._ensure_extension(  # ruff: ignore[private-member-access]
            'routes',
            _api_procedures(RoutesApi),
        )
        return RoutesApi(self)

    @cached_property
    def shapes(self) -> ShapesApi:
        self.raw._ensure_extension(  # ruff: ignore[private-member-access]
            'shapes',
            _api_procedures(ShapesApi),
        )
        return ShapesApi(self)

    @cached_property
    def drc(self) -> DrcApi:
        self.raw._ensure_extension(  # ruff: ignore[private-member-access]
            'drc',
            _api_procedures(DrcApi),
        )
        return DrcApi(self)

    # --- Bundled & Custom Extensions ---
    @cached_property
    def ext(self) -> Extensions:
        return Extensions(self)

    def close(self) -> None:
        if self._closed:
            return
        self._allegro.close()
        self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
