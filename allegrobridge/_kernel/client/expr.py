# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeVar, overload

from .hints import Skill, SkillCode
from .translator import python_value_to_skill, snake_to_camel

T = TypeVar('T')
U = TypeVar('U')
S = TypeVar('S', bound=Skill)


@dataclass(frozen=True, slots=True)
class _Raw:
    source: SkillCode


@dataclass(frozen=True, slots=True)
class _Constant:
    source: SkillCode


@dataclass(frozen=True, slots=True)
class _Attribute:
    owner: _Node
    name: str
    operator: str = '->'


@dataclass(frozen=True, slots=True)
class _Subscript:
    owner: _Node
    index: int


@dataclass(frozen=True, slots=True)
class _BinOp:
    left: _Node
    operator: str
    right: _Node


@dataclass(frozen=True, slots=True)
class _Call:
    """AST node rendered as SKILL function call."""

    name: str
    arguments: tuple[_Node, ...]
    keywords: tuple[tuple[str, _Node], ...] = ()


@dataclass(frozen=True, slots=True, eq=False)
class _Bound:
    pass


@dataclass(frozen=True, slots=True)
class _Bind:
    """AST node rendered as SKILL setof, mapcar, or foreach according to kind.

    Attributes:
        kind: The collection operation to render.
        variable: The placeholder variable bound to each element during iteration.
        values: The collection/iterable AST node being processed.
        predicate: The condition, transformed value, or operation body for each element.
    """

    kind: Literal['where', 'map', 'for_each']
    variable: _Bound
    values: _Node
    predicate: _Node


_Node = _Raw | _Constant | _Attribute | _Subscript | _BinOp | _Call | _Bound | _Bind


@dataclass(slots=True)
class _Context:
    """Compilation context tracking active variable bindings and variable names,
    e.g. expr.where() -> skill: setof projection.
    Attributes:
        _bindings: A local symbol table, CANNOT ACCESSED OUT OF SCOPE.
        Mapping from AST bound placeholder nodes to SKILL variable names.

        pointer: Monotonically increasing counter to allocate unique SKILL variable names.
    """

    _bindings: dict[_Bound, str]
    pointer: int = 0

    def get(self, bound: _Bound) -> str | None:
        return self._bindings.get(bound)

    def bind(self, bound: _Bound, name: str) -> None:
        self._bindings[bound] = name

    def unbind(self, bound: _Bound) -> None:
        del self._bindings[bound]

    def next_variable(self) -> str:
        variable = f'_expr{self.pointer}'
        self.pointer += 1
        return variable


def _render(node: _Node, context: _Context | None = None) -> SkillCode:  # ruff: ignore[complex-structure, too-many-locals]
    """Recursively compiles an AST expression node into valid SKILL code.

    Args:
        node: The AST node to render.
        context: The compilation context tracking active bindings and pointer.

    Returns:
        The formatted SKILL code representation.

    Example:
        >>> attr_node = _Attribute(_Raw(SkillCode('design')), 'width')
        >>> _render(attr_node)
        'design->width'
        >>> bin_node = _BinOp(attr_node, '>', _Constant(SkillCode('10')))
        >>> _render(bin_node)
        '(design->width > 10)'
    """
    if context is None:
        context = _Context({})

    match node:
        case _Bound():
            variable = context.get(node)
            if variable is None:
                raise RuntimeError(
                    'bound iteration variable cannot be rendered '
                    'outside its enclosing operation (where/map/for_each)'
                )
            return SkillCode(variable)
        case _Raw(source) | _Constant(source):
            return source
        case _Attribute(owner, name, operator):
            return SkillCode(f'{_render(owner, context)}{operator}{name}')
        case _Subscript(owner, index):
            return SkillCode(f'nth({index} {_render(owner, context)})')
        case _Call(name, arguments, keywords):
            args: list[str] = [_render(argument, context) for argument in arguments]
            args.extend(f'?{k} {_render(v, context)}' for k, v in keywords)
            return SkillCode(f'{name}({" ".join(args)})')
        case _Bind(kind, variable, values, predicate):
            var_name = context.next_variable()
            rendered_values = _render(values, context)
            context.bind(variable, var_name)
            rendered_predicate = _render(predicate, context)
            context.unbind(variable)
            if kind == 'where':
                return SkillCode(f'setof({var_name} {rendered_values} {rendered_predicate})')
            if kind == 'map':
                return SkillCode(
                    f'mapcar(lambda(({var_name}) {rendered_predicate}) {rendered_values})'
                )
            return SkillCode(
                f'progn(foreach({var_name} {rendered_values} {rendered_predicate}) nil)'
            )
        case _BinOp(left, operator, right):  # pragma: no branch
            return SkillCode(f'({_render(left, context)} {operator} {_render(right, context)})')


