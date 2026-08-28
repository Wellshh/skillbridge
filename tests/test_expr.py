# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from typing import Any

from pytest import raises

from skillbridge.client.expr import Expr, ListExpr
from skillbridge.client.hints import SkillCode


class EncodedOnce:
    def __init__(self) -> None:
        self.calls = 0

    def __repr_skill__(self) -> SkillCode:
        self.calls += 1
        return SkillCode('encodedValue')


def test_expr_is_explicitly_remote_and_unhashable() -> None:
    expr = Expr.raw_skill('design')

    assert expr.render() == 'design'
    assert expr.__repr_skill__() == 'design'

    with raises(TypeError, match='truth value'):
        bool(expr)

    with raises(TypeError, match='unhashable'):
        hash(expr)


def test_expr_wraps_values_without_treating_strings_as_source() -> None:
    encoded = EncodedOnce()

    wrapped = Expr.wrap(encoded)

    assert encoded.calls == 1
    assert wrapped.render() == 'encodedValue'
    assert wrapped.render() == 'encodedValue'
    assert encoded.calls == 1
    assert Expr.wrap('value').render() == '"value"'


def test_expr_renders_attributes_indexes_and_binary_operations() -> None:
    design = Expr.raw_skill('design')
    component = design.components.as_list()[0]

    assert design.board_thickness.render() == 'design->boardThickness'
    assert component.name.render() == 'nth(0 design->components)->name'
    assert (component.name == 'R1').render() == '(nth(0 design->components)->name == "R1")'
    assert ((design.width + 2) * design.scale).render() == '((design->width + 2) * design->scale)'
    assert ((design.width > 10) & (design.height <= 20)).render() == (
        'and((design->width > 10) (design->height <= 20))'
    )
    assert ((design.width > 10) | (design.height <= 20)).render() == (
        'or((design->width > 10) (design->height <= 20))'
    )
    assert design['rawName'].render() == 'design->rawName'

    with raises(AttributeError, match='not-valid'):
        getattr(design, 'not-valid')

    with raises(KeyError, match='not-valid'):
        design['not-valid']

    with raises(TypeError, match='as_list'):
        design.components[0]


def test_expr_rejects_python_protocol_attributes() -> None:
    expr = Expr.raw_skill('design')

    for name in ('_repr_html_', '_ipython_display_', '__iter__', '__call__', '_private'):
        assert not hasattr(expr, name)

    assert expr['_private'].render() == 'design->_private'


def test_list_expr_renders_list_indexing_and_mapped_attributes() -> None:
    components = Expr.raw_skill('design->components').as_list()

    assert isinstance(components, ListExpr)
    assert components.render() == 'design->components'
    assert components[0].name.render() == 'nth(0 design->components)->name'
    assert components['rawName'].render() == 'design->components->rawName'
    assert components.each.name.render() == 'design->components~>name'
    assert components.each['rawName'].render() == 'design->components~>rawName'
    assert components.each[0].name.render() == 'nth(0 design->components)->name'
    assert components.each.symbol.name.render() == 'design->components~>symbol~>name'
    assert not hasattr(components.each, '_repr_html_')

    with raises(IndexError, match='negative'):
        components[-1]

    with raises(KeyError, match='not-valid'):
        components.each['not-valid']

    with raises((AttributeError, TypeError)):
        components.each.typo = 1


def test_list_expr_has_no_nil_decoding_policy() -> None:
    as_list: Any = Expr.raw_skill('items').as_list

    with raises(TypeError, match='nil_as_empty'):
        as_list(nil_as_empty=True)


def test_list_expr_where_calls_predicate_and_encoders_once() -> None:
    calls = 0
    encoded = EncodedOnce()

    def predicate(item: Expr[Any]) -> Expr[Any]:
        nonlocal calls
        calls += 1
        return item.enabled & (item.value == encoded)

    filtered = Expr.raw_skill('items').as_list().where(predicate)

    assert calls == 1
    assert encoded.calls == 1
    assert (
        filtered.render()
        == 'setof(_expr0 items and(_expr0->enabled (_expr0->value == encodedValue)))'
    )
    assert filtered.each.name.render() == (
        'setof(_expr0 items and(_expr0->enabled (_expr0->value == encodedValue)))~>name'
    )
    assert (
        filtered.render()
        == 'setof(_expr0 items and(_expr0->enabled (_expr0->value == encodedValue)))'
    )
    assert calls == 1
    assert encoded.calls == 1


