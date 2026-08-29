# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SkillModule:
    """Packaged SKILL (.il) resource location for a SessionApi extension.
    Attributes:
        package: The Python package name containing the resource (e.g. 'allegrobridge.server').
        resource: Relative path to the .il file within the package (e.g. 'extensions/vias.il').
    """

    package: str
    resource: str
