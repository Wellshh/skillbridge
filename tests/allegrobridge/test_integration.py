from __future__ import annotations

import pytest

from skillbridge import Workspace


@pytest.fixture(scope='module')
def design(ws: Workspace) -> object:
    return ws['axlDBGetDesign']()


class TestBasicOp:
    def test_can_get_components(self, design: object) -> None:
        assert design is not None, 'Failed to get design.'
        comps = design.components

        assert len(comps) >= 1, 'The number of components in this design should be at least 1.'
