"""Pytest configuration for the test-suite."""

from __future__ import annotations

import sys

# On Windows the ``pty``/``UnixStreamServer``-based server tests cannot be
# imported (the ``skillbridge.server.python_server`` module references
# POSIX-only primitives), so skip them entirely during collection.
collect_ignore_glob = []
if sys.platform == 'win32':
    collect_ignore_glob = ['test_channel.py', 'test_server.py']
