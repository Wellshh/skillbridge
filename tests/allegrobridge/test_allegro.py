from __future__ import annotations

import re
import sys
from dataclasses import FrozenInstanceError
from inspect import signature
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock, Mock

import pytest
from pydantic import TypeAdapter

import allegrobridge.server
import skillbridge.server
from allegrobridge import Allegro
from allegrobridge.allegro import (
    _build_startup_script,  # ruff: ignore[import-private-name]
    _resolve_executable,  # ruff: ignore[import-private-name]
)
from allegrobridge.client.api import (
    Batch,
    Command,
    CommandResult,
    ComponentsApi,
    RpcArgs,
    SessionApi,
    extension,
    read,
)
from allegrobridge.client.api._rpc import _core_procedures  # ruff: ignore[import-private-name]
from allegrobridge.client.session import Session
from allegrobridge.client.workspace import Workspace
from allegrobridge.exceptions import (
    AllegroError,
    AllegroFileNotFoundError,
    AllegroLaunchError,
    AllegroProtocolError,
    AllegroServerIdentityError,
    AllegroTimeoutError,
    ExtensionError,
)
from skillbridge.exception import ProtocolError, SkillBridgeError


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
    design_refresh = next(line for line in lines if 'axlDBRefreshId' in line)
    server_start = next(line for line in lines if 'pyStartServer' in line)
    assert (
        lines.index(nonce)
        < lines.index(board_open)
        < lines.index(design_refresh)
        < lines.index(server_start)
    )
    assert 'ALLEGRO_BOARD_OPEN_FAILED' in board_open
    assert 'ALLEGRO_DESIGN_REFRESH_FAILED' in design_refresh
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
    with pytest.raises(AllegroServerIdentityError, match='different launch instance'):
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
        Mock(side_effect=AllegroServerIdentityError('different launch instance')),
    )
    with pytest.raises(AllegroServerIdentityError):
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


