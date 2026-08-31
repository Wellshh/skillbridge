# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from logging import FileHandler, Formatter, Logger, getLogger
from pathlib import Path

from rich.logging import RichHandler

__all__ = ['LOGGERS', 'setup_logging']

LOGGERS = ('allegrobridge', 'allegrobridge.cadence', 'allegrobridge.server')

_OWNED_ATTR = '_allegrobridge_owned'
_CONSOLE_FORMATTER = Formatter('%(name)s: %(message)s')
_FILE_FORMATTER = Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')


def _clear_owned(logger: Logger) -> None:
    # remove duplicated handler creations
    for handler in list(logger.handlers):
        if getattr(handler, _OWNED_ATTR, False):
            logger.removeHandler(handler)
            handler.close()


def setup_logging(
    level: str | int = 'INFO',
    *,
    console: bool = True,
    file: str | Path | None = None,
) -> None:
    """Configure console and file logging for the allegrobridge namespace.

    Replaces previously attached library handlers (preserving external ones)
    and sets `propagate = False` to prevent double emission to root logger.

    Args:
        level: Logging threshold (e.g. `'DEBUG'`, `'INFO'`, or `logging.INFO`).
        console: Whether to enable rich console output.
        file: Optional file path to write logs to.

    Example:
        >>> import allegrobridge as ab
        >>> ab.setup_logging(level='DEBUG', file='allegrobridge.log')
    """
    logger = getLogger('allegrobridge')
    _clear_owned(logger)
    logger.setLevel(level)
    if console:
        handler = RichHandler(show_path=False, rich_tracebacks=True)
        handler.setFormatter(_CONSOLE_FORMATTER)
        setattr(handler, _OWNED_ATTR, True)
        logger.addHandler(handler)
    if file is not None:
        file_handler = FileHandler(file, encoding='utf-8')
        file_handler.setFormatter(_FILE_FORMATTER)
        setattr(file_handler, _OWNED_ATTR, True)
        logger.addHandler(file_handler)
    if console or file is not None:
        logger.propagate = False
