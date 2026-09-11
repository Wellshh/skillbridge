# Round-3 directed probes: space-net via axlRenameNet, -layer honoring, width clamping.
# Fresh disposable board copy + owned Allegro CLI process + unique port.
# Evidence: probe_evidence/report3.json (written incrementally).
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from shutil import copy2

from allegrobridge import Allegro
from allegrobridge._kernel import SkillCode
from allegrobridge.util import ASSETS_DIR

import _probe_routes as pr

BOARD = ASSETS_DIR / 'shape1.brd'
OUT = Path('probe_evidence')

NET_SCAN = (
    '(let (found) '
    '(foreach n (axlDBRefreshId (axlDBGetDesign))->nets '
    '(when (or (equal n->name "NET24") (equal n->name "NET 24")) '
    '(setq found (cons n->name found)))) found)'
)


def rows_for(ws, net):
    return [r for r in pr.snapshot(ws) if r[0] == net]


def summarize(res, net):
    mine_added = [list(r) for r in res['db_added'] if r[0] == net]
    mine_removed = [list(r) for r in res['db_removed'] if r[0] == net]
    other_added = len(res['db_added']) - len(mine_added)
    return {
        'command': res['command'],
        'shell_result': res['shell_result'],
        'mine_added': mine_added,
        'mine_removed': mine_removed,
        'other_added_n': other_added,
        'added_layers': sorted({r[1] for r in mine_added}),
        'added_widths': sorted({r[6] for r in mine_added}),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    report: dict = {}
    report_file = OUT / 'report3.json'

    def save() -> None:
        report_file.write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')

    tmp = Path(tempfile.mkdtemp(prefix='ab-routes-probe3-'))
    (tmp / 'logs').mkdir(exist_ok=True)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = (tmp / 'logs').as_posix()
    board = Path(copy2(BOARD, tmp))
    port_id = pr._free_port_id()
    print(f'[probe3] launching Allegro CLI, workspace_id={port_id}, board={board}', flush=True)
    with Allegro.open(mode='cli', board=board, workspace_id=port_id) as allegro:
        session = allegro.session
        ws = allegro.workspace
        try:
            res, free = pr.enumerate_resources(session, ws)
            report['free_pairs'] = res['free_pairs']
            save()
            budget = pr.Budget(free)

            # --- P8: rename NET24 -> "NET 24", then quoted connect on its pins ---
            report['p8_rename_result'] = str(
                ws.transaction(SkillCode('(axlRenameNet "NET24" "NET 24")'))
            )
            report['p8_net_scan'] = pr.ev(ws, NET_SCAN)
            save()
            print(
                f"[probe3] p8 rename: {report['p8_rename_result']} scan={report['p8_net_scan']}",
                flush=True,
            )

            take = budget.take('NET24')
            if take and report['p8_net_scan'] == ['NET 24']:
                _, a, b = take
                r = pr.manual_connect(ws, 'NET 24', 'ETCH/TOP', '12', a[:2], b[:2], quote_net=True)
                report['p8_space_net_quoted'] = summarize(r, 'NET 24')
                report['p8_space_net_quoted']['pair'] = [list(a), list(b)]
                save()
                print('[probe3] p8 quoted done', flush=True)
                # control: unquoted space net on another pair (expect parser breakage)
                take2 = budget.take('NET24')
                if take2:
                    _, a2, b2 = take2
                    r2 = pr.manual_connect(
                        ws, 'NET 24', 'ETCH/TOP', '12', a2[:2], b2[:2], quote_net=False
                    )
                    report['p8b_space_net_unquoted'] = summarize(r2, 'NET 24')
                    report['p8b_space_net_unquoted']['pair'] = [list(a2), list(b2)]
                    save()
                    print('[probe3] p8b unquoted done', flush=True)
            else:
                report['p8_space_net_quoted'] = (
                    f"SKIPPED rename={report['p8_rename_result']} "
                    f"scan={report['p8_net_scan']} take={take}"
                )
                save()

            # --- P9: layer honoring on VCC ---
            for label, layer in (
                ('p9_layer_ETCH_BOTTOM', 'ETCH/BOTTOM'),
                ('p9b_layer_short_BOTTOM', 'BOTTOM'),
            ):
                take = budget.take('VCC')
                if not take:
                    report[label] = 'SKIPPED_NO_PAIR'
                    continue
                _, a, b = take
                r = pr.manual_connect(ws, 'VCC', layer, '25', a[:2], b[:2])
                report[label] = summarize(r, 'VCC')
                report[label]['pair'] = [list(a), list(b)]
                if not report[label]['mine_added']:
                    budget.restore('VCC', (a, b))
                save()
                print(f'[probe3] {label} done', flush=True)

            # --- P10: width honoring/clamping on VCC ---
            for label, width_text in (('p10_width_50', '50'), ('p10b_width_5', '5')):
                take = budget.take('VCC')
                if not take:
                    report[label] = 'SKIPPED_NO_PAIR'
                    continue
                _, a, b = take
                r = pr.manual_connect(ws, 'VCC', 'ETCH/TOP', width_text, a[:2], b[:2])
                report[label] = summarize(r, 'VCC')
                report[label]['pair'] = [list(a), list(b)]
                if not report[label]['mine_added']:
                    budget.restore('VCC', (a, b))
                save()
                print(f'[probe3] {label} done', flush=True)

            report['final_space_net_rows'] = [list(r) for r in rows_for(ws, 'NET 24')]
            save()
        except Exception as exc:  # noqa: BLE001 - keep partial evidence
            report['fatal'] = f'{type(exc).__name__}: {exc}'
            save()
            raise
    print(f'[probe3] report written to {report_file.resolve()}', flush=True)


if __name__ == '__main__':
    main()
