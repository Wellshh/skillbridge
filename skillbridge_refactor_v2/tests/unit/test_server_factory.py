from __future__ import annotations

from skillbridge.pipe import SkillPipe
from skillbridge.response_protocol import FramedResponseProtocol
from skillbridge.server import SingleTcpServer, create_server
from ..helpers import BlockingTextReader, RecordingWriter


def test_windows_factory_uses_tcp_and_preserves_timeout(monkeypatch) -> None:
    reader = BlockingTextReader()
    pipe = SkillPipe(
        reader,
        RecordingWriter(),
        owns_streams=True,
    )
    monkeypatch.setattr("skillbridge.server.sys.platform", "win32")
    server = create_server(
        "0",
        skill_pipe=pipe,
        single=True,
        timeout=0.25,
        force_tcp=False,
    )
    try:
        assert isinstance(server, SingleTcpServer)
        assert server.skill_timeout == 0.25
        assert server.server_address[0] == "127.0.0.1"
    finally:
        server.server_close()
        pipe.close()
        pipe.join_reader(1.0)
