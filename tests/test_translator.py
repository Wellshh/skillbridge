# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from collections.abc import Callable
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Any

from hypothesis import given
from hypothesis.strategies import floats, integers, lists, none, text
from pytest import fixture, mark, raises, warns

from allegrobridge.client.translator import Translator as ATranslator
from skillbridge import Symbol
from skillbridge.client.expr import Expr
from skillbridge.client.hints import SkillCode
from skillbridge.client.translator import (
    DefaultTranslator,
    Translator,
    build_python_path,
    build_skill_path,
    camel_to_snake,
    snake_to_camel,
)

floats = floats(allow_infinity=False, allow_nan=False)
ints = integers(min_value=-(2**63), max_value=2**63 - 1)
asciis = text(ascii_uppercase + ascii_lowercase + ascii_letters, max_size=99)
symbols = text(ascii_uppercase + ascii_lowercase + ascii_letters, min_size=4, max_size=99)
simple_types = floats | ints | none() | asciis


@fixture(scope='module')
def simple_translator() -> Translator:
    t = DefaultTranslator()
    t.register_remote_variable_type('Remote', lambda code: code)
    return t


@fixture(scope='module')
def encode_simple(simple_translator: Translator) -> Callable[[Any], Any]:
    return simple_translator.encode


@fixture(scope='module')
def decode_simple(simple_translator: Translator) -> Callable[[str], Any]:
    return simple_translator.decode


def test_snake_to_wrong_camel_case():
    assert snake_to_camel('load_XML_from_string') == 'loadXMLFromString'
    assert snake_to_camel('load_xml_from_string') == 'loadXmlFromString'


def test_wrong_camel_to_snake_case():
    assert camel_to_snake('loadXMLConfigFromString') == 'load_XML_config_from_string'
    assert camel_to_snake('loadXmlConfigFromString') == 'load_xml_config_from_string'


def test_snake_to_camel_simple_does_not_change():
    assert snake_to_camel('x') == 'x'
    assert snake_to_camel('simple') == 'simple'
    assert snake_to_camel('longbutstillsimple') == 'longbutstillsimple'


def test_snake_to_camel_input_does_not_change():
    assert snake_to_camel('alreadyCamel') == 'alreadyCamel'
    assert snake_to_camel('thisIsCamelCase') == 'thisIsCamelCase'
    assert snake_to_camel('thisIsHTML') == 'thisIsHTML'
    assert snake_to_camel('value1') == 'value1'
    assert snake_to_camel('value123') == 'value123'


def test_snake_to_camel_input_snake_changes():
    assert snake_to_camel('snake_case') == 'snakeCase'
    assert snake_to_camel('this_is_snake_case') == 'thisIsSnakeCase'
    assert snake_to_camel('layer1_mask') == 'layer1Mask'
    assert snake_to_camel('layer_mask1') == 'layerMask1'


def test_camel_to_snake_simple_does_not_change():
    assert camel_to_snake('x') == 'x'
    assert camel_to_snake('simple') == 'simple'
    assert camel_to_snake('longbutstillsimple') == 'longbutstillsimple'
    assert camel_to_snake('layout1') == 'layout1'
    assert camel_to_snake('layout123') == 'layout123'


def test_camel_to_snake_input_camel():
    assert camel_to_snake('camelCase') == 'camel_case'
    assert camel_to_snake('thisIsCamelCase') == 'this_is_camel_case'
    assert camel_to_snake('thisIsHTML') == 'this_is_HTML'
    assert camel_to_snake('abcXYz') == 'abc_x_yz'
    assert camel_to_snake('layer1Mask') == 'layer1_mask'
    assert camel_to_snake('layerMask1') == 'layer_mask1'


def test_named_parameters_are_optionally_converted(simple_translator: Translator):
    code = simple_translator.encode_call('func', 1, 2, 3, x=10, long_name=20, longName=30)
    assert code.replace(' ', '') == 'func(123?x10?longName20?longName30)'


def test_camel_to_snake_input_snake_does_not_change():
    assert camel_to_snake('snake_case') == 'snake_case'
    assert camel_to_snake('this_is_snake_case') == 'this_is_snake_case'
    assert camel_to_snake('x_Y_and_z') == 'x_y_and_z'


