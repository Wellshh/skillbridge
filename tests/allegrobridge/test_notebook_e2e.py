# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Iterator
from json import loads
from os import environ
from pathlib import Path
from shutil import copy2
from socket import socket
from subprocess import run
from sys import executable, platform
from typing import Any, cast

from pytest import TempPathFactory, fixture, mark, raises

from allegrobridge import Allegro, Workspace
from allegrobridge._kernel import UNBOUND, RemoteObject, RemoteTable, RemoteVector
from allegrobridge._kernel.client.hints import SkillCode
from allegrobridge.client.translator import Translator
from allegrobridge.util import ASSETS_DIR
from tests.support.channel import DummyChannel

JUPYTER_PROBES = (
    '_ipython_canary_method_should_not_exist_',
    '_ipython_display_',
    '_repr_mimebundle_',
    '_repr_html_',
    '_repr_markdown_',
    '_repr_svg_',
    '_repr_png_',
    '_repr_pdf_',
    '_repr_jpeg_',
    '_repr_latex_',
    '_repr_json_',
    '_repr_javascript_',
    '_rapped',
    '__wrapped__',
)
_ROOT = Path(__file__).parents[2]
_QUICKSTART = _ROOT / 'docs' / 'examples' / 'quickstart.ipynb'
_TEST_BOARD = ASSETS_DIR / 'shape1.brd'


@fixture
def notebook_workspace() -> tuple[DummyChannel, Workspace]:
    channel = DummyChannel()
    return channel, Workspace(channel, 'notebook')


@fixture
def remote_design(
    notebook_workspace: tuple[DummyChannel, Workspace],
) -> tuple[DummyChannel, Workspace, RemoteObject]:
    channel, ws = notebook_workspace
    channel.inputs.append('Remote("__py_db_0x4d2")')
    design = cast('RemoteObject', ws.db.get_design())
    assert channel.outputs.pop() == 'axlDBGetDesign()'
    return channel, ws, design


@fixture
def remote_collections(
    notebook_workspace: tuple[DummyChannel, Workspace],
) -> tuple[DummyChannel, RemoteTable, RemoteVector]:
    channel, ws = notebook_workspace
    channel.inputs.append('Table("__py_table_1")')
    table = ws.make_table('T', 0)
    assert channel.outputs.pop() == 'makeTable("T" 0)'
    channel.inputs.append('Vector("__py_vector_1")')
    vector = ws.make_vector(3, 0)
    assert channel.outputs.pop() == 'makeVector(3 0)'
    return channel, table, vector


@fixture(scope='module')
def quickstart_notebook() -> dict[str, Any]:
    return cast('dict[str, Any]', loads(_QUICKSTART.read_text(encoding='utf-8')))


@fixture(scope='class')
def notebook_allegro(tmp_path_factory: TempPathFactory) -> Iterator[Allegro]:
    mode = 'cli' if platform == 'win32' else 'manual'
    workspace_id = None
    board = None
    if mode == 'cli':
        with socket() as listener:
            listener.bind(('localhost', 0))
            workspace_id = str(listener.getsockname()[1])
        board = Path(copy2(_TEST_BOARD, tmp_path_factory.mktemp('notebook')))
    with Allegro.open(mode=mode, board=board, workspace_id=workspace_id) as opened:
        yield opened


def _source(cell: dict[str, Any]) -> str:
    source = cell['source']
    return ''.join(source) if isinstance(source, list) else cast('str', source)


def _code_cells(notebook: dict[str, Any]) -> list[tuple[int, str]]:
    return [
        (index, _source(cell))
        for index, cell in enumerate(notebook['cells'])
        if cell['cell_type'] == 'code'
    ]


