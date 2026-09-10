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


def fact(fact_id, status="verified"):
    return {
        "id": fact_id,
        "api": "axlShell",
        "constraint": "some constraint",
        "evidence": [{"path": "algroskill/doc.md", "line": 1}],
        "status": status,
    }


class GrowthGateTests(unittest.TestCase):
    def setUp(self):
        self.validate_facts = load_module("validate_facts.py", "validate_facts")
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.root = base / "skill-references"
        (self.root / "algroskill").mkdir(parents=True)
        (self.root / "algroskill" / "doc.md").write_text("line one\nline two\n")
        self.facts_path = self.root / "verified_facts.json"
        # redirect the baseline file into the temp dir
        self.baseline_path = base / "verified_facts_baseline.json"
        self.validate_facts.BASELINE_PATH = self.baseline_path

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_facts(self, facts):
        self.facts_path.write_text(
            json.dumps({"schema_version": 1, "facts": facts}), encoding="utf-8"
        )

    def run_main(self, *extra):
        return self.validate_facts.main(
            ["--root", str(self.root), *extra, str(self.facts_path)]
        )

    def test_baseline_roundtrip_holds(self):
        self.write_facts([fact("a"), fact("b", "documented")])
        self.assertEqual(self.run_main("--write-baseline"), 0)
        self.assertEqual(self.run_main("--check"), 0)

    def test_growth_passes(self):
        self.write_facts([fact("a")])
        self.run_main("--write-baseline")
        self.write_facts([fact("a"), fact("b"), fact("c", "documented")])
        self.assertEqual(self.run_main("--check"), 0)

    def test_shrinking_total_fails(self):
        self.write_facts([fact("a"), fact("b")])
        self.run_main("--write-baseline")
        self.write_facts([fact("a")])
        self.assertEqual(self.run_main("--check"), 1)

    def test_shrinking_verified_count_fails_even_when_total_holds(self):
        self.write_facts([fact("a"), fact("b", "documented")])
        self.run_main("--write-baseline")
        # same total, but the verified fact was demoted to documented
        self.write_facts([fact("a", "documented"), fact("b", "documented")])
        self.assertEqual(self.run_main("--check"), 1)

    def test_superseded_keeps_the_entry_and_passes(self):
        self.write_facts([fact("a"), fact("b")])
        self.run_main("--write-baseline")
        # retiring via superseded keeps the entry, so the counts hold
        self.write_facts([fact("a", "superseded"), fact("b")])
        self.assertEqual(self.run_main("--check"), 1)  # verified still shrank
        self.write_facts([fact("a", "superseded"), fact("b"), fact("c", "documented")])
        self.assertEqual(self.run_main("--check"), 1)  # verified still below baseline
        self.write_facts([fact("a", "superseded"), fact("b"), fact("c")])
        self.assertEqual(self.run_main("--check"), 0)  # verified restored by growth

    def test_no_baseline_file_skips_the_gate(self):
        self.write_facts([fact("a")])
        self.assertEqual(self.run_main("--check"), 0)

    def test_schema_errors_still_fail_before_the_gate(self):
        self.facts_path.write_text("{not json", encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)


if __name__ == "__main__":
    unittest.main()
