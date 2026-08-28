# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
import sys
from collections.abc import MutableMapping
from pathlib import Path
from subprocess import check_output, run
from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import Mock

from pytest import mark, raises

import skillbridge as skillbridge_module
import skillbridge.client.hints as hints_module
import skillbridge.client.objects as objects_module
from skillbridge import Expr, Key, SkillCode, keys
from skillbridge.client.channel import Channel
from skillbridge.client.functions import FunctionCollection, LiteralRemoteFunction
from skillbridge.client.objects import RemoteObject, RemoteTable, RemoteVector
from skillbridge.client.translator import DefaultTranslator, Symbol
from skillbridge.test.channel import DummyChannel
from skillbridge.test.workspace import DummyWorkspace

python = sys.executable


def test_obsolete_skill_container_wrappers_are_not_exported() -> None:
    for name in ('SkillList', 'SkillTuple', 'SkillDict'):
        assert not hasattr(skillbridge_module, name)
        assert not hasattr(hints_module, name)


@mark.parametrize(('id_', 'repr_'), [('0x10', 16), ('00001F', 31), ('10', 10)])
def test_skill_id(id_, repr_):
    assert RemoteObject(..., ..., SkillCode(f'__py_db_{id_}')).skill_id == repr_


def test_workspace_get_item():
    ws = DummyWorkspace()
    f = ws['myFunction_def']
    assert f._function == 'myFunction_def'
    assert f.expr().render() == 'myFunction_def()'


def test_remote_function_chaining():
    ws = DummyWorkspace()
    # 2-level chaining: FunctionCollection -> RemoteFunction -> RemoteFunction
    rf2 = ws.axl.db.get_design
    assert rf2._function == 'axl_db_get_design'
    assert rf2.expr().render() == 'axlDbGetDesign()'

    # Multi-level chaining
    rf3 = ws.axl.db.create.pin
    assert rf3._function == 'axl_db_create_pin'
    assert rf3.expr(1, 2).render() == 'axlDbCreatePin(1 2)'
    ws.prepare(3)
    assert rf3(1, 2) == 3
    assert ws.pop_request() == rf3.expr(1, 2).render()

    # LiteralRemoteFunction chaining preserves class type
    literal = ws['my_prefix'].sub_ns.func
    assert isinstance(literal, LiteralRemoteFunction)
    assert literal._function == 'my_prefix_sub_ns_func'
    assert literal.expr(42).render() == 'my_prefix_sub_ns_func(42)'

    assert not hasattr(rf3, 'lazy')
    assert not hasattr(rf3, 'var')


def test_remote_function_builds_expression_without_rpc() -> None:
    ws = DummyWorkspace()

    inner = ws.axl.db.get_design.expr()
    expression = ws['outer'].expr(inner, layer_name='TOP').result

    assert isinstance(expression, Expr)
    assert expression.render() == 'outer(axlDbGetDesign() ?layerName "TOP")->result'

    ws.prepare(3)
    assert ws.eval(expression) == 3
    assert ws.pop_request() == 'outer(axlDbGetDesign() ?layerName "TOP")->result'


def test_reports_skill_server_correctly():
    out = check_output([python, '-m', 'skillbridge', 'path'], encoding='utf-8')
    assert Path(out.splitlines()[1].strip()).exists()


def test_cannot_use_abc():
    with raises(NotImplementedError):
        Channel(1).send('')

    with raises(NotImplementedError):
        Channel(1).close()

    with raises(NotImplementedError):
        Channel(1).flush()


def test_direct_mode(no_cover):  # with coverage enabled this test breaks
    code = dedent(
        """
        from skillbridge import Workspace

        ws = Workspace.open(direct=True)
        cv = ws.ge.get_edit_cell_view()

        print(f"cell_view={cv}")

        assert ws.ge.get_cell_view_window(cv) == 42
        """,
    )
    virtuoso = b'success 1337\nsuccess 42'
    p = run(['python', '-c', code], capture_output=True, input=virtuoso, check=False)

    out = p.stdout.replace(b'\r\n', b'\n').replace(b' ', b'')
    err = p.stderr.replace(b'\r\n', b'\n').replace(b' ', b'')
    assert err == b'cell_view=1337\n'
    assert out == b'geGetEditCellView()\ngeGetCellViewWindow(1337)\n'


