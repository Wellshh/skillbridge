# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Iterable
from functools import partial
from importlib.resources import as_file, files
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING, Literal, TypedDict, cast

from typing_extensions import override

import allegrobridge.server
from allegrobridge.client.base import SkillModule
from allegrobridge.client.base._rpc import _core_procedures
from allegrobridge.exceptions import AllegroLaunchError, ExtensionError
from allegrobridge.util import extract_api_domains
from skillbridge.client.channel import Channel
from skillbridge.client.expr import Expr
from skillbridge.client.functions import FunctionCollection
from skillbridge.client.hints import Skill, SkillCode, Symbol
from skillbridge.client.objects import RemoteObject, RemoteTable, RemoteVector
from skillbridge.client.workspace import Workspace as GWorkspace
from skillbridge.client.workspace import WorkspaceId

from .translator import Translator

if TYPE_CHECKING:
    from ._axl_stubs import _WorkspaceTypingMixin
else:

    class _WorkspaceTypingMixin:
        pass


_TRANSACTION_FUNCTIONS = (
    '__abRunTransaction',
    '__abRunSavepointBatch',
    '__abRunDryTransaction',
)


class Workspace(_WorkspaceTypingMixin, GWorkspace):  # type: ignore[misc]
    # GWorkspace treats class annotations as FunctionCollection namespaces.

    def __init__(
        self,
        channel: Channel,
        id_: WorkspaceId,
    ) -> None:
        super().__init__(channel, id_)
        self._transaction = Txn(self)
        self._module_lock = Lock()
        self._loaded_modules: set[SkillModule] = set()
        self._module_errors: dict[SkillModule, ExtensionError] = {}

    @property
    def transaction(self) -> Txn:
        return self._transaction

    @override
    def _prepare_default_translator(self) -> Translator:
        translator = Translator()
        types = [('Remote', RemoteObject), ('Table', RemoteTable), ('Vector', RemoteVector)]

        for name, typ in types:
            construct = partial(typ, self._channel, translator)
            translator.register_remote_variable_type(name, construct)

        return translator

    @classmethod
    @override
    def _create_workspace(cls, channel: Channel, workspace_id: WorkspaceId) -> GWorkspace:
        is_allegro = channel.send("isCallable('axlDBGetDesign)") == "True"
        if not is_allegro:
            return GWorkspace(channel, workspace_id)

        workspace = cls(channel, workspace_id)
        try:
            workspace._ensure_core_runtime()
        except BaseException:
            workspace.close(log_exception=False)
            raise
        return workspace

    @classmethod
    @override
    def open(
        cls,
        workspace_id: WorkspaceId = None,
        direct: bool = False,
        *,
        force_tcp: bool = False,
    ) -> GWorkspace:
        return super().open(workspace_id, direct, force_tcp=force_tcp)

    def _has_procedures(self, procedures: tuple[str, ...]) -> bool:
        return all(self['isCallable'](Symbol(name)) for name in procedures)

    def _ensure_core_runtime(self) -> None:
        procedures = _TRANSACTION_FUNCTIONS + _core_procedures()
        if self._has_procedures(procedures):
            return

        server_file = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
        self['load'](server_file.resolve().as_posix())
        if not self._has_procedures(procedures):
            raise AllegroLaunchError('Allegro core runtime failed to load')

    def _module_is_ready(
        self,
        module: SkillModule,
        procedures: tuple[str, ...],
    ) -> bool:
        if not procedures:
            return True
        checks = (self['isCallable'].expr(Symbol(name)) for name in procedures)
        try:
            return cast('bool', self.eval(Expr.call('and', *checks)))
        except Exception as error:
            raise ExtensionError(f'SKILL module {module!r} readiness check failed') from error

    def _ensure_module(self, module: SkillModule, procedures: tuple[str, ...]) -> None:
        with self._module_lock:
            if module in self._module_errors:
                raise self._module_errors[module]
            if self._module_is_ready(module, procedures):
                return
            if module not in self._loaded_modules:
                try:
                    resource = files(module.package).joinpath(module.resource)
                    if not resource.is_file():
                        raise ExtensionError(  # ruff: ignore[raise-within-try]
                            f'SKILL resource {module.resource!r} was not found '
                            f'in package {module.package!r}'
                        )
                    with as_file(resource) as path:
                        self['load'](path.resolve().as_posix())
                except ExtensionError as error:
                    self._module_errors[module] = error
                    raise
                except Exception as error:
                    failure = ExtensionError(f'failed to load SKILL module {module!r}')
                    self._module_errors[module] = failure
                    raise failure from error
                self._loaded_modules.add(module)
            if not self._module_is_ready(module, procedures):
                raise ExtensionError(f'SKILL module {module!r} failed readiness check')


# Register domain collections as class annotations, excluding 'db' which is inherited
# rough count of axl_* apis in allegro: 792
# The lowercase APIs axlcreate and axldo are callable only through ws['api_name'].
_workspace_members = set(dir(GWorkspace))
Workspace.__annotations__ = {
    domain: FunctionCollection
    for domain in extract_api_domains()
    if (domain.isidentifier() and domain != "root" and domain not in _workspace_members)
}


class Txn:
    def __init__(self, workspace: Workspace) -> None:
        self._workspace = workspace

    def __call__(self, cmd: SkillCode) -> Skill:
        return self._workspace['__abRunTransaction'](cmd)

    def preview(self, cmd: SkillCode) -> Skill:
        return self._workspace['__abRunDryTransaction'](cmd)

    def batch(self, cmds: Iterable[SkillCode]) -> list[SavepointResult]:
        """Execute commands with savepoints, committing successes and rolling back failures.

        Returns:
            List of savepoint execution results.
        """
        commands: list[Skill] = list(cmds)
        if not commands:
            return []
        result = self._workspace['__abRunSavepointBatch'](commands)
        return cast('list[SavepointResult]', result)


class SavepointSuccess(TypedDict):
    index: int
    status: Literal['success']
    value: Skill


class SavepointFailure(TypedDict):
    index: int
    status: Literal['failure']
    error: str


SavepointResult = SavepointSuccess | SavepointFailure
