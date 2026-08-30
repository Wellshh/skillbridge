# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = ROOT / 'docs' / 'examples'


def _text_of(source: object) -> str:
    if isinstance(source, list):
        return ''.join(source)
    return str(source or '')


def _output_text(output: dict[str, Any]) -> str:
    otype = output.get('output_type')
    if otype == 'stream':
        return _text_of(output.get('text'))
    if otype in {'execute_result', 'display_data'}:
        data = output.get('data', {})
        return _text_of(data.get('text/plain'))
    if otype == 'error':
        return '\n'.join(output.get('traceback', []))
    return ''


def render_notebook(path: Path) -> str:
    nb = json.loads(path.read_text(encoding='utf-8'))
    parts: list[str] = []
    for cell in nb.get('cells', []):
        ctype = cell.get('cell_type')
        source = _text_of(cell.get('source')).strip('\n')
        if ctype == 'markdown':
            parts.append(source)
        elif ctype == 'code':
            if source:
                parts.append(f'```python\n{source}\n```')
            for output in cell.get('outputs', []):
                text = _output_text(output).strip('\n')
                if text:
                    parts.append(
                        f'<div class="nb-output" markdown>\n\n```text\n{text}\n```\n\n</div>'
                    )
    return '\n\n'.join(p for p in parts if p) + '\n'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', type=Path, default=None)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)

    paths = args.paths or sorted(DEFAULT_GLOB.glob('*.ipynb'))
    failed = False
    for path in paths:
        target = path.with_suffix('.md')
        rendered = render_notebook(path)
        if args.check:
            if not target.is_file() or target.read_text(encoding='utf-8') != rendered:
                print(f'{target}: stale')
                failed = True
        else:
            target.write_text(rendered, encoding='utf-8')
            print(f'{path.name} -> {target.name}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
