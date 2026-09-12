# Probe D diagnostic: controlled timing / exit-method experiment for the
# reproducible "S2 empty design" failure (run1-run4: Allegro launched seconds
# after the previous owned Allegro was terminate-closed silently declines
# axlOpenDesign -- gentle nil, errset.errset empty, current design stays the
# always-present unnamed/empty design; the SAME file opens fine minutes later
# in a fresh process).
#
# Hypothesis under test (labeled hypothesis per user caveat, NOT asserted):
# terminate-close is an abnormal termination -- the SKILL 'exit trigger does
# not run, so licenses/locks are not voluntarily returned; an Allegro
# launched inside the reclaim window enters a degraded state where the
# startup axlOpenDesign walks a dialog that noconfirm auto-answers No
# (axlUIYesNo documented semantics) -> gentle nil.
#
# Design:
#   PHASE 1 (replicate + map window): S1 opens the disposable board copy,
#     saves F1, terminate-close (probe_d conditions).  Fresh-process attempts
#     (probe_d_attempt.py subprocess) at increasing F1 age; A1 gets a
#     read-only `lmutil lmstat -a` snapshot DURING its window.  First success
#     stops the sweep and brackets the age boundary.
#   PHASE 2 (isolate exit method): open F1 (older now, known-openable), save
#     FRESH F1B, GRACEFUL exit via SKILL exit() (documented headless graceful
#     shutdown), then one attempt on F1B at age ~10s -- same young age as A1,
#     only the exit method differs.  A1 EMPTY + G1 OK => exit method is the
#     differentiator.  Bonus: sha256(F1) vs sha256(F1B) is an extra
#     re-save byte-stability datapoint for P0.
#
# Isolation: own temp workdir (drc-probe-timing-*), probe-owned Allegro
# processes only, unique ports, logs to logs/probe_d.timing*.log via caller
# redirection.  lmstat is a READ-ONLY license-server query.
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import subprocess
import sys
import threading
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

ATTEMPT = HERE / 'probe_d_attempt.py'
LMUTIL = r'D:\Cadence\LicenseManager\lmutil.exe'
AGES = [10.0, 60.0, 120.0, 180.0, 300.0]   # F1 age (s) at attempt launch
REF = {'t': 0.0, 'what': 'save'}            # age reference for run_attempt
WORK: Path | None = None                    # set in main(); attempt arg 1


def ev(ws, payload):
    try:
        return ws['evalstring'](payload)
    except Exception as exc:  # noqa: BLE001
        return f'ERROR {exc!r}'


def lmstat(tag: str) -> None:
    """Read-only FlexLM query; print filtered lines (checkouts on this host)."""
    try:
        out = subprocess.run([LMUTIL, 'lmstat', '-a', '-c', '5280@localhost'],
                             capture_output=True, timeout=90)
        text = ((out.stdout or b'') + (out.stderr or b'')).decode(
            'utf-8', errors='replace')
        rc = out.returncode
    except Exception as exc:  # noqa: BLE001
        print(f'LMSTAT {tag}: ERROR {exc!r}', flush=True)
        return
    keep = []
    for line in text.splitlines():
        low = line.lower()
        if ('users of' in low or 'baijunyan' in low or 'allegro' in low
                or 'total of' in low or 'license server' in low):
            keep.append(line.rstrip())
    print(f'LMSTAT {tag}: rc={rc} kept={len(keep)} lines', flush=True)
    for line in keep[:150]:
        print(f'LMSTAT {tag} | {line}', flush=True)


def run_attempt(tag: str, port: str, board: Path,
                lmstat_at: float | None = None) -> bool:
    """Fresh-process attempt via probe_d_attempt.py; tee its output."""
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    t0 = time.monotonic()
    print(f'TRIAL {tag}: launching (age_at_launch='
          f'{t0 - REF["t"]:.1f}s after {REF["what"]})', flush=True)
    proc = subprocess.Popen(
        [sys.executable, str(ATTEMPT), str(WORK), str(board), port, tag],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(HERE),
        env=env)
    try:
        if lmstat_at is not None:
            time.sleep(lmstat_at)
            lmstat(f'DURING_{tag}')
        out_b, _ = proc.communicate(timeout=480)
    except subprocess.TimeoutExpired:
        proc.kill()
        out_b, _ = proc.communicate()
        print(f'TRIAL {tag}: TIMEOUT killed', flush=True)
    out = (out_b or b'').decode('utf-8', errors='replace')
    for line in out.splitlines():
        print(line, flush=True)
    print(f'TRIAL {tag}: exit={proc.returncode} '
          f'wall={time.monotonic() - t0:.1f}s', flush=True)
    return proc.returncode == 0


def graceful_exit(allegro, tag: str, timeout: float = 90.0) -> bool:
    """SKILL exit() via a daemon thread (RPC dies with the server); wait for
    natural process exit; fall back to the standard terminate close()."""
    rt = allegro._runtime  # noqa: SLF001 - probe diagnostic
    pid = rt.process.pid

    def _send() -> None:
        try:
            allegro.session.workspace['evalstring']('exit()')
        except BaseException:  # noqa: BLE001 - server dies mid-RPC
            pass

    threading.Thread(target=_send, daemon=True).start()
    t0 = time.monotonic()
    exited = False
    while time.monotonic() - t0 < timeout:
        if rt.poll() is not None:
            exited = True
            break
        time.sleep(0.5)
    print(f'GRACEFUL {tag}: pid={pid} natural_exit={exited} '
          f'after={time.monotonic() - t0:.1f}s rc={rt.poll()!r}', flush=True)
    allegro.close()   # idempotent: tempdir/endpoint cleanup; dead proc = no-op
    return exited


