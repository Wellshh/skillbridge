from __future__ import annotations

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from allegrobridge import Allegro
from allegrobridge._kernel.client.translator import DefaultTranslator
from allegrobridge.client.api import BoardInfo, ComponentInfo, NetInfo

_PLUS_RESULT = 3
_ONE_MIB = 1_048_576
_PAYLOAD_SIZES = (64, 4096, _ONE_MIB)
_ROUNDS = 30
_WARMUP_ROUNDS = 5
AllegroContext = tuple[Allegro, BoardInfo]


def _payload_info(benchmark: BenchmarkFixture, direction: str, payload: str) -> None:
    benchmark.extra_info.update(
        direction=direction,
        payload_chars=len(payload),
        payload_bytes=len(payload.encode()),
    )


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-rpc')
def test_raw_noop(benchmark: BenchmarkFixture, allegro_context: AllegroContext) -> None:
    allegro, _ = allegro_context
    send = allegro.workspace._channel.send  # ruff: ignore[private-member-access]

    result = benchmark.pedantic(
        send,
        args=('1',),
        rounds=_ROUNDS,
        warmup_rounds=_WARMUP_ROUNDS,
        iterations=1,
    )

    assert result == '1'


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-rpc')
def test_steady_state_plus(
    benchmark: BenchmarkFixture,
    allegro_context: AllegroContext,
) -> None:
    allegro, _ = allegro_context
    plus = allegro.workspace['plus']

    result = benchmark.pedantic(
        plus,
        args=(1, 2),
        rounds=_ROUNDS,
        warmup_rounds=_WARMUP_ROUNDS,
        iterations=1,
    )

    assert result == _PLUS_RESULT


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-payload')
@pytest.mark.parametrize('size', _PAYLOAD_SIZES, ids=['64B', '4KiB', '1MiB'])
def test_request_payload(
    benchmark: BenchmarkFixture,
    allegro_context: AllegroContext,
    size: int,
) -> None:
    allegro, _ = allegro_context
    send = allegro.workspace._channel.send  # ruff: ignore[private-member-access]
    translator = DefaultTranslator()
    payload = 'x' * size
    command = f'strlen({translator.encode(payload)})'
    _payload_info(benchmark, 'request', payload)

    result = benchmark.pedantic(
        send,
        args=(command,),
        rounds=_ROUNDS,
        warmup_rounds=_WARMUP_ROUNDS,
        iterations=1,
    )

    assert result == str(size)


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-payload')
@pytest.mark.parametrize('size', _PAYLOAD_SIZES, ids=['64B', '4KiB', '1MiB'])
def test_response_payload(
    benchmark: BenchmarkFixture,
    allegro_context: AllegroContext,
    size: int,
) -> None:
    allegro, _ = allegro_context
    send = allegro.workspace._channel.send  # ruff: ignore[private-member-access]
    translator = DefaultTranslator()
    payload = 'x' * size
    assigned = send(translator.encode_assign('__abBenchmarkPayload', payload))
    assert translator.decode(assigned) is None
    _payload_info(benchmark, 'response', payload)

    encoded = benchmark.pedantic(
        send,
        args=('__abBenchmarkPayload',),
        rounds=_ROUNDS,
        warmup_rounds=_WARMUP_ROUNDS,
        iterations=1,
    )

    assert translator.decode(encoded) == payload


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-payload')
@pytest.mark.parametrize('size', _PAYLOAD_SIZES, ids=['64B', '4KiB', '1MiB'])
def test_echo_payload(
    benchmark: BenchmarkFixture,
    allegro_context: AllegroContext,
    size: int,
) -> None:
    allegro, _ = allegro_context
    build_string = allegro.workspace['buildString']
    payload = 'x' * size
    _payload_info(benchmark, 'bidirectional', payload)

    result = benchmark.pedantic(
        build_string,
        args=([payload],),
        rounds=_ROUNDS,
        warmup_rounds=_WARMUP_ROUNDS,
        iterations=1,
    )

    assert result == payload


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-domain-read')
@pytest.mark.parametrize('domain', ['board', 'components', 'nets'])
def test_domain_read(
    benchmark: BenchmarkFixture,
    allegro_context: AllegroContext,
    domain: str,
) -> None:
    allegro, board_info = allegro_context
    operation = getattr(allegro.session, domain)

    result = benchmark.pedantic(
        operation,
        rounds=_ROUNDS,
        warmup_rounds=_WARMUP_ROUNDS,
        iterations=1,
    )

    if domain == 'board':
        assert isinstance(result, BoardInfo)
        result_count = 1
    elif domain == 'components':
        assert isinstance(result, list)
        assert all(isinstance(item, ComponentInfo) for item in result)
        assert len(result) == board_info.component_count
        result_count = len(result)
    else:
        assert isinstance(result, list)
        assert all(isinstance(item, NetInfo) for item in result)
        assert len(result) == board_info.net_count
        result_count = len(result)
    benchmark.extra_info.update(domain=domain, result_count=result_count)
