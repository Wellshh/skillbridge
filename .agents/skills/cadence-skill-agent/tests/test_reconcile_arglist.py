import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reconcile_arglist.py"
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("reconcile_arglist", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_decode_simple_optional_record():
    value = [[["t_string"], ["g_general"], ["@optional"], ["g_general"], "tgg"]]
    assert MODULE.decode_ranges(value) == ([(2, 3)], "simple")


def test_decode_skips_keyword_and_rest_records():
    assert MODULE.decode_ranges([[['@key'], ['color']]]) == ([], "keyword-or-rest")
    assert MODULE.decode_ranges([[['@rest'], ['g_general']]]) == ([], "keyword-or-rest")


def test_decode_skips_special_records_and_handles_explicit_range():
    assert MODULE.decode_ranges([[['___']]]) == ([], "unsupported-record")
    assert MODULE.decode_ranges([[['sym'], 0, 1, 'S']]) == ([(0, 1)], "simple")


def test_classification_distinguishes_overlap_and_disjoint():
    assert MODULE.classify((0, 1), [(0, 0)]) == "documentation-within-actual"
    assert MODULE.classify((0, 0), [(0, 1)]) == "within-documentation"
    assert MODULE.classify((2, 2), [(2, 2)]) == "exact"
    assert MODULE.classify((1, 1), [(2, 2)]) == "disjoint"


def test_variadic_runtime_api_allowlist_is_narrow_and_evidence_backed():
    assert MODULE.VARIADIC_RUNTIME_APIS == {
        "xdifference",
        "xplus",
        "xquotient",
        "xtimes",
    }


def test_runtime_adjudication_allowlist_covers_only_reviewed_discrepancies():
    assert MODULE.RUNTIME_ADJUDICATED_APIS == {
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
    }


def test_list_functions_runtime_adjudication_preserves_raw_comparison():
    matrix = {
        "verified_on": {"allegro": "17.2-2016 S048"},
        "rows": [["listFunctions", True, [[['@optional'], ['str'], 't']]]],
    }
    report = MODULE.reconcile(
        matrix,
        Path(".agents/skills/cadence-skill-agent/skill-references"),
    )
    entry = report["comparisons"][0]
    assert entry["status"] == "runtime-adjudicated"
    assert entry["raw_status"] == "overlap-only"


def test_documentation_review_allowlist_preserves_public_contract():
    assert MODULE.DOCUMENTATION_REVIEWED_APIS == {
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
    }


def test_reconcile_labels_non_countable_runtime_encodings():
    matrix = {
        "verified_on": {"allegro": "17.2-2016 S048"},
        "rows": [
            [
                "axlAddSimpleMoveDynamics",
                True,
                [[['origin'], ['path'], ['type'], ['@key'], ['ref_point'], ['color']]],
            ],
            [
                "axlDllCall",
                True,
                [[['g_general'], ['@optional'], ['g_general'], 'g']],
            ],
        ],
    }
    report = MODULE.reconcile(
        matrix,
        Path(".agents/skills/cadence-skill-agent/skill-references"),
    )
    assert [entry["status"] for entry in report["comparisons"]] == [
        "special-encoding",
        "non-countable-documentation",
    ]


def test_documentation_contract_verified_allowlist_is_evidence_backed_batch():
    assert MODULE.DOCUMENTATION_CONTRACT_VERIFIED_APIS == {
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
    }


def test_documentation_cns_contract_verified_allowlist_is_getter_batch():
    assert MODULE.DOCUMENTATION_CNS_CONTRACT_VERIFIED_APIS == {
        "axlcnsassemblymodeget",
        "axlcnsdesignmodeget",
        "axlcnsecsetmodeget",
        "axlcnsphysicalmodeget",
        "axlcnssamenetmodeget",
        "axlcnsspacingmodeget",
        "axlpadusermasklayers",
        "axlxsectionget",
    }


def test_runtime_context_dependent_allowlist_is_explicit():
    assert MODULE.RUNTIME_CONTEXT_DEPENDENT_APIS == {
        "gcsummary",
        "listvariables",
        "loadcontext",
        "savecontext",
    }


def test_runtime_boundary_allowlist_is_explicit():
    assert MODULE.RUNTIME_BOUNDARY_APIS == {
        "axldbcreatemoduleinstance",
        "axlpadstacksettype",
        "skilldebugger",
    }


def test_runtime_boundary_classification_preserves_raw_ranges():
    matrix = {
        "verified_on": {"allegro": "17.2-2016 S048"},
        "rows": [
            [
                "axlDBCreateModuleInstance",
                True,
                [
                    [
                        ['name'],
                        ['moddef'],
                        ['origin'],
                        ['rotation'],
                        ['logic'],
                        ['@optional'],
                        ['net'],
                        ['extra'],
                        'ttttttt',
                    ]
                ],
            ],
            [
                "axlPadstackSetType",
                True,
                [[['padstack'], ['type'], ['@optional'], ['compat'], 'ttt']],
            ],
            [
                "skillDebugger",
                True,
                [
                    [
                        ['@optional'],
                        ['compat1'],
                        ['compat2'],
                        ['compat3'],
                        ['compat4'],
                        ['compat5'],
                        'ttttt',
                    ]
                ],
            ],
        ],
    }
    report = MODULE.reconcile(
        matrix,
        Path(".agents/skills/cadence-skill-agent/skill-references"),
    )
    assert [entry["status"] for entry in report["comparisons"]] == [
        "runtime-boundary",
        "runtime-boundary",
        "runtime-boundary",
    ]
    assert [entry["raw_status"] for entry in report["comparisons"]] == [
        "documentation-within-actual",
        "documentation-within-actual",
        "documentation-within-actual",
    ]