def test_camel_to_snake_input_pascal_does_not_change():
    assert camel_to_snake('Class') == 'Class'
    assert camel_to_snake('ThisIsAClass') == 'ThisIsAClass'


def test_snake_to_camel_input_pascal_does_not_change():
    assert snake_to_camel('Class') == 'Class'
    assert snake_to_camel('ThisIsAClass') == 'ThisIsAClass'


@given(ints | floats | asciis)
def test_simple_to_skill(encode_simple, i):
    assert encode_simple(i) == repr(i).replace("'", '"')


def test_constants_to_skill(encode_simple):
    assert encode_simple(None) == 'nil'
    assert encode_simple(True) == 't'  # ruff: ignore[boolean-positional-value-in-call]
    assert encode_simple(False) == 'nil'  # ruff: ignore[boolean-positional-value-in-call]


def test_lists_to_skill(encode_simple):
    assert encode_simple([]) == '(list )'
    assert encode_simple([1]) == '(list 1)'
    assert encode_simple([1, 2]) == '(list 1 2)'
    assert encode_simple([[1, 2], [3, 4]]) == '(list (list 1 2) (list 3 4))'


def test_tuples_use_skill_list_wire_format(encode_simple):
    assert encode_simple((1, 2)) == '(list 1 2)'


@given(asciis)
def test_expr_to_skill(encode_simple, a):
    assert encode_simple(Expr.raw_skill(a)) == a


def test_custom_encoder_attribute_error_is_not_swallowed(encode_simple):
    class BrokenEncoder:
        def __repr_skill__(self):
            raise AttributeError('broken encoder')

    with raises(AttributeError, match='broken encoder'):
        encode_simple(BrokenEncoder())


def test_property_list_to_python(decode_simple):
    pl = decode_simple('{"x":1,"y":2}')
    assert isinstance(pl, dict)
    assert pl['x'] == 1
    assert pl['y'] == 2
    assert pl == {'x': 1, 'y': 2}

    pl = decode_simple('{"x":Remote("__py_object_123")}')
    assert isinstance(pl, dict)
    assert 'object' in pl['x']
    assert '123' in pl['x']

    pl = decode_simple('{"x": {"y": 2}}')
    assert isinstance(pl, dict)
    assert isinstance(pl['x'], dict)
    assert pl['x']['y'] == 2
    assert pl == {'x': {'y': 2}}


def test_property_list_to_skill(encode_simple):
    p = {'x': 1, 'y': 2}
    assert encode_simple(p) == "list(nil 'x 1 'y 2)"

    p = {'x': 'x', 'y': 'y'}
    assert encode_simple(p) == """list(nil 'x "x" 'y "y")"""


def test_object_to_python(decode_simple):
    python = decode_simple('Remote("dbobject:123")')
    assert '123' in python
    assert 'dbobject' in python

    python = decode_simple('[1,2,3,Remote("dbobject:123")]')
    assert python[:3] == [1, 2, 3]
    assert '123' in python[3]
    assert 'dbobject' in python[3]

    skill = '[[1,2,3,Remote("dbobject:123")],[Remote("dbobject:234"),4,5,6]]'
    python = decode_simple(skill)
    assert python[0][:3] == [1, 2, 3]
    assert '123' in python[0][3]
    assert 'dbobject' in python[0][3]
    assert '234' in python[1][0]
    assert 'dbobject' in python[1][0]


def test_object_with_upper_case_id(decode_simple):
    python = decode_simple('Remote("rodObject:123")')
    assert 'rodObject' in python
    assert '123' in python


@given(lists(simple_types | lists(simple_types)))
def test_list_roundtrip(decode_simple, i):
    python = decode_simple(repr(i))
    assert python == i or (python is None and i == [])


def test_constants_to_python(decode_simple):
    assert decode_simple('None') is None
    assert decode_simple('True') is True


@mark.parametrize('value', [..., Exception, open])
def test_unknown_to_skill(value, encode_simple):
    with raises(Exception):
        encode_simple(value)


@given(asciis, asciis)
def test_get_attribute(simple_translator: Translator, obj, name):
    assert simple_translator.encode_getattr(obj, name).replace(' ', '') == f'{obj}->{name}'


@given(asciis, asciis, ints)
def test_set_attribute(simple_translator: Translator, obj, name, value):
    got = simple_translator.encode_setattr(obj, name, value).replace(' ', '')
    left = f'{obj}->{name}'
    expected = f'{left}={value}'
    assert got == expected


