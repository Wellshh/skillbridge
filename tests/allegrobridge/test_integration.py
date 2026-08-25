from __future__ import annotations

from collections.abc import Iterator
from json import dumps
from pathlib import Path
from shutil import copy2
from socket import socket
from sys import platform
from time import sleep
from typing import NewType

import pytest
from pydantic import ValidationError

from allegrobridge import Allegro, OpenMode, Session, Workspace
from allegrobridge.client.api import AllegroProtocolError, BoardInfo, ComponentInfo, NetInfo
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


def _net_snapshot(ws: Workspace) -> list[list[object]]:
    return ws['evalstring'](
        '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
        '(foreach net design->nets '
        '(setq result '
        '(cons (list net->name net->nBranches net->unconnected net->unplaced) result))) '
        '(reverse result))'
    )


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
