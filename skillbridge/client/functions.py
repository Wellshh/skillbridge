# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from typing_extensions import Self

from .channel import Channel
from .expr import Expr
from .hints import Key, Skill
from .translator import Translator


def keys(**attrs: Skill) -> list[Skill]:
    return [flat for key, value in attrs.items() for flat in (Key(key), value)]


class FunctionCollection:
    def __init__(self, channel: Channel, prefix: str, translator: Translator) -> None:
        self._channel = channel
        self._translate = translator
        self._prefix = prefix

    def __repr__(self) -> str:
        return f'<function collection {self._prefix}*>'

    def __dir__(self) -> list[str]:
        return sorted({*object.__dir__(self), *self._translate.function_names(self._prefix)})

    def dir(self) -> list[str]:
        code = self._translate.encode_globals(self._prefix)
        result = self._channel.send(code)
        return self._translate.decode_globals(result, self._prefix)

    def __getattr__(self, item: str) -> RemoteFunction:
        if item.startswith('_'):
            raise AttributeError(item)
        return RemoteFunction(self._channel, f'{self._prefix}_{item}', self._translate)


class RemoteFunction:
    def __init__(self, channel: Channel, func: str, translator: Translator) -> None:
        self._channel = channel
        self._translate = translator
        self._function = func

    def __call__(self, *args: Skill, **kwargs: Skill) -> Skill:
        command = self.expr(*args, **kwargs).render()
        result = self._channel.send(command)

        return self._translate.decode(result)

    def _skill_name(self) -> str:
        return self._translate.format_function_name(self._function)

    def expr(self, *args: Skill, **kwargs: Skill) -> Expr[Skill]:
        return Expr.call(self._skill_name(), *args, **kwargs)

    def __repr__(self) -> str:
        return f'<remote function {self._skill_name()}>'

    def help(self) -> str:
        command = self._translate.encode_help(self._skill_name())
        result = self._channel.send(command)
        return self._translate.decode_help(result)

    def __getattr__(self, item: str) -> Self:
        if item.startswith('_') or item in {'lazy', 'var'}:
            raise AttributeError(item)
        return self.__class__(self._channel, f"{self._function}_{item}", self._translate)


class LiteralRemoteFunction(RemoteFunction):
    def _skill_name(self) -> str:
        return self._function
