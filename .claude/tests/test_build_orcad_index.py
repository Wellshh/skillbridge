import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"


def load_module(filename, module_name):
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entry(name, cls="DboLib:", signature=None, returns="DboState",
          file="database_commands/DboLib_.md"):
    return {
        "name": name,
        "signature": signature or f"{name}()",
        "class": cls,
        "returns": returns,
        "file": file,
        "type": "database",
    }


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_module("build_orcad_index.py", "build_orcad_index")

    def test_rows_carry_class_and_declaration(self):
        parts = self.builder.render([entry("AbortTransactions")])
        self.assertIn(
            "| `AbortTransactions` | `DboLib` | `AbortTransactions() => DboState` |",
            parts[0],
        )

    def test_missing_class_and_returns_render_cleanly(self):
        parts = self.builder.render([entry("Next", cls=None, returns=None)])
        self.assertIn("| `Next` | `-` | `Next()` |", parts[0])

    def test_exact_duplicates_collapse(self):
        parts = self.builder.render([entry("Next"), entry("Next")])
        self.assertEqual(parts[0].count("| `Next` |"), 1)

    def test_same_name_different_class_is_kept(self):
        parts = self.builder.render([entry("Next"), entry("Next", cls="CisLib:")])
        self.assertEqual(parts[0].count("| `Next` |"), 2)

    def test_sorted_case_insensitive(self):
        parts = self.builder.render([entry("zebra"), entry("Apple"), entry("mango")])
        body = parts[0]
        self.assertLess(body.index("`Apple`"), body.index("`mango`"))
        self.assertLess(body.index("`mango`"), body.index("`zebra`"))

    def test_pagination_respects_the_budget(self):
        entries = [entry(f"Method{i:05d}") for i in range(2000)]
        parts = self.builder.render(entries)
        self.assertGreater(len(parts), 1)
        for part in parts:
            self.assertLessEqual(len(part), self.builder.PART_CHAR_BUDGET * 1.1)
        total_rows = sum(part.count("\n| `") for part in parts)
        self.assertEqual(total_rows, 2000)

    def test_part_headers_are_numbered(self):
        entries = [entry(f"Method{i:05d}") for i in range(2000)]
        parts = self.builder.render(entries)
        self.assertIn(f"(part 1 of {len(parts)})", parts[0])
        self.assertIn(f"(part {len(parts)} of {len(parts)})", parts[-1])


class MainTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_module("build_orcad_index.py", "build_orcad_index_main")
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "orcadcapture"
        (self.root / ".paginate").mkdir(parents=True)
        (self.root / ".paginate" / "api_index_raw.json").write_text(
            json.dumps([entry("AbortTransactions"), entry("Next")]), encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_write_then_check_roundtrip(self):
        self.assertEqual(self.builder.main(["--root", str(self.root)]), 0)
        self.assertEqual(self.builder.main(["--root", str(self.root), "--check"]), 0)
        self.assertEqual(len(list(self.root.glob("api_index.part*.md"))), 1)

    def test_check_fails_on_drift(self):
        self.builder.main(["--root", str(self.root)])
        part = self.root / "api_index.part01.md"
        part.write_text(part.read_text() + "junk\n", encoding="utf-8")
        self.assertEqual(self.builder.main(["--root", str(self.root), "--check"]), 1)

    def test_check_fails_when_parts_missing(self):
        self.assertEqual(self.builder.main(["--root", str(self.root), "--check"]), 1)

    def test_regeneration_removes_stale_parts(self):
        self.builder.main(["--root", str(self.root)])
        # shrink the raw index and regenerate: extra parts must disappear
        (self.root / ".paginate" / "api_index_raw.json").write_text(
            json.dumps([entry("AbortTransactions")]), encoding="utf-8"
        )
        self.builder.main(["--root", str(self.root)])
        self.assertEqual(self.builder.main(["--root", str(self.root), "--check"]), 0)


if __name__ == "__main__":
    unittest.main()
