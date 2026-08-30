# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest

import allegrobridge._kernel
from allegrobridge._kernel import __main__ as main_module


def test_main_dispatches_path_generate_shell_and_help(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    generate = MagicMock()
    shell = MagicMock()
    monkeypatch.setattr(main_module, 'generate_static_completion', generate)
    monkeypatch.setattr(main_module, 'shell_command', shell)

    monkeypatch.setattr(sys, 'argv', ['allegrobridge._kernel', 'path'])
    main_module.main()
    assert 'python_server.ils' in capsys.readouterr().out

    monkeypatch.setattr(sys, 'argv', ['allegrobridge._kernel', 'generate'])
    main_module.main()
    generate.assert_called_once_with()

    monkeypatch.setattr(
        sys,
        'argv',
        ['allegrobridge._kernel', 'shell', '--id', '7', '--ping', '--force-tcp'],
    )
    main_module.main()
    assert shell.call_args.args == ('7', True, True)

    monkeypatch.setattr(sys, 'argv', ['allegrobridge._kernel'])
    main_module.main()
    assert 'shell' in capsys.readouterr().out


@pytest.mark.parametrize('ping', [False, True])
def test_shell_command_opens_workspace_and_optionally_pings(
    ping: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = MagicMock()
    workspace.__getitem__.return_value.return_value = 9
    open_workspace = MagicMock(return_value=workspace)
    interact = MagicMock()
    monkeypatch.setattr(allegrobridge._kernel.Workspace, 'open', open_workspace)
    monkeypatch.setattr(main_module, 'interact', interact)
    monkeypatch.setattr(main_module, 'randrange', MagicMock(side_effect=[4, 5]))

    main_module.shell_command('7', ping=ping, force_tcp=True)

    open_workspace.assert_called_once_with('7', force_tcp=True)
    if ping:
        workspace.__getitem__.assert_called_once_with('plus')
        workspace.__getitem__.return_value.assert_called_once_with(4, 5)
    else:
        workspace.__getitem__.assert_not_called()
    assert interact.call_args.kwargs['local']['ws'] is workspace
