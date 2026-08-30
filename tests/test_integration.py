# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from pathlib import Path
from time import sleep
from typing import Any, cast
from warnings import warn

from pytest import fixture, mark, raises, skip

from allegrobridge._kernel import UNBOUND, Expr, RemoteObject, RemoteTable, Symbol, Workspace

here = Path(__file__).parent


@fixture(scope='module')
def ws() -> Workspace:
    try:
        workspace = Workspace.open()
        assert workspace['plus'](1, 2) == 3
    except (Exception, ValueError, AssertionError):  # ruff: ignore[blind-except]
        warn("Skipping integration tests, because Workspace could not connect", UserWarning)
        skip()

    return workspace


@fixture(scope='module')
def dd_libs(ws: Workspace) -> list:
    """Virtuoso library list; skips when ddGetLibList is unavailable (non-Virtuoso).

    ddGetLibList is a dfII/Virtuoso API absent in Allegro PCB, so the dd-oriented
    integration tests probe it once and skip gracefully on other backends.
    """
    try:
        return cast('list', ws.dd.get_lib_list())
    except RuntimeError as exc:
        if 'undefined function' in str(exc):
            skip('ddGetLibList unavailable (not a Virtuoso/dfII backend)')
        raise


def test_can_add_two_numbers(ws: Workspace) -> None:
    assert ws['plus'](2, 3) == 5


def test_can_create_a_hash_table(ws: Workspace) -> None:
    t = ws.make_table('T')

    assert isinstance(t, RemoteTable)
    assert str(t) == "<remote table>"


def test_can_store_keys_in_hash_table(ws: Workspace) -> None:
    t = ws.make_table('T')

    t['x'] = 123
    t[123] = [2, 3, 4]

    assert t['x'] == 123
    assert t[123] == [2, 3, 4]


def test_can_read_length_of_hash_table(ws: Workspace) -> None:
    t = ws.make_table('T')

    assert t.length() == 0
    t['x'] = 1
    assert t.length() == 1
    t['x'] = 2
    assert t.length() == 1
    del t['x']
    assert t.length() == 0


def test_can_iterate_over_hash_table_keys(ws: Workspace) -> None:
    t = ws.make_table('T')

    assert list(t) == []
    t['x'] = 1
    assert list(t) == ['x']
    t[2] = 3
    assert set(t) == {'x', 2}


def test_can_snapshot_hash_table_entries(ws: Workspace) -> None:
    t = ws.make_table('T')

    assert t.snapshot() == []
    t['x'] = 1
    assert dict(t.snapshot()) == {'x': 1}
    t['y'] = 3
    assert dict(t.snapshot()) == {'x': 1, 'y': 3}


def test_hash_table_snapshot_preserves_non_dict_keys(ws: Workspace) -> None:
    t = ws.make_table('T')

    t[None] = Symbol('nilValue')
    t[cast('Any', [1, 2])] = 3

    snapshot = t.snapshot()
    assert (None, Symbol('nilValue')) in snapshot
    assert ([1, 2], 3) in snapshot


def test_hash_table_membership_and_get_ignore_default(ws: Workspace) -> None:
    t = ws.make_table('T', 99)

    t['present'] = None

    assert t['missing'] == 99
    assert 'present' in t
    assert 'missing' not in t
    assert t.get('present', 'fallback') is None
    assert t.get('missing', 'fallback') == 'fallback'


def test_can_use_symbol_keys_in_hash_table(ws: Workspace) -> None:
    t = ws.make_table('T', None)

    t[Symbol('key')] = 123
    assert t['key'] is None
    assert t[Symbol('key')] == 123


def test_can_snapshot_sparse_vector(ws: Workspace) -> None:
    vector = ws.make_vector(4)
    vector[0] = 1
    vector[2] = None
    vector[3] = Symbol('value')

    expected = [1, UNBOUND, None, Symbol('value')]
    assert vector.snapshot() == expected
    assert list(vector) == expected
    assert UNBOUND in vector
    assert 1 in vector
    with raises(IndexError, match='unbound'):
        _ = vector[1]


def test_missing_key_raises_key_error(ws: Workspace) -> None:
    t = ws.make_table('T')

    with raises(KeyError, match=r'XYZ'):
        _ = t['XYZ']


def test_open_file(ws: Workspace) -> None:
    file = cast('RemoteObject', ws['outfile']('__test_skill_python.txt', 'w'))

    assert file.skill_parent_type == 'openfile'
    assert file.remote_type() == 'open_file'
    assert str(file) == '<remote open_file>'
    assert isinstance(dir(file), list)


def test_remote_object(dd_libs: list) -> None:
    libs = dd_libs

    assert libs
    lib = libs[0]

    assert isinstance(lib.skill_id, int)
    assert lib.skill_parent_type == 'dd'
    assert lib.remote_type() == 'Lib'
    assert str(lib).startswith('<remote dd@')
    assert set(lib.dir()) > {'cells', 'is_readable', 'group', 'name'}
    assert lib.is_readable == lib['isReadable']

    with raises(AttributeError):
        _ = lib._repr_html_

    lib.help()

    assert lib == lib  # ruff: ignore[comparison-with-itself]
    assert lib != libs[1]
    assert not (lib == 1)  # ruff: ignore[negate-equal-op]  # this tests __eq__ and the next line tests __ne__
    assert lib != 1


