from __future__ import annotations

from io import StringIO

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from skillbridge import Expr
from skillbridge.client.translator import DefaultTranslator
from skillbridge.protocol.response import Response
from skillbridge.protocol.socket import Socket

_ONE_MIB = 1_048_576
_PAYLOAD_SIZES = (64, 4096, _ONE_MIB)
_WIDTH = 10


@pytest.mark.benchmark(group='socket-header')
def test_socket_encode_header(benchmark: BenchmarkFixture) -> None:
    header = benchmark(Socket.encode_header, _ONE_MIB)

    assert header == b'   1048576'


@pytest.mark.benchmark(group='socket-header')
def test_socket_decode_header(benchmark: BenchmarkFixture) -> None:
    header = Socket.encode_header(_ONE_MIB)

    size = benchmark(Socket.decode_header, header)

    assert size == _ONE_MIB


@pytest.mark.benchmark(group='response-parser')
@pytest.mark.parametrize('size', _PAYLOAD_SIZES, ids=['64B', '4KiB', '1MiB'])
def test_response_recv_stringio(benchmark: BenchmarkFixture, size: int) -> None:
    payload = 'x' * size
    frame = f'{Response.STX}{payload}{Response.RS}'
    benchmark.extra_info.update(
        direction='response',
        payload_chars=len(payload),
        payload_bytes=len(payload.encode()),
    )

    response = benchmark(lambda: Response(StringIO(frame)).recv())

    assert response.payload == payload


@pytest.mark.benchmark(group='translator')
def test_translator_encode(benchmark: BenchmarkFixture) -> None:
    translator = DefaultTranslator()
    value = list(range(256))
    benchmark.extra_info['input_items'] = len(value)

    encoded = benchmark(translator.encode, value)

    benchmark.extra_info['encoded_bytes'] = len(encoded.encode())
    assert encoded.startswith('(list 0 1 2')


@pytest.mark.benchmark(group='translator')
def test_translator_decode(benchmark: BenchmarkFixture) -> None:
    translator = DefaultTranslator()
    payload = repr(list(range(256)))
    benchmark.extra_info.update(
        input_items=256,
        encoded_bytes=len(payload.encode()),
    )

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
