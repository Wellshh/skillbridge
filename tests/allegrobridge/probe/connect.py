# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from json import dumps
from os import getenv
from pathlib import Path
from time import perf_counter
from typing import cast

from allegrobridge import Workspace
from allegrobridge._kernel.client.hints import Skill
from tests.allegrobridge.probe.drc import _sanitize

_INTERACTION_THRESHOLD = 1.0


def _route_fingerprint(snapshot: dict[str, object]) -> tuple[str, ...]:
    routes = cast('list[object]', snapshot['routes'] or [])
    return tuple(sorted(dumps(route, sort_keys=True, separators=(',', ':')) for route in routes))


def _classify_route_change(before: dict[str, object], during: dict[str, object]) -> str:
    if _route_fingerprint(during) != _route_fingerprint(before):
        return 'done'
    return 'cancel'


def _classify_activity(mid: dict[str, object], during: dict[str, object]) -> str:
    if _route_fingerprint(during) != _route_fingerprint(mid):
        return 'active'
    return 'cancelled'


def _classify_blocking(
    report: dict[str, object],
    *,
    threshold: float = _INTERACTION_THRESHOLD,
) -> str:
    before = cast('dict[str, object]', report['before'])
    during = cast('dict[str, object]', report['during'])
    elapsed = cast('float', report['elapsed_seconds'])
    if _route_fingerprint(during) != _route_fingerprint(before):
        return 'blocking_done'
    if elapsed < threshold:
        return 'non_blocking'
    return 'blocking_cancel'


def _classify_post(report: dict[str, object]) -> bool:
    before = cast('dict[str, object]', report['before'])
    immediate = cast('dict[str, object]', report['immediate'])
    return _route_fingerprint(immediate) == _route_fingerprint(before)


class ConnectProbe:
    def __init__(self, workspace: Workspace) -> None:
        self.workspace = workspace
        workspace['load'](Path(__file__).with_suffix('.il').resolve().as_posix())

    def _call(self, procedure: str, *args: Skill) -> dict[str, object]:
        payload = self.workspace[procedure](*args)
        if not isinstance(payload, dict):
            raise TypeError(f'{procedure} returned {type(payload).__name__}, expected dict')
        report = cast('dict[str, object]', _sanitize(payload))
        dumps(report)
        return report

    @staticmethod
    def emit(filename: str, report: dict[str, object]) -> None:
        payload = dumps(report, sort_keys=True, separators=(',', ':'))
        print(payload)
        if output_directory := getenv('ALLEGRO_CONNECT_PROBE_OUTPUT_DIR'):
            path = Path(output_directory)
            path.mkdir(parents=True, exist_ok=True)
            (path / filename).write_text(payload + '\n', encoding='utf-8')

    def snapshot(self, net: str | None = None) -> dict[str, object]:
        return self._call('__abpRouteSnapshot', net)

    def blocking(self, net: str | None, command: str) -> dict[str, object]:
        start = perf_counter()
        report = self._call('__abpAddConnectRun', net, command)
        report['elapsed_seconds'] = perf_counter() - start
        before = cast('dict[str, object]', report['before'])
        during = cast('dict[str, object]', report['during'])
        report['route_change'] = _classify_route_change(before, during)
        report['blocking_semantics'] = _classify_blocking(report)
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def active(
        self,
        net: str | None,
        command: str,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        start_time = perf_counter()
        launch = self._call('__abpAddConnectRun', net, command)
        drive = self._call(
            '__abpAddConnectActiveDrive',
            net,
            start[0],
            start[1],
            end[0],
            end[1],
        )
        before = cast('dict[str, object]', launch['before'])
        mid = cast('dict[str, object]', launch['during'])
        during = cast('dict[str, object]', drive['during'])
        report: dict[str, object] = {
            'allegro_version': launch['allegro_version'],
            'before': before,
            'mid': mid,
            'during': during,
        }
        report['elapsed_seconds'] = perf_counter() - start_time
        report['route_change'] = _classify_route_change(before, mid)
        report['activity'] = _classify_activity(mid, during)
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def driven(
        self,
        net: str | None,
        command: str,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        start_time = perf_counter()
        report = self._call(
            '__abpAddConnectDriven',
            net,
            command,
            start[0],
            start[1],
            end[0],
            end[1],
        )
        report['elapsed_seconds'] = perf_counter() - start_time
        before = cast('dict[str, object]', report['before'])
        during = cast('dict[str, object]', report['during'])
        report['route_change'] = _classify_route_change(before, during)
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def post(self, net: str | None, command: str) -> dict[str, object]:
        start = perf_counter()
        report = self._call('__abpAddConnectPost', net, command)
        report['elapsed_seconds'] = perf_counter() - start
        report['fire_and_forget'] = _classify_post(report)
        report['ping'] = self.workspace['plus'](1, 2)
        return report
