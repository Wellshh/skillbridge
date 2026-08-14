#!/usr/bin/env python3
"""Build and validate deterministic indexes for the bundled Cadence references."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, NamedTuple, Optional, Sequence, Tuple

TOKEN_LIMIT = 15_000
SAFETY_RATIO = 0.9
CHARS_PER_TOKEN = 4.0
REFERENCE_DIRS = ("algroskill", "sklangref", "sklanguser")
GENERATED_INDEXES = (
    "sklang_api_index.part01.md",
    "sklang_api_index.part02.md",
    "sklang_api_index.part03.md",
    "sklang_topic_index.md",
)
LEGACY_HTML_LINK = re.compile(r"\([^)]*\.html(?:#[^)]*)?\)")
PART_NAME = re.compile(r"^(?P<stem>.+)\.part(?P<number>\d+)\.md$")
INVALID_SYMBOL_NAMES = {"...", "…"}


class ApiEntry(NamedTuple):
    name: str
    signature: str
    path: str
    line: int


class TopicEntry(NamedTuple):
    topic: str
    path: str
    line: int


class CheckResult(NamedTuple):
    ok: bool
    errors: List[str]
    warnings: List[str]


def _markdown_files(root: Path, directories: Sequence[str]) -> Iterable[Path]:
    for directory in directories:
        path = root / directory
        if path.is_dir():
            yield from sorted(path.glob("*.md"))


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _plain_heading(value: str) -> str:
    return value.replace("`", "").replace("\\_", "_").strip()


def _signature_after_heading(lines: Sequence[str], heading_index: int) -> Optional[str]:
    in_code_block = False
    code_lines: List[str] = []
    inline_lines: List[str] = []
    for line in lines[heading_index + 1 :]:
        if line.startswith(("### ", "#### Description")):
            return None
        candidate = line.strip()
        if candidate.startswith("```"):
            if in_code_block:
                declaration = " ".join(part.strip() for part in code_lines if part.strip())
                return declaration if "=>" in declaration else None
            in_code_block = True
            code_lines = []
            inline_lines = []
            continue
        if in_code_block:
            code_lines.append(candidate)
            continue
        if candidate.startswith("`") and candidate.endswith("`"):
            inline_lines.append(candidate[1:-1].strip())
            declaration = " ".join(part for part in inline_lines if part)
            if "=>" in declaration:
                return declaration
            continue
        if candidate:
            inline_lines = []
    return None


def extract_api_entries(root: Path) -> List[ApiEntry]:
    """Extract formal SKILL API headings followed by a documented signature."""
    entries: List[ApiEntry] = []
    for path in _markdown_files(root, ("sklangref",)):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if not line.startswith("### "):
                continue
            signature = _signature_after_heading(lines, index)
            if signature is None:
                continue
            heading = _plain_heading(line[4:])
            names = [
                name.strip()
                for name in heading.split(",")
                if name.strip() and name.strip() not in INVALID_SYMBOL_NAMES
            ]
            for name in names:
                entries.append(
                    ApiEntry(
                        name=name,
                        signature=signature,
                        path=_relative(path, root),
                        line=index + 1,
                    )
                )
    return sorted(entries, key=lambda entry: (entry.name.casefold(), entry.path, entry.line))


def _is_topic(value: str) -> bool:
    normalized = value.strip()
    return (
        bool(normalized)
        and not normalized.isdigit()
        and normalized
        not in {
            "Contents",
            "Index",
            "All rights reserved.",
        }
        and not normalized.startswith("Cadence SKILL Language User Guide Product Version")
    )


def extract_topic_entries(root: Path) -> List[TopicEntry]:
    """Extract navigable section headings from the SKILL User Guide chapters."""
    entries: List[TopicEntry] = []
    seen: set = set()
    for path in _markdown_files(root, ("sklanguser",)):
        if not path.name.startswith("chap"):
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            topic: Optional[str] = None
            if line.startswith(("## ", "### ")):
                topic = line.lstrip("#").strip()
            elif index + 1 < len(lines) and re.fullmatch(r"[=-]{3,}", lines[index + 1]):
                topic = line.strip()
            if topic is None or not _is_topic(topic):
                continue
            key = (topic.casefold(), _relative(path, root))
            if key in seen:
                continue
            seen.add(key)
            entries.append(TopicEntry(topic, _relative(path, root), index + 1))
    return sorted(entries, key=lambda entry: (entry.topic.casefold(), entry.path, entry.line))


def _api_part(name: str) -> int:
    first = name[:1].casefold()
    if "a" <= first <= "f":
        return 1
    if "g" <= first <= "r":
        return 2
    return 3


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("`", "\\`")


def _render_api_index(entries: Sequence[ApiEntry], part: int) -> str:
    ranges = {1: "A-F", 2: "G-R", 3: "S-Z and symbols"}
    lines = [
        "<!-- Generated by scripts/build_reference_indexes.py; do not edit manually. -->",
        "",
        f"# SKILL Language API Index ({ranges[part]})",
        "",
        "Search this file for an exact function name, then read the referenced source entry.",
        "",
        "| Symbol | Documented declaration | Source | Line |",
        "|---|---|---|---:|",
    ]
    for entry in entries:
        lines.append(
            f"| `{_escape_table(entry.name)}` | `{_escape_table(entry.signature)}` | "
            f"`{entry.path}` | {entry.line} |"
        )
    return "\n".join(lines) + "\n"


def _render_topic_index(entries: Sequence[TopicEntry]) -> str:
    lines = [
        "<!-- Generated by scripts/build_reference_indexes.py; do not edit manually. -->",
        "",
        "# SKILL Language User Guide Topic Index",
        "",
        "Search by programming intent or concept, then read the referenced chapter section.",
        "",
        "| Topic | Source | Line |",
        "|---|---|---:|",
    ]
    for entry in entries:
        lines.append(f"| {_escape_table(entry.topic)} | `{entry.path}` | {entry.line} |")
    return "\n".join(lines) + "\n"


def _estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _pdf_pages(path: Path) -> Optional[int]:
    executable = shutil.which("pdfinfo")
    if executable is None:
        return None
    result = subprocess.run(
        [executable, str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, flags=re.MULTILINE)
    return int(match.group(1)) if match else None


def _document_records(root: Path) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    for path in _markdown_files(root, REFERENCE_DIRS):
        text = path.read_text(encoding="utf-8")
        estimated_tokens = _estimate_tokens(text)
        records.append({
            "path": _relative(path, root),
            "chars": len(text),
            "estimated_tokens": estimated_tokens,
            "exceeds_limit": estimated_tokens > TOKEN_LIMIT,
            "exceeds_safety_target": estimated_tokens > TOKEN_LIMIT * SAFETY_RATIO,
        })
    return records


def _source_records(
    root: Path,
    existing_pages: Optional[Dict[str, object]] = None,
) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    docs = root / "docs"
    if not docs.is_dir():
        return records
    for path in sorted(docs.glob("*.pdf")):
        relative_path = _relative(path, root)
        physical_pages = _pdf_pages(path)
        if physical_pages is None and existing_pages is not None:
            physical_pages = existing_pages.get(relative_path)
        records.append({
            "path": relative_path,
            "source_version": "6.1.6 / November 2014",
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
            "physical_pages": physical_pages,
        })
    return records


def _legacy_html_link_count(root: Path) -> int:
    count = 0
    for path in _markdown_files(root, REFERENCE_DIRS):
        count += len(LEGACY_HTML_LINK.findall(path.read_text(encoding="utf-8")))
    return count


def _signature_name_mismatch_count(entries: Sequence[ApiEntry]) -> int:
    return sum(
        1 for entry in entries if f"{entry.name.casefold()}(" not in entry.signature.casefold()
    )


def _manifest(
    root: Path,
    api_count: int,
    topic_count: int,
    existing_pages: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    return {
        "schema_version": 2,
        "pagination": {
            "token_limit": TOKEN_LIMIT,
            "safety_ratio": SAFETY_RATIO,
            "estimator": {"method": "character_ratio", "chars_per_token": CHARS_PER_TOKEN},
        },
        "sources": _source_records(root, existing_pages),
        "documents": _document_records(root),
        "indexes": {
            "api_entries": api_count,
            "topic_entries": topic_count,
            "outputs": list(GENERATED_INDEXES),
        },
        "quality": {
            "legacy_html_links": _legacy_html_link_count(root),
            "signature_name_mismatches": _signature_name_mismatch_count(extract_api_entries(root)),
        },
    }


def _manifest_text(
    root: Path,
    api_count: int,
    topic_count: int,
    existing_pages: Optional[Dict[str, object]] = None,
) -> str:
    return (
        json.dumps(
            _manifest(root, api_count, topic_count, existing_pages),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def _existing_physical_pages(root: Path) -> Dict[str, object]:
    path = root / ".paginate" / "pagination_manifest.json"
    if not path.is_file():
        return {}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return {
        source["path"]: source.get("physical_pages")
        for source in manifest.get("sources", [])
        if isinstance(source, dict) and isinstance(source.get("path"), str)
    }


def _rendered_indexes(root: Path) -> Dict[str, str]:
    api_entries = extract_api_entries(root)
    topic_entries = extract_topic_entries(root)
    rendered: Dict[str, str] = {}
    for part in (1, 2, 3):
        selected = [entry for entry in api_entries if _api_part(entry.name) == part]
        rendered[f"sklang_api_index.part{part:02d}.md"] = _render_api_index(selected, part)
    rendered["sklang_topic_index.md"] = _render_topic_index(topic_entries)
    return rendered


def build(root: Path) -> None:
    """Generate all indexes and the portable pagination manifest."""
    api_entries = extract_api_entries(root)
    topic_entries = extract_topic_entries(root)
    for name, content in _rendered_indexes(root).items():
        (root / name).write_text(content, encoding="utf-8")
    report_dir = root / ".paginate"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "pagination_manifest.json").write_text(
        _manifest_text(root, len(api_entries), len(topic_entries)),
        encoding="utf-8",
    )


def _part_errors(root: Path) -> List[str]:
    groups: Dict[Tuple[str, str], List[int]] = {}
    for path in _markdown_files(root, REFERENCE_DIRS):
        match = PART_NAME.match(path.name)
        if match is None:
            continue
        key = (path.parent.name, match.group("stem"))
        groups.setdefault(key, []).append(int(match.group("number")))
    errors: List[str] = []
    for (directory, stem), numbers in sorted(groups.items()):
        expected = list(range(1, max(numbers) + 1))
        if sorted(numbers) != expected:
            errors.append(f"non-contiguous parts for {directory}/{stem}: {sorted(numbers)}")
    return errors


def check(root: Path) -> CheckResult:
    """Validate pagination and generated index targets without mutating the corpus."""
    errors = _part_errors(root)
    warnings: List[str] = []
    api_entries = extract_api_entries(root)
    topic_entries = extract_topic_entries(root)
    for name, expected in _rendered_indexes(root).items():
        path = root / name
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            errors.append(f"stale generated index: {name}; run the builder again")
    manifest_path = root / ".paginate" / "pagination_manifest.json"
    expected_manifest = _manifest_text(
        root,
        len(api_entries),
        len(topic_entries),
        _existing_physical_pages(root),
    )
    if (
        not manifest_path.is_file()
        or manifest_path.read_text(encoding="utf-8") != expected_manifest
    ):
        errors.append(
            "stale pagination manifest: .paginate/pagination_manifest.json; run the builder again"
        )
    for record in _document_records(root):
        if record["exceeds_limit"]:
            errors.append(
                f"{record['path']} exceeds {TOKEN_LIMIT} estimated tokens "
                f"({record['estimated_tokens']})"
            )
        elif record["exceeds_safety_target"]:
            warnings.append(
                f"{record['path']} exceeds the {int(SAFETY_RATIO * 100)}% safety target "
                f"({record['estimated_tokens']} estimated tokens)"
            )
    for entry in api_entries:
        if not (root / entry.path).is_file():
            errors.append(f"missing API index target: {entry.path}")
    legacy_links = _legacy_html_link_count(root)
    if legacy_links:
        warnings.append(f"{legacy_links} legacy .html links remain in converted source documents")
    signature_mismatches = _signature_name_mismatch_count(api_entries)
    if signature_mismatches:
        warnings.append(
            f"{signature_mismatches} API headings use a shared or mismatched source declaration; "
            "verify those entries in the source document"
        )
    return CheckResult(not errors, errors, warnings)


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1] / "skill-references"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=_default_root())
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    if arguments.check:
        result = check(root)
        for warning in result.warnings:
            print(f"warning: {warning}")
        for error in result.errors:
            print(f"error: {error}")
        return 0 if result.ok else 1
    build(root)
    print(f"generated reference indexes under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
