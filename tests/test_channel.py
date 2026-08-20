#!/usr/bin/env python3
from __future__ import annotations

import warnings
from collections.abc import Iterable, Iterator
from select import select
from socket import socket, socketpair
from threading import Thread
from typing import Literal

from _pytest.fixtures import SubRequest
from pytest import fixture, mark, raises

from skillbridge import Workspace, current_workspace, loop_var
from skillbridge.client.channel import Channel, TcpChannel, create_channel_class
from skillbridge.client.objects import RemoteObject
from skillbridge.exception import PeerClosedError
from skillbridge.protocol.socket import DEFAULT_MAX_PAYLOAD_SIZE, Socket
from tests.virtuoso import Virtuoso

WORKSPACE_ID = "8976"
channel_class = create_channel_class()
tcp_channel_class = create_channel_class(force_tcp=True)
SOCKET_TIMEOUT_SECONDS = 1.0


ComType = Literal["unix", "tcp"]


@fixture(params=['unix', 'tcp'])
def com_type(request: SubRequest) -> ComType:
    return request.param


@fixture
def server(com_type: ComType) -> Iterable[Virtuoso]:
    v = Virtuoso(WORKSPACE_ID, force_tcp=com_type == "tcp")
    v.start()
    v.wait_until_ready()
    yield v
    v.stop()


@fixture
def channel(com_type: ComType) -> Iterable[Channel]:
    c = (tcp_channel_class if com_type == "tcp" else channel_class)(WORKSPACE_ID)
    try:
        yield c
    finally:
        c.close()


@fixture
def local_tcp_channel() -> Iterator[tuple[TcpChannel, socket]]:
    local, peer = socketpair()
    local.settimeout(SOCKET_TIMEOUT_SECONDS)
    peer.settimeout(SOCKET_TIMEOUT_SECONDS)

    channel = object.__new__(TcpChannel)
    channel._max_transmission_length = 1_000_000
    channel.connected = True
    channel.socket = local
    channel._socket = Socket(local)

    try:
        yield channel, peer
    finally:
        channel.connected = False
        local.close()
        peer.close()


class TrackingSocket:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


class RaisingSocketWrapper:
    def __init__(self, error: BaseException) -> None:
        self.error = error

    def send_frame(self, _payload: bytes) -> None:
        raise self.error

    def recv_frame(self) -> bytes:
        raise self.error


def channel_raising(error: BaseException) -> tuple[TcpChannel, TrackingSocket]:
    raw_socket = TrackingSocket()
    channel = object.__new__(TcpChannel)
    channel._max_transmission_length = 1_000_000
    channel.connected = True
    channel.socket = raw_socket
    channel._socket = RaisingSocketWrapper(error)
    return channel, raw_socket


@fixture
def ws(com_type: ComType) -> Iterable[Workspace]:
    for _ in range(10):
        try:
            ws = Workspace.open(WORKSPACE_ID, force_tcp=com_type == "tcp")
        except BlockingIOError:
            continue
        else:
            break
    else:
        raise RuntimeError
    yield ws

    ws.close()


@mark.parametrize("use_tcp", argvalues=[False, True], ids=["unix", "tcp"])
def test_channel_cannot_connect_without_server(use_tcp: bool):
    with raises(Exception):
        tcp_channel_class(WORKSPACE_ID) if use_tcp else channel_class(WORKSPACE_ID)


@mark.parametrize("use_tcp", argvalues=[False, True], ids=["unix", "tcp"])
def test_channel_reconnects_without_replaying_failed_request(use_tcp: bool):
    first = Virtuoso(WORKSPACE_ID, force_tcp=use_tcp)
    first.start()
    first.wait_until_ready()

    c = (tcp_channel_class if use_tcp else channel_class)(WORKSPACE_ID)
    first.answer_success("pong")
    try:
        assert c.send("ping") == "pong"
        assert first.last_question == "ping"
    finally:
        first.stop()

    second = Virtuoso(WORKSPACE_ID, force_tcp=use_tcp)
    second.start()
    second.wait_until_ready()

    second.answer_success("toc")

    try:
        with raises(RuntimeError, match="unexpectedly died"):
            c.send("tic")
        assert second.last_question is None

        assert c.send("next") == "toc"
        assert second.last_question == "next"
    finally:
        c.close()
        second.stop()


