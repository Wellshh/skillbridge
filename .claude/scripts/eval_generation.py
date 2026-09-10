#!/usr/bin/env python3
"""Generation-quality eval: score a directory of agent-written SKILL files.

``validate_skill_api.py`` measures the validator's false-positive rate over
vendor examples; this harness measures the *agent's* hallucination rate over
code the agent itself produced.  Point ``--samples`` at any directory of
``.il``/``.ils`` files (harvested from real agent runs); every file is checked
against the corpus with the same validator used in the generation loop.

Metrics
-------
``files_with_errors`` / ``unknown_api_errors``
    the headline hallucination signal: calls to ``axl*`` names that exist in
    no corpus index.  These must trend to zero.
``hallucination_rate``
    ``unknown_api_errors / files`` - how many invented APIs per delivered file.
``arity_warnings`` / ``keyword_warnings``
    softer signals: the agent used a real API with an undocumented shape.
``expected_api_missing``
    per-task list of corpus-documented APIs the sample avoided (needs an
    ``eval_tasks.json`` manifest in the samples directory).  Reported, not
    gated: a valid alternative API is not a defect, but avoidance usually
    means the retrieval step failed and the agent improvised.

``--check`` compares against ``eval_generation_baseline.json`` and exits 1
when any gated metric regresses *or the sample count shrinks* (dropping
samples silently weakens the gate).  Baselines only move downward.

Usage::

    python3 .claude/scripts/eval_generation.py --samples .claude/eval-samples
    python3 .claude/scripts/eval_generation.py --samples <dir> --write-baseline
    python3 .claude/scripts/eval_generation.py --samples <dir> --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_skill_api import Finding, load_corpus, validate_file  # noqa: E402

SAMPLE_GLOBS = ("*.il", "*.ils")
TASKS_FILENAME = "eval_tasks.json"
BASELINE_PATH = Path(__file__).resolve().with_name("eval_generation_baseline.json")

# Metrics that must never rise; sample coverage must never shrink.
GATED_UP = ("files_with_errors", "unknown_api_errors", "hallucination_rate")
GATED_DOWN = ("files",)


class TaskGap(NamedTuple):
    task: str
    missing: List[str]


def _samples(directory: Path) -> List[Path]:
    files: List[Path] = []
    for pattern in SAMPLE_GLOBS:
        files.extend(directory.glob(pattern))
    return sorted(files)


def _load_tasks(directory: Path) -> Dict[str, List[str]]:
    manifest = directory / TASKS_FILENAME
    if not manifest.is_file():
        return {}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    return {task["id"]: list(task.get("expected_apis", [])) for task in data.get("tasks", [])}


def measure(directory: Path, root: Path) -> Dict[str, Any]:
    samples = _samples(directory)
    if not samples:
        raise FileNotFoundError(f"no .il/.ils samples found under {directory}")
    specs = load_corpus(root)

    per_file: Dict[str, List[Finding]] = {}
    for path in samples:
        per_file[path.name] = validate_file(path, root, specs, path.name)

    def count(check: str, severity: str) -> int:
        return sum(
            1
            for findings in per_file.values()
            for finding in findings
            if finding.check == check and finding.severity == severity
        )

    files_with_errors = sum(
        1
        for findings in per_file.values()
        if any(f.severity == "error" for f in findings)
    )
    unknown_api_errors = count("unknown-api", "error")

    # expected-API recall per task: which documented APIs did the sample avoid?
    tasks = _load_tasks(directory)
    gaps: List[TaskGap] = []
    for name, findings in per_file.items():
        expected = tasks.get(Path(name).stem)
        if not expected:
            continue
        text = (directory / name).read_text(encoding="utf-8", errors="replace")
        missing = [api for api in expected if api not in text]
        if missing:
            gaps.append(TaskGap(task=Path(name).stem, missing=missing))

    return {
        "files": len(samples),
        "files_with_errors": files_with_errors,
        "unknown_api_errors": unknown_api_errors,
        "hallucination_rate": unknown_api_errors / len(samples),
        "arity_warnings": count("arity", "warning"),
        "keyword_warnings": count("unknown-keyword", "warning"),
        "expected_api_missing": {gap.task: gap.missing for gap in gaps},
        "per_file": {
            name: [f"{f.severity}:{f.check}:{f.message}" for f in findings]
            for name, findings in sorted(per_file.items())
            if findings
        },
    }


def report(metrics: Dict[str, Any]) -> None:
    for key in (
        "files", "files_with_errors", "unknown_api_errors",
        "hallucination_rate", "arity_warnings", "keyword_warnings",
    ):
        value = metrics[key]
        rendered = f"{value:.4f}" if isinstance(value, float) else str(value)
        print(f"{key:20s} {rendered}")
    for task, missing in metrics["expected_api_missing"].items():
        print(f"expected-api-missing: {task}: {', '.join(missing)}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True,
                        help="directory of agent-generated .il/.ils files")
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[1] / "skill-references")
    parser.add_argument("--report", action="store_true", help="print per-file findings")
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="fail if any gated metric regresses or samples shrink")
    arguments = parser.parse_args(argv)

    metrics = measure(arguments.samples, arguments.root.resolve())
    report(metrics)
    if arguments.report:
        print()
        for name, findings in metrics["per_file"].items():
            print(f"{name}:")
            for finding in findings:
                print(f"  {finding}")

    if arguments.write_baseline:
        persistable = {key: value for key, value in metrics.items() if key != "per_file"}
        BASELINE_PATH.write_text(
            json.dumps(persistable, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"baseline written to {BASELINE_PATH.name}")
        return 0

    if arguments.check:
        if not BASELINE_PATH.is_file():
            print(f"error: no baseline at {BASELINE_PATH.name}; run --write-baseline first",
                  file=sys.stderr)
            return 1
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        regressions: List[str] = []
        for key in GATED_UP:
            if metrics[key] > baseline.get(key, 0) + 1e-9:
                regressions.append(f"{key} rose {baseline.get(key)} -> {metrics[key]}")
        for key in GATED_DOWN:
            if metrics[key] < baseline.get(key, 0):
                regressions.append(f"{key} shrank {baseline.get(key)} -> {metrics[key]}")
        for regression in regressions:
            print(f"error: {regression}", file=sys.stderr)
        if regressions:
            return 1
        print("baseline held: no generation-quality regression")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