@dataclass(frozen=True, slots=True, eq=False)  # ruff: ignore[too-many-public-methods]
class Expr(Generic[T]):
    _node: _Node
    __hash__ = None  # type: ignore[assignment]

    @classmethod
    def raw_skill(cls, source: str) -> Expr[Any]:
        return cls(_Raw(SkillCode(source)))

    @staticmethod
    def wrap(value: S) -> Expr[S]:
        """Lift/box a Python constant into an Expr AST literal."""
        return Expr(_Constant(python_value_to_skill(value)))

    def render(self) -> SkillCode:
        # True -> t, False -> nil, "str" -> "\"str\"", etc.
        return _render(self._node)

    def __repr_skill__(self) -> SkillCode:
        return self.render()

    def __bool__(self) -> bool:
        raise TypeError('an Expr has no local truth value')

    def __getattr__(self, name: str) -> Expr[Any]:
        # same as `is_jupyter_magic()` in `objects.py`
        if name.startswith('_') or not name.isidentifier():
            raise AttributeError(name)
        return Expr(_Attribute(self._node, snake_to_camel(name)))

    def __getitem__(self, item: str) -> Expr[Any]:
        if not isinstance(item, str):
            raise TypeError('integer indices require as_list()')
        if not item.isidentifier():
            raise KeyError(item)
        return Expr(_Attribute(self._node, item))

    def as_list(self) -> ListExpr[T]:
        return ListExpr(self._node)

    @staticmethod
    def _coerce(value: Any) -> _Node:
        match value:
            case Expr(node):
                return node
            case _:
                return _Constant(python_value_to_skill(value))

    def _binary(self, other: Any, operator: str) -> Expr[Any]:
        return Expr(_BinOp(self._node, operator, self._coerce(other)))

    def _reverse_binary(self, other: Any, operator: str) -> Expr[Any]:
        return Expr(_BinOp(self._coerce(other), operator, self._node))

    @staticmethod
    def call(name: str, *arguments: Any, **keywords: Any) -> Expr[Any]:
        return Expr(
            _Call(
                name,
                tuple(Expr._coerce(argument) for argument in arguments),
                tuple(
                    (snake_to_camel(key), Expr._coerce(value)) for key, value in keywords.items()
                ),
            ),
        )

    def __eq__(self, other: object) -> Expr[bool]:  # type: ignore[override]
        return self._binary(other, '==')

    def __ne__(self, other: object) -> Expr[bool]:  # type: ignore[override]
        return self._binary(other, '!=')

    def __lt__(self, other: Any) -> Expr[bool]:
        return self._binary(other, '<')

    def __le__(self, other: Any) -> Expr[bool]:
        return self._binary(other, '<=')

    def __gt__(self, other: Any) -> Expr[bool]:
        return self._binary(other, '>')

    def __ge__(self, other: Any) -> Expr[bool]:
        return self._binary(other, '>=')

    def __add__(self, other: Any) -> Expr[Any]:
        return self._binary(other, '+')

    def __radd__(self, other: Any) -> Expr[Any]:
        return self._reverse_binary(other, '+')

    def __sub__(self, other: Any) -> Expr[Any]:
        return self._binary(other, '-')

    def __rsub__(self, other: Any) -> Expr[Any]:
        return self._reverse_binary(other, '-')

    def __mul__(self, other: Any) -> Expr[Any]:
        return self._binary(other, '*')

    def __rmul__(self, other: Any) -> Expr[Any]:
        return self._reverse_binary(other, '*')

    def __truediv__(self, other: Any) -> Expr[Any]:
        return self._binary(other, '/')

    def __rtruediv__(self, other: Any) -> Expr[Any]:
        return self._reverse_binary(other, '/')

    def __pow__(self, other: Any) -> Expr[Any]:
        return self._binary(other, '**')

    def __rpow__(self, other: Any) -> Expr[Any]:
        return self._reverse_binary(other, '**')

    def __mod__(self, other: Any) -> Expr[Any]:
        return self.call('mod', self, other)

    def __rmod__(self, other: Any) -> Expr[Any]:
        return self.call('mod', other, self)

    def __neg__(self) -> Expr[Any]:
        return self.call('minus', self)

    def __invert__(self) -> Expr[bool]:
        return self.call('not', self)

    def __and__(self, other: Any) -> Expr[Any]:
        return self.call('and', self, other)

    def __rand__(self, other: Any) -> Expr[Any]:
        return self.call('and', other, self)

    def __or__(self, other: Any) -> Expr[Any]:
        return self.call('or', self, other)

    def __ror__(self, other: Any) -> Expr[Any]:
        return self.call('or', other, self)


