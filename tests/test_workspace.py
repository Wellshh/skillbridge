# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import threading
from collections import deque
from io import StringIO
from json import dumps
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from pytest import MonkeyPatch, mark, raises

import allegrobridge.server
from allegrobridge import Workspace as AllegroWorkspace
from allegrobridge._kernel import Workspace
from allegrobridge._kernel.client import workspace as workspace_module
from allegrobridge._kernel.client.channel import Channel
from allegrobridge._kernel.client.expr import Expr
from allegrobridge._kernel.client.objects import RemoteTable, RemoteVector
from allegrobridge._kernel.client.translator import DefaultTranslator
from allegrobridge._kernel.client.workspace import (
    _open_workspaces,
    current_workspace,
)
from allegrobridge.client.base import SkillModule
from allegrobridge.exceptions import ExtensionError


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


class RejectingLoadChannel(ScriptedChannel):
    def send(self, data: str) -> str:
        if data.startswith('load('):
            self.commands.append(data)
            raise RuntimeError('server rejected the load')
        return super().send(data)


def test_a_crash_while_closing_still_clears_the_cache():
    dummy_channel = DummyChannel(1)
    ws = Workspace(channel=dummy_channel, id_=123, translator=DefaultTranslator())
    _open_workspaces[Workspace, 123] = ws

    ws.close()
    assert (Workspace, 123) not in _open_workspaces


@mark.integration
def test_concurrent_open_same_id_creates_one_channel(monkeypatch: MonkeyPatch) -> None:
    """Two threads opening the same workspace id must share one channel.

    Regression for the global ``_open_workspaces`` check-then-act race: without
    a lock, both threads passed the ``cache_key not in _open_workspaces`` guard
    and created duplicate channels (one was overwritten and leaked).
    """
    created: list[Channel] = []
    created_lock = threading.Lock()
    second_creator = threading.Event()

    class CountingChannel(DummyChannel):
        def __init__(self, _workspace_id: object = None) -> None:
            super().__init__(1)
            with created_lock:
                created.append(self)
                is_first = len(created) == 1
            if is_first:
                # Hold the first creator inside the check-then-set window so a
                # second thread can also pass the membership guard. Under the
                # bug the second creator arrives (created grows to 2); under the
                # lock it cannot, blocked on the cache lock.
                second_creator.wait(timeout=0.5)
            else:
                second_creator.set()

    monkeypatch.setattr(
        workspace_module, 'create_channel_class', lambda _force_tcp: CountingChannel
    )
    _open_workspaces.pop((Workspace, 'race-id'), None)

    barrier = threading.Barrier(2, timeout=5)
    results: list[Workspace | None] = [None, None]
    errors: list[Exception] = []

    def opener(idx: int) -> None:
        try:
            barrier.wait()
            results[idx] = Workspace.open('race-id')
        except Exception as exc:  # ruff: ignore[blind-except]
            errors.append(exc)

    threads = [threading.Thread(target=opener, args=(i,), daemon=True) for i in (0, 1)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)
        assert not thread.is_alive(), 'opener thread hung'

    try:
        assert not errors, f'opener threads raised: {errors!r}'
        assert len(created) == 1, f'expected one channel, created {len(created)}'
        assert results[0] is results[1], 'concurrent opens returned different workspaces'
    finally:
        _open_workspaces.pop((Workspace, 'race-id'), None)


def test_allegro_workspace_decodes_remote_handles() -> None:
    dummy_channel = DummyChannel(1)
    ws = AllegroWorkspace(channel=dummy_channel, id_=456)

    # The allegro translator must register the Remote/Table/Vector eval types
    # (via _prepare_default_translator) so decoded SKILL handles resolve.
    result = ws._translator.decode('Remote("dbobject:123")')
    assert result._variable == 'dbobject:123'


def test_workspace_exposes_channel_epoch() -> None:
    channel = DummyChannel(1)
    ws = Workspace(channel=channel, id_=123, translator=DefaultTranslator())

    assert ws.epoch == 0

    channel._epoch = 2
    assert ws.epoch == 2


