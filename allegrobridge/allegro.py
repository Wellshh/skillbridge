# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import logging
import os
import sys
from os import getenv
from pathlib import Path
from shutil import which
from time import monotonic, sleep
from types import TracebackType
from typing import Literal
from uuid import uuid4

from typing_extensions import Self

import allegrobridge.server
from allegrobridge._kernel import server as _kernel_server
from allegrobridge._kernel.client.workspace import WorkspaceId

from ._runtime import CliRuntime
from .client.session import Session
from .client.workspace import Workspace
from .exceptions import (
    AllegroFileNotFoundError,
    AllegroLaunchError,
    AllegroServerIdentityError,
    AllegroTimeoutError,
)

OpenMode = Literal['cli', 'manual']
_LOG = logging.getLogger(__name__)
_POLL_INTERVAL = 0.1
_INSTALL_ROOT_VARS = ('CDSROOT', 'Sigrity_EDA_DIR')


def _resolve_executable(executable: str | Path) -> str:
    path = Path(executable)
    if path.is_file():
        return str(path)
    search_dirs = [
        str(Path(root) / 'tools' / 'bin') for var in _INSTALL_ROOT_VARS if (root := getenv(var))
    ]
    found = which(
        str(executable),
        path=os.pathsep.join([getenv('PATH', ''), *search_dirs]),
    )
    if found is not None:
        return found
    raise AllegroFileNotFoundError(
        f"could not find the Allegro executable {str(executable)!r}: not on PATH and no "
        f"Cadence installation found via {', '.join(_INSTALL_ROOT_VARS)}; "
        "pass the full path with executable=..."
    )


def _default_workspace_id(*, force_tcp: bool) -> str:
    return '7777' if sys.platform == 'win32' or force_tcp else 'default'


def _build_startup_script(
    *, board: Path | None, workspace_id: str, force_tcp: bool, nonce: str
) -> str:
    python_server = Path(_kernel_server.__file__).with_name('python_server.ils').as_posix()
    allegro_runtime = Path(allegrobridge.server.__file__).with_name('allegro_server.il').as_posix()
    force_tcp_flag = ' ?forceTcp t' if force_tcp else ''
    lines = [
        f'skill load("{python_server}")',
        f'skill load("{allegro_runtime}")',
        'skill axlSetVariable("noconfirm" t)',
        f'skill __abLaunchToken = "{nonce}"',
    ]
    if board is not None:
        lines.extend([
            (
                'skill unless('
                f'axlOpenDesign(?design "{board.as_posix()}" ?mode "wf") '
                'error("ALLEGRO_BOARD_OPEN_FAILED"))'
            ),
            'skill unless(axlDBRefreshId(axlDBGetDesign()) error("ALLEGRO_DESIGN_REFRESH_FAILED"))',
        ])
    lines.append(
        'skill unless('
        f'pyStartServer(?id "{workspace_id}" ?singleMode t '
        f'?python "{Path(sys.executable).as_posix()}"{force_tcp_flag}) '
        'error("ALLEGRO_SERVER_START_FAILED"))'
    )
    return '\n'.join(lines) + '\n'


