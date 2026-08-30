# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from typing import Any

from .channel import Channel
from .expr import Expr
from .hints import SkillCode
from .translator import Translator, snake_to_camel

# Remote: cadence skill runtime
# Local: python daemon thread


class GlobalVar:
    __slots__ = '_channel', '_translator', 'name'

    def __init__(self, name: str, channel: Channel, translator: Translator) -> None:
        self.name = name
        self._channel = channel
        self._translator = translator

    def read(self) -> Any:
        """Fetch from remote.

        Returns:
            Decoded Python value.
        """
        response = self._channel.send(snake_to_camel(self.name))
        return self._translator.decode(response)

    def __call__(self) -> Any:
        return self.read()

    def __str__(self) -> str:
        return f"Global({self.name})"

    def __repr__(self) -> str:
        return f"Global({self.name})"

    def write(self, value: Any) -> None:
        """Push to remote."""
        code = self._translator.encode_assign(self.name, value)
        response = self._channel.send(code)
        assert self._translator.decode(response) is None

    def __lshift__(self, value: Any) -> None:
        self.write(value)

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(snake_to_camel(self.name))

    def expr(self) -> Expr[Any]:
        return Expr.wrap(self)


def is_variable_name(string: str) -> bool:
    return not string.startswith('_') and string.isidentifier()


class Globals:
    def __init__(self, channel: Channel, translator: Translator, prefix: str) -> None:
        self._channel = channel
        self._translator = translator
        self._prefix = prefix + '_'

    def __repr__(self) -> str:
        return f"Globals(prefix={self._prefix})"

    def __getitem__(self, item: str | tuple[str, ...]) -> GlobalVar:
        if isinstance(item, tuple):
            item = '_'.join(item)

        if is_variable_name(item):
            return GlobalVar(self._prefix + item, self._channel, self._translator)

        raise AttributeError(item)

    def __setitem__(self, item: str | tuple[str, ...], value: Any) -> None:
        if isinstance(item, tuple):
            item = '_'.join(item)

        if not is_variable_name(item):
            super().__setattr__(item, value)
            return

        self[item].write(value)

    def __delitem__(self, item: str) -> None:
        self[item] = None

    def __getattr__(self, item: str) -> GlobalVar:
        return self[item]

    def __delattr__(self, item: str) -> None:
        del self[item]


class DirectGlobals:
    def __init__(self, channel: Channel, translator: Translator) -> None:
        self._channel = channel
        self._translator = translator

    def __getattr__(self, name: str) -> Any:
        code = self._translator.encode_read_variable(name)
        response = self._channel.send(code)
        return self._translator.decode(response)

    def __getitem__(self, name: str) -> Any:
        response = self._channel.send(name)
        return self._translator.decode(response)
