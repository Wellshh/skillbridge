# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from importlib import import_module
from threading import Lock
from types import ModuleType
from typing import TYPE_CHECKING, TypeVar

from allegrobridge.exceptions import ExtensionError

from ._rpc import SessionApi, _api_procedures

if TYPE_CHECKING:
    from allegrobridge.client.session.session import Session

ApiT = TypeVar('ApiT', bound=SessionApi)


# Extension Development Specification:
# 1. Location: Create `allegrobridge/client/api/extensions/<name>.py` (lowercase identifier).
# 2. Implementation: Subclass `SessionApi` and mark the class with `@extension`.
# 3. Constraint: Exactly one `@extension` class per extension module.
# 4. Usage: Access via `session.ext.<name>` (lazily imported, cached, and bound to Session).
_PACKAGE = 'allegrobridge.client.api.extensions'
_MARKER = '__session_extension__'


def extension(api: type[ApiT]) -> type[ApiT]:
    """Mark an API class as a session extension.
    Avoid corner cases: inner imported extension in extension class."""
    setattr(api, _MARKER, True)
    return api


class _Extensions:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._cache: dict[str, SessionApi] = {}
        self._errors: dict[str, ExtensionError] = {}
        self._lock = Lock()

    def __getattr__(self, name: str) -> SessionApi:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __getitem__(self, name: str) -> SessionApi:
        if not name.isidentifier() or name.lower() != name:
            raise KeyError(name)
        with self._lock:
            if name in self._cache:
                return self._cache[name]
            if name in self._errors:
                raise self._errors[name]
            try:
                ext = self._load(name)
            except ExtensionError as error:
                self._errors[name] = error
                raise
            self._cache[name] = ext
            return ext

    def _load(self, name: str) -> SessionApi:
        module_name = f'{_PACKAGE}.{name}'
        try:
            module = import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name == module_name:
                raise KeyError(name) from None
            raise ExtensionError(f'failed to import extension {name!r}') from error
        except Exception as error:
            raise ExtensionError(f'failed to import extension {name!r}') from error

        api = self._extension_class(module)
        procedures = _api_procedures(api)
        if procedures:
            self._session.raw._ensure_extension(  # ruff: ignore[private-member-access]
                name,
                procedures,
            )
        return api(self._session)

    @staticmethod
    def _extension_class(module: ModuleType) -> type[SessionApi]:
        candidates = [
            value
            for value in vars(module).values()
            if isinstance(value, type)
            and issubclass(value, SessionApi)
            and value.__module__ == module.__name__  # one module could only define one extension
            and value.__dict__.get(_MARKER, False)
        ]
        if len(candidates) != 1:
            name = module.__name__.rsplit('.', 1)[-1]
            raise ExtensionError(f'extension {name!r} must declare exactly one API class')
        return candidates[0]
