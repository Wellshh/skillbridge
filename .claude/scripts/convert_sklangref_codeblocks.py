#!/usr/bin/env python3
"""Convert code-block signatures to backtick lines in sklangref.

Fifteen sklangref functions still carry their formal declaration inside a
fenced code block.  ``check_signatures._collect_signatures`` skips code
blocks, so those declarations never reach R1-R3 validation and the index
builder falls back to a separate code-block parser.  Convert them to the
corpus convention (inline backtick lines) and repair the glue the original
HTML conversion introduced:

* multi-overload lines glued at the return type (``g_resultsetq(``)
* ``)body)`` / ``])=>`` / ``])`` closing-delimiter glue
* ``][`` bracket glue and PDF layout double-spacing
* ``|`` return separators (corpus convention is ``/``)
"""
from __future__ import annotations

from pathlib import Path

SKLANGREF = Path(__file__).resolve().parents[1] / "skill-references" / "sklangref"

# (file, heading line number, replacement backtick lines)
CONVERSIONS = [
    (
        "dataoperator.md",
        "### setq",
        [
            "setq( s_variableName g_newValueExp ) => g_result",
            "setq( s_variableName = g_newValue ) => g_result",
        ],
    ),
    (
        "datastruct.md",
        "### setarray",
        [
            "setarray( a_array x_index g_value ) => g_value",
            "setarray( o_table g_key g_value ) => g_value",
        ],
    ),
    (
        "funcprog.part01.md",
        "### begin",
        ["begin( g_exp1 [ g_exp2 ... g_expN ] ) => g_result"],
    ),
    (
        "funcprog.part01.md",
        "### define",
        [
            "define( s_var g_expression ) => s_var",
            "define( ( s_var [ s_formalVar1 ... ] ) g_body ... ) => s_var",
        ],
    ),
    (
        "funcprog.part01.md",
        "### defUserInitProc",
        [
            "defUserInitProc( t_contextName s_procName [ autoInit ] ) "
            "=> ( t_contextName s_procName )"
        ],
    ),
    (
        "funcprog.part01.md",
        "### let",
        ["let( l_bindings g_expr1 ... ) => g_result"],
    ),
    (
        "funcprog.part01.md",
        "### letrec",
        [
            "letrec( ( ( s_var1 s_initExp1 ) ( s_var2 s_initExp2 ) ... ) body ) "
            "=> g_result"
        ],
    ),
    (
        "funcprog.part01.md",
        "### letseq",
        [
            "letseq( ( ( s_var1 initExp1 ) ( s_var2 initExp2 ) ... ) body ) "
            "=> g_result"
        ],
    ),
    (
        "inputoutput.part01.md",
        "### fscanf, scanf, sscanf",
        [
            "fscanf( p_inputPort t_formatString [ s_var1 ... ] ) => x_items / nil",
            "scanf( t_formatString [ s_var1 ... ] ) => x_items / nil",
            "sscanf( t_sourceString t_formatString [ s_var1 ... ] ) => x_items / nil",
        ],
    ),
    (
        "inputoutput.part01.md",
        "### loadPort",
        [
            "loadPort( p_port [?langMode g_langMode] [?password g_password] "
            "[?ignoreErrors g_ignoreErrors] ) => t"
        ],
    ),
    (
        "stringfunc.part01.md",
        "### pcreGenCompileOptBits",
        [
            "pcreGenCompileOptBits( [ ?caseLess g_setCaseLessp ] "
            "[ ?multiLine g_setMultiLinep ] [ ?dotAll g_setDotAllp ] "
            "[ ?extended g_setExtendedp ] [ ?anchored g_setAnchoredp ] "
            "[ ?dollar_endonly g_setDollarEndonlyp ] [ ?ungreedy g_setUngreedyp ] "
            "[ ?no_auto_capture g_setNoAutoCapturep ] [ ?firstline g_setFirstlinep ] ) "
            "=> x_resultOptBits"
        ],
    ),
    (
        "stringfunc.part01.md",
        "### pcreGenExecOptBits",
        [
            "pcreGenExecOptBits( [ ?anchored g_setAnchoredp ] [ ?notbol g_setNotbolp ] "
            "[ ?noteol g_setNoteolp ] [ ?notempty g_setNotemptyp ] "
            "[ ?partial g_setPartialp ] ) => x_resultOptBits"
        ],
    ),
    (
        "stringfunc.part01.md",
        "### pcreMatchAssocList",
        [
            "pcreMatchAssocList( g_pattern l_subjects [ x_compOptBits ] "
            "[ x_execOptBits ] ) => l_results / nil / error message(s)"
        ],
    ),
    (
        "stringfunc.part01.md",
        "### pcreMatchList",
        [
            "pcreMatchList( g_pattern l_subjects [ x_compOptBits ] "
            "[ x_execOptBits ] ) => l_results / nil / error message(s)"
        ],
    ),
    (
        "stringfunc.part01.md",
        "### pcreReplace",
        [
            "pcreReplace( o_comPatObj t_source t_replacement x_index [ x_options ] ) "
            "=> t_result / t_source"
        ],
    ),
]


def convert_file(path: Path, conversions: list[tuple[str, list[str]]]) -> int:
    """Replace code-block signatures under each heading with backtick lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    replaced = 0
    for heading, signatures in conversions:
        # locate the heading
        heading_index = None
        for i, line in enumerate(lines):
            if line.strip() == heading:
                heading_index = i
                break
        if heading_index is None:
            raise RuntimeError(f"{path.name}: heading not found: {heading}")

        # find the fenced code block that follows (before any #### heading)
        open_index = None
        close_index = None
        already_converted = False
        for i in range(heading_index + 1, min(heading_index + 10, len(lines))):
            stripped = lines[i].strip()
            if stripped.startswith("####"):
                break
            # idempotency: the expected backtick lines are already in place
            if stripped == f"`{signatures[0]}`":
                already_converted = True
                break
            if stripped == "```" and open_index is None:
                open_index = i
            elif stripped == "```" and open_index is not None:
                close_index = i
                break
        if already_converted:
            continue
        if open_index is None or close_index is None:
            raise RuntimeError(
                f"{path.name}: no code block under {heading}"
            )

        # verify the code block really holds a declaration for this API
        block_text = " ".join(
            lines[j].strip() for j in range(open_index + 1, close_index)
        )
        api_name = heading[4:].split(",")[0].strip()
        if "=>" not in block_text or api_name not in block_text:
            raise RuntimeError(
                f"{path.name}: code block under {heading} is not a declaration: "
                f"{block_text[:80]!r}"
            )

        # replace ```...``` with backtick signature lines
        new_lines = [f"`{sig}`" for sig in signatures]
        lines[open_index : close_index + 1] = new_lines
        replaced += 1
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return replaced


def main() -> None:
    by_file: dict[str, list[tuple[str, list[str]]]] = {}
    for fname, heading, signatures in CONVERSIONS:
        by_file.setdefault(fname, []).append((heading, signatures))
    total = 0
    for fname, conversions in by_file.items():
        count = convert_file(SKLANGREF / fname, conversions)
        print(f"  {fname}: {count} code blocks converted")
        total += count
    print(f"Total: {total} code-block signatures converted to backtick lines")


if __name__ == "__main__":
    main()
