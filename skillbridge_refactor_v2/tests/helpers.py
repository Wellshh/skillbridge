from __future__ import annotations

import queue
import threading
from io import TextIOBase

from skillbridge.response_protocol import NAK, RS, STX


class BlockingTextReader(TextIOBase):
    """Controllable blocking reader supporting read(1) and readline()."""

    _EOF = object()

    def __init__(self) -> None:
        super().__init__()
        self._chars: queue.Queue[str | object] = queue.Queue()
        self.read_entered = threading.Event()

    def feed(self, text: str) -> None:
        for char in text:
            self._chars.put(char)

    def feed_success(self, payload: str) -> None:
        self.feed(STX + payload + RS)

    def feed_error(self, payload: str) -> None:
        self.feed(NAK + payload + RS)

    def feed_line(self, line: str) -> None:
        self.feed(line)

    def feed_eof(self) -> None:
        self._chars.put(self._EOF)

    def read(self, size: int = -1) -> str:
        self.read_entered.set()
        if size == 0:
            return ""
        if size < 0:
            size = 1
        output: list[str] = []
        for _ in range(size):
            value = self._chars.get()
            if value is self._EOF:
                if not output:
                    return ""
                self._chars.put(self._EOF)
                break
            assert isinstance(value, str)
            output.append(value)
        return "".join(output)

    def readline(self, size: int = -1) -> str:
        self.read_entered.set()
        output: list[str] = []
        while size < 0 or len(output) < size:
            value = self._chars.get()
            if value is self._EOF:
                if not output:
                    return ""
                self._chars.put(self._EOF)
                break
            assert isinstance(value, str)
            output.append(value)
            if value == "\n":
                break
        return "".join(output)

    def close(self) -> None:
        if not self.closed:
            self.feed_eof()
        super().close()


class RecordingWriter(TextIOBase):
    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()
        self._parts: list[str] = []
        self.flush_count = 0
        self.write_event = threading.Event()

    def write(self, text: str) -> int:
        with self._lock:
            self._parts.append(text)
            self.write_event.set()
        return len(text)

    def flush(self) -> None:
        with self._lock:
            self.flush_count += 1

    @property
    def text(self) -> str:
        with self._lock:
            return "".join(self._parts)

    def lines(self) -> list[str]:
        return self.text.splitlines()


class FailingWriter(RecordingWriter):
    def write(self, text: str) -> int:
        del text
        raise OSError("simulated write failure")
