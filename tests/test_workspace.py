from __future__ import annotations

from typing import Any

from pytest import MonkeyPatch, mark

from allegrobridge import Workspace as AllegroWorkspace
from skillbridge import Workspace
from skillbridge.client import workspace as workspace_module
from skillbridge.client.channel import Channel
from skillbridge.client.translator import DefaultTranslator
from skillbridge.client.workspace import (
    _open_workspaces,  # ruff: ignore[import-private-name]
    current_workspace,
)


class DummyChannel(Channel):
    def send(self, data: str) -> str:
        pass

    def flush(self) -> None:
        pass

    def try_repair(self) -> Any:
        pass

    def close(self):
        raise RuntimeError("no, i won't close")


class ProbeChannel(DummyChannel):
    def __init__(self, response: str) -> None:
        super().__init__(1)
        self.response = response
        self.commands: list[str] = []

    def send(self, data: str) -> str:
        self.commands.append(data)
        return self.response

    def close(self) -> None:
        pass


def test_a_crash_while_closing_still_clears_the_cache():
    dummy_channel = DummyChannel(1)
    ws = Workspace(channel=dummy_channel, id_=123, translator=DefaultTranslator())
    _open_workspaces[Workspace, 123] = ws

    ws.close()
    assert (Workspace, 123) not in _open_workspaces


def test_allegro_workspace_namespaces_and_chaining() -> None:
    dummy_channel = DummyChannel(1)
    ws = AllegroWorkspace(channel=dummy_channel, id_=456)

    # Allegro-specific top-level namespaces
    assert callable(ws.close)
    assert ws.db.get_design._function == 'db_get_design'
    assert ws.db.get_design.lazy() == 'axlDBGetDesign( )'

    # Multi-level chaining
    assert ws.db.create.pin.lazy(1, 2) == 'axlDBCreatePin(1 2 )'
    assert ws.geo.rotate_pt.lazy(90.0, [100.0, 0.0], None) == (
        'axlGeoRotatePt(90.0 (list 100.0 0.0) nil )'
    )
    assert ws.ui.yes_no.lazy('Proceed?') == 'axlUIYesNo("Proceed?" )'
    assert ws.spreadsheet.get_rgb_color_string.lazy(255, 0, 0) == (
        'axlSpreadsheetGetRGBColorString(255 0 0 )'
    )
    assert ws.cns.get_via_zpvf.lazy() == 'axlCNSGetViaZPVF( )'
    assert ws.drc.get_count.lazy() == 'axlDRCGetCount( )'
    assert ws.form.create.lazy('my_form') == 'axlFormCreate("my_form" )'

    # Fallback to standard axl top-level
    assert ws.axl.clear_sel_set.lazy() == 'axlClearSelSet( )'
    assert ws['plus'].lazy(1, 2) == 'plus(1 2 )'
    assert ws['axlcreate'].lazy() == 'axlcreate( )'
    assert ws['axldo'].lazy() == 'axldo( )'


def test_allegro_workspace_stays_allegro_when_made_current() -> None:
    base_ws = Workspace(channel=ProbeChannel('None'), id_=789)
    ws = AllegroWorkspace(channel=ProbeChannel('None'), id_=789)

    ws.make_current()

    assert type(current_workspace) is AllegroWorkspace
    assert current_workspace.geo is ws.geo
    assert ws.is_current
    assert not base_ws.is_current

    base_ws.close(log_exception=False)

    assert ws.is_current
    ws.close(log_exception=False)


@mark.parametrize(
    ('response', 'expected_type'),
    [('True', AllegroWorkspace), ('None', Workspace)],
)
def test_allegro_workspace_open_detects_server(
    monkeypatch: MonkeyPatch,
    response: str,
    expected_type: type[Workspace],
) -> None:
    channel = ProbeChannel(response)
    workspace_id = f'allegro-probe-{response}'
    monkeypatch.setattr(
        workspace_module,
        'create_channel_class',
        lambda _force_tcp: lambda _id: channel,
    )

    opened = AllegroWorkspace.open(workspace_id)
    reopened = AllegroWorkspace.open(workspace_id)

    assert type(opened) is expected_type
    assert reopened is opened
    assert channel.commands == ["isCallable('axlDBGetDesign)"]

    opened.close()
