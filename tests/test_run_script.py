from __future__ import annotations

import sys
from pathlib import Path
from runpy import run_module
from unittest.mock import MagicMock

import pytest

from allegrobridge._kernel import _run_script


def test_main_preserves_script_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    run_path = MagicMock()
    monkeypatch.setattr(_run_script, 'run_path', run_path)
    monkeypatch.setattr(sys, 'argv', ['runner', 'script.py', 'one', 'two'])

    _run_script.main()

    assert sys.argv == ['script.py', 'one', 'two']
    run_path.assert_called_once_with('script.py', run_name='__main__')


def test_module_ignores_shadow_package_beside_script(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    script_directory = tmp_path / 'scripts'
    script_directory.mkdir()
    shadow_package = script_directory / 'allegrobridge'
    shadow_package.mkdir()
    (shadow_package / '__init__.py').write_text('', encoding='utf-8')
    result = tmp_path / 'result.txt'
    script = script_directory / 'script.py'
    script.write_text(
        'from pathlib import Path\n'
        'from sys import argv\n'
        'from allegrobridge._kernel import Workspace\n'
        'Path(argv[1]).write_text(f"{Workspace.__module__}|{argv[2]}", encoding="utf-8")\n',
        encoding='utf-8',
    )
    monkeypatch.setattr(sys, 'argv', ['runner', str(script), str(result), 'value'])
    monkeypatch.delitem(sys.modules, _run_script.__name__)

    run_module(_run_script.__name__, run_name='__main__')

    assert result.read_text(encoding='utf-8') == 'allegrobridge._kernel.client.workspace|value'


def test_main_propagates_script_exception(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    script = tmp_path / 'script.py'
    script.write_text('raise RuntimeError("script failed")\n', encoding='utf-8')
    monkeypatch.setattr(sys, 'argv', ['runner', str(script)])

    with pytest.raises(RuntimeError, match='script failed'):
        _run_script.main()
