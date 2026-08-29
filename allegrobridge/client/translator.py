# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from json import loads

from typing_extensions import override

from allegrobridge.util import build_snake_to_axl_map
from skillbridge.client.hints import SkillCode
from skillbridge.client.translator import DefaultTranslator as GDefaultTranslator

_SNAKE_TO_AXL = build_snake_to_axl_map()


class Translator(GDefaultTranslator):
    @override
    @staticmethod
    def format_function_name(name: str) -> str:
        return _SNAKE_TO_AXL.get(name, GDefaultTranslator.format_function_name(name))

    @override
    @staticmethod
    def function_names(_prefix: str) -> tuple[str, ...]:
        stem = f'{_prefix}_'
        return tuple(sorted(name[len(stem) :] for name in _SNAKE_TO_AXL if name.startswith(stem)))

    @override
    @staticmethod
    def encode_globals(prefix: str) -> SkillCode:
        if Translator.function_names(prefix):
            prefix = 'axl'
        return GDefaultTranslator.encode_globals(prefix)

    @override
    @staticmethod
    def decode_globals(code: str, prefix: str) -> list[str]:
        names = Translator.function_names(prefix)
        if not names:
            return GDefaultTranslator.decode_globals(code, prefix)
        aliases = {_SNAKE_TO_AXL[f'{prefix}_{name}']: name for name in names}
        return [aliases[function] for function in loads(code).split() if function in aliases]
