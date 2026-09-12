# Probe D diagnostic: ONE fresh-process reopen attempt.
#
# usage: python probe_d_attempt.py <workdir> <board> <port> <tag>
#
# Opens <board> exactly like probe_d's S2/S3 sessions (Allegro.open cli +
# content verify), records doc-supported load observables:
#   axlCurrentDesign() / axlGetDrawingName()  -- "there is always a current
#       design, even unnamed" (14dsnctl.md); ->name is NOT a design dbid
#       attribute, which is why earlier probes saw None even when loaded.
#   axlLicIsProductEnabled('all)              -- checked-out license list.
# If the startup design is EMPTY, tries the documented in-session reset
# (axlKillDesign() == axlOpenDesign(<unnamed> "wf")) then one
# axlOpenDesign retry, recording errset.errset.  Exit 0 if arcs>=1 else 2.
# This is a read retry of an *open*; never a failed-write replay.
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
for _p in (str(HERE), r'D:\AutoPlacer\skillbridge'):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import probe_c as pc
import probe_d as pd
from allegrobridge import Allegro


def ev(ws, payload):
    try:
        return ws['evalstring'](payload)
    except Exception as exc:  # noqa: BLE001 - diagnostic, keep going
        return f'ERROR {exc!r}'


def observe(session, tag, phase):
    ws = session.workspace
    rows = session.routes(layer=pc.LAYER)
    n_arcs = sum(1 for r in rows if r.obj_type == 'arc')
    try:
        n_mark = len(session.drc())
    except Exception as exc:  # noqa: BLE001
        n_mark = f'ERROR {exc!r}'
    info = dict(
        arcs=n_arcs, routes=len(rows), markers=n_mark,
        cur=ev(ws, 'axlCurrentDesign()'),
        draw=ev(ws, 'axlGetDrawingName()'),
        lic=ev(ws, 'sprintf(nil "%L" axlLicIsProductEnabled(\'all))'),
        err=ev(ws, 'errset.errset'),
    )
    print(f'TRIAL {tag} {phase}: '
          + ' '.join(f'{k}={v!r}' for k, v in info.items()), flush=True)
    return info


def main() -> None:
    _workdir, board_s, port, tag = sys.argv[1:5]
    board = Path(board_s)
    pd.wait_ready(board)
    lck = pd._lck_holder_alive(Path(board_s + '.lck'))
    print(f'TRIAL {tag}: lck_before={lck}', flush=True)
    allegro = Allegro.open(mode='cli', board=board, workspace_id=port,
                           timeout=300.0)
    ok = False
    try:
        session = allegro.session
        info = observe(session, tag, 'STARTUP')
        if info['arcs'] >= 1:
            ok = True
        else:
            print(f'TRIAL {tag}: EMPTY -> axlKillDesign + axlOpenDesign '
                  f'recovery attempt', flush=True)
            ws = session.workspace
            kill = ev(ws, 'axlKillDesign()')
            print(f'TRIAL {tag}: axlKillDesign -> {kill!r}', flush=True)
            time.sleep(2.0)
            payload = ('errset.string=catch(axlOpenDesign(?design "%s" '
                       '?mode "wf") errset.errset)' % board.as_posix())
            res = ev(ws, payload)
            print(f'TRIAL {tag}: axlOpenDesign retry -> {res!r}', flush=True)
            session.refresh()
            info2 = observe(session, tag, 'AFTER_KILL_REOPEN')
            ok = info2['arcs'] >= 1
            if ok:
                print(f'TRIAL {tag}: RECOVERY_OK', flush=True)
    finally:
        allegro.close()
    print(f'TRIAL {tag}: RESULT={"OK" if ok else "EMPTY"}', flush=True)
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()
