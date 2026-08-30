# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from allegrobridge._kernel.client.hints import Skill, SkillCode
from allegrobridge._kernel.client.translator import Translator


class PassTranslator(Translator):
    def encode(self, value: Skill) -> SkillCode:
        return value  # type: ignore[return-value]

    def decode(self, code: str) -> Skill:
        return code
