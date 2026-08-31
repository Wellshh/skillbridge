# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Skill bridge adapter for Cadence Allegro 17.2."""

from __future__ import annotations

from logging import NullHandler, getLogger

from ._kernel import (
    UNBOUND,
    Expr,
    Function,
    Globals,
    GlobalVar,
    Key,
    ListExpr,
    ParseError,
    RemoteObject,
    RemoteTable,
    RemoteVector,
    SkillCode,
    Symbol,
    current_workspace,
    generate_static_completion,
    keys,
)
from ._logging import setup_logging
from .allegro import Allegro, OpenMode
from .client.base import SkillModule
from .client.session import Session
from .client.workspace import Workspace
from .version import __version__

getLogger("allegrobridge").addHandler(NullHandler())

__all__ = [
    'UNBOUND',
    'Allegro',
    'Expr',
    'Function',
    'GlobalVar',
    'Globals',
    'Key',
    'ListExpr',
    'OpenMode',
    'ParseError',
    'RemoteObject',
    'RemoteTable',
    'RemoteVector',
    'Session',
    'SkillCode',
    'SkillModule',
    'Symbol',
    'Workspace',
    '__version__',
    'current_workspace',
    'generate_static_completion',
    'keys',
    'setup_logging',
]
