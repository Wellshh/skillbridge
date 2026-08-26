from __future__ import annotations

import sys
from collections.abc import Iterator
from json import dumps
from pathlib import Path
from shutil import copy2, copytree
from socket import socket
from sys import platform
from tempfile import TemporaryDirectory
from time import sleep
from typing import NewType

import pytest
from pydantic import ValidationError

import allegrobridge.client.api.extensions as extension_package
import allegrobridge.server
from allegrobridge import Allegro, OpenMode, Session, Workspace
from allegrobridge.client.api import (
    BoardInfo,
    ComponentInfo,
    LayerInfo,
    NetInfo,
    PadstackInfo,
    PinInfo,
)
from allegrobridge.exceptions import AllegroProtocolError, ExtensionError
from allegrobridge.util import ASSETS_DIR
from skillbridge import SkillCode

ALObjectHandle = NewType('ALObjectHandle', str)
_TEST_BOARD = ASSETS_DIR / 'shape1.brd'


@pytest.fixture(scope='module')
def workspace_id() -> str | None:
    if platform != 'win32':
        return None
    with socket() as listener:
        listener.bind(('localhost', 0))
        return str(listener.getsockname()[1])


@pytest.fixture(scope='class')
def allegro(
    tmp_path_factory: pytest.TempPathFactory,
    workspace_id: str | None,
) -> Iterator[Allegro]:
    mode: OpenMode = 'cli' if platform == 'win32' else 'manual'
    board = None
    if mode == 'cli':
        board = Path(copy2(_TEST_BOARD, tmp_path_factory.mktemp('allegro')))

    with Allegro.open(mode=mode, board=board, workspace_id=workspace_id) as opened:
        yield opened


@pytest.fixture(scope='class')
def ws(allegro: Allegro) -> Workspace:
    return allegro.workspace


@pytest.fixture(scope='class')
def session(allegro: Allegro) -> Session:
    return allegro.session


@pytest.fixture(scope='class')
def extension_environment(session: Session) -> Iterator[None]:
    fixture_root = Path(__file__).with_name('fixtures')
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            extension_package,
            '__path__',
            [str(fixture_root / 'client_extensions')],
        )
        monkeypatch.setattr(
            allegrobridge.server,
            '__file__',
            str(fixture_root / 'server' / '__init__.py'),
        )
        sys.modules.pop('allegrobridge.client.api.extensions.probe', None)
        sys.modules.pop('allegrobridge.client.api.extensions.missing_server', None)
        try:
            yield
        finally:
            sys.modules.pop('allegrobridge.client.api.extensions.probe', None)
            sys.modules.pop('allegrobridge.client.api.extensions.missing_server', None)


@pytest.fixture(scope='class')
def design(ws: Workspace) -> object:
    design = ws['axlDBGetDesign']()
    return ws['axlDBRefreshId'](design)


def _board_counts(ws: Workspace) -> list[int]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign)))) '
        '(list (length design->components) (length design->symbols) (length design->nets)))'
    )


def _component_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach component design->components '
        '(setq result (cons (list component->name (not (null component->symbol))) result))) '
        '(reverse result))'
    )


def _layer_snapshot(ws: Workspace, etch_only: bool = False) -> list[list[object]]:
    return ws['evalstring'](
        "(let (result) "
        "(foreach className (axlClasses) "
        f"(when (or {'t' if not etch_only else 'nil'} (equal className \"ETCH\")) "
        "(foreach subclass (axlSubclasses className) "
        '(letseq ((name (strcat className "/" subclass)) '
        "(layer (axlLayerGet name))) "
        "(setq result (cons (list name className subclass layer->number) "
        "result)))))) (reverse result))"
    )


def _net_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach net design->nets '
        '(setq result '
        '(cons (list net->name net->nBranches net->unconnected net->unplaced) result))) '
        '(reverse result))'
    )


def _pin_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach component design->components '
        '(foreach pin component->pins '
        '(letseq ((symbol component->symbol) (netObject pin->net) '
        '(netName (when (and netObject (not (stringp netObject)) '
        '(not (equal netObject->name ""))) netObject->name)) '
        '(span (when symbol pin->startEnd))) '
        '(setq result (cons '
        '(list component->name pin->number netName pin->name '
        '(if symbol then "placed" else "unplaced") '
        '(when symbol (car pin->xy)) (when symbol (cadr pin->xy)) '
        '(when symbol pin->rotation) (when span (car span)) (when span (cadr span))) '
        'result))))) (reverse result))'
    )