class Allegro:
    """An open Allegro window connected to a Workspace."""

    def __init__(
        self,
        *,
        mode: OpenMode,
        workspace_id: WorkspaceId,
        board: Path | None,
        workspace: Workspace,
        runtime: CliRuntime | None = None,
        force_tcp: bool = False,
    ) -> None:
        self.mode = mode
        self.workspace_id = workspace_id
        self.board = board
        self._workspace = workspace
        self._runtime = runtime
        self._force_tcp = force_tcp
        self._closed = False
        self._session = Session(self)

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
        return cls(mode='manual', workspace_id=ws_id, board=board_path, workspace=workspace)

    @classmethod
    def launch(
        cls,
        board: str | Path | None = None,
        *,
        workspace_id: WorkspaceId = None,
        executable: str | Path = 'allegro.exe',
        timeout: float = 120.0,
        force_tcp: bool = False,
    ) -> Allegro:
        ws_id = (
            _default_workspace_id(force_tcp=force_tcp)
            if workspace_id is None
            else str(workspace_id)
        )
        board_path = Path(board).resolve() if board is not None else None
        if board_path is not None and not board_path.is_file():
            raise AllegroFileNotFoundError(f'Allegro board file does not exist: {board_path}')
        token = uuid4().hex
        endpoint = int(ws_id) if sys.platform == 'win32' or force_tcp else None
        runtime = CliRuntime(endpoint=endpoint)
        try:
            runtime.start(
                [_resolve_executable(executable)],
                _build_startup_script(
                    board=board_path,
                    workspace_id=ws_id,
                    force_tcp=force_tcp,
                    nonce=token,
                ),
            )
            workspace = cls._wait_for_workspace(
                runtime,
                ws_id,
                force_tcp=force_tcp,
                timeout=timeout,
                nonce=token,
            )
        except BaseException as error:
            cls._cleanup_after_error(
                runtime,
                error,
                wait_for_endpoint=not isinstance(error, AllegroServerIdentityError),
            )
            raise
        return cls(
            mode='cli',
            workspace_id=ws_id,
            board=board_path,
            workspace=workspace,
            runtime=runtime,
            force_tcp=force_tcp,
        )

    @classmethod
    def open(
        cls,
        *,
        mode: OpenMode,
        workspace_id: WorkspaceId = None,
        board: str | Path | None = None,
        executable: str | Path = 'allegro.exe',
        timeout: float = 120.0,
        force_tcp: bool = False,
    ) -> Allegro:
        if mode == 'manual':
            return cls.connect(workspace_id=workspace_id, board=board, force_tcp=force_tcp)
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
        runtime: CliRuntime,
        workspace_id: WorkspaceId,
        *,
        force_tcp: bool,
        timeout: float,
        nonce: str,
    ) -> Workspace:
        deadline = monotonic() + timeout
        last_error: OSError | RuntimeError | None = None
        while monotonic() < deadline:
            return_code = runtime.poll()
            if return_code is not None:
                raise AllegroLaunchError(
                    f'Allegro exited before the server was ready (exit code {return_code})'
                )
            try:
                return cls._open_workspace(
                    workspace_id,
                    force_tcp=force_tcp,
                    nonce=nonce,
                )
            except AllegroServerIdentityError:
                raise
            except (OSError, RuntimeError) as error:
                last_error = error
                sleep(_POLL_INTERVAL)
        raise AllegroTimeoutError(
            f'Allegro server was not ready within {timeout:g} seconds'
        ) from last_error

    @staticmethod
    def _open_workspace(
        workspace_id: WorkspaceId,
        *,
        force_tcp: bool,
        nonce: str | None = None,
    ) -> Workspace:
        workspace = Workspace.open(workspace_id, force_tcp=force_tcp)
        if not isinstance(workspace, Workspace):
            workspace.close()
            raise AllegroLaunchError('Connected server is not running in Allegro')

        def verify_identity(actual: object) -> None:
            if actual != nonce:
                raise AllegroServerIdentityError(
                    'Connected Allegro server belongs to a different launch instance'
                )

        try:
            if nonce is not None:
                actual_token = workspace['evalstring']('__abLaunchToken')
                verify_identity(actual_token)
            ok = workspace['plus'](1, 2) == 3  # ruff: ignore[magic-value-comparison]
        except BaseException:
            workspace.close()
            raise
        if not ok:
            workspace.close()
            raise AllegroLaunchError('Allegro server readiness check failed')
        return workspace

    @staticmethod
    def _cleanup_after_error(
        runtime: CliRuntime,
        original: BaseException,
        *,
        wait_for_endpoint: bool,
    ) -> None:
        try:
            runtime.close(wait_for_endpoint=wait_for_endpoint)
        except Exception:  # ruff: ignore[blind-except]
            _LOG.error('Runtime cleanup failed while handling %r', original, exc_info=True)

    @property
    def workspace(self) -> Workspace:
        return self._workspace

    @property
    def session(self) -> Session:
        return self._session

    def close(self) -> None:
        if self._closed:
            return
        try:
            self._workspace.close()
        except BaseException as error:
            if self._runtime is not None:
                self._cleanup_after_error(self._runtime, error, wait_for_endpoint=True)
            raise
        if self._runtime is not None:
            self._runtime.close()
        self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_val is None:
            self.close()
            return
        try:
            self.close()
        except Exception:  # ruff: ignore[blind-except]
            _LOG.error('Allegro close failed while leaving an exceptional context', exc_info=True)
