#!/usr/bin/env python3
"""Retrieval benchmark for ``search_api.py`` - the objective yardstick.

Ranking changes are easy to make and hard to judge by eye, so this measures
whether intent-style queries actually resolve to the right documented API.
Each case pairs a task phrasing an agent would plausibly use with the symbol
that answers it; the expected symbol is verified to exist in the corpus at load
time, so a stale case fails loudly instead of silently scoring zero.

Metrics
-------
``top1``
    fraction of queries whose rank-1 hit is an accepted answer.
``mrr``
    mean reciprocal rank - rewards getting the answer near the top.
``recall@5``
    fraction of queries with an accepted answer inside the first five hits.

Run ``--report`` to print per-query detail.  Exit status is 1 when any metric
falls below the recorded baseline in ``eval_retrieval_baseline.json``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from search_api import build_index, _default_root  # noqa: E402

BASELINE_PATH = Path(__file__).resolve().with_name("eval_retrieval_baseline.json")

# Each case: (query phrasing an agent would use, accepted answer symbols).
# Multiple accepted answers are allowed where the corpus genuinely documents
# more than one reasonable route to the same outcome.  Every symbol here is
# verified to exist in the corpus at load time; cases whose answer is a dbid
# *property* rather than a function (``dbid->bBox``, ``->nets``) are excluded
# because no symbol lookup can answer them.
CASES: List[Tuple[str, Tuple[str, ...]]] = [
    # frontier case: net-mutator prose genuinely says "net name", so this MISSes;
    # the corpus-answerable phrasing below is what agents should converge on
    ("get the name of a net", ("axlDbidName",)),
    ("get the name of a database object", ("axlDbidName",)),
    ("find a dbid by name", ("axlDBFindByName",)),
    ("rename a net", ("axlRenameNet",)),
    ("delete a net and rip up its wiring", ("axlRemoveNet",)),
    ("create a new net", ("axlDBCreateNet",)),
    ("start a database transaction", ("axlDBTransactionStart",)),
    ("roll back a transaction", ("axlDBTransactionRollback",)),
    (
        "select objects by name",
        ("axlSelectByName", "axlSingleSelectName", "axlAddSelectName", "axlSubSelectName"),
    ),
    ("get the design object", ("axlDBGetDesign",)),
    ("create a line between two points", ("axlDBCreateLine",)),
    ("display a message in the command window", ("axlUIWPrint", "axlMsgPut")),
    ("register a SKILL command", ("axlCmdRegister",)),
    ("zoom to the whole design", ("axlZoomWorld",)),
    ("change the layer of an object", ("axlChangeLayer",)),
    ("sort a list", ("sort", "sortcar")),
    ("open a file for writing", ("outfile",)),
    ("read a line from a file", ("lineread", "gets")),
    # frontier MISS: the scanf/fprintf siblings' prose mentions "number of
    # items" and "format string", so they outrank sprintf; the family in
    # top-5 still routes an agent to the right entry via cross-references
    ("format a number as a string", ("sprintf",)),
    ("get the current working directory", ("getWorkingDir",)),
    ("run a shell command", ("axlShell", "shell")),
    ("create a via", ("axlDBCreateVia",)),
    # `type` and `typep` are documented as identical functions (datastruct.md);
    # the "check" phrasing is a frontier MISS (typep's prose says "returns"),
    # the "get" phrasing is the corpus-answerable form
    ("check the type of an object", ("typep", "type")),
    ("get the data type of an object", ("typep", "type")),
    ("append to a list", ("append", "append1", "lconc")),
    ("add two bounding boxes together", ("bBoxAdd",)),
    ("check whether a value is a list", ("listp",)),
    ("enter a point interactively", ("axlEnterPoint",)),
    ("create a path along a route", ("axlDBCreatePath",)),
    ("get the version of Allegro", ("axlVersion",)),
    ("write a property to an object", ("putprop",)),
    ("compare two strings", ("strcmp", "strncmp")),
    # Keep the retrieval benchmark aligned with the expanded generation task
    # set; these are all task phrasings with corpus-backed expected APIs.
    ("report current design units", ("axlDBGetDesignUnits",)),
    ("report drawing path name", ("axlGetDrawingName",)),
    ("report top and bottom conductor layer names", ("axlConductorTopLayer", "axlConductorBottomLayer")),
    ("report selection set count", ("axlGetSelSetCount",)),
    ("report whether the find filter is open", ("axlFindFilterIsOpen",)),
    ("return the current design handle", ("axlCurrentDesign",)),
]


class CaseResult(NamedTuple):
    query: str
    expected: Tuple[str, ...]
    rank: Optional[int]
    top: Sequence[str]


def evaluate(root: Path, limit: int = 10) -> Tuple[Dict[str, float], List[CaseResult]]:
    index = build_index(root)
    known = {entry.name.casefold(): entry for entry in index.entries}

    # Fail loudly on stale cases rather than silently scoring them zero.
    stale: List[str] = []
    for query, expected in CASES:
        for name in expected:
            if name.casefold() not in known:
                stale.append(f"{query!r} expects {name!r}, absent from the corpus")
    if stale:
        for problem in stale:
            print(f"error: {problem}", file=sys.stderr)
        raise SystemExit(1)

    results: List[CaseResult] = []
    reciprocal_sum = 0.0
    top1_hits = 0
    recall_hits = 0

    for query, expected in CASES:
        wanted = {name.casefold() for name in expected}
        matches = index.search(query, limit=limit)
        names = [m.entry.name for m in matches]
        rank: Optional[int] = None
        for position, name in enumerate(names, start=1):
            if name.casefold() in wanted:
                rank = position
                break
        results.append(CaseResult(query, expected, rank, names[:5]))
        if rank == 1:
            top1_hits += 1
            reciprocal_sum += 1.0
        elif rank is not None:
            reciprocal_sum += 1.0 / rank
        if rank is not None and rank <= 5:
            recall_hits += 1

    count = len(CASES)
    metrics = {
        "cases": count,
        "top1": top1_hits / count,
        "mrr": reciprocal_sum / count,
        "recall_at_5": recall_hits / count,
    }
    return metrics, results


def report(results: Sequence[CaseResult]) -> None:
    for case in results:
        status = f"rank {case.rank}" if case.rank else f"MISS (>{len(case.top)})"
        marker = "ok " if case.rank == 1 else ("~  " if case.rank else "FAIL")
        print(f"{marker} {status:12s} {case.query}")
        if case.rank != 1:
            print(f"     wanted: {', '.join(case.expected)}")
            print(f"     got:    {', '.join(case.top)}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=_default_root())
    parser.add_argument("--report", action="store_true", help="print per-query detail")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument(
        "--check", action="store_true", help="fail if any metric regresses"
    )
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()

    metrics, results = evaluate(root, limit=arguments.limit)
    if arguments.report:
        report(results)
        print()
    for key in ("cases", "top1", "mrr", "recall_at_5"):
        value = metrics[key]
        rendered = f"{value:.4f}" if isinstance(value, float) else str(value)
        print(f"{key:14s} {rendered}")

    if arguments.write_baseline:
        BASELINE_PATH.write_text(
            json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"baseline written to {BASELINE_PATH.name}")
        return 0

    if arguments.check:
        if not BASELINE_PATH.is_file():
            print(
                f"error: no baseline at {BASELINE_PATH.name}; run --write-baseline first",
                file=sys.stderr,
            )
            return 1
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        regressions = [
            f"{key} fell {baseline[key]:.4f} -> {metrics[key]:.4f}"
            for key in ("top1", "mrr", "recall_at_5")
            if metrics[key] < baseline.get(key, 0.0) - 1e-9
        ]
        for regression in regressions:
            print(f"error: {regression}", file=sys.stderr)
        if regressions:
            return 1
        print("baseline held: no retrieval regression")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
