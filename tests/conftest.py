#!/usr/bin/env python3
"""Pytest configuration for the test-suite."""

from __future__ import annotations

import sys
from warnings import warn

import pytest

from skillbridge import Workspace

# The channel integration tests use ``pty``, which is unavailable on Windows.
collect_ignore_glob: list[str] = []
if sys.platform == 'win32':
    collect_ignore_glob = ['test_channel.py']


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        '--allegro', action='store_true', default=False, help='run allegro bridge integration tests'
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    if config.option.allegro:
        return
    for item in items:
        if item.get_closest_marker('allegro') is not None:
            item.add_marker(pytest.mark.skip(reason='requires --allegro'))


@pytest.fixture(scope='module')
def ws() -> Workspace:
    try:
        workspace = Workspace.open()
        assert workspace['plus'](1, 2) == 3
    except (Exception, ValueError, AssertionError):  # ruff: ignore[blind-except]
        warn("Skipping integration tests, because Workspace could not connect", UserWarning)
        pytest.skip()

    return workspace
