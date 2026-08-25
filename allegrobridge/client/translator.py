from __future__ import annotations

from typing_extensions import override

from allegrobridge.util import build_snake_to_axl_map
from skillbridge.client.translator import DefaultTranslator as GDefaultTranslator

_SNAKE_TO_AXL = build_snake_to_axl_map()


class Translator(GDefaultTranslator):
    @override
    @staticmethod
    def format_function_name(name: str) -> str:
        return _SNAKE_TO_AXL.get(name, GDefaultTranslator.format_function_name(name))
