#!/usr/bin/env python3
"""Validate SKILL API signature well-formedness in the reference corpus.

Catches the PDF/HTML conversion damage that build_reference_indexes.py cannot
see: parameter tokens glued without whitespace (``o_dbidg_layer`` for
``o_dbid g_layer``), signatures copied under the wrong heading, and generated
index rows drifting from the body entries they point at.

Rules:
  R1  structure      - a signature exists, carries ``=>``, balanced ()/[]
  R2  name agreement - heading name matches the signature callee (error in the
      axl domain, warning elsewhere)
  R3  atom shape     - every parameter token is a prefixed atom, a literal, or
      an allowlisted identifier; glued tokens and stray ``?`` markers error
  R4  table cross-check - signature atoms must match the documented
      ``#### Arguments`` table in both directions (the primary glue detector:
      pure prefix regexes cannot split ``n_yn_x``)
  R5  index independence - each generated index row must equal the body
      signature re-parsed at the row's own path:line

Severity policy: algroskill/ findings are errors (the axl domain is the
verified scope); findings in the other reference directories are warnings
until their own sources are reconverted. Exit code is 1 on any error, 0 when
only warnings remain.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, NamedTuple, Optional, Sequence

from build_reference_indexes import (
    API_REFERENCE_DIRS,
    AXL_REFERENCE_DIRS,
    _normalize_arrow,
    _plain_heading,
    _signature_after_heading,
)

INDEX_FILES = (
    "api_index.part01.md",
    "api_index.part02.md",
    "api_index.part03.md",
    "sklang_api_index.part01.md",
    "sklang_api_index.part02.md",
    "sklang_api_index.part03.md",
)
INDEX_ROW = re.compile(r"^\| `(?P<symbol>[^`]*)` \| `(?P<declaration>.*)` \| `(?P<path>[^`]+)` \| (?P<line>\d+) \|$")
INDEX_ESCAPES = {ord("\\"): None}
TYPE_PREFIXES = frozenset(
    {
        "s_", "g_", "t_", "o_", "l_", "x_", "f_", "n_", "d_", "r_", "p_", "b_", "i_", "u_",
        "lo_", "lg_", "lt_", "ls_", "ld_", "lx_", "us_", "tsu_",
    }
)
PREFIX_LETTERS = "sgtxolfn"
GLUED_PREFIX = re.compile(rf"[A-Za-z0-9]([{PREFIX_LETTERS}])_")
PREFIXED_ATOM = re.compile(r"^[a-z]{1,2}_[A-Za-z0-9_]+$")
UNPREFIXED_ATOM = re.compile(r"^_?[A-Za-z][A-Za-z0-9_]*$")
UPPERCASE_PREFIXED = re.compile(r"^[A-Za-z]{1,2}_[A-Za-z0-9_]+$")
LITERAL_ATOM = re.compile(r"^(\"[^\"]*\"|'[^']*'|'[A-Za-z][A-Za-z0-9_]*|nil|t|<[^<>]*>)$")
ARGUMENT_NAME = re.compile(r"`([a-z]{1,2}_[A-Za-z0-9_]*)`")
# Identifier-shaped atoms that are documented literals rather than type-prefixed
# parameters (for example S_x/uppercase renderings and camelCase names).
ALLOWLISTED_ATOMS = frozenset(
    {
        "piList",
        "Sx_arg1",
        "Sx_arg2",
        # SKILL++ object-system parameter names (skoopref/skdevref PDFs)
        "obj",
        "initargs",
        "value1",
        "value2",
        "U_funObject",
        "U_genericfuncObj",
        "break_condition",
        "break_tag",
        # SKILL++ debug function parameter names (skdevref PDF)
        "S_name",
        "S_string",
        "S_fileName",
        "S_property",
        "S_functionName",
        "S_messageName",
        "S_mode",
        "smode",
        "xy",
        "tx",
        "_nestingLevel",
        # axl-domain camelCase parameter names (sipapd bond-wire, dbid, filter)
        "all",
        "background",
        "bondFingers",
        "bondWires",
        "comp",
        "deleteWires",
        "ewlLength",
        "fingerAlign",
        "fingerLocation",
        "fingerName",
        "fingerPadstack",
        "fingerRotation",
        "fingerSnap",
        "line",
        "list",
        "lowerRight_xy",
        "lud_dbid",
        "mirror",
        "net_dbid",
        "onEnabledF",
        "orient",
        "origin",
        "parentSymbol",
        "pin_dbid",
        "placementStyle",
        "point",
        "profileName",
        "S_filter",
        "setAsMaster",
        "upperLeft_xy",
        "visible",
        "wireDiameter",
        "wireEndLocation",
        "wireEndOwner",
        "wireProfile",
        "wireStartLocation",
        "wireStartOwner",
        "xmlFileName",
        # compound parameter names that the glue detector false-positives on
        "t_varName_or_nameValuePair",
    }
)


class Finding(NamedTuple):
    severity: str  # "error" or "warning"
    path: str
    line: int
    reason: str


class BodyEntry(NamedTuple):
    name: str
    signature: str
    path: str
    line: int
    is_axl: bool
    aliases: Tuple[str, ...] = ()


def _unescape_index_cell(value: str) -> str:
    return value.translate(INDEX_ESCAPES)


STRUCTURAL_ATOMS = frozenset(
    {
        "...",
        "@rest",
        "@key",
        "@optional",
        "@body",
        "@initarg",
        "@reader",
        "@writer",
        "@initform",
        "@before",
        "@after",
        "@around",
        "(",
        ")",
        "{",
        "}",
        "*",
        "list(",
        # SKILL infix assignment operator; appears inside syntax forms such as
        # ``setq( s_variableName = g_newValue )`` (sklangref setq, second form)
        "=",
    }
)


def _split_atoms(parameter_text: str) -> List[str]:
    """Split the parameter text into candidate atoms.

    Optional-argument brackets and ``?`` markers are stripped wherever they
    occur; nested ``list( ... )`` value groups are split at their parentheses;
    ``...``/``@rest``-style structural tokens survive untouched so the caller
    can allowlist them.
    """
    parameter_text = re.sub(
        r"<([^<>]*)>",
        lambda match: "<" + match.group(1).replace(" ", "\x00").replace("/", "\x01") + ">",
        parameter_text,
    )
    # normalize any run of 2+ dots (PDF extraction artifact) to the SKILL
    # repeat marker ``...``
    parameter_text = re.sub(r"\.{2,}", "...", parameter_text)
    # separate glued closing/opening parens: ``)(`` → ``) (``
    parameter_text = parameter_text.replace(")(", ") (")
    # separate a closing paren glued to a following identifier: ``)body`` → ``) body``
    parameter_text = re.sub(r"\)([A-Za-z_])", r") \1", parameter_text)
    # collapse macro sub-expression calls: ``s_funcName( l_formalArglist )``
    # is a lambda-list element (the inner parens are not parameter delimiters);
    # strip the inner ``(`` only when it follows a type-prefixed identifier
    parameter_text = re.sub(r"\b([a-z]{1,2}_[A-Za-z0-9_]*)\(", r"\1 ", parameter_text)
    parameter_text = parameter_text.replace("(", "( ").replace(")", " ) ")
    # Normalize SKILL choice syntax ({ a | b } → ( a / b )) so the splitter
    # sees the braces as structural tokens and the pipe as a slash separator
    parameter_text = parameter_text.replace("{", "{ ").replace("}", " } ")
    parameter_text = parameter_text.replace("|", "/")
    atoms: List[str] = []
    for run in re.split(r"[,\s]+", parameter_text):
        for atom in run.split("/"):
            atom = atom.replace("\x00", " ").replace("\x01", "/").replace("[", "").replace("]", "").strip()
            # normalize two-dot repeat markers (PDF extraction artifact)
            if atom == "..":
                atom = "..."
            if atom.endswith("..."):
                if atom[:-3]:
                    atoms.append(atom[:-3])
                atoms.append("...")
                continue
            if atom.startswith("...") and len(atom) > 3:
                atoms.append("...")
                atoms.append(atom[3:])
                continue
            if atom:
                atoms.append(atom)
    return atoms


def _parameter_text(signature: str) -> Optional[str]:
    """Return the text of the first balanced (...) group, or None."""
    start = signature.find("(")
    if start < 0:
        return None
    depth = 0
    for index in range(start, len(signature)):
        char = signature[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return signature[start + 1 : index]
    return None


def _bracket_errors(signature: str) -> Optional[str]:
    depth_paren = 0
    depth_bracket = 0
    for char in signature:
        if char == "(":
            depth_paren += 1
        elif char == ")":
            depth_paren -= 1
        elif char == "[":
            depth_bracket += 1
        elif char == "]":
            depth_bracket -= 1
        if depth_paren < 0 or depth_bracket < 0:
            return "unbalanced brackets"
    if depth_paren or depth_bracket:
        return "unbalanced brackets"
    return None


def _is_glued_atom(atom: str) -> bool:
    """Detect a parameter token that swallowed a following prefixed atom.

    A token is glued when some interior position splits it into two complete
    prefixed atoms (``o_dbidg_layert_symbol`` = ``o_dbid g_layert_symbol`` →
    ``o_dbid g_layer t_symbol``). The split point sits between letters where
    the dropped space used to be, so every interior offset is probed, not just
    underscores. Both halves must carry a *known* type prefix — otherwise
    ordinary multi-word names like ``t_new_name`` would split into nonsense
    pairs like ``t_n``/``ew_name``. Multi-underscore parameter names like
    ``l_ref_point`` survive when they are listed in their own Arguments table
    (the table is ground truth); atoms absent from a table stay subject to
    this rule.
    """
    for index in range(3, len(atom) - 2):
        head, tail = atom[:index], atom[index:]
        if not (PREFIXED_ATOM.match(head) and PREFIXED_ATOM.match(tail)):
            continue
        if head.split("_", 1)[0] + "_" in TYPE_PREFIXES and tail.split("_", 1)[0] + "_" in TYPE_PREFIXES:
            return True
    return False


def check_signature_shape(
    entry: BodyEntry,
    table_names: Sequence[str] = (),
) -> Iterable[tuple[str, str]]:
    """Yield (severity, reason) findings for R1-R3 on one signature.

    ``table_names`` are the parameter names documented in the entry's own
    ``#### Arguments`` table and act as ground truth: a token the table
    documents is accepted verbatim, so multi-underscore names like
    ``l_ref_point`` that a regex cannot distinguish from glued tokens are
    spared wherever they are properly documented.
    """
    severity = "error" if entry.is_axl else "warning"
    documented = frozenset(table_names)
    signature = entry.signature
    if "=>" not in signature:
        yield severity, "signature has no '=>' return separator"
    bracket_reason = _bracket_errors(signature)
    if bracket_reason:
        yield severity, bracket_reason
    callee = signature.split("(", 1)[0].strip()
    accepted_names = {entry.name.casefold()} | {alias.casefold() for alias in entry.aliases}
    if callee.casefold() not in accepted_names:
        yield severity, f"heading name {entry.name!r} does not match signature callee {callee!r}"
    parameter_text = _parameter_text(signature)
    if parameter_text is None:
        yield severity, "signature has no (...) parameter group"
        return
    for atom in _split_atoms(parameter_text):
        if LITERAL_ATOM.match(atom) or atom in STRUCTURAL_ATOMS or atom in ALLOWLISTED_ATOMS:
            continue
        if atom in documented:
            continue
        if atom.startswith("?"):
            option_name = atom[1:].strip()
            if re.match(r"^[A-Za-z][A-Za-z0-9_]*$", option_name or ""):
                continue  # documented optional-argument marker (?name)
            yield severity, f"malformed optional-argument marker {atom!r}"
            continue
        if "?" in atom:
            yield severity, f"glued optional-argument marker in token {atom!r}"
            continue
        if PREFIXED_ATOM.match(atom):
            if _is_glued_atom(atom):
                yield severity, f"glued parameter token {atom!r}"
            continue
        if UPPERCASE_PREFIXED.match(atom) or UNPREFIXED_ATOM.match(atom):
            # only the axl domain enforces the type-prefix convention;
            # SKILL++ and sklang APIs use camelCase and uppercase names
            if entry.is_axl:
                yield "warning", f"unprefixed identifier atom {atom!r} (allowlist if literal)"
            continue
        yield severity, f"malformed parameter token {atom!r}"


# Entries exempt from the arguments-table cross-check (R4) because the source
# document's table rows are not parameters of this call form at all, or the
# source itself wobbles between two spellings of the same parameter.  Mirrors
# TABLE_SKIP_R4 in convert_html_references.py (keyed there by chapter anchor;
# the rendered corpus carries no anchors, so this list keys by API name):
#   axlFormCreate  - g_form/t_callback/s_callback are rows of the g_formAction
#                    "Action Options" sub-table, not axlFormCreate parameters
#   axlDMFileBrowse- the source table spells the options g_title/g_filters
#                    while the declaration spells ?title t_title / ?optFilters
#   axlDistance    - the source table documents the two alternate call forms
#                    generically (l_point / ll_line) while the declaration
#                    names the points l_point1/l_point2
#   axlDiffPair    - the source table documents the net arguments generically
#                    (o_net / t_net) while the declaration names the pair
#                    o_net1/t_net1/o_net2/t_net2
#
# sklangref source-document wobble (the Cadence SKILL Language Reference itself
# is inconsistent between signatures and Arguments tables):
#   let/letrec/letseq - SKILL-mode signature vs SKILL++-mode table params
#                       (binding-pair syntax flattened into separate rows)
#   declareLambda/declareNLambda - repeating s_namen param not in table
#   append       - third overload (o_table1 o_table2) params not in table
#   fscanf/scanf/sscanf - multi-name heading; table documents t_sourcestring
#                         which belongs to a different overload
#   info         - table spells g_args/r_formatstring, signature spells
#                  g_args1/t_formatstring (source naming variant)
#   foreachs     - table documents g_exprtable/s_mappingfunction from a
#                  different overload
#   if           - signature lists g_elseexpr1/g_thenexpr1 (optional params
#                  not documented in the table)
#   setSG        - signature lists g_value (not in table)
#   Vector       - table documents g_init_val/x_size, signature spells g_value
#   setarray     - signature lists g_value (not in table)
#   warn         - signature lists g_arg1 (optional, not in table)
#   remove       - table documents g_key/o_table from a different overload
#   addToNamespace - signature lists t_namespacename (optional, not in table)
#   shadow       - signature lists t_namespace (optional, not in table)
#   pcreCompile  - signature lists x_options (optional, not in table)
#   setq         - second syntax form spells the value g_newValue while the
#                  table documents the first form's g_newValueExp
TABLE_SKIP_R4_NAMES = frozenset({
    "axlFormCreate", "axlDMFileBrowse", "axlDistance", "axlDiffPair",
    # sklangref source-document wobble
    "let", "letrec", "letseq",
    "declareLambda", "declareNLambda",
    "append", "fscanf", "scanf", "sscanf",
    "info", "foreachs", "if",
    "setSG", "Vector", "setarray", "warn",
    "remove", "addToNamespace", "shadow", "pcreCompile",
    "setq",
})


def _collect_signatures(slice_lines: Sequence[str], name: str = "") -> List[str]:
    """Signature lines in a rendered slice: inline backtick lines carrying
    ``=>``. Fenced code blocks are skipped - they hold raw PDF page text or
    multi-line declarations that the signature extractor handles separately."""
    signatures: List[str] = []
    in_code_block = False
    for line in slice_lines:
        candidate = line.strip()
        if candidate.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if candidate.startswith("`") and candidate.endswith("`"):
            declaration = _normalize_arrow(candidate.strip("`"))
            if "=>" in declaration:
                signatures.append(declaration)
    return signatures


def _all_signatures_after_heading(
    lines: Sequence[str], heading_index: int, name: str = ""
) -> List[str]:
    """Every signature line rendered under the heading (overloaded call forms).

    Overloads render as consecutive backtick lines separated by ``or`` or a
    caption line; scanning stops at the first subheading.
    """
    collected: List[str] = []
    index = heading_index + 1
    while index < len(lines) and not lines[index].startswith(("### ", "#### ")):
        index += 1
    return _collect_signatures(lines[heading_index + 1 : index], name)


def _argument_table_names(
    lines: Sequence[str], entry_index: int
) -> Optional[tuple[List[str], int]]:
    """Backticked parameter names from the entry's #### Arguments table.

    Returns the names together with the heading's line index (used to union
    the sibling signatures of a function family sharing one table).

    Function families render as consecutive bare headings (a signature but no
    subheadings) followed by the sibling holding the shared sections; the
    scan crosses those bare headings to find the family's table, but stops at
    any entry that has subheadings of its own so an unrelated neighbour's
    table is never attributed here.
    """
    limit = min(entry_index + 80, len(lines))
    block_has_subheading = False
    offset = entry_index + 1
    while offset < limit:
        line = lines[offset]
        if line.startswith("#### Arguments"):
            table: List[str] = []
            for row in lines[offset + 1 : min(offset + 200, len(lines))]:
                if row.startswith("### ") or row.startswith("#### "):
                    break
                if not row.startswith("|"):
                    continue
                cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
                if len(cells) < 2 or set(cells[0]) <= {"-", " "}:
                    continue
                for match in ARGUMENT_NAME.finditer(cells[0]):
                    table.append(match.group(1))
            return table, offset
        if line.startswith("#### "):
            block_has_subheading = True
        elif line.startswith("### "):
            if block_has_subheading:
                return None
            block_has_subheading = False
        offset += 1
    return None


def _delist(atom: str) -> str:
    """Strip the leading ``l`` from a list-prefixed atom (``lo_dbid`` → ``o_dbid``).

    SKILL type convention: ``l`` + prefix = list of that type.  The Arguments
    table usually documents the singular form while the declaration uses the
    list form; de-listing lets the R4 cross-check recognize the match.
    Only de-list the well-established two-letter list prefixes to avoid
    creating spurious intermediate atoms.
    """
    for prefix in ("lo_", "lg_", "lt_", "ls_", "ld_", "lx_"):
        if atom.startswith(prefix):
            return atom[1:]
    return atom


def check_table_agreement(
    entry: BodyEntry, table: Optional[List[str]], signatures: Sequence[str] = ()
) -> Iterable[tuple[str, str]]:
    """R4: the Arguments table must not document parameters the signatures lost.

    Parameters the table documents but no rendered signature carries indicate
    dropped tokens (a glued or truncated declaration), so they error - but a
    single straggler is usually source-document wobble (alternate spellings,
    option sub-table rows) and only warns.  Signature-only parameters are
    usually optional arguments or alternatives like ``o_dbid/lo_dbid`` and
    only warn.  The union of every rendered overload counts as coverage.
    List-form variants (``lo_dbid`` ↔ ``o_dbid``) are treated as matches.
    """
    if table is None or entry.name in TABLE_SKIP_R4_NAMES:
        return
    # the printed docs wobble on case (t_netName vs t_netname); only whole
    # missing parameters indicate real glue or drift
    table_atoms = {name.casefold() for name in table}
    signature_atoms: set = set()
    for signature in signatures or ([entry.signature] if entry.signature else []):
        parameter_text = _parameter_text(signature)
        if parameter_text is None:
            continue
        signature_atoms |= {
            atom.casefold()
            for atom in _split_atoms(parameter_text)
            if PREFIXED_ATOM.match(atom)
            and (not _is_glued_atom(atom) or atom.casefold() in table_atoms)
        }
    # accept list-form variants: lo_dbid in the signature also covers o_dbid
    # in the table (SKILL convention: l + prefix = list of that type).
    # Both directions are guarded: only add the variant form when the
    # counterpart already exists in the other set, avoiding spurious atoms.
    signature_atoms |= {
        _delist(a) for a in signature_atoms if _delist(a) in table_atoms
    }
    table_atoms |= {
        "l" + a for a in table_atoms if "l" + a in signature_atoms
    }
    table_atoms |= {
        _delist(a) for a in table_atoms if _delist(a) in signature_atoms
    }
    if not table_atoms:
        return
    missing_in_signature = table_atoms - signature_atoms
    missing_in_table = signature_atoms - table_atoms
    if len(missing_in_signature) >= 2:
        severity = "error" if entry.is_axl else "warning"
        yield severity, (
            f"arguments table documents {sorted(missing_in_signature)} "
            "missing from the signature"
        )
    elif missing_in_signature and not entry.is_axl:
        # axl domain: converter gate already validated; single-missing is
        # known source-document naming wobble (t_name vs s_trigger etc.)
        yield "warning", (
            f"arguments table documents {sorted(missing_in_signature)} "
            "missing from the signature"
        )
    if missing_in_table and not entry.is_axl:
        yield "warning", (
            f"signature lists {sorted(missing_in_table)} "
            "missing from the arguments table"
        )


def _body_entries(root: Path, directory: str) -> List[tuple[BodyEntry, List[str], int]]:
    collected: List[tuple[BodyEntry, List[str], int]] = []
    dir_path = root / directory
    if not dir_path.is_dir():
        return collected
    for path in sorted(dir_path.glob("*.md")):
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
                if name.strip() and name.strip() not in {"...", "…"}
            ]
            if not names:
                continue
            # skip non-API headings (document titles, section headers like
            # "Cadence SKILL Language Reference ..." or "caar, caaar, ...")
            # that the signature extractor mistakenly picked up
            if not all(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name) for name in names):
                continue
            entry = BodyEntry(
                name=names[0],
                aliases=tuple(names[1:]),
                signature=signature,
                path=path.relative_to(root).as_posix(),
                line=index + 1,
                is_axl=directory in AXL_REFERENCE_DIRS,
            )
            collected.append((entry, lines, index))
    return collected


def check_body(root: Path) -> List[Finding]:
    findings: List[Finding] = []
    for directory in AXL_REFERENCE_DIRS + API_REFERENCE_DIRS:
        for entry, lines, entry_index in _body_entries(root, directory):
            table_info = _argument_table_names(lines, entry_index)
            table = table_info[0] if table_info else None
            signatures = _all_signatures_after_heading(lines, entry_index, entry.name)
            for signature in signatures or [entry.signature]:
                overload = entry._replace(signature=signature)
                for severity, reason in check_signature_shape(overload, table or ()):
                    findings.append(Finding(severity, entry.path, entry.line, reason))
            if table_info:
                # function families print as consecutive headings whose
                # signatures all document one shared Arguments table (the
                # axlPathArc* pattern), so coverage is the union from the
                # first sibling's heading to the shared table
                _, table_offset = table_info
                group_start = entry_index
                cursor = entry_index - 1
                while cursor >= 0 and not lines[cursor].startswith("#### "):
                    if lines[cursor].startswith("### "):
                        group_start = cursor
                    cursor -= 1
                group_signatures = _collect_signatures(lines[group_start + 1 : table_offset], entry.name)
            else:
                group_signatures = signatures
            for severity, reason in check_table_agreement(entry, table, group_signatures):
                findings.append(Finding(severity, entry.path, entry.line, reason))
    return findings


def check_indexes(root: Path) -> List[Finding]:
    """R5: every generated index row must equal the body signature at path:line."""
    findings: List[Finding] = []
    body_cache: Dict[str, List[str]] = {}
    for index_name in INDEX_FILES:
        path = root / index_name
        if not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = INDEX_ROW.match(line)
            if match is None:
                continue
            target_path = match.group("path")
            target_line = int(match.group("line"))
            expected_declaration = _normalize_arrow(_unescape_index_cell(match.group("declaration")))
            if target_path not in body_cache:
                target = root / target_path
                body_cache[target_path] = (
                    target.read_text(encoding="utf-8").splitlines() if target.is_file() else []
                )
            lines = body_cache[target_path]
            if not lines or target_line > len(lines):
                findings.append(
                    Finding("error", index_name, line_number, f"index target missing: {target_path}:{target_line}")
                )
                continue
            heading_index = target_line - 1
            if not lines[heading_index].startswith("### "):
                findings.append(
                    Finding(
                        "error",
                        index_name,
                        line_number,
                        f"index target {target_path}:{target_line} is not an API heading",
                    )
                )
                continue
            body_signature = _signature_after_heading(lines, heading_index)
            if body_signature is None or body_signature != expected_declaration:
                findings.append(
                    Finding(
                        "error",
                        index_name,
                        line_number,
                        f"index declaration differs from body {target_path}:{target_line}",
                    )
                )
    return findings


def check(root: Path) -> tuple[bool, List[str], List[str]]:
    findings = check_body(root) + check_indexes(root)
    errors = [f"{f.path}:{f.line}: {f.reason}" for f in findings if f.severity == "error"]
    warnings = [f"{f.path}:{f.line}: {f.reason}" for f in findings if f.severity == "warning"]
    return (not errors, errors, warnings)


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1] / "skill-references"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=_default_root())
    arguments = parser.parse_args(argv)
    ok, errors, warnings = check(arguments.root.resolve())
    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
