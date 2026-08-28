# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple, NewType

if TYPE_CHECKING:  # pragma: no cover
    from typing import TypeAlias

    from typing_extensions import Protocol
else:

    class Protocol:
        pass


__all__ = [
    'Function',
    'Key',
    'Number',
    'Skill',
    'SkillCode',
    'SkillComponent',
    'SupportsReprSkill',
    'Symbol',
]

Number = int | float
SkillComponent = int | str
SkillCode = NewType('SkillCode', str)


class Function(NamedTuple):
    name: str
    description: str
    aliases: set[str]


class SupportsReprSkill(Protocol):
    def __repr_skill__(self) -> SkillCode:  # pragma: no cover
        ...


if TYPE_CHECKING:  # pragma: no cover
    Skill: TypeAlias = (
        SupportsReprSkill
        | Number
        | str
        | bool
        | list['Skill']
        | tuple['Skill', ...]
        | dict[str, 'Skill']
        | None
    )

else:
    Skill = Any


class Symbol(NamedTuple):
    name: str

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(f"'{self.name}")

    def __str__(self) -> str:
        return f"Symbol({self.name})"

    def __repr__(self) -> str:
        return f"Symbol({self.name!r})"


class Key(NamedTuple):
    name: str

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(f"?{self.name}")

    def __str__(self) -> str:
        return f"Key({self.name})"

    def __repr__(self) -> str:
        return f"Key({self.name})"
