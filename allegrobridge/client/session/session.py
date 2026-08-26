"""Session management for a .brd in allegro."""

from __future__ import annotations

from functools import cached_property
from types import TracebackType
from typing import Protocol

from typing_extensions import Self

from allegrobridge.client.api import Batch, BoardApi, ComponentsApi, LayersApi, NetsApi, PinsApi
from allegrobridge.client.api._extensions import _Extensions
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
    def pins(self) -> PinsApi:
        return PinsApi(self)

    # --- Bundled & Custom Extensions ---
    @cached_property
    def ext(self) -> _Extensions:
        return _Extensions(self)

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
