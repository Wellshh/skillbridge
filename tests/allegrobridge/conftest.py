from __future__ import annotations

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if 'integration' in item.path.name:
            item.add_marker(pytest.mark.allegro)
