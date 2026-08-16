from __future__ import annotations

from time import sleep
from typing import NewType

import pytest

from skillbridge import Workspace

ALObjectHandle = NewType('ALObjectHandle', str)


@pytest.fixture(scope='class')
def design(ws: Workspace) -> object:
    # design is always not None despite a .brd being open or not
    return ws['axlDBGetDesign']()


# POC tests
class TestBasicOp:
    _IDLE_SECONDS = 5

    _design: object

    @pytest.fixture(scope='class', autouse=True)
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

    def test_can_get_nets(self) -> None:
        self._basic_oop('nets', 1)

    def test_ping(self, ws: Workspace) -> None:
        for i in range(1_000):
            assert ws['plus'](i, 0) == i

    def test_callback_keeps_working_while_idle(self, ws: Workspace) -> None:
        assert self._single_ping_test(ws)
        sleep(TestBasicOp._IDLE_SECONDS)
        assert self._single_ping_test(ws), 'Callback not available until next skill execution'

    def test_server_can_restart(self, ws: Workspace) -> None:
        try:
            assert self._single_ping_test(ws)
            assert ws['pyRestartServer']() is True

        finally:
            ws.close()
        # retry connection
        new_ws = Workspace.open()
        assert self._single_ping_test(new_ws)
