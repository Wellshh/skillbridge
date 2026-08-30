# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Callable, Iterator
from copy import deepcopy
from json import loads
from pathlib import Path
from shutil import copy2
from socket import socket
from sys import platform
from typing import TYPE_CHECKING, cast

import pytest

from allegrobridge import Allegro
from allegrobridge.util import ASSETS_DIR
from tests.allegrobridge.probe.connect import (
    ConnectProbe,
    _classify_activity,
    _classify_blocking,
    _classify_post,
    _classify_rollback,
    _classify_route_change,
)

if TYPE_CHECKING:
    from allegrobridge import Workspace

_TEST_BOARD = ASSETS_DIR / 'shape1.brd'


class FakeWorkspace:
    def __init__(self, payloads: dict[str, object]) -> None:
        self.payloads = payloads
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    def __getitem__(self, procedure: str) -> Callable[..., object]:
        def call(*args: object) -> object:
            self.calls.append((procedure, args))
            payload = self.payloads.get(procedure, True)
            if callable(payload):
                return cast('Callable[..., object]', payload)(*args)
            return payload

        return call


@pytest.fixture
def connect_allegro(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Allegro]:
    if platform != 'win32':
        pytest.skip('Connect probes require the Windows board copy')
    board = Path(copy2(_TEST_BOARD, tmp_path_factory.mktemp('connect-allegro')))
    with socket() as listener:
        listener.bind(('localhost', 0))
        workspace_id = str(listener.getsockname()[1])
    with Allegro.open(mode='cli', board=board, workspace_id=workspace_id) as opened:
        yield opened


@pytest.fixture
def connect_probe(connect_allegro: Allegro) -> ConnectProbe:
    # connect.il delegates route projection to the first-class RoutesApi.
    # The probe owns only its sibling script, so explicitly touch the public
    # lazy-loaded API before invoking the private probe entrypoints.
    _ = connect_allegro.session.routes
    return ConnectProbe(connect_allegro.workspace)


def _route(name: str) -> dict[str, object]:
    return {
        'net': name,
        'layer': 'ETCH/TOP',
        'obj_type': 'line',
        'start': {'x': 0.0, 'y': 0.0},
        'end': {'x': 1.0, 'y': 1.0},
        'width': 0.1,
        'length': 1.414,
        'radius': None,
        'is_clockwise': None,
        'center': None,
    }


def _route_snapshot(routes: list[dict[str, object]] | None) -> dict[str, object]:
    return {
        'allegro_version': '17.2',
        'routes': routes,
        'route_count': len(routes or []),
    }


@pytest.mark.parametrize(
    ('before_routes', 'during_routes', 'expected'),
    [
        (None, [_route('new')], 'done'),
        (None, None, 'cancel'),
        ([_route('a'), _route('b')], [_route('b'), _route('a')], 'cancel'),
    ],
)
def test_classifies_route_change_from_fingerprints(
    before_routes: list[dict[str, object]] | None,
    during_routes: list[dict[str, object]] | None,
    expected: str,
) -> None:
    before = _route_snapshot(before_routes)
    during = _route_snapshot(during_routes)

    assert _classify_route_change(before, during) == expected


@pytest.mark.parametrize(
    ('after', 'expected'),
    [
        ('before', 'rolled_back'),
        ('during', 'persisted'),
        ('other', 'partial'),
    ],
)
def test_classifies_route_rollback_results(after: str, expected: str) -> None:
    before = _route_snapshot([_route('before')])
    during = _route_snapshot([_route('during')])
    snapshots = {
        'before': before,
        'during': during,
        'other': _route_snapshot([_route('other')]),
    }

    assert _classify_rollback(before, during, snapshots[after]) == expected


def test_classifies_idempotent_routing_as_inconclusive() -> None:
    snapshot = _route_snapshot([_route('same')])

    assert (
        _classify_rollback(snapshot, deepcopy(snapshot), _route_snapshot([_route('after')]))
        == 'inconclusive'
    )


