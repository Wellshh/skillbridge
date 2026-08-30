# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import re
import sys
from collections.abc import Sequence
from dataclasses import FrozenInstanceError
from inspect import signature
from pathlib import Path
from typing import Annotated, TypeVar
from unittest.mock import MagicMock, Mock
from weakref import ref

import pytest
from pydantic import Field, TypeAdapter, ValidationError

import allegrobridge._kernel.server
import allegrobridge.client.api as api_module
import allegrobridge.server
from allegrobridge import Allegro
from allegrobridge._kernel import SkillCode
from allegrobridge._kernel.client.expr import Expr
from allegrobridge._kernel.exception import ProtocolError, SkillBridgeError
from allegrobridge.allegro import (
    _build_startup_script,
    _resolve_executable,
)
from allegrobridge.client.api import (
    Batch,
    BBox,
    BoardApi,
    BoardInfo,
    Cmd,
    CmdResult,
    ComponentInfo,
    ComponentRef,
    ComponentsApi,
    DrcApi,
    DrcInfo,
    LayerInfo,
    LayersApi,
    NetInfo,
    NetRef,
    NetsApi,
    PadstackInfo,
    PadstacksApi,
    PinInfo,
    PinRef,
    PinsApi,
    Point,
    RouteInfo,
    RoutesApi,
    RpcArgs,
    RpcDef,
    SessionApi,
    ShapeInfo,
    ShapesApi,
    SymbolInfo,
    SymbolsApi,
    ViaInfo,
    ViasApi,
    read,
)
from allegrobridge.client.base import BaseRecord, SessionRecord, SkillModule
from allegrobridge.client.base._record import _ID
from allegrobridge.client.base._rpc import (
    _api_procedures,
    _core_api,
    _core_procedures,
)
from allegrobridge.client.session import Session
from allegrobridge.client.translator import Translator
from allegrobridge.client.workspace import Workspace
from allegrobridge.exceptions import (
    AllegroError,
    AllegroFileNotFoundError,
    AllegroLaunchError,
    AllegroProtocolError,
    AllegroServerIdentityError,
    AllegroTimeoutError,
    ExtensionError,
    RecordIDError,
)


def _assert_id(record: SessionRecord, session: Session) -> None:
    assert record._id == _ID(ref(session), session.generation)


RecordT = TypeVar('RecordT', bound=SessionRecord)


def _bind_id(record: RecordT, session: Session) -> RecordT:
    record.model_post_init(_ID(ref(session), session.generation))
    return record


