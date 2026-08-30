# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import ast
from pathlib import Path

from allegrobridge.util import _extract_apis
from scripts.generate_axl_stubs import DOCUMENT_ONLY_NAMES

STUB_PATH = Path(__file__).parents[2] / 'allegrobridge' / 'client' / '_axl_stubs.pyi'


def _literal_value(annotation: ast.expr | None) -> str | None:
    if not isinstance(annotation, ast.Subscript):
        return None
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != 'Literal':
        return None
    value = annotation.slice
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    return None


def test_generated_stub_declares_axl_contract() -> None:
    assert STUB_PATH.is_file(), 'Phase 2 must generate the Allegro API stub'

    tree = ast.parse(STUB_PATH.read_text(encoding='utf-8'))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

    axl_methods = {
        node.target.id
        for node in classes['Axl'].body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    }
    assert {
        'air_gap',
        'alt_symbol_replace',
        'db_create_prop_dict_entry',
        'db_create_via',
        'db_find_by_name',
        'db_get_design',
        'db_text_block_create',
    } <= axl_methods

    db_methods = {
        node.target.id
        for node in classes['AxlDB'].body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    }
    assert {
        'create_prop_dict_entry',
        'create_via',
        'find_by_name',
        'get_design',
        'text_block_create',
    } <= db_methods

    literal_names = {
        value
        for node in classes['_WorkspaceTypingMixin'].body
        if isinstance(node, ast.FunctionDef) and node.name == '__getitem__'
        if (value := _literal_value((node.args.posonlyargs + node.args.args)[1].annotation))
        is not None
    }
    api_names = _extract_apis()
    assert len(api_names) == 792
    assert len(literal_names) == 786
    assert literal_names == set(api_names) - DOCUMENT_ONLY_NAMES

    callable_classes = {
        name: node
        for name, node in classes.items()
        if any(
            isinstance(base, ast.Name) and base.id == 'LiteralRemoteFunction' for base in node.bases
        )
    }
    assert len(callable_classes) == 786
    get_design = callable_classes['_AxlDBGetDesign']
    get_design_call = next(
        node
        for node in get_design.body
        if isinstance(node, ast.FunctionDef) and node.name == '__call__'
    )
    assert 'axlDBGetDesign()' in (ast.get_docstring(get_design_call) or '')
    assert 'Allegro 17.2-2016' in (ast.get_docstring(get_design_call) or '')

    axl_body = classes['Axl'].body
    get_design_member = next(
        index
        for index, node in enumerate(axl_body)
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == 'db_get_design'
    )
    member_doc = axl_body[get_design_member + 1]
    assert isinstance(member_doc, ast.Expr)
    assert isinstance(member_doc.value, ast.Constant)
    assert isinstance(member_doc.value.value, str)
    assert 'axlDBGetDesign()' in member_doc.value.value

    stub = STUB_PATH.read_text(encoding='utf-8')
    assert 'from allegrobridge._kernel.client.expr import Expr' in stub
    assert 'def __call__(self, /) -> RemoteObject | None:' in stub
    assert 'def __call__(self, s_type: Symbol, t_name: str, /) -> RemoteObject | None:' in stub
    assert 'def expr(self, /) -> Expr[RemoteObject | None]: ...' in stub
    assert (
        'def expr(self, s_type: Symbol, t_name: str, /) -> Expr[RemoteObject | None]: ...' in stub
    )
    assert 'def expr(self, value: None, /) -> Expr[list[str]]: ...' in stub
    assert (
        'def __call__(self, x_block_template: int, /, *, width: float | None = ..., '
        'height: float | None = ..., line_space: float | None = ..., '
        'char_space: float | None = ..., photo_width: float | None = ...) -> Skill:' in stub
    )
    assert 'Args:' in stub
    assert 'Returns:' in stub
    assert 'Padstack name.' in stub
    assert 'Creates a via in the layout as specified by the arguments described below.' in stub

    assert not DOCUMENT_ONLY_NAMES & literal_names