def test_workspace_eval_executes_expression_once() -> None:
    channel = ProbeChannel('3')
    ws = Workspace(channel=channel, id_=123)

    assert ws.eval(Expr.raw_skill('plus(1 2)')) == 3
    assert channel.commands == ['plus(1 2)']


def test_workspace_eval_preserves_list_decoder_results() -> None:
    channel = ScriptedChannel('None', '[1, 2]', 'None')
    ws = Workspace(channel=channel, id_=123)

    assert ws.eval(Expr.raw_skill('items').as_list()) is None
    assert ws.eval(Expr.raw_skill('items').as_list()) == [1, 2]
    filtered = Expr.raw_skill('items').as_list().where(lambda item: item.enabled)
    assert ws.eval(filtered) is None
    assert channel.commands == [
        'items',
        'items',
        'setof(_expr0 items _expr0->enabled)',
    ]


def test_workspace_builds_remote_collections_and_delegates_repair(
    monkeypatch: MonkeyPatch,
) -> None:
    channel = ScriptedChannel('Table("table")', 'Vector("vector")')
    monkeypatch.setattr(channel, 'try_repair', lambda: 'repaired')
    ws = Workspace(channel=channel, id_=123)

    assert isinstance(ws.make_table('T', 0), RemoteTable)
    assert isinstance(ws.make_vector(2, None), RemoteVector)
    assert ws.id == 123
    assert ws.try_repair() == 'repaired'
    assert channel.commands == ['makeTable("T" 0)', 'makeVector(2 nil)']


def test_workspace_define_encodes_multiline_function() -> None:
    channel = ProbeChannel('None')
    ws = Workspace(channel=channel, id_=123)

    ws.define(
        'custom_matrix_calc',
        ['limit', 'multiplier'],
        'limit +\nmultiplier',
    )

    assert channel.commands == ['defun(userCustomMatrixCalc (limit multiplier) limit + multiplier)']


def test_workspace_fix_completion_configures_ipython(monkeypatch: MonkeyPatch) -> None:
    completer = SimpleNamespace(use_jedi=True, greedy=False)
    shell = SimpleNamespace(Completer=completer)
    monkeypatch.setattr(workspace_module, 'get_ipython', lambda: shell, raising=False)

    Workspace.fix_completion()

    assert not completer.use_jedi
    assert completer.greedy


def test_workspace_direct_mode_uses_original_stdout(monkeypatch: MonkeyPatch) -> None:
    stdin = SimpleNamespace(isatty=lambda: False)
    stdout = StringIO()
    stderr = StringIO()
    monkeypatch.setattr(workspace_module.sys, 'stdin', stdin)
    monkeypatch.setattr(workspace_module.sys, 'stdout', stdout)
    monkeypatch.setattr(workspace_module.sys, 'stderr', stderr)

    ws = Workspace.open('direct', direct=True)

    assert ws.id == 'direct'
    assert ws._channel.stdout is stdout
    assert workspace_module.sys.stdout is stderr


def test_workspace_open_rejects_conflicting_mode_and_missing_server(
    monkeypatch: MonkeyPatch,
) -> None:
    with raises(ValueError, match='conflict'):
        Workspace.open(direct=True, force_tcp=True)

    def missing_server(_id: object) -> Channel:
        raise FileNotFoundError

    monkeypatch.setattr(workspace_module, 'create_channel_class', lambda _force_tcp: missing_server)

    with raises(RuntimeError, match='No server found'):
        Workspace.open('missing-server')


def test_workspace_close_can_suppress_error_and_preserve_other_cache_entry() -> None:
    ws = Workspace(channel=DummyChannel(1), id_=123)
    other = Workspace(channel=ProbeChannel('None'), id_=456)
    _open_workspaces[Workspace, 123] = ws
    _open_workspaces[Workspace, 456] = other

    try:
        ws.close(log_exception=False)

        assert (Workspace, 123) not in _open_workspaces
        assert _open_workspaces[Workspace, 456] is other
    finally:
        _open_workspaces.pop((Workspace, 456), None)


