from __future__ import annotations

from io import StringIO

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from skillbridge import Expr
from skillbridge.client.translator import DefaultTranslator
from skillbridge.protocol.response import Response
from skillbridge.protocol.socket import Socket

_ONE_MIB = 1_048_576
_WIDTH = 10


@pytest.mark.benchmark(group='socket-header')
def test_socket_header_roundtrip(benchmark: BenchmarkFixture) -> None:
    header = benchmark(Socket.encode_header, _ONE_MIB)

    assert Socket.decode_header(header) == _ONE_MIB


@pytest.mark.benchmark(group='response-parser')
def test_response_parser(benchmark: BenchmarkFixture) -> None:
    frame = f'{Response.STX}{"x" * 4096}{Response.RS}'

    response = benchmark(lambda: Response(StringIO(frame)).recv())

    assert response.payload == 'x' * 4096


@pytest.mark.benchmark(group='translator')
def test_translator_encode(benchmark: BenchmarkFixture) -> None:
    translator = DefaultTranslator()
    value = list(range(256))

    encoded = benchmark(translator.encode, value)

    assert encoded.startswith('(list 0 1 2')


@pytest.mark.benchmark(group='translator')
def test_translator_decode(benchmark: BenchmarkFixture) -> None:
    translator = DefaultTranslator()
    payload = repr(list(range(256)))

    decoded = benchmark(translator.decode, payload)

    assert decoded == list(range(256))


@pytest.mark.benchmark(group='expr-renderer')
def test_expr_renderer(benchmark: BenchmarkFixture) -> None:
    items = Expr.raw_skill('design->components').as_list()
    expression = items.where(lambda item: item.enabled & (item.width > _WIDTH)).each.name

    rendered = benchmark(expression.render)

    assert rendered == (
        'setof(_expr0 design->components and(_expr0->enabled (_expr0->width > 10)))~>name'
    )
