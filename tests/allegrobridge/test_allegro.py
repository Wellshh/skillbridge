from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from subprocess import PIPE, Popen
from time import monotonic, sleep
from unittest.mock import Mock

from pytest import MonkeyPatch, fixture, raises, skip

import allegrobridge.server
import skillbridge.server
from allegrobridge import Allegro, allegro
from allegrobridge.allegro import (
    _kill_process_tree,  # ruff: ignore[import-private-name]
    _resolve_executable,  # ruff: ignore[import-private-name]
)
from allegrobridge.client.session import Session

_PYTHON = getattr(sys, '_base_executable', None) or sys.executable


@fixture
def executable(tmp_path: Path) -> Path:
    exe = tmp_path / 'allegro.exe'
    exe.touch()
    exe.chmod(0o755)
    return exe


def test_resolve_executable_returns_explicit_path(executable: Path) -> None:
    assert _resolve_executable(executable) == str(executable)


def test_resolve_executable_searches_path(
    executable: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv('PATH', str(executable.parent))

    assert _resolve_executable(executable.name) == str(executable)


def test_resolve_executable_searches_cadence_install_roots(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    install_root = tmp_path / 'Cadence_SPB'
    exe = install_root / 'tools' / 'bin' / 'allegro.exe'
    exe.parent.mkdir(parents=True)
    exe.touch()
    exe.chmod(0o755)
    monkeypatch.setenv('PATH', str(tmp_path / 'no-allegro-here'))
    monkeypatch.delenv('CDSROOT', raising=False)
    monkeypatch.setenv('Sigrity_EDA_DIR', str(install_root))

    assert _resolve_executable('allegro.exe') == str(exe)


def test_resolve_executable_raises_with_guidance(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv('PATH', str(tmp_path))
    monkeypatch.delenv('CDSROOT', raising=False)
    monkeypatch.delenv('Sigrity_EDA_DIR', raising=False)

    with raises(FileNotFoundError, match=re.escape('allegro.exe')):
        _resolve_executable('allegro.exe')


def test_launch_writes_startup_script_that_loads_servers_and_opens_board(
    executable: Path,
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    board = tmp_path / 'shape1.brd'
    board.touch()

    command: list[str] = []
    process = Mock(poll=Mock(return_value=None), terminate=Mock())
    workspace = Mock(close=Mock())

    def fake_popen(cmd: list[str], *, shell: bool) -> Mock:
        assert not shell
        command.extend(cmd)
        return process

    monkeypatch.setattr(allegro, 'Popen', fake_popen)
    monkeypatch.setattr(allegro, '_wait_for_tcp_port_release', Mock(), raising=False)
    monkeypatch.setattr(Allegro, '_wait_for_workspace', lambda *_, **__: workspace)

    opened = Allegro.launch(board=board, executable=executable)

    command_list = command
    assert command_list[:2] == [str(executable), '-s']
    assert len(command_list) == 3

    script_path = Path(command_list[2])
    script = script_path.read_text(encoding='utf-8')
    assert 'pyStartServer' in script
    core_server = Path(skillbridge.server.__file__).with_name('python_server.il')
    transaction_server = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
    assert script.splitlines()[:2] == [
        f'skill load("{core_server.as_posix()}")',
        f'skill load("{transaction_server.as_posix()}")',
    ]
    assert 'axlSetVariable("noconfirm" t)' in script
    lines = script.splitlines()
    open_board_line = (
        'skill unless('
        f'axlOpenDesign(?design "{board.resolve().as_posix()}" ?mode "wf") '
        'error("ALLEGRO_BOARD_OPEN_FAILED"))'
    )
    start_server_line = next(line for line in lines if 'pyStartServer' in line)
    assert lines.index(open_board_line) < lines.index(start_server_line)
    assert Path(sys.executable).as_posix() in script
    assert '\\' not in script

    opened.close()
    workspace.close.assert_called_once()
    process.terminate.assert_called_once()
    assert not script_path.exists()


def test_launch_rejects_missing_board_before_starting_process(
    executable: Path,
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    popen = Mock()
    monkeypatch.setattr(allegro, 'Popen', popen)
    missing_board = tmp_path / 'missing.brd'

    with raises(FileNotFoundError, match=re.escape(str(missing_board))):
        Allegro.launch(board=missing_board, executable=executable)

    popen.assert_not_called()


def test_launch_cleans_up_when_workspace_never_connects(
    executable: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    command: list[str] = []
    process = Mock(poll=Mock(return_value=None), terminate=Mock())

    def fake_popen(cmd: list[str], *, shell: bool) -> Mock:
        assert not shell
        command.extend(cmd)
        return process

    monkeypatch.setattr(allegro, 'Popen', fake_popen)
    monkeypatch.setattr(Allegro, '_wait_for_workspace', Mock(side_effect=TimeoutError))

    with raises(TimeoutError):
        Allegro.launch(executable=executable)

    process.terminate.assert_called_once()
    assert not Path(command[2]).exists()


def test_close_waits_for_tcp_relay_after_killing_allegro(
    monkeypatch: MonkeyPatch,
) -> None:
    events: list[str] = []
    workspace = Mock(close=lambda: events.append('workspace'))
    process = Mock()
    monkeypatch.setattr(allegro, '_kill_process_tree', lambda _: events.append('allegro'))
    monkeypatch.setattr(
        allegro,
        '_wait_for_tcp_port_release',
        lambda port: events.append(f'port:{port}'),
        raising=False,
    )
    opened = Allegro(
        mode='cli',
        workspace_id='7788',
        board=None,
        workspace=workspace,
        process=process,
        force_tcp=True,
    )

    opened.close()

    assert events == ['workspace', 'allegro', 'port:7788']


class _ProbeSocket:
    def __init__(self, results: list[int]) -> None:
        self._results = results

    def __enter__(self) -> _ProbeSocket:  # ruff: ignore[non-self-return-type]
        return self

    def __exit__(self, *_: object) -> None:
        pass

    def settimeout(self, _: float) -> None:
        pass

    def connect_ex(self, _: tuple[str, int]) -> int:
        return self._results.pop(0)


def test_wait_for_tcp_port_release_retries_until_listener_stops(
    monkeypatch: MonkeyPatch,
) -> None:
    results = [0, 1]
    sleeps: list[float] = []
    monkeypatch.setattr(allegro, 'socket', lambda *_: _ProbeSocket(results))
    monkeypatch.setattr(allegro, 'sleep', sleeps.append)

    allegro._wait_for_tcp_port_release(7788)

    assert results == []
    assert sleeps == [allegro._POLL_INTERVAL]


def test_wait_for_tcp_port_release_times_out(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(allegro, 'socket', lambda *_: _ProbeSocket([0]))
    monkeypatch.setattr(allegro, 'monotonic', Mock(side_effect=[0.0, 6.0]))

    with raises(TimeoutError, match='7788'):
        allegro._wait_for_tcp_port_release(7788)


def _is_process_alive(pid: int) -> bool:
    result = subprocess.run(
        ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return str(pid) in result.stdout


def _terminate_pid(pid: int) -> None:
    subprocess.run(['taskkill', '/F', '/PID', str(pid)], timeout=10, check=False)


def test_kill_process_tree_terminates_descendants() -> None:
    if sys.platform != 'win32':
        skip('process-tree cleanup is Windows-specific')

    parent_script = (
        'import subprocess, time\n'
        'child = subprocess.Popen('
        f'[{_PYTHON!r}, "-c", "import time; time.sleep(60)"],'
        ' stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,'
        ' stderr=subprocess.DEVNULL)\n'
        'print(child.pid, flush=True)\n'
        'time.sleep(60)\n'
    )
    parent = Popen([_PYTHON, '-c', parent_script], stdout=PIPE)
    child_pid = -1
    try:
        child_pid = int(parent.stdout.readline())  # type: ignore[union-attr]
        assert _is_process_alive(child_pid)

        _kill_process_tree(parent)

        assert parent.wait(timeout=5) is not None
        deadline = monotonic() + 5
        while _is_process_alive(child_pid) and monotonic() < deadline:
            sleep(0.3)
        assert not _is_process_alive(child_pid)
    finally:
        if parent.poll() is None:
            parent.kill()
            parent.wait(timeout=5)
        if child_pid != -1 and _is_process_alive(child_pid):
            _terminate_pid(child_pid)


class TestSession:
    def test_allegro_owns_session(self) -> None:
        workspace = Mock()
        opened = Allegro(
            mode='manual',
            workspace_id='test',
            board=None,
            workspace=workspace,
        )

        assert isinstance(opened.session, Session)
        assert opened.session is opened.session
        assert opened.session.raw is workspace

    def test_exposes_workspace_and_connection_generation(self) -> None:
        workspace = Mock()
        opened = Mock(workspace=workspace)

        session = Session(opened)

        assert session.raw is workspace
        assert session.generation == 1

    def test_close_is_idempotent(self) -> None:
        opened = Mock()
        session = Session(opened)

        session.close()
        session.close()

        opened.close.assert_called_once_with()

    def test_context_manager_closes(self) -> None:
        opened = Mock()
        session = Session(opened)

        with session as entered:
            assert entered is session

        opened.close.assert_called_once_with()


def test_kill_process_tree_terminates_orphaned_descendants_when_parent_dead() -> None:
    if sys.platform != 'win32':
        skip('process-tree cleanup is Windows-specific')

    parent_script = (
        'import subprocess\n'
        'child = subprocess.Popen('
        f'[{_PYTHON!r}, "-c", "import time; time.sleep(60)"],'
        ' stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,'
        ' stderr=subprocess.DEVNULL)\n'
        'print(child.pid, flush=True)\n'
    )
    parent = Popen([_PYTHON, '-c', parent_script], stdout=PIPE)
    child_pid = -1
    try:
        child_pid = int(parent.stdout.readline())  # type: ignore[union-attr]
        parent.wait(timeout=5)
        assert parent.poll() is not None
        assert _is_process_alive(child_pid)

        _kill_process_tree(parent)

        deadline = monotonic() + 5
        while _is_process_alive(child_pid) and monotonic() < deadline:
            sleep(0.3)
        assert not _is_process_alive(child_pid)
    finally:
        if child_pid != -1 and _is_process_alive(child_pid):
            _terminate_pid(child_pid)
