from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        '--allegro', action='store_true', default=False, help='run Allegro E2E benchmarks'
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    if config.option.allegro:
        return
    for item in items:
        if item.get_closest_marker('allegro') is not None:
            item.add_marker(pytest.mark.skip(reason='requires --allegro'))
