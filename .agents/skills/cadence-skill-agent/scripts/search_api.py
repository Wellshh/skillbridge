#!/usr/bin/env python3
"""Semantic search over the SKILL reference corpus, ranked by description text.

The generated ``api_index.part*.md`` files are keyed on exact symbol names, so
an agent that knows *what it wants to do* but not *what the function is called*
often retrieves nothing and then guesses.  The canonical failure: "get the name
of a net" does not surface ``axlDbidName`` because that symbol contains no
``net`` - but its ``#### Description`` says "Provides the standard Allegro PCB
Editor name of a database object ... (for example, nets)".

This tool indexes description prose (plus symbol-name tokens) with IDF weighting
and ranks matches, so intent-style queries resolve to real documented APIs with
their signature and ``source:line``.  Everything is derived from the corpus at
run time - there is no hand-written phrase table to drift.

Usage::

    python3 .claude/scripts/search_api.py "get the name of a net"
    python3 .claude/scripts/search_api.py "delete object" --limit 5
    python3 .claude/scripts/search_api.py "transaction undo" --domain algroskill
"""

from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, NamedTuple, Optional, Sequence, Set, Tuple

# Domains whose entries carry Markdown ``#### Description`` sections.
MARKDOWN_DOMAINS = ("algroskill", "sklangref")
# Domains rendered as PDF page dumps: prose lives inside the fenced text block.
PDF_DOMAINS = ("skdevref", "skoopref", "skipcref")
ALL_DOMAINS = MARKDOWN_DOMAINS + PDF_DOMAINS

INDEX_GLOBS = ("api_index.part*.md", "sklang_api_index.part*.md")
INDEX_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`(.+?)`\s*\|\s*`(.+?)`\s*\|\s*(\d+)\s*\|$")
TOPIC_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*`(.+?)`\s*\|\s*(\d+)\s*\|$")

# Words that carry no discriminating signal in API documentation.  Intent verbs
# such as "returns" are deliberately absent: they are folded onto concept tokens
# and their ubiquity is handled by IDF weighting instead.  Domain terms
# (allegro, skill, pcb) are likewise kept - they are exactly what separates an
# ``axl*`` Allegro API from a general SKILL builtin, so stopping them out costs
# the one signal that most often identifies the right entry.
STOP_WORDS = frozenset(
    """
    a an the and or of to in for is are be been being this that these those it its
    with without from by as at on off up into over under then than there here when
    where which who whom what how all any each every some no not only own same so
    too very can could will would shall should may might must do does did done
    you your we our they them he she his her i me my whether whose whomever
    function functions value values argument arguments parameter parameters
    specified specifies specify following follow follows
    used uses use using example examples note notes see also reference
    references if else nil t one two three first second third
    currently current usually often simply just may
    """.split()
)

TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_]*")

# Words whose trailing plural must not be stripped ("class" -> "clas").
STEM_EXCEPTIONS = frozenset(
    """
    class bus gas bias alias this axis chassis status plus minus process
    address progress access success less pass mass loss cross
    """.split()
)

# Intent verbs: documentation says "provides the name", an agent asks "get the
# name".  Mapping both sides onto a shared concept token is what makes
# intent-style queries resolve at all - without it the correct entry matches
# only on nouns and loses to entries that happen to repeat the query's verb.
INTENT_CONCEPTS = {
    "GET": (
        "get", "gets", "getting", "retrieve", "retrieves", "fetch", "fetches",
        "read", "reads", "reading", "obtain", "obtains", "provide", "provides",
        "providing", "return", "returns", "returning", "query", "queries",
        "report", "reports", "show", "shows", "display", "displays", "give",
        "gives", "output", "outputs", "extract", "extracts",
    ),
    "CREATE": (
        "create", "creates", "creating", "make", "makes", "making", "add",
        "adds", "adding", "build", "builds", "generate", "generates", "new",
        "insert", "inserts", "define", "defines", "construct", "constructs",
        "place", "places", "draw", "draws",
    ),
    "DELETE": (
        "delete", "deletes", "deleting", "remove", "removes", "removing",
        "ripup", "rip", "rips", "ripping", "destroy", "destroys", "clear",
        "clears", "erase", "erases", "drop", "drops", "purge", "purges",
        "unset",
    ),
    "FIND": (
        "find", "finds", "finding", "search", "searches", "locate", "locates",
        "lookup", "look", "detect", "detects", "identify", "identifies",
        "select", "selects", "match", "matches", "scan", "scans",
    ),
    "SET": (
        "set", "sets", "setting", "assign", "assigns", "put", "puts", "write",
        "writes", "update", "updates", "modify", "modifies", "change",
        "changes", "apply", "applies", "load", "loads", "store", "stores",
        "replace", "replaces", "replaced", "overwrite", "overwrites",
    ),
    "CHECK": (
        "check", "checks", "verify", "verifies", "test", "tests", "validate",
        "validates", "compare", "compares", "predicate", "p", "isp",
    ),
}
TOKEN_TO_CONCEPT = {
    word: concept for concept, words in INTENT_CONCEPTS.items() for word in words
}

