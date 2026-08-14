from __future__ import annotations

import pytest

from skillbridge import Workspace


@pytest.fixture(scope='module')
def design(ws: Workspace) -> object:
    return ws['axlDBGetDesign']()


class TestBasicOp:
    def test_can_get_components(self, design: object) -> None:
        comps = design.components if design is not None else None

        assert comps is not None, 'No board is open: the design has no components database.'
        assert len(comps) >= 1, 'The number of components in this design should be at least 1.'