def test_list_expression(ws: Workspace, dd_libs: list) -> None:
    lib = max(dd_libs, key=lambda lib: len(lib.cells or ()))

    cells = lib.expr().cells.as_list()

    assert isinstance(lib.cells, list)
    assert cast('int', ws['length'](cells)) > 0
    assert ws['length'](cells.where(lambda cell: cell.name == '__no_cell_is_named_this')) == 0

    assert ws.eval(cells[0]) == lib.cells[0]
    assert ws.eval(cells) == lib.cells

    names = ws.make_table('CellNames')

    ws.eval(
        cells.for_each(
            lambda cell: ws['setarray'].expr(names, cell['name'], cell['readPath']),
        ),
    )

    for cell in [ws.eval(cells[0]), ws.eval(cells[1]), ws.eval(cells[2])]:
        if cell is None:
            continue

        assert names[cell.name] == cell.read_path

    ws.eval(cells.for_each(lambda _cell: Expr.call('print', 123)))

    read_write = cells.where(lambda cell: cell.is_readable & cell.is_writable)
    read_only = cells.where(lambda cell: cell.is_readable & ~cell.is_writable)
    write_only = cells.where(lambda cell: ~cell.is_readable & cell.is_writable)
    nothing = cells.where(lambda cell: ~cell.is_readable & ~cell.is_writable)
    assert ws['length'](cells) == sum(
        cast('int', ws['length'](group)) for group in (read_only, read_write, write_only, nothing)
    )


def test_vector_without_default(ws: Workspace) -> None:
    v = ws.make_vector(10)

    assert v.length() == 10

    for i in range(-7, 14):
        with raises(IndexError, match=str(i)):
            _ = v[i]

    v[0] = 10
    v[2] = 12

    assert list(v) == [10, UNBOUND, 12, *([UNBOUND] * 7)]
    v[1] = 11
    assert list(v) == [10, 11, 12, *([UNBOUND] * 7)]

    assert v[0] == 10

    with raises(IndexError, match='10'):
        v[10] = 100


def test_direct_globals(ws: Workspace) -> None:
    ws['set'](Symbol('myGlobalValue'), 102030)

    assert ws.__.my_global_value == 102030
    assert ws.__['myGlobalValue'] == 102030


def test_collections_with_default(ws: Workspace) -> None:
    t = ws.make_table('T', 123)
    assert t[10] == 123

    v = ws.make_vector(10, 12)
    assert list(v) == [12] * 10


def test_table_getattr_is_equivalent_to_symbol_lookup(ws: Workspace) -> None:
    t = ws.make_table('T')

    t[Symbol('abcDef')] = 10
    assert t.abc_def == 10

    t.xyz_abc = 20
    assert t[Symbol('xyzAbc')] == 20


def test_nil_t_nil_is_not_a_disembodied_property_list(ws: Workspace) -> None:
    assert ws["cdr"]([0, None, True, None]) == [None, True, None]


def test_run_script_does_not_block(ws: Workspace) -> None:
    variable = 'skillbridge_script_args'
    ws['set'](Symbol(variable), 0)
    assert ws['pyRunScript'](str(here / 'script.py'), args=(variable, '42', '0.25'))

    assert ws['plus'](Expr.raw_skill(variable), 1) == 1
    sleep(1.0)
    assert ws['plus'](Expr.raw_skill(variable), 1) == 43


def test_run_script_blocks_when_requested(ws: Workspace) -> None:
    variable = 'skillbridge_script_args'
    ws['set'](Symbol(variable), 0)
    assert ws['pyRunScript'](str(here / 'script.py'), args=(variable, '42', '0.25'), block=True)

    assert ws['plus'](Expr.raw_skill(variable), 1) == 43


@mark.skip
def test_form_vectors_have_dir(ws: Workspace) -> None:
    form = ws.hi.get_current_form()
    assert 'button_layout' in dir(form)


@mark.skip
def test_form_vectors_have_getattr(ws: Workspace) -> None:
    form = ws.hi.get_current_form()
    assert isinstance(cast('Any', form).button_layout, list)


def test_outstring(ws: Workspace) -> None:
    outstring = ws['outstring']
    get_outstring = ws['getOutstring']
    close = ws['close']
    fprintf = ws['fprintf']

    s = outstring()
    assert get_outstring(s) == ""  # ruff: ignore[compare-to-empty-string]

    assert fprintf(s, "Hello ")
    assert get_outstring(s) == "Hello "

    assert fprintf(s, "World")
    assert get_outstring(s) == "Hello World"

    assert close(s)
    assert get_outstring(s) is None


def test_load_temporary_large_skill_file(tmp_path: Path, ws: Workspace) -> None:
    function = '__skillbridgeLargeBatchCalc'
    statements = '\n'.join('      total = total + 1' for _ in range(5_000))
    script = (
        f"(putd '{function} nil)\n"
        f'(defun {function} ()\n'
        '  (let((total)\n'
        '    total = 0\n'
        f'{statements}\n'
        '    total))\n'
    )
    script_path = tmp_path / 'generated_large_logic.il'
    script_path.write_text(script, encoding='utf-8')

    try:
        assert ws['load'](script_path.resolve().as_posix()) is True
        assert ws[function]() == 5_000
    finally:
        ws['putd'](Symbol(function), None)


def test_large_rpc_payload(ws: Workspace) -> None:
    payload = 'x' * 1_048_576

    assert ws['strlen'](payload) == len(payload)


def test_workspace_define_multiline_custom_function(ws: Workspace) -> None:
    function = 'userCustomMatrixCalc'
    code = """
    let((acc)
      acc = 0
      for(i 1 limit
        acc = acc + i * multiplier
      )
      acc
    )
    """

    try:
        ws.define('custom_matrix_calc', args=['limit', 'multiplier'], code=code)
        assert ws[function](10, 2) == 110
    finally:
        ws['putd'](Symbol(function), None)
