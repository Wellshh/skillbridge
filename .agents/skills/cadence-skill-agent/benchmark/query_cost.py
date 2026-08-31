from __future__ import annotations

import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / 'skill-references'

GAP_APIS = [
    'axlShell',
    'axlShellPost',
    'axlEnterPath',
    'axlEnterPoint',
    'axlCmdRegister',
    'axlDBTransactionStart',
    'axlDBTransactionRollback',
]

SLICE_LINES = 40

_TICK = re.compile(r'`([^`]+)`')
_TRAILING_LINE = re.compile(r'(\d+)\s*\|\s*$')


def find_index_entry(api: str, reference_root: Path = REFERENCE_ROOT) -> tuple[str, int] | None:
    for index_path in sorted(reference_root.glob('api_index.part*.md')):
        for raw_line in index_path.read_text(encoding='utf-8').splitlines():
            if not raw_line.startswith('|'):
                continue
            ticks = _TICK.findall(raw_line)
            if len(ticks) < 3 or ticks[0].strip('*') != api:
                continue
            return ticks[2], int(_TRAILING_LINE.search(raw_line).group(1))
    return None


def slice_bytes(
    source: str,
    line: int,
    reference_root: Path = REFERENCE_ROOT,
    slice_lines: int = SLICE_LINES,
) -> int:
    lines = (reference_root / source).read_bytes().splitlines(keepends=True)
    return sum(len(entry) for entry in lines[line - 1 : line - 1 + slice_lines])


def whole_chapter_bytes(source: str, reference_root: Path = REFERENCE_ROOT) -> int:
    return len((reference_root / source).read_bytes())


def measure_query_cost(reference_root: Path = REFERENCE_ROOT) -> dict:
    resolved: list[str] = []
    missing: list[str] = []
    query_bytes_sliced = 0
    query_bytes_whole_chapter = 0
    for api in GAP_APIS:
        entry = find_index_entry(api, reference_root)
        if entry is None:
            missing.append(api)
            continue
        source, line = entry
        resolved.append(api)
        query_bytes_sliced += slice_bytes(source, line, reference_root)
        query_bytes_whole_chapter += whole_chapter_bytes(source, reference_root)
    return {
        'query_bytes_sliced': query_bytes_sliced,
        'query_bytes_whole_chapter': query_bytes_whole_chapter,
        'resolved': resolved,
        'missing': missing,
    }
