from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path


def find_repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".agents/skills/cadence-skill-agent/SKILL.md").is_file():
            return parent
    raise RuntimeError("cannot locate repository root")


ROOT = find_repository_root()
SOURCE = ROOT / ".agents/skills/cadence-skill-agent"
CLAUDE = ROOT / ".claude"


def parse_skill(source: str) -> tuple[dict[str, str], str]:
    if not source.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    frontmatter, body = source[4:].split("\n---\n", maxsplit=1)
    fields = {
        key: value.strip()
        for key, value in (line.split(":", maxsplit=1) for line in frontmatter.splitlines())
    }
    return fields, body.strip("\n")


def render_codex_agent(source: str) -> str:
    fields, body = parse_skill(source)
    if "'''" in body:
        raise ValueError("SKILL.md cannot contain a TOML multiline literal delimiter")
    return (
        f"description = {json.dumps(fields['description'], ensure_ascii=False)}\n"
        "developer_instructions = '''\n"
        f"{body}\n"
        "'''\n"
        f"name = {json.dumps(fields['name'], ensure_ascii=False)}\n"
    )


def render_claude_agent(source: str) -> str:
    fields, body = parse_skill(source)
    body = body.replace(
        ".agents/skills/cadence-skill-agent/skill-references/",
        ".claude/skill-references/",
    ).replace(
        ".agents/skills/cadence-skill-agent/scripts/",
        ".claude/scripts/",
    )
    return (
        "---\n"
        f"name: {fields['name']}\n"
        f"description: {fields['description']}\n"
        "tools: Read, Write, Edit, Grep, Glob, Bash\n"
        "model: inherit\n"
        "memory: project\n"
        "---\n\n"
        f"{body}\n"
    )


def adapt_reference(data: bytes) -> bytes:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return (
        text
        .replace("\r\n", "\n")
        .replace(
            ".agents/skills/cadence-skill-agent/SKILL.md",
            ".claude/agents/cadence-skill-agent.md",
        )
        .replace(
            ".agents/skills/cadence-skill-agent/skill-references/",
            ".claude/skill-references/",
        )
        .replace(
            ".agents/skills/cadence-skill-agent/scripts/",
            ".claude/scripts/",
        )
        .encode("utf-8")
    )


def expected_files() -> dict[Path, bytes]:
    files = {
        ROOT / ".codex/agents/cadence-skill-agent.toml": render_codex_agent(
            (SOURCE / "SKILL.md").read_text(encoding="utf-8")
        ).encode("utf-8"),
        CLAUDE / "agents/cadence-skill-agent.md": render_claude_agent(
            (SOURCE / "SKILL.md").read_text(encoding="utf-8")
        ).encode("utf-8"),
    }
    reference_root = SOURCE / "skill-references"
    for source in reference_root.rglob("*"):
        if source.is_file() and "__pycache__" not in source.parts:
            destination = CLAUDE / "skill-references" / source.relative_to(reference_root)
            files[destination] = adapt_reference(source.read_bytes())
    for name in (
        "build_reference_indexes.py",
        "convert_pdf_references.py",
        "sync_claude.py",
    ):
        files[CLAUDE / "scripts" / name] = (SOURCE / "scripts" / name).read_bytes()
    files[CLAUDE / "tests/test_sync_claude.py"] = (
        SOURCE / "tests/test_sync_claude.py"
    ).read_bytes()
    return files


def stale_reference_files(root: Path, expected: set[Path]) -> list[Path]:
    orcad_index = root / "orcad-capture-tcltk-agent.md"
    orcad_root = root / "orcadcapture"
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path not in expected
        and path != orcad_index
        and orcad_root not in path.parents
    )


def synchronize(*, check: bool) -> list[Path]:
    expected = expected_files()
    changed: list[Path] = []
    for destination, content in expected.items():
        current = destination.read_bytes() if destination.is_file() else None
        if current == content:
            continue
        changed.append(destination)
        if not check:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    changed.extend(stale_reference_files(CLAUDE / "skill-references", set(expected)))
    return changed


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = synchronize(check=args.check)
    if args.check and changed:
        for path in changed:
            print(f"out of sync: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
