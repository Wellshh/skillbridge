# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections import Counter
from json import dumps
from math import isfinite
from os import getenv
from pathlib import Path
from time import perf_counter, sleep
from typing import cast

from pydantic import TypeAdapter

from allegrobridge import Workspace
from allegrobridge._kernel.client.hints import Skill, SkillCode
from allegrobridge.client.api.routes import RouteInfo
from tests.allegrobridge.probe.drc import _sanitize

_INTERACTION_THRESHOLD = 1.0
_ROUTES = TypeAdapter(list[RouteInfo])


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


def _added_routes(before: dict[str, object], after: dict[str, object]) -> list[dict[str, object]]:
    """Return only route projections absent from the before snapshot."""
    before_keys = Counter(
        dumps(route, sort_keys=True, separators=(',', ':'))
        for route in cast('list[object]', before.get('routes') or [])
    )
    added: list[dict[str, object]] = []
    for route in cast('list[object]', after.get('routes') or []):
        key = dumps(route, sort_keys=True, separators=(',', ':'))
        if before_keys[key]:
            before_keys[key] -= 1
        else:
            added.append(cast('dict[str, object]', route))
    return added


def _validate_route_info(routes: list[dict[str, object]]) -> None:
    _ROUTES.validate_python(routes, strict=True)


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

    @staticmethod
    def build_command(net: str, layer: str, width: float) -> str:
        """Build the only add-connect command used by the structured probes."""
        if (
            not isinstance(net, str)
            or not net.strip()
            or any(
                char.isspace() or char in ';\'"' or ord(char) < 32 or ord(char) == 127
                for char in net
            )
        ):
            raise ValueError('net must be a non-empty name without whitespace')
        if (
            not isinstance(layer, str)
            or not layer.strip()
            or any(
                char.isspace() or char in ';\'"' or ord(char) < 32 or ord(char) == 127
                for char in layer
            )
        ):
            raise ValueError('layer must be a non-empty name without whitespace')
        if not isinstance(width, (int, float)) or not isfinite(width) or width <= 0:
            raise ValueError('width must be a positive finite number')
        return f'add connect -net {net} -layer {layer} -width {width:g}'

    def driven_structured(
        self,
        net: str,
        layer: str,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        report = self.driven(net, self.build_command(net, layer, width), start, end)
        report['added_routes'] = _added_routes(
            cast('dict[str, object]', report['before']),
            cast('dict[str, object]', report['during']),
        )
        _validate_route_info(cast('list[dict[str, object]]', report['added_routes']))
        report['input'] = {
            'net': net,
            'layer': layer,
            'width': width,
            'start': {'x': start[0], 'y': start[1]},
            'end': {'x': end[0], 'y': end[1]},
        }
        return report

    @staticmethod
    def _skill_call(
        procedure: str,
        net: str,
        command: str,
        start: tuple[float, float],
        end: tuple[float, float],
        action: str,
    ) -> SkillCode:
        # Probe inputs are selected from the board and never user-facing raw RPC.
        def quote(value: str) -> str:
            return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'

        return SkillCode(
            f'{procedure}({quote(net)} {quote(command)} '
            f'{start[0]} {start[1]} {end[0]} {end[1]} {quote(action)})'
        )

    def transaction(
        self,
        net: str,
        layer: str,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
        action: str,
    ) -> dict[str, object]:
        command = self.build_command(net, layer, width)
        report = self._call(
            '__abpAddConnectTransaction',
            net,
            command,
            start[0],
            start[1],
            end[0],
            end[1],
            action,
        )
        before = cast('dict[str, object]', report['before'])
        during = cast('dict[str, object]', report['during'])
        terminal = cast('dict[str, object]', report['after'])
        report['added_routes'] = _added_routes(before, during)
        report['terminal_added_routes'] = _added_routes(before, terminal)
        _validate_route_info(cast('list[dict[str, object]]', report['added_routes']))
        _validate_route_info(cast('list[dict[str, object]]', report['terminal_added_routes']))
        report['route_change'] = _classify_route_change(before, during)
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def preview(
        self,
        net: str,
        layer: str,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        command = self.build_command(net, layer, width)
        expr = self._skill_call('__abpAddConnectTransaction', net, command, start, end, 'none')
        try:
            result = self.workspace.transaction.preview(expr)
        except RuntimeError as error:
            return {
                'status': 'error',
                'error': {'type': type(error).__name__, 'message': str(error), 'repr': repr(error)},
            }
        report = cast('dict[str, object]', _sanitize(result))
        report['status'] = 'success'
        report['added_routes'] = _added_routes(
            cast('dict[str, object]', report['before']),
            cast('dict[str, object]', report['during']),
        )
        _validate_route_info(cast('list[dict[str, object]]', report['added_routes']))
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def batch(
        self,
        net: str,
        layer: str,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        command = self.build_command(net, layer, width)
        board_before = self.snapshot(net)
        expr = self._skill_call('__abpAddConnectTransaction', net, command, start, end, 'none')
        try:
            result = self.workspace.transaction.batch([expr])
        except RuntimeError as error:
            return {
                'status': 'error',
                'error': {'type': type(error).__name__, 'message': str(error), 'repr': repr(error)},
            }
        board_after = self.snapshot(net)
        batch_result = _sanitize(result)
        report: dict[str, object] = {'status': 'success', 'batch_result': batch_result}
        report['batch_before_count'] = board_before.get('route_count')
        report['final_count'] = board_after.get('route_count')
        report['added_routes'] = _added_routes(board_before, board_after)
        _validate_route_info(cast('list[dict[str, object]]', report['added_routes']))
        values = batch_result if isinstance(batch_result, list) else []
        inner = values[0].get('value') if values and isinstance(values[0], dict) else None
        if isinstance(inner, dict):
            inner_before = inner.get('before')
            inner_during = inner.get('during')
            report['batch_inner_before_count'] = (
                inner_before.get('route_count') if isinstance(inner_before, dict) else None
            )
            report['batch_inner_during_count'] = (
                inner_during.get('route_count') if isinstance(inner_during, dict) else None
            )
        report['batch_effect'] = (
            'added_routes' if report['added_routes'] else 'no_observable_new_routes'
        )
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def dbid(
        self,
        net: str,
        layer: str,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        command = self.build_command(net, layer, width)
        report = self._call(
            '__abpAddConnectDbidProbe', net, command, start[0], start[1], end[0], end[1]
        )
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def post_driven(
        self,
        net: str,
        layer: str,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> dict[str, object]:
        command = self.build_command(net, layer, width)
        report = self._call(
            '__abpAddConnectPostDriven', net, command, start[0], start[1], end[0], end[1]
        )
        polls = [cast('dict[str, object]', report['immediate'])]
        for _ in range(5):
            sleep(0.2)
            polls.append(self.snapshot(net))
        report['polls'] = polls
        report['final'] = polls[-1]
        report['added_routes'] = _added_routes(
            cast('dict[str, object]', report['before']), polls[-1]
        )
        _validate_route_info(cast('list[dict[str, object]]', report['added_routes']))
        report['ping'] = self.workspace['plus'](1, 2)
        return report

    def post(self, net: str | None, command: str) -> dict[str, object]:
        start = perf_counter()
        report = self._call('__abpAddConnectPost', net, command)
        report['elapsed_seconds'] = perf_counter() - start
        report['fire_and_forget'] = _classify_post(report)
        report['ping'] = self.workspace['plus'](1, 2)
        return report
