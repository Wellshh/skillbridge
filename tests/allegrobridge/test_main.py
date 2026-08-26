from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest

from allegrobridge import __main__ as main_module

PYTHON_SERVER = (
    Path(__file__).parents[2] / 'skillbridge' / 'server' / 'python_server.il'
).resolve()
ALLEGRO_SERVER = (
    Path(__file__).parents[2] / 'allegrobridge' / 'server' / 'allegro_server.il'
).resolve()


def test_path_prints_load_instructions_for_existing_server_files(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main_module.main(['path'])

    out = capsys.readouterr().out
    assert f'load("{PYTHON_SERVER.as_posix()}")' in out
    assert f'load("{ALLEGRO_SERVER.as_posix()}")' in out
    assert PYTHON_SERVER.is_file()
    assert ALLEGRO_SERVER.is_file()


def test_main_without_command_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    main_module.main([])

    assert 'path' in capsys.readouterr().out


def test_main_entry_point(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, 'argv', ['allegrobridge'])

    runpy.run_module('allegrobridge.__main__', run_name='__main__')

    assert 'path' in capsys.readouterr().out
