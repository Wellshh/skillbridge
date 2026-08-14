from __future__ import annotations

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
    _design: object

    @pytest.fixture(autouse=True)
    def _inject(self, design: object) -> None:
        self._design = design

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
