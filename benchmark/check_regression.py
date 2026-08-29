from __future__ import annotations

import argparse
import json
from pathlib import Path

_MACHINE_KEYS = ('node', 'system', 'machine', 'python_version')


def _load(path: Path) -> tuple[tuple[object, ...], dict[str, tuple[float, float]]]:
    report = json.loads(path.read_text(encoding='utf-8'))
    machine = tuple(report['machine_info'][key] for key in _MACHINE_KEYS)
    stats = {
        benchmark['fullname']: (benchmark['stats']['median'], benchmark['stats']['iqr'])
        for benchmark in report['benchmarks']
    }
    return machine, stats


def regressions(baseline_path: Path, first_path: Path, second_path: Path) -> list[str]:
    baseline_machine, baseline = _load(baseline_path)
    first_machine, first = _load(first_path)
    second_machine, second = _load(second_path)
    if baseline_machine != first_machine or baseline_machine != second_machine:
        raise ValueError('benchmark reports must come from the same host and Python runtime')
    if baseline.keys() != first.keys() or baseline.keys() != second.keys():
        raise ValueError('benchmark reports must contain the same tests')
    return sorted(
        name
        for name, (median, iqr) in baseline.items()
        if first[name][0] > median + iqr and second[name][0] > median + iqr
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('baseline', type=Path)
    parser.add_argument('first', type=Path)
    parser.add_argument('second', type=Path)
    args = parser.parse_args()
    failed = regressions(args.baseline, args.first, args.second)
    if failed:
        parser.error(f'consecutive median regression beyond baseline IQR: {", ".join(failed)}')


if __name__ == '__main__':
    main()
