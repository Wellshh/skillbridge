import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "skill_lint.py"
REPO_ROOT = Path(__file__).parents[4]
FIXTURES = REPO_ROOT / "tests" / "skill" / "qtest" / "src" / "qcover" / "fixtures"


def run_lint(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )


def write_fixture(directory: Path, name: str, text: str) -> Path:
    path = directory / name
    path.write_text(text, encoding="utf-8")
    return path


class SkillLintTests(unittest.TestCase):
    def test_balanced_fixture_is_clean(self) -> None:
        result = run_lint(str(FIXTURES / "branches.il"))

        assert result.returncode == 0
        assert not result.stdout

    def test_unbalanced_paren_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            path = write_fixture(
                Path(directory),
                "unbalanced.il",
                "(defun foo () (let ((x 1) (println x))\n",
            )

            result = run_lint(str(path))

            assert result.returncode == 1
            assert "ERROR" in result.stdout
            assert "(" in result.stdout

    def test_unterminated_string_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            path = write_fixture(
                Path(directory),
                "badstring.il",
                '(println "abc)\n',
            )

            result = run_lint(str(path))

            assert result.returncode == 1
            assert "unterminated string" in result.stdout

    def test_static_only_does_not_flag_eval_time_error(self) -> None:
        result = run_lint(str(FIXTURES / "invalid.il"))

        assert result.returncode == 0
        assert not result.stdout

    def test_parens_in_strings_and_comments_ignored(self) -> None:
        with TemporaryDirectory() as directory:
            path = write_fixture(
                Path(directory),
                "masked.il",
                '(println "(", 42) ; (unclosed\n',
            )

            result = run_lint(str(path))

            assert result.returncode == 0
            assert not result.stdout

    def test_unclosed_bracket_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            path = write_fixture(
                Path(directory),
                "bracket.il",
                "let((a #[1 2\n",
            )

            result = run_lint(str(path))

            assert result.returncode == 1
            assert "[" in result.stdout

    def test_quiet_suppresses_stdout(self) -> None:
        with TemporaryDirectory() as directory:
            path = write_fixture(Path(directory), "bad.il", "(\n")

            result = run_lint(str(path), "--quiet")

            assert result.returncode == 1
            assert not result.stdout


if __name__ == "__main__":
    unittest.main()
