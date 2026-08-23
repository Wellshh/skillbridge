from __future__ import annotations

import re
import sys
from inspect import signature
from pathlib import Path

from pytest import MonkeyPatch, fixture, raises

from allegrobridge import Allegro, allegro
from allegrobridge.allegro import _resolve_executable  # ruff: ignore[import-private-name]


class FakeProcess:
    def __init__(self) -> None:
        self.terminated = False

    def poll(self) -> None:
        return None

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.terminated = True

    def wait(self, timeout: float | None = None) -> int:
        del timeout
        return 0


class FakeWorkspace:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


class LaunchRecorder:
    def __init__(self) -> None:
        self.process = FakeProcess()
        self.workspace = FakeWorkspace()
        self.command: list[str] = []

    @property
    def script_path(self) -> Path:
        return Path(self.command[2])


@fixture
def launch_recorder(monkeypatch: MonkeyPatch) -> LaunchRecorder:
    recorder = LaunchRecorder()

    def fake_popen(command: list[str], *, shell: bool) -> FakeProcess:
        assert not shell
        recorder.command = command
        return recorder.process

    monkeypatch.setattr(allegro, 'Popen', fake_popen)
    return recorder


@fixture
def executable(tmp_path: Path) -> Path:
    exe = tmp_path / 'allegro.exe'
    exe.touch()
    exe.chmod(0o755)
    return exe


def stub_ready(monkeypatch: MonkeyPatch, workspace: FakeWorkspace) -> None:
    def ready(
        process: object,
        workspace_id: object,
        *,
        force_tcp: bool,
        timeout: float,
    ) -> FakeWorkspace:
        del process, workspace_id, force_tcp, timeout
        return workspace

    monkeypatch.setattr(Allegro, '_wait_for_workspace', ready)


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
    launch_recorder: LaunchRecorder,
    executable: Path,
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    board = tmp_path / 'shape1.brd'
    board.touch()
    stub_ready(monkeypatch, launch_recorder.workspace)

    opened = Allegro.launch(board=board, executable=executable)

    command = launch_recorder.command
    assert command[:2] == [str(executable), '-s']
    assert command[3] == board.resolve().as_posix()

    script = launch_recorder.script_path.read_text(encoding='utf-8')
    assert 'pyStartServer' in script
    assert Path(sys.executable).as_posix() in script
    assert '\\' not in script

    opened.close()
    assert launch_recorder.workspace.closed
    assert launch_recorder.process.terminated
    assert not launch_recorder.script_path.exists()


def test_launch_cleans_up_when_workspace_never_connects(
    launch_recorder: LaunchRecorder,
    executable: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    def never_ready(
        process: object,
        workspace_id: object,
        *,
        force_tcp: bool,
        timeout: float,
    ) -> None:
        raise TimeoutError

    monkeypatch.setattr(Allegro, '_wait_for_workspace', never_ready)

    with raises(TimeoutError):
        Allegro.launch(executable=executable)

    assert launch_recorder.process.terminated
    assert not launch_recorder.script_path.exists()


def test_default_launch_timeout_covers_cold_start() -> None:
    for method in (Allegro.launch, Allegro.open):
        assert signature(method).parameters['timeout'].default >= 120
