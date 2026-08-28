# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import suppress
from json import dumps
from pathlib import Path
from shutil import copy2, copytree
from socket import socket
from sys import platform
from tempfile import TemporaryDirectory
from time import sleep
from typing import Any, NewType, cast
from weakref import ref

import pytest
from pydantic import ValidationError

import allegrobridge.client.api.extensions as extension_package
import allegrobridge.server
from allegrobridge import Allegro, OpenMode, Session, Workspace
from allegrobridge.client.api import (
    BBox,
    BoardInfo,
    CmdResult,
    ComponentInfo,
    ComponentRef,
    DrcInfo,
    LayerInfo,
    NetInfo,
    NetRef,
    PadstackInfo,
    PinInfo,
    PinRef,
    Point,
    RouteInfo,
    ShapeInfo,
    SymbolInfo,
    ViaInfo,
)
from allegrobridge.client.base._record import _ID  # ruff: ignore[import-private-name]
from allegrobridge.exceptions import (
    AllegroProtocolError,
    ExtensionError,
    RecordIDError,
)
from allegrobridge.util import ASSETS_DIR
from skillbridge import SkillCode

ALObjectHandle = NewType('ALObjectHandle', str)
_TEST_BOARD = ASSETS_DIR / 'shape1.brd'


def _session_id(session: Session) -> _ID:
    return _ID(ref(session), session.generation)


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


def _symbol_snapshot(ws: Workspace, type_: str | None = None) -> list[list[object]]:
    encoded_type = 'nil' if type_ is None else dumps(type_)
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach symbol design->symbols '
        f'(when (or (null {encoded_type}) (equal {encoded_type} symbol->type)) '
        '(setq result (cons '
        '(list symbol->name symbol->type symbol->refdes '
        '(car symbol->xy) (cadr symbol->xy) symbol->rotation) result)))) '
        '(reverse result))'
    )


def _via_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach netObject design->nets '
        '(foreach branch netObject->branches '
        '(foreach item branch->children '
        '(when (equal item->objType "via") '
        '(let ((span item->startEnd)) '
        '(setq result (cons '
        '(list item->name netObject->name (car item->xy) (cadr item->xy) '
        'item->rotation (if item->isMirrored then "mirrored" else "unmirrored") '
        '(car span) (cadr span) item->pads~>layer) result))))))) '
        '(foreach branch (axlDBGetLonelyBranches) '
        '(foreach item branch->children '
        '(when (equal item->objType "via") '
        '(let ((span item->startEnd)) '
        '(setq result (cons '
        '(list item->name nil (car item->xy) (cadr item->xy) '
        'item->rotation (if item->isMirrored then "mirrored" else "unmirrored") '
        '(car span) (cadr span) item->pads~>layer) result)))))) '
        '(reverse result))'
    )


def _route_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach netObject design->nets '
        '(foreach branch netObject->branches '
        '(foreach path branch->children '
        '(when (and (equal path->objType "path") path->isEtch) '
        '(foreach segment path->segments '
        '(when (equal segment->objType "line") '
        '(let ((ends segment->startEnd)) '
        '(setq result (cons '
        '(list netObject->name segment->layer '
        '(car (car ends)) (cadr (car ends)) '
        '(car (cadr ends)) (cadr (cadr ends)) segment->width) result))))))))) '
        '(foreach branch (axlDBGetLonelyBranches) '
        '(foreach path branch->children '
        '(when (and (equal path->objType "path") path->isEtch) '
        '(foreach segment path->segments '
        '(when (equal segment->objType "line") '
        '(let ((ends segment->startEnd)) '
        '(setq result (cons '
        '(list nil segment->layer '
        '(car (car ends)) (cadr (car ends)) '
        '(car (cadr ends)) (cadr (cadr ends)) segment->width) result)))))))) '
        '(reverse result))'
    )


