# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from pytest import fixture, raises, warns

from allegrobridge._kernel import Key, ParseError
from tests.support import DummyWorkspace, PassWorkspace
from tests.support.channel import DummyChannel


@fixture
def ws() -> DummyWorkspace:
    return DummyWorkspace()


@fixture
def passws() -> PassWorkspace:
    return PassWorkspace()


def test_success(ws):
    ws.prepare(101)

    assert ws.db.add_one(100) == 101
    assert ws.pop_match('dbAddOne.*100')


def test_key(ws):
    assert str(Key("arg")) == "Key(arg)"
    assert repr(Key("arg")) == "Key(arg)"
    assert Key("arg").__repr_skill__() == "?arg"


def test_remote_object(ws):
    ws.prepare_remote('I1')
    inst = ws.db.find_any_inst(None, "foo")

    ws.prepare(1)
    ws.prepare(2)
    assert inst.x == 1
    assert inst.y == 2


def test_error(ws):
    ws.prepare_error("nope")

    with raises(ParseError, match="nope"):
        ws.db.add_one(1)


def test_warning(ws):
    ws.prepare_warning(101, "deprecated")

    with warns(UserWarning, match="deprecated"):
        assert ws.db.add_one(100) == 101


def test_pass_works(passws):
    passws.prepare(Ellipsis)
    assert passws.user.call()

    class UserDefined:
        def __init__(self, x: int) -> None:
            self.x = x

        def __repr__(self) -> str:
            return "user defined"

        def __str__(self) -> str:
            return "user defined"

    u = UserDefined(123)
    passws.prepare(u)

    assert passws.user.call() is u
    assert passws._test_translator.encode('value') == 'value'
    assert passws._test_channel.flush() is None
    assert passws._test_channel.try_repair() is None


def test_dummy_channel_reports_unprepared_request() -> None:
    channel = DummyChannel()

    with raises(RuntimeError, match=r'request was short$'):
        channel.send('short')
    with raises(RuntimeError, match=rf'request was {"x" * 100}\.\.\.$'):
        channel.send('x' * 101)
