# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from ast import AST, Call, Constant, Dict, List, Name, UAdd, UnaryOp, USub, parse
from collections.abc import Callable, Iterable
from json import dumps, loads
from logging import getLogger
from re import Match, findall, sub
from typing import Any, NoReturn, cast
from warnings import warn_explicit

from .hints import Skill, SkillCode, Symbol

_logger = getLogger("allegrobridge.cadence")


class ParseError(Exception):
    pass


def _raise_error(message: str) -> NoReturn:
    raise ParseError(message)


def _show_warning(message: str, result: Any) -> Any:
    for i, line in enumerate(message.splitlines(keepends=False)):
        # redirected logs from skill server
        clean = line.strip()
        if not clean or clean == "*WARNING*":
            continue
        if clean.startswith("*WARNING*"):
            clean = clean[9:].lstrip()
            _logger.warning(clean)
        else:
            _logger.info(clean)
        warn_explicit(clean, UserWarning, "Skill response", i)
    return result


_STATIC_EVAL_CONTEXT: dict[str, Any] = {
    'Symbol': Symbol,
    'error': _raise_error,
    'warning': _show_warning,
}


def _eval(node: AST, context: dict[str, Any]) -> Any:  # ruff: ignore[complex-structure, too-many-branches]
    """Safely evaluate responses from skill server."""
    match node:
        case Constant(value=value):
            if value is None or type(value) in {bool, float, int, str}:
                return value
            raise ParseError(f'Unsupported constant: {type(value).__name__}')
        case List(elts=elements):
            return [_eval(element, context) for element in elements]
        case Dict(keys=keys, values=values):
            result: dict[str, Any] = {}
            for key_node, value_node in zip(keys, values, strict=True):
                if key_node is None:
                    raise ParseError('Dictionary unpacking is not supported')
                key = _eval(key_node, context)
                if not isinstance(key, str):
                    raise ParseError('Dictionary keys must be strings')
                result[key] = _eval(value_node, context)
            return result
        case UnaryOp(op=USub() | UAdd() as op, operand=operand):
            if not isinstance(operand, Constant) or type(operand.value) not in {float, int}:
                raise ParseError('Signed values must be numeric constants')
            value = cast('int | float', operand.value)
            return -value if isinstance(op, USub) else +value
        case Call(func=func, args=args, keywords=keywords):
            if not isinstance(func, Name) or keywords:
                raise ParseError('Only positional calls to registered functions are supported')
            try:
                function = context[func.id]
            except KeyError:
                raise ParseError(f'Unknown function: {func.id}') from None
            return function(*(_eval(argument, context) for argument in args))
        case _:
            raise ParseError(f'Unsupported response expression: {type(node).__name__}')


def _skill_value_to_python(string: str, eval_context: dict[str, Any] | None = None) -> Skill:
    context = _STATIC_EVAL_CONTEXT if eval_context is None else eval_context
    try:
        expression = parse(string, mode='eval')
    except SyntaxError as error:
        raise ParseError(str(error)) from None
    return cast('Skill', _eval(expression.body, context))


def _upper_without_first(match: Match[str]) -> str:
    return match.group()[1:].upper()


def snake_to_camel(snake: str) -> str:
    if snake.startswith('_') or '_' not in snake:
        return snake
    return sub(r'_[a-zA-Z]', _upper_without_first, snake)


def camel_to_snake(camel: str) -> str:
    if camel[0].isupper():
        return camel
    parts = findall(r"[a-z0-9]+|[A-Z][a-z0-9]+|[A-Z]+(?=[A-Z_][a-z]|$)", camel)
    return '_'.join(
        part.lower() if not part[-1].isupper() or len(part) == 1 else part for part in parts
    )


def python_value_to_skill(value: Skill) -> SkillCode:
    repr_skill = getattr(type(value), '__repr_skill__', None)
    if repr_skill is not None:
        return cast('SkillCode', repr_skill(value))

    if isinstance(value, dict):
        items = ' '.join(f"'{key} {python_value_to_skill(value)}" for key, value in value.items())
        return SkillCode(f'list(nil {items})')

    if value is False or value is None:
        return SkillCode('nil')

    if value is True:
        return SkillCode('t')

    if isinstance(value, (int, float, str)):
        return SkillCode(dumps(value))

    if isinstance(value, (list, tuple)):
        inner = ' '.join(python_value_to_skill(item) for item in value)
        return SkillCode(f'(list {inner})')

    type_ = type(value).__name__
    raise RuntimeError(f"Cannot convert object {type_!r} to skill.") from None


