from __future__ import annotations

import sys
from contextlib import suppress
from os import getenv
from pathlib import Path
from shutil import which
from subprocess import Popen, TimeoutExpired
from tempfile import TemporaryDirectory
from time import monotonic, sleep
from types import TracebackType
from typing import Literal

import skillbridge.server
from skillbridge.client.workspace import WorkspaceId

from .client.workspace import Workspace

OpenMode = Literal['cli', 'manual']

_POLL_INTERVAL = 0.1
_PROCESS_EXIT_TIMEOUT = 5.0

_INSTALL_ROOT_VARS = ('CDSROOT', 'Sigrity_EDA_DIR')


def _resolve_executable(executable: str | Path) -> str:
    path = Path(executable)
    if path.is_file():
        return str(path)

    found = which(str(executable))
    if found is not None:
        return found

    names = [path.name] if path.suffix else [path.name, f'{path.name}.exe']
    for var in _INSTALL_ROOT_VARS:
        root = getenv(var)
        if root is None:
            continue
        for name in names:
            candidate = Path(root) / 'tools' / 'bin' / name
            if candidate.is_file():
                return str(candidate)

    raise FileNotFoundError(
        f"could not find the Allegro executable {str(executable)!r}: not on PATH and no "
        f"Cadence installation found via {', '.join(_INSTALL_ROOT_VARS)}; "
        "pass the full path with executable=..."
    )


def _default_workspace_id(*, force_tcp: bool) -> str:
    return '7777' if sys.platform == 'win32' or force_tcp else 'default'


class Allegro:
    """An open Allegro window connected to a Workspace."""

    def __init__(
        self,
        *,
        mode: OpenMode,
        workspace_id: WorkspaceId,
        board: Path | None,
        workspace: Workspace,
        process: Popen[bytes] | None = None,
        temp_dir: TemporaryDirectory[str] | None = None,
    ) -> None:
        self.mode = mode
        self.workspace_id = workspace_id
        self.board = board
        self._workspace = workspace
        self._process = process
        self._temp_dir = temp_dir
        self._closed = False

    @classmethod
    def connect(
        cls,
        workspace_id: WorkspaceId = None,
        *,
        board: str | Path | None = None,
        force_tcp: bool = False,
    ) -> Allegro:
        ws_id = (
            _default_workspace_id(force_tcp=force_tcp)
            if workspace_id is None
            else str(workspace_id)
        )
        board_path = Path(board).resolve() if board is not None else None
        workspace = cls._open_workspace(ws_id, force_tcp=force_tcp)
        return cls(
            mode='manual',
            workspace_id=ws_id,
            board=board_path,
            workspace=workspace,
        )

    @classmethod
    def launch(
        cls,
        board: str | Path | None = None,
        *,
        workspace_id: WorkspaceId = None,
        executable: str | Path = "allegro.exe",
        timeout: float = 120.0,
        force_tcp: bool = False,
    ) -> Allegro:
        ws_id = (
            _default_workspace_id(force_tcp=force_tcp)
            if workspace_id is None
            else str(workspace_id)
        )
        board_path = Path(board).resolve() if board is not None else None
        resolved = _resolve_executable(executable)

        server_file = Path(skillbridge.server.__file__).with_name('python_server.il').as_posix()
        force_tcp_flag = ' ?forceTcp t' if force_tcp else ''
        script_content = (
            f'skill load("{server_file}")\n'
            f'skill pyStartServer(?id "{ws_id}" ?singleMode t '
            f'?python "{Path(sys.executable).as_posix()}"{force_tcp_flag})\n'
        )

        temp_dir = TemporaryDirectory(prefix='allegrobridge-')
        script_path = Path(temp_dir.name) / 'startup.scr'
        command = [resolved, '-s', script_path.as_posix()]
        if board_path is not None:
            command.append(board_path.as_posix())

        try:
            script_path.write_text(script_content, encoding='utf-8')
            process = Popen(command, shell=False)  # ruff: ignore[subprocess-without-shell-equals-true]
        except BaseException:
            temp_dir.cleanup()
            raise

        try:
            workspace = cls._wait_for_workspace(
                process,
                ws_id,
                force_tcp=force_tcp,
                timeout=timeout,
            )
        except BaseException:
            cls._stop_process(process)
            temp_dir.cleanup()
            raise

        return cls(
            mode='cli',
            workspace_id=ws_id,
            board=board_path,
            workspace=workspace,
            process=process,
            temp_dir=temp_dir,
        )

    @classmethod
    def open(
        cls,
        *,
        mode: OpenMode,
        workspace_id: WorkspaceId = None,
        board: str | Path | None = None,
        executable: str | Path = "allegro.exe",
        timeout: float = 120.0,
        force_tcp: bool = False,
    ) -> Allegro:
        if mode == 'manual':
            return cls.connect(
                workspace_id=workspace_id,
                board=board,
                force_tcp=force_tcp,
            )
        if mode == 'cli':
            return cls.launch(
                board=board,
                workspace_id=workspace_id,
                executable=executable,
                timeout=timeout,
                force_tcp=force_tcp,
            )
        raise ValueError("mode must be 'cli' or 'manual'")

    @classmethod
    def _wait_for_workspace(
        cls,
        process: Popen[bytes],
        workspace_id: WorkspaceId,
        *,
        force_tcp: bool,
        timeout: float,
    ) -> Workspace:
        deadline = monotonic() + timeout
        last_error: OSError | RuntimeError | None = None
        while monotonic() < deadline:
            return_code = process.poll()
            if return_code is not None:
                raise RuntimeError(
                    f"Allegro exited before the server was ready (exit code {return_code})"
                )

            try:
                return cls._open_workspace(workspace_id, force_tcp=force_tcp)
            except (OSError, RuntimeError) as error:
                last_error = error
                sleep(_POLL_INTERVAL)

        raise TimeoutError(
            f"Allegro server was not ready within {timeout:g} seconds"
        ) from last_error

    @staticmethod
    def _open_workspace(workspace_id: WorkspaceId, *, force_tcp: bool) -> Workspace:
        workspace = Workspace.open(workspace_id, force_tcp=force_tcp)
        if not isinstance(workspace, Workspace):
            workspace.close()
            raise RuntimeError("Connected server is not running in Allegro")

        try:
            ok = workspace['plus'](1, 2) == 3  # ruff: ignore[magic-value-comparison]
        except BaseException:
            workspace.close()
            raise
        if not ok:
            workspace.close()
            raise RuntimeError("Allegro server readiness check failed")
        return workspace

    @staticmethod
    def _stop_process(process: Popen[bytes]) -> None:
        if process.poll() is not None:
            return
        with suppress(OSError):
            process.terminate()
        try:
            process.wait(timeout=_PROCESS_EXIT_TIMEOUT)
        except TimeoutExpired:
            with suppress(OSError):
                process.kill()
            process.wait(timeout=_PROCESS_EXIT_TIMEOUT)

    @property
    def workspace(self) -> Workspace:
        return self._workspace

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True

        self._workspace.close()
        if self._process is not None:
            self._stop_process(self._process)
        if self._temp_dir is not None:
            self._temp_dir.cleanup()

    def __enter__(self) -> Allegro:  # ruff: ignore[non-self-return-type]
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
