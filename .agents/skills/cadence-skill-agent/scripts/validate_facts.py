from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / "skill-references"
FACTS_PATH = REFERENCE_ROOT / "verified_facts.json"

REQUIRED_FACT_FIELDS = ("id", "api", "constraint", "evidence", "status")
VALID_STATUS = ("verified", "documented", "superseded")


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def validate(facts_path: Path = FACTS_PATH, reference_root: Path = REFERENCE_ROOT) -> list[str]:
    errors: list[str] = []
    if not facts_path.is_file():
        return [f"missing facts file: {facts_path}"]
    try:
        data = json.loads(facts_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    facts = data.get("facts") if isinstance(data, dict) else None
    if not isinstance(facts, list) or not facts:
        errors.append("facts must be a non-empty list")
        return errors
    seen_ids: set[str] = set()
    for fact in facts:
        if not isinstance(fact, dict):
            errors.append("each fact must be an object")
            continue
        fact_id = str(fact.get("id", "<missing>"))
        for field in REQUIRED_FACT_FIELDS:
            if field not in fact:
                errors.append(f"{fact_id}: missing field {field}")
        if fact.get("status") not in VALID_STATUS:
            errors.append(f"{fact_id}: invalid status {fact.get('status')!r}")
        if fact_id in seen_ids:
            errors.append(f"{fact_id}: duplicate id")
        if fact_id != "<missing>":
            seen_ids.add(fact_id)
        evidence = fact.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{fact_id}: evidence must be a non-empty list")
            continue
        for entry in evidence:
            if not isinstance(entry, dict):
                errors.append(f"{fact_id}: evidence entry must be an object")
                continue
            if "path" in entry and "line" in entry:
                doc = reference_root / entry["path"]
                if not doc.is_file():
                    errors.append(f"{fact_id}: evidence path missing: {entry['path']}")
                else:
                    line = entry["line"]
                    if not isinstance(line, int) or line < 1 or line > _line_count(doc):
                        errors.append(
                            f"{fact_id}: evidence line out of range: {entry['path']}:{line}"
                        )
            elif "probe" in entry:
                if not isinstance(entry["probe"], str) or not entry["probe"]:
                    errors.append(f"{fact_id}: evidence probe must be a non-empty string")
            else:
                errors.append(f"{fact_id}: evidence entry needs path+line or probe")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate verified_facts.json schema and evidence."
    )
    parser.add_argument(
        "--root", type=Path, default=None, help="reference root overriding the default"
    )
    parser.add_argument("--check", action="store_true", help="alias; always validates")
    parser.add_argument("facts", nargs="?", type=Path, default=None, help="facts file to validate")
    args = parser.parse_args(argv)
    reference_root = args.root if args.root is not None else REFERENCE_ROOT
    facts_path = args.facts if args.facts is not None else reference_root / "verified_facts.json"
    errors = validate(facts_path, reference_root)
    for error in errors:
        print(f"error: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