CaseSwitcher = Callable[[str], str]


def build_skill_path(
    components: Iterable[str | int],
    case_switcher: CaseSwitcher = snake_to_camel,
) -> SkillCode:
    it = iter(components)
    path = case_switcher(str(next(it)))

    for component in it:
        if isinstance(component, int):
            path = f'(nth {component} {path})'
        else:
            path = f'{path}->{case_switcher(component)}'

    return SkillCode(path)


def build_python_path(components: Iterable[str | int]) -> SkillCode:
    it = iter(components)
    path = str(next(it))

    for component in it:
        path = f"{path}[{component}]" if isinstance(component, int) else f"{path}.{component}"

    return SkillCode(path)


class Translator:
    @staticmethod
    def format_function_name(name: str) -> str:
        return snake_to_camel(name)

    @staticmethod
    def function_names(_prefix: str) -> tuple[str, ...]:
        return ()

    @staticmethod
    def encode_dir(obj: SkillCode) -> SkillCode:
        parts = ' '.join(
            (
                f'{obj}->?',
                f"if( type({obj}) == 'rodObj then {obj}->systemHandleNames)",
                f'if( type({obj}) == \'rodObj then {obj}->userHandleNames)',
            ),
        )
        code = f'mapcar(lambda((attr) sprintf(nil "%s" attr)) nconc({parts}))'
        return SkillCode(code)

    @staticmethod
    def decode_dir(code: str) -> list[str]:
        attributes = _skill_value_to_python(code) or ()
        return [camel_to_snake(attr) for attr in cast('list[str]', attributes)]

    @staticmethod
    def encode_getattr(
        obj: SkillCode,
        key: str,
        case_switcher: CaseSwitcher = snake_to_camel,
    ) -> SkillCode:
        return build_skill_path([obj, key], case_switcher)

    @staticmethod
    def encode_globals(prefix: str) -> SkillCode:
        return SkillCode(f'buildString(listFunctions("^{prefix}[A-Z]"))')

    @staticmethod
    def encode_read_variable(name: str) -> SkillCode:
        return SkillCode(snake_to_camel(name))

    def encode_assign(self, variable: str, value: Any) -> SkillCode:
        encoded_value = self.encode(value)
        return SkillCode(f'{snake_to_camel(variable)} = {encoded_value} nil')

    @staticmethod
    def decode_globals(code: str, prefix: str) -> list[str]:
        stem = f'{camel_to_snake(prefix)}_'
        return [camel_to_snake(function).removeprefix(stem) for function in loads(code).split()]

    @staticmethod
    def encode_help(symbol: str) -> SkillCode:
        code = f"""
            _text = outstring()
            poport = _text help({snake_to_camel(symbol)})
            poport = stdout getOutstring(_text)
        """.replace(
            "\n",
            " ",
        )
        return SkillCode(code)

    @staticmethod
    def decode_help(help_: str) -> str:
        info = loads(help_)
        assert isinstance(info, str)
        return info

    @staticmethod
    def encode_setattr(
        obj: SkillCode,
        key: str,
        value: Any,
        case_switcher: CaseSwitcher = snake_to_camel,
    ) -> SkillCode:
        code = build_skill_path([obj, key], case_switcher)
        value = python_value_to_skill(value)
        return SkillCode(f'{code} = {value}')

    def encode(self, value: Skill) -> SkillCode:
        raise NotImplementedError

    def decode(self, code: str) -> Skill:
        raise NotImplementedError


class DefaultTranslator(Translator):
    def __init__(self) -> None:
        self.context: dict[str, Any] = _STATIC_EVAL_CONTEXT.copy()

    def register_remote_variable_type(self, name: str, constructor: Callable[[str], Skill]) -> None:
        self.context[name] = constructor

    def encode(self, value: Skill) -> SkillCode:
        return python_value_to_skill(value)

    def decode(self, code: str) -> Skill:
        return _skill_value_to_python(code, self.context)
