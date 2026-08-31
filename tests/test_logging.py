# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import io
import logging

from rich.logging import RichHandler

from allegrobridge._logging import LOGGERS, setup_logging


def test_init_installs_single_null_handler() -> None:
    logger = logging.getLogger('allegrobridge')
    assert [type(h) for h in logger.handlers] == [logging.NullHandler]
    assert logger.propagate is True


def test_init_exposes_logger_names() -> None:
    assert LOGGERS == ('allegrobridge', 'allegrobridge.cadence', 'allegrobridge.server')


def test_setup_logging_defaults_to_rich_console_handler() -> None:
    setup_logging('WARNING')
    logger = logging.getLogger('allegrobridge')
    owned = [h for h in logger.handlers if getattr(h, '_allegrobridge_owned', False)]
    assert [type(h) for h in owned] == [RichHandler]
    assert logger.level == logging.WARNING
    assert logger.propagate is False

    record = logger.makeRecord(
        'allegrobridge.cadence', logging.INFO, __file__, 1, 'hello', (), None
    )
    assert owned[0].formatter is not None
    assert owned[0].formatter.format(record) == 'allegrobridge.cadence: hello'


def test_setup_logging_with_file_adds_tagged_file_handler(tmp_path) -> None:
    file_path = tmp_path / 'allegrobridge_server.log'
    setup_logging(file=file_path)
    logger = logging.getLogger('allegrobridge')
    owned = [h for h in logger.handlers if getattr(h, '_allegrobridge_owned', False)]
    assert any(isinstance(h, RichHandler) for h in owned)
    file_handler = next(h for h in owned if isinstance(h, logging.FileHandler))
    assert file_handler.baseFilename == str(file_path)

    logging.getLogger('allegrobridge.cadence').info('hello')
    file_handler.flush()
    content = file_path.read_text(encoding='utf-8')
    assert 'allegrobridge.cadence' in content
    assert 'INFO' in content
    assert 'hello' in content


def test_setup_logging_console_false_adds_only_file_handler(tmp_path) -> None:
    setup_logging(console=False, file=tmp_path / 'allegrobridge_server.log')
    owned = [
        h
        for h in logging.getLogger('allegrobridge').handlers
        if getattr(h, '_allegrobridge_owned', False)
    ]
    assert [type(h) for h in owned] == [logging.FileHandler]


def test_setup_logging_is_idempotent(tmp_path) -> None:
    logger = logging.getLogger('allegrobridge')
    setup_logging(file=tmp_path / 'first.log')
    first_owned = [h for h in logger.handlers if getattr(h, '_allegrobridge_owned', False)]
    setup_logging(file=tmp_path / 'second.log')
    owned = [h for h in logger.handlers if getattr(h, '_allegrobridge_owned', False)]
    assert len(owned) == 2
    assert all(h not in first_owned for h in owned)


def test_setup_logging_closes_owned_file_handler_on_replace(tmp_path) -> None:
    logger = logging.getLogger('allegrobridge')
    setup_logging(file=tmp_path / 'first.log')
    first_file = next(h for h in logger.handlers if isinstance(h, logging.FileHandler))
    first_stream = first_file.stream
    assert first_stream is not None
    setup_logging(file=tmp_path / 'second.log')
    assert first_stream.closed is True
    assert first_file not in logger.handlers


def test_setup_logging_preserves_user_handler() -> None:
    user_handler = logging.StreamHandler(io.StringIO())
    logger = logging.getLogger('allegrobridge')
    logger.addHandler(user_handler)
    setup_logging()
    setup_logging()
    assert user_handler in logger.handlers
    assert user_handler.stream.closed is False
    owned = [h for h in logger.handlers if getattr(h, '_allegrobridge_owned', False)]
    assert len(owned) == 1


def test_cadence_child_record_reaches_allegrobridge_handler() -> None:
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
    logging.getLogger('allegrobridge').addHandler(handler)
    logging.getLogger('allegrobridge').setLevel(logging.INFO)

    logging.getLogger('allegrobridge.cadence').info('hello from cadence')

    assert stream.getvalue().rstrip('\n') == 'allegrobridge.cadence hello from cadence'
