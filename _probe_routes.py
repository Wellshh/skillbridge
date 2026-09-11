# One-shot directed probes for routes.connect() edge behavior (NOT a committed test).
# Disposable board copy + owned Allegro CLI process + unique port per AGENTS.md.
# Evidence: probe_evidence/report.json (written incrementally after each probe).
from __future__ import annotations

import json
import os
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path
from shutil import copy2
from socket import socket
from time import sleep
from typing import Any

from allegrobridge import Allegro
from allegrobridge._kernel import SkillCode
from allegrobridge.util import ASSETS_DIR

BOARD = ASSETS_DIR / 'shape1.brd'
OUT = Path('probe_evidence')

SNAPSHOT = (
    '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
    '(foreach netObject design->nets '
    '(foreach branch netObject->branches '
    '(foreach path branch->children '
    '(when (and (equal path->objType "path") path->isEtch) '
    '(foreach segment path->segments '
    '(when (or (equal segment->objType "line") (equal segment->objType "arc")) '
    '(let ((ends segment->startEnd)) '
    '(setq result (cons '
    '(list netObject->name segment->layer '
    '(car (car ends)) (cadr (car ends)) '
    '(car (cadr ends)) (cadr (cadr ends)) segment->width) result))))))))) '
    '(foreach branch (axlDBGetLonelyBranches) '
    '(foreach path branch->children '
    '(when (and (equal path->objType "path") path->isEtch) '
    '(foreach segment path->segments '
    '(when (or (equal segment->objType "line") (equal segment->objType "arc")) '
    '(let ((ends segment->startEnd)) '
    '(setq result (cons '
    '(list nil segment->layer '
    '(car (car ends)) (cadr (car ends)) '
    '(car (cadr ends)) (cadr (cadr ends)) segment->width) result)))))))) '
    '(reverse result))'
)

# net -> branches -> placed pin coordinates, to tell which pin pairs are already connected
BRANCH_PINS = (
    '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
    '(foreach netObject design->nets '
    '(foreach branch netObject->branches '
    '(let (coords) '
    '(foreach child branch->children '
    '(when (and (equal child->objType "pin") child->xy) '
    '(setq coords (cons (list (car child->xy) (cadr child->xy)) coords)))) '
    '(when coords '
    '(setq result (cons (list netObject->name coords) result)))))) '
    'result)'
)

TEES = (
    '(letseq ((design (axlDBRefreshId (axlDBGetDesign))) result) '
    '(foreach netObject design->nets '
    '(foreach branch netObject->branches '
    '(foreach child branch->children '
    '(when (and (equal child->objType "tee") child->xy) '
    '(setq result (cons (list netObject->name (car child->xy) (cadr child->xy)) '
    'result)))))) '
    '(reverse result))'
)


def _free_port_id() -> str:
    with socket() as listener:
        listener.bind(('localhost', 0))
        return str(listener.getsockname()[1])


def ev(ws: Any, code: str) -> Any:
    return ws['evalstring'](code)


def snapshot(ws: Any) -> list[tuple[Any, ...]]:
    return [tuple(row) for row in ev(ws, SNAPSHOT)]


def diff(before: list[tuple], after: list[tuple]) -> tuple[list[tuple], list[tuple]]:
    remaining = Counter(before)
    added = []
    for row in after:
        if remaining[row]:
            remaining[row] -= 1
        else:
            added.append(row)
    remaining2 = Counter(after)
    removed = []
    for row in before:
        if remaining2[row]:
            remaining2[row] -= 1
        else:
            removed.append(row)
    return added, removed


def api_connect(
    session: Any, ws: Any, net: str, p0: tuple, p1: tuple, layer: str, width: float
) -> dict:
    before = snapshot(ws)
    tees_before = ev(ws, TEES)
    try:
        added = session.routes.connect(
            net, (float(p0[0]), float(p0[1])), (float(p1[0]), float(p1[1])), layer, width
        )
        outcome: dict = {'status': 'ok', 'returned': [r.model_dump(mode='json') for r in added]}
    except Exception as exc:  # noqa: BLE001 - probe records everything
        outcome = {'status': 'error', 'type': type(exc).__name__, 'message': str(exc)}
    db_added, db_removed = [], []
    for _ in range(6):
        after = snapshot(ws)
        db_added, db_removed = diff(before, after)
        if db_added or db_removed:
            break
        sleep(0.5)
    outcome.update({
        'requested': {
            'net': net,
            'layer': layer,
            'width': width,
            'start': list(p0),
            'end': list(p1),
        },
        'db_added': [list(r) for r in db_added],
        'db_removed': [list(r) for r in db_removed],
        'tees_before': tees_before,
        'tees_after': ev(ws, TEES),
    })
    return outcome