def test_channel_connects(server: Virtuoso):
    c = tcp_channel_class(WORKSPACE_ID) if server.force_tcp else channel_class(WORKSPACE_ID)
    assert c.connected
    assert c.max_transmission_length == DEFAULT_MAX_PAYLOAD_SIZE
    c.close()


def test_one_message_is_send(server: Virtuoso, channel: Channel):
    server.answer_success("pong")
    answer = channel.send("ping")

    assert answer == "pong"
    assert server.last_question == "ping"


def test_many_messages_are_send(server: Virtuoso, channel: Channel):
    for index in range(10):
        question = f"question-{index}"

        server.answer_success(f"answer-{index}")
        answer = channel.send(question)

        assert answer == f"answer-{index}"
        assert server.last_question == question


def test_raise_on_failure(server: Virtuoso, channel: Channel):
    server.answer_failure("pong")

    with raises(Exception, match="pong"):
        channel.send("ping")


def test_workspace_contains_prefixes(server: Virtuoso, ws: Workspace):
    assert "db" in dir(ws)
    assert hasattr(ws, "db")
    server.answer_success('"geGetEditCellView"')
    assert "get_edit_cell_view" in dir(ws.ge)
    server.answer_success('"geGetEditCellView"')
    assert "get_edit_cell_view" in repr(ws.ge)


def test_function_call_is_send(server: Virtuoso, ws: Workspace):
    server.answer_success("1")
    cell = ws.ge.get_edit_cell_view()

    assert "geGetEditCellView" in server.last_question
    assert cell == 1

    server.answer_success('"geGetEditCellView ... doc"')
    assert "geGetEditCellView" in repr(ws.ge.get_edit_cell_view)


def test_unknown_function_raises(server: Virtuoso, ws: Workspace):
    server.answer_failure("")
    with raises(RuntimeError):
        ws.ge.this_does_not_exist_and_will_hopefully_never_exist()

    server.answer_success('Remote("__py_object_123")')
    result = ws.ge.get_edit_cell_view()
    with raises(AttributeError):
        _ = result._repr_html_


def test_list_is_mapped(server: Virtuoso, ws: Workspace):
    server.answer_success("[1,2,3,[4,5,6],[7,8,9,[10,11,12]]]")
    result = ws.ge.get_edit_cell_view()

    assert result == [1, 2, 3, [4, 5, 6], [7, 8, 9, [10, 11, 12]]]


def test_property_list_is_mapped(server: Virtuoso, ws: Workspace):
    server.answer_success("{'x': 1, 'y': 2}")
    result = ws.ge.get_edit_cell_view()

    assert result["x"] == 1
    assert result["y"] == 2


def test_object_is_mapped(server: Virtuoso, ws: Workspace):
    server.answer_object("object", 0x1234)
    result = ws.ge.get_edit_cell_view()

    assert isinstance(result, RemoteObject)
    server.answer_success('"object"')
    string = str(result)
    assert "object@0x1234" in string

    server.answer_success('["x","y","z"]')
    doc = result.getdoc()
    assert "x" in doc
    assert "y" in doc
    assert "z" in doc


def test_db_object_repr(server: Virtuoso, ws: Workspace):
    server.answer_object("db", 1234)
    db = ws.ge.get_edit_cell_view()
    server.answer_success('"instance"')
    assert "instance" in str(db)
    assert "objType" in server.last_question


def test_dd_object_repr(server: Virtuoso, ws: Workspace):
    server.answer_object("dd", 1234)
    dd = ws.ge.get_edit_cell_view()
    server.answer_success('Symbol("DDthingTYPE")')
    assert "thing" in str(dd)
    assert "objType" in server.last_question


