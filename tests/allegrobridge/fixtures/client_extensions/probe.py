# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api import (
    ComponentInfo,
    RpcArgs,
    SessionApi,
    SkillModule,
    read,
    write,
)

_COMPONENTS = TypeAdapter(list[ComponentInfo])
_COMPONENT = TypeAdapter(ComponentInfo)


class ProbeApi(SessionApi):
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/probe.il')

    @read('__abp_probe_project', _COMPONENTS)
    def __call__(self) -> RpcArgs:
        return ()

    @write('__abp_probe_move', _COMPONENT)
    def move(
        self,
        refdes: str,
        *,
        x: float,
        y: float,
        rotation: float | None = None,
    ) -> RpcArgs:
        return refdes, x, y, rotation
