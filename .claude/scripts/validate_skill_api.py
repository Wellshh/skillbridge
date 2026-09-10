#!/usr/bin/env python3
"""Corpus-grounded API validator for generated SKILL ``.il`` / ``.ils`` code.

``skill_lint.py`` is purely lexical: it catches unbalanced parentheses and
unterminated strings but knows nothing about the Allegro API, so a hallucinated
``axlGetNetByName`` sails through with exit 0 and is only caught later by a
full Windows Allegro session.  This validator closes that gap offline by
checking every call site against the generated reference indexes
(``api_index.part*.md`` + ``sklang_api_index.part*.md``, 1411 indexed symbols)
plus explicitly verified platform-only callables in ``verified_facts.json``.

Checks
------
``unknown-api``
    An ``axl``-prefixed call whose name is not in the corpus index.  This is
    the hallucination signature: agents invent plausible Allegro names.  The
    finding carries up to three ranked real candidates so the fix is a
    substitution, not a guess.  A fact marked ``verified`` with
    ``isCallable=true`` is an intentional platform-only exception; facts
    marked ``isCallable=false`` remain errors.
``arity``
    A known API called with an argument count outside its documented
    ``[required, required + optional]`` range.  Only evaluated for signatures
    simple enough to count unambiguously (no variadic ``...``, no ``?keyword``
    args, no ``/`` choice groups); ambiguous signatures are skipped rather
    than guessed at.
``unknown-keyword``
    A ``?keyword`` argument absent from the called API's signature.

Calibration
-----------
Unknown names outside the ``axl`` namespace are deliberately **not** reported:
the corpus documents Allegro PCB (``axl*``) and the general SKILL language, but
official Cadence example code also calls ``dbc*``, ``tsel*``, ``ash*`` and
per-file test procedures that share the ``axl`` prefix.  File-level scope
analysis collects every locally bound name (``procedure``, ``let``/``prog``
variables, ``lambda``/``foreach`` parameters, assignment targets) so those are
never flagged.  Run ``--self-test`` to measure the false-positive rate against
the bundled official examples.

Exit status is 1 when any error-severity finding is reported.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Sequence, Set, Tuple

# ---------------------------------------------------------------------------
# corpus ground truth
# ---------------------------------------------------------------------------

AXL_INDEX_GLOB = "api_index.part*.md"
SKLANG_INDEX_GLOB = "sklang_api_index.part*.md"
INDEX_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`(.+?)`\s*\|\s*`(.+?)`\s*\|\s*(\d+)\s*\|$")
EXAMPLES_GLOB = "examples/**/*.il"
FACTS_FILENAME = "verified_facts.json"
# Length-preserving, non-splittable filler for blanked string contents.  Must
# not be whitespace (the arity counter would re-split the literal) and must not
# be an identifier character (it would merge with neighbouring tokens).
STRING_FILLER = "\x00"

IDENTIFIER = r"[A-Za-z_][A-Za-z0-9_!?<>*+\-]*"

# Forms whose first argument is the name being bound.  Both call syntaxes are
# handled lexically, so ``(defun f (x) ...)`` and ``define( f lambda(...) )``
# bind ``f`` alike.  ``defInitProc``/``defUserInitProc`` are excluded: they
# register an already-existing procedure rather than defining a new name.
DEFINING_FORMS = frozenset(
    name.casefold()
    for name in (
        "procedure", "defun", "defmacro", "defalias", "define",
        "declareLambda", "declareNLambda", "defStruct", "defclass",
        "defmethod", "defvar",
    )
)

# Loop forms bind their iteration variable in the same position a defining form
# binds its name: ``foreach( item list body )``.
LOOP_FORMS = frozenset(name.casefold() for name in ("foreach", "for", "dotimes"))

# Forms that bind the first identifier inside the group (definition or loop).
BINDS_FIRST_FORMS = DEFINING_FORMS | LOOP_FORMS

# Forms whose binding-list group introduces local variables/parameters.
PARAMETERISED_FORMS = frozenset(
    name.casefold()
    for name in (
        "let", "letseq", "letrec", "letStar", "prog", "prog1", "prog2",
        "lambda", "procedure", "defun", "defmacro", "defmethod",
    )
)


class Arity(NamedTuple):
    """What one documented declaration allows at a call site."""

    required: int
    optional: int
    variadic: bool
    keywords: Tuple[str, ...]
    countable: bool


class ApiSpec(NamedTuple):
    """One documented API symbol, with every overload it declares."""

    name: str
    signature: str
    source: str
    line: int
    arities: Tuple[Arity, ...]

    @property
    def keywords(self) -> Tuple[str, ...]:
        seen: List[str] = []
        for arity in self.arities:
            for keyword in arity.keywords:
                if keyword not in seen:
                    seen.append(keyword)
        return tuple(seen)

    @property
    def countable(self) -> bool:
        """Arity is only judgeable when *every* overload is countable.

        A variadic or keyword-taking alternative can absorb any argument count,
        so the presence of one makes positional checking unsound.
        """
        return bool(self.arities) and all(a.countable for a in self.arities)

    def accepts(self, count: int) -> bool:
        return any(a.required <= count <= a.required + a.optional for a in self.arities)

    def arity_summary(self) -> str:
        parts = []
        for arity in self.arities:
            if arity.optional:
                parts.append(f"{arity.required}-{arity.required + arity.optional}")
            else:
                parts.append(str(arity.required))
        return " or ".join(dict.fromkeys(parts))


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1] / "skill-references"


def _parameter_text(signature: str) -> Optional[str]:
    """Text of the first balanced ``(...)`` group, or None."""
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


def _top_level_tokens(text: str) -> List[str]:
    """Split parameter text on whitespace at nesting depth zero.

    Bracketed optional groups and parenthesised sub-groups stay intact so
    ``[ ?langMode g_langMode ]`` counts as one optional parameter.
    """
    tokens: List[str] = []
    depth = 0
    current: List[str] = []
    for char in text:
        if char in "([":
            depth += 1
            current.append(char)
        elif char in ")]":
            depth -= 1
            current.append(char)
        elif char.isspace() and depth == 0:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(char)
    if current:
        tokens.append("".join(current))
    return tokens


def _parse_arity(signature: str) -> Arity:
    """Derive what one documented declaration allows at a call site."""
    parameter_text = _parameter_text(signature)
    if parameter_text is None:
        return Arity(0, 0, False, (), False)

    tokens = _top_level_tokens(parameter_text)
    required = 0
    optional = 0
    variadic = False
    keywords: List[str] = []
    ambiguous = False
    for token in tokens:
        stripped = token.strip()
        if not stripped:
            continue
        # keyword arguments make positional counting meaningless
        for match in re.finditer(r"\?([A-Za-z_][A-Za-z0-9_]*)", stripped):
            keywords.append(match.group(1))
        if "?" in stripped:
            ambiguous = True
        # ``...`` may sit inside a bracket group (``printf( t_fmt [ g_arg1 ... ] )``)
        # or stand alone; either way the form absorbs any number of arguments
        if "..." in stripped or "...." in stripped:
            variadic = True
            if stripped.startswith("["):
                optional += 1
            elif stripped not in {"...", "...."}:
                required += 1
            continue
        # ``t_name/o_dbid`` choice groups are still one positional slot
        if stripped.startswith("["):
            optional += 1
        else:
            required += 1
    countable = not ambiguous and not variadic and not keywords
    return Arity(required, optional, variadic, tuple(dict.fromkeys(keywords)), countable)


def load_corpus(root: Path) -> Dict[str, ApiSpec]:
    """Every documented symbol, keyed by lowercased name.

    Overloaded symbols accumulate one :class:`Arity` per declaration so a call
    matching *any* documented form is accepted.
    """
    specs: Dict[str, ApiSpec] = {}
    for pattern in (AXL_INDEX_GLOB, SKLANG_INDEX_GLOB):
        for path in sorted(root.glob(pattern)):
            for row in path.read_text(encoding="utf-8").splitlines():
                match = INDEX_ROW.match(row)
                if match is None:
                    continue
                name, signature, source, line = match.groups()
                key = name.casefold()
                arity = _parse_arity(signature)
                existing = specs.get(key)
                if existing is None:
                    specs[key] = ApiSpec(
                        name=name,
                        signature=signature,
                        source=source,
                        line=int(line),
                        arities=(arity,),
                    )
                elif arity not in existing.arities:
                    specs[key] = existing._replace(
                        arities=existing.arities + (arity,)
                    )
    return specs


def load_verified_callables(root: Path) -> Set[str]:
    """Return platform-only symbols confirmed callable by a real probe.

    Facts intentionally do not supply a signature, so these names bypass only
    ``unknown-api``; callers still need the Windows gate for signature/arity.
    The constraint marker is the backward-compatible schema used by the
    existing facts file, while ``isCallable=false`` entries are not admitted.
    """
    path = root / FACTS_FILENAME
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    facts = data.get("facts", []) if isinstance(data, dict) else []
    return {
        str(fact["api"]).casefold()
        for fact in facts
        if isinstance(fact, dict)
        and fact.get("status") == "verified"
        and re.search(r"\bisCallable\s*=\s*true\b", str(fact.get("constraint", "")), re.I)
        and fact.get("api")
    }


# ---------------------------------------------------------------------------
# SKILL lexing and scope analysis
# ---------------------------------------------------------------------------


def strip_comments_and_strings(text: str) -> str:
    """Blank out ``;`` comments, string literals and quoted lists.

    Offsets stay aligned with the original text so reported line and column
    numbers are the author's, not the lexer's.  Blanked spans become
    ``STRING_FILLER`` rather than spaces: a space-filled literal would be
    re-split into several argument tokens by the arity counter.

    A quoted list ``'( a b )`` is data, not a call, so its whole balanced group
    is blanked; a quoted atom ``'sym`` needs no treatment because it carries no
    parenthesis for the call-site scan to find.
    """
    out: List[str] = []
    index = 0
    length = len(text)
    in_string = False
    in_comment = False
    while index < length:
        char = text[index]
        if in_comment:
            if char == "\n":
                in_comment = False
                out.append(char)
            else:
                out.append(" ")
            index += 1
            continue
        if in_string:
            if char == "\\" and index + 1 < length:
                out.append(STRING_FILLER * 2)
                index += 2
                continue
            if char == '"':
                in_string = False
                out.append('"')
            elif char == "\n":
                # unterminated string: let skill_lint report it, stop lexing it
                in_string = False
                out.append(char)
            else:
                out.append(STRING_FILLER)
            index += 1
            continue
        if char == ";":
            in_comment = True
            out.append(" ")
            index += 1
            continue
        if char == '"':
            in_string = True
            out.append(char)
            index += 1
            continue
        if char == "'":
            probe = index + 1
            while probe < length and text[probe].isspace() and text[probe] != "\n":
                probe += 1
            if probe < length and text[probe] == "(":
                close = _match_closing_paren(text, probe)
                if close is not None:
                    span = text[index : close + 1]
                    # keep newlines so line numbering survives
                    out.append(
                        "".join("\n" if c == "\n" else STRING_FILLER for c in span)
                    )
                    index = close + 1
                    continue
            out.append(char)
            index += 1
            continue
        out.append(char)
        index += 1
    return "".join(out)


class _Group(NamedTuple):
    """State for one open parenthesis while scanning for bound names."""

    depth: int
    kind: str  # "define-prefix" | "params" | "plain"
    ident_count: int
    child_used: bool
    binds_all: bool


def collect_local_names(lexed: str) -> Set[str]:
    """Every name the file binds itself, so calls to them are not external.

    SKILL accepts both call syntaxes, and the bound name sits in a different
    position in each::

        procedure( axlHelper( x ) ... )   conventional: opener before the paren
        (defun axlHelper (x) ...)         prefix: form is the first identifier

    Groups are therefore tracked lexically.  Scope is deliberately file-level
    rather than block-level: over-approximating the set of local names trades a
    little sensitivity for a much lower false-positive rate on real code.

    Known limitation: a conventional-form opener must be immediately followed by
    its parenthesis.  ``procedure ( f( x ) )`` with a space before the paren is
    not recognised as a definition, because tolerating that space would make the
    Lisp prefix form ``(null (car x))`` attribute the inner call's arguments to
    ``null``.  Under-binding costs a false positive; over-binding would hide a
    real hallucination, so the conservative side is chosen.
    """
    locals_: Set[str] = set()
    depth = 0
    groups: List[_Group] = []
    pending: Optional[str] = None
    pending_end = -1
    index = 0
    length = len(lexed)

    while index < length:
        char = lexed[index]

        if char in "([":
            depth += 1
            opener = pending if pending_end == index else None
            scan = index + 1
            head = None
            while scan < length:
                if lexed[scan].isspace():
                    scan += 1
                    continue
                # skip string literals: some forms put a context name first
                if lexed[scan] == '"':
                    close_quote = lexed.find('"', scan + 1)
                    if close_quote < 0:
                        break
                    scan = close_quote + 1
                    continue
                head_match = re.match(IDENTIFIER, lexed[scan:])
                head = head_match.group(0) if head_match else None
                break

            binds_all = False
            kind = "plain"
            if opener is not None:
                if opener.casefold() in BINDS_FIRST_FORMS and head:
                    # conventional defining/loop form: the head is the bound name
                    locals_.add(head.casefold())
                elif opener.casefold() in PARAMETERISED_FORMS:
                    kind = "params"
            elif head is not None:
                if head.casefold() in BINDS_FIRST_FORMS:
                    # prefix defining form: the second identifier is bound
                    kind = "define-prefix"
                elif head.casefold() in PARAMETERISED_FORMS:
                    kind = "params"
            # a binding list nested directly inside a parameterised form
            if groups and groups[-1].kind == "params" and not groups[-1].child_used:
                binds_all = True
                groups[-1] = groups[-1]._replace(child_used=True)

            groups.append(_Group(depth, kind, 0, False, binds_all))
            index = scan
            continue

        if char in ")]":
            while groups and groups[-1].depth >= depth:
                groups.pop()
            depth -= 1
            pending = None
            index += 1
            continue

        if char in {'"', STRING_FILLER}:
            index += 1
            continue

        match = re.match(IDENTIFIER, lexed[index:])
        if match is None:
            index += 1
            continue
        token = match.group(0)
        lowered = token.casefold()
        index += len(token)
        pending = token
        pending_end = index

        if not groups:
            continue
        top = groups[-1]
        if top.binds_all:
            # inside a let/prog/lambda binding list
            locals_.add(lowered)
            continue
        count = top.ident_count + 1
        groups[-1] = top._replace(ident_count=count)
        if top.kind == "define-prefix" and count == 2:
            locals_.add(lowered)

    # assignment targets (SKILL creates globals implicitly on first assign)
    for match in re.finditer(rf"({IDENTIFIER})\s*=(?!=)", lexed):
        locals_.add(match.group(1).casefold())
    return locals_


class CallSite(NamedTuple):
    name: str
    line: int
    column: int
    arguments: List[str]
    keywords: Tuple[str, ...]


# Conventional SKILL call: ``name( a b )``.  No whitespace is allowed before the
# parenthesis - permitting it would make the Lisp prefix form ``(null (car x))``
# match at ``null`` and attribute the inner call's arguments to the outer one.
CONVENTIONAL_CALL = re.compile(rf"({IDENTIFIER})\(")
# Lisp prefix call: ``( name a b )``.  The open paren must not be preceded by an
# identifier character (that would be the conventional form's own parenthesis),
# and the name must be followed by whitespace or the closing paren.
PREFIX_CALL = re.compile(rf"(?<![A-Za-z0-9_!?<>*+\-])\(\s*({IDENTIFIER})(?=[\s)])")


def _match_closing_paren(lexed: str, open_index: int) -> Optional[int]:
    depth = 0
    for index in range(open_index, len(lexed)):
        char = lexed[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    return None


def _split_arguments(argument_text: str) -> List[str]:
    """Split a call's argument list at nesting depth zero."""
    return _top_level_tokens(argument_text)


