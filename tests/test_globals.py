from collections import deque
from typing import Any

from pytest import fixture, mark, raises

from skillbridge.client.channel import Channel
from skillbridge.client.globals import DirectGlobals, Globals, GlobalVar, is_variable_name
from skillbridge.client.translator import DefaultTranslator
from skillbridge.client.var import Var


class Redirect(Channel):
    def __init__(self) -> None:
        super().__init__(1_000_000)
        self.commands: list[str] = []
        self.responses: deque[str] = deque()

    def prepare(self, response: str) -> None:
        self.responses.append(response)

    def send(self, data: str) -> str:
        self.commands.append(data)
        return self.responses.popleft()

    def close(self) -> None:
        pass

    def flush(self) -> None:
        pass

    def try_repair(self) -> Any:
        return None


@fixture
def redirect() -> Redirect:
    return Redirect()


@fixture
def translator() -> DefaultTranslator:
    return DefaultTranslator()


@fixture
def globals_(redirect: Redirect, translator: DefaultTranslator) -> Globals:
    return Globals(redirect, translator, 'prefix')


def test_global_var_reads_and_writes(
    redirect: Redirect,
    translator: DefaultTranslator,
) -> None:
    variable = GlobalVar('prefix_x', redirect, translator)

    redirect.prepare('123')
    assert variable.read() == 123
    redirect.prepare('456')
    assert variable() == 456

    redirect.prepare('None')
    assert variable.write(789) is None
    redirect.prepare('None')
    assert (variable << 987) is None

    assert redirect.commands == [
        'prefixX',
        'prefixX',
        'prefixX = 789 nil',
        'prefixX = 987 nil',
    ]


def test_global_var_representation(
    redirect: Redirect,
    translator: DefaultTranslator,
) -> None:
    variable = GlobalVar('prefix_x', redirect, translator)

    assert str(variable) == 'Global(prefix_x)'
    assert repr(variable) == 'Global(prefix_x)'
    assert variable.__repr_skill__() == 'prefixX'


def test_global_var_collection_expressions(
    redirect: Redirect,
    translator: DefaultTranslator,
) -> None:
    variable = GlobalVar('prefix_x', redirect, translator)

    assert variable.map(Var('(i + 1)')).__repr_skill__() == 'mapcar(lambda((i) (i + 1) ) prefixX )'
    assert variable.map(Var('(i + j)'), j=Var('prefixY')).__repr_skill__() == (
        'mapcar(lambda((i j) (i + j) ) prefixX prefixY )'
    )
    with raises(AssertionError, match="Cannot use loop var 'i' twice"):
        variable.map(Var('i'), i=Var('prefixY'))

    assert variable.filter(Var('(i != 2)')).__repr_skill__() == 'setof(i prefixX (i != 2) )'
    redirect.prepare('None')
    assert variable.for_each(Var('delete(i)')) is None
    assert redirect.commands == ['foreach(i prefixX delete(i) ) nil']


@mark.parametrize(
    ('name', 'expected'),
    [('valid_name', True), ('_private', False), ('not-valid', False)],
)
def test_variable_name_validation(name: str, expected: bool) -> None:
    assert is_variable_name(name) is expected


def test_globals_resolves_names(globals_: Globals) -> None:
    assert repr(globals_) == 'Globals(prefix=prefix_)'
    assert globals_.value.name == 'prefix_value'
    assert globals_['value'].name == 'prefix_value'
    assert globals_['abc', 'def'].name == 'prefix_abc_def'

    with raises(AttributeError, match='_private'):
        _ = globals_['_private']


def test_globals_delegates_writes_and_deletes(
    globals_: Globals,
    redirect: Redirect,
) -> None:
    for _ in range(4):
        redirect.prepare('None')

    globals_['value'] = 1
    globals_['abc', 'def'] = 2
    del globals_.value
    del globals_['other']

    assert redirect.commands == [
        'prefixValue = 1 nil',
        'prefixAbcDef = 2 nil',
        'prefixValue = nil nil',
        'prefixOther = nil nil',
    ]


def test_globals_preserves_invalid_name_as_local_attribute(globals_: Globals) -> None:
    globals_['_local'] = 123

    assert globals_._local == 123


def test_direct_globals_reads_values(
    redirect: Redirect,
    translator: DefaultTranslator,
) -> None:
    direct = DirectGlobals(redirect, translator)

    redirect.prepare('123')
    assert direct.my_value == 123
    redirect.prepare('456')
    assert direct['literalName'] == 456
    assert redirect.commands == ['myValue', 'literalName']
