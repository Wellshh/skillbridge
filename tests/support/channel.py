# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

from collections import deque
from typing import Any

from allegrobridge._kernel.client.channel import Channel

_MAX_ERROR_REPORT = 100


class DummyChannel(Channel):
    def __init__(self) -> None:
        super().__init__(0)

        self.outputs: deque[str] = deque()
        self.inputs: deque[str] = deque()

    def _try_queue(self, data: str) -> str:
        try:
            result = self.inputs.popleft()
        except IndexError:
            short_data = data if len(data) < _MAX_ERROR_REPORT else data[:_MAX_ERROR_REPORT] + "..."
            raise RuntimeError(
                f"No input provided for TestChannel: request was {short_data}",
            ) from None
        else:
            self.outputs.append(data)
            return result

    def send(self, data: str) -> Any:
        return self._try_queue(data)

    def close(self) -> None:
        pass

    def flush(self) -> None:
        pass

    def try_repair(self) -> Any:
        pass