# Abbreviations the corpus uses habitually; both forms are indexed.
TOKEN_ALIAS = {"prop": "property", "props": "property"}

# Intent verbs that appear fused inside all-lowercase SKILL builtin names:
# ``lineread`` is line+read, ``putprop`` is put+prop.  camelCase splitting
# cannot see inside these names, so a query for "read a line" never matched
# ``lineread`` at all.  Only all-lowercase, non-``axl`` tokens are split (axl*
# names are camelCase and already split), and the remainder must be at least
# three letters so "thread" does not become th+read.
EMBEDDED_SUFFIX_VERBS = ("read", "write", "find", "print", "sort", "open", "close")
EMBEDDED_PREFIX_VERBS = ("get", "put", "set", "make", "has")


def _embedded_verb_forms(token: str) -> List[str]:
    """Concept + remainder for intent verbs fused into a lowercase name."""
    if len(token) < 7 or not token.isalpha() or token.startswith("axl"):
        return []
    for verb in EMBEDDED_SUFFIX_VERBS:
        if token.endswith(verb) and len(token) - len(verb) >= 3:
            concept = TOKEN_TO_CONCEPT.get(verb)
            remainder = token[: -len(verb)]
            forms = ([concept] if concept else []) + [remainder, _stem(remainder)]
            return [f for f in dict.fromkeys(forms) if f and f not in STOP_WORDS]
    for verb in EMBEDDED_PREFIX_VERBS:
        if token.startswith(verb) and len(token) - len(verb) >= 3:
            concept = TOKEN_TO_CONCEPT.get(verb)
            remainder = token[len(verb) :]
            forms = ([concept] if concept else []) + [remainder, _stem(remainder)]
            return [f for f in dict.fromkeys(forms) if f and f not in STOP_WORDS]
    return []


def _stem(token: str) -> str:
    """Very light plural/possessive normalisation.

    Only the obvious cases are folded - ``nets``/``net``, ``names``/``name``,
    ``pins``/``pin`` - because aggressive stemming destroys the SKILL type
    prefixes and camelCase fragments that carry the real signal.  Both the
    original and the stemmed form are indexed, so exact matches still win.

    ``-es`` is only stripped when what remains ends in a sibilant
    (``boxes``→``box``, ``classes``→``class``); otherwise ``names`` would lose
    its trailing ``e`` and stop matching the singular the query actually uses.
    """
    if token in STEM_EXCEPTIONS or len(token) < 4:
        return token
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith("es") and len(token) > 4:
        candidate = token[:-2]
        if candidate.endswith(("s", "x", "z", "ch", "sh")):
            return candidate
    if token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _predicate_forms(token: str) -> List[str]:
    """Extra index terms for SKILL's trailing-``p`` predicate convention.

    ``listp`` means "is a list", but camelCase splitting cannot see inside an
    all-lowercase name, so a query for "list" never matched ``listp``.  Emitting
    the name without its predicate suffix fixes that whole family (``typep``,
    ``stringp``, ``numberp``, ``pairp``, ``tablep``, ``fixp``, ``zerop``, ...).
    """
    if len(token) >= 4 and token.endswith("p") and token[:-1].isalpha():
        base = token[:-1]
        if len(base) >= 3:
            stemmed = _stem(base)
            return [base] if stemmed == base else [base, stemmed]
    return []


class Entry(NamedTuple):
    """One documented API symbol plus the prose that describes it."""

    name: str
    signature: str
    source: str
    line: int
    description: str
    domain: str


class Match(NamedTuple):
    entry: Entry
    score: float
    matched_terms: Tuple[str, ...]


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1] / "skill-references"