def test_symbol_correct_repr():
    assert str(Symbol('abc')) == 'Symbol(abc)'
    assert repr(Symbol('abc')) == "Symbol('abc')"


def test_empty_keys():
    assert keys() == []


def test_one_key():
    assert keys(x=1) == [Key('x'), 1]
    assert keys(xyz="123") == [Key('xyz'), "123"]


def test_many_keys():
    assert keys(x=1, y=(2, 3), z=True, abc="abcdef", ghi=keys(x=2)) == [
        Key('x'),
        1,
        Key('y'),
        (2, 3),
        Key('z'),
        True,
        Key('abc'),
        "abcdef",
        Key('ghi'),
        [Key('x'), 2],
    ]


def test_remote_object_builds_expression_without_rpc() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    remote = RemoteObject(channel, translator, SkillCode('TESTTEST_123'))

    expression = remote.expr().components.as_list().where(lambda item: item.enabled)

    assert expression.render() == 'setof(_expr0 TESTTEST_123->components _expr0->enabled)'
    assert not hasattr(remote, 'lazy')
    assert not channel.outputs

    channel.inputs.append('["name"]')
    assert dir(remote) == ['name']
    assert channel.outputs.pop() == translator.encode_dir(SkillCode('TESTTEST_123'))

    open_file = RemoteObject(channel, translator, SkillCode('__py_openfile_22'))
    assert 'skill_type' in dir(open_file)
    assert not channel.outputs


def test_remote_table_dunders_do_not_hide_remote_io() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    table = RemoteTable(channel, translator, SkillCode('TABLE'))

    assert str(table) == '<remote table>'
    assert repr(table) == '<remote table>'
    assert not hasattr(table, '_repr_html_')
    assert not isinstance(table, MutableMapping)
    with raises(TypeError, match=r'length\(\)'):
        bool(table)
    with raises(TypeError):
        len(table)
    assert not channel.outputs


def test_remote_table_operations_send_one_request_each() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    table = RemoteTable(channel, translator, SkillCode('TABLE'))

    channel.inputs.append('2')
    assert table.length() == 2
    assert channel.outputs.pop() == 'length(TABLE )'

    channel.inputs.append('1')
    assert table['key'] == 1
    assert channel.outputs.pop() == 'arrayref(TABLE "key" )'

    channel.inputs.append('None')
    table['key'] = 2
    assert channel.outputs.pop() == 'setarray(TABLE "key" 2 )'

    channel.inputs.append('None')
    del table['key']
    assert channel.outputs.pop() == 'remove("key" TABLE )'

    channel.inputs.append('3')
    assert table.foo == 3
    assert channel.outputs.pop() == "arrayref(TABLE 'foo )"

    channel.inputs.append('None')
    table.foo = 4
    assert channel.outputs.pop() == "setarray(TABLE 'foo 4 )"

    channel.inputs.append("error('missing')")
    with raises(KeyError, match='missing'):
        _ = table['missing']
    assert channel.outputs.pop() == 'arrayref(TABLE "missing" )'


def test_remote_table_snapshot_and_iteration_each_use_one_request() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    table = RemoteTable(channel, translator, SkillCode('TABLE'))

    channel.inputs.append('[[True, "x", 1], [True, [1, 2], 3]]')
    assert table.snapshot() == [('x', 1), ([1, 2], 3)]
    assert list(channel.outputs) == [
        'mapcar(lambda((_entry) list(t car(_entry) cadr(_entry))) tableToList(TABLE))',
    ]

    channel.outputs.clear()
    channel.inputs.append('None')
    assert table.snapshot() == []
    assert list(channel.outputs) == [
        'mapcar(lambda((_entry) list(t car(_entry) cadr(_entry))) tableToList(TABLE))',
    ]

    channel.outputs.clear()
    channel.inputs.append('[[True, "x", 1], [True, 2, 3]]')
    assert list(table) == ['x', 2]
    assert list(channel.outputs) == [
        'mapcar(lambda((_entry) list(t car(_entry) cadr(_entry))) tableToList(TABLE))',
    ]


