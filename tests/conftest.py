#!/usr/bin/env python3
# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Pytest configuration for the test-suite."""

from __future__ import annotations

import sys
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