def _tokens(text: str) -> List[str]:
    """Lowercased tokens with camelCase splitting, stemming and intent folding.

    Ordinary words contribute themselves plus their singular stem, so an exact
    wording match still outranks a paraphrase.  Intent verbs are different:
    they fold onto their shared concept token ONLY ("returns", "provides" and
    "gets" all index as just ``GET``).  Emitting the literal verb alongside its
    concept would double-count any document that happens to use the query's own
    wording, letting ``axlNetEcsetValueGet`` beat ``axlDbidName`` on "get the
    name of a net" purely because the verb "get" sits in its name.
    """
    out: List[str] = []
    for raw in TOKEN.findall(text):
        lowered = raw.casefold()
        pieces = [lowered]
        # split camelCase so ``DbidName`` also indexes as ``dbid`` + ``name``
        for part in re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+", raw):
            piece = part.casefold()
            if len(piece) > 2 and piece != lowered:
                pieces.append(piece)
        for piece in pieces:
            if len(piece) < 2 or piece in STOP_WORDS:
                continue
            stemmed = _stem(piece)
            concept = TOKEN_TO_CONCEPT.get(piece) or TOKEN_TO_CONCEPT.get(stemmed)
            if concept:
                out.append(concept)
                continue
            out.append(piece)
            if stemmed != piece and stemmed not in STOP_WORDS:
                out.append(stemmed)
            alias = TOKEN_ALIAS.get(piece) or TOKEN_ALIAS.get(stemmed)
            if alias and alias not in out:
                out.append(alias)
            for form in _predicate_forms(piece):
                if form not in STOP_WORDS and form not in out:
                    out.append(form)
        # fused-verb builtins (``lineread``, ``putprop``) only exist in
        # lowercase; cased tokens were already split by camelCase above
        if raw.islower():
            for form in _embedded_verb_forms(lowered):
                if form not in out:
                    out.append(form)
                alias = TOKEN_ALIAS.get(form)
                if alias and alias not in out:
                    out.append(alias)
    return out


def _load_index(root: Path) -> Dict[str, Entry]:
    """Every indexed symbol, keyed by lowercased name."""
    entries: Dict[str, Entry] = {}
    for pattern in INDEX_GLOBS:
        for path in sorted(root.glob(pattern)):
            for row in path.read_text(encoding="utf-8").splitlines():
                match = INDEX_ROW.match(row)
                if match is None:
                    continue
                name, signature, source, line = match.groups()
                domain = source.split("/")[0]
                entries[name.casefold()] = Entry(
                    name=name,
                    signature=signature,
                    source=source,
                    line=int(line),
                    description="",
                    domain=domain,
                )
    return entries


def _markdown_descriptions(path: Path) -> Dict[int, str]:
    """``#### Description`` prose keyed by the owning ``### heading`` line."""
    lines = path.read_text(encoding="utf-8").splitlines()
    result: Dict[int, str] = {}
    heading_line: Optional[int] = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("### "):
            heading_line = index + 1
        elif line.startswith("#### Description") and heading_line is not None:
            body: List[str] = []
            cursor = index + 1
            while cursor < len(lines):
                candidate = lines[cursor]
                if candidate.startswith("### ") or candidate.startswith("#### "):
                    break
                if candidate.strip():
                    body.append(candidate.strip())
                cursor += 1
            if body:
                result[heading_line] = " ".join(body)
        index += 1
    return result


def _pdf_descriptions(path: Path) -> Dict[int, str]:
    """Prose following each ``### heading``, for PDF page-dump domains."""
    lines = path.read_text(encoding="utf-8").splitlines()
    result: Dict[int, str] = {}
    index = 0
    while index < len(lines):
        if lines[index].startswith("### "):
            heading_line = index + 1
            body: List[str] = []
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].startswith("### "):
                candidate = lines[cursor].strip()
                # skip fences and the page furniture, keep the prose; the
                # backticked signature echo is already indexed as the
                # signature field and would double-count its name tokens here
                if (
                    candidate
                    and not candidate.startswith("```")
                    and not candidate.startswith("## PDF page")
                    and not (candidate.startswith("`") and "=>" in candidate)
                ):
                    body.append(candidate)
                cursor += 1
            if body:
                result[heading_line] = " ".join(body)[:4000]
        index += 1
    return result


def attach_descriptions(root: Path, entries: Dict[str, Entry]) -> None:
    """Fill in each entry's description prose from its body file, in place."""
    cache: Dict[Path, Dict[int, str]] = {}
    for key, entry in entries.items():
        path = root / entry.source
        if not path.is_file():
            continue
        if path not in cache:
            if entry.domain in PDF_DOMAINS:
                cache[path] = _pdf_descriptions(path)
            else:
                cache[path] = _markdown_descriptions(path)
        entry_description = cache[path].get(entry.line, "")
        entries[key] = entry._replace(description=entry_description)


