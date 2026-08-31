from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_LINT_SCRIPT = SKILL_ROOT / 'scripts' / 'skill_lint.py'
VALID_CORPUS_ROOT = SKILL_ROOT / 'skill-references' / 'examples' / 'skill'

MAX_VALID_FILES = 15

INVALID_SNIPPETS = (
    '(defun foo () (let ((x 1) (println x))',
    '(println "abc)',
    '(let ((a #[1 2)',
)


def run_lint(script: Path, path: Path) -> int:
    return subprocess.run(
        [sys.executable, str(script), str(path), '--quiet'],
        check=False,
    ).returncode


def measure_skill_lint(
    corpus_root: Path = VALID_CORPUS_ROOT,
    script: Path = SKILL_LINT_SCRIPT,
    max_valid: int = MAX_VALID_FILES,
) -> dict:
    valid_files = sorted(corpus_root.rglob('*.il'))[:max_valid]
    fp_files = [str(path) for path in valid_files if run_lint(script, path) != 0]
    missed_invalid: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        for index, snippet in enumerate(INVALID_SNIPPETS):
            invalid_path = Path(tmp) / f'invalid_{index}.il'
            invalid_path.write_text(snippet, encoding='utf-8')
            if run_lint(script, invalid_path) != 1:
                missed_invalid.append(f'invalid_{index}')
    catch_rate = (len(INVALID_SNIPPETS) - len(missed_invalid)) / len(INVALID_SNIPPETS)
    fp_rate = len(fp_files) / len(valid_files)
    return {
        'catch_rate': catch_rate,
        'fp_rate': fp_rate,
        'valid_count': len(valid_files),
        'invalid_count': len(INVALID_SNIPPETS),
        'fp_files': fp_files,
        'missed_invalid': missed_invalid,
    }
