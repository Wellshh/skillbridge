#!/usr/bin/env python3
"""Rebalance oversized generated sklangref pages at API-heading boundaries.

The original HTML/PDF source is not bundled in this checkout.  This utility
therefore treats the existing generated pages as an ordered stream, removes
only their generated pagination headers, and writes the same stream back with
safer page boundaries.  It never splits inside a top-level API section.
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import List, Sequence, Tuple


TARGET_TOKENS = 13_480
CHARS_PER_TOKEN = 4.0
STEMS = ("funcprog", "inputoutput")
HEADER = re.compile(r"\A<!--\nsource: sklangref/[^\n]+\npart: \d+/\d+\nestimated_tokens: \d+\n-->\n\n")
TOP_LEVEL_HEADING = re.compile(r"(?m)^### (?!Cadence SKILL Language Reference[^\r\n]*$)[^\r\n]+")


def _estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def _part_paths(root: Path, stem: str) -> List[Path]:
    paths = sorted(root.glob(f"{stem}.part*.md"))
    if not paths:
        raise RuntimeError(f"missing existing pages for {stem}")
    return paths


def _reassemble(root: Path, stem: str) -> str:
    chunks: List[str] = []
    for path in _part_paths(root, stem):
        text = path.read_text(encoding="utf-8")
        chunks.append(HEADER.sub("", text, count=1))
    return "".join(chunks)


def _choose_boundaries(text: str) -> List[int]:
    total_tokens = _estimate_tokens(text)
    if total_tokens <= TARGET_TOKENS:
        return [len(text)]

    candidates = [match.start() for match in TOP_LEVEL_HEADING.finditer(text)]
    boundaries: List[int] = []
    start = 0
    while _estimate_tokens(text[start:]) > TARGET_TOKENS:
        eligible = [position for position in candidates if start < position <= start + int(TARGET_TOKENS * CHARS_PER_TOKEN)]
        if not eligible:
            raise RuntimeError(f"no safe top-level heading boundary for {start}")
        boundary = eligible[-1]
        boundaries.append(boundary)
        start = boundary
    boundaries.append(len(text))
    return boundaries


def _write_pages(root: Path, stem: str, text: str) -> List[Tuple[Path, int]]:
    boundaries = _choose_boundaries(text)
    starts = [0] + boundaries[:-1]
    outputs: List[Tuple[Path, int]] = []
    for index, (start, end) in enumerate(zip(starts, boundaries), start=1):
        body = text[start:end]
        header = (
            "<!--\n"
            f"source: sklangref/{stem}.md\n"
            f"part: {index}/{len(boundaries)}\n"
            f"estimated_tokens: {_estimate_tokens(body)}\n"
            "-->\n\n"
        )
        path = root / f"{stem}.part{index:02d}.md"
        path.write_text(header + body, encoding="utf-8")
        outputs.append((path, _estimate_tokens(header + body)))

    for stale in sorted(root.glob(f"{stem}.part*.md")):
        if stale not in {path for path, _ in outputs}:
            stale.unlink()
    return outputs


def repage(root: Path) -> None:
    for stem in STEMS:
        text = _reassemble(root, stem)
        outputs = _write_pages(root, stem, text)
        details = ", ".join(f"{path.name}={tokens}" for path, tokens in outputs)
        print(f"{stem}: {details}")


def check(root: Path) -> int:
    failures: List[str] = []
    for stem in STEMS:
        text = _reassemble(root, stem)
        for part_name, tokens in _write_pages_preview(root, stem, text):
            if tokens > TARGET_TOKENS:
                failures.append(f"{stem} would exceed target: {part_name}={tokens}")
    for failure in failures:
        print(f"error: {failure}")
    return 1 if failures else 0


def _write_pages_preview(root: Path, stem: str, text: str) -> List[Tuple[str, int]]:
    boundaries = _choose_boundaries(text)
    starts = [0] + boundaries[:-1]
    result = []
    for index, (start, end) in enumerate(zip(starts, boundaries), start=1):
        body = text[start:end]
        header = (
            "<!--\n"
            f"source: sklangref/{stem}.md\n"
            f"part: {index}/{len(boundaries)}\n"
            f"estimated_tokens: {_estimate_tokens(body)}\n"
            "-->\n\n"
        )
        result.append((f"{stem}.part{index:02d}.md", _estimate_tokens(header + body)))
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "skill-references" / "sklangref")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.check:
        return check(root)
    repage(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