def find_call_sites(lexed: str) -> List[CallSite]:
    """Every call site in both SKILL call syntaxes, with parsed arguments."""
    sites: List[CallSite] = []
    seen: Set[Tuple[int, str]] = set()

    def add(name: str, name_start: int, open_index: int, argument_text: str) -> None:
        if name.startswith("?"):
            return
        key = (name_start, name.casefold())
        if key in seen:
            return
        seen.add(key)
        keywords = tuple(
            m.group(1) for m in re.finditer(rf"\?({IDENTIFIER})", argument_text)
        )
        line = lexed.count("\n", 0, name_start) + 1
        column = name_start - (lexed.rfind("\n", 0, name_start) + 1) + 1
        sites.append(
            CallSite(name, line, column, _split_arguments(argument_text), keywords)
        )

    for match in CONVENTIONAL_CALL.finditer(lexed):
        open_index = match.end() - 1
        close_index = _match_closing_paren(lexed, open_index)
        if close_index is None:
            continue
        add(match.group(1), match.start(1), open_index, lexed[open_index + 1 : close_index])

    for match in PREFIX_CALL.finditer(lexed):
        # the parenthesis belongs to the prefix form; find its own closer
        open_index = lexed.rfind("(", 0, match.start(1))
        if open_index < 0:
            continue
        close_index = _match_closing_paren(lexed, open_index)
        if close_index is None:
            continue
        # arguments are everything after the called name
        argument_text = lexed[match.end(1) : close_index]
        add(match.group(1), match.start(1), open_index, argument_text)

    sites.sort(key=lambda site: (site.line, site.column))
    return sites


