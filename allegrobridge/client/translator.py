from __future__ import annotations

from skillbridge.client.translator import Translator as GTranslator

# Hardcode the non-regular function prefix pattern in allegro axl_* apis
_THREE_LETTER_ACRONYMS = {"drc", "cns", "grp", "cvf", "wfm", "uiw"}
_ACRONYM_LEN = 2


class Translator(GTranslator):
    @staticmethod
    def format_function_name(snake: str) -> str:
        if "_" not in snake and snake.startswith("axl"):
            return snake

        parts = snake.split("_")

        if parts[0].lower() != "axl":
            parts.insert(0, "axl")

        fmt_parts = []
        for i, part in enumerate(parts):
            if i == 0:
                fmt_parts.append(part.lower())  # start with 'axl'
            elif len(part) == _ACRONYM_LEN or part.lower() in _THREE_LETTER_ACRONYMS:
                fmt_parts.append(part.upper())  # 'db' -> 'DB', 'ui' -> 'UI', 'drc' -> 'DRC'
            else:
                fmt_parts.append(part.capitalize())  # 'geo' -> 'Geo', 'form' -> 'Form'

        return "".join(fmt_parts)