def test_allegro_workspace_namespaces_and_chaining() -> None:
    dummy_channel = DummyChannel(1)
    ws = AllegroWorkspace(channel=dummy_channel, id_=456)

    # Allegro-specific top-level namespaces
    assert callable(ws.close)
    assert ws.db.get_design._function == 'db_get_design'
    assert ws.db.get_design.expr().render() == 'axlDBGetDesign()'

    # Multi-level chaining
    assert ws.db.create.pin.expr(1, 2).render() == 'axlDBCreatePin(1 2)'
    assert ws.geo.rotate_pt.expr(90.0, [100.0, 0.0], None).render() == (
        'axlGeoRotatePt(90.0 (list 100.0 0.0) nil)'
    )
    assert ws.ui.yes_no.expr('Proceed?').render() == 'axlUIYesNo("Proceed?")'
    assert ws.spreadsheet.get_rgb_color_string.expr(255, 0, 0).render() == (
        'axlSpreadsheetGetRGBColorString(255 0 0)'
    )
    assert ws.cns.get_via_zpvf.expr().render() == 'axlCNSGetViaZPVF()'
    assert ws.drc.get_count.expr().render() == 'axlDRCGetCount()'
    assert ws.form.create.expr('my_form').render() == 'axlFormCreate("my_form")'

    # Fallback to standard axl top-level
    assert ws.axl.clear_sel_set.expr().render() == 'axlClearSelSet()'
    assert ws['plus'].expr(1, 2).render() == 'plus(1 2)'
    assert ws['axlcreate'].expr().render() == 'axlcreate()'
    assert ws['axldo'].expr().render() == 'axldo()'


def test_allegro_workspace_annotations_do_not_pollute_base_workspace() -> None:
    assert AllegroWorkspace.__annotations__ is not Workspace.__annotations__
    assert 'air' in AllegroWorkspace.__annotations__
    assert 'air' not in Workspace.__annotations__


def test_allegro_workspace_expr_chaining_and_transaction_integration() -> None:
    channel = ScriptedChannel('"result"')
    ws = AllegroWorkspace(channel=channel, id_=456)

    design = ws.axl.db.get.design.expr()

    assert (
        design.components.as_list()[0].name.render() == 'nth(0 axlDBGetDesign()->components)->name'
    )
    assert (design.board_thickness > 1.6).render() == '(axlDBGetDesign()->boardThickness > 1.6)'

    nested_cmd = ws.axl.db_add_prop.expr(design, ['BOARD_THICKNESS', 0.12]).render()
    assert nested_cmd == 'axlDBAddProp(axlDBGetDesign() (list "BOARD_THICKNESS" 0.12))'

    res = ws.transaction(nested_cmd)
    assert res == 'result'
    assert channel.commands == [
        '__abRunTransaction("axlDBAddProp(axlDBGetDesign() (list \\"BOARD_THICKNESS\\" 0.12))")'
    ]


def test_allegro_transaction_facade_delegates_to_extension() -> None:
    channel = ScriptedChannel(
        '3',
        '"preview"',
        '[{"index": 0, "status": "success", "value": 3}]',
    )
    ws = AllegroWorkspace(channel=channel, id_=456)
    command = ws['plus'].expr(1, 2).render()

    assert ws.transaction(command) == 3
    assert ws.transaction.preview(command) == 'preview'
    assert ws.transaction.batch([command]) == [
        {'index': 0, 'status': 'success', 'value': 3},
    ]
    assert channel.commands == [
        '__abRunTransaction("plus(1 2)")',
        '__abRunDryTransaction("plus(1 2)")',
        '__abRunSavepointBatch((list "plus(1 2)"))',
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
            "isCallable('__abRunTransaction)",
            "isCallable('__abRunSavepointBatch)",
            "isCallable('__abRunDryTransaction)",
            "isCallable('__abProjectBoard)",
            "isCallable('__abProjectComponents)",
            "isCallable('__abMoveComponent)",
            "isCallable('__abMoveComponentsBy)",
            "isCallable('__abProjectLayers)",
            "isCallable('__abProjectNets)",
            "isCallable('__abProjectPadstacks)",
            "isCallable('__abProjectPins)",
            "isCallable('__abProjectSymbols)",
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
        "isCallable('__abRunTransaction)",
        f'load({dumps(server_file.resolve().as_posix())})',
        "isCallable('__abRunTransaction)",
        "isCallable('__abRunSavepointBatch)",
        "isCallable('__abRunDryTransaction)",
        "isCallable('__abProjectBoard)",
        "isCallable('__abProjectComponents)",
        "isCallable('__abMoveComponent)",
        "isCallable('__abMoveComponentsBy)",
        "isCallable('__abProjectLayers)",
        "isCallable('__abProjectNets)",
        "isCallable('__abProjectPadstacks)",
        "isCallable('__abProjectPins)",
        "isCallable('__abProjectSymbols)",
    ]

    opened.close()


