# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from typing_extensions import Self

from .channel import Channel
from .expr import Expr
from .hints import Skill, SkillCode
from .translator import Translator

remote_variable_attributes = frozenset(('_channel', '_variable', '_translator', '_epoch'))


class RemoteVariable:
    def __init__(self, channel: Channel, translator: Translator, variable: SkillCode) -> None:
        self._channel = channel
        self._variable = variable
        self._translator = translator

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(self._variable)

    def expr(self) -> Expr[Self]:
        return Expr.wrap(self)

    def __repr__(self) -> str:
        return self.__str__()

    def _call(self, function: str, *args: Skill, **kwargs: Skill) -> Skill:
        code = Expr.call(function, *args, **kwargs).render()
        result = self._channel.send(code)
        return self._translator.decode(result)
