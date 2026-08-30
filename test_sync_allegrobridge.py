# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import os
import shutil
from collections.abc import Mapping, Sequence
from pathlib import Path
from subprocess import CompletedProcess, run

_SCRIPT = Path(__file__).parent / 'sync-allegrobridge.sh'


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    check: bool = True,
) -> CompletedProcess:
    return run(  # ruff: ignore[subprocess-without-shell-equals-true]
        command,
        cwd=str(cwd),
        env=env,
        check=check,
        capture_output=True,
        text=True,
    )


def _git(repo: Path, *args: str) -> CompletedProcess:
    return _run(['git', *args], cwd=repo)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def _commit(repo: Path, message: str) -> None:
    _git(repo, 'add', '-A')
    _git(repo, 'commit', '-q', '-m', message)


def _make_repositories(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    source = tmp_path / 'skillbridge'
    target = tmp_path / 'allegrobridge-extract'
    source.mkdir()
    target.mkdir()

    for repo in (source, target):
        _git(repo, 'init', '-q')
        _git(repo, 'config', 'user.name', 'Sync Test')
        _git(repo, 'config', 'user.email', 'sync@example.invalid')

    files = {
        'conftest.py': 'source pytest configuration\n',
        'mkdocs.yml': 'site_name: fixture\n',
        'allegrobridge/module.py': 'source module\n',
        'allegrobridge/PLAN.md': 'private plan\n',
        'allegrobridge/nested/.DS_Store': 'metadata\n',
        'allegrobridge/_kernel/server/module.py': 'source server\n',
        'allegrobridge/_kernel/server/SECRET.md': 'private secret\n',
        'allegrobridge/_kernel/nested/.DS_Store': 'metadata\n',
        'tests/test_example.py': 'def test_example():\n    assert True\n',
        'tests/nested/.DS_Store': 'metadata\n',
        'benchmark/test_micro.py': 'def test_micro():\n    assert True\n',
        'benchmark/nested/.DS_Store': 'metadata\n',
        'scripts/tool.py': 'print("tool")\n',
        'scripts/nested/.DS_Store': 'metadata\n',
        'docs/index.md': '# Fixture\n',
        'docs/nested/.DS_Store': 'metadata\n',
    }
    for relative_path, content in files.items():
        _write(source / relative_path, content)
    _write(source / 'pyproject.toml', 'source project\n')
    _commit(source, 'fixture change')

    _write(target / 'README.md', 'extract root\n')
    _write(target / 'pyproject.toml', 'target project\n')
    _write(target / 'allegrobridge/obsolete.py', 'obsolete\n')
    _write(target / 'skillbridge/legacy.py', 'legacy\n')
    _commit(target, 'extract baseline')
    shutil.copy2(_SCRIPT, source / _SCRIPT.name)
    return source, target, files


def test_sync_mirrors_committed_directories_and_is_idempotent(tmp_path: Path) -> None:
    source, target, files = _make_repositories(tmp_path)

    first = _run(['bash', str(source / _SCRIPT.name)], cwd=source, env=os.environ.copy())

    source_hash = _git(source, 'log', '-1', '--format=%h').stdout.strip()
    assert f'sync: mirrored skillbridge@{source_hash} -> allegrobridge-extract' in first.stdout
    assert _git(target, 'log', '-1', '--format=%s').stdout.strip() == (
        f'chore(sync): from skillbridge@{source_hash}: fixture change'
    )
    assert (target / 'README.md').read_text(encoding='utf-8') == 'extract root\n'
    assert (target / 'pyproject.toml').read_text(encoding='utf-8') == 'target project\n'
    assert not (target / 'allegrobridge/obsolete.py').exists()
    assert not (target / 'skillbridge').exists()
    for relative_path, content in files.items():
        destination = target / relative_path
        if destination.name == '.DS_Store' or relative_path in {
            'allegrobridge/PLAN.md',
            'allegrobridge/_kernel/server/SECRET.md',
        }:
            assert not destination.exists()
        else:
            assert destination.read_text(encoding='utf-8') == content

    commit_count = _git(target, 'rev-list', '--count', 'HEAD').stdout
    second = _run(['bash', str(source / _SCRIPT.name)], cwd=source, env=os.environ.copy())
    assert second.stdout.strip() == 'sync: allegrobridge-extract already up to date'
    assert _git(target, 'rev-list', '--count', 'HEAD').stdout == commit_count


def test_sync_refuses_dirty_target_before_writing(tmp_path: Path) -> None:
    source, target, _ = _make_repositories(tmp_path)
    readme = target / 'README.md'
    readme.write_text('uncommitted root change\n', encoding='utf-8')
    before_status = _git(target, 'status', '--short').stdout
    before_commit = _git(target, 'rev-parse', 'HEAD').stdout

    result = _run(
        ['bash', str(source / _SCRIPT.name)],
        cwd=source,
        env=os.environ.copy(),
        check=False,
    )

    assert result.returncode != 0
    assert 'has uncommitted changes' in result.stderr
    assert readme.read_text(encoding='utf-8') == 'uncommitted root change\n'
    assert (target / 'allegrobridge/obsolete.py').read_text(encoding='utf-8') == 'obsolete\n'
    assert _git(target, 'status', '--short').stdout == before_status
    assert _git(target, 'rev-parse', 'HEAD').stdout == before_commit
