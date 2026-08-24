from __future__ import annotations

from collections.abc import Iterator
from json import dumps
from pathlib import Path
from shutil import copy2
from sys import platform
from time import sleep
from typing import NewType

import pytest
from pydantic import ValidationError

from allegrobridge import Allegro, OpenMode, Session, Workspace
from allegrobridge.client.api import AllegroProtocolError, BoardInfo
from allegrobridge.util import ASSETS_DIR
from skillbridge import SkillCode

ALObjectHandle = NewType('ALObjectHandle', str)
_TEST_BOARD = ASSETS_DIR / 'shape1.brd'


@pytest.fixture(scope='class')
def allegro(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Allegro]:
    mode: OpenMode = 'cli' if platform == 'win32' else 'manual'
    board = None
    if mode == 'cli':
        board = Path(copy2(_TEST_BOARD, tmp_path_factory.mktemp('allegro')))

    with Allegro.open(mode=mode, board=board) as opened:
        yield opened


@pytest.fixture(scope='class')
def ws(allegro: Allegro) -> Workspace:
    return allegro.workspace


@pytest.fixture(scope='class')
def session(allegro: Allegro) -> Session:
    return allegro.session


@pytest.fixture(scope='class')
def design(ws: Workspace) -> object:
    # design is always not None despite a .brd being open or not
    return ws['axlDBGetDesign']()


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

        get_thickness = 'cadr(assoc("BOARD_THICKNESS" axlDBGetProperties(axlDBGetDesign())))'
        snapshot = (
            f'list(nil \'property {get_thickness} '
            "'components length(axlDBGetDesign()->components) "
            "'symbols length(axlDBGetDesign()->symbols))"
        )
        original_snapshot = ws['evalstring'](snapshot)
        original = original_snapshot['property']

        try:
            success_command = (
                'progn('
                'axlDBAddProp(axlDBGetDesign() list("BOARD_THICKNESS" 0.123456)) '
                f'{get_thickness})'
            )
            failed_command = (
                'progn('
                'axlDBAddProp(axlDBGetDesign() list("BOARD_THICKNESS" 0.654321)) '
                'error("savepoint-item"))'
            )
            results = ws.transaction.batch([
                SkillCode(success_command),
                SkillCode(failed_command),
            ])
            persisted = ws['evalstring'](snapshot)

            assert results[0] == {
                'index': 0,
                'status': 'success',
                'value': persisted['property'],
            }
            assert results[1]['index'] == 1
            assert results[1]['status'] == 'failure'
            assert 'SAVEPOINT_COMMAND_FAILED' in results[1]['error']

            with pytest.raises(RuntimeError, match='TRANSACTION_COMMAND_FAILED'):
                ws.transaction(
                    SkillCode(
                        'progn('
                        'axlDBAddProp(axlDBGetDesign() list("BOARD_THICKNESS" 0.222222)) '
                        'error("atomic-item"))'
                    )
                )
            assert ws['evalstring'](snapshot) == persisted

            preview = ws.transaction.preview(
                SkillCode(
                    f'progn(axlDBAddProp(axlDBGetDesign() '
                    f'list("BOARD_THICKNESS" 0.333333)) {snapshot})'
                )
            )
            assert preview.keys() == {'property', 'components', 'symbols'}
            assert isinstance(preview['property'], (bool, dict, float, int, list, str, type(None)))
            assert preview['property'] != persisted['property']
            assert preview['components'] == persisted['components']
            assert preview['symbols'] == persisted['symbols']
            assert ws['evalstring'](snapshot) == persisted
            assert ws['plus'](1, 2) == 3
        finally:
            if original is None:
                ws.transaction(SkillCode('axlDBDeleteProp(nil "BOARD_THICKNESS")'))
            else:
                ws.transaction(
                    SkillCode(
                        f'axlDBAddProp(axlDBGetDesign() list("BOARD_THICKNESS" {dumps(original)}))'
                    )
                )
        assert ws['evalstring'](snapshot) == original_snapshot


class TestBoardApi:
    def test_default_call_returns_board_info(
        self,
        design: object,
        session: Session,
    ) -> None:
        board = session.board()

        assert isinstance(board, BoardInfo)
        assert board.path.endswith('.brd')
        assert board.units
        assert board.component_count == len(design.components)
        assert board.symbol_count == len(design.symbols)
        assert board.net_count == len(design.nets)
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
                candidate = Workspace.open()
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