class SearchIndex:
    """Field-weighted BM25 index over symbol names, signatures and prose.

    BM25 rather than cosine: API descriptions vary wildly in length, and
    cosine's raw term-frequency norm buries short, precisely-worded entries
    below long ones that merely repeat a query term.  BM25 saturates term
    frequency (``name`` appearing five times is not five times the evidence)
    and normalises length by a tunable ``b``.

    Field weights are applied to the term frequency, *not* by repeating tokens.
    Repetition would inflate the document length and so be partly cancelled by
    BM25's own length normalisation - an entry whose name matches would gain
    less than intended while paying a length penalty for it.

    A coordination bonus on top rewards entries matching more *distinct* query
    terms, which is what intent queries need: "get the name of a net" should
    prefer an entry covering get+name+net over one that repeats "net" often.

    Two further calibrations:

    - The return type (the text after ``=>``) is indexed as its own
      ``returns`` field.  "format a number as a string" is answered by
      ``sprintf`` precisely because it returns ``t_string`` while ``fprintf``
      returns ``t`` - the return type is often the only place that signal
      lives.
    - Concept tokens (``GET``, ``CREATE``, ...) score at a flat
      ``CONCEPT_WEIGHT`` regardless of field.  They are a paraphrase bridge,
      not literal evidence: at name-field weight every getter/setter/deleter
      name would outscore a document that matches the query's discriminating
      noun, so all of ``getCompatContextVersion``/``getSkillVersion``/... used
      to tie above ``axlVersion`` for "get the version of Allegro".
    - A proximity bonus rewards query terms that co-occur *close together in
      the description prose*.  This is what separates ``axlDbidName`` ("name
      of a database object ... nets ...") from ``axlRenameNet`` on "get the
      name of a net": both match all query terms, but the latter only via its
      ``t_old_name``/``t_new_name`` signature arguments - the words never meet
      in its prose.

    Coordination coverage is weighted by IDF mass, not term count, so matching
    the rare discriminating term counts for more than matching a common one.
    """

    K1 = 1.4
    B = 0.55
    COORD_WEIGHT = 0.45
    PROX_WEIGHT = 0.6
    PROX_WINDOW = 8
    FIELD_WEIGHTS = {"name": 4.0, "signature": 2.0, "returns": 1.0, "description": 1.0}
    CONCEPT_WEIGHT = 1.0

    def __init__(self, entries: Iterable[Entry]):
        self.entries = list(entries)
        self.document_count = len(self.entries)
        # per document, per field, term -> raw count
        self.fields: List[Dict[str, Dict[str, int]]] = []
        self.doc_lengths: List[int] = []
        self.postings: Dict[str, List[int]] = defaultdict(list)
        # description term -> token offsets, for the proximity bonus
        self.prose_positions: List[Dict[str, List[int]]] = []

        for entry in self.entries:
            signature, _, returns = entry.signature.partition("=>")
            field_tokens = {
                "name": _tokens(entry.name),
                "signature": _tokens(signature),
                "returns": _tokens(returns),
                "description": _tokens(entry.description),
            }
            field_counts = {
                field: _counts(tokens) for field, tokens in field_tokens.items()
            }
            self.fields.append(field_counts)
            length = sum(len(tokens) for tokens in field_tokens.values())
            self.doc_lengths.append(max(length, 1))
            positions: Dict[str, List[int]] = defaultdict(list)
            for offset, token in enumerate(field_tokens["description"]):
                positions[token].append(offset)
            self.prose_positions.append(dict(positions))
            # One posting per (term, document).  A term appearing in several
            # fields must not be posted repeatedly or BM25 would score that
            # document once per field it occurs in.
            document_index = len(self.fields) - 1
            terms: Set[str] = set()
            for counts in field_counts.values():
                terms.update(counts)
            for term in terms:
                self.postings[term].append(document_index)

        self.average_length = (
            sum(self.doc_lengths) / self.document_count if self.document_count else 1.0
        )
        self.idf = {
            term: math.log(
                1.0
                + (self.document_count - len(hits) + 0.5) / (len(hits) + 0.5)
            )
            for term, hits in self.postings.items()
        }

    def _frequency(self, index: int, term: str) -> float:
        """Field-weighted term frequency for one document.

        Concept tokens bypass field weights: ``get`` inside a getter's *name*
        must not count four times what ``get`` in prose counts, or every
        getter-named API would outrank the entry that actually matches the
        query's noun.
        """
        counts = self.fields[index]
        if term in INTENT_CONCEPTS:
            return self.CONCEPT_WEIGHT * sum(
                counts.get(field, {}).get(term, 0) for field in self.FIELD_WEIGHTS
            )
        return sum(
            self.FIELD_WEIGHTS[field] * counts.get(field, {}).get(term, 0)
            for field in self.FIELD_WEIGHTS
        )

    def search(self, query: str, limit: int = 8, domain: Optional[str] = None) -> List[Match]:
        query_counts = _counts(_tokens(query))
        if not query_counts:
            return []
        query_terms = [t for t in query_counts if t in self.postings]
        if not query_terms:
            return []
        # discard terms so common they carry no signal for this corpus
        query_terms = [t for t in query_terms if self.idf[t] > 0.05]
        if not query_terms:
            return []

        scores: Dict[int, float] = defaultdict(float)
        matched: Dict[int, List[str]] = defaultdict(list)
        for term in query_terms:
            weight = self.idf[term]
            for index in self.postings[term]:
                frequency = self._frequency(index, term)
                if frequency <= 0:
                    continue
                denominator = frequency + self.K1 * (
                    1.0 - self.B + self.B * self.doc_lengths[index] / self.average_length
                )
                scores[index] += weight * frequency * (self.K1 + 1.0) / denominator
                matched[index].append(term)

        results: List[Match] = []
        total_idf = sum(self.idf[t] for t in query_terms)
        for index, raw_score in scores.items():
            entry = self.entries[index]
            if domain and entry.domain != domain:
                continue
            matched_terms = set(matched[index])
            coverage = sum(self.idf[t] for t in matched_terms) / total_idf
            score = raw_score * (1.0 + self.COORD_WEIGHT * coverage)
            score += self._proximity_bonus(index, matched_terms)
            results.append(
                Match(
                    entry=entry,
                    score=score,
                    matched_terms=tuple(sorted(matched_terms)),
                )
            )
        results.sort(key=lambda match: (-match.score, match.entry.name.casefold()))
        return results[:limit]

    def _proximity_bonus(self, index: int, matched_terms: set) -> float:
        """Reward query terms that co-occur close together in the prose.

        Concept tokens are excluded: they are ubiquitous paraphrase bridges,
        so their distance to anything carries no signal.  Only literal terms
        meeting inside the description (not the signature) indicate that the
        document actually *discusses* the query's concepts together.
        """
        literal = [t for t in matched_terms if t not in INTENT_CONCEPTS]
        positions = self.prose_positions[index]
        present = [t for t in literal if t in positions]
        bonus = 0.0
        for first, second in combinations(present, 2):
            distance = min(
                abs(a - b) for a in positions[first] for b in positions[second]
            )
            if distance <= self.PROX_WINDOW:
                closeness = 1.0 - distance / (self.PROX_WINDOW + 1)
                bonus += (
                    self.PROX_WEIGHT
                    * min(self.idf[first], self.idf[second])
                    * closeness
                )
        return bonus


