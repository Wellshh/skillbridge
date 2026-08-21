from __future__ import annotations

from typing import Any

from allegrobridge.client.workspace import Workspace as AllegroWorkspace
from skillbridge import Workspace
from skillbridge.client.channel import Channel
from skillbridge.client.translator import DefaultTranslator
from skillbridge.client.workspace import _open_workspaces  # ruff: ignore[import-private-name]


class DummyChannel(Channel):
    def send(self, data: str) -> str:
        pass

    def flush(self) -> None:
        pass

    def try_repair(self) -> Any:
        pass

    def close(self):
        raise RuntimeError("no, i won't close")


def test_a_crash_while_closing_still_clears_the_cache():
    dummy_channel = DummyChannel(1)
    ws = Workspace(channel=dummy_channel, id_=123, translator=DefaultTranslator())
    _open_workspaces[123] = ws

    ws.close()
    assert 123 not in _open_workspaces


def test_allegro_workspace_namespaces_and_chaining() -> None:
    dummy_channel = DummyChannel(1)
    ws = AllegroWorkspace(channel=dummy_channel, id_=456)

    # Allegro-specific top-level namespaces
    assert ws.db.get_design._function == 'db_get_design'
    assert ws.db.get_design.lazy() == 'axlDBGetDesign( )'

    # Multi-level chaining
    assert ws.db.create.pin.lazy(1, 2) == 'axlDBCreatePin(1 2 )'
    assert ws.geo.distance.lazy(10, 20) == 'axlGeoDistance(10 20 )'
    assert ws.ui.confirm.lazy('Proceed?') == 'axlUIConfirm("Proceed?" )'
    assert ws.drc.get_design_drcs.lazy() == 'axlDRCGetDesignDrcs( )'
    assert ws.form.create.lazy('my_form') == 'axlFormCreate("my_form" )'

    # Fallback to standard axl top-level
    assert ws.axl.clear_sel_set.lazy() == 'axlClearSelSet( )'