def _session(workspace: Mock | None = None) -> Session:
    workspace = MagicMock() if workspace is None else workspace
    workspace.epoch = 0
    return Session(Mock(workspace=workspace))


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
    core = Path(allegrobridge._kernel.server.__file__).with_name('python_server.il')
    runtime = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
    assert lines[:2] == [
        f'skill load("{core.as_posix()}")',
        f'skill load("{runtime.as_posix()}")',
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

    def test_exposes_workspace_and_epoch(self) -> None:
        workspace = Mock(epoch=0)
        session = _session(workspace)
        assert session.raw is workspace
        assert session.generation == 1

        session.refresh()

        assert session.generation == 2
        assert workspace.mock_calls == []

    def test_sessions_independently_follow_shared_workspace_reconnects(self) -> None:
        workspace = Mock(epoch=0)
        first = _session(workspace)
        second = _session(workspace)

        workspace.epoch = 2

        assert first.generation == 3
        assert second.generation == 3
        assert first.generation == 3

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


class TestSessionBindings:
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/probe.il')

    @staticmethod
    def _api(name: str, procedure: str) -> type[SessionApi]:
        def project(self: SessionApi) -> RpcArgs:
            return ()

        return type(
            name,
            (SessionApi,),
            {
                'module': TestSessionBindings.module,
                'project': read(procedure, TypeAdapter(int))(project),
            },
        )

    def test_bind_prepares_and_caches_api_by_class(self) -> None:
        api = self._api('ProbeApi', '__abp_probe_project')
        workspace = MagicMock()
        session = _session(workspace)

        first = session.bind(api)

        assert isinstance(first, api)
        assert session.bind(api) is first
        workspace._ensure_module.assert_called_once_with(
            self.module,
            ('__abp_probe_project',),
        )

    def test_skill_module_is_an_immutable_cache_key(self) -> None:
        assert hash(self.module) == hash(
            SkillModule('tests.allegrobridge.fixtures', 'server/extensions/probe.il')
        )
        with pytest.raises(FrozenInstanceError):
            self.module.resource = 'changed.il'  # type: ignore[misc]

    def test_bind_isolates_readiness_errors_by_api_class(self) -> None:
        broken = self._api('BrokenApi', '__abp_broken_project')
        working = self._api('WorkingApi', '__abp_working_project')
        failure = ExtensionError('broken readiness')
        workspace = MagicMock()
        workspace._ensure_module.side_effect = [failure, None]
        session = _session(workspace)

        with pytest.raises(ExtensionError) as first:
            session.bind(broken)
        with pytest.raises(ExtensionError) as second:
            session.bind(broken)

        assert second.value is first.value
        assert isinstance(session.bind(working), working)
        assert workspace._ensure_module.call_count == 2

    def test_bind_rejects_api_without_skill_module(self) -> None:
        class LocalApi(SessionApi):
            pass

        with pytest.raises(TypeError, match='SkillModule'):
            _session().bind(LocalApi)

    def test_session_has_no_dynamic_extension_namespace(self) -> None:
        assert not hasattr(_session(), 'ext')

    def test_core_api_slot_is_local_and_cached(self) -> None:
        workspace = MagicMock()
        session = _session(workspace)

        assert session.board is session.board
        assert isinstance(session.board, BoardApi)
        workspace._ensure_module.assert_not_called()


class TestCoreKeyedApi:
    def test_returns_matches_and_rejects_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        component = object()
        net = object()
        monkeypatch.setattr(ComponentsApi, '_project', Mock(side_effect=[[component], None]))
        monkeypatch.setattr(NetsApi, '_project', Mock(side_effect=[[net], None]))
        session = _session()

        assert session.components['R1'] is component
        with pytest.raises(KeyError, match='MISSING'):
            _ = session.components['MISSING']
        assert session.nets['GND'] is net
        with pytest.raises(KeyError, match='MISSING'):
            _ = session.nets['MISSING']

    def test_nets_exposes_single_request_collection_operations(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        net = object()
        project = Mock(return_value=[net])
        monkeypatch.setattr(NetsApi, '_project', project)
        nets = _session().nets

        assert nets.snapshot() == [net]
        project.assert_called_once_with(None)
        project.reset_mock()
        assert list(nets) == [net]
        project.assert_called_once_with(None)
        project.reset_mock()
        assert nets.get('GND') is net
        project.assert_called_once_with('GND')
        project.reset_mock()
        assert 'GND' in nets
        project.assert_called_once_with('GND')
        project.reset_mock()
        with pytest.raises(TypeError, match='snapshot'):
            bool(nets)
        project.assert_not_called()

    def test_keyed_collection_distinguishes_missing_ambiguous_and_protocol_errors(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        project = Mock(side_effect=[[], [], [object(), object()], AllegroProtocolError('bad')])
        monkeypatch.setattr(NetsApi, '_project', project)
        nets = _session().nets

        assert nets.get('MISSING') is None
        assert 'MISSING' not in nets
        with pytest.raises(AllegroProtocolError, match='multiple records'):
            _ = nets['DUPLICATE']
        with pytest.raises(AllegroProtocolError, match='bad'):
            nets.get('BROKEN')

    @pytest.mark.parametrize(
        ('api_type', 'key'),
        [
            (ComponentsApi, 42),
            (LayersApi, ('ETCH/TOP',)),
            (NetsApi, 42),
            (PadstacksApi, object()),
            (PinsApi, 'GND'),
            (PinsApi, 'ab'),
            (PinsApi, ('U1',)),
            (PinsApi, ('U1', '1', 'extra')),
            (PinsApi, (1, '1')),
            (PinsApi, ['U1', '1']),
            (PinsApi, 42),
        ],
    )
    def test_contains_rejects_invalid_keys_without_rpc(
        self,
        monkeypatch: pytest.MonkeyPatch,
        api_type: type[SessionApi],
        key: object,
    ) -> None:
        project = Mock()
        monkeypatch.setattr(api_type, '_project', project)
        api = api_type(_session())

        assert key not in api  # type: ignore[operator]
        project.assert_not_called()

    @pytest.mark.parametrize(
        ('api_type', 'snapshot_args', 'key', 'query_args'),
        [
            (ComponentsApi, (None, True), 'R1', ('R1', True)),
            (LayersApi, (None, False), 'ETCH/TOP', ('ETCH/TOP', False)),
            (PadstacksApi, (None,), 'VIA12', ('VIA12',)),
            (PinsApi, (None, None, None), ('U1', '1'), ('U1', '1', None)),
        ],
    )
    def test_domain_collections_preserve_projection_arguments(
        self,
        monkeypatch: pytest.MonkeyPatch,
        api_type: type[SessionApi],
        snapshot_args: tuple[object, ...],
        key: object,
        query_args: tuple[object, ...],
    ) -> None:
        item = object()
        project = Mock(return_value=[item])
        monkeypatch.setattr(api_type, '_project', project)
        api = api_type(_session())

        assert api.snapshot() == [item]  # type: ignore[attr-defined]
        project.assert_called_once_with(*snapshot_args)
        project.reset_mock()
        assert api[key] is item  # type: ignore[index]
        project.assert_called_once_with(*query_args)
        project.reset_mock()
        assert key in api  # type: ignore[operator]
        project.assert_called_once_with(*query_args)


class TestCollectionApi:
    @pytest.mark.parametrize(
        ('api_type', 'snapshot_kwargs'),
        [
            (SymbolsApi, {'type': None}),
            (ViasApi, {'net': None, 'layer': None, 'padstack': None}),
            (RoutesApi, {'net': None, 'layer': None}),
            (ShapesApi, {'net': None, 'layer': None, 'dynamic': None}),
            (DrcApi, {}),
        ],
    )
    def test_domain_collections_preserve_snapshot_arguments(
        self,
        monkeypatch: pytest.MonkeyPatch,
        api_type: type[SessionApi],
        snapshot_kwargs: dict[str, object],
    ) -> None:
        item = object()
        project = Mock(return_value=[item])
        monkeypatch.setattr(api_type, '_project', project)
        api = api_type(_session())

        assert api.snapshot() == [item]  # type: ignore[attr-defined]
        project.assert_called_once_with(**snapshot_kwargs)


class TestRpcInheritance:
    def test_resolves_inheritance_and_reads_current_core_class(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def declaration(self: SessionApi) -> RpcArgs:
            return ()

        def operation(procedure: str) -> object:
            return read(procedure, TypeAdapter(int))(declaration)

        class BaseApi(SessionApi):
            inherited = operation('__base')
            hidden = operation('__hidden')
            shared = operation('__shared')

        class OtherApi(SessionApi):
            other = operation('__other')
            alias = operation('__shared')

        class ChildApi(BaseApi, OtherApi):
            hidden = None
            child = operation('__child')
            shared = operation('__shared')

        assert _api_procedures(ChildApi) == ('__child', '__shared', '__base', '__other')
        monkeypatch.setattr(
            ComponentsApi,
            'late',
            operation('__abLateCoreProbe'),
            raising=False,
        )
        assert '__abLateCoreProbe' in _core_procedures()


class TestGeometry:
    def test_values_are_immutable_tuples(self) -> None:
        point = Point(1.0, 2.0)
        x, y = point
        bbox = BBox(point, Point(3.0, 4.0))

        assert (x, y) == (1.0, 2.0)
        assert point[0] == point.x
        assert bbox[1] == bbox.ur
        with pytest.raises(AttributeError):
            point.x = 3.0  # type: ignore[misc]

    def test_values_use_explicit_skill_encoding(self) -> None:
        translator = Translator()

        assert translator.encode(Point(1.0, 2.0)) == '(list 1.0 2.0)'
        assert translator.encode(BBox(Point(1.0, 2.0), Point(3.0, 4.0))) == (
            '(list (list 1.0 2.0) (list 3.0 4.0))'
        )

    def test_records_expose_local_locations(self) -> None:
        symbol = SymbolInfo(
            name='RES_0402',
            type='PACKAGE',
            refdes='R1',
            x=1.0,
            y=2.0,
            rotation=90.0,
        )
        placed = ComponentInfo(
            refdes='R1',
            device_type='RESISTOR',
            package='RES_0402',
            component_class='DISCRETE',
            placement='placed',
            x=1.0,
            y=2.0,
            rotation=90.0,
        )
        unplaced = placed.model_copy(
            update={'placement': 'unplaced', 'x': None, 'y': None, 'rotation': None}
        )

        assert symbol.location == Point(1.0, 2.0)
        assert placed.location == Point(1.0, 2.0)
        assert unplaced.location is None

    @pytest.mark.parametrize('value', [float('nan'), float('inf'), float('-inf')])
    def test_records_reject_non_finite_locations(self, value: float) -> None:
        with pytest.raises(ValidationError):
            SymbolInfo(
                name='RES_0402',
                type='PACKAGE',
                refdes='R1',
                x=value,
                y=2.0,
                rotation=90.0,
            )
        with pytest.raises(ValidationError):
            ComponentInfo(
                refdes='R1',
                device_type='RESISTOR',
                package='RES_0402',
                component_class='DISCRETE',
                placement='placed',
                x=value,
                y=2.0,
                rotation=90.0,
            )

    @pytest.mark.parametrize(
        'value',
        [True, '1.0', float('nan'), float('inf'), float('-inf')],
    )
    def test_encoder_rejects_invalid_coordinates(self, value: object) -> None:
        with pytest.raises(ValidationError):
            Translator().encode(Point(value, 2.0))  # type: ignore[arg-type]


class TestReadApi:
    def test_client_api_exports_only_public_declarations(self) -> None:
        assert set(api_module.__all__) == {
            'Batch',
            'BBox',
            'BoardApi',
            'BoardInfo',
            'Cmd',
            'CmdResult',
            'Collection',
            'ComponentRef',
            'ComponentInfo',
            'ComponentsApi',
            'DrcApi',
            'DrcInfo',
            'DrcObjectRef',
            'KeyedCollection',
            'LayerInfo',
            'LayersApi',
            'NetInfo',
            'NetRef',
            'NetsApi',
            'PadstackInfo',
            'PadstacksApi',
            'PinInfo',
            'PinRef',
            'PinsApi',
            'Point',
            'RouteInfo',
            'RoutesApi',
            'RpcArgs',
            'RpcDef',
            'SessionApi',
            'ShapeInfo',
            'ShapesApi',
            'SkillModule',
            'SymbolInfo',
            'SymbolsApi',
            'ViaInfo',
            'ViasApi',
            'read',
            'write',
        }
        assert not hasattr(api_module, 'AllegroProtocolError')
        assert not hasattr(api_module, 'core_api')
        assert not hasattr(api_module, '_Record')
        assert not hasattr(api_module, 'BaseRecord')
        assert not hasattr(api_module, 'SessionRecord')

    def test_core_procedures_are_collected_from_api_declarations(self) -> None:
        procedures = (
            '__abProjectBoard',
            '__abProjectComponents',
            '__abMoveComponent',
            '__abMoveComponentsBy',
            '__abProjectLayers',
            '__abProjectNets',
            '__abProjectPadstacks',
            '__abProjectPins',
            '__abProjectSymbols',
        )
        assert _core_procedures() == procedures
        assert _core_api(ComponentsApi) is ComponentsApi
        assert _core_procedures() == procedures

    def test_operations_expose_immutable_metadata(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.side_effect = [None, None, None, None, None]
        session = _session(workspace)

        class ProbeApi(SessionApi):
            @read('__abList', TypeAdapter(list[int]))
            def items(self) -> RpcArgs:
                return ()

            @read('__abOptionalList', TypeAdapter(list[int] | None))
            def optional_items(self) -> RpcArgs:
                return ()

            @read('__abInt', TypeAdapter(int))
            def count(self) -> RpcArgs:
                return ()

            @read('__abSequence', TypeAdapter(Sequence[int]))
            def sequence(self) -> RpcArgs:
                return ()

            @read('__abNonEmptyList', TypeAdapter(Annotated[list[int], Field(min_length=1)]))
            def non_empty_items(self) -> RpcArgs:
                return ()

        api = ProbeApi(session)
        assert api.items() == []
        assert api.optional_items() is None
        with pytest.raises(AllegroProtocolError, match='__abInt'):
            api.count()
        with pytest.raises(AllegroProtocolError, match='__abSequence'):
            api.sequence()
        with pytest.raises(AllegroProtocolError, match='__abNonEmptyList'):
            api.non_empty_items()
        assert ProbeApi.items.spec == RpcDef('read', '__abList')
        assert DrcApi.check.spec == RpcDef('direct', '__abCheckDrcs')
        assert ComponentsApi.move.spec == RpcDef('write', '__abMoveComponent')
        assert ComponentsApi.move_by.spec == RpcDef('write', '__abMoveComponentsBy')
        assert not hasattr(ProbeApi.items.spec, 'nil_as_empty_list')
        with pytest.raises(FrozenInstanceError):
            ProbeApi.items.spec.kind = 'write'

    def test_declaration_preserves_signature_and_sends_once(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = 3
        session = _session(workspace)

        class ProbeApi(SessionApi):
            @read('__abProbe', TypeAdapter(int))
            def read(self, left: int, right: int = 0) -> RpcArgs:
                return left, right

        api = ProbeApi(session)

        assert str(signature(api.read)) == "(left: 'int', right: 'int' = 0) -> 'RpcArgs'"
        assert api.read(1, right=2) == 3
        workspace.__getitem__.assert_called_once_with('__abProbe')
        workspace.__getitem__.return_value.assert_called_once_with(1, 2)

    def test_read_api_binds_private_id(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = {
            'path': 'shape1.brd',
            'units': 'mils',
            'component_count': 1,
            'symbol_count': 1,
            'net_count': 1,
        }
        session = _session(workspace)

        board = session.board()

        assert board.path == 'shape1.brd'
        _assert_id(board, session)

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
        session = _session(workspace)

        assert session.components() == []
        component = session.components()[0]
        _assert_id(component, session)
        with pytest.raises(AllegroProtocolError, match='__abProjectNets'):
            session.nets()

    def test_net_records_bind_private_id(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'name': 'GND',
                'branch_count': 1,
                'unconnected_count': 0,
                'unplaced_pin_count': 0,
            }
        ]
        session = _session(workspace)

        net = session.nets()[0]

        _assert_id(net, session)
        assert NetInfo.model_construct(name='GND')._id is None
        assert '_id' not in net.model_dump()

    @pytest.mark.parametrize(
        'record_type',
        [
            BoardInfo,
            ComponentInfo,
            DrcInfo,
            LayerInfo,
            NetInfo,
            PadstackInfo,
            PinInfo,
            RouteInfo,
            ShapeInfo,
            SymbolInfo,
            ViaInfo,
        ],
    )
    def test_database_records_use_private_id(self, record_type: type[BaseRecord]) -> None:
        assert issubclass(record_type, SessionRecord)
        assert 'session_generation' not in record_type.model_fields

    def test_layers_delegate_filters_and_lookup_to_one_projection(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'name': 'ETCH/TOP',
                'class_name': 'ETCH',
                'subclass': 'TOP',
                'number': 1,
            }
        ]
        session = _session(workspace)

        layers = session.layers(etch_only=True)

        assert [layer.model_dump() for layer in layers] == [
            LayerInfo(
                name='ETCH/TOP',
                class_name='ETCH',
                subclass='TOP',
                number=1,
            ).model_dump()
        ]
        _assert_id(layers[0], session)
        assert session.layers is session.layers
        etch_only = True
        workspace.__getitem__.return_value.assert_called_once_with(None, etch_only)

        assert session.layers['ETCH/TOP'].name == 'ETCH/TOP'
        etch_only = False
        workspace.__getitem__.return_value.assert_called_with('ETCH/TOP', etch_only)
        assert not LayerInfo(
            name='BOARD GEOMETRY/OUTLINE',
            class_name='BOARD GEOMETRY',
            subclass='OUTLINE',
            number=0,
        ).is_etch

    def test_layers_getitem_raises_when_name_is_missing(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = None
        session = _session(workspace)

        with pytest.raises(KeyError, match='ETCH/__MISSING__'):
            _ = session.layers['ETCH/__MISSING__']

    def test_pins_delegate_filters_and_stable_lookup(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'refdes': 'U1',
                'number': '1',
                'net': 'GND',
                'padstack': 'PAD60CIR30D',
                'placement': 'placed',
                'x': 1.0,
                'y': 2.0,
                'rotation': 0.0,
                'start_layer': 'ETCH/TOP',
                'end_layer': 'ETCH/BOTTOM',
            }
        ]
        session = _session(workspace)

        pins = session.pins(component='U1', net='GND')

        assert [pin.model_dump() for pin in pins] == [
            PinInfo(
                refdes='U1',
                number='1',
                net='GND',
                padstack='PAD60CIR30D',
                placement='placed',
                x=1.0,
                y=2.0,
                rotation=0.0,
                start_layer='ETCH/TOP',
                end_layer='ETCH/BOTTOM',
            ).model_dump()
        ]
        _assert_id(pins[0], session)
        assert session.pins is session.pins
        workspace.__getitem__.return_value.assert_called_once_with('U1', None, 'GND')

        assert session.pins['U1', '1'] == pins[0]
        workspace.__getitem__.return_value.assert_called_with('U1', '1', None)

    def test_pins_getitem_raises_when_key_is_missing(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = None
        session = _session(workspace)

        with pytest.raises(KeyError, match=r"\('U1', '__MISSING__'\)"):
            _ = session.pins['U1', '__MISSING__']

    def test_padstacks_delegate_collection_and_lookup(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'name': 'VIA12',
                'type': 'through',
                'usage': 'through_via',
                'start_layer': 'TOP',
                'end_layer': 'BOTTOM',
            }
        ]
        session = _session(workspace)

        padstacks = session.padstacks()

        assert [padstack.model_dump() for padstack in padstacks] == [
            PadstackInfo(
                name='VIA12',
                type='through',
                usage='through_via',
                start_layer='TOP',
                end_layer='BOTTOM',
            ).model_dump()
        ]
        _assert_id(padstacks[0], session)
        assert session.padstacks is session.padstacks
        workspace.__getitem__.return_value.assert_called_once_with(None)

        assert session.padstacks['VIA12'] == padstacks[0]
        workspace.__getitem__.return_value.assert_called_with('VIA12')

    def test_padstacks_getitem_raises_when_name_is_missing(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = None
        session = _session(workspace)

        with pytest.raises(KeyError, match='__MISSING_PADSTACK__'):
            _ = session.padstacks['__MISSING_PADSTACK__']

    def test_symbols_delegate_type_filter_to_one_projection(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'name': 'RES_0402',
                'type': 'PACKAGE',
                'refdes': 'R1',
                'x': 1.0,
                'y': 2.0,
                'rotation': 90.0,
            }
        ]
        session = _session(workspace)

        symbols = session.symbols(type='PACKAGE')

        assert [symbol.model_dump() for symbol in symbols] == [
            SymbolInfo(
                name='RES_0402',
                type='PACKAGE',
                refdes='R1',
                x=1.0,
                y=2.0,
                rotation=90.0,
            ).model_dump()
        ]
        _assert_id(symbols[0], session)
        assert session.symbols is session.symbols
        workspace.__getitem__.return_value.assert_called_once_with('PACKAGE')

    def test_vias_load_extension_once_and_delegate_filters(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'padstack': 'VIA12',
                'net': 'GND',
                'x': 1.0,
                'y': 2.0,
                'rotation': 0.0,
                'mirroring': 'unmirrored',
                'start_layer': 'ETCH/TOP',
                'end_layer': 'ETCH/BOTTOM',
            }
        ]
        session = _session(workspace)

        vias = session.vias(net='GND', layer='ETCH/TOP', padstack='VIA12')

        workspace._ensure_module.assert_called_once_with(
            ViasApi.module,
            ('__abProjectVias', '__abCreateVia'),
        )
        assert session.vias is session.vias
        assert [via.model_dump() for via in vias] == [
            ViaInfo(
                padstack='VIA12',
                net='GND',
                x=1.0,
                y=2.0,
                rotation=0.0,
                mirroring='unmirrored',
                start_layer='ETCH/TOP',
                end_layer='ETCH/BOTTOM',
            ).model_dump()
        ]
        _assert_id(vias[0], session)
        workspace.__getitem__.return_value.assert_called_once_with(
            'GND',
            'ETCH/TOP',
            'VIA12',
        )

    def test_via_create_command_uses_expression_and_keeps_arguments(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.expr.return_value = Expr.raw_skill('__abCreateVia(...)')
        session = _session(workspace)

        command = session.vias.create.command(
            'VIA12',
            at=(1.0, 2.0),
            net='GND',
            rotation=90.0,
            mirrored=True,
        )

        assert command.proc == '__abCreateVia'
        assert command.expr == SkillCode('__abCreateVia(...)')
        assert remote.expr.call_args.args == ('VIA12', Point(1.0, 2.0), 'GND', True, 90.0)
        assert isinstance(remote.expr.call_args.args[1], Point)

    @pytest.mark.parametrize(
        'value',
        [True, '1.0', float('nan'), float('inf'), float('-inf')],
    )
    def test_via_create_rejects_invalid_geometry_before_rpc(self, value: object) -> None:
        workspace = MagicMock()
        session = _session(workspace)

        invalid = [
            ((value, 2.0), 0.0),
            ((1.0, 2.0), value),
        ]
        for at, rotation in invalid:
            with pytest.raises(ValidationError):
                session.vias.create.command(
                    'VIA12',
                    at=at,  # type: ignore[arg-type]
                    rotation=rotation,  # type: ignore[arg-type]
                )

        workspace.__getitem__.assert_not_called()

    def test_routes_load_extension_once_and_delegate_filters(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'net': 'GND',
                'layer': 'ETCH/TOP',
                'start': {'x': 1.0, 'y': 2.0},
                'end': {'x': 3.0, 'y': 4.0},
                'width': 0.2,
            }
        ]
        session = _session(workspace)

        routes = session.routes(net='GND', layer='ETCH/TOP')

        workspace._ensure_module.assert_called_once_with(
            RoutesApi.module,
            ('__abProjectRoutes', '__abCreateRoute'),
        )
        assert session.routes is session.routes
        assert [route.model_dump() for route in routes] == [
            RouteInfo(
                net='GND',
                layer='ETCH/TOP',
                start=Point(x=1.0, y=2.0),
                end=Point(x=3.0, y=4.0),
                width=0.2,
            ).model_dump()
        ]
        _assert_id(routes[0], session)
        workspace.__getitem__.return_value.assert_called_once_with('GND', 'ETCH/TOP')

    def test_route_create_command_uses_expression_and_keeps_arguments(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.expr.return_value = Expr.raw_skill('__abCreateRoute(...)')
        session = _session(workspace)

        command = session.routes.create.command(
            'GND',
            [(1.0, 2.0), (3.0, 4.0)],
            'ETCH/TOP',
            0.2,
        )

        assert command.proc == '__abCreateRoute'
        assert command.expr == SkillCode('__abCreateRoute(...)')
        assert remote.expr.call_args.args == (
            'GND',
            [Point(1.0, 2.0), Point(3.0, 4.0)],
            'ETCH/TOP',
            0.2,
        )
        assert type(remote.expr.call_args.args[1]) is list
        assert all(isinstance(point, Point) for point in remote.expr.call_args.args[1])

    @pytest.mark.parametrize(
        ('points', 'width', 'message'),
        [
            ([(1.0, 2.0)], 0.2, 'at least two'),
            ([(1.0, 2.0), (3.0,)], 0.2, 'two coordinates'),
            ([(1.0, 2.0), (3.0, 4.0)], 0.0, 'positive'),
        ],
    )
    def test_route_create_rejects_invalid_geometry(
        self,
        points: list[tuple[float, ...]],
        width: float,
        message: str,
    ) -> None:
        session = _session()

        with pytest.raises(ValueError, match=message):
            session.routes.create.command(
                'GND',
                points,  # type: ignore[arg-type]
                'ETCH/TOP',
                width,
            )

    @pytest.mark.parametrize(
        'value',
        [True, '1.0', float('nan'), float('inf'), float('-inf')],
    )
    def test_route_create_rejects_invalid_coordinates_before_rpc(self, value: object) -> None:
        workspace = MagicMock()
        session = _session(workspace)

        invalid = [
            ([(value, 2.0), (3.0, 4.0)], 0.2),
            ([(1.0, 2.0), (3.0, 4.0)], value),
        ]
        for points, width in invalid:
            with pytest.raises(ValidationError):
                session.routes.create.command(
                    'GND',
                    points,  # type: ignore[arg-type]
                    'ETCH/TOP',
                    width,  # type: ignore[arg-type]
                )

        workspace.__getitem__.assert_not_called()

    @pytest.mark.parametrize('value', [float('nan'), float('inf'), float('-inf')])
    def test_route_projection_rejects_non_finite_geometry(self, value: float) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'net': 'GND',
                'layer': 'ETCH/TOP',
                'start': {'x': value, 'y': 2.0},
                'end': {'x': 3.0, 'y': 4.0},
                'width': 0.2,
            }
        ]

        with pytest.raises(AllegroProtocolError, match='__abProjectRoutes'):
            _session(workspace).routes()

    @pytest.mark.parametrize(
        ('dynamic', 'encoded'),
        [(None, None), (True, 'dynamic'), (False, 'static')],
    )
    def test_shapes_load_extension_once_and_encode_dynamic_filter(
        self,
        dynamic: bool | None,
        encoded: str | None,
    ) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'net': 'GND',
                'layer': 'ETCH/TOP',
                'dynamic': 'dynamic',
                'bbox': {
                    'll': {'x': 1.0, 'y': 2.0},
                    'ur': {'x': 3.0, 'y': 4.0},
                },
            }
        ]
        session = _session(workspace)

        shapes = session.shapes(net='GND', layer='ETCH/TOP', dynamic=dynamic)

        workspace._ensure_module.assert_called_once_with(
            ShapesApi.module,
            ('__abProjectShapes',),
        )
        assert session.shapes is session.shapes
        assert [shape.model_dump() for shape in shapes] == [
            ShapeInfo(
                net='GND',
                layer='ETCH/TOP',
                dynamic='dynamic',
                bbox=BBox(
                    ll=Point(x=1.0, y=2.0),
                    ur=Point(x=3.0, y=4.0),
                ),
            ).model_dump()
        ]
        _assert_id(shapes[0], session)
        workspace.__getitem__.return_value.assert_called_once_with(
            'GND',
            'ETCH/TOP',
            encoded,
        )

    def test_drc_loads_extension_once_and_projects_stable_references(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = [
            {
                'name': 'Ts Allowed',
                'category': 'PHYSICAL CONSTRAINTS',
                'source': 'VOLTAGE',
                'expected': 'NOT_ALLOWED',
                'actual': 'ANYWHERE',
                'layer': 'DRC ERROR CLASS/GND',
                'location': {'x': 1.0, 'y': 2.0},
                'bbox': {
                    'll': {'x': 0.0, 'y': 1.0},
                    'ur': {'x': 2.0, 'y': 3.0},
                },
                'objects': [
                    {'kind': 'pin', 'refdes': 'U3', 'number': '14'},
                    {'kind': 'component', 'refdes': 'U3'},
                    {'kind': 'net', 'name': 'VCC'},
                ],
            }
        ]
        session = _session(workspace)

        drcs = session.drc()

        workspace._ensure_module.assert_called_once_with(
            DrcApi.module,
            ('__abProjectDrcs', '__abUpdateDrcs', '__abCheckDrcs'),
        )
        assert session.drc is session.drc
        assert [drc.model_dump() for drc in drcs] == [
            DrcInfo(
                name='Ts Allowed',
                category='PHYSICAL CONSTRAINTS',
                source='VOLTAGE',
                expected='NOT_ALLOWED',
                actual='ANYWHERE',
                layer='DRC ERROR CLASS/GND',
                location=Point(x=1.0, y=2.0),
                bbox=BBox(
                    ll=Point(x=0.0, y=1.0),
                    ur=Point(x=2.0, y=3.0),
                ),
                objects=[
                    PinRef(kind='pin', refdes='U3', number='14'),
                    ComponentRef(kind='component', refdes='U3'),
                    NetRef(kind='net', name='VCC'),
                ],
            ).model_dump()
        ]
        _assert_id(drcs[0], session)
        workspace.__getitem__.return_value.assert_called_once_with()


class TestDrcApi:
    def test_maps_stable_targets_and_executes_directly(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.return_value = None
        session = _session(workspace)
        drc = session.drc
        workspace.reset_mock()
        targets: list[tuple[ComponentInfo | NetInfo | PinInfo, tuple[str, str, str | None]]] = [
            (
                _bind_id(
                    ComponentInfo.model_construct(refdes='R1'),
                    session,
                ),
                ('component', 'R1', None),
            ),
            (
                _bind_id(
                    NetInfo.model_construct(name='GND'),
                    session,
                ),
                ('net', 'GND', None),
            ),
            (
                _bind_id(
                    PinInfo.model_construct(refdes='R1', number='1'),
                    session,
                ),
                ('pin', 'R1', '1'),
            ),
        ]

        for target, expected_args in targets:
            assert drc.check(target) == []
            workspace.__getitem__.return_value.assert_called_once_with(*expected_args)
            workspace.__getitem__.return_value.reset_mock()

        workspace.transaction.assert_not_called()
        assert DrcApi.check.spec.proc == '__abCheckDrcs'  # type: ignore[attr-defined]
        assert not hasattr(drc.check, 'preview')
        assert not hasattr(drc.check, 'command')

    @pytest.mark.parametrize(
        ('target', 'message'),
        [
            (NetInfo.model_construct(name='GND'), 'not bound'),
            (None, 'another Session'),
        ],
    )
    def test_rejects_invalid_record_provenance_before_rpc(
        self,
        target: NetInfo | None,
        message: str,
    ) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        drc = session.drc
        if target is None:
            owner = _session()
            target = _bind_id(NetInfo.model_construct(name='GND'), owner)
        workspace.reset_mock()

        with pytest.raises(RecordIDError, match=message):
            drc.check(target)

        assert workspace.mock_calls == []

    def test_rejects_record_from_collected_session_before_rpc(self) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        drc = session.drc
        target = _bind_id(NetInfo.model_construct(name='GND'), _session())
        workspace.reset_mock()

        with pytest.raises(RecordIDError, match='no longer available'):
            drc.check(target)

        assert workspace.mock_calls == []

    def test_refresh_makes_record_stale_before_rpc(self) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        drc = session.drc
        target = _bind_id(NetInfo.model_construct(name='GND'), session)
        session.refresh()
        workspace.reset_mock()

        with pytest.raises(RecordIDError, match='stale'):
            drc.check(target)

        assert workspace.mock_calls == []

    def test_reconnect_rejects_old_record_and_accepts_new_record(self) -> None:
        workspace = MagicMock(epoch=0)
        workspace.__getitem__.return_value.return_value = [
            {
                'name': 'GND',
                'branch_count': 1,
                'unconnected_count': 0,
                'unplaced_pin_count': 0,
            }
        ]
        session = _session(workspace)
        drc = session.drc
        old = session.nets()[0]
        workspace.epoch = 1
        current = session.nets()[0]
        workspace.__getitem__.return_value.return_value = []
        workspace.reset_mock()

        with pytest.raises(RecordIDError, match='stale'):
            drc.check(old)
        assert workspace.mock_calls == []

        assert drc.check(current) == []
        _assert_id(current, session)
        workspace.__getitem__.return_value.assert_called_once_with('net', 'GND', None)

    def test_rejects_invalid_target_and_payload(self) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        drc = session.drc

        with pytest.raises(TypeError, match='ComponentInfo, NetInfo, or PinInfo'):
            drc.check(object())  # type: ignore[arg-type]

        workspace.__getitem__.return_value.return_value = [{'name': 'incomplete'}]
        target = _bind_id(NetInfo.model_construct(name='GND'), session)
        with pytest.raises(AllegroProtocolError, match='__abCheckDrcs'):
            drc.check(target)


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
        remote.expr.return_value = Expr.raw_skill('__abMoveComponent("R1" 1.0 2.0 nil)')
        workspace.transaction.return_value = self._component_payload(1.0)
        session = _session(workspace)

        command = session.components.move.command('R1', x=1.0, y=2.0)
        rotated = session.components.move.command('R1', x=1, y=2, rotation=90)

        assert ComponentsApi.move.spec.proc == '__abMoveComponent'
        assert list(signature(session.components.move).parameters) == [
            'refdes',
            'x',
            'y',
            'rotation',
        ]
        assert isinstance(command, Cmd)
        assert command.proc == '__abMoveComponent'
        assert command.expr == '__abMoveComponent("R1" 1.0 2.0 nil)'
        assert rotated.proc == '__abMoveComponent'
        assert remote.expr.call_args.args == ('R1', 1.0, 2.0, 90.0)
        workspace.transaction.assert_not_called()
        with pytest.raises(FrozenInstanceError):
            command.proc = '__changed'

        moved = session.components.move('R1', x=1.0, y=2.0)

        assert moved.x == pytest.approx(1.0)
        _assert_id(moved, session)
        workspace.transaction.assert_called_once_with(command.expr)

    @pytest.mark.parametrize(
        'value',
        [True, '1.0', float('nan'), float('inf'), float('-inf')],
    )
    def test_move_rejects_invalid_geometry_before_rpc(self, value: object) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        invalid = [
            (value, 2.0, None),
            (1.0, value, None),
            (1.0, 2.0, value),
        ]

        for x, y, rotation in invalid:
            with pytest.raises(ValidationError):
                session.components.move.command(
                    'R1',
                    x=x,  # type: ignore[arg-type]
                    y=y,  # type: ignore[arg-type]
                    rotation=rotation,  # type: ignore[arg-type]
                )

        workspace.__getitem__.assert_not_called()

    def test_move_by_builds_one_atomic_command_and_preserves_order(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        expression = '__abMoveComponentsBy((list "R1" "R2") 1.0 2.0)'
        remote.expr.return_value = Expr.raw_skill(expression)
        payloads = [
            self._component_payload(2.0),
            self._component_payload(3.0) | {'refdes': 'R2'},
        ]
        workspace.transaction.return_value = payloads
        session = _session(workspace)
        components = [
            _bind_id(ComponentInfo.model_validate(self._component_payload(1.0)), session),
            _bind_id(
                ComponentInfo.model_validate(self._component_payload(2.0) | {'refdes': 'R2'}),
                session,
            ),
        ]

        command = session.components.move_by.command(components, dx=1.0, dy=2.0)

        assert ComponentsApi.move_by.spec.proc == '__abMoveComponentsBy'
        assert list(signature(session.components.move_by).parameters) == ['components', 'dx', 'dy']
        assert command.proc == '__abMoveComponentsBy'
        assert command.expr == expression
        assert remote.expr.call_args.args == (['R1', 'R2'], 1.0, 2.0)
        workspace.transaction.assert_not_called()

        moved = session.components.move_by(components, dx=1.0, dy=2.0)

        assert [component.refdes for component in moved] == ['R1', 'R2']
        assert [component.x for component in moved] == [2.0, 3.0]
        assert all(component._id == _ID(ref(session), session.generation) for component in moved)
        workspace.transaction.assert_called_once_with(expression)

    @pytest.mark.parametrize(
        ('dx', 'dy'),
        [
            (True, 1.0),
            ('1.0', 1.0),
            (float('nan'), 1.0),
            (1.0, float('inf')),
            (1.0, float('-inf')),
        ],
    )
    def test_move_by_rejects_invalid_delta_before_rpc(self, dx: object, dy: object) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        component = _bind_id(
            ComponentInfo.model_validate(self._component_payload(1.0)),
            session,
        )

        with pytest.raises(ValidationError):
            session.components.move_by.command(
                [component],
                dx=dx,  # type: ignore[arg-type]
                dy=dy,  # type: ignore[arg-type]
            )

        workspace.__getitem__.assert_not_called()

    def test_move_by_rejects_duplicate_refdes_before_rpc(self) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        component = _bind_id(
            ComponentInfo.model_validate(self._component_payload(1.0)),
            session,
        )

        with pytest.raises(ValueError, match="duplicate component refdes: 'R1'"):
            session.components.move_by.command([component, component], dx=1.0, dy=2.0)

        workspace.__getitem__.assert_not_called()

    def test_move_by_rejects_unbound_foreign_and_stale_records_before_rpc(self) -> None:
        workspace = MagicMock()
        session = _session(workspace)
        other = _session()
        unbound = ComponentInfo.model_validate(self._component_payload(1.0))
        foreign = _bind_id(ComponentInfo.model_validate(self._component_payload(1.0)), other)
        stale = _bind_id(ComponentInfo.model_validate(self._component_payload(1.0)), session)
        session.refresh()

        for component, message in [
            (unbound, 'not bound'),
            (foreign, 'another Session'),
            (stale, 'stale'),
        ]:
            with pytest.raises(RecordIDError, match=message):
                session.components.move_by.command([component], dx=1.0, dy=2.0)

        workspace.__getitem__.assert_not_called()

    def test_command_derives_id_from_session(self) -> None:
        session = _session()

        command = Cmd(
            session,
            SkillCode('move1()'),
            '__abMoveComponent',
            TypeAdapter(ComponentInfo),
        )

        assert command._id == _ID(ref(session), session.generation)

    def test_preview_uses_dry_transaction(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.expr.return_value = Expr.raw_skill('__abMoveComponent("R1" 3.0 2.0 nil)')
        workspace.transaction.preview.return_value = self._component_payload(3.0)
        session = _session(workspace)

        preview = session.components.move.preview('R1', x=3.0, y=2.0)

        assert preview.x == pytest.approx(3.0)
        workspace.transaction.assert_not_called()
        workspace.transaction.preview.assert_called_once_with('__abMoveComponent("R1" 3.0 2.0 nil)')

    def test_stale_command_does_not_execute(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)
        command = session.components.move.command('R1', x=1.0, y=2.0)
        session.refresh()
        workspace.reset_mock()

        with pytest.raises(RecordIDError, match=r'Command.*stale'):
            command._execute()

        assert workspace.mock_calls == []

    def test_refresh_during_write_rejects_response(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)

        def refresh_during_transaction(_expr: SkillCode) -> dict[str, object]:
            session.refresh()
            return self._component_payload(1.0)

        workspace.transaction.side_effect = refresh_during_transaction

        with pytest.raises(RecordIDError, match=r'Command.*stale'):
            session.components.move('R1', x=1.0, y=2.0)

        workspace.transaction.assert_called_once()

    def test_reconnect_makes_existing_command_stale_before_rpc(self) -> None:
        workspace = MagicMock(epoch=0)
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)
        command = session.components.move.command('R1', x=1.0, y=2.0)
        workspace.epoch = 1
        workspace.reset_mock()

        with pytest.raises(RecordIDError, match=r'Command.*stale'):
            command._execute()

        workspace.transaction.assert_not_called()

    def test_drc_update_supports_command_immediate_and_preview(self) -> None:
        workspace = MagicMock()
        remote = workspace.__getitem__.return_value
        remote.expr.return_value = Expr.raw_skill('__abUpdateDrcs()')
        workspace.transaction.return_value = None
        workspace.transaction.preview.return_value = [
            {
                'name': 'Spacing',
                'category': 'NET SPACING CONSTRAINTS',
                'source': 'DEFAULT',
                'expected': '10 MILS',
                'actual': '5 MILS',
                'layer': 'DRC ERROR CLASS/TOP',
                'location': {'x': 1.0, 'y': 2.0},
                'bbox': {
                    'll': {'x': 0.0, 'y': 1.0},
                    'ur': {'x': 2.0, 'y': 3.0},
                },
                'objects': [],
            }
        ]
        session = _session(workspace)
        drc = session.drc
        workspace.reset_mock()

        command = drc.update.command()

        assert DrcApi.update.spec.proc == '__abUpdateDrcs'
        assert command.proc == '__abUpdateDrcs'
        assert command.expr == '__abUpdateDrcs()'
        workspace.transaction.assert_not_called()
        remote.assert_not_called()

        assert drc.update() == []
        workspace.transaction.assert_called_once_with(command.expr)

        preview = drc.update.preview()
        assert len(preview) == 1
        _assert_id(preview[0], session)
        workspace.transaction.preview.assert_called_once_with(command.expr)

    def test_drc_update_rejects_invalid_payload(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('__abUpdateDrcs()')
        workspace.transaction.return_value = [{'name': 'incomplete'}]
        session = _session(workspace)

        with pytest.raises(AllegroProtocolError, match='__abUpdateDrcs'):
            session.drc.update()


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
        workspace.__getitem__.return_value.expr.side_effect = [
            Expr.raw_skill('move1()'),
            Expr.raw_skill('move2()'),
        ]
        workspace.transaction.return_value = [self._payload('R1', 1.0), self._payload('R2', 2.0)]
        session = _session(workspace)

        with session.batch('move two') as batch:
            assert isinstance(batch, Batch)
            first = batch.call(session.components.move, 'R1', x=1.0, y=2.0)
            second = batch.call(session.components.move, 'R2', x=2.0, y=2.0)
            with pytest.raises(RuntimeError, match='pending'):
                _ = first.value

        assert isinstance(first, CmdResult)
        assert first.value.refdes == 'R1'
        assert second.value.refdes == 'R2'
        composite = workspace.transaction.call_args.args[0]
        assert 'progn' in composite
        assert composite.index('move1()') < composite.index('move2()')
        assert 'reverse(results)' in composite
        workspace.transaction.assert_called_once()

    def test_call_builds_and_adds_typed_command(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        workspace.transaction.return_value = [self._payload('R1', 1.0)]
        session = _session(workspace)

        with session.batch() as batch:
            result = batch.call(
                session.components.move,
                'R1',
                x=1.0,
                y=2.0,
            )

        assert result.value.refdes == 'R1'
        workspace.transaction.assert_called_once()

    def test_call_accepts_bound_write_without_command_suffix(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        workspace.transaction.return_value = [self._payload('R1', 1.0)]
        session = _session(workspace)

        with session.batch() as batch:
            result = batch.call(
                session.components.move,
                'R1',
                x=1.0,
                y=2.0,
            )
            with pytest.raises(RuntimeError, match='pending'):
                _ = result.value
            workspace.transaction.assert_not_called()

        assert result.value.refdes == 'R1'
        workspace.transaction.assert_called_once()

    def test_dry_run_uses_preview_and_empty_batch_sends_nothing(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        workspace.transaction.preview.return_value = [self._payload('R1', 1.0)]
        session = _session(workspace)

        with session.batch(dry_run=True) as batch:
            result = batch.call(session.components.move, 'R1', x=1.0, y=2.0)

        assert result.value.refdes == 'R1'
        workspace.transaction.assert_not_called()
        workspace.transaction.preview.assert_called_once()

        workspace.reset_mock()
        with session.batch():
            pass
        workspace.transaction.assert_not_called()
        workspace.transaction.preview.assert_not_called()

    def test_rejects_cross_session_command(self) -> None:
        session = _session()
        other = _session()
        command = other.components.move.command('R1', x=1.0, y=2.0)

        with (
            session.batch() as batch,
            pytest.raises(
                RecordIDError,
                match=r'Command.*another Session',
            ),
        ):
            batch.add(command)

    def test_rejects_stale_command_and_batch_before_rpc(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)
        command = session.components.move.command('R1', x=1.0, y=2.0)
        session.refresh()
        stale_batch = session.batch()
        session.refresh()
        current_batch = session.batch()
        current_command = session.components.move.command('R1', x=1.0, y=2.0)
        workspace.reset_mock()

        with current_batch, pytest.raises(RecordIDError, match=r'Command.*stale'):
            current_batch.add(command)
        with stale_batch, pytest.raises(RecordIDError, match=r'Batch.*stale'):
            stale_batch.add(current_command)

        assert workspace.mock_calls == []

    def test_refresh_after_add_fails_results_without_sending(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)
        results: list[CmdResult[ComponentInfo]] = []

        def execute() -> None:
            with session.batch() as batch:
                results.append(batch.call(session.components.move, 'R1', x=1.0, y=2.0))
                session.refresh()

        with pytest.raises(RecordIDError, match=r'Batch.*stale') as raised:
            execute()

        workspace.transaction.assert_not_called()
        with pytest.raises(RecordIDError) as result_error:
            _ = results[0].value
        assert result_error.value is raised.value

    @pytest.mark.parametrize('change', ['refresh', 'reconnect'])
    def test_generation_change_during_batch_rejects_response(self, change: str) -> None:
        workspace = MagicMock(epoch=0)
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)
        advance = session.refresh if change == 'refresh' else lambda: setattr(workspace, 'epoch', 1)

        def change_during_transaction(_expr: SkillCode) -> list[dict[str, object]]:
            advance()
            return [self._payload('R1', 1.0)]

        workspace.transaction.side_effect = change_during_transaction
        results: list[CmdResult[ComponentInfo]] = []

        def execute() -> None:
            with session.batch() as batch:
                results.append(batch.call(session.components.move, 'R1', x=1.0, y=2.0))

        with pytest.raises(RecordIDError, match=r'Batch.*stale') as raised:
            execute()

        workspace.transaction.assert_called_once()
        with pytest.raises(RecordIDError) as result_error:
            _ = results[0].value
        assert result_error.value is raised.value

    def test_context_error_cancels_results_without_sending(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        session = _session(workspace)
        error = ValueError('body')
        results: list[CmdResult[object]] = []

        def cancel() -> None:
            with session.batch() as batch:
                results.append(batch.call(session.components.move, 'R1', x=1.0, y=2.0))
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
        workspace.__getitem__.return_value.expr.return_value = Expr.raw_skill('move1()')
        workspace.transaction.return_value = payload
        session = _session(workspace)
        results: list[CmdResult[object]] = []

        def execute() -> None:
            with session.batch() as batch:
                results.append(batch.call(session.components.move, 'R1', x=1.0, y=2.0))

        with pytest.raises(AllegroProtocolError, match='batch'):
            execute()

        with pytest.raises(AllegroProtocolError, match='batch'):
            _ = results[0].value

    def test_validation_finishes_before_any_result_is_resolved(self) -> None:
        workspace = MagicMock()
        workspace.__getitem__.return_value.expr.side_effect = [
            Expr.raw_skill('move1()'),
            Expr.raw_skill('move2()'),
        ]
        workspace.transaction.return_value = [self._payload('R1', 1.0), None]
        session = _session(workspace)
        results: list[CmdResult[object]] = []

        def execute() -> None:
            with session.batch() as batch:
                results.extend([
                    batch.call(session.components.move, 'R1', x=1.0, y=2.0),
                    batch.call(session.components.move, 'R2', x=2.0, y=2.0),
                ])

        with pytest.raises(AllegroProtocolError, match='__abMoveComponent'):
            execute()
        for result in results:
            with pytest.raises(AllegroProtocolError, match='__abMoveComponent'):
                _ = result.value

    def test_batch_is_single_use_and_add_requires_active_context(self) -> None:
        session = _session()
        batch = session.batch()

        with pytest.raises(RuntimeError, match='active'):
            batch.add(Mock(spec=Cmd))
        with batch:
            pass
        with pytest.raises(RuntimeError, match='active'):
            batch.add(Mock(spec=Cmd))
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
    assert issubclass(RecordIDError, (AllegroError, ValueError))