def _padstack_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach padstack design->padstacks '
        '(let ((span padstack->startEnd)) '
        '(setq result (cons '
        '(list padstack->name padstack->type padstack->usage '
        '(when span (car span)) (when span (cadr span))) result)))) '
        '(reverse result))'
    )


def _run_skill_suite(workspace_id: str | None) -> str:
    if platform != 'win32':
        pytest.skip('automatic SKILL suite launch requires Windows Allegro')

    repository = Path(__file__).parents[2]
    with TemporaryDirectory(prefix='allegrobridge-skill-') as temporary_directory:
        temporary_repository = Path(temporary_directory)
        skill_tests = copytree(
            repository / 'tests' / 'skill', temporary_repository / 'tests' / 'skill'
        )
        for source in (
            repository / 'skillbridge' / '__init__.py',
            repository / 'skillbridge' / 'server' / 'python_server.il',
            repository / 'allegrobridge' / 'server' / 'allegro_server.il',
            _TEST_BOARD,
        ):
            destination = temporary_repository / source.relative_to(repository)
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(source, destination)

        run_file = (skill_tests / 'run.ils').resolve().as_posix()
        skill_code = f"""
            let((capturePort failure loadResult report)
                capturePort = outstring()
                unwindProtect(
                    let(((poport capturePort))
                        loadResult = errset(load({dumps(run_file)}))
                        unless(loadResult failure = errset.errset)
                        report = getOutstring(capturePort)
                    )
                    close(capturePort)
                )
                list(loadResult failure report)
            )
        """.replace('\n', ' ')

        with Allegro.open(mode='cli', workspace_id=workspace_id) as opened:
            result = opened.workspace['evalstring'](skill_code)

    assert isinstance(result, list)
    load_result, failure, report = result
    assert isinstance(report, str)
    assert load_result, f'{failure}\n{report}'
    return report