def test_remote_table_membership_and_get_ignore_table_default() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    table = RemoteTable(channel, translator, SkillCode('TABLE'))

    channel.inputs.append('99')
    assert table['missing'] == 99
    assert channel.outputs.pop() == 'arrayref(TABLE "missing" )'

    channel.inputs.append('[True, None]')
    assert 'present' in table
    assert channel.outputs.pop() == (
        'let(((_key "present")) if(exists(_item TABLE equal(_item _key)) list(t TABLE[_key]) nil))'
    )

    channel.inputs.append('None')
    assert 'missing' not in table
    assert channel.outputs.pop() == (
        'let(((_key "missing")) if(exists(_item TABLE equal(_item _key)) list(t TABLE[_key]) nil))'
    )

    channel.inputs.append('[True, None]')
    assert table.get('present', 'fallback') is None
    assert channel.outputs.pop() == (
        'let(((_key "present")) if(exists(_item TABLE equal(_item _key)) list(t TABLE[_key]) nil))'
    )

    channel.inputs.append('None')
    assert table.get('missing', 'fallback') == 'fallback'
    assert channel.outputs.pop() == (
        'let(((_key "missing")) if(exists(_item TABLE equal(_item _key)) list(t TABLE[_key]) nil))'
    )


def test_unbound_is_a_public_read_only_sentinel() -> None:
    assert skillbridge_module.UNBOUND is objects_module.UNBOUND
    assert not hasattr(hints_module, 'UNBOUND')
    assert str(skillbridge_module.UNBOUND) == 'UNBOUND'
    assert repr(skillbridge_module.UNBOUND) == 'UNBOUND'
    with raises(AttributeError):
        skillbridge_module.UNBOUND.value = 1


def test_remote_vector_dunders_and_negative_indexes_do_not_send_requests() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    vector = RemoteVector(channel, translator, SkillCode('VECTOR'))

    assert str(vector) == '<remote vector>'
    assert repr(vector) == '<remote vector>'
    assert 'snapshot' in dir(vector)
    assert not hasattr(vector, '_repr_html_')
    with raises(TypeError, match=r'length\(\)'):
        bool(vector)
    with raises(TypeError):
        len(vector)
    with raises(IndexError, match='-1'):
        _ = vector[-1]
    with raises(IndexError, match='-1'):
        vector[-1] = 1
    assert not channel.outputs


def test_remote_vector_snapshot_iteration_and_membership_each_use_one_request() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    vector = RemoteVector(channel, translator, SkillCode('VECTOR'))
    snapshot_command = (
        'let((_result _value (_size length(VECTOR))) '
        'when(_size > 0 for(_index 0 sub1(_size) '
        "_value = VECTOR[_index] _result = cons(if(boundp('_value) "
        'list(t _value) list(nil t)) _result))) reverse(_result))'
    )

    channel.inputs.append('[[True, 1], [None, True], [True, None]]')
    assert vector.snapshot() == [1, skillbridge_module.UNBOUND, None]
    assert channel.outputs.pop() == snapshot_command

    channel.inputs.append('None')
    assert vector.snapshot() == []
    assert channel.outputs.pop() == snapshot_command

    channel.inputs.append('[[True, "x"], [None, True]]')
    assert list(vector) == ['x', skillbridge_module.UNBOUND]
    assert channel.outputs.pop() == snapshot_command

    channel.inputs.append('[[True, 1], [None, True]]')
    assert skillbridge_module.UNBOUND in vector
    assert channel.outputs.pop() == snapshot_command

    channel.inputs.append('[[True, 1], [None, True]]')
    assert 2 not in vector
    assert channel.outputs.pop() == snapshot_command


