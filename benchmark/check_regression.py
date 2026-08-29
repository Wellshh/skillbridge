from __future__ import annotations

import argparse
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from string import hexdigits
from typing import cast

_MIN_RUNS = 3
_SHA256_HEX_LENGTH = 64
_CONTEXT_COUNT_KEYS = ('board_component_count', 'board_symbol_count', 'board_net_count')


@dataclass(frozen=True)
class SampleSummary:
    center: float
    within_run_noise: float
    process_noise: float


@dataclass(frozen=True)
class CaseComparison:
    name: str
    baseline: SampleSummary
    candidate: SampleSummary
    relative_delta: float


@dataclass(frozen=True)
class _Report:
    machine_info: dict[str, object]
    version: str
    benchmark_context: dict[str, object]
    commit_id: str
    benchmarks: dict[str, tuple[float, float]]


def _dict(value: object, field: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f'{field} must be a JSON object')
    return cast('dict[str, object]', value)


def _list(value: object, field: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f'{field} must be a JSON array')
    return cast('list[object]', value)


def _string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f'{field} must be a non-empty string')
    return value


def _number(value: object, field: str, *, positive: bool) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{field} must be a number')
    result = float(value)
    if not math.isfinite(result) or (result <= 0 if positive else result < 0):
        qualifier = 'positive' if positive else 'non-negative'
        raise ValueError(f'{field} must be a finite {qualifier} number')
    return result


def _benchmark_context(value: object) -> dict[str, object]:
    context = _dict(value, 'benchmark_context')
    _string(context.get('allegro_full_version'), 'benchmark_context.allegro_full_version')
    _string(context.get('allegro_release'), 'benchmark_context.allegro_release')
    digest = _string(context.get('board_sha256'), 'benchmark_context.board_sha256')
    if len(digest) != _SHA256_HEX_LENGTH or any(character not in hexdigits for character in digest):
        raise ValueError(
            f'benchmark_context.board_sha256 must contain {_SHA256_HEX_LENGTH} hexadecimal digits'
        )
    for key in _CONTEXT_COUNT_KEYS:
        count = context.get(key)
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError(f'benchmark_context.{key} must be a non-negative integer')
    return context


def _parse_report(raw: object) -> _Report:
    report = _dict(raw, 'report')
    machine_info = _dict(report.get('machine_info'), 'machine_info')
    version = _string(report.get('version'), 'version')
    benchmark_context = _benchmark_context(report.get('benchmark_context'))
    commit_info = _dict(report.get('commit_info'), 'commit_info')
    commit_id = _string(commit_info.get('id'), 'commit_info.id')
    if commit_info.get('dirty') is not False:
        raise ValueError('dirty benchmark reports are not comparable')

    benchmarks: dict[str, tuple[float, float]] = {}
    for index, raw_benchmark in enumerate(_list(report.get('benchmarks'), 'benchmarks')):
        benchmark = _dict(raw_benchmark, f'benchmarks[{index}]')
        name = _string(benchmark.get('fullname'), f'benchmarks[{index}].fullname')
        if name in benchmarks:
            raise ValueError(f'duplicate benchmark: {name}')
        stats = _dict(benchmark.get('stats'), f'benchmarks[{index}].stats')
        benchmarks[name] = (
            _number(stats.get('median'), f'{name}.median', positive=True),
            _number(stats.get('iqr'), f'{name}.iqr', positive=False),
        )
    if not benchmarks:
        raise ValueError('benchmarks must not be empty')

    return _Report(machine_info, version, benchmark_context, commit_id, benchmarks)


def _load(path: Path) -> _Report:
    try:
        raw: object = json.loads(path.read_text(encoding='utf-8'))
        return _parse_report(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f'invalid benchmark report {path}: {exc}') from exc


def _validate_side(label: str, reports: Sequence[_Report]) -> None:
    if len({report.commit_id for report in reports}) != 1:
        raise ValueError(f'{label} reports must use one commit')


