from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import query_cost
import score
import skill_lint_corpus


def _reference_root(tmp_path: Path, api: str, source: str, start_line: int) -> Path:
    (tmp_path / 'algroskill').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'api_index.part01.md').write_text(
        '| Symbol | Declaration | Source | Line |\n'
        '|---|---|---|---:|\n'
        f'| `{api}` | `{api}(x)=> t` | `{source}` | {start_line} |\n',
        encoding='utf-8',
    )
    return tmp_path


def _chapter(path: Path, line_count: int) -> bytes:
    data = ''.join(f'line-{i}-{"x" * (i % 7)}\n' for i in range(1, line_count + 1)).encode('utf-8')
    path.write_bytes(data)
    return data


def _expected_slice_bytes(data: bytes, start_line: int, slice_lines: int) -> int:
    lines = data.splitlines(keepends=True)
    return sum(len(line) for line in lines[start_line - 1 : start_line - 1 + slice_lines])


def _score_value(query_bytes_sliced: int, fp_rate: float, catch_rate: float) -> dict:
    return {
        'query_bytes_sliced': query_bytes_sliced,
        'query_bytes_whole_chapter': query_bytes_sliced + 1000,
        'skill_lint': {
            'catch_rate': catch_rate,
            'fp_rate': fp_rate,
            'valid_count': 3,
            'invalid_count': 3,
        },
    }


def test_query_cost_counts_slice_and_whole_chapter(tmp_path: Path) -> None:
    start_line = 5
    root = _reference_root(tmp_path, 'axlShell', 'algroskill/foo.md', start_line)
    data = _chapter(root / 'algroskill' / 'foo.md', 100)

    result = query_cost.measure_query_cost(root)

    assert result['query_bytes_sliced'] == _expected_slice_bytes(
        data, start_line, query_cost.SLICE_LINES
    )
    assert result['query_bytes_whole_chapter'] == len(data)
    assert result['query_bytes_sliced'] < result['query_bytes_whole_chapter']
    assert result['resolved'] == ['axlShell']
    assert 'axlShellPost' in result['missing']


def test_query_cost_records_missing_apis(tmp_path: Path) -> None:
    (tmp_path / 'api_index.part01.md').write_text(
        '| Symbol | Declaration | Source | Line |\n', encoding='utf-8'
    )

    result = query_cost.measure_query_cost(tmp_path)

    assert result['resolved'] == []
    assert result['missing'] == list(query_cost.GAP_APIS)


def test_skill_lint_corpus_catches_invalid_without_fp(tmp_path: Path) -> None:
    corpus = tmp_path / 'corpus'
    corpus.mkdir()
    (corpus / 'ok.il').write_text('(defun ok () (println "hi"))\n', encoding='utf-8')

    result = skill_lint_corpus.measure_skill_lint(
        corpus_root=corpus, script=skill_lint_corpus.SKILL_LINT_SCRIPT
    )

    assert result['catch_rate'] == 1.0
    assert result['fp_rate'] == 0.0
    assert result['valid_count'] == 1
    assert result['invalid_count'] == len(skill_lint_corpus.INVALID_SNIPPETS)
    assert result['fp_files'] == []
    assert result['missed_invalid'] == []


def test_skill_lint_corpus_reports_fp_on_broken_valid_file(tmp_path: Path) -> None:
    corpus = tmp_path / 'corpus'
    corpus.mkdir()
    (corpus / 'broken.il').write_text('(defun foo () (let ((x 1) (println x))', encoding='utf-8')

    result = skill_lint_corpus.measure_skill_lint(
        corpus_root=corpus, script=skill_lint_corpus.SKILL_LINT_SCRIPT
    )

    assert result['catch_rate'] == 1.0
    assert result['fp_rate'] == 1.0
    assert result['valid_count'] == 1
    assert len(result['fp_files']) == 1


def test_check_fails_when_query_bytes_sliced_increases(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(score, 'build_score', lambda: _score_value(200, 0.0, 1.0))
    baseline_path = tmp_path / 'baseline.json'
    baseline_path.write_text(json.dumps(_score_value(100, 0.0, 1.0)), encoding='utf-8')
    monkeypatch.setattr(score, 'BASELINE_PATH', baseline_path)

    assert score.main(['--check']) == 1
    assert len(capsys.readouterr().out.strip().splitlines()) == 1


def test_check_passes_when_query_bytes_sliced_decreases(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(score, 'build_score', lambda: _score_value(100, 0.0, 1.0))
    baseline_path = tmp_path / 'baseline.json'
    baseline_path.write_text(json.dumps(_score_value(200, 0.0, 1.0)), encoding='utf-8')
    monkeypatch.setattr(score, 'BASELINE_PATH', baseline_path)

    assert score.main(['--check']) == 0


def test_check_fails_when_catch_rate_decreases(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(score, 'build_score', lambda: _score_value(100, 0.0, 0.5))
    baseline_path = tmp_path / 'baseline.json'
    baseline_path.write_text(json.dumps(_score_value(100, 0.0, 1.0)), encoding='utf-8')
    monkeypatch.setattr(score, 'BASELINE_PATH', baseline_path)

    assert score.main(['--check']) == 1


def test_check_fails_when_fp_rate_increases(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(score, 'build_score', lambda: _score_value(100, 0.5, 1.0))
    baseline_path = tmp_path / 'baseline.json'
    baseline_path.write_text(json.dumps(_score_value(100, 0.0, 1.0)), encoding='utf-8')
    monkeypatch.setattr(score, 'BASELINE_PATH', baseline_path)

    assert score.main(['--check']) == 1


def test_baseline_writes_current_score(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    expected = _score_value(100, 0.0, 1.0)
    monkeypatch.setattr(score, 'build_score', lambda: expected)
    baseline_path = tmp_path / 'baseline.json'
    monkeypatch.setattr(score, 'BASELINE_PATH', baseline_path)

    assert score.main(['--baseline']) == 0
    assert json.loads(baseline_path.read_text(encoding='utf-8')) == expected
