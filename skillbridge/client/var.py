# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .hints import SkillCode
from .translator import DefaultTranslator, python_value_to_skill, snake_to_camel


@dataclass(frozen=True)
class Var:
    """Build a lazy SKILL expression."""

    _expression: str

    def __bool__(self) -> bool:
        raise TypeError('a Var expression has no local truth value')

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(self._expression)

    def __str__(self) -> str:
        return f"Var({self._expression})"

    def __repr__(self) -> str:
        return f"Var({self._expression!r})"

    def __getattr__(self, item: str) -> Var:
        return Var(f'{self._expression}->{snake_to_camel(item)}')

    def __getitem__(self, item: str | int) -> Var:
        if isinstance(item, str):
            return Var(f'{self._expression}->{item}')
        return Var(f'nth({item} {self._expression})')

    def _infix(self, other: Any, op: str) -> Var:
        return Var(f'({self._expression} {op} {python_value_to_skill(other)})')

    def __eq__(self, other: object) -> Var:  # type: ignore[override]
        return self._infix(other, '==')

    def __ne__(self, other: object) -> Var:  # type: ignore[override]
        return self._infix(other, '!=')

    def __lt__(self, other: Any) -> Var:
        return self._infix(other, '<')

    def __le__(self, other: Any) -> Var:
        return self._infix(other, '<=')

    def __gt__(self, other: Any) -> Var:
        return self._infix(other, '>')

    def __ge__(self, other: Any) -> Var:
        return self._infix(other, '>=')

    def __add__(self, other: Any) -> Var:
        return self._infix(other, '+')

    def __sub__(self, other: Any) -> Var:
        return self._infix(other, '-')

    def __mul__(self, other: Any) -> Var:
        return self._infix(other, '*')

    def __truediv__(self, other: Any) -> Var:
        return self._infix(other, '/')

    def __and__(self, other: Any) -> Var:
        return Var(DefaultTranslator.encode_call('and', self, other))

    def __or__(self, other: Any) -> Var:
        return Var(DefaultTranslator.encode_call('or', self, other))