def _different_keys(reference: dict[str, object], current: dict[str, object]) -> str:
    different = reference.keys() ^ current.keys()
    different.update(
        key for key in reference.keys() & current.keys() if reference[key] != current[key]
    )
    return ', '.join(sorted(different))


def _validate_comparable(reports: Sequence[_Report]) -> None:
    reference = reports[0]
    reference_tests = reference.benchmarks.keys()
    for report in reports[1:]:
        if report.machine_info != reference.machine_info:
            different = _different_keys(reference.machine_info, report.machine_info)
            raise ValueError(
                f'benchmark reports must have identical machine_info; different keys: {different}'
            )
        if report.version != reference.version:
            raise ValueError('benchmark reports must use the same pytest-benchmark version')
        if report.benchmark_context != reference.benchmark_context:
            different = _different_keys(reference.benchmark_context, report.benchmark_context)
            raise ValueError(
                f'benchmark reports must have identical benchmark_context; '
                f'different keys: {different}'
            )
        if report.benchmarks.keys() != reference_tests:
            raise ValueError('benchmark reports must contain the same benchmark tests')


def _summarize(samples: Sequence[tuple[float, float]]) -> SampleSummary:
    medians = [sample_median for sample_median, _ in samples]
    center = float(median(medians))
    within_run_noise = float(median(run_iqr / run_median for run_median, run_iqr in samples))
    process_mad = float(median(abs(run_median - center) for run_median in medians))
    return SampleSummary(center, within_run_noise, process_mad / center)


def compare_reports(
    baseline_paths: Sequence[Path],
    candidate_paths: Sequence[Path],
) -> list[CaseComparison]:
    if len(baseline_paths) < _MIN_RUNS:
        raise ValueError(f'at least {_MIN_RUNS} baseline reports are required')
    if len(candidate_paths) < _MIN_RUNS:
        raise ValueError(f'at least {_MIN_RUNS} candidate reports are required')

    baseline = [_load(path) for path in baseline_paths]
    candidate = [_load(path) for path in candidate_paths]
    _validate_side('baseline', baseline)
    _validate_side('candidate', candidate)
    _validate_comparable([*baseline, *candidate])

    comparisons = []
    for name in sorted(baseline[0].benchmarks):
        baseline_summary = _summarize([report.benchmarks[name] for report in baseline])
        candidate_summary = _summarize([report.benchmarks[name] for report in candidate])
        comparisons.append(
            CaseComparison(
                name=name,
                baseline=baseline_summary,
                candidate=candidate_summary,
                relative_delta=(candidate_summary.center - baseline_summary.center)
                / baseline_summary.center,
            )
        )
    return comparisons


def _format_comparison(comparison: CaseComparison) -> str:
    name = comparison.name.replace('|', r'\|')
    return (
        f'| {name} | {comparison.baseline.center:.6g} | '
        f'{comparison.candidate.center:.6g} | {comparison.relative_delta:+.2%} | '
        f'{comparison.baseline.within_run_noise:.2%} | '
        f'{comparison.candidate.within_run_noise:.2%} | '
        f'{comparison.baseline.process_noise:.2%} | '
        f'{comparison.candidate.process_noise:.2%} |'
    )


def format_report(comparisons: Sequence[CaseComparison]) -> str:
    lines = [
        (
            '| benchmark | baseline median (s) | candidate median (s) | delta | '
            'baseline within | candidate within | baseline process | candidate process |'
        ),
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ]
    lines.extend(
        _format_comparison(comparison)
        for comparison in sorted(comparisons, key=lambda item: item.name)
    )
    return '\n'.join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Compare independent pytest-benchmark reports')
    parser.add_argument('--baseline', nargs='+', required=True, type=Path)
    parser.add_argument('--candidate', nargs='+', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        comparisons = compare_reports(args.baseline, args.candidate)
    except ValueError as exc:
        parser.error(str(exc))
    print(format_report(comparisons))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
