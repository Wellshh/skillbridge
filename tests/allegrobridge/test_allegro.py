from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

import allegrobridge.server
import skillbridge.server
from allegrobridge import Allegro
from allegrobridge.allegro import (
    _build_startup_script,  # ruff: ignore[import-private-name]
    _resolve_executable,  # ruff: ignore[import-private-name]
    _ServerIdentityError,  # ruff: ignore[import-private-name]
)
from allegrobridge.client.session import Session
from allegrobridge.client.workspace import Workspace


@pytest.fixture
def executable(tmp_path: Path) -> Path:
    exe = tmp_path / 'allegro.exe'
    exe.touch()
    exe.chmod(0o755)
    return exe


def test_resolve_executable_returns_explicit_path(executable: Path) -> None:
    assert _resolve_executable(executable) == str(executable)


def test_resolve_executable_searches_path(
    executable: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('PATH', str(executable.parent))
    assert _resolve_executable(executable.name) == str(executable)


def test_resolve_executable_searches_cadence_install_roots(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    install_root = tmp_path / 'Cadence_SPB'
    exe = install_root / 'tools' / 'bin' / 'allegro.exe'
    exe.parent.mkdir(parents=True)
    exe.touch()
    exe.chmod(0o755)
    monkeypatch.setenv('PATH', str(tmp_path / 'missing'))
    monkeypatch.delenv('CDSROOT', raising=False)
    monkeypatch.setenv('Sigrity_EDA_DIR', str(install_root))
    assert _resolve_executable('allegro.exe') == str(exe)


def test_resolve_executable_raises_with_guidance(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv('PATH', str(tmp_path))
    monkeypatch.delenv('CDSROOT', raising=False)
    monkeypatch.delenv('Sigrity_EDA_DIR', raising=False)
    with pytest.raises(FileNotFoundError, match=re.escape('allegro.exe')):
        _resolve_executable('allegro.exe')


def test_startup_script_orders_nonce_board_and_guarded_server(tmp_path: Path) -> None:
    board = tmp_path / 'shape1.brd'
    script = _build_startup_script(
        board=board,
        workspace_id='7788',
        force_tcp=True,
        nonce='launch-instance',
    )
    lines = script.splitlines()
    core = Path(skillbridge.server.__file__).with_name('python_server.il')
    extension = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
    assert lines[:2] == [
        f'skill load("{core.as_posix()}")',
        f'skill load("{extension.as_posix()}")',
    ]
    nonce = 'skill __abLaunchToken = "launch-instance"'
    board_open = next(line for line in lines if 'axlOpenDesign' in line)
    server_start = next(line for line in lines if 'pyStartServer' in line)
    assert lines.index(nonce) < lines.index(board_open) < lines.index(server_start)
    assert 'ALLEGRO_BOARD_OPEN_FAILED' in board_open
    assert server_start.startswith('skill unless(')
    assert 'ALLEGRO_SERVER_START_FAILED' in server_start
    assert '?forceTcp t' in server_start
    assert Path(sys.executable).as_posix() in server_start
    assert '\\' not in script


def test_launch_rejects_missing_board_before_runtime(
    executable: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runtime = Mock()
    monkeypatch.setattr('allegrobridge.allegro.CliRuntime', runtime)
    missing = tmp_path / 'missing.brd'
    with pytest.raises(FileNotFoundError, match=re.escape(str(missing))):
        Allegro.launch(board=missing, executable=executable)
    runtime.assert_not_called()


def test_launch_cleans_up_timeout_without_masking_it(
    executable: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = Mock()
    runtime.close.side_effect = RuntimeError('cleanup failed')
    monkeypatch.setattr('allegrobridge.allegro.CliRuntime', Mock(return_value=runtime))
    monkeypatch.setattr(Allegro, '_wait_for_workspace', Mock(side_effect=TimeoutError('ready')))
    with pytest.raises(TimeoutError, match='ready'):
        Allegro.launch(executable=executable)
    runtime.close.assert_called_once_with(wait_for_endpoint=True)


def test_launch_cleans_up_keyboard_interrupt(
    executable: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = Mock()
    monkeypatch.setattr('allegrobridge.allegro.CliRuntime', Mock(return_value=runtime))
    monkeypatch.setattr(Allegro, '_wait_for_workspace', Mock(side_effect=KeyboardInterrupt))
    with pytest.raises(KeyboardInterrupt):
        Allegro.launch(executable=executable)
    runtime.close.assert_called_once_with(wait_for_endpoint=True)


def test_identity_mismatch_closes_unknown_workspace_and_fails_immediately(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = MagicMock(spec=Workspace)
    workspace.__getitem__.side_effect = lambda name: Mock(
        return_value='old-token' if name == 'evalstring' else 3
    )
    monkeypatch.setattr('allegrobridge.allegro.Workspace.open', Mock(return_value=workspace))
    with pytest.raises(_ServerIdentityError, match='different launch instance'):
        Allegro._open_workspace('7788', force_tcp=True, nonce='new-instance')
    workspace.close.assert_called_once_with()


def test_identity_mismatch_does_not_wait_for_unknown_endpoint(
    executable: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = Mock()
    monkeypatch.setattr('allegrobridge.allegro.CliRuntime', Mock(return_value=runtime))
    monkeypatch.setattr(
        Allegro,
        '_wait_for_workspace',
        Mock(side_effect=_ServerIdentityError('different launch instance')),
    )
    with pytest.raises(_ServerIdentityError):
        Allegro.launch(executable=executable)
    runtime.close.assert_called_once_with(wait_for_endpoint=False)


def test_close_can_retry_after_runtime_failure() -> None:
    workspace = Mock()
    runtime = Mock()
    runtime.close.side_effect = [RuntimeError('busy'), None]
    opened = Allegro(
        mode='cli',
        workspace_id='7788',
        board=None,
        workspace=workspace,
        runtime=runtime,
    )
    with pytest.raises(RuntimeError, match='busy'):
        opened.close()
    opened.close()
    opened.close()
    assert runtime.close.call_count == 2


def test_context_body_error_is_not_replaced_by_close_error() -> None:
    workspace = Mock()
    workspace.close.side_effect = RuntimeError('close')
    opened = Allegro(
        mode='manual',
        workspace_id='manual',
        board=None,
        workspace=workspace,
    )
    with pytest.raises(ValueError, match='body'), opened:
        raise ValueError('body')


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
        session = Session(Mock(workspace=workspace))
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