# ---------------------------------------------------------------------------
# findings
# ---------------------------------------------------------------------------


class Finding(NamedTuple):
    path: str
    line: int
    column: int
    severity: str
    check: str
    message: str


# Allegro PCB namespace: the corpus indexes 792 documented axl symbols, so an
# unknown axl name is strong evidence of hallucination rather than a corpus gap.
AXL_PREFIX = re.compile(r"^axl", re.IGNORECASE)

# SKILL syntax forms take body expressions that their documented signature does
# not enumerate (``if`` accepts any number of else-expressions via implicit
# progn; ``foreach``/``when``/``let`` bodies are sequences).  Positional arity
# from the declaration is not a sound bound for these, so skip the check.
SYNTAX_FORMS = frozenset(
    {
        "if", "when", "unless", "cond", "case", "caseq",
        "foreach", "for", "while", "dotimes", "loop",
        "let", "letseq", "letrec", "letStar", "prog", "prog1", "prog2",
        "begin", "lambda", "procedure", "catch", "errset", "errsetstring",
        "unwindProtect", "go", "label", "return", "declare",
        "setq", "set",
    }
)
SYNTAX_FORMS_LOWER = frozenset(name.casefold() for name in SYNTAX_FORMS)


def _camel_tokens(name: str) -> Set[str]:
    parts = re.split(r"[_\-\s]+", name)
    tokens: Set[str] = set()
    for part in parts:
        for token in re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+", part):
            if len(token) > 1:
                tokens.add(token.casefold())
    return tokens


