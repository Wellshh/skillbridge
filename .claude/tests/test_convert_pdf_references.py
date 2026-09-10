import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "convert_pdf_references.py"


def load_converter():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("convert_pdf_references", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NormalizeSignatureTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_choice_syntax_braces_and_pipes_normalized(self):
        self.assertEqual(
            self.conv._normalize_pdf_signature("func( { s_a | t_b | t } ) => g"),
            "func( ( s_a / t_b / t ) ) => g",
        )

    def test_glued_keyword_prefix_stripped(self):
        self.assertEqual(
            self.conv._normalize_pdf_signature("init( [ u_?key1 value1 ] ) => t"),
            "init( [ ?key1 value1 ] ) => t",
        )

    def test_whitespace_collapsed(self):
        self.assertEqual(
            self.conv._normalize_pdf_signature("func(  t_a   t_b  ) => t"),
            "func( t_a t_b ) => t",
        )


class RepairSignatureTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_missing_closing_paren_added(self):
        self.assertEqual(
            self.conv._repair_pdf_signature("func( t_a => t"),
            "func( t_a ) => t",
        )

    def test_missing_closing_bracket_and_paren_added(self):
        self.assertEqual(
            self.conv._repair_pdf_signature("func( [t_a => t"),
            "func( [t_a ] ) => t",
        )

    def test_already_balanced_unchanged(self):
        self.assertEqual(
            self.conv._repair_pdf_signature("func( t_a ) => t"),
            "func( t_a ) => t",
        )


class StopLineTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_exact_section_header_stops(self):
        self.assertTrue(self.conv._is_signature_stop_line("Description"))
        self.assertTrue(self.conv._is_signature_stop_line("Arguments:"))

    def test_where_clause_stops(self):
        self.assertTrue(
            self.conv._is_signature_stop_line("where break_condition can be either")
        )

    def test_parameter_line_does_not_stop(self):
        self.assertFalse(self.conv._is_signature_stop_line("[ S_name ]"))
        self.assertFalse(self.conv._is_signature_stop_line("=> t / nil"))


class ExtractDeclarationsTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_where_clause_skipped_return_preserved(self):
        page = (
            "breakptMethod\n"
            "breakptMethod(\n"
            "     [ S_name ]\n"
            "     [break_condition])\n"
            "     where break_condition can be either\n"
            "     (break_tag\n"
            "     g_condition\n"
            "     )\n"
            "     => t / nil\n"
        )
        decls = self.conv.extract_api_declarations(page)
        self.assertEqual(len(decls), 1)
        self.assertEqual(decls[0].names, ("breakptMethod",))
        self.assertIn("=>", decls[0].signature)
        self.assertNotIn("where", decls[0].signature)
        self.assertNotIn("break_tag", decls[0].signature)

    def test_choice_syntax_in_signature(self):
        page = (
            "needNCells\n"
            "needNCells(\n"
            "     {s_cellType | S_userType}\n"
            "     x_cellCount\n"
            "     )\n"
            "     => t | nil\n"
        )
        decls = self.conv.extract_api_declarations(page)
        self.assertEqual(len(decls), 1)
        # braces normalized to parens, pipes to slashes
        self.assertNotIn("{", decls[0].signature)
        self.assertNotIn("|", decls[0].signature)

    def test_missing_closing_paren_repaired(self):
        page = (
            "skTabulate\n"
            "skTabulate(\n"
            "     ?fileNames g_names\n"
            "     [?reportFile t_reportFile]\n"
            "     => t\n"
        )
        decls = self.conv.extract_api_declarations(page)
        self.assertEqual(len(decls), 1)
        # _repair_pdf_signature adds the missing closing paren
        self.assertEqual(decls[0].signature.count("("), decls[0].signature.count(")"))


if __name__ == "__main__":
    unittest.main()
