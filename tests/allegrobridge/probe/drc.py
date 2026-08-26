# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from json import dumps
from os import getenv
from pathlib import Path
from re import sub
from typing import cast

from allegrobridge import Workspace
from skillbridge.client.hints import Skill

_SIGNATURE_FIELDS = ('type', 'name', 'source', 'layer')


def _signature(values: list[object]) -> dict[str, object]:
    if len(values) != len(_SIGNATURE_FIELDS):
        raise ValueError(
            f'expected {len(_SIGNATURE_FIELDS)} DRC signature fields, got {len(values)}'
        )
    return dict(zip(_SIGNATURE_FIELDS, values))


def _sanitize(value: object) -> object:
    if isinstance(value, str):
        return sub(r'\b[A-Za-z][A-Za-z0-9_]*:[0-9A-Fa-f]+\b', '<dbid>', value)
    if isinstance(value, list):
        return [_sanitize(child) for child in value]
    if isinstance(value, dict):
        return {key: _sanitize(child) for key, child in value.items()}
    return value


def _marker_fingerprint(snapshot: dict[str, object]) -> tuple[str, ...]:
    marker_values = snapshot.get('marker_fingerprints')
    if marker_values is None:
        marker_values = snapshot.get('marker_summary')
    if marker_values is None:
        marker_values = snapshot['markers']
    return tuple(
        sorted(
            dumps(marker, sort_keys=True, separators=(',', ':'))
            for marker in cast('list[object]', marker_values)
        )
    )


def _snapshot_fingerprint(snapshot: dict[str, object]) -> tuple[object, object, tuple[str, ...]]:
    return snapshot['drc_state'], snapshot['drcs_length'], _marker_fingerprint(snapshot)


def _classify_rollback(
    before: dict[str, object],
    during: dict[str, object],
    after: dict[str, object],
) -> str:
    before_state = _snapshot_fingerprint(before)
    during_state = _snapshot_fingerprint(during)
    after_state = _snapshot_fingerprint(after)
    if during_state == before_state:
        return 'inconclusive'
    if after_state == before_state:
        return 'rolled_back'
    if after_state == during_state:
        return 'persisted'
    return 'partial'


def _classify_coupling(
    before: dict[str, object],
    during: dict[str, object],
    after: dict[str, object],
) -> str:
    before_component = dumps(before['component'], sort_keys=True)
    during_component = dumps(during['component'], sort_keys=True)
    after_component = dumps(after['component'], sort_keys=True)
    before_drc = _marker_fingerprint(cast('dict[str, object]', before['drc']))
    during_drc = _marker_fingerprint(cast('dict[str, object]', during['drc']))
    after_drc = _marker_fingerprint(cast('dict[str, object]', after['drc']))
    if during_component == before_component or during_drc == before_drc:
        return 'inconclusive'
    if after_component == before_component and after_drc == before_drc:
        return 'rolled_back'
    if after_component == during_component and after_drc == during_drc:
        return 'persisted'
    return 'partial'


def _classify_item_scenario(report: dict[str, object]) -> str:
    if report['status'] != 'completed':
        return 'failed'
    before = cast('dict[str, object]', report['before'])
    after_move = cast('dict[str, object]', report['after_move'])
    if _marker_fingerprint(cast('dict[str, object]', before['drc'])) != _marker_fingerprint(
        cast('dict[str, object]', after_move['drc'])
    ):
        return 'pre_item_changed'
    classification = _classify_coupling(
        before,
        cast('dict[str, object]', report['during']),
        cast('dict[str, object]', report['after_terminal']),
    )
    if report['mode'] == 'commit' and classification == 'persisted':
        return 'committed'
    return classification


