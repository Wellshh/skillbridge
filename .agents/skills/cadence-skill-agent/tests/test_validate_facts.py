from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_facts.py"


def load_validator():
    spec_dir = str(SCRIPT_PATH.parent)
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    import importlib.util

    spec = importlib.util.spec_from_file_location("validate_facts", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(root: Path, facts: list[dict]) -> Path:
    path = root / "verified_facts.json"
    path.write_text(
        json.dumps({"schema_version": 1, "facts": facts}, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def _doc(root: Path, name: str, lines: int) -> None:
    folder = root / "algroskill"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(
        "\n".join(f"line {i}" for i in range(1, lines + 1)) + "\n", encoding="utf-8"
    )


def test_valid_facts_file_passes(tmp_path: Path) -> None:
    validator = load_validator()
    _doc(tmp_path, "cmdshl.md", 700)
    facts = _write(
        tmp_path,
        [
            {
                "id": "axlShellPost-underscore-prefix",
                "api": "axlShellPost",
                "constraint": "subsequent commands need `_` prefix",
                "evidence": [{"path": "algroskill/cmdshl.md", "line": 632}],
                "verified_on": {"allegro": "17.2-2016"},
                "status": "documented",
                "source": "reference-doc",
            }
        ],
    )

    assert validator.validate(facts, tmp_path) == []


def test_missing_evidence_path_fails(tmp_path: Path) -> None:
    validator = load_validator()
    facts = _write(
        tmp_path,
        [
            {
                "id": "bad-path",
                "api": "axlShell",
                "constraint": "x",
                "evidence": [{"path": "algroskill/missing.md", "line": 1}],
                "status": "documented",
                "source": "reference-doc",
            }
        ],
    )

    errors = validator.validate(facts, tmp_path)
    assert any("bad-path" in e and "missing" in e for e in errors)


def test_verified_status_requires_evidence(tmp_path: Path) -> None:
    validator = load_validator()
    _doc(tmp_path, "cmdshl.md", 10)
    facts = _write(
        tmp_path,
        [
            {
                "id": "verified-empty",
                "api": "axlShell",
                "constraint": "x",
                "evidence": [],
                "status": "verified",
                "source": "reference-doc",
            }
        ],
    )

    errors = validator.validate(facts, tmp_path)
    assert any("verified-empty" in e for e in errors)


def test_evidence_line_out_of_range_fails(tmp_path: Path) -> None:
    validator = load_validator()
    _doc(tmp_path, "cmdshl.md", 5)
    facts = _write(
        tmp_path,
        [
            {
                "id": "bad-line",
                "api": "axlShell",
                "constraint": "x",
                "evidence": [{"path": "algroskill/cmdshl.md", "line": 999}],
                "status": "documented",
                "source": "reference-doc",
            }
        ],
    )

    errors = validator.validate(facts, tmp_path)
    assert any("bad-line" in e and "out of range" in e for e in errors)


def test_invalid_status_fails(tmp_path: Path) -> None:
    validator = load_validator()
    _doc(tmp_path, "cmdshl.md", 5)
    facts = _write(
        tmp_path,
        [
            {
                "id": "bad-status",
                "api": "axlShell",
                "constraint": "x",
                "evidence": [{"path": "algroskill/cmdshl.md", "line": 1}],
                "status": "guess",
                "source": "reference-doc",
            }
        ],
    )

    errors = validator.validate(facts, tmp_path)
    assert any("bad-status" in e and "invalid status" in e for e in errors)


def test_duplicate_id_fails(tmp_path: Path) -> None:
    validator = load_validator()
    _doc(tmp_path, "cmdshl.md", 5)
    facts = _write(
        tmp_path,
        [
            {
                "id": "dup",
                "api": "axlShell",
                "constraint": "x",
                "evidence": [{"path": "algroskill/cmdshl.md", "line": 1}],
                "status": "documented",
                "source": "reference-doc",
            },
            {
                "id": "dup",
                "api": "axlShell",
                "constraint": "y",
                "evidence": [{"path": "algroskill/cmdshl.md", "line": 2}],
                "status": "documented",
                "source": "reference-doc",
            },
        ],
    )

    errors = validator.validate(facts, tmp_path)
    assert any("dup" in e and "duplicate" in e for e in errors)


def test_probe_evidence_accepts_nonempty_string(tmp_path: Path) -> None:
    validator = load_validator()
    facts = _write(
        tmp_path,
        [
            {
                "id": "probe-fact",
                "api": "axlShellPost",
                "constraint": "x",
                "evidence": [{"probe": ".artifacts/connect-probes-fixed-full/connect-post.json"}],
                "status": "verified",
                "source": "probe",
            }
        ],
    )

    assert validator.validate(facts, tmp_path) == []


def test_real_verified_facts_file_is_valid() -> None:
    validator = load_validator()
    assert validator.validate(validator.FACTS_PATH, validator.REFERENCE_ROOT) == []
    data = json.loads(validator.FACTS_PATH.read_text(encoding="utf-8"))
    apis = {fact["api"] for fact in data["facts"]}
    assert "axlShellPost" in apis
    assert "axlCmdRegister" in apis