def manual_connect(
    ws: Any,
    net: str,
    layer: str,
    width_text: str,
    p0: tuple,
    p1: tuple,
    quote_net: bool = False,
    quote_layer: bool = False,
) -> dict:
    n = f'"{net}"' if quote_net else net
    lay = f'"{layer}"' if quote_layer else layer
    cmd = (
        f'add connect -net {n} -layer {lay} -width {width_text}; '
        f'pick {p0[0]!r} {p0[1]!r}; pick {p1[0]!r} {p1[1]!r}; done'
    )
    escaped = cmd.replace('\\', '\\\\').replace('"', '\\"')
    before = snapshot(ws)
    shell_result = ev(ws, f'(axlShell "{escaped}")')
    ws.transaction(SkillCode('t'))
    added, removed = [], []
    for _ in range(6):
        after = snapshot(ws)
        added, removed = diff(before, after)
        if added or removed:
            break
        sleep(0.5)
    return {
        'command': cmd,
        'shell_result': shell_result,
        'db_added': [list(r) for r in added],
        'db_removed': [list(r) for r in removed],
    }


def probe0_formats_and_grid(ws: Any) -> dict:
    out: dict = {}
    for w in ('0.2', '0.0001', '1e-5', '1e-6', '1e-7', '0.000001', '12345678.9'):
        try:
            out[f'lsprintf_L[{w}]'] = ev(ws, f'(lsprintf "%L" {w})')
        except Exception as exc:  # noqa: BLE001
            out[f'lsprintf_L[{w}]'] = f'ERROR {exc}'
    out['lsprintf_L["MY NET"]'] = ev(ws, '(lsprintf "%L" "MY NET")')
    try:
        out['grid_names'] = ev(ws, '(axlDBGridGet nil)')
    except Exception as exc:  # noqa: BLE001
        out['grid_names'] = f'ERROR {exc}'
    for name in ('ETCH/TOP', 'TOP'):
        try:
            out[f'grid[{name}]'] = ev(ws, f'(axlDBGridGet "{name}")')
        except Exception as exc:  # noqa: BLE001
            out[f'grid[{name}]'] = f'ERROR {exc}'
    for sub in ('TOP', 'ETCH/TOP'):
        try:
            out[f'minLineWidth[{sub}]'] = ev(ws, f'(axlCNSGetDefaultMinLineWidth "{sub}")')
        except Exception as exc:  # noqa: BLE001
            out[f'minLineWidth[{sub}]'] = f'ERROR {exc}'
    return out


def grid_offset(p0: dict, default: float = 0.0137) -> float:
    for key in ('grid[ETCH/TOP]', 'grid[TOP]'):
        g = p0.get(key)
        xg = None
        if isinstance(g, dict):
            xg = g.get('xGrids')
        elif isinstance(g, (list, tuple)):  # disembodied plist: ['xGrids', [...], ...]
            for i, item in enumerate(g):
                if item in ('xGrids', 'xgrids') and i + 1 < len(g):
                    xg = g[i + 1]
        if isinstance(xg, (list, tuple)) and xg:
            try:
                value = float(xg[0])
                if value > 0:
                    return value / 3.0
            except (TypeError, ValueError):
                pass
    return default


def enumerate_resources(session: Any, ws: Any) -> dict:
    nets = [n.model_dump(mode='json') for n in session.nets()]
    pins_by_net: dict[str, list[tuple[float, float, str, str]]] = {}
    for entry in nets:
        name = entry['name']
        pins = [p for p in session.pins(net=name) if p.placement == 'placed' and p.x is not None]
        if len(pins) >= 2:
            pins_by_net[name] = [(float(p.x), float(p.y), p.refdes, p.number) for p in pins]
    branch = ev(ws, BRANCH_PINS)
    connected: set[tuple[str, tuple[float, float], tuple[float, float]]] = set()
    for entry in branch:
        netname, coords = entry[0], entry[1]
        pts = [(round(float(c[0]), 5), round(float(c[1]), 5)) for c in coords]
        for a, b in combinations(pts, 2):
            connected.add((netname, a, b))
            connected.add((netname, b, a))
    free: dict[str, list[tuple[tuple, tuple]]] = {}
    for netname, pins in pins_by_net.items():
        pairs = []
        for a, b in combinations(pins, 2):
            ka = (round(a[0], 5), round(a[1], 5))
            kb = (round(b[0], 5), round(b[1], 5))
            if (netname, ka, kb) not in connected:
                pairs.append((a, b))
        if pairs:
            free[netname] = pairs
    routes_by_net: dict[str, dict] = {}
    for netname in pins_by_net:
        rs = session.routes(net=netname)
        if rs:
            routes_by_net[netname] = {'layer': rs[0].layer, 'width': rs[0].width}
    layers = [lay.model_dump(mode='json') for lay in session.layers()]
    etch_layers = [
        lay['name'] for lay in layers if lay.get('class_name') == 'ETCH' or lay.get('is_etch')
    ]
    return {
        'nets': nets,
        'pins_by_net': {k: [list(p) for p in v] for k, v in pins_by_net.items()},
        'branch_pins_raw': branch,
        'free_pairs': {k: len(v) for k, v in free.items()},
        'routes_by_net': routes_by_net,
        'etch_layers': etch_layers,
    }, free


