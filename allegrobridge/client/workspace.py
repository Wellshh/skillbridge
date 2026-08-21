from __future__ import annotations

from allegrobridge.util import extract_api_domains
from skillbridge.client.channel import Channel
from skillbridge.client.functions import FunctionCollection
from skillbridge.client.workspace import Workspace as GWorkspace
from skillbridge.client.workspace import WorkspaceId

from .translator import Translator


class Workspace(GWorkspace):
    def __init__(
        self,
        channel: Channel,
        id_: WorkspaceId,
    ) -> None:
        super().__init__(channel, id_, Translator())

    @classmethod
    def _create_workspace(cls, channel: Channel, workspace_id: WorkspaceId) -> GWorkspace:
        # send a poll request to detect allegro env
        is_allegro = channel.send("isCallable('axlDBGetDesign)") == "True"
        workspace_class = cls if is_allegro else GWorkspace
        return workspace_class(channel, workspace_id)


# Register domain collections as class annotations, excluding 'db' which is inherited
# rough count of axl_* apis in allegro: 792
# The lowercase APIs axlcreate and axldo are callable only through ws['api_name'].
_workspace_members = set(dir(GWorkspace))
Workspace.__annotations__.update({
    domain: FunctionCollection
    for domain in extract_api_domains()
    if (
        domain.isidentifier()
        and domain != "root"
        and domain not in _workspace_members
    )
})
