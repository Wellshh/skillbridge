# Probe D diag: why did session 2 open an EMPTY design from probe_d_F1.brd?
# Hypothesis: axlSaveDesign leaves a stale advisory .lck (dead PID); headless
# axlOpenDesign refuses the locked file, the startup-script error() goes only
# to the Allegro console, and pyStartServer still starts -> bridge connects
# to an empty current design (matches run1: arcs=0, markers=0, F2=96KB).
# A/B: open F1 as-is (lck present) -> counts; delete stale lck (probe-owned
# file, PID verified dead) -> reopen -> counts.  Own processes, unique ports.
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import subprocess
import sys
from pathlib import Path
from socket import socket
from tempfile import mkdtemp

from allegrobridge import Allegro

WORK = Path(sys.argv[1])
F1 = WORK / 'probe_d_F1.brd'
LCK = Path(str(F1) + '.lck')
# expected committed P1 upper arc from run1 S1_PRE (for content verify)
P1_KEY = ('NFC_SWP', 300.0, 410.0, 302.0001, 410.0)


def free_port() -> str:
    with socket() as listener:
        listener.bind(('localhost', 0))
        return str(listener.getsockname()[1])


def pid_alive(pid: int) -> bool:
    out = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                         capture_output=True, text=True).stdout
    return str(pid) in out


def inspect(label: str) -> None:
    with Allegro.open(mode='cli', board=F1, workspace_id=free_port(),
                      timeout=300.0) as allegro:
        session = allegro.session
        try:
            name = session.workspace['evalstring'](
                'axlDBGetDesign()->name')
        except Exception as exc:
            name = f'ERROR {exc!r}'
        rows = session.routes(layer='ETCH/TOP')
        arcs = [r for r in rows if r.obj_type == 'arc']
        n_mark = len(session.drc())
        print(f'DIAG {label}: design_name={name!r} arcs={len(arcs)} '
              f'routes={len(rows)} markers={n_mark}', flush=True)
        for r in arcs:
            key = (r.net, float(r.start.x), float(r.start.y),
                   float(r.end.x), float(r.end.y))
            if key == P1_KEY:
                print(f'DIAG {label}: P1_UPPER cx={float(r.center.x)!r} '
                      f'cy={float(r.center.y)!r} r={float(r.radius)!r} '
                      f'length={float(r.length)!r} cw={r.is_clockwise!r}',
                      flush=True)


def main() -> None:
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = \
        mkdtemp(prefix='probe-d-diag-')
    print(f'DIAG board={F1} exists={F1.exists()} size={F1.stat().st_size}',
          flush=True)
    print(f'DIAG lck_exists={LCK.exists()}', flush=True)
    if LCK.exists():
        pid = None
        for line in LCK.read_text().splitlines():
            if line.startswith('PID='):
                pid = int(line.split('=', 1)[1])
        alive = pid_alive(pid) if pid is not None else None
        print(f'DIAG lck pid={pid} alive={alive}', flush=True)
        if alive:
            print('DIAG ABORT: lock holder alive (not ours to break)',
                  flush=True)
            return
    inspect('PHASE_A_LCK_PRESENT')
    if LCK.exists():
        LCK.unlink()
        print('DIAG lck_removed=True', flush=True)
    inspect('PHASE_B_LCK_REMOVED')
    print('DIAG DONE', flush=True)


if __name__ == '__main__':
    main()
