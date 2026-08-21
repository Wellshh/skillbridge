from __future__ import annotations

from allegrobridge.util import build_snake_to_axl_map
from skillbridge.client.translator import Translator as GTranslator

_SNAKE_TO_AXL = build_snake_to_axl_map()


class Translator(GTranslator):
    @staticmethod
    def format_function_name(name: str) -> str:
        return _SNAKE_TO_AXL.get(name, GTranslator.format_function_name(name))
