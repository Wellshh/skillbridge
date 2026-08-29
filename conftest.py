# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Shared pytest configuration."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        '--allegro', action='store_true', default=False, help='run Allegro integration tests'
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    if config.getoption('--allegro'):
        return
    for item in items:
        if item.get_closest_marker('allegro') is not None:
            item.add_marker(pytest.mark.skip(reason='requires --allegro'))
