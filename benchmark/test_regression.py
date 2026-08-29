from __future__ import annotations

import json
from pathlib import Path

import pytest

from benchmark.check_regression import regressions


def _report(path: Path, *, node: str = 'host', median: float = 10.0) -> Path:
    path.write_text(
        json.dumps({
            'machine_info': {
                'node': node,
                'system': 'Windows',
                'machine': 'AMD64',
                'python_version': '3.10.0',
            },
            'benchmarks': [
                {
                    'fullname': 'benchmark/test_allegro.py::test_rpc',
                    'stats': {'median': median, 'iqr': 2.0},
                }
            ],
        }),
        encoding='utf-8',
    )
    return path


def test_requires_two_consecutive_regressions_beyond_baseline_iqr(tmp_path: Path) -> None:
    baseline = _report(tmp_path / 'baseline.json')
    first = _report(tmp_path / 'first.json', median=13.0)
    recovered = _report(tmp_path / 'recovered.json', median=12.0)
    second = _report(tmp_path / 'second.json', median=13.0)

    assert regressions(baseline, first, recovered) == []
    assert regressions(baseline, first, second) == ['benchmark/test_allegro.py::test_rpc']


def test_rejects_different_hosts_or_test_sets(tmp_path: Path) -> None:
    baseline = _report(tmp_path / 'baseline.json')
    other_host = _report(tmp_path / 'host.json', node='other')
    other_tests = _report(tmp_path / 'tests.json')
    report = json.loads(other_tests.read_text(encoding='utf-8'))
    report['benchmarks'][0]['fullname'] = 'other'
    other_tests.write_text(json.dumps(report), encoding='utf-8')

    with pytest.raises(ValueError, match='same host'):
        regressions(baseline, other_host, baseline)
    with pytest.raises(ValueError, match='same tests'):
        regressions(baseline, other_tests, baseline)
