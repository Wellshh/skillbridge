from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import query_cost
import skill_lint_corpus

BASELINE_PATH = Path(__file__).resolve().parent / 'baseline.json'


def build_score() -> dict:
    query = query_cost.measure_query_cost()
    lint = skill_lint_corpus.measure_skill_lint()
    return {
        'query_bytes_sliced': query['query_bytes_sliced'],
        'query_bytes_whole_chapter': query['query_bytes_whole_chapter'],
        'skill_lint': {
            'catch_rate': lint['catch_rate'],
            'fp_rate': lint['fp_rate'],
            'valid_count': lint['valid_count'],
            'invalid_count': lint['invalid_count'],
        },
    }


def regressions(current: dict, baseline: dict) -> list[str]:
    diffs = []
    if current['query_bytes_sliced'] > baseline['query_bytes_sliced']:
        diffs.append(
            f"query_bytes_sliced {baseline['query_bytes_sliced']}"
            f" -> {current['query_bytes_sliced']}"
        )
    if current['skill_lint']['fp_rate'] > baseline['skill_lint']['fp_rate']:
        diffs.append(
            f"fp_rate {baseline['skill_lint']['fp_rate']} -> {current['skill_lint']['fp_rate']}"
        )
    if current['skill_lint']['catch_rate'] < baseline['skill_lint']['catch_rate']:
        diffs.append(
            f"catch_rate {baseline['skill_lint']['catch_rate']}"
            f" -> {current['skill_lint']['catch_rate']}"
        )
    return diffs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='cadence-skill-agent flow benchmark.')
    parser.add_argument('--check', action='store_true', help='compare score against baseline')
    parser.add_argument('--baseline', action='store_true', help='write current score to baseline')
    args = parser.parse_args(argv)

    current = build_score()

    if args.baseline:
        BASELINE_PATH.write_text(json.dumps(current, indent=2) + '\n', encoding='utf-8')
        print(f'wrote {BASELINE_PATH}')
        return 0

    if args.check:
        baseline = json.loads(BASELINE_PATH.read_text(encoding='utf-8'))
        diffs = regressions(current, baseline)
        comparison = (
            f"query_bytes_sliced {baseline['query_bytes_sliced']} -> {current['query_bytes_sliced']}"
            f" | fp_rate {baseline['skill_lint']['fp_rate']} -> {current['skill_lint']['fp_rate']}"
            f" | catch_rate {baseline['skill_lint']['catch_rate']}"
            f" -> {current['skill_lint']['catch_rate']}"
        )
        print(f"{'REGRESSED' if diffs else 'OK'}: {comparison}")
        return 1 if diffs else 0

    print(json.dumps(current))
    return 0


if __name__ == '__main__':
    sys.exit(main())
