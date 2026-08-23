from typing import cast
from skillbridge.client.workspace import WorkspaceId, _open_workspaces
from .client.workspace import Workspace
from skillbridge.client.workspace import Workspace as GWorkspace
from pathlib import Path
from typing import Literal
OpenMode = Literal['cli', 'manual']


class Allegro:
    """Lifecycle manager for an active,
    communicable Allegro instance under manual or command mode."""

    mode: OpenMode
    id_: WorkspaceId 
    _board: Path | None

    def __init__(
        self,
        *,
        mode: OpenMode,
        id_: WorkspaceId,
        board: Path | None
    ) -> None:
    
    @classmethod
    def open(
        cls,
        *,
        mode: OpenMode,
        workspace_id: WorkspaceId,
        executable: str | Path = "allegro.exe",
        timeout: float = 30
    ) -> Allegro:
        ...

    @property
    def workspace(self) -> Workspace:
        cache_key = (Workspace, self.id_)
        assert cache_key in _open_workspaces, f"workspace not initialized yet, call Allegro.open() first."
        return cast(Workspace, _open_workspaces[cache_key])

    def close(self) -> None: 
        ...

    def __enter__(self) -> Allegro:
        ...

    def __exit__(self) -> None:
        ...

    