class Budget:
    """Hands out fresh pin pairs; each successful connect consumes a pair."""

    def __init__(self, free: dict[str, list[tuple[tuple, tuple]]]) -> None:
        self._free = {k: list(v) for k, v in free.items()}

    def counts(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._free.items()}

    def take(self, net: str | None = None) -> tuple[str, tuple, tuple] | None:
        candidates = sorted(self._free.items(), key=lambda kv: -len(kv[1]))
        if net is not None:
            candidates = [(k, v) for k, v in candidates if k == net]
        for name, pairs in candidates:
            if pairs:
                a, b = pairs.pop(0)
                return name, a, b
        return None

    def restore(self, net: str, pair: tuple[tuple, tuple]) -> None:
        self._free.setdefault(net, []).append(pair)


def default_layer_width(res: dict, net: str) -> tuple[str, float]:
    info = res['routes_by_net'].get(net)
    if info:
        return info['layer'], float(info['width'])
    etch = res['etch_layers']
    layer = 'ETCH/TOP' if 'ETCH/TOP' in etch else (etch[0] if etch else 'ETCH/TOP')
    return layer, 0.2


def probe1_grid_snap(session, ws, res, budget, p0) -> dict:
    out: dict = {}
    off = grid_offset(p0)
    out['offset_used'] = off

    # case A: exact pin-to-pin control
    take = budget.take()
    if take:
        net, a, b = take
        layer, width = default_layer_width(res, net)
        out['A_exact_pins'] = api_connect(session, ws, net, a[:2], b[:2], layer, width)
    else:
        out['A_exact_pins'] = 'SKIPPED_NO_PAIRS'

    # case C first (midair, likely no-op so the pair survives), then B on the same pair
    take = budget.take()
    if take:
        net, a, b = take
        layer, width = default_layer_width(res, net)
        midair0 = (a[0] + 37.5 + off, a[1] + 21.5 - off)
        midair1 = (b[0] - 37.5 + off, b[1] - 21.5 - off)
        out['C_midair'] = api_connect(session, ws, net, midair0, midair1, layer, width)
        if not out['C_midair'].get('db_added'):
            # pair not consumed -> reuse for B with off-grid offsets around the pins
            bx0 = (a[0] + off, a[1] - off)
            bx1 = (b[0] - off, b[1] + off)
            out['B_offgrid_near_pins'] = api_connect(session, ws, net, bx0, bx1, layer, width)
        else:
            budget.restore(net, (a, b))  # consumed anyway; keep books honest
            take2 = budget.take()
            if take2:
                net2, a2, b2 = take2
                layer2, width2 = default_layer_width(res, net2)
                out['B_offgrid_near_pins'] = api_connect(
                    session,
                    ws,
                    net2,
                    (a2[0] + off, a2[1] - off),
                    (b2[0] - off, b2[1] + off),
                    layer2,
                    width2,
                )
            else:
                out['B_offgrid_near_pins'] = 'SKIPPED_NO_PAIRS'
    else:
        out['C_midair'] = 'SKIPPED_NO_PAIRS'
        out['B_offgrid_near_pins'] = 'SKIPPED_NO_PAIRS'
    return out