def _counts(tokens: Sequence[str]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for token in tokens:
        counts[token] += 1
    return dict(counts)


def build_index(root: Path, domains: Optional[Sequence[str]] = None) -> SearchIndex:
    entries = _load_index(root)
    attach_descriptions(root, entries)
    selected = list(entries.values())
    if domains:
        wanted = {d.casefold() for d in domains}
        selected = [e for e in selected if e.domain.casefold() in wanted]
    return SearchIndex(selected)


def _snippet(description: str, terms: Sequence[str], width: int = 160) -> str:
    """A short window of the description around the first matched term."""
    if not description:
        return ""
    lowered = description.casefold()
    position = -1
    for term in terms:
        found = lowered.find(term)
        if found >= 0 and (position < 0 or found < position):
            position = found
    if position < 0:
        return description[:width].strip()
    start = max(0, position - width // 3)
    excerpt = description[start : start + width].strip()
    prefix = "..." if start > 0 else ""
    suffix = "..." if start + width < len(description) else ""
    return f"{prefix}{excerpt}{suffix}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="what you want to do, in plain words")
    parser.add_argument("--root", type=Path, default=_default_root())
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument(
        "--domain",
        choices=sorted(ALL_DOMAINS),
        help="restrict to one reference domain",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="print only name and signature"
    )
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    query = " ".join(arguments.query)

    index = build_index(root, [arguments.domain] if arguments.domain else None)
    matches = index.search(query, limit=arguments.limit)
    if not matches:
        print(f"no corpus match for {query!r}")
        return 1

    for rank, match in enumerate(matches, start=1):
        entry = match.entry
        print(f"{rank}. {entry.name}   (score {match.score:.3f})")
        if not arguments.quiet:
            print(f"   `{entry.signature}`")
            print(f"   {entry.source}:{entry.line}")
            print(f"   matched: {', '.join(match.matched_terms)}")
            snippet = _snippet(entry.description, match.matched_terms)
            if snippet:
                print(f"   {snippet}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