class TestUnit:
    def test_quickstart_notebook_is_clean_and_compilable(
        self,
        quickstart_notebook: dict[str, Any],
    ) -> None:
        assert quickstart_notebook['nbformat'] == 4
        assert quickstart_notebook['metadata']['kernelspec']['name'] == 'python3'
        assert quickstart_notebook['cells']
        assert _source(quickstart_notebook['cells'][0]).startswith('# AllegroBridge Quickstart')

        code_cells = _code_cells(quickstart_notebook)
        assert code_cells
        for index, source in code_cells:
            compile(source, f'{_QUICKSTART.name}:cell-{index}', 'exec')
            cell = quickstart_notebook['cells'][index]
            assert cell['execution_count'] is None
            assert cell['outputs'] == []

    def test_notebook_function_display_and_probing_send_no_requests(
        self,
        notebook_workspace: tuple[DummyChannel, Workspace],
    ) -> None:
        channel, ws = notebook_workspace

        assert repr(ws.db) == '<function collection db*>'
        assert repr(ws.axl) == '<function collection axl*>'
        assert 'get_design' in dir(ws.db)
        assert 'db_get_design' in dir(ws.axl)
        assert 'dir' in dir(ws.db)
        assert 'db' in dir(ws)
        for probe in (*JUPYTER_PROBES, '__call__'):
            assert not hasattr(ws.db, probe)
        assert not callable(ws.db)
        assert not channel.outputs

        get_design = ws.db.get_design
        assert repr(get_design) == '<remote function axlDBGetDesign>'
        for probe in JUPYTER_PROBES:
            assert not hasattr(get_design, probe)
        assert not hasattr(get_design, 'lazy')
        assert not hasattr(get_design, 'var')
        assert callable(get_design)
        assert not channel.outputs

        expression = get_design.expr()
        assert expression.render() == 'axlDBGetDesign()'
        for probe in JUPYTER_PROBES:
            assert not hasattr(expression, probe)
        with raises(TypeError, match='no local truth value'):
            bool(expression)
        assert not channel.outputs

    def test_notebook_object_display_and_probing_send_no_requests(
        self,
        remote_design: tuple[DummyChannel, Workspace, RemoteObject],
    ) -> None:
        channel, _, design = remote_design
        assert str(design) == '<remote db@0x4d2>'
        assert repr(design) == '<remote object@0x4d2>'
        assert design.skill_id == 0x4D2
        assert design.skill_parent_type == 'db'
        assert 'dir' in dir(design)
        assert design == design  # ruff: ignore[comparison-with-itself]
        for probe in JUPYTER_PROBES:
            assert not hasattr(design, probe)
        assert not hasattr(design, 'lazy')
        assert callable(design)
        assert not channel.outputs

    def test_notebook_collection_display_and_probing_send_no_requests(
        self,
        remote_collections: tuple[DummyChannel, RemoteTable, RemoteVector],
    ) -> None:
        channel, table, vector = remote_collections
        assert str(table) == '<remote table>'
        assert repr(table) == '<remote table>'
        assert str(vector) == '<remote vector>'
        assert repr(vector) == '<remote vector>'
        for probe in (*JUPYTER_PROBES, '__call__'):
            assert not hasattr(table, probe)
            assert not hasattr(vector, probe)
        assert not callable(table)
        assert not callable(vector)
        with raises(TypeError, match=r'length\(\)'):
            bool(table)
        with raises(TypeError, match=r'length\(\)'):
            bool(vector)
        assert not channel.outputs

    def test_notebook_function_and_object_operations_send_one_request_each(
        self,
        remote_design: tuple[DummyChannel, Workspace, RemoteObject],
    ) -> None:
        channel, ws, design = remote_design

        channel.inputs.append('[[0, 0], [100, 200]]')
        assert design.b_box == [[0, 0], [100, 200]]
        assert channel.outputs.pop() == '__py_db_0x4d2->bBox'

        channel.inputs.append('[[0, 0], [1, 1]]')
        design.b_box = [[0, 0], [1, 1]]
        assert channel.outputs.pop() == '__py_db_0x4d2->bBox = (list (list 0 0) (list 1 1))'

        channel.inputs.append('["bBox", "objType"]')
        assert design.dir() == ['b_box', 'obj_type']
        assert channel.outputs.pop() == Translator.encode_dir(SkillCode('__py_db_0x4d2'))

        channel.inputs.append('["bBox", "objType"]')
        assert design.help() == 'Properties:\n- b_box\n- obj_type'
        assert channel.outputs.pop() == Translator.encode_dir(SkillCode('__py_db_0x4d2'))

        channel.inputs.append('"axlDBGetDesign axlDBCreateNet axlGeoDistance"')
        assert ws.db.dir() == ['get_design', 'create_net']
        assert channel.outputs.pop() == 'buildString(listFunctions("^axl[A-Z]"))'

        channel.inputs.append('"axlDBGetDesign() => d_design"')
        assert ws.db.get_design.help() == 'axlDBGetDesign() => d_design'
        assert channel.outputs.pop() == Translator.encode_help('axlDBGetDesign')

        assert not channel.outputs
        assert not channel.inputs

    def test_notebook_collection_operations_send_one_request_each(
        self,
        remote_collections: tuple[DummyChannel, RemoteTable, RemoteVector],
    ) -> None:
        channel, table, vector = remote_collections
        table_snapshot_command = (
            'mapcar(lambda((_entry) list(t car(_entry) cadr(_entry))) tableToList(__py_table_1))'
        )
        membership_command = (
            'let(((_key "x")) '
            'if(exists(_item __py_table_1 equal(_item _key)) list(t __py_table_1[_key]) nil))'
        )
        vector_snapshot_command = (
            'let((_result _value (_size length(__py_vector_1))) '
            'when(_size > 0 for(_index 0 sub1(_size) '
            "_value = __py_vector_1[_index] _result = cons(if(boundp('_value) "
            'list(t _value) list(nil t)) _result))) reverse(_result))'
        )

        channel.inputs.append('2')
        assert table.length() == 2
        assert channel.outputs.pop() == 'length(__py_table_1)'

        channel.inputs.append('1')
        assert table['key'] == 1
        assert channel.outputs.pop() == 'arrayref(__py_table_1 "key")'

        channel.inputs.append('None')
        table['key'] = 2
        assert channel.outputs.pop() == 'setarray(__py_table_1 "key" 2)'

        channel.inputs.append('[True, 1]')
        assert 'x' in table
        assert channel.outputs.pop() == membership_command

        channel.inputs.append('None')
        del table['key']
        assert channel.outputs.pop() == 'remove("key" __py_table_1)'

        channel.inputs.append('[[True, "x", 1]]')
        assert table.snapshot() == [('x', 1)]
        assert channel.outputs.pop() == table_snapshot_command

        channel.inputs.append('3')
        assert vector.length() == 3
        assert channel.outputs.pop() == 'length(__py_vector_1)'

        channel.inputs.append('10')
        assert vector[0] == 10
        assert channel.outputs.pop() == 'arrayref(__py_vector_1 0)'

        channel.inputs.append('None')
        vector[1] = 20
        assert channel.outputs.pop() == 'setarray(__py_vector_1 1 20)'

        channel.inputs.append('[[True, 10], [None, True], [True, 30]]')
        assert vector.snapshot() == [10, UNBOUND, 30]
        assert channel.outputs.pop() == vector_snapshot_command

        assert not channel.outputs
        assert not channel.inputs


@mark.allegro
@mark.integration
class TestE2E:
    def test_quickstart_notebook(
        self,
        quickstart_notebook: dict[str, Any],
        notebook_allegro: Allegro,
    ) -> None:
        source = '\n\n'.join(code for _, code in _code_cells(quickstart_notebook))
        notebook_allegro.workspace.close()
        env = dict(environ)
        env['ALLEGROBRIDGE_WORKSPACE_ID'] = str(notebook_allegro.workspace_id)
        completed = run(
            [executable, '-c', source],
            cwd=_ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        assert completed.returncode == 0, completed.stdout + completed.stderr
        assert 'quickstart complete' in completed.stdout

        ws = Workspace.open(notebook_allegro.workspace_id)
        assert ws['plus'](1, 2) == 3
        ws.close()
