"""Pytest configuration for the test-suite."""

from __future__ import annotations

import sys
from warnings import warn

import pytest

from skillbridge import Workspace

# On Windows the ``pty``/``UnixStreamServer``-based server tests cannot be
# imported (the ``skillbridge.server.python_server`` module references
# POSIX-only primitives), so skip them entirely during collection.
collect_ignore_glob: list[str] = []
if sys.platform == 'win32':
    collect_ignore_glob = ['test_channel.py', 'test_server.py']


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