def _shape_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(let (result) '
        '(foreach shape (axlDBGetShapes nil) '
        '(letseq ((netObject shape->net) '
        '(netName (when (and netObject (not (stringp netObject)) '
        '(not (equal netObject->name ""))) netObject->name)) '
        '(bbox shape->bBox)) '
        '(setq result (cons '
        '(list netName shape->layer '
        '(if shape->shapeIsBoundary then "dynamic" else "static") '
        '(car (car bbox)) (cadr (car bbox)) '
        '(car (cadr bbox)) (cadr (cadr bbox))) result)))) '
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
        copytree(
            repository / 'allegrobridge' / 'server' / 'extensions',
            temporary_repository / 'allegrobridge' / 'server' / 'extensions',
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
        assert board._id == _session_id(session)

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
        assert all(layer._id == _session_id(session) for layer in layers)
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
        assert all(component._id == _session_id(session) for component in components)

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

    def test_refresh_cancels_pending_batch_before_server(self, session: Session) -> None:
        component = next(component for component in session.components() if component.x is not None)

        def execute() -> None:
            with session.batch('stale batch') as batch:
                batch.add(
                    session.components.move.command(
                        component.refdes,
                        x=cast('float', component.x),
                        y=cast('float', component.y),
                        rotation=component.rotation,
                    )
                )
                session.refresh()

        with pytest.raises(RecordIDError, match=r'Batch.*stale'):
            execute()

        assert session.raw['plus'](1, 2) == 3

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
        assert commands == ['__abProjectComponents(nil t)']

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
        assert commands == ['__abRunTransaction("__abMoveComponent(\\"R1\\" 1.0 2.0 nil)")']

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
        assert commands == ['__abProjectComponents(nil t)']


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
        assert all(net._id == _session_id(session) for net in nets)

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
        assert commands == ['__abProjectNets(nil)']

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
        assert commands == ['__abProjectNets(nil)']


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
        assert all(pin._id == _session_id(session) for pin in pins)

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
        assert all(padstack._id == _session_id(session) for padstack in padstacks)

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


class TestSymbolsApi:
    def test_default_call_projects_symbols(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        symbols = session.symbols()

        assert all(isinstance(symbol, SymbolInfo) for symbol in symbols)
        assert [
            (symbol.name, symbol.type, symbol.refdes, symbol.x, symbol.y, symbol.rotation)
            for symbol in symbols
        ] == [tuple(item) for item in _symbol_snapshot(ws)]
        assert all(symbol._id == _session_id(session) for symbol in symbols)

    def test_type_filter_projects_only_matching_symbols(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        type_ = session.symbols()[0].type

        symbols = session.symbols(type=type_)

        assert symbols
        assert all(symbol.type == type_ for symbol in symbols)
        assert [
            (symbol.name, symbol.type, symbol.refdes, symbol.x, symbol.y, symbol.rotation)
            for symbol in symbols
        ] == [tuple(item) for item in _symbol_snapshot(ws, type_)]

    def test_unknown_type_returns_empty_collection(self, session: Session) -> None:
        assert session.symbols(type='__MISSING_SYMBOL_TYPE__') == []

    def test_symbol_info_is_frozen(self, session: Session) -> None:
        symbol = session.symbols()[0]

        with pytest.raises(ValidationError, match='frozen'):
            symbol.name = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [
                {
                    'type': 'PACKAGE',
                    'refdes': 'R1',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                }
            ],
            [
                {
                    'name': 'RES_0402',
                    'type': 'PACKAGE',
                    'refdes': 'R1',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'name': 'RES_0402',
                    'type': 'PACKAGE',
                    'refdes': 'R1',
                    'x': 'bad',
                    'y': 2.0,
                    'rotation': 0.0,
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

        with pytest.raises(AllegroProtocolError, match='__abProjectSymbols'):
            session.symbols()


class TestViasApi:
    @staticmethod
    def _require_writable(allegro: Allegro) -> None:
        if allegro.mode != 'cli':
            pytest.skip('via write test requires the Windows board copy')

    @staticmethod
    def _values(via: ViaInfo) -> tuple[object, ...]:
        return (
            via.padstack,
            via.net,
            via.x,
            via.y,
            via.rotation,
            via.mirroring,
            via.start_layer,
            via.end_layer,
        )

    def test_default_call_projects_vias(self, session: Session, ws: Workspace) -> None:
        vias = session.vias()
        snapshot = _via_snapshot(ws)

        assert vias
        assert all(isinstance(via, ViaInfo) for via in vias)
        assert [self._values(via) for via in vias] == [tuple(item[:8]) for item in snapshot]
        assert all(via._id == _session_id(session) for via in vias)

    def test_filters_match_single_rpc_snapshot(self, session: Session, ws: Workspace) -> None:
        snapshot = _via_snapshot(ws)
        expected = snapshot[0]
        padstack, net, _, _, _, _, start_layer, _, pad_layers = expected

        vias = session.vias(net=net, layer=start_layer, padstack=padstack)

        assert [self._values(via) for via in vias] == [
            tuple(item[:8])
            for item in snapshot
            if item[0] == padstack and (net is None or item[1] == net) and start_layer in item[8]
        ]
        assert start_layer in pad_layers

    def test_missing_filters_return_empty_collection(self, session: Session) -> None:
        assert session.vias(padstack='__MISSING_PADSTACK__') == []

    def test_create_commits_and_returns_projection(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        original = session.vias()[0]
        at = (original.x + 0.1, original.y + 0.1)

        created = session.vias.create(original.padstack, at=at, net=original.net)

        assert created.padstack == original.padstack
        assert created.net == original.net
        assert created.x == pytest.approx(at[0])
        assert created.y == pytest.approx(at[1])
        assert any(
            via.padstack == created.padstack
            and via.x == pytest.approx(created.x)
            and via.y == pytest.approx(created.y)
            for via in session.vias()
        )

    def test_create_preview_returns_projection_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        self._require_writable(allegro)
        original = session.vias()[0]
        before = _via_snapshot(ws)

        preview = session.vias.create.preview(
            original.padstack,
            at=(original.x + 0.2, original.y + 0.2),
            net=original.net,
            rotation=45.0,
            mirrored=True,
        )

        assert preview.rotation == pytest.approx(45.0)
        assert preview.mirroring == 'mirrored'
        assert _via_snapshot(ws) == before

    def test_atomic_batch_commits_in_order(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        original = session.vias()[0]
        before = len(session.vias())

        with session.batch('create two vias') as batch:
            first = batch.add(
                session.vias.create.command(
                    original.padstack,
                    at=(original.x + 0.3, original.y + 0.3),
                    net=original.net,
                )
            )
            second = batch.add(
                session.vias.create.command(
                    original.padstack,
                    at=(original.x + 0.4, original.y + 0.4),
                    net=original.net,
                )
            )

        assert first.value.x == pytest.approx(original.x + 0.3)
        assert second.value.x == pytest.approx(original.x + 0.4)
        assert len(session.vias()) == before + 2

    def test_atomic_batch_failure_rolls_back_all(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        self._require_writable(allegro)
        original = session.vias()[0]
        before = _via_snapshot(ws)

        def execute() -> None:
            with session.batch('rollback invalid via') as batch:
                batch.add(
                    session.vias.create.command(
                        original.padstack,
                        at=(original.x + 0.5, original.y + 0.5),
                        net=original.net,
                    )
                )
                batch.add(
                    session.vias.create.command(
                        '__MISSING_PADSTACK__',
                        at=(original.x + 0.6, original.y + 0.6),
                    )
                )

        with pytest.raises(RuntimeError):
            execute()

        assert _via_snapshot(ws) == before

    def test_dry_run_batch_returns_results_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        self._require_writable(allegro)
        original = session.vias()[0]
        before = _via_snapshot(ws)

        with session.batch('preview vias', dry_run=True) as batch:
            result = batch.add(
                session.vias.create.command(
                    original.padstack,
                    at=(original.x + 0.7, original.y + 0.7),
                    net=original.net,
                )
            )

        assert result.value.x == pytest.approx(original.x + 0.7)
        assert _via_snapshot(ws) == before

    def test_via_info_is_frozen(self, session: Session) -> None:
        via = session.vias()[0]

        with pytest.raises(ValidationError, match='frozen'):
            via.padstack = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [{'padstack': 'VIA12'}],
            [
                {
                    'padstack': 'VIA12',
                    'net': 'GND',
                    'x': 1.0,
                    'y': 2.0,
                    'rotation': 0.0,
                    'mirroring': 'unmirrored',
                    'start_layer': 'ETCH/TOP',
                    'end_layer': 'ETCH/BOTTOM',
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'padstack': 'VIA12',
                    'net': 'GND',
                    'x': 'bad',
                    'y': 2.0,
                    'rotation': 0.0,
                    'mirroring': 'unmirrored',
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

        with pytest.raises(AllegroProtocolError, match='__abProjectVias'):
            session.vias()


class TestRoutesApi:
    @staticmethod
    def _require_writable(allegro: Allegro) -> None:
        if allegro.mode != 'cli':
            pytest.skip('route write test requires the Windows board copy')

    @staticmethod
    def _values(route: RouteInfo) -> tuple[object, ...]:
        return (
            route.net,
            route.layer,
            route.start.x,
            route.start.y,
            route.end.x,
            route.end.y,
            route.width,
        )

    @staticmethod
    def _source(session: Session) -> tuple[RouteInfo, str]:
        route = next(route for route in session.routes() if route.net is not None)
        return route, cast('str', route.net)

    @staticmethod
    def _new_points(route: RouteInfo, direction: float = 1.0) -> list[tuple[float, float]]:
        distance = max(route.width * 4.0, 0.1)
        return [
            (route.end.x, route.end.y),
            (route.end.x + distance * direction, route.end.y),
        ]

    def test_default_call_projects_straight_routes(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        routes = session.routes()
        snapshot = _route_snapshot(ws)

        assert routes
        assert all(isinstance(route, RouteInfo) for route in routes)
        assert all(isinstance(route.start, Point) for route in routes)
        assert [self._values(route) for route in routes] == [tuple(item) for item in snapshot]
        assert all(route._id == _session_id(session) for route in routes)

    def test_filters_match_single_rpc_snapshot(self, session: Session, ws: Workspace) -> None:
        expected = _route_snapshot(ws)[0]
        net = cast('str | None', expected[0])
        layer = cast('str', expected[1])

        routes = session.routes(net=net, layer=layer)

        assert [self._values(route) for route in routes] == [
            tuple(item)
            for item in _route_snapshot(ws)
            if (net is None or item[0] == net) and item[1] == layer
        ]

    def test_missing_filters_return_empty_collection(self, session: Session) -> None:
        assert session.routes(net='__MISSING_NET__') == []
        assert session.routes(layer='__MISSING_LAYER__') == []

    def test_create_commits_and_returns_projections(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        source, net = self._source(session)

        created = session.routes.create(
            net,
            self._new_points(source),
            source.layer,
            source.width,
        )

        assert created
        assert all(isinstance(route, RouteInfo) for route in created)
        current = {self._values(route) for route in session.routes()}
        assert all(self._values(route) in current for route in created)

    def test_create_preview_returns_projections_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        self._require_writable(allegro)
        source, net = self._source(session)
        before = _route_snapshot(ws)

        preview = session.routes.create.preview(
            net,
            self._new_points(source, -1.0),
            source.layer,
            source.width,
        )

        assert preview
        assert _route_snapshot(ws) == before

    def test_atomic_batch_commits_in_order(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        source, net = self._source(session)

        with session.batch('create two routes') as batch:
            first = batch.add(
                session.routes.create.command(
                    net,
                    self._new_points(source),
                    source.layer,
                    source.width,
                )
            )
            second = batch.add(
                session.routes.create.command(
                    net,
                    self._new_points(source, -1.0),
                    source.layer,
                    source.width,
                )
            )

        assert first.value
        assert second.value

    def test_atomic_batch_failure_rolls_back_all(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        self._require_writable(allegro)
        source, net = self._source(session)
        before = _route_snapshot(ws)

        def execute() -> None:
            with session.batch('rollback invalid route') as batch:
                batch.add(
                    session.routes.create.command(
                        net,
                        self._new_points(source),
                        source.layer,
                        source.width,
                    )
                )
                batch.add(
                    session.routes.create.command(
                        net,
                        self._new_points(source),
                        '__MISSING_LAYER__',
                        source.width,
                    )
                )

        with pytest.raises(RuntimeError):
            execute()

        assert _route_snapshot(ws) == before

    def test_dry_run_batch_returns_results_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        self._require_writable(allegro)
        source, net = self._source(session)
        before = _route_snapshot(ws)

        with session.batch('preview route', dry_run=True) as batch:
            result = batch.add(
                session.routes.create.command(
                    net,
                    self._new_points(source),
                    source.layer,
                    source.width,
                )
            )

        assert result.value
        assert _route_snapshot(ws) == before

    def test_route_info_is_frozen(self, session: Session) -> None:
        route = session.routes()[0]

        with pytest.raises(ValidationError, match='frozen'):
            route.layer = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [{'net': 'GND'}],
            [
                {
                    'net': 'GND',
                    'layer': 'ETCH/TOP',
                    'start': {'x': 1.0, 'y': 2.0},
                    'end': {'x': 3.0, 'y': 4.0},
                    'width': 0.2,
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'net': 'GND',
                    'layer': 'ETCH/TOP',
                    'start': {'x': 'bad', 'y': 2.0},
                    'end': {'x': 3.0, 'y': 4.0},
                    'width': 0.2,
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

        with pytest.raises(AllegroProtocolError, match='__abProjectRoutes'):
            session.routes()


class TestShapesApi:
    @staticmethod
    def _values(shape: ShapeInfo) -> tuple[object, ...]:
        return (
            shape.net,
            shape.layer,
            shape.dynamic,
            shape.bbox.lower_left.x,
            shape.bbox.lower_left.y,
            shape.bbox.upper_right.x,
            shape.bbox.upper_right.y,
        )

    def test_default_call_projects_shapes(self, session: Session, ws: Workspace) -> None:
        shapes = session.shapes()
        snapshot = _shape_snapshot(ws)

        assert shapes
        assert all(isinstance(shape, ShapeInfo) for shape in shapes)
        assert all(isinstance(shape.bbox, BBox) for shape in shapes)
        assert [self._values(shape) for shape in shapes] == [tuple(item) for item in snapshot]
        assert all(shape._id == _session_id(session) for shape in shapes)

    @pytest.mark.parametrize('dynamic', [True, False])
    def test_dynamic_filter_matches_single_rpc_snapshot(
        self,
        dynamic: bool,
        session: Session,
        ws: Workspace,
    ) -> None:
        snapshot = _shape_snapshot(ws)
        state = 'dynamic' if dynamic else 'static'
        expected = next(item for item in snapshot if item[2] == state)
        layer = cast('str', expected[1])

        shapes = session.shapes(layer=layer, dynamic=dynamic)

        assert [self._values(shape) for shape in shapes] == [
            tuple(item) for item in snapshot if item[1] == layer and item[2] == state
        ]

    def test_net_and_layer_filters_match_single_rpc_snapshot(
        self,
        session: Session,
        ws: Workspace,
    ) -> None:
        snapshot = _shape_snapshot(ws)
        expected = next(item for item in snapshot if item[0] is not None)
        net = cast('str', expected[0])
        layer = cast('str', expected[1])

        shapes = session.shapes(net=net, layer=layer)

        assert [self._values(shape) for shape in shapes] == [
            tuple(item) for item in snapshot if item[0] == net and item[1] == layer
        ]

    def test_missing_filters_return_empty_collection(self, session: Session) -> None:
        assert session.shapes(net='__MISSING_NET__') == []
        assert session.shapes(layer='__MISSING_LAYER__') == []

    def test_shape_info_is_frozen(self, session: Session) -> None:
        shape = session.shapes()[0]

        with pytest.raises(ValidationError, match='frozen'):
            shape.layer = 'changed'

    @pytest.mark.parametrize(
        'payload',
        [
            [{'net': 'GND'}],
            [
                {
                    'net': 'GND',
                    'layer': 'ETCH/TOP',
                    'dynamic': 'dynamic',
                    'bbox': {
                        'lower_left': {'x': 1.0, 'y': 2.0},
                        'upper_right': {'x': 3.0, 'y': 4.0},
                    },
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'net': 'GND',
                    'layer': 'ETCH/TOP',
                    'dynamic': 'bad',
                    'bbox': {
                        'lower_left': {'x': 1.0, 'y': 2.0},
                        'upper_right': {'x': 3.0, 'y': 4.0},
                    },
                }
            ],
            [
                {
                    'net': 'GND',
                    'layer': 'ETCH/TOP',
                    'dynamic': 'dynamic',
                    'bbox': {
                        'lower_left': {'x': 'bad', 'y': 2.0},
                        'upper_right': {'x': 3.0, 'y': 4.0},
                    },
                }
            ],
        ],
        ids=['missing-field', 'extra-field', 'wrong-state', 'wrong-point-type'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        monkeypatch.setattr(session.raw._channel, 'send', lambda _: repr(payload))

        with pytest.raises(AllegroProtocolError, match='__abProjectShapes'):
            session.shapes()


class TestDrcApi:
    @staticmethod
    def _require_writable(allegro: Allegro) -> None:
        if allegro.mode != 'cli':
            pytest.skip('DRC write test requires the Windows board copy')

    @staticmethod
    def _movement_pair(session: Session) -> tuple[ComponentInfo, ComponentInfo]:
        components = sorted(
            session.components(include_unplaced=False),
            key=lambda component: component.refdes,
        )
        source = components[0]
        target = next(
            component
            for component in components[1:]
            if (component.x, component.y) != (source.x, source.y)
        )
        assert source.x is not None
        assert source.y is not None
        assert source.rotation is not None
        assert target.x is not None
        assert target.y is not None
        assert target.rotation is not None
        return source, target

    @staticmethod
    def _snapshot(drcs: list[DrcInfo]) -> list[str]:
        return sorted(map(repr, drcs))

    @staticmethod
    def _restore(session: Session, component: ComponentInfo) -> None:
        assert component.x is not None
        assert component.y is not None
        session.components.move(
            component.refdes,
            x=component.x,
            y=component.y,
            rotation=component.rotation,
        )
        session.drc.update()

    def test_projects_current_markers(
        self,
        allegro: Allegro,
        session: Session,
        ws: Workspace,
    ) -> None:
        drcs = session.drc()
        expected_count = ws['evalstring'](
            '(let ((design (axlDBRefreshId (axlDBGetDesign)))) (length design->drcs))'
        )

        assert len(drcs) == expected_count
        assert all(isinstance(drc, DrcInfo) for drc in drcs)
        assert all(drc._id == _session_id(session) for drc in drcs)
        assert 'dbid:' not in repr(drcs)
        if allegro.mode == 'cli':
            references = [reference for drc in drcs for reference in drc.objects]
            assert any(isinstance(reference, ComponentRef) for reference in references)
            assert any(isinstance(reference, NetRef) for reference in references)
            assert any(isinstance(reference, PinRef) for reference in references)

    def test_update_preview_returns_projection_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)

        # Windows Allegro 17.2 S048 probes on independent shape1.brd copies disproved
        # the old assumption that separate axlDRCUpdate calls must return byte-for-byte
        # identical marker projections. In 20 committed/preview pairs, four committed
        # recalculations changed the persisted marker projection and one preview result
        # differed from its immediately preceding projection. The drift affected the xy
        # and bBox of the same DRC signature; all 20 preview rollbacks restored the exact
        # pre-preview projection, and every subsequent RPC ping succeeded. Consequently,
        # this test verifies the actual transaction contract: preview returns detached
        # DrcInfo values, then leaves the design exactly as it was immediately beforehand.
        session.drc.update()
        before_preview = session.drc()

        preview = session.drc.update.preview()

        assert all(isinstance(drc, DrcInfo) for drc in preview)
        assert all(drc._id == _session_id(session) for drc in preview)
        assert 'dbid:' not in repr(preview)
        assert self._snapshot(session.drc()) == self._snapshot(before_preview)

    def test_check_component_net_and_pin_immediately(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        pin = next(pin for pin in session.pins() if pin.net)
        targets: list[ComponentInfo | NetInfo | PinInfo] = [
            session.components[pin.refdes],
            session.nets[cast('str', pin.net)],
            pin,
        ]
        generation = session.generation

        try:
            for target in targets:
                checked = session.drc.check(target)
                assert all(isinstance(drc, DrcInfo) for drc in checked)
                assert all(drc._id == _ID(ref(session), generation) for drc in checked)
                assert 'dbid:' not in repr(checked)
        finally:
            session.drc.update()

        assert session.generation == generation

    def test_refresh_rejects_stale_check_target(self, session: Session) -> None:
        target = session.nets()[0]

        session.refresh()

        with pytest.raises(RecordIDError, match='stale'):
            session.drc.check(target)
        assert session.raw['plus'](1, 2) == 3

    def test_update_commits_current_markers(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        generation = session.generation

        updated = session.drc.update()

        assert self._snapshot(session.drc()) == self._snapshot(updated)
        assert session.generation == generation
        assert all(drc._id == _session_id(session) for drc in updated)

    def test_mixed_batch_commits_move_then_drc_update(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        source, target = self._movement_pair(session)
        baseline = session.drc.update()

        try:
            with session.batch('move then update DRC') as batch:
                moved = batch.add(
                    session.components.move.command(
                        source.refdes,
                        x=cast('float', target.x),
                        y=cast('float', target.y),
                        rotation=cast('float', target.rotation),
                    )
                )
                drcs = batch.add(session.drc.update.command())

            assert moved.value.x == pytest.approx(target.x)
            assert self._snapshot(drcs.value) != self._snapshot(baseline)
            assert session.components[source.refdes] == moved.value
            assert self._snapshot(session.drc()) == self._snapshot(drcs.value)
        finally:
            self._restore(session, source)

    def test_mixed_dry_run_returns_results_and_rolls_back(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        source, target = self._movement_pair(session)
        baseline = session.drc.update()

        with session.batch('preview move and DRC', dry_run=True) as batch:
            moved = batch.add(
                session.components.move.command(
                    source.refdes,
                    x=cast('float', target.x),
                    y=cast('float', target.y),
                    rotation=cast('float', target.rotation),
                )
            )
            drcs = batch.add(session.drc.update.command())

        assert moved.value.x == pytest.approx(target.x)
        assert self._snapshot(drcs.value) != self._snapshot(baseline)
        assert session.components[source.refdes] == source
        assert self._snapshot(session.drc()) == self._snapshot(baseline)

    def test_failed_mixed_batch_rolls_back_component_and_drc(
        self,
        allegro: Allegro,
        session: Session,
    ) -> None:
        self._require_writable(allegro)
        source, target = self._movement_pair(session)
        baseline = session.drc.update()
        results: list[CmdResult[Any]] = []

        def execute() -> None:
            with session.batch('rollback move and DRC') as batch:
                results.extend([
                    batch.add(
                        session.components.move.command(
                            source.refdes,
                            x=cast('float', target.x),
                            y=cast('float', target.y),
                            rotation=cast('float', target.rotation),
                        )
                    ),
                    batch.add(session.drc.update.command()),
                    batch.add(
                        session.components.move.command(
                            '__MISSING_COMPONENT__',
                            x=1.0,
                            y=2.0,
                        )
                    ),
                ])

        with pytest.raises(RuntimeError, match='COMPONENT_NOT_FOUND') as raised:
            execute()

        assert session.components[source.refdes] == source
        assert self._snapshot(session.drc()) == self._snapshot(baseline)
        for result in results:
            with pytest.raises(RuntimeError, match='COMPONENT_NOT_FOUND') as stored:
                _ = result.value
            assert stored.value is raised.value

    @pytest.mark.parametrize(
        'payload',
        [
            [{'name': 'Ts Allowed'}],
            [
                {
                    'name': 'Ts Allowed',
                    'category': 'PHYSICAL CONSTRAINTS',
                    'source': 'DEFAULT',
                    'expected': 'NOT_ALLOWED',
                    'actual': 'ANYWHERE',
                    'layer': 'DRC ERROR CLASS/TOP',
                    'location': {'x': 1.0, 'y': 2.0},
                    'bbox': {
                        'lower_left': {'x': 0.0, 'y': 1.0},
                        'upper_right': {'x': 2.0, 'y': 3.0},
                    },
                    'objects': [],
                    'dbid': 'db:1',
                }
            ],
            [
                {
                    'name': 'Ts Allowed',
                    'category': 'PHYSICAL CONSTRAINTS',
                    'source': 'DEFAULT',
                    'expected': 'NOT_ALLOWED',
                    'actual': 'ANYWHERE',
                    'layer': 'DRC ERROR CLASS/TOP',
                    'location': {'x': 'bad', 'y': 2.0},
                    'bbox': {
                        'lower_left': {'x': 0.0, 'y': 1.0},
                        'upper_right': {'x': 2.0, 'y': 3.0},
                    },
                    'objects': [],
                }
            ],
            [
                {
                    'name': 'Ts Allowed',
                    'category': 'PHYSICAL CONSTRAINTS',
                    'source': 'DEFAULT',
                    'expected': 'NOT_ALLOWED',
                    'actual': 'ANYWHERE',
                    'layer': 'DRC ERROR CLASS/TOP',
                    'location': {'x': 1.0, 'y': 2.0},
                    'bbox': {
                        'lower_left': {'x': 0.0, 'y': 1.0},
                        'upper_right': {'x': 2.0, 'y': 3.0},
                    },
                    'objects': [{'kind': 'shape'}],
                }
            ],
        ],
        ids=['missing-field', 'extra-field', 'wrong-point-type', 'unknown-reference'],
    )
    def test_protocol_mismatch_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
        payload: object,
        session: Session,
    ) -> None:
        drc = session.drc
        monkeypatch.setattr(session.raw._channel, 'send', lambda _: repr(payload))

        with pytest.raises(AllegroProtocolError, match='__abProjectDrcs'):
            drc()


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
        assert session.board()._id == _session_id(session)
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

    def test_server_can_restart(self, ws: Workspace, session: Session) -> None:
        epoch = ws.epoch
        session_generation = session.generation
        assert self._single_ping_test(ws)
        assert ws['pyRestartServer']() is True

        for _ in range(40):
            with suppress(OSError, RuntimeError, ConnectionResetError):
                self._single_ping_test(ws)
            if ws.epoch > epoch:
                break
            sleep(0.5)
        else:
            pytest.fail('workspace did not reconnect after server restart')

        assert ws.epoch == epoch + 1
        assert session.generation == session_generation + 1
        assert self._single_ping_test(ws)
