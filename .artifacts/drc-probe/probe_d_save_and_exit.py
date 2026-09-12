# Probe D diagnostic: minimal saver that EXITS right after saving F1.
# Used to test whether a young F1 (age ~15-30s) opens fine when the saving
# python process is already dead and no ALLEGROBRIDGE_LOG_DIRECTORY env is
# inherited -- separating "file age" / "orchestrator aliveness" / "env var"
# as the differentiator for the silent axlOpenDesign refusal.
#
# usage: python probe_d_save_and_exit.py
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import sys
import time
from pathlib import Path
from shutil import copy2
from tempfile import mkdtemp

HERE = Path(__file__).resolve().parent
for _p in (str(HERE), r'D:\AutoPlacer\skillbridge'):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import probe_c as pc
import probe_d as pd
from allegrobridge import Allegro
from allegrobridge.util import ASSETS_DIR


def main() -> None:
    # optional argv[1] = seconds to stay alive AFTER close (liveness control)
    stay = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    work = Path(mkdtemp(prefix='drc-probe-h2-'))
    board = Path(copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work))
    f1 = work / 'probe_d_F1.brd'
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    port = pd._free_port()
    print(f'SAVER: workdir={work}', flush=True)
    pd.wait_ready(board)
    allegro = Allegro.open(mode='cli', board=board, workspace_id=port,
                           timeout=300.0)
    try:
        session = allegro.session
        rows = session.routes(layer=pc.LAYER)
        n_arcs = sum(1 for r in rows if r.obj_type == 'arc')
        sv = session.workspace['axlSaveDesign'](design=f1.as_posix(),
                                                no_confirm=True)
        print(f'SAVER: arcs={n_arcs} save={sv!r} exists={f1.exists()} '
              f'size={f1.stat().st_size if f1.exists() else None}', flush=True)
        print(f'SAVE_TS {time.time():.3f}', flush=True)
    finally:
        allegro.close()   # terminate close == probe_d S1 conditions
    if stay > 0:
        print(f'SAVER_SLEEPING pid={os.getpid()} stay={stay} '
              f'workdir={work}', flush=True)
        time.sleep(stay)
    print(f'SAVER_EXIT workdir={work}', flush=True)


if __name__ == '__main__':
    main()