def test_nested_remote_object(server: Virtuoso, ws: Workspace):
    server.answer_object("parent", 1234)
    parent = ws.ge.get_edit_cell_view()
    server.answer_object("child", 1234)
    child = parent.child
    assert isinstance(child, RemoteObject)


def test_send_back_objects(server: Virtuoso, ws: Workspace):
    server.answer_object("object", 123)
    result = ws.ge.get_edit_cell_view()

    server.answer_object("window", 234)
    window = ws.ge.get_cell_view_window(result)

    assert window._variable == "__py_window_234"


def test_setattr(server: Virtuoso, ws: Workspace):
    server.answer_object("object", 123)
    result = ws.ge.get_edit_cell_view()

    server.answer_success("123")
    result.x = 234

    assert server.last_question.strip().replace(" ", "") == "__py_object_123->x=234"


def test_object_equality(server: Virtuoso, ws: Workspace):
    server.answer_object("object", 123)
    server.answer_object("object", 123)
    server.answer_object("object", 234)

    first = ws.ge.get_edit_cell_view()
    second = ws.ge.get_edit_cell_view()
    third = ws.ge.get_edit_cell_view()

    assert first == second
    assert first != third
    assert second != third
    assert not (first == 1)  # ruff: ignore[negate-equal-op]  # this tests __eq__ and the next line tests __ne__
    assert first != 1


def test_fix_completion_does_not_raise(server: Virtuoso, ws: Workspace):
    ws.fix_completion()


def test_max_transmission_length_is_honored(server: Virtuoso, ws: Workspace):
    _ = server
    ws.max_transmission_length = 100
    assert ws.max_transmission_length == 100
    assert ws._channel

    with raises(ValueError, match="max transmission"):
        ws._channel.send("x" * 200)


def test_flush_does_no_harm(server: Virtuoso, ws: Workspace):
    ws.flush()


