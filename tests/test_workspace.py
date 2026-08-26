# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from collections import deque
from json import dumps
from pathlib import Path
from threading import Thread
from typing import Any

from pytest import MonkeyPatch, mark, raises

import allegrobridge.server
from allegrobridge import Workspace as AllegroWorkspace
from allegrobridge.exceptions import ExtensionError
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


class RejectingChannel(DummyChannel):
    def __init__(self) -> None:
        super().__init__(1)
        self.closed = False

    def send(self, _data: str) -> str:
        raise RuntimeError('server rejected the request')

    def close(self) -> None:
        self.closed = True


class RejectingCloseChannel(RejectingChannel):
    def close(self) -> None:
        raise OSError('channel close failed')


class ScriptedChannel(DummyChannel):
    def __init__(self, *responses: str) -> None:
        super().__init__(1)
        self.responses = deque(responses)
        self.commands: list[str] = []
        self.closed = False

    def send(self, data: str) -> str:
        self.commands.append(data)
        return self.responses.popleft()

    def close(self) -> None:
        self.closed = True


def test_a_crash_while_closing_still_clears_the_cache():
    dummy_channel = DummyChannel(1)
    ws = Workspace(channel=dummy_channel, id_=123, translator=DefaultTranslator())
    _open_workspaces[Workspace, 123] = ws

    ws.close()
    assert (Workspace, 123) not in _open_workspaces


def test_allegro_workspace_decodes_remote_handles() -> None:
    dummy_channel = DummyChannel(1)
    ws = AllegroWorkspace(channel=dummy_channel, id_=456)

    # The allegro translator must register the Remote/Table/Vector eval types
    # (via _prepare_default_translator) so decoded SKILL handles resolve.
    result = ws._translator.decode('Remote("dbobject:123")')
    assert result._variable == 'dbobject:123'


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


def test_allegro_workspace_annotations_do_not_pollute_base_workspace() -> None:
    assert AllegroWorkspace.__annotations__ is not Workspace.__annotations__
    assert 'air' in AllegroWorkspace.__annotations__
    assert 'air' not in Workspace.__annotations__


def test_allegro_workspace_var_chaining_and_transaction_integration() -> None:
    channel = ScriptedChannel('"result"')
    ws = AllegroWorkspace(channel=channel, id_=456)

    assert ws.axl.db.get.design.lazy() == 'axlDBGetDesign( )'
    design = ws.axl.db.get.design.var()

    assert (
        design.components[0].name.__repr_skill__() == 'nth(0 axlDBGetDesign( )->components)->name'
    )
    assert (
        design.board_thickness > 1.6
    ).__repr_skill__() == '(axlDBGetDesign( )->boardThickness > 1.6)'

    nested_cmd = ws.axl.db_add_prop.lazy(design, ['BOARD_THICKNESS', 0.12])
    assert nested_cmd == 'axlDBAddProp(axlDBGetDesign( ) (list "BOARD_THICKNESS" 0.12) )'

    res = ws.transaction(nested_cmd)
    assert res == 'result'
    assert channel.commands == [
        '__abRunTransaction("axlDBAddProp(axlDBGetDesign( ) (list \\"BOARD_THICKNESS\\" 0.12) )" )'
    ]


def test_allegro_transaction_facade_delegates_to_extension() -> None:
    channel = ScriptedChannel(
        '3',
        '"preview"',
        '[{"index": 0, "status": "success", "value": 3}]',
    )
    ws = AllegroWorkspace(channel=channel, id_=456)
    command = ws['plus'].lazy(1, 2)

    assert ws.transaction(command) == 3
    assert ws.transaction.preview(command) == 'preview'
    assert ws.transaction.batch([command]) == [
        {'index': 0, 'status': 'success', 'value': 3},
    ]
    assert channel.commands == [
        '__abRunTransaction("plus(1 2 )" )',
        '__abRunDryTransaction("plus(1 2 )" )',
        '__abRunSavepointBatch((list "plus(1 2 )") )',
    ]


def test_allegro_transaction_empty_batch_does_not_send() -> None:
    channel = ScriptedChannel()
    ws = AllegroWorkspace(channel=channel, id_=456)

    assert ws.transaction.batch([]) == []
    assert channel.commands == []


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
    expected_commands = ["isCallable('axlDBGetDesign)"]
    if expected_type is AllegroWorkspace:
        expected_commands.extend([
            "isCallable('__abRunTransaction )",
            "isCallable('__abRunSavepointBatch )",
            "isCallable('__abRunDryTransaction )",
            "isCallable('__abProjectBoard )",
            "isCallable('__abProjectComponents )",
            "isCallable('__abMoveComponent )",
            "isCallable('__abProjectLayers )",
            "isCallable('__abProjectNets )",
            "isCallable('__abProjectPadstacks )",
            "isCallable('__abProjectPins )",
            "isCallable('__abProjectSymbols )",
        ])
    assert channel.commands == expected_commands

    opened.close()


