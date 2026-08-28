# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import (
    Any,
    cast,
)

from .hints import Skill, SkillCode, Symbol
from .remote import RemoteVariable, remote_variable_attributes
from .translator import ParseError, snake_to_camel


def is_jupyter_magic(attribute: str) -> bool:
    ignore = {
        '_ipython_canary_method_should_not_exist_',
        '_ipython_display_',
        '_repr_mimebundle_',
        '_repr_html_',
        '_repr_markdown_',
        '_repr_svg_',
        '_repr_png_',
        '_repr_pdf_',
        '_repr_jpeg_',
        '_repr_latex_',
        '_repr_json_',
        '_repr_javascript_',
        '_rapped',
        '__wrapped__',
        '__call__',
    }
    return attribute in ignore


class WithAttributeAccess(RemoteVariable):
    def __getattr__(self, key: str) -> Any:
        if key == 'lazy' or is_jupyter_magic(key):
            raise AttributeError(key)

        result = self._send(self._translator.encode_getattr(self._variable, key))
        return self._translator.decode(result)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in remote_variable_attributes:
            return super().__setattr__(key, value)

        result = self._send(self._translator.encode_setattr(self._variable, key, value))
        self._translator.decode(result)
        return None

    def __dir__(self) -> Iterable[str]:
        if self._is_open_file():
            return super().__dir__()

        response = self._send(self._translator.encode_dir(self._variable))
        return self._translator.decode_dir(response)

    def _send(self, command: SkillCode) -> Any:
        return self._channel.send(command).strip()

    def _is_open_file(self) -> bool:
        return False


class RemoteObject(WithAttributeAccess, RemoteVariable):
    @property
    def skill_id(self) -> int:
        address = self._variable[5:].rsplit('_', maxsplit=1)[1]
        try:
            return int(address, 0)
        except ValueError:
            if address.startswith('0x0x'):  # some skill objects have two '0x' in their name
                address = address[2:]
            return int(address, 16)

    @property
    def skill_parent_type(self) -> str:
        return self._variable[5:].rsplit('_', maxsplit=1)[0]

    def _is_open_file(self) -> bool:
        return self._variable.startswith('__py_openfile_')

    @property
    def skill_type(self) -> str | None:
        if self._is_open_file():
            return 'open_file'

        try:
            typ = self.obj_type
        except RuntimeError:
            return None
        if typ is None:
            return None
        if isinstance(typ, Symbol):
            return typ.name[2:-4]
        return cast('str', typ)

    def __str__(self) -> str:
        typ = self.skill_type or self.skill_parent_type
        if typ == 'open_file':
            name = self._call('lsprintf', '%s', self)
            assert isinstance(name, str)
            return f"<remote open_file {name[6:-1]!r}>"
        return f"<remote {typ}@{hex(self.skill_id)}>"

    def __repr__(self) -> str:
        return f"<remote object@{hex(self.skill_id)}>"

    def __getitem__(self, item: str) -> Any:
        result = self._send(self._translator.encode_getattr(self._variable, item, lambda x: x))
        return self._translator.decode(result)

    def __setitem__(self, key: str, value: Any) -> None:
        result = self._send(
            self._translator.encode_setattr(self._variable, key, value, lambda x: x),
        )
        self._translator.decode(result)

    def getdoc(self) -> str:
        return "Properties:\n- " + '\n- '.join(dir(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RemoteObject):
            return self._variable == other._variable
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, RemoteObject):
            return self._variable != other._variable
        return NotImplemented

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._call('funcall', self, *args, **kwargs)


class RemoteCollection(RemoteVariable):
    def __str__(self) -> str:
        kind = type(self).__name__.removeprefix('Remote').lower()
        return f'<remote {kind}>'

    def __bool__(self) -> bool:
        raise TypeError('Remote collections have no implicit truth value; use length()')

    def length(self) -> int:
        return cast('int', self._call('length', self))

    def __getitem__(self, item: Skill) -> Skill:
        return self._call('arrayref', self, item)

    def __setitem__(self, key: Skill, value: Skill) -> None:
        self._call('setarray', self, key, value)

    def __delitem__(self, item: Skill) -> None:
        self._call('remove', item, self)


class RemoteTable(RemoteCollection):
    def __getitem__(self, item: Skill) -> Skill:
        try:
            return super().__getitem__(item)
        except ParseError:
            raise KeyError(item) from None

    def __getattr__(self, item: str) -> Skill:
        if is_jupyter_magic(item):
            raise AttributeError(item)
        return self[Symbol(snake_to_camel(item))]

    def __setattr__(self, key: str, value: Skill) -> None:
        if key in remote_variable_attributes:
            super().__setattr__(key, value)
        else:
            self[Symbol(snake_to_camel(key))] = value

    def __iter__(self) -> Iterator[Skill]:
        return (key for key, _value in self.snapshot())

    def __contains__(self, item: Skill) -> bool:
        return self._find(item) is not None

    def get(self, item: Skill, default: Skill = None) -> Skill:
        result = self._find(item)
        return default if result is None else result[1]

    def snapshot(self) -> list[tuple[Skill, Skill]]:
        table = self.__repr_skill__()
        code = SkillCode(
            f'mapcar(lambda((_entry) list(t car(_entry) cadr(_entry))) tableToList({table}))',
        )
        entries = cast(
            'list[list[Skill]] | None',
            self._translator.decode(self._channel.send(code)),
        )
        return [] if entries is None else [(entry[1], entry[2]) for entry in entries]

    def _find(self, item: Skill) -> list[Skill] | None:
        key = self._translator.encode(item)
        table = self.__repr_skill__()
        code = SkillCode(
            f'let(((_key {key})) '
            f'if(exists(_item {table} equal(_item _key)) list(t {table}[_key]) nil))',
        )
        result = self._channel.send(code)
        return cast('list[Skill] | None', self._translator.decode(result))


class RemoteVector(RemoteCollection, WithAttributeAccess):
    def __getitem__(self, item: Skill) -> Skill:
        try:
            return super().__getitem__(item)
        except RuntimeError as e:
            if "array index out of bounds" in str(e):
                raise IndexError(
                    f"list index {item} out of range (len={self.length()})",
                ) from None
            raise  # pragma: no cover
        except ParseError:
            raise IndexError(f"list index {item} out of range (len={self.length()})") from None

    def __setitem__(self, item: Skill, value: Skill) -> None:
        try:
            super().__setitem__(item, value)
        except RuntimeError as e:
            if "array index out of bounds" in str(e):
                raise IndexError(
                    f"list index {item} out of range (len={self.length()})",
                ) from None
            raise  # pragma: no cover
