from __future__ import annotations

from skillbridge.client.channel import Channel
from skillbridge.client.functions import FunctionCollection
from skillbridge.client.workspace import Workspace as GWorkspace
from skillbridge.client.workspace import WorkspaceId

from .translator import Translator


class Workspace(GWorkspace):
    # rough count of axl_* apis in allegro: 796

    geo: FunctionCollection
    ui: FunctionCollection
    form: FunctionCollection
    poly: FunctionCollection
    drc: FunctionCollection
    cmd: FunctionCollection

    def __init__(
        self,
        channel: Channel,
        id_: WorkspaceId,
    ) -> None:
        super().__init__(channel, id_, Translator())

    @classmethod
    def _create_workspace(cls, channel: Channel, workspace_id: WorkspaceId) -> GWorkspace:
        # send a poll request to detect allegro env
        is_allegro = channel.send("isCallable('axlDBGetDesign)") == 'True'
        workspace_class = cls if is_allegro else GWorkspace
        return workspace_class(channel, workspace_id)
