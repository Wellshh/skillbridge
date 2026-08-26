# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from .channel import Channel
from .hints import Skill, SkillCode
from .translator import Translator

remote_variable_attributes = frozenset(('_channel', '_variable', '_translator'))


class RemoteVariable:
    def __init__(self, channel: Channel, translator: Translator, variable: SkillCode) -> None:
        self._channel = channel
        self._variable = variable
        self._translator = translator

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(self._variable)

    def __repr__(self) -> str:
        return self.__str__()

    def _call(self, function: str, *args: Skill, **kwargs: Skill) -> Skill:
        code = self._translator.encode_call(function, *args, **kwargs)
        result = self._channel.send(code)
        return self._translator.decode(result)
