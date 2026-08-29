from __future__ import annotations

import json
import math
import runpy
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from benchmark.check_regression import compare_reports, format_report, main

_CASE = 'benchmark/test_allegro.py::test_rpc'
_CONTEXT = {
    'allegro_full_version': '17.2-2016 S048',
    'allegro_release': '17.2',
    'board_sha256': 'a' * 64,
    'board_component_count': 4,
    'board_symbol_count': 5,
    'board_net_count': 6,
}


def _report(
    path: Path,
    *,
    commit_id: str,
    median: float,
    iqr: float,
    name: str = _CASE,
) -> Path:
    path.write_text(
        json.dumps({
            'version': '5.3.0',
            'machine_info': {
                'node': 'benchmark-host',
                'system': 'Windows',
                'machine': 'AMD64',
                'python_version': '3.12.0',
            },
            'commit_info': {'id': commit_id, 'dirty': False},
            'benchmark_context': _CONTEXT,
            'benchmarks': [
                {
                    'fullname': name,
                    'stats': {'median': median, 'iqr': iqr},
                }
            ],
        }),
        encoding='utf-8',
    )
    return path


def _run_reports(
    tmp_path: Path,
    side: str,
    *,
    commit_id: str,
    medians: tuple[float, float, float],
    iqrs: tuple[float, float, float],
) -> list[Path]:
    return [
        _report(
            tmp_path / f'{side}-{index}.json',
            commit_id=commit_id,
            median=run_median,
            iqr=run_iqr,
        )
        for index, (run_median, run_iqr) in enumerate(zip(medians, iqrs, strict=True))
    ]


def _reports(tmp_path: Path) -> tuple[list[Path], list[Path]]:
    baseline = _run_reports(
        tmp_path,
        'baseline',
        commit_id='baseline-commit',
        medians=(9.0, 10.0, 11.0),
        iqrs=(0.9, 2.0, 1.1),
    )
    candidate = _run_reports(
        tmp_path,
        'candidate',
        commit_id='candidate-commit',
        medians=(11.0, 12.0, 13.0),
        iqrs=(1.1, 1.2, 2.6),
    )
    return baseline, candidate


def _rewrite(path: Path, update: Callable[[dict[str, object]], None]) -> None:
    report = json.loads(path.read_text(encoding='utf-8'))
    update(report)
    path.write_text(json.dumps(report), encoding='utf-8')


def test_compares_run_centers_and_both_noise_sources(tmp_path: Path) -> None:
    baseline, candidate = _reports(tmp_path)

    comparison = compare_reports(baseline, candidate)[0]

    assert comparison.name == _CASE
    assert comparison.baseline.center == pytest.approx(10.0)
    assert comparison.candidate.center == pytest.approx(12.0)
    assert comparison.relative_delta == pytest.approx(0.2)
    assert comparison.baseline.within_run_noise == pytest.approx(0.1)
    assert comparison.candidate.within_run_noise == pytest.approx(0.1)
    assert comparison.baseline.process_noise == pytest.approx(0.1)
    assert comparison.candidate.process_noise == pytest.approx(1 / 12)


def test_formats_a_deterministic_sorted_report(tmp_path: Path) -> None:
    baseline, candidate = _reports(tmp_path)
    for path in (*baseline, *candidate):
        report = json.loads(path.read_text(encoding='utf-8'))
        report['benchmarks'].append({
            'fullname': 'benchmark/test_allegro.py::test_a_first',
            'stats': {'median': 1.0, 'iqr': 0.0},
        })
        path.write_text(json.dumps(report), encoding='utf-8')

    output = format_report(compare_reports(baseline, candidate))

    assert output.splitlines() == [
        (
            '| benchmark | baseline median (s) | candidate median (s) | delta | '
            'baseline within | candidate within | baseline process | candidate process |'
        ),
        '|---|---:|---:|---:|---:|---:|---:|---:|',
        (
            '| benchmark/test_allegro.py::test_a_first | 1 | 1 | +0.00% | 0.00% | '
            '0.00% | 0.00% | 0.00% |'
        ),
        (
            '| benchmark/test_allegro.py::test_rpc | 10 | 12 | +20.00% | 10.00% | '
            '10.00% | 10.00% | 8.33% |'
        ),
    ]


@pytest.mark.parametrize(
    ('label', 'mutate', 'error'),
    [
        (
            'machine',
            lambda report: report.__setitem__('machine_info', {'node': 'other'}),
            'machine_info.*node',
        ),
        ('version', lambda report: report.__setitem__('version', '6.0.0'), 'version'),
        (
            'context',
            lambda report: report['benchmark_context'].__setitem__('board_net_count', 7),
            'benchmark_context.*board_net_count',
        ),
        (
            'tests',
            lambda report: report['benchmarks'][0].__setitem__('fullname', 'other'),
            'same benchmark tests',
        ),
        (
            'dirty',
            lambda report: report['commit_info'].update(dirty=True),
            'dirty',
        ),
    ],
)
def test_rejects_incomparable_reports(
    tmp_path: Path,
    label: str,
    mutate: Callable[[dict[str, object]], None],
    error: str,
) -> None:
    baseline, candidate = _reports(tmp_path)
    _rewrite(candidate[1], mutate)

    with pytest.raises(ValueError, match=error):
        compare_reports(baseline, candidate)