def _blocking_report(
    during_routes: list[dict[str, object]] | None,
    elapsed: float,
) -> dict[str, object]:
    return {
        'before': _route_snapshot(None),
        'during': _route_snapshot(during_routes),
        'elapsed_seconds': elapsed,
    }


@pytest.mark.parametrize(
    ('during_routes', 'elapsed', 'expected'),
    [
        ([_route('new')], 0.1, 'blocking_done'),
        ([_route('new')], 60.0, 'blocking_done'),
        (None, 0.1, 'non_blocking'),
        (None, 1.0, 'blocking_cancel'),
        (None, 60.0, 'blocking_cancel'),
    ],
)
def test_classifies_blocking_semantics(
    during_routes: list[dict[str, object]] | None,
    elapsed: float,
    expected: str,
) -> None:
    assert _classify_blocking(_blocking_report(during_routes, elapsed)) == expected


def test_blocking_threshold_override_reclassifies_wait() -> None:
    report = _blocking_report(None, 5.0)

    assert _classify_blocking(report, threshold=10.0) == 'non_blocking'


def test_classifies_post_immediate_snapshot_as_fire_and_forget() -> None:
    report = {'before': _route_snapshot(None), 'immediate': _route_snapshot(None)}

    assert _classify_post(report) is True


def test_classifies_post_immediate_execution_as_not_fire_and_forget() -> None:
    report = {
        'before': _route_snapshot(None),
        'immediate': _route_snapshot([_route('new')]),
    }

    assert _classify_post(report) is False


def test_probe_loads_sibling_skill_file_and_sanitizes_payload() -> None:
    workspace = FakeWorkspace({'probe': {'value': 'dbid:ABC123'}})
    probe = ConnectProbe(cast('Workspace', workspace))

    assert probe._call('probe') == {'value': '<dbid>'}
    assert workspace.calls[0][0] == 'load'
    assert cast('str', workspace.calls[0][1][0]).endswith('/probe/connect.il')


def test_probe_rejects_non_mapping_payload() -> None:
    probe = ConnectProbe(cast('Workspace', FakeWorkspace({'probe': []})))

    with pytest.raises(TypeError, match='probe returned list, expected dict'):
        probe._call('probe')


def test_snapshot_probes_routes_and_forwards_net() -> None:
    payload = _route_snapshot([_route('GND')])
    workspace = FakeWorkspace({'__abpRouteSnapshot': payload})
    probe = ConnectProbe(cast('Workspace', workspace))

    assert probe.snapshot() == payload
    assert probe.snapshot('GND') == payload
    assert [call[1] for call in workspace.calls if call[0] == '__abpRouteSnapshot'] == [
        (None,),
        ('GND',),
    ]


def test_emit_prints_and_optionally_writes_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv('ALLEGRO_CONNECT_PROBE_OUTPUT_DIR', str(tmp_path))

    ConnectProbe.emit('report.json', {'value': 1})

    assert loads(capsys.readouterr().out) == {'value': 1}
    assert loads((tmp_path / 'report.json').read_text(encoding='utf-8')) == {'value': 1}


