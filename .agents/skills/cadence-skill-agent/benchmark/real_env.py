from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from allegrobridge import Workspace

SKILL_ROOT = Path(__file__).resolve().parents[1]
CORPUS_ROOT = Path(__file__).resolve().parent / "corpus"
SCORE_PATH = Path(__file__).resolve().parent / "real_env_score.json"


def _posix(path: Path) -> str:
    return path.resolve().as_posix()


def _sklint_code(il_path: Path, lint_path: Path) -> str:
    return (
        f'errset(sklint(?file "{_posix(il_path)}" ?checkPubFuncs t ?noPrintLog t '
        f'?outputFile "{_posix(lint_path)}"))'
    )


def _load_code(il_path: Path) -> str:
    return f'errset(load("{_posix(il_path)}"))'


def _smoke_code(smoke_path: Path) -> str:
    source = smoke_path.read_text(encoding="utf-8").replace("\n", " ")
    return (
        "let((capturePort smokeResult ping report) "
        "capturePort = outstring() "
        "unwindProtect("
        "let(((poport capturePort)) "
        f"smokeResult = progn({source}) "
        "ping = plus(1 2) "
        "report = getOutstring(capturePort)) "
        "close(capturePort)) "
        "list(smokeResult ping report))"
    )


def _decode_smoke(result: object) -> dict:
    if not isinstance(result, (list, tuple)) or len(result) != 3:
        return {}
    smoke_result, ping, report = result
    return {"smoke_result": smoke_result, "ping": ping, "report": report}


def verify_il(
    workspace: Workspace,
    il_path: Path,
    smoke_path: Path,
    *,
    lint_dir: Path,
) -> dict:
    il_path = Path(il_path)
    lint_dir = Path(lint_dir)
    lint_dir.mkdir(parents=True, exist_ok=True)
    lint_path = lint_dir / f"{il_path.stem}.lint"
    if lint_path.exists():
        lint_path.unlink()

    sklint_result = workspace["evalstring"](_sklint_code(il_path, lint_path))
    sklint_pass = bool(sklint_result)
    lint_report = lint_path.read_text(encoding="utf-8") if lint_path.is_file() else ""

    load_result = workspace["evalstring"](_load_code(il_path))
    load_pass = bool(load_result)

    smoke_result = workspace["evalstring"](_smoke_code(smoke_path))
    smoke = _decode_smoke(smoke_result)
    smoke_pass = bool(smoke.get("smoke_result")) and smoke.get("ping") == 3

    return {
        "sklint_pass": sklint_pass,
        "load_pass": load_pass,
        "smoke_pass": smoke_pass,
        "lint_report": lint_report,
        "smoke_report": smoke.get("report", ""),
    }


def corpus_tasks() -> list[tuple[str, Path, Path]]:
    tasks = []
    for task_dir in sorted(CORPUS_ROOT.iterdir()):
        if not task_dir.is_dir():
            continue
        il = task_dir / "agent.il"
        if not il.is_file():
            il = task_dir / "oracle.il"
        smoke = task_dir / "smoke.ils"
        if not il.is_file() or not smoke.is_file():
            continue
        tasks.append((task_dir.name, il, smoke))
    return tasks