@pytest.mark.parametrize('side', ['baseline', 'candidate'])
def test_requires_one_commit_per_side(tmp_path: Path, side: str) -> None:
    baseline, candidate = _reports(tmp_path)
    reports = baseline if side == 'baseline' else candidate
    _rewrite(reports[1], lambda report: report['commit_info'].__setitem__('id', 'other'))

    with pytest.raises(ValueError, match=rf'{side} reports must use one commit'):
        compare_reports(baseline, candidate)


def test_requires_three_reports_per_side(tmp_path: Path) -> None:
    baseline, candidate = _reports(tmp_path)

    with pytest.raises(ValueError, match='at least 3 baseline'):
        compare_reports(baseline[:2], candidate)
    with pytest.raises(ValueError, match='at least 3 candidate'):
        compare_reports(baseline, candidate[:2])


def test_rejects_invalid_json_as_invalid_report(tmp_path: Path) -> None:
    baseline, candidate = _reports(tmp_path)
    candidate[0].write_text('{', encoding='utf-8')

    with pytest.raises(ValueError, match='invalid benchmark report'):
        compare_reports(baseline, candidate)


@pytest.mark.parametrize(
    ('mutate', 'error'),
    [
        (lambda report: report.__setitem__('machine_info', []), 'machine_info'),
        (lambda report: report.__setitem__('version', ''), 'version'),
        (lambda report: report.__setitem__('benchmark_context', []), 'benchmark_context'),
        (lambda report: report.__setitem__('benchmarks', {}), 'benchmarks'),
        (lambda report: report.__setitem__('benchmarks', []), 'must not be empty'),
        (
            lambda report: report['benchmarks'].append(report['benchmarks'][0]),
            'duplicate benchmark',
        ),
        (
            lambda report: report['benchmarks'][0]['stats'].update(median=True),
            'median must be a number',
        ),
        (
            lambda report: report['benchmarks'][0]['stats'].__setitem__('median', 0),
            'median must be a finite positive number',
        ),
        (
            lambda report: report['benchmarks'][0]['stats'].__setitem__('iqr', -1),
            'iqr must be a finite non-negative number',
        ),
        (
            lambda report: report['benchmarks'][0]['stats'].__setitem__('iqr', math.inf),
            'iqr must be a finite non-negative number',
        ),
    ],
)
def test_rejects_invalid_report_schema(
    tmp_path: Path,
    mutate: Callable[[dict[str, object]], None],
    error: str,
) -> None:
    baseline, candidate = _reports(tmp_path)
    _rewrite(candidate[0], mutate)

    with pytest.raises(ValueError, match=error):
        compare_reports(baseline, candidate)


def test_rejects_non_object_report(tmp_path: Path) -> None:
    baseline, candidate = _reports(tmp_path)
    candidate[0].write_text('[]', encoding='utf-8')

    with pytest.raises(ValueError, match='report must be a JSON object'):
        compare_reports(baseline, candidate)


def test_requires_canonical_allegro_benchmark_context(tmp_path: Path) -> None:
    baseline, candidate = _reports(tmp_path)
    for path in (*baseline, *candidate):
        _rewrite(path, lambda report: report.__setitem__('benchmark_context', {}))

    with pytest.raises(ValueError, match=r'benchmark_context\.allegro_full_version'):
        compare_reports(baseline, candidate)


@pytest.mark.parametrize(
    ('field', 'value', 'error'),
    [
        ('board_sha256', 'not-a-digest', '64 hexadecimal'),
        ('board_sha256', 'g' * 64, '64 hexadecimal'),
        ('board_component_count', True, 'non-negative integer'),
        ('board_component_count', 1.5, 'non-negative integer'),
        ('board_symbol_count', -1, 'non-negative integer'),
    ],
)
def test_validates_canonical_benchmark_context_values(
    tmp_path: Path,
    field: str,
    value: object,
    error: str,
) -> None:
    baseline, candidate = _reports(tmp_path)
    _rewrite(
        candidate[0],
        lambda report: report['benchmark_context'].__setitem__(field, value),
    )

    with pytest.raises(ValueError, match=error):
        compare_reports(baseline, candidate)


def test_cli_prints_report_and_returns_zero(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    baseline, candidate = _reports(tmp_path)

    result = main([
        '--baseline',
        *(str(path) for path in baseline),
        '--candidate',
        *(str(path) for path in candidate),
    ])

    assert result == 0
    assert f'| {_CASE} | 10 | 12 | +20.00% |' in capsys.readouterr().out


def test_cli_exits_two_for_incomparable_reports(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    baseline, candidate = _reports(tmp_path)
    _rewrite(candidate[0], lambda report: report.__setitem__('version', '6.0.0'))

    with pytest.raises(SystemExit) as exc_info:
        main([
            '--baseline',
            *(str(path) for path in baseline),
            '--candidate',
            *(str(path) for path in candidate),
        ])

    assert exc_info.value.code == 2
    assert 'version' in capsys.readouterr().err


def test_script_entrypoint_exits_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline, candidate = _reports(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'check_regression.py',
            '--baseline',
            *(str(path) for path in baseline),
            '--candidate',
            *(str(path) for path in candidate),
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(
            str(Path(__file__).parents[1] / 'benchmark' / 'check_regression.py'),
            run_name='__main__',
        )

    assert exc_info.value.code == 0