def _strip_axl(name: str) -> str:
    return re.sub(r"^axl", "", name, flags=re.IGNORECASE).casefold()


def _common_prefix(left: str, right: str) -> str:
    index = 0
    while index < len(left) and index < len(right) and left[index] == right[index]:
        index += 1
    return left[:index]


def suggest_candidates(name: str, specs: Dict[str, ApiSpec], limit: int = 3) -> List[ApiSpec]:
    """Rank real corpus symbols that the author probably meant.

    Ranking blends camelCase token overlap (catches ``axlGetNetByName`` →
    ``axlDbidName``/``axlDBFindByName``), stem similarity and prefix overlap,
    all computed with the ``axl`` namespace prefix removed from both sides so
    the comparison is like for like.
    """
    target_tokens = _camel_tokens(name)
    stem = _strip_axl(name)
    scored: List[Tuple[float, ApiSpec]] = []
    for candidate in specs.values():
        if AXL_PREFIX.match(name) and not AXL_PREFIX.match(candidate.name):
            continue
        candidate_stem = _strip_axl(candidate.name)
        candidate_tokens = _camel_tokens(candidate.name)
        overlap = len(target_tokens & candidate_tokens)
        union = len(target_tokens | candidate_tokens) or 1
        token_score = overlap / union
        ratio = difflib.SequenceMatcher(None, stem, candidate_stem).ratio()
        shared_prefix = len(_common_prefix(stem, candidate_stem))
        prefix_bonus = min(shared_prefix / max(len(stem), 1), 1.0) * 0.2
        score = 0.5 * token_score + 0.35 * ratio + prefix_bonus
        if score > 0.28:
            scored.append((score, candidate))
    scored.sort(key=lambda pair: (-pair[0], pair[1].name))
    return [candidate for _, candidate in scored[:limit]]


