from __future__ import annotations

import ast
from pathlib import Path

from allegrobridge.util import _extract_apis  # ruff: ignore[import-private-name]
from scripts.generate_axl_stubs import DOCUMENT_ONLY_NAMES

STUB_PATH = Path(__file__).parents[2] / 'allegrobridge' / 'client' / '_axl_stubs.pyi'


def _literal_value(annotation: ast.expr | None) -> str | None:
    if not isinstance(annotation, ast.Subscript):
        return None
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != 'Literal':
        return None
    value = annotation.slice
    return value.value if isinstance(value, ast.Constant) and isinstance(value.value, str) else None


def test_generated_stub_declares_axl_contract() -> None:
    assert STUB_PATH.is_file(), 'Phase 2 must generate the Allegro API stub'

    tree = ast.parse(STUB_PATH.read_text(encoding='utf-8'))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

    axl_methods = {node.name for node in classes['Axl'].body if isinstance(node, ast.FunctionDef)}
    assert {
        'air_gap',
        'alt_symbol_replace',
        'db_create_prop_dict_entry',
        'db_create_via',
        'db_find_by_name',
        'db_get_design',
        'db_text_block_create',
    } <= axl_methods

    db_methods = {node.name for node in classes['AxlDB'].body if isinstance(node, ast.FunctionDef)}
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
        if (value := _literal_value(node.args.args[1].annotation)) is not None
    }
    api_names = _extract_apis()
    assert len(api_names) == 792
    assert len(literal_names) == 786
    assert literal_names == set(api_names) - DOCUMENT_ONLY_NAMES