class TestApi:
    def test_session_uses_opened_workspace(
        self,
        allegro: Allegro,
        ws: Workspace,
    ) -> None:
        session = allegro.session

        assert isinstance(session, Session)
        assert session.raw is ws
        assert session.generation == 1
        assert session.raw['plus'](1, 2) == 3

    def test_transaction_extension_commits_and_rolls_back(self, ws: Workspace) -> None:
        assert ws.transaction(SkillCode('42')) == 42
        with pytest.raises(RuntimeError, match='TRANSACTION_COMMAND_FAILED'):
            ws.transaction(SkillCode('error("integration-rollback")'))
        assert ws['plus'](1, 2) == 3

    def test_savepoint_batch_and_dry_run_database_semantics(
        self,
        allegro: Allegro,
        ws: Workspace,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('database transaction test requires the Windows board copy')

        get_nets = 'progn(axlDBRefreshId(axlDBGetDesign()) length(axlDBGetDesign()->nets))'
        snapshot = (
            f'list(nil \'nets {get_nets} '
            "'components length(axlDBGetDesign()->components) "
            "'symbols length(axlDBGetDesign()->symbols))"
        )
        original_snapshot = ws['evalstring'](snapshot)

        try:
            success_command = f'progn(axlDBCreateNet("ITEST_TXN_SUCCESS") {get_nets})'
            failed_command = 'progn(axlDBCreateNet("ITEST_TXN_FAIL") error("savepoint-item"))'
            results = ws.transaction.batch([
                SkillCode(success_command),
                SkillCode(failed_command),
            ])
            persisted = ws['evalstring'](snapshot)

            assert results[0] == {
                'index': 0,
                'status': 'success',
                'value': persisted['nets'],
            }
            assert results[1]['index'] == 1
            assert results[1]['status'] == 'failure'
            assert 'SAVEPOINT_COMMAND_FAILED' in results[1]['error']

            with pytest.raises(RuntimeError, match='TRANSACTION_COMMAND_FAILED'):
                ws.transaction(
                    SkillCode('progn(axlDBCreateNet("ITEST_TXN_ATOMIC") error("atomic-item"))')
                )
            assert ws['evalstring'](snapshot) == persisted

            preview = ws.transaction.preview(
                SkillCode(f'progn(axlDBCreateNet("ITEST_TXN_PREVIEW") {snapshot})')
            )
            assert preview.keys() == {'nets', 'components', 'symbols'}
            assert isinstance(preview['nets'], int)
            assert preview['nets'] != persisted['nets']
            assert preview['components'] == persisted['components']
            assert preview['symbols'] == persisted['symbols']
            assert ws['evalstring'](snapshot) == persisted
            assert ws['plus'](1, 2) == 3
        finally:
            ws.transaction(
                SkillCode(
                    'progn(axlDeleteObject(axlDBCreateNet("ITEST_TXN_SUCCESS")) '
                    'axlDBRefreshId(axlDBGetDesign()))'
                )
            )
        assert ws['evalstring'](snapshot) == original_snapshot


class TestBoardApi:
    def test_default_call_returns_board_info(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        board = session.board()
        component_count, symbol_count, net_count = _board_counts(ws)

        assert isinstance(board, BoardInfo)
        assert board.path.endswith('.brd')
        assert board.units
        assert board.component_count == component_count
        assert board.symbol_count == symbol_count
        assert board.net_count == net_count
        assert board.session_generation == session.generation

    def test_board_info_is_frozen(self, session: Session) -> None:
        board = session.board()

        with pytest.raises(ValidationError, match='frozen'):
            board.path = 'changed.brd'

    @pytest.mark.parametrize(
        'payload',
        [
            {
                'units': 'mils',
                'component_count': 1,
                'symbol_count': 1,
                'net_count': 1,
            },
            {
                'path': 'shape1.brd',
                'units': 'mils',
                'component_count': 1,
                'symbol_count': 1,
                'net_count': 1,
                'dbid': 'db:1',
            },
            {
                'path': 'shape1.brd',
                'units': 'mils',
                'component_count': '1',
                'symbol_count': 1,
                'net_count': 1,
            },
        ],
        ids=['missing-field', 'extra-field', 'wrong-type'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: dict[str, object],
        session: Session,
    ) -> None:
        monkeypatch.setattr(session.raw._channel, 'send', lambda _: repr(payload))

        with pytest.raises(AllegroProtocolError, match='__abProjectBoard'):
            session.board()


class TestLayersApi:
    @pytest.mark.parametrize('etch_only', [False, True])
    def test_call_projects_layers(
        self,
        session: Session,
        ws: Workspace,
        etch_only: bool,
    ) -> None:
        layers = session.layers(etch_only=etch_only)
        snapshot = _layer_snapshot(ws, etch_only)

        assert all(isinstance(layer, LayerInfo) for layer in layers)
        assert [
            (layer.name, layer.class_name, layer.subclass, layer.number) for layer in layers
        ] == [tuple(item) for item in snapshot]
        assert all(layer.session_generation == session.generation for layer in layers)
        if etch_only:
            assert all(layer.class_name == 'ETCH' for layer in layers)

    def test_getitem_returns_layer_by_qualified_name(self, session: Session) -> None:
        expected = session.layers(etch_only=True)[0]

        assert session.layers[expected.name] == expected

    def test_getitem_raises_key_error_when_name_is_missing(self, session: Session) -> None:
        with pytest.raises(KeyError, match='__MISSING_LAYER__'):
            _ = session.layers['ETCH/__MISSING_LAYER__']

    def test_layer_info_is_frozen(self, session: Session) -> None:
        layer = session.layers()[0]

        with pytest.raises(ValidationError, match='frozen'):
            layer.name = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [{'class_name': 'ETCH', 'subclass': 'TOP', 'number': 1}],
            [
                {
                    'name': 'ETCH/TOP',
                    'class_name': 'ETCH',
                    'subclass': 'TOP',
                    'number': 1,
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'name': 'ETCH/TOP',
                    'class_name': 'ETCH',
                    'subclass': 'TOP',
                    'number': '1',
                }
            ],
        ],
        ids=['missing-field', 'extra-field', 'wrong-type'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        monkeypatch.setattr(session.raw._channel, 'send', lambda _: repr(payload))

        with pytest.raises(AllegroProtocolError, match='__abProjectLayers'):
            session.layers()


class TestComponentsApi:
    def test_default_call_projects_all_components(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        components = session.components()
        snapshot = _component_snapshot(ws)

        assert all(isinstance(component, ComponentInfo) for component in components)
        assert [component.refdes for component in components] == [item[0] for item in snapshot]
        assert all(component.session_generation == session.generation for component in components)

    def test_call_can_exclude_unplaced_components(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        components = session.components(include_unplaced=False)
        snapshot = _component_snapshot(ws)

        assert [component.refdes for component in components] == [
            item[0] for item in snapshot if item[1]
        ]
        assert all(component.placement == 'placed' for component in components)

    def test_getitem_returns_component_by_refdes(self, session: Session) -> None:
        expected = session.components()[0]

        assert session.components[expected.refdes] == expected

    def test_getitem_raises_key_error_when_refdes_is_missing(self, session: Session) -> None:
        with pytest.raises(KeyError, match='__MISSING_COMPONENT__'):
            _ = session.components['__MISSING_COMPONENT__']

    def test_move_projects_updated_component(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('component move test requires the Windows board copy')

        original = session.components(include_unplaced=False)[0]
        assert original.x is not None
        assert original.y is not None
        assert original.rotation is not None
        target_x = original.x + 1.0
        target_y = original.y + 1.0
        target_rotation = original.rotation + 15.0

        try:
            moved = session.components.move(
                original.refdes,
                x=target_x,
                y=target_y,
                rotation=target_rotation,
            )
            assert moved.refdes == original.refdes
            assert moved.placement == 'placed'
            assert moved.x == pytest.approx(target_x)
            assert moved.y == pytest.approx(target_y)
            assert moved.rotation == pytest.approx(target_rotation)
        finally:
            session.components.move(
                original.refdes,
                x=original.x,
                y=original.y,
                rotation=original.rotation,
            )

    def test_move_raises_for_missing_component(self, allegro: Allegro, session: Session) -> None:
        if allegro.mode != 'cli':
            pytest.skip('component move test requires the Windows board copy')

        with pytest.raises(RuntimeError, match='COMPONENT_NOT_FOUND'):
            session.components.move('__MISSING_COMPONENT__', x=1.0, y=2.0)

    def test_move_preview_returns_projection_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('component move test requires the Windows board copy')

        original = session.components(include_unplaced=False)[0]
        assert original.x is not None
        assert original.y is not None

        preview = session.components.move.preview(
            original.refdes,
            x=original.x + 1.0,
            y=original.y + 1.0,
        )

        assert preview.x == pytest.approx(original.x + 1.0)
        assert preview.y == pytest.approx(original.y + 1.0)
        assert session.components[original.refdes] == original

    def test_atomic_batch_commits_in_order(self, allegro: Allegro, session: Session) -> None:
        if allegro.mode != 'cli':
            pytest.skip('component batch test requires the Windows board copy')

        originals = session.components(include_unplaced=False)[:2]
        assert len(originals) == 2
        assert all(component.x is not None and component.y is not None for component in originals)

        try:
            with session.batch('move two components') as batch:
                results = [
                    batch.add(
                        session.components.move.command(
                            component.refdes,
                            x=component.x + index + 1.0,
                            y=component.y + index + 1.0,
                        )
                    )
                    for index, component in enumerate(originals)
                ]

            assert [result.value.refdes for result in results] == [
                component.refdes for component in originals
            ]
            assert [session.components[item.refdes].x for item in originals] == [
                result.value.x for result in results
            ]
        finally:
            for component in originals:
                session.components.move(
                    component.refdes,
                    x=component.x,
                    y=component.y,
                    rotation=component.rotation,
                )

    def test_atomic_batch_failure_rolls_back_all(self, allegro: Allegro, session: Session) -> None:
        if allegro.mode != 'cli':
            pytest.skip('component batch test requires the Windows board copy')

        original = session.components(include_unplaced=False)[0]
        assert original.x is not None
        assert original.y is not None
        results = []

        def execute() -> None:
            with session.batch() as batch:
                results.extend([
                    batch.add(
                        session.components.move.command(
                            original.refdes,
                            x=original.x + 1.0,
                            y=original.y + 1.0,
                        )
                    ),
                    batch.add(
                        session.components.move.command('__MISSING_COMPONENT__', x=1.0, y=2.0)
                    ),
                ])

        with pytest.raises(RuntimeError, match='COMPONENT_NOT_FOUND'):
            execute()

        moved, missing = results

        assert session.components[original.refdes] == original
        with pytest.raises(RuntimeError, match='COMPONENT_NOT_FOUND'):
            _ = moved.value
        with pytest.raises(RuntimeError, match='COMPONENT_NOT_FOUND'):
            _ = missing.value

    def test_dry_run_batch_returns_results_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('component batch test requires the Windows board copy')

        original = session.components(include_unplaced=False)[0]
        assert original.x is not None
        assert original.y is not None

        with session.batch('preview move', dry_run=True) as batch:
            result = batch.add(
                session.components.move.command(
                    original.refdes,
                    x=original.x + 1.0,
                    y=original.y + 1.0,
                )
            )

        assert result.value.x == pytest.approx(original.x + 1.0)
        assert session.components[original.refdes] == original

    def test_component_info_is_frozen(self, session: Session) -> None:
        component = session.components()[0]

        with pytest.raises(ValidationError, match='frozen'):
            component.refdes = 'changed'

    def test_empty_projection_returns_empty_list(
        self,
        monkeypatch: pytest.MonkeyPatch,
        session: Session,
    ) -> None:
        commands: list[str] = []

        def send(command: str) -> str:
            commands.append(command)
            return 'None'

        monkeypatch.setattr(session.raw._channel, 'send', send)

        assert session.components() == []
        assert commands == ['__abProjectComponents(nil t )']

    def test_move_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        session: Session,
    ) -> None:
        commands: list[str] = []

        def send(command: str) -> str:
            commands.append(command)
            return repr({'refdes': 'R1'})

        monkeypatch.setattr(session.raw._channel, 'send', send)

        with pytest.raises(AllegroProtocolError, match='__abMoveComponent'):
            session.components.move('R1', x=1.0, y=2.0)
        assert commands == ['__abRunTransaction("__abMoveComponent(\\"R1\\" 1.0 2.0 nil )" )']

    @pytest.mark.parametrize(
        'payload',
        [
            [
                {
                    'device_type': 'RESISTOR',
                    'package': 'RES_0402',
                    'component_class': 'DISCRETE',
                    'placement': 'placed',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                }
            ],
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
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'refdes': 'R1',
                    'device_type': 'RESISTOR',
                    'package': 'RES_0402',
                    'component_class': 'DISCRETE',
                    'placement': 'placed',
                    'x': '1.0',
                    'y': 2.0,
                    'rotation': 0.0,
                }
            ],
            [42],
            {'refdes': 'R1'},
        ],
        ids=['missing-field', 'extra-field', 'wrong-type', 'non-record', 'wrong-container'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        commands: list[str] = []

        def send(command: str) -> str:
            commands.append(command)
            return repr(payload)

        monkeypatch.setattr(session.raw._channel, 'send', send)

        with pytest.raises(AllegroProtocolError, match='__abProjectComponents'):
            session.components()
        assert commands == ['__abProjectComponents(nil t )']


class TestNetsApi:
    def test_default_call_projects_design_nets(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        nets = session.nets()
        snapshot = _net_snapshot(ws)

        assert all(isinstance(net, NetInfo) for net in nets)
        assert [net.name for net in nets] == [item[0] for item in snapshot]
        assert [
            (net.branch_count, net.unconnected_count, net.unplaced_pin_count) for net in nets
        ] == [tuple(item[1:]) for item in snapshot]
        assert all(net.session_generation == session.generation for net in nets)

    def test_getitem_returns_net_by_name(self, session: Session) -> None:
        expected = session.nets()[0]

        assert session.nets[expected.name] == expected

    def test_getitem_raises_key_error_when_name_is_missing(self, session: Session) -> None:
        with pytest.raises(KeyError, match='__MISSING_NET__'):
            _ = session.nets['__MISSING_NET__']

    def test_net_info_is_frozen(self, session: Session) -> None:
        net = session.nets()[0]

        with pytest.raises(ValidationError, match='frozen'):
            net.name = 'changed'

    def test_empty_projection_returns_empty_list(
        self,
        monkeypatch: pytest.MonkeyPatch,
        session: Session,
    ) -> None:
        commands: list[str] = []

        def send(command: str) -> str:
            commands.append(command)
            return 'None'

        monkeypatch.setattr(session.raw._channel, 'send', send)

        assert session.nets() == []
        assert commands == ['__abProjectNets(nil )']

    @pytest.mark.parametrize(
        'payload',
        [
            [
                {
                    'branch_count': 1,
                    'unconnected_count': 0,
                    'unplaced_pin_count': 0,
                }
            ],
            [
                {
                    'name': 'GND',
                    'branch_count': 1,
                    'unconnected_count': 0,
                    'unplaced_pin_count': 0,
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'name': 'GND',
                    'branch_count': '1',
                    'unconnected_count': 0,
                    'unplaced_pin_count': 0,
                }
            ],
            [42],
            {'name': 'GND'},
        ],
        ids=['missing-field', 'extra-field', 'wrong-type', 'non-record', 'wrong-container'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        commands: list[str] = []

        def send(command: str) -> str:
            commands.append(command)
            return repr(payload)

        monkeypatch.setattr(session.raw._channel, 'send', send)

        with pytest.raises(AllegroProtocolError, match='__abProjectNets'):
            session.nets()
        assert commands == ['__abProjectNets(nil )']


class TestPinsApi:
    def test_default_call_projects_component_pins(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        pins = session.pins()

        assert all(isinstance(pin, PinInfo) for pin in pins)
        assert [
            (
                pin.refdes,
                pin.number,
                pin.net,
                pin.padstack,
                pin.placement,
                pin.x,
                pin.y,
                pin.rotation,
                pin.start_layer,
                pin.end_layer,
            )
            for pin in pins
        ] == [tuple(item) for item in _pin_snapshot(ws)]
        assert all(pin.session_generation == session.generation for pin in pins)

    def test_call_filters_by_component_and_net(self, session: Session) -> None:
        expected = next(pin for pin in session.pins() if pin.net is not None)

        pins = session.pins(component=expected.refdes, net=expected.net)

        assert expected in pins
        assert all(pin.refdes == expected.refdes and pin.net == expected.net for pin in pins)

    def test_getitem_returns_pin_by_stable_key(self, session: Session) -> None:
        expected = session.pins()[0]

        assert session.pins[expected.refdes, expected.number] == expected

    def test_getitem_raises_key_error_when_pin_is_missing(self, session: Session) -> None:
        with pytest.raises(KeyError, match='__MISSING_PIN__'):
            _ = session.pins['U1', '__MISSING_PIN__']

    def test_pin_info_is_frozen(self, session: Session) -> None:
        pin = session.pins()[0]

        with pytest.raises(ValidationError, match='frozen'):
            pin.number = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [
                {
                    'number': '1',
                    'net': 'GND',
                    'padstack': 'PAD',
                    'placement': 'placed',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                    'start_layer': 'ETCH/TOP',
                    'end_layer': 'ETCH/BOTTOM',
                }
            ],
            [
                {
                    'refdes': 'U1',
                    'number': '1',
                    'net': 'GND',
                    'padstack': 'PAD',
                    'placement': 'placed',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                    'start_layer': 'ETCH/TOP',
                    'end_layer': 'ETCH/BOTTOM',
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'refdes': 'U1',
                    'number': 1,
                    'net': 'GND',
                    'padstack': 'PAD',
                    'placement': 'placed',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                    'start_layer': 'ETCH/TOP',
                    'end_layer': 'ETCH/BOTTOM',
                }
            ],
        ],
        ids=['missing-field', 'extra-field', 'wrong-type'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        monkeypatch.setattr(session.raw._channel, 'send', lambda _: repr(payload))

        with pytest.raises(AllegroProtocolError, match='__abProjectPins'):
            session.pins()


class TestPadstacksApi:
    def test_default_call_projects_padstacks(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        padstacks = session.padstacks()

        assert all(isinstance(padstack, PadstackInfo) for padstack in padstacks)
        assert [
            (
                padstack.name,
                padstack.type,
                padstack.usage,
                padstack.start_layer,
                padstack.end_layer,
            )
            for padstack in padstacks
        ] == [tuple(item) for item in _padstack_snapshot(ws)]
        assert all(
            padstack.session_generation == session.generation for padstack in padstacks
        )

    def test_getitem_returns_padstack_by_name(self, session: Session) -> None:
        expected = session.padstacks()[0]

        assert session.padstacks[expected.name] == expected

    def test_getitem_raises_key_error_when_name_is_missing(self, session: Session) -> None:
        with pytest.raises(KeyError, match='__MISSING_PADSTACK__'):
            _ = session.padstacks['__MISSING_PADSTACK__']

    def test_padstack_info_is_frozen(self, session: Session) -> None:
        padstack = session.padstacks()[0]

        with pytest.raises(ValidationError, match='frozen'):
            padstack.name = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [
                {
                    'type': 'through',
                    'usage': 'through_via',
                    'start_layer': 'TOP',
                    'end_layer': 'BOTTOM',
                }
            ],
            [
                {
                    'name': 'VIA12',
                    'type': 'through',
                    'usage': 'through_via',
                    'start_layer': 'TOP',
                    'end_layer': 'BOTTOM',
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'name': 'VIA12',
                    'type': 1,
                    'usage': 'through_via',
                    'start_layer': 'TOP',
                    'end_layer': 'BOTTOM',
                }
            ],
        ],
        ids=['missing-field', 'extra-field', 'wrong-type'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        monkeypatch.setattr(session.raw._channel, 'send', lambda _: repr(payload))

        with pytest.raises(AllegroProtocolError, match='__abProjectPadstacks'):
            session.padstacks()


@pytest.mark.usefixtures('extension_environment')
class TestExtensionApi:
    def test_missing_extension_is_cached_and_core_api_survives(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('extension loading test requires the Windows board copy')

        with pytest.raises(ExtensionError, match='missing_server') as first:
            _ = session.ext.missing_server
        with pytest.raises(ExtensionError, match='missing_server') as second:
            _ = session.ext.missing_server

        assert second.value is first.value
        assert session.raw['plus'](1, 2) == 3
        assert session.board().session_generation == session.generation
        assert isinstance(session.components(), list)
        assert isinstance(session.nets(), list)
        assert session.raw.transaction(SkillCode('42')) == 42

    def test_extension_read_loads_and_returns_strict_records(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('extension loading test requires the Windows board copy')

        probe = session.ext.probe

        assert probe is session.ext['probe']
        assert probe() == session.components()

    def test_extension_write_commits_atomically(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('extension write test requires the Windows board copy')

        original = session.components(include_unplaced=False)[0]
        assert original.x is not None
        assert original.y is not None

        try:
            moved = session.ext.probe.move(
                original.refdes,
                x=original.x + 1.0,
                y=original.y + 1.0,
            )
            assert moved.x == pytest.approx(original.x + 1.0)
            assert moved.y == pytest.approx(original.y + 1.0)
            assert session.components[original.refdes] == moved
        finally:
            session.components.move(
                original.refdes,
                x=original.x,
                y=original.y,
                rotation=original.rotation,
            )

    def test_extension_command_mixes_with_core_atomic_batch(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        if allegro.mode != 'cli':
            pytest.skip('extension batch test requires the Windows board copy')

        originals = session.components(include_unplaced=False)[:2]
        assert len(originals) == 2
        assert all(component.x is not None and component.y is not None for component in originals)

        try:
            with session.batch('mixed extension batch') as batch:
                extension_result = batch.add(
                    session.ext.probe.move.command(
                        originals[0].refdes,
                        x=originals[0].x + 1.0,
                        y=originals[0].y + 1.0,
                    )
                )
                core_result = batch.add(
                    session.components.move.command(
                        originals[1].refdes,
                        x=originals[1].x + 2.0,
                        y=originals[1].y + 2.0,
                    )
                )

            assert [extension_result.value.refdes, core_result.value.refdes] == [
                component.refdes for component in originals
            ]
        finally:
            for component in originals:
                session.components.move(
                    component.refdes,
                    x=component.x,
                    y=component.y,
                    rotation=component.rotation,
                )


class TestSkill:
    def test_run_skill_suite_returns_report_to_python(self, workspace_id: str | None) -> None:
        report = _run_skill_suite(workspace_id)

        assert '0 failed, 0 skipped, 0 xfailed ===' in report
        assert 'branches covered (100.00%)' in report


# POC tests
class TestBasicOp:
    _IDLE_SECONDS = 5

    _design: object

    @pytest.fixture(autouse=True)
    def _inject(self, design: object) -> None:
        self._design = design

    def _single_ping_test(self, obj_workspace: Workspace) -> bool:
        return obj_workspace['plus'](1, 2) == 3

    def _basic_oop(self, attr: ALObjectHandle, length: int | None = None) -> None:
        obj = getattr(self._design, attr, None)

        assert obj is not None, f'No board is open: the design has no {attr} database.'
        if length is not None:
            assert len(obj) >= length, (
                f'The number of {attr} in this design should be at least {length}'
            )

    def test_can_get_components(self) -> None:
        self._basic_oop('components', 1)

    def test_workspace_detects_allegro(self, ws: Workspace) -> None:
        assert type(ws) is Workspace

    def test_allegro_window_matches_platform(
        self,
        allegro: Allegro,
        ws: Workspace,
    ) -> None:
        expected_mode: OpenMode = 'cli' if platform == 'win32' else 'manual'
        assert allegro.mode == expected_mode
        assert allegro.workspace is ws
        assert (allegro.board is not None) is (expected_mode == 'cli')

    def test_can_get_nets(self) -> None:
        self._basic_oop('nets', 1)

    def test_ping(self, ws: Workspace) -> None:
        for i in range(1_000):
            assert ws['plus'](i, 0) == i

    def test_geo_rotate_pt(self, ws: Workspace) -> None:
        rotated = ws.geo.rotate_pt(90.0, [100.0, 0.0], None)
        assert rotated == pytest.approx([0.0, 100.0])

    def test_callback_keeps_working_while_idle(self, ws: Workspace) -> None:
        assert self._single_ping_test(ws)
        sleep(TestBasicOp._IDLE_SECONDS)
        assert self._single_ping_test(ws), 'Callback not available until next skill execution'

    def test_py_show_log_prints_latest_lines_and_closes_port(
        self,
        ws: Workspace,
        tmp_path: Path,
    ) -> None:
        log_path = tmp_path / 'skillbridge_py_show_log_test.log'
        log_lines = [f'log-entry-{index}\n' for index in range(5)]
        log_path.write_text(''.join(log_lines), encoding='utf-8')

        def capture_py_show_log(requested_length: int) -> str:
            skill_code = f"""
                let((capturePort oldLogName output)
                    oldLogName = pyShowLog.logName
                    capturePort = outstring()
                    unwindProtect(
                        {{
                            pyShowLog.logName = {dumps(log_path.as_posix())}
                            let(((poport capturePort))
                                pyShowLog({requested_length})
                            )
                            output = getOutstring(capturePort)
                        }}
                        {{
                            pyShowLog.logName = oldLogName
                            close(capturePort)
                        }}
                    )
                    output
                )
            """.replace('\n', ' ')
            output = ws['evalstring'](skill_code)
            assert isinstance(output, str)
            return output

        latest_lines = capture_py_show_log(3)
        more_lines_than_available = capture_py_show_log(len(log_lines) + 3)

        try:
            log_path.unlink()
        except OSError as error:
            pytest.fail(f'pyShowLog left its input port open: {error}', pytrace=False)

        assert latest_lines == ''.join(log_lines[-3:])
        assert more_lines_than_available == ''.join(log_lines)
        assert 'unbound' not in more_lines_than_available.lower()
        assert not log_path.exists()

    def test_server_can_restart(self, ws: Workspace) -> None:
        try:
            assert self._single_ping_test(ws)
            assert ws['pyRestartServer']() is True

        finally:
            ws.close()

        new_ws = None
        for _ in range(40):
            try:
                candidate = Workspace.open(ws.id)
                if type(candidate) is Workspace and self._single_ping_test(candidate):
                    new_ws = candidate
                    break
                candidate.close()
            except (OSError, RuntimeError, ConnectionResetError):
                sleep(0.5)
                continue
        assert new_ws is not None, 'server did not come back as an Allegro workspace after restart'
        try:
            assert self._single_ping_test(new_ws)
        finally:
            new_ws.close()