class DrcProbe:
    def __init__(self, workspace: Workspace) -> None:
        self.workspace = workspace
        workspace['load'](Path(__file__).with_suffix('.il').resolve().as_posix())

    def _call(self, procedure: str, *args: Skill) -> dict[str, object]:
        payload = self.workspace[procedure](*args)
        if not isinstance(payload, dict):
            raise TypeError(f'{procedure} returned {type(payload).__name__}, expected dict')
        report = cast('dict[str, object]', _sanitize(payload))
        dumps(report)
        return report

    @staticmethod
    def emit(filename: str, report: dict[str, object]) -> None:
        payload = dumps(report, sort_keys=True, separators=(',', ':'))
        print(payload)
        if output_directory := getenv('ALLEGRO_DRC_PROBE_OUTPUT_DIR'):
            path = Path(output_directory)
            path.mkdir(parents=True, exist_ok=True)
            (path / filename).write_text(payload + '\n', encoding='utf-8')

    @staticmethod
    def _aggregate_marker_schema(markers: object) -> list[dict[str, object]]:
        grouped: dict[str, dict[str, object]] = {}
        for marker in cast('list[dict[str, object]]', markers or []):
            signature_values = cast('list[object]', marker['signature'])
            signature = _signature(signature_values)
            signature_key = dumps(signature, sort_keys=True)
            group = grouped.setdefault(
                signature_key,
                {'signature': signature, 'count': 0, 'attributes': {}},
            )
            group['count'] = cast('int', group['count']) + 1
            attributes = cast('dict[str, dict[str, object]]', group['attributes'])
            for attribute in cast('list[dict[str, object]]', marker['attributes']):
                variant_key = dumps(
                    [attribute['name'], attribute['runtime_type'], attribute['value']],
                    sort_keys=True,
                )
                variant = attributes.setdefault(variant_key, {**attribute, 'count': 0})
                variant['count'] = cast('int', variant['count']) + 1
        result: list[dict[str, object]] = []
        for group in grouped.values():
            group['attributes'] = list(cast('dict[str, object]', group['attributes']).values())
            result.append(group)
        return result

    @staticmethod
    def _summarize_phase(phase: dict[str, object]) -> None:
        signatures: dict[str, dict[str, object]] = {}
        for values in cast('list[list[object]]', phase.pop('markers')):
            signature = _signature(values)
            key = dumps(signature, sort_keys=True)
            group = signatures.setdefault(key, {'signature': signature, 'count': 0})
            group['count'] = cast('int', group['count']) + 1
        phase['marker_summary'] = list(signatures.values())

    def schema(self) -> dict[str, object]:
        report = self._call('__abpDrcSchema')
        report['current'] = self._aggregate_marker_schema(report['current'])
        report['waived'] = self._aggregate_marker_schema(report['waived'])
        all_groups = cast('list[dict[str, object]]', report['current']) + cast(
            'list[dict[str, object]]', report['waived']
        )
        field_types: dict[str, set[str]] = {'actual': set(), 'expected': set()}
        category_fields: dict[str, list[str]] = {}
        for group in all_groups:
            signature_key = dumps(group['signature'], sort_keys=True)
            names: set[str] = set()
            for attribute in cast('list[dict[str, object]]', group['attributes']):
                name = cast('str', attribute['name'])
                names.add(name)
                if name.casefold() in field_types:
                    field_types[name.casefold()].add(cast('str', attribute['runtime_type']))
            category_fields[signature_key] = sorted(names)
        report['observations'] = {
            'actual_runtime_types': sorted(field_types['actual']),
            'expected_runtime_types': sorted(field_types['expected']),
            'actual_always_string': field_types['actual'] == {'string'},
            'expected_always_string': field_types['expected'] == {'string'},
            'category_fields': category_fields,
            'waived_has_independent_schema': bool(report['waived']),
        }
        return report

    def violations(self) -> dict[str, object]:
        report = self._call('__abpDrcViolations')
        grouped: dict[str, dict[str, object]] = {}
        stable_refs: list[dict[str, object]] = []
        net_paths: list[dict[str, object]] = []
        pin_refs: list[dict[str, object]] = []
        unresolved: set[str] = set()
        for marker in cast('list[dict[str, object]]', report['markers']):
            signature_values = cast('list[object]', marker['signature'])
            signature = _signature(signature_values)
            signature_key = dumps(signature, sort_keys=True)
            group = grouped.setdefault(
                signature_key,
                {'signature': signature, 'marker_count': 0, 'violation_samples': []},
            )
            group['marker_count'] = cast('int', group['marker_count']) + 1
            samples = cast('list[dict[str, object]]', group['violation_samples'])
            for violation in cast('list[dict[str, object]]', marker['violations']):
                if len(samples) < 2:
                    samples.append(violation)
        for group in grouped.values():
            for violation in cast('list[dict[str, object]]', group['violation_samples']):
                nodes = [(violation['id'], violation)] + [
                    (parent['id'], parent)
                    for parent in cast('list[dict[str, object]]', violation['parents'] or [])
                ]
                for path, node in nodes:
                    stable_ref = cast('dict[str, object]', node['stable_ref'])
                    if stable_ref['reference_type'] == 'Kind':
                        unresolved.add(cast('str', stable_ref['kind']))
                    else:
                        observation = {
                            'signature': group['signature'],
                            'path': path,
                            'reference': stable_ref,
                        }
                        stable_refs.append(observation)
                        if stable_ref['reference_type'] == 'PinRef':
                            pin_refs.append(observation)
                    if node['net_ref']:
                        net_paths.append({
                            'signature': group['signature'],
                            'path': path,
                            'reference': node['net_ref'],
                        })
        report['markers'] = list(grouped.values())
        report['reference_summary'] = {
            'stable_references': stable_refs,
            'net_resolution_paths': net_paths,
            'pin_references': pin_refs,
            'kinds_without_stable_business_key': sorted(unresolved),
        }
        return report

    def update(self) -> dict[str, object]:
        report = self._call('__abpDrcUpdate')
        for phase_name in ('before', 'disabled', 'after_update', 'after_restore'):
            self._summarize_phase(cast('dict[str, object]', report[phase_name]))
        return report

    def stable_keys(self) -> dict[str, object]:
        return self._call('__abpDrcStableKeys')

    def item_for(self, kind: str, key: dict[str, object]) -> dict[str, object]:
        report = self._call(
            '__abpDrcItem',
            kind,
            cast('str | None', key.get('refdes')),
            cast('str | None', key.get('name')),
            cast('str | None', key.get('number')),
        )
        if report['status'] == 'found' and report['markers'] is None:
            report['markers'] = []
        return report

    def item(self) -> dict[str, object]:
        keys = self.stable_keys()
        observations: list[dict[str, object]] = []
        missing_observations: list[dict[str, object]] = []
        missing_keys: dict[str, dict[str, object]] = {
            'component': {'refdes': '__MISSING_DRC_COMPONENT__'},
            'net': {'name': '__MISSING_DRC_NET__'},
            'pin': {'refdes': '__MISSING_DRC_COMPONENT__', 'number': '__MISSING_PIN__'},
        }
        for kind in ('component', 'net', 'pin'):
            key = keys[kind]
            assert isinstance(key, dict), f'shape1.brd has no stable {kind} key'
            observations.append(self.item_for(kind, cast('dict[str, object]', key)))
            missing_observations.append(self.item_for(kind, missing_keys[kind]))
        for observation in observations:
            markers = cast('list[dict[str, object]]', observation['markers'])
            observation['count_matches_marker_list_length'] = (
                observation['count'] == observation['marker_list_length']
            )
            observation['markers_match_drc_info_fields'] = all(
                {'type', 'name', 'source', 'layer', 'actual', 'expected', 'xy', 'bBox'}
                <= marker.keys()
                for marker in markers
            )
        return {
            'allegro_version': keys['allegro_version'],
            'stable_keys': {kind: keys[kind] for kind in ('component', 'net', 'pin')},
            'objects': observations,
            'missing_objects': missing_observations,
        }

    def cleanup(self) -> dict[str, object]:
        before = self._call('__abpDrcStatus')
        python_error: dict[str, str] = {}
        try:
            self.workspace['__abpDrcFault']()
        except RuntimeError as error:
            if 'DRC_CLEANUP_PROBE_ERROR' not in str(error):
                raise
            python_error = {
                'type': type(error).__name__,
                'message': str(error),
                'repr': repr(error),
            }
        else:
            raise AssertionError('__abpDrcFault did not raise')
        restored = self._call('__abpDrcStatus')
        restored.pop('allegro_version')
        restored['ping'] = self.workspace['plus'](1, 2)
        return cast(
            'dict[str, object]',
            _sanitize({
                'allegro_version': before['allegro_version'],
                'before': before,
                'python_error': python_error,
                'restored': restored,
                'touched_state': ['drcEnable'],
                'selection_or_find_filter_operations': [],
            }),
        )

    def transaction_rollback(self) -> dict[str, object]:
        report = self._call('__abpDrcTransactionRollback')
        for phase_name in ('before', 'during', 'after_rollback', 'after_cleanup'):
            phase = report.get(phase_name)
            if isinstance(phase, dict):
                self._summarize_phase(cast('dict[str, object]', phase))
        if report['status'] == 'completed':
            report['classification'] = _classify_rollback(
                cast('dict[str, object]', report['before']),
                cast('dict[str, object]', report['during']),
                cast('dict[str, object]', report['after_rollback']),
            )
        else:
            report['classification'] = 'failed'
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def _placed_component_pair(self) -> tuple[dict[str, object], dict[str, object]]:
        include_unplaced = False
        components = cast(
            'list[dict[str, object]]',
            self.workspace['__abProjectComponents'](None, include_unplaced),
        )
        components.sort(key=lambda component: cast('str', component['refdes']))
        assert components, 'shape1.brd requires two placed components at distinct locations'
        source = components[0]
        targets = [
            component
            for component in components[1:]
            if (component['x'], component['y']) != (source['x'], source['y'])
        ]
        assert targets, 'shape1.brd requires two placed components at distinct locations'
        return source, targets[0]

    def database_coupling(self) -> dict[str, object]:
        source, target = self._placed_component_pair()
        report = self._call(
            '__abpDrcDatabaseCoupling',
            cast('str', source['refdes']),
            cast('str', target['refdes']),
        )
        for phase_name in ('before', 'during', 'after_rollback', 'after_cleanup'):
            phase = report.get(phase_name)
            if isinstance(phase, dict):
                drc = cast('dict[str, object]', phase['drc'])
                self._summarize_phase(drc)
        if report['status'] == 'completed':
            report['classification'] = _classify_coupling(
                cast('dict[str, object]', report['before']),
                cast('dict[str, object]', report['during']),
                cast('dict[str, object]', report['after_rollback']),
            )
        else:
            report['classification'] = 'failed'
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def _item_transaction_scenario(
        self,
        mode: str,
        key: dict[str, object],
        source_refdes: str,
        target_refdes: str,
    ) -> dict[str, object]:
        report = self._call(
            '__abpDrcItemTransactionScenario',
            mode,
            cast('str', key['kind']),
            cast('str | None', key.get('refdes')),
            cast('str | None', key.get('name')),
            cast('str | None', key.get('number')),
            source_refdes,
            target_refdes,
        )
        for phase_name in ('before', 'after_move', 'during', 'after_terminal', 'after_cleanup'):
            phase = report.get(phase_name)
            if isinstance(phase, dict):
                self._summarize_phase(cast('dict[str, object]', phase['drc']))
        report['classification'] = _classify_item_scenario(report)
        report['key'] = key
        return report

    def item_transaction(self) -> dict[str, object]:
        source, target = self._placed_component_pair()
        source_refdes = cast('str', source['refdes'])
        target_refdes = cast('str', target['refdes'])
        candidates = cast(
            'list[dict[str, object]]',
            self._call('__abpDrcItemCandidates', source_refdes)['candidates'],
        )
        discovery = [
            self._item_transaction_scenario(
                'rollback',
                key,
                source_refdes,
                target_refdes,
            )
            for key in candidates
        ]
        selected = next(
            (
                cast('dict[str, object]', scenario['key'])
                for scenario in discovery
                if scenario['classification'] == 'rolled_back'
            ),
            None,
        )
        commit = None
        error = None
        classification = 'inconclusive'
        if selected is not None:
            commit = self._item_transaction_scenario(
                'commit', selected, source_refdes, target_refdes
            )
            error = self._item_transaction_scenario('error', selected, source_refdes, target_refdes)
            if commit['classification'] == 'committed' and error['classification'] == 'rolled_back':
                classification = 'verified'
        return {
            'allegro_version': discovery[0].get('allegro_version') if discovery else None,
            'source_refdes': source_refdes,
            'target_refdes': target_refdes,
            'classification': classification,
            'selected': selected,
            'discovery': discovery,
            'commit': commit,
            'error': error,
            'ping': self.workspace['plus'](1, 2),
        }
