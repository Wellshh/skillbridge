from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Literal, Self, cast

from skillbridge.client.workspace import (
    WorkspaceId,
    _open_workspaces,  # ruff: ignore[import-private-name]
)

from .client.workspace import Workspace

OpenMode = Literal['cli', 'manual']


class Allegro:
    """Lifecycle manager for an active,
    communicable Allegro instance under manual or command mode."""

    mode: OpenMode
    id_: WorkspaceId
    _board: Path | None

    def __init__(self, *, mode: OpenMode, id_: WorkspaceId, board: Path | None) -> None: ...

    @classmethod
    def open(
        cls,
        *,
        mode: OpenMode,
        workspace_id: WorkspaceId,
        executable: str | Path = "allegro.exe",
        timeout: float = 30,
    ) -> Allegro:
        raise NotImplementedError

    @property
    def workspace(self) -> Workspace:
        cache_key = (Workspace, self.id_)
        assert cache_key in _open_workspaces, (
            "workspace not initialized yet, call Allegro.open() first."
        )
        return cast('Workspace', _open_workspaces[cache_key])

    def close(self) -> None: ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