def main() -> None:
    global WORK
    work = Path(mkdtemp(prefix='drc-probe-timing-'))
    WORK = work
    board = Path(copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work))
    f1 = work / 'probe_d_F1.brd'
    f1b = work / 'probe_d_F1B.brd'
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    ports = [pd._free_port() for _ in range(8)]
    print(f'WORKDIR {work}', flush=True)
    print(f'PORTS {ports}', flush=True)

    # ---------------- PHASE 0/1: S1 real save, terminate close -------------
    pd.wait_ready(board)
    allegro = Allegro.open(mode='cli', board=board, workspace_id=ports[0],
                           timeout=300.0)
    try:
        session = allegro.session
        rows = session.routes(layer=pc.LAYER)
        n_arcs = sum(1 for r in rows if r.obj_type == 'arc')
        print(f'S1: arcs={n_arcs} routes={len(rows)} markers='
              f'{len(session.drc())}', flush=True)
        lic = ev(session.workspace,
                 'sprintf(nil "%L" axlLicIsProductEnabled(\'all))')
        print(f'LIC S1: {lic!r}', flush=True)
        save1 = session.workspace['axlSaveDesign'](design=f1.as_posix(),
                                                   no_confirm=True)
        t_save = time.monotonic()
        REF.update(t=t_save, what='F1 save')
        print(f'SAVE F1: result={save1!r} exists={f1.exists()} '
              f'size={f1.stat().st_size if f1.exists() else None}', flush=True)
        if f1.exists():
            print(f'F1_SHA256 {pd.sha256(f1)}', flush=True)
    finally:
        allegro.close()          # terminate close == probe_d S1 conditions
    print(f'S1 closed (terminate) +{time.monotonic() - t_save:.1f}s '
          f'after save', flush=True)
    lmstat('POST_S1_TERMINATE')

    # ---------------- PHASE 1: fresh-process attempts, age sweep -----------
    first_ok_age = None
    for i, age in enumerate(AGES):
        wait = (t_save + age) - time.monotonic()
        if wait > 0:
            print(f'PHASE1: sleeping {wait:.1f}s until F1 age {age:.0f}s',
                  flush=True)
            time.sleep(wait)
        tag = f'A{i + 1}_age{age:.0f}s'
        ok = run_attempt(tag, ports[1 + i], f1,
                         lmstat_at=50.0 if i == 0 else None)
        if ok:
            first_ok_age = age
            print(f'PHASE1: first success at scheduled F1 age {age:.0f}s '
                  f'(actual {time.monotonic() - t_save:.1f}s)', flush=True)
            break
    else:
        print(f'PHASE1: no success up to scheduled age {AGES[-1]:.0f}s '
              f'(actual {time.monotonic() - t_save:.1f}s)', flush=True)

    # ---------------- PHASE 2: graceful exit() at the SAME young age -------
    pd.wait_ready(f1)
    allegro2 = Allegro.open(mode='cli', board=f1, workspace_id=ports[6],
                            timeout=300.0)
    t_saveb = None
    try:
        session2 = allegro2.session
        rows2 = session2.routes(layer=pc.LAYER)
        n2 = sum(1 for r in rows2 if r.obj_type == 'arc')
        print(f'P2OPEN F1: arcs={n2} routes={len(rows2)} markers='
              f'{len(session2.drc())}', flush=True)
        lic2 = ev(session2.workspace,
                  'sprintf(nil "%L" axlLicIsProductEnabled(\'all))')
        print(f'LIC P2: {lic2!r}', flush=True)
        saveb = session2.workspace['axlSaveDesign'](design=f1b.as_posix(),
                                                    no_confirm=True)
        t_saveb = time.monotonic()
        print(f'SAVE F1B: result={saveb!r} exists={f1b.exists()} '
              f'size={f1b.stat().st_size if f1b.exists() else None}',
              flush=True)
        if f1b.exists():
            hb = pd.sha256(f1b)
            print(f'F1B_SHA256 {hb}', flush=True)
            if f1.exists():
                print(f'F1_F1B_IDENTICAL {hb == pd.sha256(f1)}', flush=True)
        graceful_exit(allegro2, 'P2')
    finally:
        try:
            allegro2.close()
        except Exception:  # noqa: BLE001 - already closed on the happy path
            pass
    lmstat('POST_GRACEFUL_EXIT')

    g_ok = None
    if t_saveb is not None and f1b.exists():
        REF.update(t=t_saveb, what='F1B save')
        wait = (t_saveb + 10.0) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        g_ok = run_attempt('G1_graceful_age10s', ports[7], f1b, lmstat_at=50.0)

    # ---------------- SUMMARY ----------------------------------------------
    print('SUMMARY', flush=True)
    print(f'SUMMARY PHASE1_first_ok_age={first_ok_age}', flush=True)
    print(f'SUMMARY PHASE2_graceful_attempt_ok={g_ok}', flush=True)
    print('SUMMARY interpretation: compare A1 (terminate exit, F1 age '
          '~10s) vs G1 (graceful exit, F1B age ~10s); equal ages isolate '
          'the exit method', flush=True)
    print(f'WORKDIR_KEEP {work}', flush=True)


if __name__ == '__main__':
    main()
