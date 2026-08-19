from __future__ import annotations

from io import StringIO

import pytest

from skillbridge.response_protocol import (
    FramedResponseProtocol,
    SkillResponseProtocolError,
)


def test_framed_success_preserves_multiline_payload() -> None:
    response = FramedResponseProtocol().read_response(StringIO("\x02line one\nline two\x1e"))
    assert response.ok
    assert response.payload == "line one\nline two"


def test_framed_error_is_distinct_from_success() -> None:
    response = FramedResponseProtocol().read_response(StringIO("\x15bad expression\x1e"))
    assert not response.ok
    assert response.payload == "bad expression"


def test_strict_framing_rejects_preamble() -> None:
    with pytest.raises(SkillResponseProtocolError):
        FramedResponseProtocol().read_response(StringIO("noise\x02ok\x1e"))


def test_optional_preamble_ignoring() -> None:
    response = FramedResponseProtocol(ignore_preamble=True).read_response(
        StringIO("noise\n\x02ok\x1e")
    )
    assert response.payload == "ok"


def test_framed_protocol_rejects_oversized_payload() -> None:
    with pytest.raises(SkillResponseProtocolError):
        FramedResponseProtocol(max_payload_chars=3).read_response(StringIO("\x02four\x1e"))


def test_framed_protocol_reports_eof_inside_frame() -> None:
    with pytest.raises(EOFError, match="inside response frame"):
        FramedResponseProtocol().read_response(StringIO("\x02partial"))
