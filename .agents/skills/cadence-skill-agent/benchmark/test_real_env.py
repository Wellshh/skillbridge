from __future__ import annotations

import json
import sys
from collections.abc import Callable, Iterator
from pathlib import Path
from shutil import copy2
from socket import socket
from sys import platform
from typing import TYPE_CHECKING

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import real_env

if TYPE_CHECKING:
    from allegrobridge import Allegro

_TEST_BOARD = Path(__file__).resolve().parents[3] / "allegrobridge" / "assets" / "shape1.brd"


class FakeWorkspace:
    def __init__(self, results: list[object]) -> None:
        self._results = list(results)
        self.calls: list[tuple[str, str]] = []

    def __getitem__(self, key: str) -> Callable[..., object]:
        def call(*args: object, **kwargs: object) -> object:
            self.calls.append((key, args[0] if args else ""))
            return self._results.pop(0) if self._results else None

        return call


@pytest.fixture
def smoke_path(tmp_path: Path) -> Path:
    path = tmp_path / "smoke.ils"
    path.write_text("(dummy)\n", encoding="utf-8")
    return path


def test_verify_il_all_pass(tmp_path: Path, smoke_path: Path) -> None:
    workspace = FakeWorkspace([True, True, ["17.2", 3, ""]])
    report = real_env.verify_il(workspace, tmp_path / "x.il", smoke_path, lint_dir=tmp_path)
    assert report["sklint_pass"] is True
    assert report["load_pass"] is True
    assert report["smoke_pass"] is True
    assert [call[0] for call in workspace.calls] == ["evalstring"] * 3


def test_verify_il_sklint_failure(tmp_path: Path, smoke_path: Path) -> None:
    workspace = FakeWorkspace([None, True, ["r", 3, ""]])
    report = real_env.verify_il(workspace, tmp_path / "x.il", smoke_path, lint_dir=tmp_path)
    assert report["sklint_pass"] is False
    assert report["load_pass"] is True


def test_verify_il_load_failure(tmp_path: Path, smoke_path: Path) -> None:
    workspace = FakeWorkspace([True, None, ["r", 3, ""]])
    report = real_env.verify_il(workspace, tmp_path / "x.il", smoke_path, lint_dir=tmp_path)
    assert report["load_pass"] is False


def test_verify_il_smoke_result_failure(tmp_path: Path, smoke_path: Path) -> None:
    workspace = FakeWorkspace([True, True, [None, 3, ""]])
    report = real_env.verify_il(workspace, tmp_path / "x.il", smoke_path, lint_dir=tmp_path)
    assert report["smoke_pass"] is False


def test_verify_il_smoke_ping_failure(tmp_path: Path, smoke_path: Path) -> None:
    workspace = FakeWorkspace([True, True, ["r", 999, ""]])
    report = real_env.verify_il(workspace, tmp_path / "x.il", smoke_path, lint_dir=tmp_path)
    assert report["smoke_pass"] is False


def test_corpus_tasks_discovers_version_and_ping() -> None:
    tasks = {name: (il, smoke) for name, il, smoke in real_env.corpus_tasks()}
    assert set(tasks) == {"ping", "version"}
    for il, smoke in tasks.values():
        assert il.name == "oracle.il"
        assert smoke.name == "smoke.ils"


@pytest.fixture(scope="session")
def real_env_score() -> Iterator[dict]:
    score: dict = {"tasks": []}
    yield score
    real_env.SCORE_PATH.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")


@pytest.fixture
def bench_allegro(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Allegro]:
    if platform != "win32":
        pytest.skip("real-env benchmark requires the Windows Allegro board")
    board = Path(copy2(_TEST_BOARD, tmp_path_factory.mktemp("real-env")))
    with socket() as listener:
        listener.bind(("localhost", 0))
        workspace_id = str(listener.getsockname()[1])
    from allegrobridge import Allegro

    with Allegro.open(mode="cli", board=board, workspace_id=workspace_id) as opened:
        yield opened


@pytest.mark.allegro
@pytest.mark.timeout(600)
class TestRealEnvBenchmark:
    @pytest.mark.parametrize(
        ("task_id", "il_path", "smoke_path"),
        [(t[0], t[1], t[2]) for t in real_env.corpus_tasks()],
        ids=[t[0] for t in real_env.corpus_tasks()],
    )
    def test_il_passes_real_environment(
        self,
        bench_allegro: Allegro,
        real_env_score: dict,
        task_id: str,
        il_path: Path,
        smoke_path: Path,
        tmp_path: Path,
    ) -> None:
        report = real_env.verify_il(bench_allegro.workspace, il_path, smoke_path, lint_dir=tmp_path)
        real_env_score["tasks"].append({
            "id": task_id,
            "il": il_path.name,
            "sklint_pass": report["sklint_pass"],
            "load_pass": report["load_pass"],
            "smoke_pass": report["smoke_pass"],
        })
        assert report["sklint_pass"], report["lint_report"]
        assert report["load_pass"]
        assert report["smoke_pass"], report["smoke_report"]