def test_allegro_workspace_loads_missing_core_runtime(
    monkeypatch: MonkeyPatch,
) -> None:
    channel = ScriptedChannel(
        'True',
        'None',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
        'True',
    )
    monkeypatch.setattr(
        workspace_module,
        'create_channel_class',
        lambda _force_tcp: lambda _id: channel,
    )

    opened = AllegroWorkspace.open('missing-transaction-runtime')

    assert type(opened) is AllegroWorkspace
    server_file = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
    assert channel.commands == [
        "isCallable('axlDBGetDesign)",
        "isCallable('__abRunTransaction )",
        f'load({dumps(server_file.resolve().as_posix())} )',
        "isCallable('__abRunTransaction )",
        "isCallable('__abRunSavepointBatch )",
        "isCallable('__abRunDryTransaction )",
        "isCallable('__abProjectBoard )",
        "isCallable('__abProjectComponents )",
        "isCallable('__abMoveComponent )",
        "isCallable('__abProjectLayers )",
        "isCallable('__abProjectNets )",
        "isCallable('__abProjectPadstacks )",
        "isCallable('__abProjectPins )",
        "isCallable('__abProjectSymbols )",
    ]

    opened.close()


def test_allegro_workspace_loads_extension_once_across_threads(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    package = tmp_path / 'server'
    extension_dir = package / 'extensions'
    extension_dir.mkdir(parents=True)
    (extension_dir / 'constraints.il').touch()
    monkeypatch.setattr(allegrobridge.server, '__file__', str(package / '__init__.py'))
    channel = ScriptedChannel('None', 'None', 'True')
    ws = AllegroWorkspace(channel=channel, id_=456)
    threads = [
        Thread(
            target=ws._ensure_extension,
            args=('constraints', ('__abp_constraints_project',)),
        )
        for _ in range(2)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    path = (extension_dir / 'constraints.il').resolve().as_posix()
    assert channel.commands == [
        "isCallable('__abp_constraints_project )",
        f'load({dumps(path)} )',
        "isCallable('__abp_constraints_project )",
    ]


def test_allegro_workspace_caches_extension_failure(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    package = tmp_path / 'server'
    package.mkdir()
    monkeypatch.setattr(allegrobridge.server, '__file__', str(package / '__init__.py'))
    channel = ScriptedChannel('None')
    ws = AllegroWorkspace(channel=channel, id_=456)

    with raises(ExtensionError) as first:
        ws._ensure_extension('missing', ('__abp_missing_project',))
    with raises(ExtensionError) as second:
        ws._ensure_extension('missing', ('__abp_missing_project',))

    assert second.value is first.value
    assert channel.commands == ["isCallable('__abp_missing_project )"]


def test_allegro_workspace_skips_present_extension() -> None:
    channel = ScriptedChannel('True')
    ws = AllegroWorkspace(channel=channel, id_=456)

    ws._ensure_extension('constraints', ('__abp_constraints_project',))
    ws._ensure_extension('constraints', ('__abp_constraints_project',))

    assert channel.commands == ["isCallable('__abp_constraints_project )"]


def test_allegro_workspace_caches_extension_readiness_failure(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    package = tmp_path / 'server'
    extension_dir = package / 'extensions'
    extension_dir.mkdir(parents=True)
    (extension_dir / 'broken.il').touch()
    monkeypatch.setattr(allegrobridge.server, '__file__', str(package / '__init__.py'))
    channel = ScriptedChannel('None', 'None', 'None')
    ws = AllegroWorkspace(channel=channel, id_=456)

    with raises(ExtensionError, match='readiness') as first:
        ws._ensure_extension('broken', ('__abp_broken_project',))
    with raises(ExtensionError, match='readiness') as second:
        ws._ensure_extension('broken', ('__abp_broken_project',))

    path = (extension_dir / 'broken.il').resolve().as_posix()
    assert second.value is first.value
    assert channel.commands == [
        "isCallable('__abp_broken_project )",
        f'load({dumps(path)} )',
        "isCallable('__abp_broken_project )",
    ]


def test_allegro_workspace_closes_when_core_runtime_stays_incomplete(
    monkeypatch: MonkeyPatch,
) -> None:
    channel = ScriptedChannel('True', 'None', 'True', 'None')
    monkeypatch.setattr(
        workspace_module,
        'create_channel_class',
        lambda _force_tcp: lambda _id: channel,
    )

    with raises(RuntimeError, match='Allegro core runtime'):
        AllegroWorkspace.open('incomplete-transaction-runtime')

    assert channel.closed


def test_allegro_workspace_open_closes_channel_when_server_rejects_request(
    monkeypatch: MonkeyPatch,
) -> None:
    channel = RejectingChannel()
    monkeypatch.setattr(
        workspace_module,
        'create_channel_class',
        lambda _force_tcp: lambda _id: channel,
    )

    with raises(RuntimeError, match='rejected'):
        AllegroWorkspace.open('rejecting-server')

    assert channel.closed
    assert (AllegroWorkspace, 'rejecting-server') not in _open_workspaces


def test_workspace_open_preserves_creation_error_when_channel_close_fails(
    monkeypatch: MonkeyPatch,
) -> None:
    channel = RejectingCloseChannel()
    monkeypatch.setattr(
        workspace_module,
        'create_channel_class',
        lambda _force_tcp: lambda _id: channel,
    )

    with raises(RuntimeError, match='server rejected the request'):
        AllegroWorkspace.open('rejecting-server-with-close-failure')

    assert (
        AllegroWorkspace,
        'rejecting-server-with-close-failure',
    ) not in _open_workspaces
