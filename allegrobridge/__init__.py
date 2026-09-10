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
from .client.api import (
    ArcTo,
    Batch,
    BBox,
    Board,
    Cmd,
    CmdResult,
    Component,
    ComponentRef,
    Drc,
    DrcFigure,
    DrcObjectRef,
    Layer,
    LineTo,
    Net,
    NetRef,
    Padstack,
    PcbSymbol,
    Pin,
    PinRef,
    Point,
    Route,
    Shape,
    Via,
)
from .client.base import SkillModule
from .client.session import Session
from .client.workspace import Workspace
from .version import __version__

getLogger("allegrobridge").addHandler(NullHandler())

__all__ = [
    'UNBOUND',
    'Allegro',
    'ArcTo',
    'BBox',
    'Batch',
    'Board',
    'Cmd',
    'CmdResult',
    'Component',
    'ComponentRef',
    'Drc',
    'DrcFigure',
    'DrcObjectRef',
    'Expr',
    'Function',
    'GlobalVar',
    'Globals',
    'Key',
    'Layer',
    'LineTo',
    'ListExpr',
    'Net',
    'NetRef',
    'OpenMode',
    'Padstack',
    'ParseError',
    'PcbSymbol',
    'Pin',
    'PinRef',
    'Point',
    'RemoteObject',
    'RemoteTable',
    'RemoteVector',
    'Route',
    'Session',
    'Shape',
    'SkillCode',
    'SkillModule',
    'Symbol',
    'Via',
    'Workspace',
    '__version__',
    'current_workspace',
    'generate_static_completion',
    'keys',
    'setup_logging',
]
