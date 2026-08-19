import importlib.util
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "convert_pdf_references.py"


def load_converter():
    spec = importlib.util.spec_from_file_location("convert_pdf_references", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PdfReferenceConverterTests(unittest.TestCase):
    def test_extracts_multiline_formal_declaration(self):
        page = (
            "ipcBeginProcess\n"
            "ipcBeginProcess(\n"
            "  t_command\n"
            "  [ t_hostName ]\n"
            ")\n"
            "=> o_childId\n\n"
            "Description\n"
        )

        declarations = load_converter().extract_api_declarations(page)

        self.assertEqual([entry.names for entry in declarations], [("ipcBeginProcess",)])
        self.assertEqual(
            declarations[0].signature,
            "ipcBeginProcess( t_command [ t_hostName ] ) => o_childId",
        )

    def test_does_not_treat_example_call_as_a_declaration(self):
        page = 'Example\nresult = ipcBeginProcess("hostname")\n=> ipc:3\n'

        declarations = load_converter().extract_api_declarations(page)

        self.assertEqual(declarations, [])

    def test_splits_only_between_physical_pages(self):
        converter = load_converter()
        page = "x" * (converter.PART_CHAR_LIMIT // 2 + 100)

        parts = converter.render_document("skipcref", [page, page, page])

        self.assertEqual(len(parts), 3)
        self.assertIn("## PDF page 1", parts[0])
        self.assertIn("## PDF page 2", parts[1])
        self.assertIn("## PDF page 3", parts[2])

    def test_keeps_multi_page_api_entry_in_one_part(self):
        converter = load_converter()
        first_api = "firstApi\nfirstApi(\n)\n=> t\n"
        continuation = "argument details\n" + "x" * converter.PART_CHAR_LIMIT
        second_api = "secondApi\nsecondApi(\n)\n=> t\n"

        parts = converter.render_document(
            "skipcref",
            [first_api, continuation, second_api],
        )

        self.assertEqual(len(parts), 2)
        self.assertIn("### firstApi", parts[0])
        self.assertIn("## PDF page 2", parts[0])
        self.assertNotIn("### secondApi", parts[0])
        self.assertIn("### secondApi", parts[1])


if __name__ == "__main__":
    unittest.main()
