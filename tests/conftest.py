#!/usr/bin/env python3
# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Pytest configuration for the test-suite."""

from __future__ import annotations

import logging
import sys
from collections.abc import Iterator
from warnings import warn

import pytest

from allegrobridge._kernel import Workspace

# The channel integration tests use ``pty``, which is unavailable on Windows.
collect_ignore_glob: list[str] = []
if sys.platform == 'win32':
    collect_ignore_glob = ['test_channel.py']


@pytest.fixture(scope='module')
def ws() -> Workspace:
    try:
        workspace = Workspace.open()
        assert workspace['plus'](1, 2) == 3
    except (Exception, ValueError, AssertionError):  # ruff: ignore[blind-except]
        warn("Skipping integration tests, because Workspace could not connect", UserWarning)
        pytest.skip()

    return workspace


@pytest.fixture(autouse=True)
def restore_logging_state() -> Iterator[None]:
    logger = logging.getLogger('allegrobridge')
    saved_handlers = list(logger.handlers)
    saved_level = logger.level
    saved_propagate = logger.propagate
    yield
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
    logger.handlers[:] = saved_handlers
    logger.level = saved_level
    logger.propagate = saved_propagate
