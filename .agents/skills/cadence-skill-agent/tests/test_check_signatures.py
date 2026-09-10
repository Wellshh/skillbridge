import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "check_signatures.py"


def load_checker():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("check_signatures", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_entry(root, directory, filename, heading, signature, body="#### Description\n\nText.\n"):
    directory_dir = root / directory
    directory_dir.mkdir(exist_ok=True)
    (directory_dir / filename).write_text(
        f"### {heading}\n\n`{signature}`\n\n{body}\n", encoding="utf-8"
    )


class SignatureCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.checker = load_checker()

    def tearDown(self):
        self.temp_dir.cleanup()

    def findings(self, directory="algroskill"):
        findings = self.checker.check_body(self.root)
        return [f for f in findings if f.path.startswith(directory + "/")]

    def errors(self, directory="algroskill"):
        return [f for f in self.findings(directory) if f.severity == "error"]

    def test_well_spaced_signature_passes(self):
        write_entry(
            self.root,
            "algroskill",
            "07dbaccs.md",
            "axlAltSymbolOK",
            "axlAltSymbolOK( t_name/o_dbid g_layer t_symbol ) => t/nil",
        )

        self.assertEqual(self.errors(), [])

    def test_glued_signature_is_an_error(self):
        write_entry(
            self.root,
            "algroskill",
            "07dbaccs.md",
            "axlAltSymbolOK",
            "axlAltSymbolOK(t_name/o_dbidg_layert_symbol) => t/nil",
        )

        errors = self.errors()
        self.assertTrue(any("glued parameter token" in error.reason for error in errors))

    def test_glued_inner_prefix_like_n_yn_x_is_an_error(self):
        write_entry(
            self.root,
            "algroskill",
            "trigono.md",
            "atan2",
            "atan2(n_yn_x) => f_result",
        )

        self.assertTrue(any("glued parameter token" in error.reason for error in self.errors()))

    def test_glued_optional_marker_is_an_error(self):
        write_entry(
            self.root,
            "algroskill",
            "sipapd.md",
            "axlDBCreatePin",
            "axlDBCreatePin( t_pinName?use ) => o_pin/nil",
        )

        self.assertTrue(
            any("optional-argument marker" in error.reason for error in self.errors())
        )

    def test_structural_and_literal_atoms_pass(self):
        write_entry(
            self.root,
            "algroskill",
            "23utils.md",
            "axlExample",
            'axlExample( l_args... t_mode \'max "ETCH" nil ) => t/nil',
        )

        self.assertEqual(self.errors(), [])

    def test_name_mismatch_is_an_error_in_axl_domain(self):
        write_entry(
            self.root,
            "algroskill",
            "07dbaccs.md",
            "axlAltSymbolReplace",
            "axlAltSymbolOK( t_name/o_dbid t_symbol ) => t/nil",
        )

        self.assertTrue(
            any("does not match signature callee" in error.reason for error in self.errors())
        )

    def test_name_mismatch_is_a_warning_outside_axl(self):
        write_entry(
            self.root,
            "sklangref",
            "core.md",
            "append1",
            "append( l_list1 l_list2 ) => l_result",
        )

        findings = self.findings("sklangref")
        self.assertTrue(
            any(f.severity == "warning" and "does not match" in f.reason for f in findings)
        )
        self.assertEqual(self.errors("sklangref"), [])

    def test_argument_table_disagreement_is_detected(self):
        write_entry(
            self.root,
            "algroskill",
            "07dbaccs.md",
            "axlAltSymbolList",
            "axlAltSymbolList( t_name/o_dbid g_layer ) => lt_symbols/nil",
            body=(
                "#### Arguments\n\n"
                "| Name | Description |\n"
                "|---|---|\n"
                "| `t_name` | component definition or a refdes name |\n"
                "| `o_dbid` | a symbol instance |\n"
                "| `g_layer` | `top`, `'bottom`, or `'internal` |\n"
                "| `g_extra` | documented but missing from the signature |\n"
                "| `g_extra2` | also documented but missing |\n"
            ),
        )

        self.assertTrue(
            any("missing from the signature" in error.reason for error in self.errors())
        )

    def test_single_missing_table_parameter_only_warns(self):
        # single-missing in the axl domain is suppressed (converter gate
        # already validated); test with a non-axl domain instead
        write_entry(
            self.root,
            "sklangref",
            "core.md",
            "myFunc",
            "myFunc( t_a g_b ) => t/nil",
            body=(
                "#### Arguments\n\n"
                "| Name | Description |\n"
                "|---|---|\n"
                "| `t_a` | first arg |\n"
                "| `g_b` | second arg |\n"
                "| `g_extra` | documented but missing from the signature |\n"
            ),
        )

        findings = self.findings("sklangref")
        self.assertEqual(self.errors("sklangref"), [])
        self.assertTrue(
            any(
                f.severity == "warning" and "missing from the signature" in f.reason
                for f in findings
            )
        )

    def test_overload_signatures_cover_table_parameters(self):
        directory = self.root / "algroskill"
        directory.mkdir(exist_ok=True)
        (directory / "26logacc.md").write_text(
            "### axlRenameNet\n\n"
            "`axlRenameNet( t_old_name t_new_name ) => t/nil`\n\n"
            "or\n\n"
            "`axlRenameNet( o_dbid t_new_name ) => t/nil`\n\n"
            "#### Arguments\n\n"
            "| Name | Description |\n"
            "|---|---|\n"
            "| `t_old_name` | existing net name |\n"
            "| `o_dbid` | object on the net |\n"
            "| `t_new_name` | new net name |\n",
            encoding="utf-8",
        )

        self.assertEqual(self.errors(), [])

    def test_description_before_arguments_table_is_found(self):
        write_entry(
            self.root,
            "algroskill",
            "07dbaccs.md",
            "axlAltSymbolOK",
            "axlAltSymbolOK( t_name/o_dbid g_layer t_symbol ) => t/nil",
            body=(
                "#### Description\n\nText.\n\n"
                "#### Arguments\n\n"
                "| Name | Description |\n"
                "|---|---|\n"
                "| `t_name` | component definition or a refdes name |\n"
                "| `o_dbid` | a symbol instance |\n"
                "| `g_layer` | layer |\n"
                "| `t_symbol` | the symbol |\n"
            ),
        )

        self.assertEqual(self.errors(), [])

    def test_index_row_drift_from_body_is_detected(self):
        body = self.root / "algroskill"
        body.mkdir(exist_ok=True)
        (body / "25dbmisc.md").write_text(
            "### axlBackDrill\n\n"
            "`axlBackDrill( o_dbid s_layer ) => l_result/nil`\n\n"
            "#### Description\n\nText.\n",
            encoding="utf-8",
        )
        (self.root / "api_index.part01.md").write_text(
            "<!-- Generated by scripts/build_reference_indexes.py; do not edit manually. -->\n"
            "\n"
            "# axl* API Index (part 1 of 3)\n"
            "\n"
            "| Symbol | Documented declaration | Source | Line |\n"
            "|---|---|---|---:|\n"
            "| `axlBackDrill` | `axlBackDrill( o_dbid s_layer ) => l_wrong/nil` "
            "| `algroskill/25dbmisc.md` | 1 |\n",
            encoding="utf-8",
        )

        errors = [f for f in self.checker.check_indexes(self.root) if f.severity == "error"]

        self.assertTrue(
            any("differs from body" in error.reason for error in errors)
        )

    def test_check_reports_error_exit(self):
        write_entry(
            self.root,
            "algroskill",
            "07dbaccs.md",
            "axlAltSymbolOK",
            "axlAltSymbolOK(t_name/o_dbidg_layert_symbol) => t/nil",
        )

        ok, errors, warnings = self.checker.check(self.root)

        self.assertFalse(ok)
        self.assertTrue(errors)
        self.assertEqual([w for w in warnings if "algroskill" in w], [])

    def test_choice_syntax_braces_and_pipes_pass(self):
        write_entry(
            self.root,
            "sklangref",
            "core.md",
            "needNCells",
            "needNCells( {s_cellType | S_userType} x_cellCount ) => t | nil",
        )

        self.assertEqual(self.errors("sklangref"), [])

    def test_glued_closing_opening_parens_split(self):
        write_entry(
            self.root,
            "sklangref",
            "controlflow.md",
            "do",
            "do( ( ( s_var1 g_init1 )( s_var2 g_init2 ) ) g_body ) => g_value",
        )

        self.assertEqual(self.errors("sklangref"), [])

    def test_two_dot_repeat_marker_normalized(self):
        write_entry(
            self.root,
            "sklangref",
            "dataoperator.md",
            "rotatef",
            "rotatef( [gplace1 ][ gplace2 ].....[ gplacen ] ) => g_new",
        )

        self.assertEqual(self.errors("sklangref"), [])

    def test_list_form_matches_singular_in_table(self):
        write_entry(
            self.root,
            "algroskill",
            "06intedt.md",
            "axlDelete",
            "axlDelete( lo_dbid ) => t/nil",
            body=(
                "#### Arguments\n\n"
                "| Name | Description |\n"
                "|---|---|\n"
                "| `o_dbid` | the dbid to delete |\n"
            ),
        )

        findings = self.findings()
        # list-form lo_dbid should match table's o_dbid — no "missing" warning
        self.assertEqual(
            [f for f in findings if "missing" in f.reason], []
        )

    def test_infix_assignment_operator_is_structural(self):
        # setq's second syntax form carries the SKILL infix ``=`` operator
        # inside the parameter list; it must not be flagged as malformed
        write_entry(
            self.root,
            "sklangref",
            "dataoperator.md",
            "setq",
            "setq( s_variableName = g_newValue ) => g_result",
        )

        self.assertEqual(self.errors("sklangref"), [])
        findings = self.findings("sklangref")
        self.assertEqual(
            [f for f in findings if "malformed" in f.reason], []
        )


class DelistTests(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker()

    def test_delist_strips_list_prefix(self):
        self.assertEqual(self.checker._delist("lo_dbid"), "o_dbid")
        self.assertEqual(self.checker._delist("lt_symbols"), "t_symbols")
        self.assertEqual(self.checker._delist("o_dbid"), "o_dbid")

    def test_delist_leaves_unprefixed_unchanged(self):
        self.assertEqual(self.checker._delist("obj"), "obj")
        self.assertEqual(self.checker._delist("bondWires"), "bondWires")


if __name__ == "__main__":
    unittest.main()