def test_allegro_workspace_loads_skill_module_once_for_multiple_apis() -> None:
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/probe.il')
    channel = ScriptedChannel('False', 'None', 'True', 'True')
    ws = AllegroWorkspace(channel=channel, id_=456)

    ws._ensure_module(module, ('__abp_probe_project',))
    ws._ensure_module(module, ('__abp_probe_move',))

    resource = Path(__file__).parent / 'allegrobridge/fixtures/server/extensions/probe.il'
    assert channel.commands == [
        "and(isCallable('__abp_probe_project))",
        f'load({dumps(resource.resolve().as_posix())})',
        "and(isCallable('__abp_probe_project))",
        "and(isCallable('__abp_probe_move))",
    ]


def test_allegro_workspace_checks_all_module_procedures_in_one_request() -> None:
    module = SkillModule('example_plugin', 'server.il')
    channel = ScriptedChannel('True')
    ws = AllegroWorkspace(channel=channel, id_=456)

    ws._ensure_module(module, ('firstProcedure', 'secondProcedure'))
    ws._ensure_module(module, ())

    assert channel.commands == ["and(isCallable('firstProcedure) isCallable('secondProcedure))"]


def test_allegro_workspace_module_readiness_failure_does_not_poison_other_api() -> None:
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/probe.il')
    channel = ScriptedChannel('False', 'None', 'False', 'False', 'False', 'True')
    ws = AllegroWorkspace(channel=channel, id_=456)

    with raises(ExtensionError, match='readiness'):
        ws._ensure_module(module, ('__abp_missing_project',))
    with raises(ExtensionError, match='readiness'):
        ws._ensure_module(module, ('__abp_other_missing_project',))

    ws._ensure_module(module, ('__abp_probe_project',))
    assert len([command for command in channel.commands if command.startswith('load(')]) == 1


def test_allegro_workspace_caches_skill_module_load_failure() -> None:
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/missing.il')
    channel = ScriptedChannel('False')
    ws = AllegroWorkspace(channel=channel, id_=456)

    with raises(ExtensionError, match='was not found') as first:
        ws._ensure_module(module, ('__abp_missing_project',))
    with raises(ExtensionError) as second:
        ws._ensure_module(module, ('__abp_missing_project',))

    assert second.value is first.value
    assert channel.commands == ["and(isCallable('__abp_missing_project))"]


def test_allegro_workspace_wraps_module_readiness_transport_failure() -> None:
    module = SkillModule('example_plugin', 'server.il')
    ws = AllegroWorkspace(channel=RejectingChannel(), id_=456)

    with raises(ExtensionError, match='readiness check failed') as failure:
        ws._ensure_module(module, ('serverProcedure',))

    assert isinstance(failure.value.__cause__, RuntimeError)


def test_allegro_workspace_caches_skill_module_transport_failure() -> None:
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/probe.il')
    channel = RejectingLoadChannel('False')
    ws = AllegroWorkspace(channel=channel, id_=456)

    with raises(ExtensionError, match='failed to load SKILL module') as first:
        ws._ensure_module(module, ('__abp_probe_project',))
    with raises(ExtensionError) as second:
        ws._ensure_module(module, ('__abp_probe_project',))

    assert second.value is first.value
    assert isinstance(first.value.__cause__, RuntimeError)
    assert len(channel.commands) == 2


def test_allegro_workspace_has_no_legacy_extension_loader() -> None:
    assert not hasattr(AllegroWorkspace(channel=ScriptedChannel(), id_=456), '_ensure_extension')


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
