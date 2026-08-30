from __future__ import annotations

import sys
from collections.abc import Iterator
from hashlib import sha256
from pathlib import Path
from shutil import copy2
from socket import socket

import pytest

from allegrobridge import Allegro
from allegrobridge._kernel.client.hints import Symbol
from allegrobridge.client.api import BoardInfo
from allegrobridge.util import ASSETS_DIR

_BENCHMARK_CONTEXT: dict[str, object] = {}


@pytest.fixture(scope='module')
def allegro_context(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[tuple[Allegro, BoardInfo]]:
    if sys.platform != 'win32':
        pytest.skip('canonical Allegro benchmarks require Windows CLI mode')

    with socket() as listener:
        listener.bind(('localhost', 0))
        workspace_id = str(listener.getsockname()[1])

    board = Path(copy2(ASSETS_DIR / 'shape1.brd', tmp_path_factory.mktemp('benchmark')))
    with Allegro.open(mode='cli', board=board, workspace_id=workspace_id) as opened:
        board_info = opened.session.board()
        full_version = opened.workspace.axl.version(Symbol('fullVersion'))
        release = opened.workspace.axl.version(Symbol('release'))
        assert isinstance(full_version, str)
        assert isinstance(release, str)
        _BENCHMARK_CONTEXT.clear()
        _BENCHMARK_CONTEXT.update(
            allegro_full_version=full_version,
            allegro_release=release,
            board_sha256=sha256(board.read_bytes()).hexdigest(),
            board_component_count=board_info.component_count,
            board_symbol_count=board_info.symbol_count,
            board_net_count=board_info.net_count,
        )
        yield opened, board_info


def pytest_benchmark_update_json(
    config: pytest.Config,
    benchmarks: list[object],
    output_json: dict[str, object],
) -> None:
    _ = config, benchmarks
    output_json['benchmark_context'] = _BENCHMARK_CONTEXT.copy()
