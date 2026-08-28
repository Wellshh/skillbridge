# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Static metadata for the Session domain APIs.

Single source of truth for the docs capability matrix and the generated API
index; the explicit ``@cached_property`` accessors on ``Session`` stay as-is.
"""

from __future__ import annotations

from typing import NamedTuple


class DomainInfo(NamedTuple):
    name: str
    capabilities: frozenset[str]
    lazy: bool = False


DOMAINS: tuple[DomainInfo, ...] = (
    DomainInfo("board", frozenset({"read"})),
    DomainInfo("components", frozenset({"read", "write", "preview", "batch"})),
    DomainInfo("layers", frozenset({"read"})),
    DomainInfo("nets", frozenset({"read"})),
    DomainInfo("padstacks", frozenset({"read"})),
    DomainInfo("pins", frozenset({"read"})),
    DomainInfo("symbols", frozenset({"read"})),
    DomainInfo("vias", frozenset({"read", "write", "preview"}), lazy=True),
    DomainInfo("routes", frozenset({"read", "write", "preview"}), lazy=True),
    DomainInfo("shapes", frozenset({"read", "write"}), lazy=True),
    DomainInfo("drc", frozenset({"read", "update"}), lazy=True),
)
