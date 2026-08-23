from __future__ import annotations

from collections.abc import Iterator
from json import dumps
from pathlib import Path
from shutil import copy2
from sys import platform
from time import sleep
from typing import NewType

import pytest

from allegrobridge import Allegro, OpenMode, Workspace
from allegrobridge.util import ASSETS_DIR

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
def design(ws: Workspace) -> object:
    # design is always not None despite a .brd being open or not
    return ws['axlDBGetDesign']()


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
