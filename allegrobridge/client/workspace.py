from __future__ import annotations

from collections.abc import Iterable
from functools import partial
from pathlib import Path
from typing import Literal, TypedDict, Union, cast

import allegrobridge.server
from allegrobridge.util import extract_api_domains
from skillbridge.client.channel import Channel
from skillbridge.client.functions import FunctionCollection
from skillbridge.client.hints import Skill, SkillCode, SkillList, Symbol
from skillbridge.client.objects import RemoteObject, RemoteTable, RemoteVector
from skillbridge.client.translator import DefaultTranslator
from skillbridge.client.workspace import Workspace as GWorkspace
from skillbridge.client.workspace import WorkspaceId

from .translator import Translator

_EXTENSION_FUNCTIONS = (
    '__abRunTransaction',
    '__abRunSavepointBatch',
    '__abRunDryTransaction',
    '__abProjectBoard',
    '__abProjectComponents',
    '__abMoveComponent',
    '__abProjectNets',
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

    @property
    def transaction(self) -> Txn:
        return self._transaction

    def _prepare_default_translator(self) -> DefaultTranslator:
        translator = Translator()
        types = [('Remote', RemoteObject), ('Table', RemoteTable), ('Vector', RemoteVector)]

        for name, typ in types:
            construct = partial(typ, self._channel, translator)
            translator.register_remote_variable_type(name, construct)

        return translator

    @classmethod
    def _create_workspace(cls, channel: Channel, workspace_id: WorkspaceId) -> GWorkspace:
        is_allegro = channel.send("isCallable('axlDBGetDesign)") == "True"
        if not is_allegro:
            return GWorkspace(channel, workspace_id)

        workspace = cls(channel, workspace_id)
        try:
            workspace._ensure_extension()
        except BaseException:
            workspace.close(log_exception=False)
            raise
        return workspace

    def _has_extension(self) -> bool:
        return all(self['isCallable'](Symbol(name)) for name in _EXTENSION_FUNCTIONS)

    def _ensure_extension(self) -> None:
        if self._has_extension():
            return

        server_file = Path(allegrobridge.server.__file__).with_name('allegro_server.il')
        self['load'](server_file.resolve().as_posix())
        if not self._has_extension():
            raise RuntimeError('Allegro extension failed to load')


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
