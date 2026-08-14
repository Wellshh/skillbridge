import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "build_reference_indexes.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_reference_indexes", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReferenceIndexBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "sklangref").mkdir()
        (self.root / "sklanguser").mkdir()
        (self.root / "skipcref").mkdir()
        (self.root / "skdevref").mkdir()
        (self.root / "skoopref").mkdir()
        (self.root / "docs").mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_extracts_only_api_headings_with_signatures(self):
        source = self.root / "sklangref" / "core.md"
        source.write_text(
            "# Core Functions\n\n"
            "### arglist\n\n"
            "`arglist( g_function ) => l_argumentList`\n\n"
            "#### Description\n\nText.\n\n"
            "### Narrative heading\n\nNo signature here.\n",
            encoding="utf-8",
        )

        entries = load_builder().extract_api_entries(self.root)

        self.assertEqual([entry.name for entry in entries], ["arglist"])
        self.assertEqual(entries[0].signature, "arglist( g_function ) => l_argumentList")
        self.assertEqual(entries[0].path, "sklangref/core.md")

    def test_extracts_fenced_declaration_without_falling_through_to_example(self):
        source = self.root / "sklangref" / "list.md"
        source.write_text(
            "### append\n\n"
            "```\nappend( l_list1 l_list2 ) => l_result\n```\n\n"
            "#### Description\n\nText.\n\n"
            "#### Example\n\n`append('(1) '(2)) => (1 2)`\n",
            encoding="utf-8",
        )

        entries = load_builder().extract_api_entries(self.root)

        self.assertEqual(entries[0].signature, "append( l_list1 l_list2 ) => l_result")

    def test_normalizes_markdown_markup_in_api_names(self):
        source = self.root / "sklangref" / "dataoperator.md"
        source.write_text(
            "### setf\\_`<helper>`\n\n`setf_<helper>( g_new[ g_cell ]) => g_result`\n",
            encoding="utf-8",
        )

        entries = load_builder().extract_api_entries(self.root)

        self.assertEqual(entries[0].name, "setf_<helper>")

    def test_joins_multiline_inline_signature_and_ignores_ellipsis_alias(self):
        source = self.root / "sklangref" / "inputoutput.md"
        source.write_text(
            "### putc, ...\n\n"
            "`putc( s_character [ p_outputPort ] )`\n"
            "`=> s_symbol`\n\n"
            "#### Description\n",
            encoding="utf-8",
        )

        entries = load_builder().extract_api_entries(self.root)

        self.assertEqual([entry.name for entry in entries], ["putc"])
        self.assertEqual(
            entries[0].signature,
            "putc( s_character [ p_outputPort ] ) => s_symbol",
        )

    def test_builds_api_and_topic_indexes_with_relative_targets(self):
        (self.root / "sklangref" / "core.md").write_text(
            "### arglist\n\n`arglist( g_function ) => l_argumentList`\n",
            encoding="utf-8",
        )
        (self.root / "sklangref" / "stringfunc.part02.md").write_text(
            "### strlen\n\n`strlen( t_string ) => x_length`\n",
            encoding="utf-8",
        )
        (self.root / "sklanguser" / "chap1.md").write_text(
            "1\n=\n\nGetting Started\n===============\n\n### Solving Common Problems\n",
            encoding="utf-8",
        )

        builder = load_builder()
        builder.build(self.root)

        api_index = (self.root / "sklang_api_index.part01.md").read_text(encoding="utf-8")
        symbol_index = (self.root / "sklang_api_index.part03.md").read_text(encoding="utf-8")
        topic_index = (self.root / "sklang_topic_index.md").read_text(encoding="utf-8")
        self.assertIn(
            "| `arglist` | `arglist( g_function ) => l_argumentList` | `sklangref/core.md` |",
            api_index,
        )
        self.assertIn(
            "| `strlen` | `strlen( t_string ) => x_length` | `sklangref/stringfunc.part02.md` |",
            symbol_index,
        )
        self.assertIn("| Getting Started | `sklanguser/chap1.md` |", topic_index)
        self.assertIn("| Solving Common Problems | `sklanguser/chap1.md` |", topic_index)

    def test_indexes_supplemental_skill_api_references(self):
        (self.root / "skipcref" / "skipcref.part01.md").write_text(
            "### ipcBeginProcess\n\n"
            "`ipcBeginProcess( t_command [ t_hostName ] ) => o_childId`\n",
            encoding="utf-8",
        )
        (self.root / "skoopref" / "skoopref.part01.md").write_text(
            "### makeInstance\n\n"
            "`makeInstance( us_class @rest l_initargs ) => g_instance`\n",
            encoding="utf-8",
        )

        builder = load_builder()
        builder.build(self.root)

        ipc_index = (self.root / "sklang_api_index.part02.md").read_text(encoding="utf-8")
        object_index = (self.root / "sklang_api_index.part02.md").read_text(encoding="utf-8")
        self.assertIn("`skipcref/skipcref.part01.md`", ipc_index)
        self.assertIn("`skoopref/skoopref.part01.md`", object_index)

    def test_manifest_is_portable_and_reports_legacy_links(self):
        (self.root / "sklangref" / "core.md").write_text(
            "### arglist\n\n`arglist( g_function ) => l_argumentList`\n\n"
            "[strcmp](stringfunc.html#123)\n",
            encoding="utf-8",
        )

        builder = load_builder()
        builder.build(self.root)

        manifest = json.loads(
            (self.root / ".paginate" / "pagination_manifest.json").read_text(encoding="utf-8")
        )
        serialized = json.dumps(manifest)
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual(
            manifest["indexes"]["api_reference_dirs"],
            ["sklangref", "skipcref", "skdevref", "skoopref"],
        )
        self.assertNotIn(str(self.root), serialized)
        self.assertEqual(manifest["quality"]["legacy_html_links"], 1)
        self.assertEqual(manifest["documents"][0]["path"], "sklangref/core.md")

    def test_check_rejects_a_document_over_the_token_limit(self):
        (self.root / "sklangref" / "huge.md").write_text("x" * 60_004, encoding="utf-8")

        result = load_builder().check(self.root)

        self.assertFalse(result.ok)
        self.assertTrue(any("huge.md" in error for error in result.errors))

    def test_check_rejects_a_stale_generated_index(self):
        (self.root / "sklangref" / "core.md").write_text(
            "### arglist\n\n`arglist( g_function ) => l_argumentList`\n",
            encoding="utf-8",
        )
        builder = load_builder()
        builder.build(self.root)
        (self.root / "sklang_api_index.part01.md").write_text("stale\n", encoding="utf-8")

        result = builder.check(self.root)

        self.assertFalse(result.ok)
        self.assertTrue(any("stale generated index" in error for error in result.errors))

    def test_check_rejects_a_stale_pagination_manifest(self):
        source = self.root / "sklangref" / "core.md"
        source.write_text(
            "### arglist\n\n`arglist( g_function ) => l_argumentList`\n",
            encoding="utf-8",
        )
        builder = load_builder()
        builder.build(self.root)
        source.write_text(source.read_text(encoding="utf-8") + "\nMore prose.\n", encoding="utf-8")

        result = builder.check(self.root)

        self.assertFalse(result.ok)
        self.assertTrue(any("stale pagination manifest" in error for error in result.errors))

    def test_check_reuses_recorded_page_count_when_pdfinfo_is_unavailable(self):
        (self.root / "docs" / "manual.pdf").write_bytes(b"test pdf fixture")
        builder = load_builder()
        with mock.patch.object(builder, "_pdf_pages", return_value=12):
            builder.build(self.root)

        with mock.patch.object(builder, "_pdf_pages", return_value=None):
            result = builder.check(self.root)

        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