def test_list_expr_builds_map_and_for_each_with_scoped_bindings() -> None:
    calls = 0
    items = Expr.raw_skill('items').as_list()

    def transform(item: Expr[Any]) -> Expr[Any]:
        nonlocal calls
        calls += 1
        return item.value + 1

    mapped = items.map(transform)
    action = items.for_each(lambda item: Expr.call('delete', item))

    assert isinstance(mapped, ListExpr)
    assert mapped.render() == 'mapcar(lambda((_expr0) (_expr0->value + 1)) items)'
    assert action.render() == 'progn(foreach(_expr0 items delete(_expr0)) nil)'
    assert calls == 1


def test_list_expr_where_uses_unique_nested_bindings() -> None:
    items = Expr.raw_skill('items').as_list()

    filtered = items.where(
        lambda outer: items.where(lambda inner: inner.parent == outer.name),
    )

    assert filtered.render() == (
        'setof(_expr0 items setof(_expr1 items (_expr1->parent == _expr0->name)))'
    )

    sibling = (
        items.where(lambda item: item.enabled).each.name
        == items.where(
            lambda item: item.visible,
        ).each.name
    )
    assert sibling.render() == (
        '(setof(_expr0 items _expr0->enabled)~>name == setof(_expr1 items _expr1->visible)~>name)'
    )


def test_list_expr_rejects_escaped_binding() -> None:
    captured: Expr[Any] | None = None

    def predicate(item: Expr[Any]) -> Expr[Any]:
        nonlocal captured
        captured = item
        return item.enabled

    filtered = Expr.raw_skill('items').as_list().where(predicate)

    assert captured is not None
    with raises(RuntimeError, match='bound iteration variable'):
        captured.value.render()
    with raises(RuntimeError, match='bound iteration variable'):
        (filtered.each.value == captured.value).render()

    # Map binding escape
    captured_map: Expr[Any] | None = None

    def mapper(item: Expr[Any]) -> Expr[Any]:
        nonlocal captured_map
        captured_map = item
        return item.value + 1

    Expr.raw_skill('items').as_list().map(mapper)
    assert captured_map is not None
    with raises(RuntimeError, match='bound iteration variable'):
        captured_map.value.render()

    # For-each binding escape
    captured_each: Expr[Any] | None = None

    def eacher(item: Expr[Any]) -> Expr[Any]:
        nonlocal captured_each
        captured_each = item
        return Expr.call('print', item)

    Expr.raw_skill('items').as_list().for_each(eacher)
    assert captured_each is not None
    with raises(RuntimeError, match='bound iteration variable'):
        captured_each.render()


def test_expr_encodes_values_once() -> None:
    binary_value = EncodedOnce()
    call_value = EncodedOnce()
    binary_expr = Expr.raw_skill('left') + binary_value
    call_expr = Expr.raw_skill('left') % call_value

    assert binary_value.calls == 1
    assert call_value.calls == 1
    assert binary_expr.render() == '(left + encodedValue)'
    assert binary_expr.render() == '(left + encodedValue)'
    assert call_expr.render() == 'mod(left encodedValue)'
    assert call_expr.render() == 'mod(left encodedValue)'
    assert binary_value.calls == 1
    assert call_value.calls == 1


def test_expr_comparisons_and_arithmetic() -> None:
    value = Expr.raw_skill('value')

    operations: list[tuple[Expr[Any], str]] = [
        (value != 1, '(value != 1)'),
        (value < 1, '(value < 1)'),
        (value <= 1, '(value <= 1)'),
        (value > 1, '(value > 1)'),
        (value >= 1, '(value >= 1)'),
        (value - 1, '(value - 1)'),
        (value * 2, '(value * 2)'),
        (value / 2, '(value / 2)'),
    ]

    for expr, expected in operations:
        assert expr.render() == expected


def test_expr_renders_reflected_unary_and_extended_operations() -> None:
    value = Expr.raw_skill('value')
    condition = value > 0

    operations: list[tuple[Expr[Any], str]] = [
        (2 + value, '(2 + value)'),
        (2 - value, '(2 - value)'),
        (2 * value, '(2 * value)'),
        (2 / value, '(2 / value)'),
        (True & condition, 'and(t (value > 0))'),
        (False | condition, 'or(nil (value > 0))'),
        (-value, 'minus(value)'),
        (~condition, 'not((value > 0))'),
        (value**2, '(value ** 2)'),
        (2**value, '(2 ** value)'),
        (value % 2, 'mod(value 2)'),
        (2 % value, 'mod(2 value)'),
    ]

    for expr, expected in operations:
        assert expr.render() == expected
