from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest.mock import Mock

from pytest import MonkeyPatch, fixture, raises

import allegrobridge.server
import skillbridge.server
from allegrobridge import Allegro, allegro
from allegrobridge.allegro import _resolve_executable  # ruff: ignore[import-private-name]


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


def test_launch_writes_posix_startup_script_and_passes_board(
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
    monkeypatch.setattr(Allegro, '_wait_for_workspace', lambda *_, **__: workspace)

    opened = Allegro.launch(board=board, executable=executable)

    command_list = command
    assert command_list[:2] == [str(executable), '-s']
    assert command_list[3] == board.resolve().as_posix()

    script_path = Path(command_list[2])
    script = script_path.read_text(encoding='utf-8')
    assert 'pyStartServer' in script
    core_server = Path(skillbridge.server.__file__).with_name('python_server.il')
    transaction_server = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
    assert script.splitlines()[:2] == [
        f'skill load("{core_server.as_posix()}")',
        f'skill load("{transaction_server.as_posix()}")',
    ]
    assert Path(sys.executable).as_posix() in script
    assert '\\' not in script

    opened.close()
    workspace.close.assert_called_once()
    process.terminate.assert_called_once()
    assert not script_path.exists()


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
