# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api.record import (
    Component,
    Drc,
    Net,
    Pin,
)
from allegrobridge.client.base import Collection, SkillModule
from allegrobridge.client.base._rpc import RpcArgs, direct, read, write

_PROCEDURE = '__abProjectDrcs'
_UPDATE_PROCEDURE = '__abUpdateDrcs'
_CHECK_PROCEDURE = '__abCheckDrcs'

_DrcList = list[Drc]
_DRCS = TypeAdapter(_DrcList)


class DrcApi(Collection[Drc]):
    module = SkillModule('allegrobridge.server', 'extensions/drc.il')

    @read(_PROCEDURE, _DRCS)
    def _project(self) -> RpcArgs:
        return ()

    def __call__(self) -> list[Drc]:
        return self.snapshot()

    def _snapshot(self) -> list[Drc]:
        return self._project()

    @write(_UPDATE_PROCEDURE, _DRCS)
    def update(self) -> RpcArgs:
        return ()

    # axlDRCItem mutates marker state that database rollback does not reliably restore.
    # Keep check as one direct RPC: no preview, command, or Batch affordances.
    @direct(_CHECK_PROCEDURE, _DRCS)
    def check(self, target: Component | Net | Pin) -> RpcArgs:
        match target:
            case Component():
                return 'component', target.refdes, None
            case Net():
                return 'net', target.name, None
            case Pin():
                return 'pin', target.refdes, target.number
            case _:
                raise TypeError('target must be Component, Net, or Pin')
