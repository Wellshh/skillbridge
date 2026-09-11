#!/usr/bin/env python3
"""Reconcile real Allegro ``arglist`` probes with the reference index.

The probe stores one SKILL ``arglist`` value as JSON.  A normal value is a
list containing one record; the record contains one list per formal argument,
optional markers, and usually a trailing compact type string.  Keyword and
rest-argument forms are reported but deliberately excluded from simple
positional arity adjudication.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from validate_skill_api import ApiSpec, load_corpus

Range = Tuple[int, int]

# Verified on Allegro 17.2-2016 S048: these integer arithmetic built-ins use
# one compact type slot in arglist even though the public callable form is
# variadic with two or more operands. Keep this list evidence-backed and
# narrow; a one-slot record is not generally proof of variadic behavior.
VARIADIC_RUNTIME_APIS = frozenset({
    "xdifference",
    "xplus",
    "xquotient",
    "xtimes",
})

# The ten remaining disjoint rows were individually checked against the S048
# matrix, the cited source entry/examples, and (for axl* names) the generated
# stub override policy. Keep the raw documented comparison in each report
# entry, but mark the discrepancy as adjudicated instead of leaving it as an
# unresolved arity conflict.
RUNTIME_ADJUDICATED_APIS = frozenset({
    "axlcnspurgecsets",
    "axlcnspurgeobjects",
    "axldbchangedesignunits",
    "axldllcalllist",
    "axlgetdiestackmemberset",
    "axlpolyexpand",
    "axlpolyoperation",
    "axlpurgepadstacks",
    "axluiwmove",
    "listfunctions",
    "putc",
})

# These rows are source-reviewed cases where the S048 observed range is a
# strict subset of the documented public range. Preserve the documentation
# contract and expose the narrower observation separately for traceability.
DOCUMENTATION_REVIEWED_APIS = frozenset({
    "axlclearobjectcustomcolor",
    "axlcustomcolorobject",
    "axlcvfcolorchooserdlg",
    "axldbcreateexternaldrc",
    "axldeletebondwire",
    "axlformcreate",
    "axlgeopointinshape",
    "axlgetlinelock",
    "axlhighlightobject",
    "axlsetvariable",
    "axlxsectionset",
    "declare",
    "mapcon",
    "tracelevlimit",
})

# Documented public forms for these API contracts were exercised successfully
# in fresh S048 sessions. Their wider arglist records remain visible as raw
# comparisons; no public contract is widened. The small number of stateful
# entries use disposable resources and explicit cleanup.
DOCUMENTATION_CONTRACT_VERIFIED_APIS = frozenset({
    "axlextentdb",
    "axlfindfilterisopen",
    "axlflushdisplay",
    "axlgetfindfilter",
    "axlgetselset",
    "axlgetselsetcount",
    "axloktoproceed",
    "axlversion",
    "axlclipboardgettext",
    "filelength",
    "isfileencrypted",
    "parsestring",
    "readstring",
    "linereadstring",
    "expandmacro",
    "expandmacrodeep",
    "maketable",
    "filetell",
    "read",
    "lineread",
    "axladdselectall",
    "axlclearselset",
    "getmethodspecializers",
    "gets",
    "defvar",
    "createdir",
    "deletedir",
    "unprofile",
    "axlautoopenfindfilter",
    "axlopenfindfilter",
    "axlclosefindfilter",
    "axlsubselectall",
    "axlcolorpriorityset",
    "axldesignflip",
    "axlzoomfit",
    "axlzoomworld",
    "axladdselectname",
    "axladdselectobject",
    "axlsingleselectobject",
    "axlsubselectname",
    "axlsubselectobject",
    "axlaltsymbollist",
    "axlaltsymbolok",
    "axlcnsecsetvalueget",
    "axlexportxmldbrecords",
    "axldbtunesectorsize",
    "axlextractmap",
    "axlcolorset",
    "axlpadsuppressset",
    "axlmsgcontextinbuf",
    "axlmsgcontextremove",
    "axlpackagedesigncheckdrcerror",
    "axlpackagedesignchecklogerror",
    "axlsetalias",
    "axlsetfunckey",
    "axlcnsdesignmodeset",
    "axlcnsdesignvalueset",
    "axlcnsphysicalmodeset",
    "axlcnsspacingmodeset",
    "axlcnsassemblymodeset",
    "axlcnssamenetmodeset",
    "axlcnsecsetmodeset",
    "axlcnsecsetvalueset",
    "ipcsetpriority",
    "axldrawobject",
    "axleraseobject",
    "encrypt",
    "axldbcreatepropdictentry",
    "axlpadstackedit",
    "axldbassignnet",
    "axldbchangetext",
    "axluiwhelpregister",
    "axldbcreatecloseshape",
    "axldbsetlock",
    "axluimenuinsert",
    "axldiffpair",
    "axlformcolorize",
    "debugquit",
    "axldbcreatepin",
})

DOCUMENTATION_CNS_CONTRACT_VERIFIED_APIS = frozenset({
    "axlcnsassemblymodeget",
    "axlcnsdesignmodeget",
    "axlcnsecsetmodeget",
    "axlcnsphysicalmodeget",
    "axlcnssamenetmodeget",
    "axlcnsspacingmodeget",
    "axlpadusermasklayers",
    "axlxsectionget",
})

RUNTIME_CONTEXT_DEPENDENT_APIS = frozenset({
    "gcsummary",
    "listvariables",
    "loadcontext",
    "savecontext",
})

# These documented forms were exercised in real S048 processes but their
# observable behavior is a runtime boundary rather than a stable success
# contract: module reuse returned nil, padstack type mutation was a no-op (and
# an alternate edit path hung), and skillDebugger entered an interactive top
# level. Keep the raw arity comparison while preventing false stub expansion.
RUNTIME_BOUNDARY_APIS = frozenset({
    "axldbcreatemoduleinstance",
    "axlpadstacksettype",
    "skilldebugger",
})


def _record_range(record: Any) -> Optional[Range]:
    """Decode a simple positional ``arglist`` record into min/max arity."""
    if not isinstance(record, list) or record == [None]:
        return None
    if record in ([], [""]):
        return (0, 0)
    if not isinstance(record[-1], str):
        return None

    # Some SKILL built-ins encode a min/max interval explicitly after a
    # symbolic marker rather than listing formal slots (for example
    # ``help`` and ``edit``).
    if (
        len(record) >= 4
        and record[0] in (["args"], ["sym"])
        and isinstance(record[1], int)
        and isinstance(record[2], int)
        and record[1] <= record[2]
    ):
        return (record[1], record[2])

    markers = {
        item[0] for item in record if isinstance(item, list) and item and isinstance(item[0], str)
    }
    if "@key" in markers or "@rest" in markers:
        return None

    # The trailing compact string is metadata, not a formal parameter.
    slots = record[:-1]
    required = 0
    optional = 0
    optional_mode = False
    for item in slots:
        if isinstance(item, list) and item and item[0] == "@optional":
            optional_mode = True
            continue
        if optional_mode:
            optional += 1
        else:
            required += 1
    return (required, required + optional)


def decode_ranges(arglist: Any) -> Tuple[List[Range], str]:
    """Return simple ranges and a status for one probe value."""
    if not isinstance(arglist, list) or len(arglist) != 1:
        return [], "unsupported-shape"
    record = arglist[0]
    if not isinstance(record, list):
        return [], "unsupported-record"
    result = _record_range(record)
    if result is None:
        if record == [None]:
            return [], "unsupported-record"
        markers = {
            item[0]
            for item in record
            if isinstance(item, list) and item and isinstance(item[0], str)
        }
        return [], "keyword-or-rest" if markers & {"@key", "@rest"} else "unsupported-record"
    return [result], "simple"


def _doc_ranges(spec: Optional[ApiSpec]) -> List[Range]:
    if spec is None:
        return []
    return [
        (arity.required, arity.required + arity.optional)
        for arity in spec.arities
        if arity.countable
    ]


def classify(actual: Range, documented: Sequence[Range]) -> str:
    if actual in documented:
        return "exact"
    if any(actual[0] >= low and actual[1] <= high for low, high in documented):
        return "within-documentation"
    if any(low >= actual[0] and high <= actual[1] for low, high in documented):
        return "documentation-within-actual"
    if any(actual[0] <= high and actual[1] >= low for low, high in documented):
        return "overlap-only"
    return "disjoint"


def _reconcile_row(
    name: str,
    callable_: bool,
    arglist: Any,
    specs: Dict[str, ApiSpec],
) -> Dict[str, Any]:
    entry: Dict[str, Any] = {"name": name, "callable": callable_}
    if not callable_:
        entry["status"] = "not-callable"
        return entry

    actual, decode_status = decode_ranges(arglist)
    entry["decode_status"] = decode_status
    if not actual:
        entry["status"] = {
            "keyword-or-rest": "special-encoding",
            "unsupported-record": "unsupported-encoding",
        }.get(decode_status, "non-countable-documentation")
        return entry

    spec = specs.get(str(name).casefold())
    documented = _doc_ranges(spec)
    entry["actual_ranges"] = [list(value) for value in actual]
    entry["documented_ranges"] = [list(value) for value in documented]
    if spec is not None:
        entry["signature"] = spec.signature
    if not documented:
        entry["status"] = "non-countable-documentation"
        return entry

    normalized_name = str(name).casefold()
    adjudications = {
        "runtime-adjudicated": (
            RUNTIME_ADJUDICATED_APIS,
            (
                "S048 arglist/source-example review resolved the discrepancy; "
                "retain the raw documentation comparison for traceability."
            ),
        ),
        "documentation-reviewed": (
            DOCUMENTATION_REVIEWED_APIS,
            (
                "Source entry reviewed against S048 arglist; the observed range "
                "is a strict subset of the documented public range, so retain "
                "the documentation contract without a stub override."
            ),
        ),
        "documentation-contract-verified": (
            DOCUMENTATION_CONTRACT_VERIFIED_APIS | DOCUMENTATION_CNS_CONTRACT_VERIFIED_APIS,
            (
                "The documented public form returned successfully in a fresh S048 "
                "session; retain the public contract and leave the wider runtime "
                "arglist comparison visible."
            ),
        ),
        "runtime-context-dependent": (
            RUNTIME_CONTEXT_DEPENDENT_APIS,
            (
                "isCallable/arglist are present, but documented-type candidate calls "
                "failed in the current S048 context; do not widen the public "
                "contract or generated stub without a suitable context."
            ),
        ),
        "runtime-boundary": (
            RUNTIME_BOUNDARY_APIS,
            (
                "The documented form was exercised in a real S048 process, but the "
                "observed result is a runtime boundary rather than a stable success "
                "contract; retain the public documentation and do not widen the "
                "generated stub."
            ),
        ),
    }
    if normalized_name in VARIADIC_RUNTIME_APIS:
        entry["status"] = "runtime-variadic"
        return entry
    for status, (names, adjudication) in adjudications.items():
        if normalized_name in names:
            entry["raw_status"] = classify(actual[0], documented)
            entry["status"] = status
            entry["adjudication"] = adjudication
            return entry
    entry["status"] = classify(actual[0], documented)
    return entry


def reconcile(matrix: Dict[str, Any], references: Path) -> Dict[str, Any]:
    specs = load_corpus(references)
    comparisons = [
        _reconcile_row(name, callable_, arglist, specs)
        for name, callable_, arglist in matrix.get("rows", [])
    ]

    counts: Dict[str, int] = {}
    for entry in comparisons:
        status = str(entry["status"])
        counts[status] = counts.get(status, 0) + 1
    return {
        "artifact": "arglist-reconciliation",
        "schema_version": 1,
        "verified_on": matrix.get("verified_on"),
        "source_matrix": ".artifacts/iscalable-matrix-17.2-S048-full.json",
        "method": {
            "arglist": "trailing compact type string excluded; @optional marks following slots optional",
            "excluded": "@key, @rest, malformed records, and non-countable documentation arities",
            "classification": (
                "exact, within-documentation, documentation-within-actual, "
                "runtime-variadic, runtime-adjudicated, runtime-boundary, "
                "overlap-only, disjoint"
            ),
        },
        "counts": counts,
        "comparisons": comparisons,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix", type=Path)
    parser.add_argument("--references", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    references = args.references or Path(__file__).resolve().parents[1] / "skill-references"
    report = reconcile(json.loads(args.matrix.read_text(encoding="utf-8")), references)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