def validate_file(
    path: Path,
    root: Path,
    specs: Dict[str, ApiSpec],
    display: str,
    verified_callables: Optional[Set[str]] = None,
) -> List[Finding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return validate_text(text, specs, display, verified_callables)


def validate_text(
    text: str,
    specs: Dict[str, ApiSpec],
    display: str,
    verified_callables: Optional[Set[str]] = None,
) -> List[Finding]:
    """Validate SKILL source held in memory (LSP buffers) or read from disk."""
    findings: List[Finding] = []
    verified_callables = verified_callables or set()
    lexed = strip_comments_and_strings(text)
    locals_ = collect_local_names(lexed)

    for site in find_call_sites(lexed):
        key = site.name.casefold()
        if key in locals_:
            continue
        spec = specs.get(key)
        if spec is None:
            # Only the Allegro PCB namespace is judged.  General SKILL has far
            # more builtins than the language reference indexes, and other
            # prefixes (dbc*/tsel*/ash*/hi*/ge*) are outside corpus scope.
            if not AXL_PREFIX.match(site.name):
                continue
            if key in verified_callables:
                # A platform probe proved the symbol exists, but there is no
                # corpus signature to make an offline arity claim.
                continue
            suggestions = suggest_candidates(site.name, specs)
            detail = ""
            if suggestions:
                detail = "  did you mean: " + "; ".join(
                    f"{s.name} ({s.source}:{s.line})" for s in suggestions
                )
            findings.append(
                Finding(
                    path=display,
                    line=site.line,
                    column=site.column,
                    severity="error",
                    check="unknown-api",
                    message=(
                        f"unknown API '{site.name}' - not among the "
                        f"{len(specs)} symbols indexed from the corpus; if this "
                        f"is a real Allegro extension confirm with isCallable "
                        f"on the target platform.{detail}"
                    ),
                )
            )
            continue

        # arity: only when every overload is unambiguous and the callee is not
        # a syntax form whose body expressions the declaration does not count
        if spec.countable and site.name.casefold() not in SYNTAX_FORMS_LOWER:
            positional = [a for a in site.arguments if not a.startswith("?")]
            count = len(positional)
            if not spec.accepts(count):
                findings.append(
                    Finding(
                        path=display,
                        line=site.line,
                        column=site.column,
                        severity="warning",
                        check="arity",
                        message=(
                            f"{spec.name} called with {count} argument(s); "
                            f"signature allows {spec.arity_summary()}: "
                            f"`{spec.signature}` ({spec.source}:{spec.line})"
                        ),
                    )
                )

        # keyword arguments
        if site.keywords and spec.keywords:
            allowed = {k.casefold() for k in spec.keywords}
            for keyword in site.keywords:
                if keyword.casefold() not in allowed:
                    findings.append(
                        Finding(
                            path=display,
                            line=site.line,
                            column=site.column,
                            severity="warning",
                            check="unknown-keyword",
                            message=(
                                f"{spec.name} has no documented ?{keyword} "
                                f"argument; signature allows "
                                f"{', '.join('?' + k for k in spec.keywords)}: "
                                f"`{spec.signature}` ({spec.source}:{spec.line})"
                            ),
                        )
                    )
    return findings


def validate_paths(paths: Sequence[Path], root: Path) -> List[Finding]:
    specs = load_corpus(root)
    verified_callables = load_verified_callables(root)
    findings: List[Finding] = []
    for path in paths:
        try:
            display = path.relative_to(root.parent.parent).as_posix()
        except ValueError:
            display = path.as_posix()
        findings.extend(validate_file(path, root, specs, display, verified_callables))
    return findings


# ---------------------------------------------------------------------------
# self-test: false-positive rate over the bundled official Cadence examples
# ---------------------------------------------------------------------------


BASELINE_PATH = Path(__file__).resolve().with_name("validate_skill_api_baseline.json")


def _measure(root: Path) -> Dict[str, Any]:
    """Measure validator output over the bundled official Cadence examples.

    These files are correct, vendor-shipped code: anything reported against
    them is either a corpus coverage gap or a validator defect, so the numbers
    form a false-positive baseline that must not regress.
    """
    examples = sorted(root.glob(EXAMPLES_GLOB))
    if not examples:
        raise FileNotFoundError(f"no examples found under {root / 'examples'}")
    specs = load_corpus(root)
    verified_callables = load_verified_callables(root)
    files_with_errors = 0
    files_with_findings = 0
    total_errors = 0
    total_warnings = 0
    per_check: Dict[str, int] = {}
    for path in examples:
        findings = validate_file(path, root, specs, path.name, verified_callables)
        errors = [f for f in findings if f.severity == "error"]
        if errors:
            files_with_errors += 1
        if findings:
            files_with_findings += 1
        total_errors += len(errors)
        total_warnings += sum(1 for f in findings if f.severity == "warning")
        for finding in findings:
            per_check[finding.check] = per_check.get(finding.check, 0) + 1
    return {
        "example_files": len(examples),
        "files_with_errors": files_with_errors,
        "files_with_findings": files_with_findings,
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "by_check": dict(sorted(per_check.items())),
    }


def self_test(root: Path, write_baseline: bool = False, check: bool = False) -> int:
    """Report, record, or gate on the false-positive baseline."""
    measured = _measure(root)
    count = measured["example_files"]
    print(f"official example files:      {count}")
    print(f"files with >=1 error:        {measured['files_with_errors']}")
    print(f"files with any finding:      {measured['files_with_findings']}")
    print(f"file error rate:             {measured['files_with_errors'] / count:.4f}")
    print(f"total errors:                {measured['total_errors']}")
    print(f"total warnings:              {measured['total_warnings']}")
    for name, value in sorted(measured["by_check"].items(), key=lambda kv: -kv[1]):
        print(f"  {name:18s} {value}")

    if write_baseline:
        BASELINE_PATH.write_text(
            json.dumps(measured, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"baseline written to {BASELINE_PATH.name}")
        return 0

    if check:
        if not BASELINE_PATH.is_file():
            print(
                f"error: no baseline at {BASELINE_PATH.name}; "
                "run --write-baseline first",
                file=sys.stderr,
            )
            return 1
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        regressions: List[str] = []
        for key in ("files_with_errors", "total_errors", "total_warnings"):
            before = baseline.get(key, 0)
            if measured[key] > before:
                regressions.append(f"{key} rose {before} -> {measured[key]}")
        baseline_checks = baseline.get("by_check", {})
        for name, value in measured["by_check"].items():
            before = baseline_checks.get(name, 0)
            if value > before:
                regressions.append(f"{name} findings rose {before} -> {value}")
        for regression in regressions:
            print(f"error: {regression}", file=sys.stderr)
        if regressions:
            return 1
        print("baseline held: no false-positive regression")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help=".il / .ils files to validate")
    parser.add_argument("--root", type=Path, default=_default_root())
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="measure findings over the bundled official Cadence examples",
    )
    parser.add_argument(
        "--write-baseline",
        action="store_true",
        help="record the current self-test numbers as the false-positive baseline",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the self-test numbers regress past the recorded baseline",
    )
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()

    if arguments.self_test or arguments.write_baseline or arguments.check:
        return self_test(
            root,
            write_baseline=arguments.write_baseline,
            check=arguments.check,
        )
    if not arguments.files:
        parser.error("pass at least one .il/.ils file, or use --self-test")

    findings = validate_paths([f.resolve() for f in arguments.files], root)
    for finding in findings:
        print(
            f"{finding.path}:{finding.line}:{finding.column}: "
            f"{finding.severity.upper()} [{finding.check}] {finding.message}"
        )
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
