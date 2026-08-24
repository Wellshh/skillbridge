from __future__ import annotations

import os
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

import allegrobridge.server
import skillbridge.server
from skillbridge.client.workspace import WorkspaceId

from .client.workspace import Workspace

OpenMode = Literal['cli', 'manual']

_POLL_INTERVAL = 0.1
_PROCESS_EXIT_TIMEOUT = 5.0

if sys.platform == 'win32':  # pragma: no cover - exercised on Windows dev/CI hosts
    import ctypes
    from ctypes import wintypes

    _PROCESS_TERMINATE = 0x0001
    _TH32CS_SNAPPROCESS = 0x00000002

    class _ProcessEntry32W(ctypes.Structure):
        _fields_ = [
            ('dwSize', wintypes.DWORD),
            ('cntUsage', wintypes.DWORD),
            ('th32ProcessID', wintypes.DWORD),
            ('th32DefaultHeapID', ctypes.c_void_p),
            ('th32ModuleID', wintypes.DWORD),
            ('cntThreads', wintypes.DWORD),
            ('th32ParentProcessID', wintypes.DWORD),
            ('pcPriClassBase', ctypes.c_long),
            ('dwFlags', wintypes.DWORD),
            ('szExeFile', wintypes.WCHAR * 260),
        ]

    _kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.Process32FirstW.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_ProcessEntry32W),
    ]
    _kernel32.Process32NextW.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_ProcessEntry32W),
    ]

    def _descendant_pids(root_pid: int) -> list[int]:
        snapshot = _kernel32.CreateToolhelp32Snapshot(_TH32CS_SNAPPROCESS, 0)
        if not snapshot:
            return []
        children: dict[int, list[int]] = {}
        entry = _ProcessEntry32W()
        entry.dwSize = ctypes.sizeof(_ProcessEntry32W)
        try:
            if not _kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
                return []
            while True:
                children.setdefault(entry.th32ParentProcessID, []).append(entry.th32ProcessID)
                if not _kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                    break
        finally:
            _kernel32.CloseHandle(snapshot)
        found: list[int] = []
        pending = list(children.get(root_pid, []))
        while pending:
            pid = pending.pop()
            found.append(pid)
            pending.extend(children.get(pid, []))
        return found

    def _terminate_pid(pid: int) -> None:
        handle = _kernel32.OpenProcess(_PROCESS_TERMINATE, False, pid)  # ruff: ignore[boolean-positional-value-in-call]
        if handle:
            _kernel32.TerminateProcess(handle, 1)
            _kernel32.CloseHandle(handle)


def _kill_process_tree(process: Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    pid = process.pid
    if sys.platform == 'win32' and isinstance(pid, int):
        for child_pid in _descendant_pids(pid):
            with suppress(OSError):
                _terminate_pid(child_pid)
    with suppress(OSError):
        process.terminate()
    try:
        process.wait(timeout=_PROCESS_EXIT_TIMEOUT)
    except TimeoutExpired:
        with suppress(OSError):
            process.kill()
        process.wait(timeout=_PROCESS_EXIT_TIMEOUT)


_INSTALL_ROOT_VARS = ('CDSROOT', 'Sigrity_EDA_DIR')


def _resolve_executable(executable: str | Path) -> str:
    path = Path(executable)
    if path.is_file():
        return str(path)

    search_dirs = [
        str(Path(root) / 'tools' / 'bin') for var in _INSTALL_ROOT_VARS if (root := getenv(var))
    ]
    search_path = os.pathsep.join([getenv('PATH', ''), *search_dirs])

    found = which(str(executable), path=search_path)
    if found is not None:
        return found

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
        transaction_file = (
            Path(allegrobridge.server.__file__).with_name('allegro_server.il').as_posix()
        )
        force_tcp_flag = ' ?forceTcp t' if force_tcp else ''
        script_content = (
            f'skill load("{server_file}")\n'
            f'skill load("{transaction_file}")\n'
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
            _kill_process_tree(process)
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

    @property
    def workspace(self) -> Workspace:
        return self._workspace

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True

        self._workspace.close()
        if self._process is not None:
            _kill_process_tree(self._process)
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
