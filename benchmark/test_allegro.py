from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path
from shutil import copy2
from socket import socket

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from allegrobridge import Allegro
from allegrobridge.util import ASSETS_DIR

_PLUS_RESULT = 3


@pytest.fixture(scope='module')
def allegro(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Allegro]:
    mode = 'cli' if sys.platform == 'win32' else 'manual'
    workspace_id = None
    board = None
    if mode == 'cli':
        with socket() as listener:
            listener.bind(('localhost', 0))
            workspace_id = str(listener.getsockname()[1])
        board = Path(copy2(ASSETS_DIR / 'shape1.brd', tmp_path_factory.mktemp('benchmark')))
    with Allegro.open(mode=mode, board=board, workspace_id=workspace_id) as opened:
        yield opened


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-rpc')
def test_steady_state_plus(benchmark: BenchmarkFixture, allegro: Allegro) -> None:
    plus = allegro.workspace['plus']

    result = benchmark.pedantic(plus, args=(1, 2), rounds=30, warmup_rounds=5, iterations=1)

    assert result == _PLUS_RESULT


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-payload')
@pytest.mark.parametrize('size', [64, 4096])
def test_string_roundtrip(
    benchmark: BenchmarkFixture,
    allegro: Allegro,
    size: int,
) -> None:
    build_string = allegro.workspace['buildString']
    payload = 'x' * size

    result = benchmark.pedantic(
        build_string,
        args=([payload],),
        rounds=30,
        warmup_rounds=5,
        iterations=1,
    )

    assert result == payload


@pytest.mark.allegro
@pytest.mark.benchmark(group='allegro-domain-read')
@pytest.mark.parametrize('domain', ['board', 'components', 'nets'])
def test_domain_read(
    benchmark: BenchmarkFixture,
    allegro: Allegro,
    domain: str,
) -> None:
    operation = getattr(allegro.session, domain)

    result = benchmark.pedantic(operation, rounds=30, warmup_rounds=5, iterations=1)

    assert result is not None