def test_emit_only_prints_without_output_directory(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv('ALLEGRO_CONNECT_PROBE_OUTPUT_DIR', raising=False)

    ConnectProbe.emit('unused.json', {'value': 2})

    assert loads(capsys.readouterr().out) == {'value': 2}


def test_blocking_report_includes_elapsed_and_classification() -> None:
    completed = {
        'status': 'completed',
        'before': _route_snapshot(None),
        'during': _route_snapshot([_route('new')]),
        'after_rollback': _route_snapshot(None),
        'after_cleanup': _route_snapshot(None),
    }
    workspace = FakeWorkspace({'__abpAddConnectBlocking': completed, 'plus': 3})
    probe = ConnectProbe(cast('Workspace', workspace))

    report = probe.blocking(None, 'add connect')

    assert isinstance(report['elapsed_seconds'], float)
    assert report['route_change'] == 'done'
    assert report['blocking_semantics'] == 'blocking_done'
    assert report['rollback_coverage'] == 'rolled_back'
    assert report['ping'] == 3
    assert workspace.calls[-2] == ('__abpAddConnectBlocking', (None, 'add connect'))

    canceled = {
        'status': 'completed',
        'before': _route_snapshot(None),
        'during': _route_snapshot(None),
        'after_rollback': _route_snapshot(None),
        'after_cleanup': _route_snapshot(None),
    }
    workspace.payloads['__abpAddConnectBlocking'] = canceled

    report = probe.blocking('GND', 'add connect')

    assert report['route_change'] == 'cancel'
    assert report['blocking_semantics'] == 'non_blocking'
    assert report['rollback_coverage'] == 'inconclusive'
    assert workspace.calls[-2] == ('__abpAddConnectBlocking', ('GND', 'add connect'))


def test_post_report_classifies_fire_and_forget() -> None:
    payload = {
        'before': _route_snapshot(None),
        'immediate': _route_snapshot(None),
        'shell_return': True,
    }
    workspace = FakeWorkspace({'__abpAddConnectPost': payload, 'plus': 3})
    probe = ConnectProbe(cast('Workspace', workspace))

    report = probe.post(None, 'add connect')

    assert isinstance(report['elapsed_seconds'], float)
    assert report['fire_and_forget'] is True
    assert report['ping'] == 3
    assert workspace.calls[-2] == ('__abpAddConnectPost', (None, 'add connect'))


def test_classifies_activity_from_fingerprints() -> None:
    mid = _route_snapshot(None)
    unchanged = _route_snapshot(None)
    changed = _route_snapshot([_route('new')])

    assert _classify_activity(mid, changed) == 'active'
    assert _classify_activity(mid, unchanged) == 'cancelled'


def test_active_report_classifies_background_active() -> None:
    launch = {
        'allegro_version': '17.2',
        'status': 'completed',
        'before': _route_snapshot(None),
        'mid': _route_snapshot(None),
    }
    drive = {
        'command': 'pick 0.0 0.0; pick 1.0 1.0; done',
        'during': _route_snapshot([_route('new')]),
        'after_rollback': _route_snapshot(None),
        'rolled_back': True,
    }
    workspace = FakeWorkspace(
        {
            '__abpAddConnectLaunch': launch,
            '__abpAddConnectActiveDrive': drive,
            '__abpAddConnectCleanup': {'after_cleanup': _route_snapshot(None)},
            'plus': 3,
        },
    )
    probe = ConnectProbe(cast('Workspace', workspace))

    report = probe.active('GND', 'add connect -net GND', (0.0, 0.0), (1.0, 1.0))

    assert isinstance(report['elapsed_seconds'], float)
    assert report['status'] == 'completed'
    assert report['route_change'] == 'cancel'
    assert report['activity'] == 'active'
    assert report['rollback_coverage'] == 'rolled_back'
    assert report['ping'] == 3
    assert workspace.calls[-4] == ('__abpAddConnectLaunch', ('GND', 'add connect -net GND'))
    assert workspace.calls[-3] == ('__abpAddConnectActiveDrive', ('GND', 0.0, 0.0, 1.0, 1.0))
    assert workspace.calls[-2] == ('__abpAddConnectCleanup', ('GND',))


def test_active_report_classifies_cancelled() -> None:
    launch = {
        'allegro_version': '17.2',
        'status': 'completed',
        'before': _route_snapshot(None),
        'mid': _route_snapshot(None),
    }
    drive = {
        'command': 'pick 0.0 0.0; pick 1.0 1.0; done',
        'during': _route_snapshot(None),
        'after_rollback': _route_snapshot(None),
        'rolled_back': True,
    }
    workspace = FakeWorkspace(
        {
            '__abpAddConnectLaunch': launch,
            '__abpAddConnectActiveDrive': drive,
            '__abpAddConnectCleanup': {'after_cleanup': _route_snapshot(None)},
            'plus': 3,
        },
    )
    probe = ConnectProbe(cast('Workspace', workspace))

    report = probe.active(None, 'add connect', (0.0, 0.0), (1.0, 1.0))

    assert report['activity'] == 'cancelled'
    assert report['rollback_coverage'] == 'inconclusive'
    assert workspace.calls[-4] == ('__abpAddConnectLaunch', (None, 'add connect'))


def test_active_report_cleans_up_when_drive_fails() -> None:
    def fail(*args: object) -> object:
        raise RuntimeError('shell died')

    launch = {
        'allegro_version': '17.2',
        'status': 'completed',
        'before': _route_snapshot(None),
        'mid': _route_snapshot(None),
    }
    workspace = FakeWorkspace(
        {
            '__abpAddConnectLaunch': launch,
            '__abpAddConnectActiveDrive': fail,
            '__abpAddConnectCleanup': {'after_cleanup': _route_snapshot(None)},
            'plus': 3,
        },
    )
    probe = ConnectProbe(cast('Workspace', workspace))

    with pytest.raises(RuntimeError, match='shell died'):
        probe.active(None, 'add connect', (0.0, 0.0), (1.0, 1.0))

    assert workspace.calls[-1] == ('__abpAddConnectCleanup', (None,))


def test_active_report_cleans_up_when_launch_fails() -> None:
    def fail(*args: object) -> object:
        raise RuntimeError('launch died')

    workspace = FakeWorkspace(
        {
            '__abpAddConnectLaunch': fail,
            '__abpAddConnectCleanup': {'after_cleanup': _route_snapshot(None)},
            'plus': 3,
        },
    )
    probe = ConnectProbe(cast('Workspace', workspace))

    with pytest.raises(RuntimeError, match='launch died'):
        probe.active(None, 'add connect', (0.0, 0.0), (1.0, 1.0))

    assert workspace.calls[-1] == ('__abpAddConnectCleanup', (None,))


def test_driven_report_classifies_done_and_rollback() -> None:
    completed = {
        'status': 'completed',
        'command': 'add connect; pick 0.0 0.0; pick 1.0 1.0; done',
        'before': _route_snapshot(None),
        'during': _route_snapshot([_route('new')]),
        'after_rollback': _route_snapshot(None),
        'after_cleanup': _route_snapshot(None),
    }
    workspace = FakeWorkspace({'__abpAddConnectDriven': completed, 'plus': 3})
    probe = ConnectProbe(cast('Workspace', workspace))

    report = probe.driven('GND', 'add connect', (0.0, 0.0), (1.0, 1.0))

    assert isinstance(report['elapsed_seconds'], float)
    assert report['route_change'] == 'done'
    assert report['rollback_coverage'] == 'rolled_back'
    assert report['ping'] == 3
    assert workspace.calls[-2] == (
        '__abpAddConnectDriven',
        ('GND', 'add connect', 0.0, 0.0, 1.0, 1.0),
    )


def test_driven_report_classifies_cancel_as_inconclusive() -> None:
    canceled = {
        'status': 'completed',
        'command': 'add connect; pick 0.0 0.0; pick 1.0 1.0; done',
        'before': _route_snapshot(None),
        'during': _route_snapshot(None),
        'after_rollback': _route_snapshot(None),
        'after_cleanup': _route_snapshot(None),
    }
    workspace = FakeWorkspace({'__abpAddConnectDriven': canceled, 'plus': 3})
    probe = ConnectProbe(cast('Workspace', workspace))

    report = probe.driven(None, 'add connect', (0.0, 0.0), (1.0, 1.0))

    assert report['route_change'] == 'cancel'
    assert report['rollback_coverage'] == 'inconclusive'
    assert workspace.calls[-2] == (
        '__abpAddConnectDriven',
        (None, 'add connect', 0.0, 0.0, 1.0, 1.0),
    )


@pytest.mark.allegro
@pytest.mark.timeout(600)
class TestConnectProbe:
    def test_axlshell_add_connect_blocks_until_user(self, connect_probe: ConnectProbe) -> None:
        report = connect_probe.blocking(None, 'add connect')
        connect_probe.emit('connect-blocking.json', report)
        assert report['status'] == 'completed'
        assert isinstance(report['elapsed_seconds'], float)
        assert report['route_change'] in {'done', 'cancel'}
        assert report['blocking_semantics'] in {
            'blocking_done',
            'non_blocking',
            'blocking_cancel',
        }
        assert isinstance(report['before'], dict)
        assert isinstance(report['during'], dict)
        assert report['ping'] == 3

    def test_axlshellpost_add_connect_returns_immediately(
        self,
        connect_probe: ConnectProbe,
    ) -> None:
        report = connect_probe.post(None, 'add connect')
        connect_probe.emit('connect-post.json', report)
        assert report['shell_return'] is True
        assert report['fire_and_forget'] is True
        assert report['elapsed_seconds'] < 1.0
        assert report['ping'] == 3

    def test_transaction_rollback_after_interactive_routing(
        self,
        connect_probe: ConnectProbe,
    ) -> None:
        report = connect_probe.blocking(None, 'add connect')
        connect_probe.emit('connect-transaction-rollback.json', report)
        assert report['status'] == 'completed'
        assert report['rollback_coverage'] in {
            'inconclusive',
            'rolled_back',
            'persisted',
            'partial',
        }
        assert isinstance(report['after_rollback'], dict)
        assert isinstance(report['after_cleanup'], dict)
        assert report['ping'] == 3

    def test_add_connect_flag_syntax(self, connect_probe: ConnectProbe) -> None:
        routes = cast('list[dict[str, object]] | None', connect_probe.snapshot(None)['routes'])
        if not routes:
            pytest.skip('shape1.brd has no routable net')
        net = cast('str', routes[0]['net'])
        report = connect_probe.blocking(None, f'add connect -net {net} -layer ETCH/TOP -width 0.2')
        connect_probe.emit('connect-flag-syntax.json', report)
        assert report['status'] == 'completed'
        assert isinstance(report['during'], dict)
        assert report['ping'] == 3

    def test_add_connect_stays_active_after_axlshell_returns(
        self,
        connect_probe: ConnectProbe,
        connect_allegro: Allegro,
    ) -> None:
        routes = cast('list[dict[str, object]] | None', connect_probe.snapshot(None)['routes'])
        if not routes:
            pytest.skip('shape1.brd has no routable net')
        net = cast('str', routes[0]['net'])
        pin = next(iter(connect_allegro.session.pins(net=net)), None)
        if pin is None or pin.x is None or pin.y is None:
            pytest.skip(f'net {net} has no placed pin')
        start = (pin.x, pin.y)
        end = (pin.x + 1.0, pin.y + 1.0)
        report = connect_probe.active(net, f'add connect -net {net}', start, end)
        connect_probe.emit('connect-activity.json', report)
        assert report['status'] == 'completed'
        assert report['route_change'] == 'cancel'
        assert report['activity'] in {'active', 'cancelled'}
        assert report['rollback_coverage'] in {
            'inconclusive',
            'rolled_back',
            'persisted',
            'partial',
        }
        assert report['ping'] == 3

    def test_driven_add_connect_completes_route(
        self,
        connect_probe: ConnectProbe,
        connect_allegro: Allegro,
    ) -> None:
        routes = cast('list[dict[str, object]] | None', connect_probe.snapshot(None)['routes'])
        if not routes:
            pytest.skip('shape1.brd has no routable net')
        net = cast('str', routes[0]['net'])
        pin = next(iter(connect_allegro.session.pins(net=net)), None)
        if pin is None or pin.x is None or pin.y is None:
            pytest.skip(f'net {net} has no placed pin')
        start = (pin.x, pin.y)
        end = (pin.x + 1.0, pin.y + 1.0)
        report = connect_probe.driven(net, f'add connect -net {net}', start, end)
        connect_probe.emit('connect-driven.json', report)
        assert report['status'] == 'completed'
        assert report['route_change'] in {'done', 'cancel'}
        assert report['rollback_coverage'] in {
            'inconclusive',
            'rolled_back',
            'persisted',
            'partial',
        }
        assert report['ping'] == 3
