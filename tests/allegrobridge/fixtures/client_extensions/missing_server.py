# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.api import RpcArgs, SessionApi, SkillModule, read


class MissingServerApi(SessionApi):
    module = SkillModule('tests.allegrobridge.fixtures', 'server/extensions/missing.il')

    @read('__abp_missing_server_probe', TypeAdapter(int))
    def probe(self) -> RpcArgs:
        return ()
