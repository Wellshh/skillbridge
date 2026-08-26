# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from typing import Any, NamedTuple, cast

from ..client.hints import Skill, SkillCode
from ..client.translator import Translator


class FunctionCall(NamedTuple):
    name: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


class PassTranslator(Translator):
    def encode(self, value: Skill) -> SkillCode:
        return value  # type: ignore[return-value]

    def decode(self, code: str) -> Skill:
        return code

    @staticmethod
    def encode_call(func_name: str, *args: Skill, **kwargs: Skill) -> SkillCode:
        return cast("SkillCode", FunctionCall(func_name, args, kwargs))
