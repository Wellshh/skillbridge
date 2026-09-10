#!/usr/bin/env python3
"""Fix malformed bullet-image pseudo-tables in sklangref Markdown files.

The current sklangref .md files were converted from an HTML source that used
bullet images in table cells.  The converter rendered each bullet as a separate
2-row "table" with an empty header::

    |  |
    | --- | ---
    | `param` | description text

This script merges consecutive groups into a single proper Markdown table::

    | Name | Description |
    |---|---|
    | `param1` | description text |
    | `param2` | description text |

Sections processed: ``#### Arguments``, ``#### Value Returned``,
``#### Values Returned``, ``#### Argument``, ``#### Arguments:``.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

SKLANGREF_DIR = Path(__file__).resolve().parents[1] / "skill-references" / "sklangref"

# Section headers that contain parameter tables
TABLE_SECTIONS = {
    "#### Arguments",
    "#### Value Returned",
    "#### Values Returned",
    "#### Argument",
    "#### Arguments:",
}

# Malformed table row patterns
EMPTY_HEADER = re.compile(r"^\|\s*\|$")
SEPARATOR = re.compile(r"^\|\s*-{3,}\s*\|\s*-{3,}\s*$")
DATA_ROW = re.compile(r"^\|\s*`([^`]*)`\s*\|\s*(.*?)$")
# Also handle data rows without backticks (rare)
DATA_ROW_PLAIN = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)$")


def _is_table_section(line: str) -> bool:
    """True if line is a section header that contains parameter tables."""
    stripped = line.strip()
    return stripped in TABLE_SECTIONS


def _is_section_header(line: str) -> bool:
    """True if line is any #### heading (marks end of a table section)."""
    return line.strip().startswith("####")


def _parse_data_row(line: str) -> Tuple[str, str] | None:
    """Parse a malformed data row into (param, description)."""
    stripped = line.strip()
    m = DATA_ROW.match(stripped)
    if m:
        return m.group(1), m.group(2).rstrip()
    m = DATA_ROW_PLAIN.match(stripped)
    if m:
        param = m.group(1).strip()
        desc = m.group(2).strip()
        # Skip separator-like rows
        if param.startswith("---") or not param:
            return None
        return param, desc
    return None


def fix_tables_in_file(path: Path) -> int:
    """Fix malformed tables in a single file. Returns number of tables fixed."""
    lines = path.read_text(encoding="utf-8").splitlines()
    result: List[str] = []
    tables_fixed = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if we're entering a table section
        if _is_table_section(line):
            result.append(line)
            i += 1
            # Skip blank lines after section header
            while i < len(lines) and not lines[i].strip():
                result.append(lines[i])
                i += 1

            # Collect all malformed table groups in this section
            groups: List[Tuple[str, str]] = []  # (param, description)
            while i < len(lines):
                stripped = lines[i].strip()

                # End of section
                if _is_section_header(lines[i]) or (
                    stripped and not stripped.startswith("|") and not EMPTY_HEADER.match(stripped)
                    and groups  # only stop if we've collected at least one group
                ):
                    break

                # Empty header row
                if EMPTY_HEADER.match(stripped):
                    i += 1
                    # Expect separator next
                    if i < len(lines) and SEPARATOR.match(lines[i].strip()):
                        i += 1
                    # Expect data row next
                    if i < len(lines):
                        parsed = _parse_data_row(lines[i])
                        if parsed:
                            param, desc = parsed
                            i += 1
                            # Collect continuation lines (non-table, non-heading, non-blank)
                            while i < len(lines):
                                next_stripped = lines[i].strip()
                                if (
                                    not next_stripped
                                    or next_stripped.startswith("|")
                                    or next_stripped.startswith("#")
                                    or EMPTY_HEADER.match(next_stripped)
                                ):
                                    break
                                # Continuation line — append to description
                                desc = desc + " " + next_stripped if desc else next_stripped
                                i += 1
                            groups.append((param, desc))
                        else:
                            # Not a data row — skip
                            i += 1
                    continue

                # Blank line within section
                if not stripped:
                    i += 1
                    continue

                # Non-table, non-blank line — end of section
                break

            if groups:
                # Render as proper Markdown table
                if result and result[-1].strip():
                    result.append("")
                result.append("| Name | Description |")
                result.append("|---|---|")
                for param, desc in groups:
                    # Ensure param has backticks if it looks like a code identifier
                    if not param.startswith("`") and re.match(r"^[A-Za-z_]", param):
                        param_display = f"`{param}`"
                    else:
                        param_display = param
                    # Ensure description ends with |
                    desc_clean = desc.rstrip()
                    if not desc_clean.endswith("|"):
                        desc_clean += " |"
                    result.append(f"| {param_display} | {desc_clean}")
                result.append("")
                tables_fixed += 1
            continue

        result.append(line)
        i += 1

    if tables_fixed:
        path.write_text("\n".join(result) + "\n", encoding="utf-8")
    return tables_fixed


def main() -> None:
    total = 0
    for path in sorted(SKLANGREF_DIR.glob("*.md")):
        count = fix_tables_in_file(path)
        if count:
            print(f"  {path.name}: {count} tables fixed")
            total += count
    print(f"Total: {total} tables fixed across {len(list(SKLANGREF_DIR.glob('*.md')))} files")


if __name__ == "__main__":
    main()
