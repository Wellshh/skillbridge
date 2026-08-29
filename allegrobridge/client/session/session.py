# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Session management for a .brd in allegro."""

from __future__ import annotations

from functools import cached_property
from threading import Lock
from types import TracebackType
from typing import Protocol, TypeVar, cast

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
from allegrobridge.client.base import Extensions, SkillModule
from allegrobridge.client.base._rpc import SessionApi, _api_procedures
from allegrobridge.client.workspace import Workspace
from allegrobridge.exceptions import ExtensionError


class _Allegro(Protocol):
    @property
    def workspace(self) -> Workspace: ...

    def close(self) -> None: ...


ApiT = TypeVar('ApiT', bound=SessionApi)


class Session:  # ruff: ignore[too-many-public-methods]
    def __init__(self, allegro: _Allegro) -> None:
        self._allegro = allegro
        self._generation = 1
        self._epoch = self.raw.epoch
        self._closed = False
        self._bindings: dict[type[SessionApi], SessionApi] = {}
        self._binding_errors: dict[type[SessionApi], ExtensionError] = {}
        self._binding_lock = Lock()

    @property
    def raw(self) -> Workspace:
        return self._allegro.workspace

    @property
    def generation(self) -> int:
        # Lazily absorb underlying connection reconnects into session generation.
        epoch = self.raw.epoch
        self._generation += epoch - self._epoch
        self._epoch = epoch
        return self._generation

    def refresh(self) -> None:
        self._generation += 1

    def batch(self, description: str = '', *, dry_run: bool = False) -> Batch:
        return Batch(self, description, dry_run=dry_run)

    def bind(self, api_type: type[ApiT]) -> ApiT:
        """Binds and lazily initializes a strongly-typed extension API to this session.
        Ensures that the declared `SkillModule` (`api_type.module`) and its required
        SKILL procedures are loaded and ready in the remote Allegro workspace. Bound
        API instances are cached per session, ensuring singleton behavior and thread safety.
        Args:
            api_type: The `SessionApi` subclass to bind. Must declare a `module: SkillModule`
                class attribute specifying the packaged `.il` resource.
        Returns:
            An initialized, strongly-typed instance of `api_type` bound to this session.
        Raises:
            TypeError: If `api_type` does not declare a valid `SkillModule`.
            ExtensionError: If the remote SKILL module cannot be located, fails to load,
                or fails the procedure readiness check.
        Example:
            >>> class ProbeApi(SessionApi):
            ...     module = SkillModule('my_package.fixtures', 'server/extensions/probe.il')
            ...
            ...     @read('__abp_probe_project', TypeAdapter(list[ComponentInfo]))
            ...     def __call__(self) -> RpcArgs:
            ...         return ()
            >>> probe = session.bind(ProbeApi)
            >>> components = probe()
        """
        with self._binding_lock:
            if api_type in self._bindings:
                return cast('ApiT', self._bindings[api_type])
            if api_type in self._binding_errors:
                raise self._binding_errors[api_type]
            module = getattr(api_type, 'module', None)
            if not isinstance(module, SkillModule):
                raise TypeError(f'{api_type.__name__} must declare a SkillModule')
            try:
                self.raw._ensure_module(  # ruff: ignore[private-member-access]
                    module,
                    _api_procedures(api_type),
                )
            except ExtensionError as error:
                self._binding_errors[api_type] = error
                raise
            api = api_type(self)
            self._bindings[api_type] = api
            return api

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
