# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from pytest import raises

from skillbridge import Var


def test_var_string_conversion():
    assert str(Var('x')) == 'Var(x)'
    assert repr(Var('x')) == "Var('x')"
    assert Var('x').__repr_skill__() == 'x'


def test_var_truthiness_raises_type_error():
    with raises(TypeError, match='has no local truth value'):
        bool(Var('x'))


def test_var_attribute_access():
    assert Var('x').y.z.__repr_skill__() == 'x->y->z'
    assert Var('x').name.__repr_skill__() == 'x->name'


def test_var_item_access():
    assert Var('x')[0][1].__repr_skill__() == 'nth(1 nth(0 x))'
    assert Var('x')['name'].__repr_skill__() == 'x->name'


def test_infix():
    assert (Var('x') == 123).__repr_skill__() == '(x == 123)'
    assert (Var('x') != 123).__repr_skill__() == '(x != 123)'
    assert (Var('x') > 123).__repr_skill__() == '(x > 123)'
    assert (Var('x') >= 123).__repr_skill__() == '(x >= 123)'
    assert (Var('x') < 123).__repr_skill__() == '(x < 123)'
    assert (Var('x') <= 123).__repr_skill__() == '(x <= 123)'
    assert (Var('x') + 123).__repr_skill__() == '(x + 123)'
    assert (Var('x') - 123).__repr_skill__() == '(x - 123)'
    assert (Var('x') * 123).__repr_skill__() == '(x * 123)'
    assert (Var('x') / 123).__repr_skill__() == '(x / 123)'
    assert (Var('x') | Var('y')).__repr_skill__() == 'or(x y )'
    assert (Var('x') & Var('y')).__repr_skill__() == 'and(x y )'


def test_getattr_performs_conversion():
    assert Var('x').abc_def.__repr_skill__() == 'x->abcDef'


def test_getitem_does_not_perform_conversion():
    assert Var('x')['abc_def'].__repr_skill__() == 'x->abc_def'
