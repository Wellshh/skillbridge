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
from tests.allegrobridge.probe.drc import (
    DrcProbe,
    _classify_coupling,
    _classify_rollback,
    _signature,
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
def drc_allegro(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Allegro]:
    if platform != 'win32':
        pytest.skip('DRC probes require the Windows board copy')
    board = Path(copy2(_TEST_BOARD, tmp_path_factory.mktemp('drc-allegro')))
    with socket() as listener:
        listener.bind(('localhost', 0))
        workspace_id = str(listener.getsockname()[1])
    with Allegro.open(mode='cli', board=board, workspace_id=workspace_id) as opened:
        yield opened


@pytest.fixture
def drc_probe(drc_allegro: Allegro) -> DrcProbe:
    return DrcProbe(drc_allegro.workspace)


def _snapshot(marker: str) -> dict[str, object]:
    return {
        'drc_enable': True,
        'drc_state': 'upToDate',
        'reported_count': 1,
        'drcs_length': 1,
        'marker_summary': [
            {
                'signature': {
                    'type': marker,
                    'name': 'name',
                    'source': 'source',
                    'layer': 'layer',
                },
                'count': 1,
            }
        ],
    }


@pytest.mark.parametrize(
    ('after', 'expected'),
    [
        ('before', 'rolled_back'),
        ('during', 'persisted'),
        ('other', 'partial'),
    ],
)
def test_classifies_observable_rollback_results(after: str, expected: str) -> None:
    before = _snapshot('before')
    during = _snapshot('during')
    snapshots = {'before': before, 'during': during, 'other': _snapshot('other')}

    assert _classify_rollback(before, during, snapshots[after]) == expected


def test_classifies_idempotent_operation_as_inconclusive() -> None:
    snapshot = _snapshot('same')

    assert _classify_rollback(snapshot, deepcopy(snapshot), _snapshot('after')) == 'inconclusive'


def test_rollback_comparison_ignores_reported_count_and_marker_order() -> None:
    before = _snapshot('before')
    before['marker_summary'] = [
        {'signature': {'type': 'b'}, 'count': 2},
        {'signature': {'type': 'a'}, 'count': 1},
    ]
    during = _snapshot('during')
    after = deepcopy(before)
    after['reported_count'] = 99
    after['marker_summary'] = list(
        reversed(cast('list[dict[str, object]]', after['marker_summary']))
    )

    assert _classify_rollback(before, during, after) == 'rolled_back'


def test_rollback_comparison_prefers_full_marker_fingerprints() -> None:
    before = _snapshot('before')
    before['marker_fingerprints'] = [['before', [1.0, 2.0]]]
    during = _snapshot('during')
    during['marker_fingerprints'] = [['during', [2.0, 3.0]]]
    after = deepcopy(before)

    assert _classify_rollback(before, during, after) == 'rolled_back'


def test_signature_rejects_protocol_drift() -> None:
    with pytest.raises(ValueError, match='expected 4 DRC signature fields, got 3'):
        _signature(['type', 'name', 'source'])


def test_probe_loads_sibling_skill_file_and_sanitizes_payload() -> None:
    workspace = FakeWorkspace({'probe': {'value': 'dbid:ABC123'}})
    probe = DrcProbe(cast('Workspace', workspace))

    assert probe._call('probe') == {'value': '<dbid>'}
    assert workspace.calls[0][0] == 'load'
    assert cast('str', workspace.calls[0][1][0]).endswith('/probe/drc.il')


def test_probe_rejects_non_mapping_payload() -> None:
    probe = DrcProbe(cast('Workspace', FakeWorkspace({'probe': []})))

    with pytest.raises(TypeError, match='probe returned list, expected dict'):
        probe._call('probe')


def test_emit_prints_and_optionally_writes_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv('ALLEGRO_DRC_PROBE_OUTPUT_DIR', str(tmp_path))

    DrcProbe.emit('report.json', {'value': 1})

    assert loads(capsys.readouterr().out) == {'value': 1}
    assert loads((tmp_path / 'report.json').read_text(encoding='utf-8')) == {'value': 1}


def test_emit_only_prints_without_output_directory(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv('ALLEGRO_DRC_PROBE_OUTPUT_DIR', raising=False)

    DrcProbe.emit('unused.json', {'value': 2})

    assert loads(capsys.readouterr().out) == {'value': 2}


def test_schema_aggregates_marker_and_attribute_variants() -> None:
    marker = {
        'signature': ['type', 'name', 'source', 'layer'],
        'attributes': [
            {'name': 'actual', 'runtime_type': 'string', 'value': 'a'},
            {'name': 'expected', 'runtime_type': 'string', 'value': 'e'},
            {'name': 'other', 'runtime_type': 'fixnum', 'value': '1'},
        ],
    }
    payload = {
        'reported_count': 2,
        'drcs_length': 2,
        'waived_length': 1,
        'current': [marker, deepcopy(marker)],
        'waived': [deepcopy(marker)],
    }
    probe = DrcProbe(cast('Workspace', FakeWorkspace({'__abpDrcSchema': payload})))

    report = probe.schema()

    current = cast('list[dict[str, object]]', report['current'])
    assert current[0]['count'] == 2
    assert report['observations'] == {
        'actual_runtime_types': ['string'],
        'expected_runtime_types': ['string'],
        'actual_always_string': True,
        'expected_always_string': True,
        'category_fields': {
            '{"layer": "layer", "name": "name", "source": "source", "type": "type"}': [
                'actual',
                'expected',
                'other',
            ]
        },
        'waived_has_independent_schema': True,
    }
    assert DrcProbe._aggregate_marker_schema(None) == []


def test_violations_aggregate_stable_and_unresolved_references() -> None:
    signature = ['type', 'name', 'source', 'layer']
    pin = {
        'id': 'object_0',
        'stable_ref': {'reference_type': 'PinRef', 'refdes': 'U1', 'number': '1'},
        'net_ref': {'reference_type': 'NetRef', 'name': 'GND'},
        'parents': [
            {
                'id': 'parent_0',
                'stable_ref': {'reference_type': 'Kind', 'kind': 'shape'},
                'net_ref': None,
            }
        ],
    }
    component = {
        'id': 'object_1',
        'stable_ref': {'reference_type': 'ComponentRef', 'refdes': 'U1'},
        'net_ref': None,
        'parents': None,
    }
    ignored = {
        'id': 'object_2',
        'stable_ref': {'reference_type': 'Kind', 'kind': 'ignored'},
        'net_ref': None,
        'parents': [],
    }
    payload = {
        'markers': [
            {'signature': signature, 'violations': [pin, component, ignored]},
            {'signature': signature, 'violations': [ignored]},
        ]
    }
    probe = DrcProbe(cast('Workspace', FakeWorkspace({'__abpDrcViolations': payload})))

    report = probe.violations()

    markers = cast('list[dict[str, object]]', report['markers'])
    summary = cast('dict[str, object]', report['reference_summary'])
    assert markers[0]['marker_count'] == 2
    assert len(cast('list[object]', markers[0]['violation_samples'])) == 2
    assert len(cast('list[object]', summary['pin_references'])) == 1
    assert summary['kinds_without_stable_business_key'] == ['shape']


def _raw_phase(marker: str) -> dict[str, object]:
    return {
        'drc_enable': True,
        'drc_state': 'upToDate',
        'reported_count': 1,
        'drcs_length': 1,
        'markers': [[marker, 'name', 'source', 'layer']],
    }


def _coupling_phase(
    x: float,
    marker: str,
    *,
    drc_state: str = 'upToDate',
) -> dict[str, object]:
    drc = _raw_phase(marker)
    drc['drc_state'] = drc_state
    return {
        'component': {'refdes': 'R1', 'x': x, 'y': 2.0, 'rotation': 0.0},
        'drc': drc,
    }


@pytest.mark.parametrize(
    ('during', 'after', 'expected'),
    [
        (_coupling_phase(2.0, 'during'), _coupling_phase(1.0, 'before'), 'rolled_back'),
        (_coupling_phase(1.0, 'before'), _coupling_phase(1.0, 'before'), 'inconclusive'),
        (_coupling_phase(2.0, 'before'), _coupling_phase(1.0, 'before'), 'inconclusive'),
        (_coupling_phase(1.0, 'during'), _coupling_phase(1.0, 'before'), 'inconclusive'),
        (
            _coupling_phase(2.0, 'before', drc_state='outOfDate'),
            _coupling_phase(1.0, 'before'),
            'inconclusive',
        ),
        (_coupling_phase(2.0, 'during'), _coupling_phase(2.0, 'during'), 'persisted'),
        (_coupling_phase(2.0, 'during'), _coupling_phase(1.0, 'other'), 'partial'),
    ],
)
def test_classifies_database_and_drc_coupling(
    during: dict[str, object],
    after: dict[str, object],
    expected: str,
) -> None:
    assert _classify_coupling(_coupling_phase(1.0, 'before'), during, after) == expected


def test_update_and_stable_keys_project_reports() -> None:
    update = {
        phase: _raw_phase(phase)
        for phase in ('before', 'disabled', 'after_update', 'after_restore')
    }
    keys = {
        'allegro_version': '17.2',
        'component': {'refdes': 'U1'},
        'net': {'name': 'GND'},
        'pin': {'refdes': 'U1', 'number': '1'},
    }
    probe = DrcProbe(
        cast(
            'Workspace',
            FakeWorkspace({
                '__abpDrcUpdate': update,
                '__abpDrcStableKeys': keys,
            }),
        )
    )

    report = probe.update()

    assert 'marker_summary' in cast('dict[str, object]', report['before'])
    assert probe.stable_keys() == keys


def test_item_resolves_stable_scalar_keys_and_normalizes_markers() -> None:
    keys = {
        'allegro_version': '17.2',
        'component': {'refdes': 'U1'},
        'net': {'name': 'GND'},
        'pin': {'refdes': 'U1', 'number': '1'},
    }

    def item(
        kind: str,
        refdes: str | None,
        name: str | None,
        number: str | None,
    ) -> dict[str, object]:
        missing = any(value and value.startswith('__MISSING') for value in (refdes, name, number))
        if missing:
            return {'status': 'missing', 'kind': kind}
        marker = {
            'type': 'type',
            'name': 'name',
            'source': 'source',
            'layer': 'layer',
            'actual': 'actual',
            'expected': 'expected',
            'xy': [0, 0],
            'bBox': [[0, 0], [1, 1]],
        }
        return {
            'status': 'found',
            'kind': kind,
            'count': 1,
            'marker_list_length': 1,
            'markers': None if kind == 'component' else [marker],
        }

    workspace = FakeWorkspace({
        '__abpDrcStableKeys': keys,
        '__abpDrcItem': item,
        'plus': 3,
    })
    probe = DrcProbe(cast('Workspace', workspace))

    report = probe.item()

    objects = cast('list[dict[str, object]]', report['objects'])
    assert objects[0]['markers'] == []
    assert all(item['count_matches_marker_list_length'] for item in objects[1:])
    assert report['ping'] == 3
    assert [call[1] for call in workspace.calls if call[0] == '__abpDrcItem'][:3] == [
        ('component', 'U1', None, None),
        ('component', '__MISSING_DRC_COMPONENT__', None, None),
        ('net', None, 'GND', None),
    ]


def test_cleanup_reports_expected_fault_and_server_health() -> None:
    status = {
        'allegro_version': '17.2',
        'drc_enable': True,
        'drc_state': 'upToDate',
        'reported_count': 1,
    }

    def fault() -> None:
        raise RuntimeError('DRC_CLEANUP_PROBE_ERROR dbid:ABC')

    probe = DrcProbe(
        cast(
            'Workspace',
            FakeWorkspace({
                '__abpDrcStatus': status,
                '__abpDrcFault': fault,
                'plus': 3,
            }),
        )
    )

    report = probe.cleanup()

    assert cast('dict[str, object]', report['restored'])['ping'] == 3
    assert '<dbid>' in cast('dict[str, str]', report['python_error'])['message']


@pytest.mark.parametrize(
    'fault',
    [lambda: None, lambda: (_ for _ in ()).throw(RuntimeError('unexpected'))],
)
def test_cleanup_rejects_missing_or_unexpected_fault(fault: Callable[[], None]) -> None:
    status = {
        'allegro_version': '17.2',
        'drc_enable': True,
        'drc_state': 'upToDate',
        'reported_count': 1,
    }
    probe = DrcProbe(
        cast(
            'Workspace',
            FakeWorkspace({
                '__abpDrcStatus': status,
                '__abpDrcFault': fault,
            }),
        )
    )

    with pytest.raises((AssertionError, RuntimeError)):
        probe.cleanup()


def test_transaction_report_classifies_completed_and_failed_runs() -> None:
    completed = {
        'status': 'completed',
        'before': _raw_phase('before'),
        'during': _raw_phase('during'),
        'after_rollback': _raw_phase('before'),
        'after_cleanup': _raw_phase('before'),
    }
    failed = {
        'status': 'start_failed',
        'before': _raw_phase('before'),
        'during': None,
        'after_rollback': None,
        'after_cleanup': _raw_phase('before'),
    }
    workspace = FakeWorkspace({'__abpDrcTransactionRollback': completed, 'plus': 3})
    probe = DrcProbe(cast('Workspace', workspace))

    assert probe.transaction_rollback()['classification'] == 'rolled_back'
    workspace.payloads['__abpDrcTransactionRollback'] = failed
    assert probe.transaction_rollback()['classification'] == 'failed'


def test_convergence_report_compares_direct_and_transaction_cycles() -> None:
    baseline = {**_raw_phase('baseline'), 'dynamic_ood_count': 1}
    changed = {**_raw_phase('changed'), 'dynamic_ood_count': 1}
    completed = {
        'status': 'completed',
        'baseline': deepcopy(baseline),
        'after_direct': deepcopy(baseline),
        'commit_cycles': [
            {
                'status': 'completed',
                'before': deepcopy(baseline),
                'during': deepcopy(changed),
                'after_commit': deepcopy(changed),
            }
        ],
        'cycles': [
            {
                'status': 'completed',
                'before': deepcopy(baseline),
                'during': deepcopy(changed),
                'after_rollback': deepcopy(baseline),
            }
        ],
        'after_cycles': deepcopy(baseline),
        'after_post_update': deepcopy(baseline),
    }
    workspace = FakeWorkspace({'__abpDrcConvergence': completed, 'plus': 3})
    probe = DrcProbe(cast('Workspace', workspace))

    report = probe.convergence(rounds=3)

    observations = cast('dict[str, object]', report['observations'])
    commit_cycles = cast('list[dict[str, object]]', report['commit_cycles'])
    cycles = cast('list[dict[str, object]]', report['cycles'])
    assert observations['direct_update_stable'] is True
    assert observations['post_update_stable'] is True
    assert commit_cycles[0]['marker_classification'] == 'persisted'
    assert commit_cycles[0]['dynamic_shape_classification'] == 'inconclusive'
    assert commit_cycles[0]['marker_terminal_matches_operation'] is True
    assert cycles[0]['marker_classification'] == 'rolled_back'
    assert cycles[0]['dynamic_shape_classification'] == 'inconclusive'
    assert cycles[0]['marker_terminal_matches_before'] is True
    assert cycles[0]['dynamic_shape_terminal_matches_before'] is True
    assert report['ping'] == 3
    assert workspace.calls[-2] == ('__abpDrcConvergence', (3,))


def test_database_coupling_selects_sorted_components_and_classifies_report() -> None:
    completed = {
        'status': 'completed',
        'before': _coupling_phase(1.0, 'before'),
        'during': _coupling_phase(2.0, 'during'),
        'after_rollback': _coupling_phase(1.0, 'before'),
        'after_cleanup': _coupling_phase(1.0, 'before'),
    }
    workspace = FakeWorkspace({
        '__abProjectComponents': [
            {'refdes': 'R2', 'x': 2.0, 'y': 2.0},
            {'refdes': 'R1', 'x': 1.0, 'y': 1.0},
        ],
        '__abpDrcDatabaseCoupling': completed,
        'plus': 3,
    })
    probe = DrcProbe(cast('Workspace', workspace))

    report = probe.database_coupling()

    assert report['classification'] == 'rolled_back'
    assert report['ping'] == 3
    assert workspace.calls[-2] == ('__abpDrcDatabaseCoupling', ('R1', 'R2'))
    workspace.payloads['__abpDrcDatabaseCoupling'] = {
        'status': 'start_failed',
        'before': _coupling_phase(1.0, 'before'),
        'during': None,
        'after_rollback': None,
        'after_cleanup': _coupling_phase(1.0, 'before'),
    }
    assert probe.database_coupling()['classification'] == 'failed'


def test_database_coupling_requires_two_placed_components() -> None:
    probe = DrcProbe(
        cast(
            'Workspace',
            FakeWorkspace({'__abProjectComponents': [{'refdes': 'R1', 'x': 1.0, 'y': 1.0}]}),
        )
    )

    with pytest.raises(AssertionError, match='two placed components'):
        probe.database_coupling()


@pytest.mark.allegro
class TestDrcProbe:
    def test_reports_current_marker_schema(self, drc_probe: DrcProbe) -> None:
        report = drc_probe.schema()
        drc_probe.emit('drc-schema.json', report)
        assert isinstance(report['reported_count'], int)
        assert isinstance(report['drcs_length'], int)
        assert isinstance(report['waived_length'], int)
        assert report['current']
        assert isinstance(report['observations'], dict)

    def test_reports_violation_schema_and_references(self, drc_probe: DrcProbe) -> None:
        report = drc_probe.violations()
        drc_probe.emit('drc-violations.json', report)
        assert isinstance(report['reported_count'], int)
        assert isinstance(report['markers'], list)
        assert isinstance(report['reference_summary'], dict)

    def test_updates_drc_and_restores_control(
        self,
        drc_probe: DrcProbe,
        drc_allegro: Allegro,
    ) -> None:
        report = drc_probe.update()
        cleanup = drc_allegro.workspace['evalstring'](
            "(list nil 'enabled (axlDBControl 'drcEnable) "
            "'state (sprintf nil \"%L\" (axlDBRefreshId (axlDBGetDesign))->drcState) "
            "'count (axlDRCGetCount) 'ping (plus 1 2))"
        )
        report['cleanup'] = cleanup
        drc_probe.emit('drc-update.json', report)
        assert all(
            name in report for name in ('before', 'disabled', 'after_update', 'after_restore')
        )
        assert isinstance(cleanup, dict)
        assert cleanup['ping'] == 3
        before = cast('dict[str, object]', report['before'])
        assert cleanup['enabled'] == before['drc_enable']

    def test_runs_drc_item_for_component_net_and_pin(self, drc_probe: DrcProbe) -> None:
        report = drc_probe.item()
        drc_probe.emit('drc-item.json', report)
        objects = cast('list[dict[str, object]]', report['objects'])
        missing_objects = cast('list[dict[str, object]]', report['missing_objects'])
        assert [item['kind'] for item in objects] == ['component', 'net', 'pin']
        assert all(item['status'] == 'found' for item in objects)
        assert all(item['status'] == 'missing' for item in missing_objects)
        assert all(isinstance(item['count'], int) for item in objects)
        assert all(isinstance(item['markers'], list) for item in objects)
        assert report['ping'] == 3
        assert len({item['ending_drc_enable'] for item in objects + missing_objects}) == 1

    def test_restores_drc_after_error(self, drc_probe: DrcProbe) -> None:
        report = drc_probe.cleanup()
        drc_probe.emit('drc-cleanup.json', report)
        assert report['python_error']
        assert isinstance(report['restored'], dict)
        restored = cast('dict[str, object]', report['restored'])
        before = cast('dict[str, object]', report['before'])
        assert restored['ping'] == 3
        assert restored['drc_enable'] == before['drc_enable']

    def test_reports_transaction_rollback_behavior(self, drc_probe: DrcProbe) -> None:
        report = drc_probe.transaction_rollback()
        drc_probe.emit('drc-transaction-rollback.json', report)
        assert report['status'] == 'completed'
        assert report['classification'] in {
            'inconclusive',
            'rolled_back',
            'persisted',
            'partial',
        }
        assert report['ping'] == 3
        before = cast('dict[str, object]', report['before'])
        after_cleanup = cast('dict[str, object]', report['after_cleanup'])
        assert after_cleanup['drc_enable'] == before['drc_enable']

    def test_reports_update_preview_convergence(self, drc_probe: DrcProbe) -> None:
        report = drc_probe.convergence(rounds=5)
        drc_probe.emit('drc-preview-convergence.json', report)
        assert report['status'] == 'completed'
        assert report['ping'] == 3
        cycles = cast('list[dict[str, object]]', report['cycles'])
        commit_cycles = cast('list[dict[str, object]]', report['commit_cycles'])
        assert len(cycles) == 5
        assert len(commit_cycles) == 5
        assert all(cycle['status'] == 'completed' for cycle in cycles)
        assert all(cycle['status'] == 'completed' for cycle in commit_cycles)
        assert all(cycle['rollback_result'] is True for cycle in cycles)
        assert all(cycle['commit_result'] is True for cycle in commit_cycles)
        assert all(cycle['marker_terminal_matches_before'] is True for cycle in cycles)
        assert all(cycle['dynamic_shape_terminal_matches_before'] is True for cycle in cycles)

    def test_reports_database_write_drc_coupling_and_rollback(
        self,
        drc_probe: DrcProbe,
    ) -> None:
        report = drc_probe.database_coupling()
        drc_probe.emit('drc-database-coupling.json', report)
        assert report['status'] == 'completed'
        assert report['classification'] == 'rolled_back'
        assert report['ping'] == 3
        before = cast('dict[str, object]', report['before'])
        during = cast('dict[str, object]', report['during'])
        after_cleanup = cast('dict[str, object]', report['after_cleanup'])
        assert during['component'] != before['component']
        assert during['drc'] != before['drc']
        assert after_cleanup['component'] == before['component']
        before_drc = cast('dict[str, object]', before['drc'])
        during_drc = cast('dict[str, object]', during['drc'])
        after_drc = cast('dict[str, object]', after_cleanup['drc'])
        assert during_drc['marker_fingerprints'] != before_drc['marker_fingerprints']
        assert after_drc['marker_fingerprints'] == before_drc['marker_fingerprints']
        assert after_drc['drc_enable'] == report['original_drc_enable']
