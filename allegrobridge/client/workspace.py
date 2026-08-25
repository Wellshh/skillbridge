from __future__ import annotations

from collections.abc import Iterable
from functools import partial
from pathlib import Path
from threading import Lock
from typing import Literal, TypedDict, Union, cast

from typing_extensions import override

import allegrobridge.server
from allegrobridge.client.api._rpc import _core_procedures
from allegrobridge.exceptions import AllegroLaunchError, ExtensionError
from allegrobridge.util import extract_api_domains
from skillbridge.client.channel import Channel
from skillbridge.client.functions import FunctionCollection
from skillbridge.client.hints import Skill, SkillCode, SkillList, Symbol
from skillbridge.client.objects import RemoteObject, RemoteTable, RemoteVector
from skillbridge.client.workspace import Workspace as GWorkspace
from skillbridge.client.workspace import WorkspaceId

from .translator import Translator

_TRANSACTION_FUNCTIONS = (
    '__abRunTransaction',
    '__abRunSavepointBatch',
    '__abRunDryTransaction',
)


class Workspace(GWorkspace):
    # GWorkspace treats class annotations as FunctionCollection namespaces.

    def __init__(
        self,
        channel: Channel,
        id_: WorkspaceId,
    ) -> None:
        super().__init__(channel, id_)
        self._transaction = Txn(self)
        self._extension_lock = Lock()
        self._loaded_extensions: set[str] = set()
        self._extension_errors: dict[str, ExtensionError] = {}

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

    def _ensure_extension(self, name: str, procedures: tuple[str, ...]) -> None:
        def load() -> None:
            if self._has_procedures(procedures):
                return
            server_dir = Path(allegrobridge.server.__file__).parent
            path = server_dir / 'extensions' / f'{name}.il'
            if not path.is_file():
                raise ExtensionError(f'SKILL file for extension {name!r} was not found')
            self['load'](path.resolve().as_posix())
            if not self._has_procedures(procedures):
                raise ExtensionError(f'extension {name!r} failed readiness check')

        with self._extension_lock:
            if name in self._loaded_extensions:
                return
            if name in self._extension_errors:
                raise self._extension_errors[name]
            try:
                load()
            except ExtensionError as error:
                self._extension_errors[name] = error
                raise
            except Exception as error:
                failure = ExtensionError(f'failed to load extension {name!r}')
                self._extension_errors[name] = failure
                raise failure from error
            self._loaded_extensions.add(name)


# Register domain collections as class annotations, excluding 'db' which is inherited
# rough count of axl_* apis in allegro: 792
# The lowercase APIs axlcreate and axldo are callable only through ws['api_name'].
_workspace_members = set(dir(GWorkspace))
Workspace.__annotations__.update({
    domain: FunctionCollection
    for domain in extract_api_domains()
    if (domain.isidentifier() and domain != "root" and domain not in _workspace_members)
})


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
        commands = list(cmds)
        if not commands:
            return []
        result = self._workspace['__abRunSavepointBatch'](SkillList(commands))
        return cast('list[SavepointResult]', result)


class SavepointSuccess(TypedDict):
    index: int
    status: Literal['success']
    value: Skill


class SavepointFailure(TypedDict):
    index: int
    status: Literal['failure']
    error: str


SavepointResult = Union[SavepointSuccess, SavepointFailure]
