#!/usr/bin/env python3
"""Verify an assessment JSON's api_evidence against the corpus indexes.

The cadence-skill-agent emits an assessment block before writing code,
committing to the APIs it will use with their signature and ``source:line``.
That commitment is the cheapest place to catch hallucination - before any
``.il`` exists - but only if it is machine-checked.  An agent can write a
plausible-looking ``signature`` for a function it never actually looked up,
or cite a ``source`` it never opened.

This verifier re-checks every ``payload.api_evidence[]`` entry against
``api_index.part*.md`` / ``sklang_api_index.part*.md``:

``api-unknown`` (error)
    the symbol is not in any index.  Top-3 real candidates are suggested;
    if the API is a genuine corpus gap (e.g. ``axlXSection*``), the escape
    hatch is the Windows ``isCallable`` gate plus a ``verified_facts.json``
    entry - not a fabricated citation.
``source-mismatch`` (error)
    the cited ``source`` file is not the one the index records.  Quoting a
    source you did not read is how signature hallucinations survive review.
``signature-mismatch`` (error)
    the cited declaration differs from the indexed one (whitespace-insensitive;
    omitting the ``=>`` return part is allowed).  The assessment's signature is
    what the implementation will be written against, so it must be the
    documented one.
``line-mismatch`` (warning)
    the cited line differs - usually stale after re-pagination; re-read the
    entry.

Usage::

    python3 .claude/scripts/verify_assessment.py assessment.json
    ... | python3 .claude/scripts/verify_assessment.py -          # stdin

Exit status is 1 when any error-level finding exists.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_skill_api import ApiSpec, load_corpus, suggest_candidates  # noqa: E402


class Finding(NamedTuple):
    level: str  # "error" | "warning"
    check: str
    api: str
    detail: str


def _normalize_signature(text: str) -> str:
    """Collapse whitespace, then drop it around parens and ``=>``.

    Spaces *between* tokens are kept ("f( a b )" and "f( ab )" declare
    different arities and must not compare equal); only formatting whitespace
    is ignored.
    """
    collapsed = re.sub(r"\s+", " ", text).strip()
    collapsed = re.sub(r"\s*([()])\s*", r"\1", collapsed)
    return re.sub(r"\s*=>\s*", "=>", collapsed)


def _signature_matches(cited: str, documented: str) -> bool:
    """Whitespace-insensitive equality; the ``=>`` return part may be omitted."""
    cited_norm = _normalize_signature(cited)
    doc_norm = _normalize_signature(documented)
    if cited_norm == doc_norm:
        return True
    head = _normalize_signature(documented.split("=>")[0])
    return bool(cited_norm) and cited_norm == head


def verify_evidence(
    evidence: Sequence[dict], specs: Dict[str, ApiSpec]
) -> List[Finding]:
    findings: List[Finding] = []
    for entry in evidence:
        api = str(entry.get("api", "")).strip()
        if not api:
            findings.append(Finding("error", "api-empty", "<empty>", "evidence entry has no api name"))
            continue
        spec = specs.get(api.casefold())
        if spec is None:
            suggestion = ""
            candidates = suggest_candidates(api, specs)
            if candidates:
                suggestion = "; did you mean: " + ", ".join(
                    f"{c.name} ({c.source}:{c.line})" for c in candidates
                )
            findings.append(
                Finding("error", "api-unknown", api, f"not in any corpus index{suggestion}")
            )
            continue

        cited_source = str(entry.get("source", "")).strip()
        if cited_source and cited_source != spec.source:
            findings.append(
                Finding(
                    "error", "source-mismatch", api,
                    f"cited {cited_source!r} but the index records {spec.source!r}",
                )
            )

        cited_line = entry.get("line", 0)
        try:
            cited_line = int(cited_line)
        except (TypeError, ValueError):
            cited_line = 0
        if cited_line and cited_line != spec.line:
            findings.append(
                Finding(
                    "warning", "line-mismatch", api,
                    f"cited line {cited_line} but the index records {spec.line} "
                    "(stale citation; re-read the entry)",
                )
            )

        cited_signature = str(entry.get("signature", "")).strip()
        if cited_signature and not _signature_matches(cited_signature, spec.signature):
            findings.append(
                Finding(
                    "error", "signature-mismatch", api,
                    f"cited `{cited_signature}` but the index documents `{spec.signature}`",
                )
            )
    return findings


def _load_assessment(path: str) -> dict:
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    # tolerate the assessment being embedded in surrounding prose/markdown
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match is None:
        raise SystemExit("error: no JSON object found in the input")
    return json.loads(match.group(0))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assessment", help="assessment JSON file, or - for stdin")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "skill-references",
    )
    arguments = parser.parse_args(argv)

    assessment = _load_assessment(arguments.assessment)
    payload = assessment.get("payload", assessment)
    evidence = payload.get("api_evidence")
    if not evidence:
        print("warning: no api_evidence entries; nothing to verify")
        return 0

    specs = load_corpus(arguments.root)
    findings = verify_evidence(evidence, specs)
    for finding in findings:
        print(f"{finding.level}: {finding.check}: {finding.api} - {finding.detail}")

    errors = sum(1 for f in findings if f.level == "error")
    warnings = sum(1 for f in findings if f.level == "warning")
    print(f"\n{len(evidence)} evidence entries: {errors} errors, {warnings} warnings")
    if errors:
        print("fix the assessment against the cited corpus entries before writing code")
        return 1
    print("assessment verified against the corpus")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