@dataclass(frozen=True, slots=True, eq=False)
class ListExpr(Expr[list[T] | None], Generic[T]):
    @overload
    def __getitem__(self, item: int) -> Expr[T]: ...

    @overload
    def __getitem__(self, item: str) -> Expr[Any]: ...

    def __getitem__(self, item: str | int) -> Expr[Any]:
        if isinstance(item, str):
            return Expr.__getitem__(self, item)
        if item < 0:
            raise IndexError('negative list indices are not supported')
        return Expr(_Subscript(self._node, item))

    @property
    def each(self) -> ListExpr[Any]:
        return _EachExpr(self._node)

    def _bind(
        self,
        kind: Literal['where', 'map', 'for_each'],
        operation: Callable[[Expr[T]], Any],
    ) -> _Bind:
        variable = _Bound()
        result = operation(Expr(variable))
        return _Bind(kind, variable, self._node, self._coerce(result))

    def where(self, predicate: Callable[[Expr[T]], Expr[Any] | bool]) -> ListExpr[T]:
        return ListExpr(self._bind('where', predicate))

    def map(self, transform: Callable[[Expr[T]], Expr[U] | U]) -> ListExpr[U]:
        return ListExpr(self._bind('map', transform))

    def for_each(self, operation: Callable[[Expr[T]], Expr[Any]]) -> Expr[None]:
        return Expr(self._bind('for_each', operation))


@dataclass(frozen=True, slots=True, eq=False)
class _EachExpr(ListExpr[T]):
    def __getattr__(self, name: str) -> _EachExpr[Any]:
        if name.startswith('_') or not name.isidentifier():
            raise AttributeError(name)
        node = _Attribute(self._node, snake_to_camel(name), '~>')
        return _EachExpr(node)

    @overload
    def __getitem__(self, item: int) -> Expr[T]: ...

    @overload
    def __getitem__(self, item: str) -> _EachExpr[Any]: ...

    def __getitem__(self, item: str | int) -> Expr[Any]:
        if not isinstance(item, str):
            return ListExpr.__getitem__(self, item)
        if not item.isidentifier():
            raise KeyError(item)
        return _EachExpr(_Attribute(self._node, item, '~>'))
