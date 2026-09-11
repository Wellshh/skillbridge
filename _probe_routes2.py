# Round-2 directed probes: space-containing net name, -layer format, width clamping.
# Fresh disposable board copy + owned Allegro CLI process + unique port.
# Evidence: probe_evidence/report2.json (written incrementally).
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from shutil import copy2
from time import sleep

from allegrobridge import Allegro
from allegrobridge._kernel import SkillCode
from allegrobridge.util import ASSETS_DIR

import _probe_routes as pr

BOARD = ASSETS_DIR / 'shape1.brd'
OUT = Path('probe_evidence')

NET_EXISTS = (
    '(let ((found nil)) '
    '(foreach n (axlDBRefreshId (axlDBGetDesign))->nets '
    '(when (equal n->name "MY NET") (setq found t))) found)'
)


def rows_for_net(ws, net):
    return [r for r in pr.snapshot(ws) if r[0] == net]


def try_manual_connect(ws, net, layer, width_text, pairs, quote_net=True, label=''):
    """Run manual_connect over candidate point pairs until copper appears on `net`."""
    attempts = []
    for p0, p1 in pairs:
        res = pr.manual_connect(ws, net, layer, width_text, p0, p1, quote_net=quote_net)
        mine = [r for r in res['db_added'] if r[0] == net]
        attempts.append({
            'pair': [list(p0), list(p1)],
            'mine_added': [list(r) for r in mine],
            'db_added_n': len(res['db_added']),
            'db_removed_n': len(res['db_removed']),
            'command': res['command'],
            'shell_result': res['shell_result'],
        })
        if mine:
            return {
                'label': label,
                'layer_requested': layer,
                'width_requested': width_text,
                'quote_net': quote_net,
                'attempts': attempts,
                'success_pair': [list(p0), list(p1)],
            }
    return {
        'label': label,
        'layer_requested': layer,
        'width_requested': width_text,
        'quote_net': quote_net,
        'attempts': attempts,
        'success_pair': None,
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    report: dict = {}
    report_file = OUT / 'report2.json'

    def save() -> None:
        report_file.write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')

    tmp = Path(tempfile.mkdtemp(prefix='ab-routes-probe2-'))
    (tmp / 'logs').mkdir(exist_ok=True)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = (tmp / 'logs').as_posix()
    board = Path(copy2(BOARD, tmp))
    port_id = pr._free_port_id()
    print(f'[probe2] launching Allegro CLI, workspace_id={port_id}, board={board}', flush=True)
    with Allegro.open(mode='cli', board=board, workspace_id=port_id) as allegro:
        session = allegro.session
        ws = allegro.workspace
        try:
            # --- create a fresh net with a space in its name (transactional write) ---
            report['create_net'] = str(ws.transaction(SkillCode('(axlDBCreateNet "MY NET")')))
            report['net_exists'] = pr.ev(ws, NET_EXISTS)
            save()
            print(f"[probe2] net created: exists={report['net_exists']}", flush=True)

            # candidate empty-area pairs (away from known pins 1200-3500 x 500-2640)
            pairs_a = [
                ((2800.0, 2000.0), (3000.0, 2200.0)),
                ((2200.0, 650.0), (2400.0, 650.0)),
                ((1600.0, 2400.0), (1700.0, 2500.0)),
            ]
            pairs_b = [
                ((2800.0, 2300.0), (3000.0, 2500.0)),
                ((2200.0, 750.0), (2400.0, 750.0)),
                ((1600.0, 2200.0), (1700.0, 2300.0)),
            ]

            # --- P5: space-containing net, quoted, layer ETCH/TOP, width 50 ---
            report['p5_space_net_quoted'] = try_manual_connect(
                ws, 'MY NET', 'ETCH/TOP', '50', pairs_a, quote_net=True, label='space_net_quoted'
            )
            save()
            print('[probe2] p5 done', flush=True)

            # --- P5b: control - unquoted space net (expected to fail/misparse) ---
            report['p5b_space_net_unquoted'] = try_manual_connect(
                ws,
                'MY NET',
                'ETCH/TOP',
                '50',
                [pairs_b[0]],
                quote_net=False,
                label='space_net_unquoted',
            )
            save()
            print('[probe2] p5b done', flush=True)

            # --- P6: layer format - short subclass name "TOP" ---
            mine_before = rows_for_net(ws, 'MY NET')
            report['p6_layer_short_name'] = try_manual_connect(
                ws, 'MY NET', 'TOP', '50', pairs_b, quote_net=True, label='layer_TOP'
            )
            report['p6_rows_before'] = [list(r) for r in mine_before]
            save()
            print('[probe2] p6 done', flush=True)

            # --- P7: width clamping on the fresh net (tiny width, same layer as P5) ---
            pairs_c = [((3100.0, 2000.0), (3200.0, 2100.0)), ((1450.0, 2450.0), (1550.0, 2550.0))]
            report['p7_width_tiny'] = try_manual_connect(
                ws, 'MY NET', 'ETCH/TOP', '0.0001', pairs_c, quote_net=True, label='width_0.0001'
            )
            save()
            print('[probe2] p7 done', flush=True)

            report['final_my_net_rows'] = [list(r) for r in rows_for_net(ws, 'MY NET')]
            report['final_tees_my_net'] = [t for t in pr.ev(ws, pr.TEES) if t[0] == 'MY NET']
            save()
        except Exception as exc:  # noqa: BLE001 - keep partial evidence
            report['fatal'] = f'{type(exc).__name__}: {exc}'
            save()
            raise
    print(f'[probe2] report written to {report_file.resolve()}', flush=True)


if __name__ == '__main__':
    main()