@given(symbols)
def test_symbol_is_parsed(decode_simple, name):
    parsed = decode_simple(f"Symbol({name!r})")
    assert isinstance(parsed, Symbol)
    assert parsed.name == name


@given(symbols)
def test_symbol_is_dumped(encode_simple, name):
    skill = encode_simple(Symbol(name))
    assert skill == f"'{name}"


def test_skill_help_adds_question_mark(simple_translator: Translator):
    assert 'x->?' in simple_translator.encode_dir(SkillCode('x'))
    assert 'x->y->?' in simple_translator.encode_dir(SkillCode('x->y'))


def test_skill_help_to_list(simple_translator: Translator):
    expected = ['abc', 'def', 'camel_case', 'snake_case']
    assert simple_translator.decode_dir('["abc","def","camelCase","snake_case"]') == expected


def test_skill_setattr_ok(simple_translator: Translator):
    skill = simple_translator.encode_setattr(SkillCode('x'), 'key', 123).replace(' ', '')
    assert skill == 'x->key=123'

    skill = simple_translator.encode_setattr(SkillCode('x->y'), 'key', 123).replace(' ', '')
    assert skill == 'x->y->key=123'


def test_python_path():
    assert build_python_path(['x']) == 'x'
    assert build_python_path(['x', 'y']) == 'x.y'
    assert build_python_path(['x', 'y', 123]) == 'x.y[123]'


def test_skill_path_supports_integer_indexes():
    assert build_skill_path(['x', 1, 'name']) == '(nth 1 x)->name'


def test_warning_prefix_is_removed(decode_simple):
    with warns(UserWarning, match='prefixed'):
        assert decode_simple("warning('*WARNING*prefixed', 1)") == 1


@mark.parametrize(
    ('snake_name', 'expected_skill_name'),
    [
        ('db_get_design', 'axlDBGetDesign'),
        ('drc_get_count', 'axlDRCGetCount'),
        ('geo_rotate_pt', 'axlGeoRotatePt'),
        ('ui_yes_no', 'axlUIYesNo'),
        ('spreadsheet_get_rgb_color_string', 'axlSpreadsheetGetRGBColorString'),
        ('cns_get_via_zpvf', 'axlCNSGetViaZPVF'),
        ('cns_add_via', 'axlCnsAddVia'),
        ('is_point_inside_box', 'axlIsPointInsideBox'),
        ('dbid_name', 'axlDbidName'),
        ('pad_suppress_ok_layer', 'axlPadSuppressOkLayer'),
        ('package_design_check_drc_error', 'axlPackageDesignCheckDrcError'),
        ('form_create', 'axlFormCreate'),
        ('axl_clear_sel_set', 'axlClearSelSet'),
        ('axlDBGetDesign', 'axlDBGetDesign'),
        ('axl_cns_add_via', 'axlCnsAddVia'),
        ('axl_is_point_inside_box', 'axlIsPointInsideBox'),
        ('axl_dbid_name', 'axlDbidName'),
        ('axl_pad_suppress_ok_layer', 'axlPadSuppressOkLayer'),
        ('axl_package_design_check_drc_error', 'axlPackageDesignCheckDrcError'),
    ],
)
def test_allegro_translator_format_function_name(
    snake_name: str,
    expected_skill_name: str,
) -> None:
    assert ATranslator.format_function_name(snake_name) == expected_skill_name


def test_allegro_translator_falls_back_for_unknown_functions() -> None:
    assert ATranslator.format_function_name('user_custom_function') == 'userCustomFunction'
    assert ATranslator.format_function_name('axl_custom_function') == 'axlCustomFunction'


def test_allegro_translator_has_working_decode() -> None:
    a = ATranslator()
    assert a.decode('3') == 3
    assert a.decode('None') is None
    assert a.decode('True') is True
    assert a.decode('[1,2,3]') == [1, 2, 3]
    assert a.decode('{"x":1,"y":2}') == {'x': 1, 'y': 2}


def test_allegro_translator_has_working_encode() -> None:
    a = ATranslator()
    value = True
    assert a.encode(3) == '3'
    assert a.encode(None) == 'nil'
    assert a.encode(value) == 't'
    assert a.encode([1, 2]) == '(list 1 2)'