class TestTcpChannelCleanup:
    def test_send_failure_reconnects_without_retrying(
        self,
        local_tcp_channel: tuple[TcpChannel, socket],
        monkeypatch,
    ) -> None:
        channel, peer = local_tcp_channel
        next_local, next_peer = socketpair()
        next_local.settimeout(SOCKET_TIMEOUT_SECONDS)
        next_peer.settimeout(SOCKET_TIMEOUT_SECONDS)

        def start() -> socket:
            channel.connected = True
            return next_local

        monkeypatch.setattr(channel, 'start', start)
        peer.close()

        try:
            with raises(RuntimeError, match='unexpectedly died'):
                channel.send('write()')
            assert select([next_peer], [], [], 0)[0] == []

            Socket(next_peer).send_frame(b'success ok')
            assert channel.send('next()') == 'ok'
            assert Socket(next_peer).recv_frame() == b'next()'
        finally:
            channel.connected = False
            next_local.close()
            next_peer.close()

    def test_lost_response_reconnects_without_replaying_request(
        self,
        local_tcp_channel: tuple[TcpChannel, socket],
        monkeypatch,
    ) -> None:
        channel, peer = local_tcp_channel
        next_local, next_peer = socketpair()
        next_local.settimeout(SOCKET_TIMEOUT_SECONDS)
        next_peer.settimeout(SOCKET_TIMEOUT_SECONDS)
        received: list[bytes] = []

        def start() -> socket:
            channel.connected = True
            return next_local

        def drop_response() -> None:
            received.append(Socket(peer).recv_frame())
            peer.close()

        monkeypatch.setattr(channel, 'start', start)
        dropping = Thread(target=drop_response)
        dropping.start()

        try:
            with raises(RuntimeError, match='unexpectedly died'):
                channel.send('write()')
            dropping.join(SOCKET_TIMEOUT_SECONDS)
            assert not dropping.is_alive()
            assert received == [b'write()']
            assert select([next_peer], [], [], 0)[0] == []

            Socket(next_peer).send_frame(b'success ok')
            assert channel.send('next()') == 'ok'
            assert Socket(next_peer).recv_frame() == b'next()'
        finally:
            channel.connected = False
            next_local.close()
            next_peer.close()

    def test_close_sends_close_frame_and_releases_socket(
        self,
        local_tcp_channel: tuple[TcpChannel, socket],
    ) -> None:
        channel, peer = local_tcp_channel

        channel.close()

        assert Socket(peer).recv_frame() == b'$close'
        assert not channel.connected
        assert channel.socket.fileno() == -1

    def test_close_ignores_connection_error_and_releases_socket(self) -> None:
        channel, raw_socket = channel_raising(BrokenPipeError())

        channel.close()

        assert raw_socket.closed
        assert not channel.connected

    def test_close_propagates_unexpected_error_after_releasing_socket(self) -> None:
        channel, raw_socket = channel_raising(RuntimeError('unexpected'))

        try:
            with raises(RuntimeError, match='unexpected'):
                channel.close()
        finally:
            channel.connected = False

        assert raw_socket.closed
        assert not channel.connected

    def test_close_propagates_keyboard_interrupt_after_releasing_socket(self) -> None:
        channel, raw_socket = channel_raising(KeyboardInterrupt())

        try:
            with raises(KeyboardInterrupt):
                channel.close()
        finally:
            channel.connected = False

        assert raw_socket.closed
        assert not channel.connected

    def test_flush_discards_all_complete_queued_frames(
        self,
        local_tcp_channel: tuple[TcpChannel, socket],
    ) -> None:
        channel, peer = local_tcp_channel
        sending = Socket(peer)
        sending.send_frame(b'first')
        sending.send_frame(b'second')

        channel.flush()

        assert select([channel.socket], [], [], 0)[0] == []
        sending.send_frame(b'next')
        assert channel._socket.recv_frame() == b'next'

    @mark.parametrize(
        'error',
        [
            PeerClosedError(10, 4),
            RuntimeError('unexpected'),
            KeyboardInterrupt(),
        ],
        ids=['peer-closed', 'runtime-error', 'keyboard-interrupt'],
    )
    def test_flush_propagates_read_error(self, monkeypatch, error: BaseException) -> None:
        channel, _ = channel_raising(error)
        readiness = iter([([channel.socket], [], []), ([], [], [])])
        monkeypatch.setattr(
            'skillbridge.client.channel.select',
            lambda *_args, **_kwargs: next(readiness),
        )

        try:
            with raises(type(error), match=str(error) or None):
                channel.flush()
        finally:
            channel.connected = False


def test_make_workspace_current(server: Virtuoso, ws: Workspace):
    _ = server
    assert not current_workspace.is_current
    assert not ws.is_current

    ws.make_current()

    assert current_workspace.is_current
    assert ws.is_current


def test_use_current_workspace(server: Virtuoso, ws: Workspace):
    with raises(RuntimeError):
        current_workspace.ge.get_edit_cell_view()

    ws.make_current()

    server.answer_success('"ok"')
    assert current_workspace.ge.get_edit_cell_view() == "ok"

    ws.close()

    with raises(RuntimeError):
        current_workspace.ge.get_edit_cell_view()


def test_warning_is_printed(server: Virtuoso, ws: Workspace):
    server.answer_success('warning("This is a warning", 1234)')

    with warnings.catch_warnings(record=True) as w:
        result = ws.ge.get_edit_cell_view()

    assert len(w) == 1
    assert w[0].category is UserWarning
    assert "This is a warning" in str(w[0].message)

    assert result == 1234


