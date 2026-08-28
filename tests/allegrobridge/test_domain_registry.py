# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from functools import cached_property

from allegrobridge import Session
from allegrobridge.client.session.domains import DOMAINS


def test_registry_covers_session_properties() -> None:
    expected = {
        'board',
        'components',
        'layers',
        'nets',
        'padstacks',
        'pins',
        'symbols',
        'vias',
        'routes',
        'shapes',
        'drc',
    }
    assert {d.name for d in DOMAINS} == expected
    assert len(DOMAINS) == 11


def test_registry_names_are_real_session_properties() -> None:
    for domain in DOMAINS:
        assert isinstance(getattr(Session, domain.name, None), (property, cached_property)), (
            domain.name
        )


def test_lazy_domains_match_extension_loaders() -> None:
    lazy = {d.name for d in DOMAINS if d.lazy}
    assert lazy == {'vias', 'routes', 'shapes', 'drc'}


def test_capabilities_nonempty_and_known() -> None:
    known = {'read', 'write', 'preview', 'batch', 'update'}
    for domain in DOMAINS:
        assert domain.capabilities, domain.name
        assert domain.capabilities <= known, domain.name
