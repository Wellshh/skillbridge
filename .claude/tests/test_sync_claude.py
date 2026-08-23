import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "sync_claude.py"


def load_sync_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("sync_claude", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentSyncTests(unittest.TestCase):
    def test_renders_codex_agent_toml(self) -> None:
        source = (
            "---\n"
            "name: cadence-skill-agent\n"
            "description: Test description.\n"
            "---\n"
            "Read .agents/skills/cadence-skill-agent/skill-references/api.md.\n"
        )

        rendered = load_sync_module().render_codex_agent(source)

        assert 'name = "cadence-skill-agent"' in rendered
        assert 'description = "Test description."' in rendered
        assert "developer_instructions = '''" in rendered
        assert ".agents/skills/cadence-skill-agent/skill-references/api.md" in rendered

    def test_renders_claude_frontmatter_and_paths(self) -> None:
        source = (
            "---\n"
            "name: cadence-skill-agent\n"
            "description: Test description.\n"
            "---\n"
            "Read .agents/skills/cadence-skill-agent/skill-references/api.md.\n"
            "Run .agents/skills/cadence-skill-agent/scripts/check.py.\n"
        )

        rendered = load_sync_module().render_claude_agent(source)

        assert "tools: Read, Write, Edit, Grep, Glob, Bash" in rendered
        assert "model: inherit" in rendered
        assert "memory: project" in rendered
        assert ".claude/skill-references/api.md" in rendered
        assert ".claude/scripts/check.py" in rendered
        assert ".agents/skills/cadence-skill-agent/" not in rendered

    def test_normalizes_reference_for_claude(self) -> None:
        source = (
            b"Read .agents/skills/cadence-skill-agent/SKILL.md and "
            b".agents/skills/cadence-skill-agent/skill-references/api.md.\r\n"
        )

        assert load_sync_module().adapt_reference(source) == (
            b"Read .claude/agents/cadence-skill-agent.md and "
            b".claude/skill-references/api.md.\n"
        )

    def test_reports_stale_cadence_references_but_keeps_orcad(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            managed = root / "managed.md"
            stale = root / "examples/old.il"
            orcad_index = root / "orcad-capture-tcltk-agent.md"
            orcad_reference = root / "orcadcapture/api.md"
            for path in (managed, stale, orcad_index, orcad_reference):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()

            assert load_sync_module().stale_reference_files(root, {managed}) == [
                stale
            ]

    def test_repository_is_synchronized(self) -> None:
        assert load_sync_module().synchronize(check=True) == []


if __name__ == "__main__":
    unittest.main()