def test_funcall_shortcut(server: Virtuoso, ws: Workspace):
    server.answer_object("testfun", 123)
    fun = ws.ge.get_edit_cell_view()

    server.answer_success("42")
    assert fun() == 42
    assert server.last_question == "funcall(__py_testfun_123 )"

    server.answer_success("41")
    assert fun(1, 2, 3) == 41
    assert server.last_question == "funcall(__py_testfun_123 1 2 3 )"

    server.answer_success("40")
    assert fun(a=1, b=2, c=3) == 40
    assert server.last_question == "funcall(__py_testfun_123 ?a 1 ?b 2 ?c 3)"

    server.answer_success("39")
    assert fun(10, 20, 30, a=1, b=2, c=3) == 39
    assert server.last_question == "funcall(__py_testfun_123 10 20 30 ?a 1 ?b 2 ?c 3)"


def test_open_file(server: Virtuoso, ws: Workspace):
    server.answer_object("openfile", 22)
    f = ws.ge.get_edit_cell_view()

    assert f.skill_type == "open_file"
    server.answer_success("'port:\"test.txt\"'")
    assert str(f) == "<remote open_file 'test.txt'>"
    assert server.last_question == 'lsprintf("%s" __py_openfile_22 )'

    assert dir(f)


def test_globals_direct_write(server: Virtuoso, ws: Workspace):
    g = ws.globals("prefix")
    server.answer_success("None")
    g.x << "123"
    assert server.last_question == 'prefixX = "123" nil'


def test_globals_read(server: Virtuoso, ws: Workspace):
    g = ws.globals("prefix")
    server.answer_success("123")
    assert g.x() == 123
    assert server.last_question == "prefixX"


def test_globals_repr(server: Virtuoso, ws: Workspace):
    _ = server
    g = ws.globals("prefix")

    assert str(g.x) == "Global(prefix_x)"
    assert repr(g.x) == "Global(prefix_x)"
    assert g.x.__repr_skill__() == "prefixX"


def test_globals_map_car(server: Virtuoso, ws: Workspace):
    _ = server
    g = ws.globals("prefix")

    assert g.x.map(loop_var + 1).name == "mapcar(lambda((i) (i + 1) ) prefixX )"


def test_globals_for_each(server: Virtuoso, ws: Workspace):
    g = ws.globals("prefix")

    server.answer_success("None")
    assert g.x.for_each(ws.db.delete.var(loop_var)) is None
    assert server.last_question == "foreach(i prefixX dbDelete(i ) ) nil"


def test_globals_filter(server: Virtuoso, ws: Workspace):
    _ = server
    g = ws.globals("prefix")

    assert g.x.filter(loop_var != 2).name == "setof(i prefixX (i != 2) )"


def test_globals_tuple_write(server: Virtuoso, ws: Workspace):
    g = ws.globals("prefix")

    server.answer_success("None")
    g["abc", "def"] = 1

    assert server.last_question == "prefixAbcDef = 1 nil"


def test_globals_tuple_read(server: Virtuoso, ws: Workspace):
    _ = server
    g = ws.globals("prefix")

    assert g["abc", "def"].name == "prefix_abc_def"


def test_globals_delete(server: Virtuoso, ws: Workspace):
    g = ws.globals("prefix")

    server.answer_success("None")
    del g.x

    assert server.last_question == "prefixX = nil nil"


def test_globals_raises_when_attribute_is_invalid(
    server: Virtuoso,
    ws: Workspace,
):
    g = ws.globals("prefix")
    with raises(AttributeError):
        print(g.__wat__)


def test_raw_object_access(server: Virtuoso, ws: Workspace):
    server.answer_object("object", 22)

    x = ws.db.get_stuff()

    server.answer_success("123")
    i = x.abc_def
    assert i == 123
    assert server.last_question == "__py_object_22->abcDef"

    server.answer_success("234")
    i = x["abc_def"]
    assert i == 234
    assert server.last_question == "__py_object_22->abc_def"

    server.answer_success("True")
    x.abc_def = 345
    assert server.last_question == "__py_object_22->abcDef = 345"

    server.answer_success("True")
    x["abc_def"] = 456
    assert server.last_question == "__py_object_22->abc_def = 456"