class TestSessionExtensions:
    @staticmethod
    def _module(name: str = 'constraints') -> tuple[ModuleType, type[SessionApi]]:
        module = ModuleType(f'allegrobridge.client.api.extensions.{name}')
        api = extension(type('ConstraintsApi', (SessionApi,), {'__module__': module.__name__}))
        module.ConstraintsApi = api
        return module, api

    def test_imports_on_first_access_and_caches_per_session(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        module, api = self._module()
        importer = Mock(return_value=module)
        monkeypatch.setattr('allegrobridge.client.api._extensions.import_module', importer)
        session = Session(Mock(workspace=MagicMock()))
        ext = session.ext
        importer.assert_not_called()

        plugin = ext.constraints

        assert isinstance(plugin, api)
        assert ext['constraints'] is plugin
        assert session.extensions.constraints is plugin
        importer.assert_called_once_with('allegrobridge.client.api.extensions.constraints')

    def test_unknown_extension_uses_python_lookup_errors(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        module_name = 'allegrobridge.client.api.extensions.missing'
        error = ModuleNotFoundError(name=module_name)
        monkeypatch.setattr(
            'allegrobridge.client.api._extensions.import_module',
            Mock(side_effect=error),
        )
        ext = Session(Mock(workspace=MagicMock())).ext

        with pytest.raises(AttributeError, match='missing'):
            _ = ext.missing
        with pytest.raises(KeyError, match='missing'):
            _ = ext['missing']
        with pytest.raises(KeyError, match='not-valid'):
            _ = ext['not-valid']
        with pytest.raises(KeyError, match='Constraints'):
            _ = ext['Constraints']

    @pytest.mark.parametrize('failure', ['declaration', 'dependency', 'import'])
    def test_extension_load_failure_is_isolated(
        self,
        monkeypatch: pytest.MonkeyPatch,
        failure: str,
    ) -> None:
        module = ModuleType('allegrobridge.client.api.extensions.broken')
        side_effect = {
            'declaration': module,
            'dependency': ModuleNotFoundError(name='dependency'),
            'import': ValueError('import failed'),
        }[failure]
        monkeypatch.setattr(
            'allegrobridge.client.api._extensions.import_module',
            Mock(side_effect=side_effect)
            if isinstance(side_effect, BaseException)
            else Mock(return_value=side_effect),
        )
        session = Session(Mock(workspace=MagicMock()))

        with pytest.raises(ExtensionError, match='broken'):
            _ = session.ext.broken
        assert session.board is session.board


class TestReadApi:
    def test_core_procedures_are_collected_from_api_declarations(self) -> None:
        assert _core_procedures() == (
            '__abProjectBoard',
            '__abProjectComponents',
            '__abMoveComponent',
            '__abProjectNets',
        )

    def test_declaration_preserves_signature_and_sends_once(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = 3
        session = Session(Mock(workspace=workspace))

        class ProbeApi(SessionApi):
            @read('__abProbe', TypeAdapter(int))
            def read(self, left: int, right: int = 0) -> RpcArgs:
                return left, right

        api = ProbeApi(session)

        assert str(signature(api.read)) == "(left: 'int', right: 'int' = 0) -> 'RpcArgs'"
        assert api.read(1, right=2) == 3
        workspace.__getitem__.assert_called_once_with('__abProbe')
        workspace.__getitem__.return_value.assert_called_once_with(1, 2)

    def test_read_api_injects_generation_into_records(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = {
            'path': 'shape1.brd',
            'units': 'mils',
            'component_count': 1,
            'symbol_count': 1,
            'net_count': 1,
        }
        session = Session(Mock(workspace=workspace))

        board = session.board()

        assert board.path == 'shape1.brd'
        assert board.session_generation == session.generation

    def test_read_api_maps_none_to_empty_and_wraps_validation_errors(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.side_effect = [
            None,
            [
                {
                    'refdes': 'R1',
                    'device_type': 'RESISTOR',
                    'package': 'RES_0402',
                    'component_class': 'DISCRETE',
                    'placement': 'placed',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                }
            ],
            [42],
        ]
        session = Session(Mock(workspace=workspace))

        assert session.components() == []
        assert session.components()[0].session_generation == session.generation
        with pytest.raises(AllegroProtocolError, match='__abProjectNets'):
            session.nets()


class TestWriteApi:
    @staticmethod
    def _component_payload(x: float) -> dict[str, object]:
        return {
            'refdes': 'R1',
            'device_type': 'RESISTOR',
            'package': 'RES_0402',
            'component_class': 'DISCRETE',
            'placement': 'placed',
            'x': x,
            'y': 2.0,
            'rotation': 0.0,
        }

    def test_command_is_inert_and_immediate_call_is_atomic(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.lazy.return_value = '__abMoveComponent("R1" 1.0 2.0 nil )'
        workspace.transaction.return_value = self._component_payload(1.0)
        session = Session(Mock(workspace=workspace))

        command = session.components.move.command('R1', x=1.0, y=2.0)

        assert ComponentsApi.move.procedure == '__abMoveComponent'
        assert list(signature(session.components.move).parameters) == [
            'refdes',
            'x',
            'y',
            'rotation',
        ]
        assert isinstance(command, Command)
        assert command.procedure == '__abMoveComponent'
        assert command.expression == '__abMoveComponent("R1" 1.0 2.0 nil )'
        workspace.transaction.assert_not_called()
        with pytest.raises(FrozenInstanceError):
            command.procedure = '__changed'

        moved = session.components.move('R1', x=1.0, y=2.0)

        assert moved.x == pytest.approx(1.0)
        assert moved.session_generation == session.generation
        workspace.transaction.assert_called_once_with(command.expression)

    def test_preview_uses_dry_transaction(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.lazy.return_value = '__abMoveComponent("R1" 3.0 2.0 nil )'
        workspace.transaction.preview.return_value = self._component_payload(3.0)
        session = Session(Mock(workspace=workspace))

        preview = session.components.move.preview('R1', x=3.0, y=2.0)

        assert preview.x == pytest.approx(3.0)
        workspace.transaction.assert_not_called()
        workspace.transaction.preview.assert_called_once_with(
            '__abMoveComponent("R1" 3.0 2.0 nil )'
        )


class TestBatch:
    @staticmethod
    def _payload(refdes: str, x: float) -> dict[str, object]:
        return {
            'refdes': refdes,
            'device_type': 'RESISTOR',
            'package': 'RES_0402',
            'component_class': 'DISCRETE',
            'placement': 'placed',
            'x': x,
            'y': 2.0,
            'rotation': 0.0,
        }

    def test_resolves_ordered_results_with_one_rpc(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.lazy.side_effect = ['move1()', 'move2()']
        workspace.transaction.return_value = [self._payload('R1', 1.0), self._payload('R2', 2.0)]
        session = Session(Mock(workspace=workspace))

        with session.batch('move two') as batch:
            assert isinstance(batch, Batch)
            first = batch.add(session.components.move.command('R1', x=1.0, y=2.0))
            second = batch.add(session.components.move.command('R2', x=2.0, y=2.0))
            with pytest.raises(RuntimeError, match='pending'):
                _ = first.value

        assert isinstance(first, CommandResult)
        assert first.value.refdes == 'R1'
        assert second.value.refdes == 'R2'
        composite = workspace.transaction.call_args.args[0]
        assert 'progn' in composite
        assert composite.index('move1()') < composite.index('move2()')
        assert 'reverse(results)' in composite
        workspace.transaction.assert_called_once()

    def test_dry_run_uses_preview_and_empty_batch_sends_nothing(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.lazy.return_value = 'move1()'
        workspace.transaction.preview.return_value = [self._payload('R1', 1.0)]
        session = Session(Mock(workspace=workspace))

        with session.batch(dry_run=True) as batch:
            result = batch.add(session.components.move.command('R1', x=1.0, y=2.0))

        assert result.value.refdes == 'R1'
        workspace.transaction.assert_not_called()
        workspace.transaction.preview.assert_called_once()

        workspace.reset_mock()
        with session.batch():
            pass
        workspace.transaction.assert_not_called()
        workspace.transaction.preview.assert_not_called()

    def test_rejects_cross_session_command(self) -> None:
        session = Session(Mock(workspace=MagicMock()))
        other = Session(Mock(workspace=MagicMock()))
        command = other.components.move.command('R1', x=1.0, y=2.0)

        with session.batch() as batch, pytest.raises(ValueError, match='Session'):
            batch.add(command)

    def test_context_error_cancels_results_without_sending(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.lazy.return_value = 'move1()'
        session = Session(Mock(workspace=workspace))
        error = ValueError('body')
        results: list[CommandResult[object]] = []

        def cancel() -> None:
            with session.batch() as batch:
                results.append(batch.add(session.components.move.command('R1', x=1.0, y=2.0)))
                raise error

        with pytest.raises(ValueError, match='body'):
            cancel()

        with pytest.raises(ValueError) as raised:
            _ = results[0].value
        assert raised.value is error
        workspace.transaction.assert_not_called()

    @pytest.mark.parametrize('payload', [None, [], [None, None]])
    def test_protocol_failure_fails_every_result(self, payload: object) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.lazy.return_value = 'move1()'
        workspace.transaction.return_value = payload
        session = Session(Mock(workspace=workspace))
        results: list[CommandResult[object]] = []

        def execute() -> None:
            with session.batch() as batch:
                results.append(batch.add(session.components.move.command('R1', x=1.0, y=2.0)))

        with pytest.raises(AllegroProtocolError, match='batch'):
            execute()

        with pytest.raises(AllegroProtocolError, match='batch'):
            _ = results[0].value

    def test_validation_finishes_before_any_result_is_resolved(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.lazy.side_effect = ['move1()', 'move2()']
        workspace.transaction.return_value = [self._payload('R1', 1.0), None]
        session = Session(Mock(workspace=workspace))
        results: list[CommandResult[object]] = []

        def execute() -> None:
            with session.batch() as batch:
                results.extend([
                    batch.add(session.components.move.command('R1', x=1.0, y=2.0)),
                    batch.add(session.components.move.command('R2', x=2.0, y=2.0)),
                ])

        with pytest.raises(AllegroProtocolError, match='__abMoveComponent'):
            execute()
        for result in results:
            with pytest.raises(AllegroProtocolError, match='__abMoveComponent'):
                _ = result.value

    def test_batch_is_single_use_and_add_requires_active_context(self) -> None:
        session = Session(Mock(workspace=MagicMock()))
        batch = session.batch()

        with pytest.raises(RuntimeError, match='active'):
            batch.add(Mock(spec=Command))
        with batch:
            pass
        with pytest.raises(RuntimeError, match='active'):
            batch.add(Mock(spec=Command))
        with pytest.raises(RuntimeError, match='already used'), batch:
            pass


def test_allegro_errors_share_skillbridge_root() -> None:
    assert issubclass(AllegroError, SkillBridgeError)
    assert issubclass(AllegroProtocolError, ProtocolError)
    assert issubclass(AllegroProtocolError, AllegroError)
    assert issubclass(AllegroFileNotFoundError, FileNotFoundError)
    assert issubclass(AllegroLaunchError, AllegroError)
    assert issubclass(AllegroTimeoutError, AllegroLaunchError)
    assert issubclass(ExtensionError, AllegroError)
