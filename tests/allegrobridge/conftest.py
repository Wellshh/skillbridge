from __future__ import annotations

from pathlib import Path

import pytest

_ALLEGRO_DIR = Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if Path(str(item.path)).is_relative_to(_ALLEGRO_DIR):
            item.add_marker(pytest.mark.allegro)