def test_remote_vector_item_operations_send_one_request() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    vector = RemoteVector(channel, translator, SkillCode('VECTOR'))

    channel.inputs.append('1')
    assert vector[0] == 1
    assert channel.outputs.pop() == 'arrayref(VECTOR 0 )'

    channel.inputs.append('None')
    vector[1] = 2
    assert channel.outputs.pop() == 'setarray(VECTOR 1 2 )'

    channel.inputs.append("error('unbound')")
    with raises(IndexError, match=r'1.*unbound'):
        _ = vector[1]
    assert channel.outputs.pop() == 'arrayref(VECTOR 1 )'


def test_remote_vector_bounds_errors_do_not_request_length() -> None:
    channel = DummyChannel()
    translator = DefaultTranslator()
    vector = RemoteVector(channel, translator, SkillCode('VECTOR'))

    send = Mock(side_effect=RuntimeError('array index out of bounds'))
    channel.send = send
    with raises(IndexError, match=r'5.*out of range'):
        _ = vector[5]
    send.assert_called_once_with('arrayref(VECTOR 5 )')

    send = Mock(side_effect=RuntimeError('array index out of bounds'))
    channel.send = send
    with raises(IndexError, match=r'5.*out of range'):
        vector[5] = 1
    send.assert_called_once_with('setarray(VECTOR 5 1 )')


def test_static_completion_generator_covers_valid_and_empty_namespaces(
    monkeypatch,
    tmp_path,
) -> None:
    package = tmp_path / 'skillbridge'
    client = package / 'client'
    client.mkdir(parents=True)
    annotation = client / 'workspace.pyi'
    options_calls = []

    def options(*args, **kwargs):
        options_calls.append((args, kwargs))
        return object()

    def generate_stubs(_options):
        annotation.write_text('class Workspace:\n    db: FunctionCollection\n', encoding='utf-8')

    channel = DummyChannel()
    translator = DefaultTranslator()
    db = FunctionCollection(channel, 'db', translator)
    db._dir = ['valid', 'not-valid', 'class']
    empty = FunctionCollection(channel, 'empty', translator)
    empty._dir = ['not-valid', 'class']
    workspace = SimpleNamespace(db=db, empty=empty, other=object())
    workspace.__dict__['_private'] = db
    workspace.__dict__['class'] = db

    monkeypatch.setattr(skillbridge_module, '__file__', str(package / '__init__.py'))
    monkeypatch.setattr(skillbridge_module, 'chdir', lambda _path: None)
    monkeypatch.setattr(skillbridge_module, 'import_stub_gen', lambda: (options, generate_stubs))
    monkeypatch.setattr(skillbridge_module.Workspace, 'open', staticmethod(lambda: workspace))

    skillbridge_module.generate_static_completion()
    first = annotation.read_text(encoding='utf-8')
    skillbridge_module.generate_static_completion()

    assert len(options_calls) == 2
    assert '    db: FunctionCollection' not in first
    assert '    class db:' in first
    assert '        valid: staticmethod' in first
    assert '    class empty:\n        pass' in first
    assert 'not-valid' not in first


def test_static_completion_imports_mypy_generator() -> None:
    options, generate_stubs = skillbridge_module.import_stub_gen()

    assert callable(options)
    assert callable(generate_stubs)


def test_double_hex_prefix_does_not_crash():
    remote = RemoteObject(..., ..., SkillCode('__py_stuff_0x0xcafe'))

    assert remote.skill_id == 0xCAFE
    assert remote.skill_parent_type == 'stuff'
    assert RemoteObject(..., ..., SkillCode('__py_stuff_0xcafe')).skill_id == 0xCAFE


def test_object_representation_does_not_send_requests():
    assert (
        str([RemoteObject(..., ..., SkillCode('__py_stuff_0x0xcafe'))])
        == '[<remote object@0xcafe>]'
    )


def test_failing_skill_type_is_handled():
    channel = DummyChannel()
    translator = DefaultTranslator()
    r = RemoteObject(channel, translator, SkillCode('__py_stuff_0x0xcafe'))
    channel.inputs.append('None')
    assert r.skill_type is None
    assert r.skill_type is None
