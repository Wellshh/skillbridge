import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "convert_html_references.py"


def load_converter():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("convert_html_references", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entry_of(conv, html_text, name):
    blocks = conv.parse_chapter(html_text)
    entries = conv.collect_entries(blocks)
    matches = [entry for entry in entries if entry.name == name]
    assert matches, f"entry {name} not parsed from {html_text!r}"
    return matches[0]


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_dd_separators_restore_signature_whitespace(self):
        entry = entry_of(
            self.conv,
            '<h3><a name="1">axlFoo</a></h3>'
            '<dl><font face="\'Courier New\'"><a name="2">axlFoo(<dd>o_dbid<dd>g_layer<dd>) =&gt; t&#47;nil</a></font></dl>'
            "<h4>Description</h4><p>Does foo.</p>",
            "axlFoo",
        )

        self.assertEqual(entry.declarations, ["axlFoo( o_dbid g_layer ) => t/nil"])

    def test_entity_reference_does_not_split_a_token(self):
        # &#47; arrives as its own data event; concatenation must not add spaces
        entry = entry_of(
            self.conv,
            '<h3><a name="1">axlFoo</a></h3>'
            "<dl>axlFoo(<dd>t_a<dd>) =&gt; l_result&#47;nil</dl>"
            "<h4>Description</h4><p>Does foo.</p>",
            "axlFoo",
        )

        self.assertEqual(entry.declarations, ["axlFoo( t_a ) => l_result/nil"])

    def test_or_separated_overloads_are_both_kept(self):
        entry = entry_of(
            self.conv,
            '<h3><a name="1">axlBar</a></h3>'
            "<dl>axlBar(<dd>t_x<dd>) =&gt; t&#47;nil</dl>"
            "<p>or</p>"
            "<dl>axlBar(<dd>o_dbid<dd>) =&gt; t&#47;nil</dl>"
            "<h4>Description</h4><p>Two forms.</p>",
            "axlBar",
        )

        self.assertEqual(
            entry.declarations,
            ["axlBar( t_x ) => t/nil", "axlBar( o_dbid ) => t/nil"],
        )

    def test_prose_paragraph_ends_the_declaration_zone(self):
        entry = entry_of(
            self.conv,
            '<h3><a name="1">axlQux</a></h3>'
            "<dl>axlQux(<dd>l_list<dd>) =&gt; r_path&#47;nil</dl>"
            "<p>Description</p>"
            "<p>A convenience function.</p>",
            "axlQux",
        )

        self.assertEqual(entry.declarations, ["axlQux( l_list ) => r_path/nil"])
        self.assertIn("Description", entry.sections)
        self.assertEqual(entry.sections["Description"][0].payload, "A convenience function.")

    def test_bullet_caption_between_overloads_stays_out_of_signature(self):
        entry = entry_of(
            self.conv,
            '<h3><a name="1">axlBaz</a></h3>'
            "<div><table><tr><td></td><td>Command caption</td></tr></table></div>"
            "<dl>axlBaz(<dd>x_id<dd>t_text<dd>) =&gt; t&#47;nil</dl>"
            "<div><table><tr><td></td><td>Other caption</td></tr></table></div>"
            "<dl>axlBaz(<dd>x_id<dd>) =&gt; t&#47;nil</dl>"
            "<h4>Description</h4><p>Does baz.</p>",
            "axlBaz",
        )

        self.assertEqual(
            entry.declarations,
            [
                "Command caption",
                "axlBaz( x_id t_text ) => t/nil",
                "Other caption",
                "axlBaz( x_id ) => t/nil",
            ],
        )

    def test_example_blockquote_does_not_pollute_declarations(self):
        entry = entry_of(
            self.conv,
            '<h3><a name="1">axlFoo</a></h3>'
            "<dl>axlFoo(<dd>t_a<dd>) =&gt; t&#47;nil</dl>"
            '<h4><a name="9">Examples</a></h4><blockquote>axlFoo("x")</blockquote>',
            "axlFoo",
        )

        self.assertEqual(entry.declarations, ["axlFoo( t_a ) => t/nil"])
        self.assertEqual(entry.sections["Examples"][0].kind, "example")

    def test_dl_fragments_after_prose_caption_accumulate(self):
        # movedown pattern: a prose <p> caption, then the declaration split
        # across <dl>s whose arrow sits in the last fragment
        entry = entry_of(
            self.conv,
            '<h3><a name="1">movedown</a></h3>'
            "<p>movedown - move an element one item farther from the head of a list</p>"
            "<dl>movedown(</dl><dl>g_elem</dl><dl>l_list</dl><dl>) --&gt; l_newlist</dl>"
            "<h4>Description</h4><p>Moves.</p>",
            "movedown",
        )

        self.assertEqual(
            entry.declarations, ["movedown(", "g_elem", "l_list", ") => l_newlist"]
        )
        self.assertEqual(
            self.conv._select_declaration("movedown", entry.declarations),
            "movedown( g_elem l_list ) => l_newlist",
        )

    def test_reassembles_captioned_fragment_groups(self):
        # axlDiffPair pattern: bullet captions interleave with declaration
        # fragments split across <dl>s per call form
        declarations = [
            "Add DiffPair",
            "axlDiffPair( t_diffpair o_net1/t_net1 o_net2/t_net2",
            ")",
            "=> o_diffpair/nil",
            "Modify DiffPair",
            "axlDiffPair( o_diffpair/t_diffpair",
            ")",
            "=> t/nil",
        ]

        self.assertEqual(
            self.conv._reassemble_declarations("axlDiffPair", declarations),
            [
                ("note", "Add DiffPair"),
                (
                    "signature",
                    "axlDiffPair( t_diffpair o_net1/t_net1 o_net2/t_net2 ) => o_diffpair/nil",
                ),
                ("note", "Modify DiffPair"),
                ("signature", "axlDiffPair( o_diffpair/t_diffpair ) => t/nil"),
            ],
        )

    def test_reassembly_keeps_prose_only_sections_as_notes(self):
        items = self.conv._reassemble_declarations(
            "axlIgnoreFixed", ["See axlDBIgnoreFixed."]
        )

        self.assertEqual(items, [("note", "See axlDBIgnoreFixed.")])


class DeclarationHelpersTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_normalize_arrow_variants(self):
        self.assertEqual(
            self.conv._normalize_declaration("axlA( t_x ) ==> t/nil"),
            "axlA( t_x ) => t/nil",
        )

    def test_normalize_repeat_marker(self):
        self.assertEqual(
            self.conv._normalize_declaration("axlA( [[s_n g_v] .... ] ) => t"),
            "axlA( [[s_n g_v] ... ] ) => t",
        )

    def test_normalize_stray_backtick_and_brace(self):
        # printed defect: a stray backtick and a "}" closing the bracket
        self.assertEqual(
            self.conv._normalize_declaration("axlA( [`line} ) => t"),
            "axlA( [line] ) => t",
        )

    def test_repair_adds_missing_parentheses(self):
        self.assertEqual(
            self.conv._repair_declaration("axlA t_x ) => t/nil"),
            "axlA( t_x ) => t/nil",
        )
        self.assertEqual(
            self.conv._repair_declaration("axlA( t_x [g_y] => t/nil"),
            "axlA( t_x [g_y] ) => t/nil",
        )

    def test_matching_declarations_picks_overloads_only(self):
        declarations = [
            "axlA( t_x ) => t/nil",
            "axlA( o_id ) => t/nil",
            "axlB( t_y ) => t/nil",
        ]

        self.assertEqual(
            self.conv._matching_declarations("axlA", declarations),
            declarations[:2],
        )


class SiblingRedistributionTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_family_declarations_move_to_bare_sibling_headings(self):
        blocks = self.conv.parse_chapter(
            '<h3><a name="1">axlFamA</a></h3>'
            '<h3><a name="2">axlFamB</a></h3>'
            '<h3><a name="3">axlFamC</a></h3>'
            "<dl>axlFamA(<dd>t_a<dd>) =&gt; t&#47;nil</dl>"
            "<dl>axlFamB(<dd>t_b<dd>) =&gt; t&#47;nil</dl>"
            "<dl>axlFamC(<dd>t_c<dd>) =&gt; t&#47;nil</dl>"
            "<h4>Description</h4><p>Family.</p>"
        )
        entries = self.conv.collect_entries(blocks)
        moved, donor_of = self.conv._redistribute_sibling_declarations(entries)
        by_name = {entry.name: entry for entry in entries}

        self.assertEqual(by_name["axlFamA"].declarations, ["axlFamA( t_a ) => t/nil"])
        self.assertEqual(by_name["axlFamB"].declarations, ["axlFamB( t_b ) => t/nil"])
        self.assertEqual(by_name["axlFamC"].declarations, ["axlFamC( t_c ) => t/nil"])
        self.assertEqual(sorted(moved["3"]), ["axlFamA( t_a ) => t/nil", "axlFamB( t_b ) => t/nil"])
        self.assertEqual(donor_of, {"1": "3", "2": "3"})

    def test_full_entries_keep_their_declarations(self):
        blocks = self.conv.parse_chapter(
            '<h3><a name="1">axlFull</a></h3>'
            "<dl>axlFull(<dd>t_a<dd>) =&gt; t&#47;nil</dl>"
            "<h4>Description</h4><p>Full.</p>"
            '<h3><a name="2">axlNext</a></h3>'
            "<dl>axlNext(<dd>t_b<dd>) =&gt; t&#47;nil</dl>"
        )
        entries = self.conv.collect_entries(blocks)
        moved, _ = self.conv._redistribute_sibling_declarations(entries)

        self.assertEqual(moved, {})
        self.assertEqual(entries[0].declarations, ["axlFull( t_a ) => t/nil"])


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_overloads_render_with_captions_and_or(self):
        entry = self.conv.Entry("axlBaz", "1", [], {})
        rendered = self.conv.render_entry(
            entry,
            [
                ("note", "First caption"),
                ("signature", "axlBaz( x_id t_text ) => t/nil"),
                ("note", "Second caption"),
                ("signature", "axlBaz( x_id ) => t/nil"),
                ("signature", "axlBaz( ll_items ) => t/nil"),
            ],
        )

        self.assertIn("First caption\n\n`axlBaz( x_id t_text ) => t/nil`", rendered)
        self.assertIn("Second caption\n\n`axlBaz( x_id ) => t/nil`", rendered)
        # two bare signatures in a row are separated by "or"
        self.assertIn("`axlBaz( x_id ) => t/nil`\n\nor\n\n`axlBaz( ll_items ) => t/nil`", rendered)

    def test_missing_table_atoms_unions_selected_signatures(self):
        entry = self.conv.Entry(
            "axlX", "1", ["axlX( g_option ) => t"], {}
        )

        missing = self.conv._missing_table_atoms(
            entry, ["g_option", "o_dbid"], selected=["axlX( g_option o_dbid ) => t"]
        )

        self.assertEqual(missing, [])


class SplitTests(unittest.TestCase):
    def setUp(self):
        self.conv = load_converter()

    def test_small_chapter_stays_single_file(self):
        outputs = self.conv.split_parts("01tiny", ["### axlA\n\n`axlA( ) => t`\n\n"])

        self.assertEqual([name for name, _ in outputs], ["01tiny.md"])

    def test_large_chapter_splits_on_entry_boundaries(self):
        entry = "### axlA\n\n`axlA( ) => t`\n\n" + ("x" * 2000 + "\n\n")
        count = self.conv.PART_TOKEN_TARGET // (len(entry) // 4) + 2
        outputs = self.conv.split_parts("09big", [entry] * max(count, 2))

        self.assertGreater(len(outputs), 1)
        for name, content in outputs:
            self.assertRegex(name, r"09big\.part\d+\.md$")
            self.assertIn("part:", content)
            # no entry is cut in the middle: every chunk starts at a boundary
            body = content.split("-->", 1)[1]
            self.assertTrue(body.lstrip().startswith("### "))


if __name__ == "__main__":
    unittest.main()