def probe2_t_junction(session, ws, res, budget, p0) -> dict:
    pins_by_net = {k: [tuple(p) for p in v] for k, v in res['pins_by_net'].items()}
    net = None
    for name, count in sorted(budget.counts().items(), key=lambda kv: -kv[1]):
        if len(pins_by_net.get(name, [])) >= 3 and count >= 1:
            net = name
            break
    if net is None:
        return {
            'status': 'SKIPPED_NEED_NET_WITH_3_PINS',
            'pin_counts': {k: len(v) for k, v in pins_by_net.items()},
            'free_pair_counts': budget.counts(),
        }
    pins = pins_by_net[net]
    layer, width = default_layer_width(res, net)
    out: dict = {'net': net, 'layer': layer, 'width': width, 'pins': [list(p) for p in pins]}
    # baseline: connect a known-unconnected pin pair through the API
    take = budget.take(net)
    if take is None:
        out['baseline'] = 'SKIPPED_NO_PAIR'
        return out
    _, a, b = take
    out['baseline'] = api_connect(session, ws, net, a[:2], b[:2], layer, width)
    # find a segment of this net to T into: prefer one just created
    rows = out['baseline'].get('db_added') or [list(r) for r in snapshot(ws) if r[0] == net]
    if not rows:
        out['t_step'] = 'SKIPPED_NO_SEGMENT'
        return out
    seg = max(
        rows,
        key=lambda r: ((float(r[2]) - float(r[4])) ** 2 + (float(r[3]) - float(r[5])) ** 2) ** 0.5,
    )
    mid = ((float(seg[2]) + float(seg[4])) / 2.0, (float(seg[3]) + float(seg[5])) / 2.0)
    target = max(pins, key=lambda p: (p[0] - mid[0]) ** 2 + (p[1] - mid[1]) ** 2)
    out['t_segment'] = list(seg)
    out['t_mid'] = list(mid)
    out['t_target_pin'] = list(target)
    out['t_step'] = api_connect(session, ws, net, mid, target[:2], layer, width)
    return out


def probe3_quoted_net(ws, res, budget) -> dict:
    out: dict = {}
    take = budget.take()
    if not take:
        return {'quoted_net': 'SKIPPED_NO_PAIRS'}
    net, a, b = take
    layer, width = default_layer_width(res, net)
    out['quoted_net'] = manual_connect(ws, net, layer, repr(width), a[:2], b[:2], quote_net=True)
    if not out['quoted_net']['db_added']:
        budget.restore(net, (a, b))
        take = budget.take()
        if take:
            net, a, b = take
            layer, width = default_layer_width(res, net)
            out['quoted_net_and_layer'] = manual_connect(
                ws, net, layer, repr(width), a[:2], b[:2], quote_net=True, quote_layer=True
            )
            if not out['quoted_net_and_layer']['db_added']:
                budget.restore(net, (a, b))
                # unquoted control on the same pair to prove the pair was routable
                out['unquoted_control'] = manual_connect(ws, net, layer, repr(width), a[:2], b[:2])
    return out


def probe4_tiny_width(ws, res, budget) -> dict:
    out: dict = {}
    for label, width_text in (('positional_0.0001', '0.0001'), ('exponent_1e-07', '1e-07')):
        take = budget.take()
        if not take:
            out[label] = 'SKIPPED_NO_PAIRS'
            continue
        net, a, b = take
        layer, _ = default_layer_width(res, net)
        result = manual_connect(ws, net, layer, width_text, a[:2], b[:2])
        result['widths_readback'] = sorted({r[6] for r in result['db_added']})
        out[label] = result
        if not result['db_added']:
            budget.restore(net, (a, b))
    return out


def main() -> None:
    OUT.mkdir(exist_ok=True)
    report: dict = {}
    report_file = OUT / 'report.json'

    def save() -> None:
        report_file.write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')

    tmp = Path(tempfile.mkdtemp(prefix='ab-routes-probe-'))
    (tmp / 'logs').mkdir(exist_ok=True)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = (tmp / 'logs').as_posix()
    board = Path(copy2(BOARD, tmp))
    port_id = _free_port_id()
    print(f'[probe] launching Allegro CLI, workspace_id={port_id}, board={board}', flush=True)
    with Allegro.open(mode='cli', board=board, workspace_id=port_id) as allegro:
        session = allegro.session
        ws = allegro.workspace
        try:
            report['p0_formats_and_grid'] = probe0_formats_and_grid(ws)
            save()
            print('[probe] p0 done', flush=True)

            res, free = enumerate_resources(session, ws)
            report['resources'] = res
            save()
            print(f"[probe] resources: free_pairs={res['free_pairs']}", flush=True)
            budget = Budget(free)

            p0 = report['p0_formats_and_grid']
            report['p1_grid_snap'] = probe1_grid_snap(session, ws, res, budget, p0)
            save()
            print('[probe] p1 done', flush=True)

            report['p2_t_junction'] = probe2_t_junction(session, ws, res, budget, p0)
            save()
            print('[probe] p2 done', flush=True)

            report['p3_quoted_net'] = probe3_quoted_net(ws, res, budget)
            save()
            print('[probe] p3 done', flush=True)

            report['p4_tiny_width'] = probe4_tiny_width(ws, res, budget)
            save()
            print('[probe] p4 done', flush=True)
        except Exception as exc:  # noqa: BLE001 - keep partial evidence
            report['fatal'] = f'{type(exc).__name__}: {exc}'
            save()
            raise
    print(f'[probe] report written to {report_file.resolve()}', flush=True)


if __name__ == '__main__':
    main()
