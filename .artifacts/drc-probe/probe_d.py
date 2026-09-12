# Probe D: DRC state-consistency + save/reopen round-trip + equivalent
# representation.  Disposable board copy (probe_d-specific), own Allegro
# processes, unique ports per launch.  No production code modified.  Reuses
# probe_c harness helpers (import probe_c as pc).
#
# Question map (user's parallel-probe table):
#   P0 create/save/reopen state comparison -- does committed subgrid geometry
#      (non-grid ARC centers, e.g. delta ~2e-6 = 0.02 DBU designs) and the
#      DRC verdict survive save->reopen->save bit-exactly, or does the save
#      normalize?  Caveat kept honest: even if file round-trip agrees with
#      API read-back, "stored in memory + derived at query" vs "derived at
#      save and written back" remain indistinguishable from the outside.
#   P1 DRC update/suppression behavior -- same final geometry reached via
#      different create/check orders: first check vs repeated check vs full
#      axlDRCUpdate vs check after save/reopen; A-then-B vs B-then-A;
#      delete-recreate (raw-SKILL canary: client API exposes no dbid/delete).
#   P2 equivalent geometry -- the same finite arc with start/end swapped and
#      direction flipped (cw'=not cw): committed center/radius/length bits and
#      spacing verdict consistent with the forward representation?
#
# Stages (cells at y0, all <=698 per diag_y700 extent boundary; empty region
# x in [298,304], y in [380,690] proven by probe_c):
#   STAGE 0  y0=390 rule learning (natural arc + tight line) -> R, marker name
#   STAGE 1  y0=410 P1 violation pair (delta in [1.5e-6,2.5e-6]):
#            upper-alone precheck, first/repeat x3 checks, full drc.update(),
#            post-update check; y0=430 P2 clean pair (margin window): repeat
#            checks; P1 recheck after P2 exists (far-object addition).
#   STAGE 2  y0=450 ORD_A upper-first vs y0=470 ORD_B lower-first (same delta
#            window) -> order-swap consistency.
#   STAGE 3  y0=490 FWD forward upper vs y0=510 REV reversed upper
#            (S'=E, E'=S, cw'=True, center offset identical +20mm) ->
#            equivalent-representation consistency.
#   STAGE 4  delete P1 upper via raw SKILL select-box (evalstring escape
#            hatch; canary: only delete when selset count == 1), recreate with
#            identical requested bits, compare committed bits + verdict.
#            SKIP (warn, don't crash) if headless selection is unavailable.
#   STAGE 5  pre-save snapshot (bits/verdicts/marker count) ->
#            axlSaveDesign(F1, ?noConfirm t) -> session.refresh() -> post-save
#            snapshot (same session) -> close -> session 2 opens F1 (fresh
#            port): persisted marker count, snapshot compare, verdict recheck,
#            drc.update() persisted-vs-regenerated counts -> save F2
#            unmodified -> sha256(F1) vs sha256(F2) -> session 3 opens F2:
#            snapshot compare.
#
# Isolation: temp workdir per run, probe_d_F1/F2 names, 3 unique ports, logs
# to logs/probe_d.*.  axlSaveDesign clears all axl dbid handles -> every stage
# boundary that saves/deletes calls session.refresh() and re-queries fresh
# rows (client rows are generation-guarded and raise when stale; we only ever
# carry plain float dicts across those boundaries).
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import hashlib
import math
import pickle
import subprocess
import sys
import time
from collections import Counter
from decimal import Decimal
from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

import arc_oracle as orc
import probe_c as pc
from scan_window import CX_NAT, CY_OFF, EX, SX
from allegrobridge import Allegro
from allegrobridge.client.api.geometry import ArcTo
from allegrobridge.util import ASSETS_DIR

DELTA_WIN = ('delta', Decimal('1.5e-6'), Decimal('2.5e-6'))
MARGIN_WIN = ('margin', Decimal('5e-7'), Decimal('2.5e-5'))
VTAGS = ['P1_UPPER', 'P2_UPPER', 'ORD_A_UPPER', 'ORD_B_UPPER',
         'FWD_UPPER', 'REV_UPPER']
TRACK: dict = {}      # tag -> dict(net,S,E,req_C,cw,partner,com{cx,cy,r,length,cw})
RESULTS: dict = {}    # final RESULT lines


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def marker_count(drc, stage: str):
    try:
        n = len(drc())
    except Exception as exc:
        n = f'ERROR {exc!r}'
    print(f'COUNT {stage}: total_markers={n}', flush=True)
    return n


# --------------------------------------------------------------------------
# session-open guard (run1 postmortem): the startup script's axlOpenDesign
# failure only prints to the discarded Allegro console -- pyStartServer still
# starts, so Allegro.open() "succeeds" with an EMPTY current design (run1
# sessions 2/3: arcs=0, markers=0, F2=96KB).  Diag proved the same F1 opens
# fine minutes later (stale dead-PID .lck does NOT block axlOpenDesign), so
# the run1 failure was a transient at open time (session-1 process teardown /
# file release timing -- hypothesis, not asserted).  Guard: before launching,
# wait until no .lck holder PID is alive AND the .brd opens exclusively;
# after launching, verify content; on empty design close, wait, retry ONCE on
# a fresh port.  Retrying an *open* is a read retry, not a failed-write
# replay.
# --------------------------------------------------------------------------

def _free_port() -> str:
    with socket() as listener:
        listener.bind(('localhost', 0))
        return str(listener.getsockname()[1])


def _pid_alive(pid: int) -> bool:
    out = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                         capture_output=True, text=True).stdout
    return str(pid) in out


def _lck_holder_alive(lck: Path):
    """Return (pid, alive) if a .lck exists with a parseable PID, else None."""
    if not lck.exists():
        return None
    pid = None
    try:
        for line in lck.read_text().splitlines():
            if line.startswith('PID='):
                pid = int(line.split('=', 1)[1])
    except Exception:
        return None
    if pid is None:
        return None
    return pid, _pid_alive(pid)


def wait_ready(board: Path, timeout: float = 90.0) -> None:
    """Poll until board file is exclusively openable and no live .lck holder."""
    board = Path(board)   # shutil.copy2 returns str when dst is a directory
    lck = Path(str(board) + '.lck')
    deadline = time.monotonic() + timeout
    while True:
        holder = _lck_holder_alive(lck)
        busy = holder is not None and holder[1]
        try:
            with open(board, 'r+b'):
                exclusive = True
        except OSError:
            exclusive = False
        if exclusive and not busy:
            print(f'OPEN_READY {board.name}: lck_holder={holder} '
                  f'exclusive={exclusive}', flush=True)
            return
        if time.monotonic() >= deadline:
            print(f'OPEN_READY {board.name}: TIMEOUT lck_holder={holder} '
                  f'exclusive={exclusive} (proceeding anyway)', flush=True)
            return
        time.sleep(2.0)


def _design_name(session) -> str:
    try:
        return repr(session.workspace['evalstring'](
            '__abDName=axlDBGetDesign()->name'))
    except Exception as exc:
        return f'ERROR {exc!r}'


def open_verified(board: Path, first_port: str, stage: str,
                  min_arcs: int = 1):
    """Allegro.open + content verify; in-session reopen recovery; one retry.

    Run1/run2 postmortem: the startup script's axlOpenDesign failure only
    prints to the discarded Allegro console, so Allegro.open() 'succeeds'
    with an EMPTY design.  Diag proves the same F1 opens fine minutes later
    in a fresh process (even with the stale dead-PID .lck present), so the
    failure is tied to launching shortly after the previous owned Allegro
    was terminated -- mechanism (license reclaim / lock-table timing) is a
    hypothesis, not asserted.  Recovery: while the session is still alive,
    re-issue axlOpenDesign via evalstring and CAPTURE the return value --
    this is the only channel that reveals Allegro's actual error text.
    """
    board = Path(board)
    for attempt, port in enumerate((first_port, _free_port()), start=1):
        wait_ready(board)
        allegro = Allegro.open(mode='cli', board=board, workspace_id=port,
                               timeout=300.0)
        try:
            session = allegro.session
            rows = session.routes(layer=pc.LAYER)
            n_arcs = sum(1 for r in rows if r.obj_type == 'arc')
            size = board.stat().st_size if board.exists() else -1
            print(f'OPEN_VERIFY {stage} attempt={attempt} port={port}: '
                  f'arcs={n_arcs} routes={len(rows)} board_size={size}',
                  flush=True)
            if n_arcs >= min_arcs:
                return allegro
            print(f'OPEN_VERIFY {stage}: EMPTY despite size={size}; '
                  f'name_before={_design_name(session)}', flush=True)
            try:
                # keep payload < ~200 chars (evalstring col-255 open question)
                payload = ('errset.string=catch(axlOpenDesign(?design "%s" '
                           '?mode "wf") errset.errset)' % board.as_posix())
                print(f'REOPEN {stage} attempt={attempt}: '
                      f'payload_len={len(payload)}', flush=True)
                res = session.workspace['evalstring'](payload)
                print(f'REOPEN {stage} attempt={attempt}: result={res!r} '
                      f'name_after={_design_name(session)}', flush=True)
            except Exception as exc:
                print(f'REOPEN {stage} attempt={attempt}: FAILED {exc!r}',
                      flush=True)
            for extra in ('errset.errset',
                          'get_pname(errset.errset)',
                          'axlDesignIsFixed()',
                          'axlDBGetDesign()'):
                try:
                    val = session.workspace['evalstring'](extra)
                    print(f'REOPEN_INFO {stage} attempt={attempt}: '
                          f'{extra} -> {val!r}', flush=True)
                except Exception as exc:
                    print(f'REOPEN_INFO {stage} attempt={attempt}: '
                          f'{extra} -> ERROR {exc!r}', flush=True)
            rows = session.routes(layer=pc.LAYER)
            n_arcs = sum(1 for r in rows if r.obj_type == 'arc')
            print(f'REOPEN_VERIFY {stage} attempt={attempt}: arcs={n_arcs} '
                  f'routes={len(rows)}', flush=True)
            if n_arcs >= min_arcs:
                RESULTS[f'REOPEN_RECOVERY_{stage}'] = (
                    f'attempt={attempt} (startup open failed silently)')
                session.refresh()   # new design -> new dbid generation
                return allegro
            # recoverable only by tearing down OUR process and retrying.
            allegro.close()
        except BaseException:
            allegro.close()
            raise
        if attempt == 1:
            print(f'OPEN_VERIFY {stage}: still empty after in-session '
                  f'reopen; closed, waiting 30s before single retry',
                  flush=True)
            time.sleep(30.0)
    raise RuntimeError(f'{stage}: design empty after open retry: {board}')


# --------------------------------------------------------------------------
# snapshots (plain float dicts only -- safe across refresh/save boundaries)
# --------------------------------------------------------------------------

def snap(session, stage: str) -> dict:
    rows = [r for r in session.routes(layer=pc.LAYER) if r.obj_type == 'arc']
    out: dict = {}
    for r in rows:
        key = (r.net, float(r.start.x), float(r.start.y),
               float(r.end.x), float(r.end.y))
        out.setdefault(key, []).append(dict(
            cx=float(r.center.x), cy=float(r.center.y), r=float(r.radius),
            length=float(r.length), cw=r.is_clockwise, w=float(r.width)))
    dup = sum(1 for v in out.values() if len(v) > 1)
    print(f'SNAP {stage}: total_arcs={len(rows)} distinct_keys={len(out)} '
          f'duplicate_keys={dup}', flush=True)
    return out


def snap_compare(tag: str, a: dict, b: dict) -> int:
    bad = 0
    for t, info in sorted(TRACK.items()):
        key = (info['net'], info['S'][0], info['S'][1],
               info['E'][0], info['E'][1])
        la, lb = a.get(key), b.get(key)
        if not la or not lb:
            print(f'SNAPDIFF {tag} {t}: MISSING in '
                  f'{"a" if not la else "b"}', flush=True)
            bad += 1
            continue
        ra, rb = la[0], lb[0]
        fields = {k: (orc.bits(ra[k]) == orc.bits(rb[k]))
                  for k in ('cx', 'cy', 'r', 'length')}
        fields['cw'] = ra['cw'] == rb['cw']
        if not all(fields.values()):
            bad += 1
            diffs = {k: (ra[k], rb[k]) for k, ok in fields.items() if not ok}
            print(f'SNAPDIFF {tag} {t}: {diffs}', flush=True)
    print(f'SNAPDIFF {tag}: mismatches={bad}/{len(TRACK)}', flush=True)
    return bad


def find_row(session, info: dict):
    for r in session.routes(net=info['net'], layer=pc.LAYER):
        if (r.obj_type == 'arc'
                and (float(r.start.x), float(r.start.y)) == info['S']
                and (float(r.end.x), float(r.end.y)) == info['E']):
            return r
    return None


def check_cell(session, drc, tag_key: str, stage: str, marker_name: str):
    """Fresh-row targeted drc.check with partner attribution.  Returns
    (verdict, actual, expected) -- comparable tuple across stages."""
    info = TRACK[tag_key]
    row = find_row(session, info)
    if row is None:
        print(f'VERDICT {stage} {tag_key}: ROW_NOT_FOUND', flush=True)
        return ('ROW_NOT_FOUND', None, None)
    hits = pc.run_drc(drc, row, f'{stage}:{tag_key}', marker_name,
                      info['partner'])
    verdict = 'FLAGGED' if hits else ('clean' if hits is not None else 'ERROR')
    actual = hits[0][2] if hits else None
    expected = hits[0][1] if hits else None
    print(f'VERDICT {stage} {tag_key}: {verdict} actual={actual!r} '
          f'expected={expected!r}', flush=True)
    return (verdict, actual, expected)


def verdict_snapshot(session, drc, stage: str, marker_name: str,
                     tags=VTAGS) -> dict:
    return {t: check_cell(session, drc, t, stage, marker_name) for t in tags}


def verdict_compare(stage: str, base: dict, cur: dict, tags) -> list:
    bad = []
    for t in tags:
        if t in base and t in cur and base[t] != cur[t]:
            bad.append(t)
            print(f'VERDIFF {stage} {t}: {base[t]} -> {cur[t]}', flush=True)
    print(f'VERDIFF {stage}: mismatches={len(bad)}/{len(list(tags))}',
          flush=True)
    return bad


# --------------------------------------------------------------------------
# cell construction (mirrors probe_c run_cc_rung geometry, explicit orders)
# --------------------------------------------------------------------------

def plan_cell(y0, R_dec: Decimal, delta_dec: Decimal, kind: str,
              lo: Decimal, hi: Decimal, cy1_override=None):
    y1_dec = Decimal(int(y0)) - delta_dec
    y1_f = float(y1_dec)
    cy2_f = float(y1_dec - pc.CY_OFF_DEC)
    r2_f = math.hypot(CX_NAT - SX, cy2_f - y1_f)
    if cy1_override is not None:
        cy1 = cy1_override
        r1_f = math.hypot(CX_NAT - SX, cy1 - float(y0))
        clear = pc.pair_clear_exact(cy1, r1_f, cy2_f, r2_f)
        val = R_dec - clear if kind == 'delta' else clear - R_dec
    else:
        found = pc.find_eps_pair(float(y0), y1_f, cy2_f, r2_f, R_dec,
                                 kind, lo, hi)
        if found is None:
            return None
        cy1, val = found
    return dict(y0=float(y0), y1_f=y1_f, cy1=cy1, cy2_f=cy2_f,
                planned_val=val, kind=kind, lo=lo, hi=hi)


def _track(tag, net, S, E, C, cw, row, partner):
    TRACK[tag] = dict(
        net=net, S=(S[0], S[1]), E=(E[0], E[1]), req_C=C, cw=cw,
        partner=partner,
        com=dict(cx=float(row.center.x), cy=float(row.center.y),
                 r=float(row.radius), length=float(row.length),
                 cw=row.is_clockwise))


def create_pair(session, drc, padstack, tag, plan, marker_name,
                lower_first=False, reverse_upper=False):
    """Create upper (NET_A) + lower partner (NET_B) arcs for one cell.
    reverse_upper: S'=E, E'=S, cw'=True (same bottom-bulging finite arc).
    lower_first: create+check partner BEFORE the upper arc exists (order-swap
    variable).  Records planned/committed and the pre-partner check."""
    y0, y1_f = plan['y0'], plan['y1_f']
    cy1, cy2_f = plan['cy1'], plan['cy2_f']
    if reverse_upper:
        S_u, E_u, cw_u = (EX, y0), (SX, y0), True
    else:
        S_u, E_u, cw_u = (SX, y0), (EX, y0), False
    C_u = (CX_NAT, cy1)
    C_l = (CX_NAT, cy2_f)
    S_l, E_l = (SX, y1_f), (EX, y1_f)
    print(f'=== CELL {tag} y0={y0!r} y1={y1_f!r} lower_first={lower_first} '
          f'reverse_upper={reverse_upper} planned {plan["kind"]}='
          f'{plan["planned_val"]}', flush=True)
    print(f'   PLANNED cy1={cy1!r} bits={orc.bits(cy1)} '
          f'eps={Decimal(cy1) - Decimal(y0) - pc.CY_OFF_DEC}', flush=True)

    def make_upper():
        row = pc.create_arc_net(session, padstack, pc.NET_A, S_u, E_u, C_u,
                                cw_u, tag + '_UPPER')
        if row is not None:
            _track(tag + '_UPPER', pc.NET_A, S_u, E_u, C_u, cw_u, row,
                   ('arc', pc.NET_B, S_l))
        return row

    def make_lower():
        row = pc.create_arc_net(session, padstack, pc.NET_B, S_l, E_l, C_l,
                                True, tag + '_LOWER')
        if row is not None:
            _track(tag + '_LOWER', pc.NET_B, S_l, E_l, C_l, True, row,
                   ('arc', pc.NET_A, S_u))
        return row

    if lower_first:
        lower = make_lower()
        if lower is not None:
            hits = pc.run_drc(drc, lower, f'{tag}_LOWER_ALONE', marker_name,
                              ('arc', pc.NET_A, S_u))
            print(f'PRECHECK {tag}: lower-alone (upper absent) -> '
                  f'{_vstr(hits)}', flush=True)
        upper = make_upper()
    else:
        upper = make_upper()
        if upper is not None:
            hits = pc.run_drc(drc, upper, f'{tag}_UPPER_ALONE', marker_name,
                              ('arc', pc.NET_B, S_l))
            print(f'PRECHECK {tag}: upper-alone (partner absent) -> '
                  f'{_vstr(hits)}', flush=True)
        lower = make_lower()
    if upper is None or lower is None:
        print(f'CELL {tag}: CREATE_FAILED', flush=True)
        return None, None
    cl = pc.pair_clear_exact(TRACK[tag + '_UPPER']['com']['cy'],
                             TRACK[tag + '_UPPER']['com']['r'],
                             TRACK[tag + '_LOWER']['com']['cy'],
                             TRACK[tag + '_LOWER']['com']['r'])
    kind, lo, hi = plan['kind'], plan['lo'], plan['hi']
    # committed delta/margin needs the learned R -- plan carries it
    R_dec = plan.get('R_dec')
    if R_dec is not None:
        val = R_dec - cl if kind == 'delta' else cl - R_dec
        print(f'COMMITTED_CELL {tag}: clear={cl} {kind}={val} '
              f'in_window={lo <= val <= hi}', flush=True)
    else:
        print(f'COMMITTED_CELL {tag}: clear={cl}', flush=True)
    return upper, lower


def _vstr(hits) -> str:
    if hits is None:
        return 'ERROR(check failed)'
    return f'FLAGGED hits={len(hits)}' if hits else 'clean'


def committed_clear(tag: str) -> Decimal:
    u = TRACK[tag + '_UPPER']['com']
    l = TRACK[tag + '_LOWER']['com']
    return pc.pair_clear_exact(u['cy'], u['r'], l['cy'], l['r'])


# --------------------------------------------------------------------------
# STAGE 4: delete-recreate canary via raw SKILL (no client delete API;
# Route records expose no dbid -> evalstring select-box escape hatch)
# --------------------------------------------------------------------------

def stage4_delete_recreate(session, drc, padstack, ws, marker_name):
    tag = 'P1_UPPER'
    info = TRACK[tag]
    orig_com = info['com']
    v_before = check_cell(session, drc, tag, 'DEL_PRECHECK', marker_name)
    marker_count(drc, 'DEL_BEFORE')
    S, E = info['S'], info['E']
    # box: full x-span +-0.15, y from chord-1.0 (arc bottom ~chord-0.883+eps,
    # partner top is ~0.09 below chord-1.0 -> excluded) to chord+0.15
    y0 = S[1]
    bx0, by0 = min(S[0], E[0]) - 0.15, y0 - 1.0
    bx1, by1 = max(S[0], E[0]) + 0.15, y0 + 0.15
    box = f'list({bx0!r}:{by0!r} {bx1!r}:{by1!r})'
    deleted = False
    for filt in ('arcs', 'clines'):
        try:
            ws['evalstring'](
                f'axlSetFindFilter(?enabled list("noall" "{filt}") '
                f'?onButtons list("noall" "{filt}"))')
            sel_ok = ws['evalstring'](f'axlSingleSelectBox({box})')
            n_raw = ws['evalstring']('length(axlGetSelSet())')
            try:
                n = int(n_raw)
            except (TypeError, ValueError):
                n = -1
            print(f'DELETE_SELECT filter={filt} '
                  f'box=({bx0},{by0})-({bx1},{by1}): sel_ok={sel_ok!r} '
                  f'selset_count={n_raw!r}', flush=True)
            if n == 1:
                res = ws['evalstring'](
                    'if(axlDeleteObject(axlGetSelSet()) 1 0)')
                print(f'DELETE_RESULT filter={filt}: {res!r}', flush=True)
                deleted = (res == 1)
                break
            # n != 1 (incl. >1 ambiguous): NEVER delete unowned/extra
            # objects; fall through to next filter
        except Exception as exc:
            print(f'DELETE_SELECT_FAILED filter={filt}: {exc!r}', flush=True)
    session.refresh()
    if not deleted:
        print('STAGE4: SKIP (delete canary unavailable headless or selset '
              'not exactly 1; P1 arc left intact)', flush=True)
        RESULTS['DELETE_RECREATE'] = 'SKIPPED'
        return
    row = find_row(session, info)
    print(f'DELETE_VERIFY: row_present_after_delete={row is not None}',
          flush=True)
    if row is not None:
        print('STAGE4: ABORT_RECREATE (old arc still present -- would '
              'create a duplicate key)', flush=True)
        RESULTS['DELETE_RECREATE'] = 'ABORTED_STILL_PRESENT'
        return
    marker_count(drc, 'DEL_AFTER_DELETE')
    rows = session.routes.create(
        info['net'],
        [info['S'], ArcTo(end=info['E'], center=info['req_C'],
                          clockwise=info['cw'])],
        pc.LAYER, pc.WIDTH)
    arcs = [r for r in rows if r.obj_type == 'arc']
    if not arcs:
        print('RECREATE: NO ARC ROW', flush=True)
        RESULTS['DELETE_RECREATE'] = 'RECREATE_FAILED'
        return
    r2 = arcs[0]
    new_com = dict(cx=float(r2.center.x), cy=float(r2.center.y),
                   r=float(r2.radius), length=float(r2.length),
                   cw=r2.is_clockwise)
    same = all(orc.bits(new_com[k]) == orc.bits(orig_com[k])
               for k in ('cx', 'cy', 'r', 'length')) \
        and new_com['cw'] == orig_com['cw']
    print(f'RECREATE_BITS: identical={same} '
          f'dcy={Decimal(new_com["cy"]) - Decimal(orig_com["cy"])} '
          f'dr={Decimal(new_com["r"]) - Decimal(orig_com["r"])}', flush=True)
    TRACK[tag]['com'] = new_com
    v_after = check_cell(session, drc, tag, 'DEL_POSTRECREATE', marker_name)
    marker_count(drc, 'DEL_AFTER_RECREATE')
    print(f'RECREATE_VERDICT: before={v_before} after={v_after} '
          f'stable={v_before == v_after}', flush=True)
    RESULTS['DELETE_RECREATE'] = (f'bits_identical={same} '
                                  f'verdict_stable={v_before == v_after}')


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> None:
    if '--selftest' in sys.argv:
        R = Decimal('0.06')
        delta = pc.floor_grid(R + 2 * Decimal(pc.R_NAT_F) + pc.W_TOTAL
                              - 2 * pc.CY_OFF_DEC)
        print(f'SELFTEST DELTA={delta}', flush=True)
        for y0, win in ((410, DELTA_WIN), (430, MARGIN_WIN),
                        (450, DELTA_WIN), (470, DELTA_WIN),
                        (490, DELTA_WIN)):
            p = plan_cell(y0, R, delta, win[0], win[1], win[2])
            print(f'SELFTEST y0={y0} {win[0]}: '
                  f'{"FOUND cy1=%r val=%s" % (p["cy1"], p["planned_val"]) if p else "NOT FOUND"}',
                  flush=True)
        # REV cell: cy1 = FWD planned + 20 (no scan)
        pf = plan_cell(490, R, delta, *DELTA_WIN)
        if pf:
            pr = plan_cell(510, R, delta, DELTA_WIN[0], DELTA_WIN[1],
                           DELTA_WIN[2],
                           cy1_override=float(Decimal(pf['cy1']) + 20))
            print(f'SELFTEST REV y0=510: cy1={pr["cy1"]!r} '
                  f'val={pr["planned_val"]}', flush=True)
        print('SELFTEST DONE', flush=True)
        return

    argv = sys.argv[1:]
    if '--phase' in argv:
        _phase_main(argv)
        return

    # Legacy single-process path (kept for the record): S2/S3 are known to
    # get an EMPTY design in-process right after S1's terminate-close
    # (root-cause campaign 2026-09: the silent axlOpenDesign refusal
    # correlates 15/15 vs 8/8 with the python process that terminate-closed
    # the F1-owning Allegro still being alive -- file age, env vars, licenses
    # and process lineage all excluded by controlled experiments; see
    # logs/probe_d.timing.*, logs/probe_d.h2.*, logs/probe_d.alive.*).
    work = Path(mkdtemp(prefix='drc-probe-d-'))
    state = run_s1(work)
    run_s2(state)
    run_s3(state)
    _summary()


def _phase_main(argv) -> None:
    """Process-separated phases: s1 creates + saves F1 and pickles state;
    s2/s3 reopen F1/F2 in fresh processes AFTER the saving process exited
    (mitigation for the empty-design open refusal).  Pickle keeps Decimals,
    tuple keys and float bits exact across the handoff."""
    i = argv.index('--phase')
    phase = argv[i + 1]
    if phase == 's1':
        work = Path(mkdtemp(prefix='drc-probe-d-'))
        state = run_s1(work)
        sf = work / 'probe_d_state.pkl'
        with open(sf, 'wb') as fh:
            pickle.dump(state, fh, protocol=4)
        print(f'STATE_FILE {sf}', flush=True)
        _summary()
        return
    sf = Path(argv[i + 2])
    with open(sf, 'rb') as fh:
        state = pickle.load(fh)
    TRACK.clear()
    TRACK.update(state['TRACK'])
    RESULTS.clear()
    RESULTS.update(state['RESULTS'])
    if phase == 's2':
        run_s2(state)
    elif phase == 's3':
        run_s3(state)
    else:
        raise SystemExit(f'unknown phase {phase!r}')
    with open(sf, 'wb') as fh:
        pickle.dump(state, fh, protocol=4)
    _summary()


def _sync_state(state: dict) -> dict:
    state['TRACK'] = dict(TRACK)
    state['RESULTS'] = dict(RESULTS)
    return state


def run_s1(work: Path) -> dict:
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    f1 = work / 'probe_d_F1.brd'
    f2 = work / 'probe_d_F2.brd'
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    print(f'WORKDIR {work}', flush=True)
    print(f'BOARD_COPY_SHA256_START {sha256(board)}', flush=True)
    ports = [_free_port() for _ in range(3)]
    print(f'PORTS {ports}', flush=True)
    state = dict(work=work, board=Path(board), f1=f1, f2=f2, ports=ports,
                 marker_name=None, s1_pre=None, v1_pre=None,
                 c1_pre=None, c1_post=None)

    # ==================================================================
    # SESSION 1: creation, checks, update, delete-recreate, save F1
    # ==================================================================
    with open_verified(board, ports[0], 'S1') as allegro:
        session = allegro.session
        ws = session.workspace
        drc = session.drc
        padstack = Counter(v.padstack
                           for v in session.vias()).most_common(1)[0][0]
        print('PADSTACK:', padstack, flush=True)
        marker_count(drc, 'BASELINE')

        # ---- STAGE 0: rule learning (probe_c STAGE1 pattern) ------------
        print('STAGE0: rule learning (natural arc y0=390 + tight line)',
              flush=True)
        cy_nat = 390.0 + CY_OFF
        s0_arc = pc.create_arc_net(session, padstack, pc.NET_A, (SX, 390.0),
                                   (EX, 390.0), (CX_NAT, cy_nat), False,
                                   'STAGE0_ARC')
        if s0_arc is None or s0_arc.center is None:
            print('STAGE0: ARC CREATION FAILED - ABORT', flush=True)
            return _sync_state(state)
        p1 = Decimal(float(s0_arc.center.y)) - Decimal(float(s0_arc.radius))
        L_dec = pc.floor_grid(p1 - pc.W_TOTAL - pc.NOMINAL_TIGHT)
        pc.create_line(session, padstack, float(L_dec), 'STAGE0_LINE')
        found = pc.run_drc(drc, s0_arc, 'STAGE0', None)
        if not found:
            print('STAGE0: NO SPACING MARKER - cannot learn R; ABORT',
                  flush=True)
            return _sync_state(state)
        if len(found) > 1:
            pref = [t for t in found
                    if t[0].lower() == 'line to line spacing']
            if pref:
                print(f'STAGE0: {len(found)} spacing markers; preferring '
                      f'Line to Line Spacing', flush=True)
                found = pref
        marker_name, expected, actual, _ = found[0]
        R_dec = Decimal(pc._quantity(expected))
        delta_dec = pc.floor_grid(R_dec + 2 * Decimal(pc.R_NAT_F)
                                  + pc.W_TOTAL - 2 * pc.CY_OFF_DEC)
        print(f'STAGE0: marker_name={marker_name!r} R={R_dec} '
              f'(actual={actual!r}) DELTA={delta_dec}', flush=True)
        marker_count(drc, 'STAGE0_END')

        def plan(y0, win, cy1_override=None):
            p = plan_cell(y0, R_dec, delta_dec, win[0], win[1], win[2],
                          cy1_override=cy1_override)
            if p is not None:
                p['R_dec'] = R_dec
            return p

        # ---- STAGE 1: repeat checks + full update ------------------------
        print('STAGE1: P1 violation cell y0=410 (repeat/update stability)',
              flush=True)
        plan_p1 = plan(410, DELTA_WIN)
        if plan_p1 is None:
            print('STAGE1: EPS_SCAN_FAILED - ABORT', flush=True)
            return _sync_state(state)
        create_pair(session, drc, padstack, 'P1', plan_p1, marker_name)
        c_after_create = marker_count(drc, 'P1_AFTER_CREATE')
        h1 = check_cell(session, drc, 'P1_UPPER', 'P1_CHECK1', marker_name)
        h2 = check_cell(session, drc, 'P1_UPPER', 'P1_CHECK2', marker_name)
        h3 = check_cell(session, drc, 'P1_UPPER', 'P1_CHECK3', marker_name)
        RESULTS['REPEAT_STABLE'] = (h1 == h2 == h3)
        print(f'REPEAT_STABLE: {h1 == h2 == h3} h1={h1} h2={h2} h3={h3}',
              flush=True)
        try:
            upd = drc.update()
            print(f'UPDATE: axlDRCUpdate markers_returned={len(upd)}',
                  flush=True)
            RESULTS['UPDATE_OK'] = True
        except Exception as exc:
            print(f'UPDATE: FAILED {exc!r}', flush=True)
            RESULTS['UPDATE_OK'] = f'FAILED {exc!r}'
        c_after_update = marker_count(drc, 'P1_AFTER_UPDATE')
        h4 = check_cell(session, drc, 'P1_UPPER', 'P1_CHECK4_AFTER_UPDATE',
                        marker_name)
        RESULTS['UPDATE_VERDICT_STABLE'] = (h4 == h1)
        print(f'UPDATE_VERDICT_STABLE: {h4 == h1} h4={h4}', flush=True)
        RESULTS['COUNT_CREATE_VS_UPDATE'] = (c_after_create, c_after_update)

        print('STAGE1: P2 clean cell y0=430 (margin window)', flush=True)
        plan_p2 = plan(430, MARGIN_WIN)
        if plan_p2 is not None:
            create_pair(session, drc, padstack, 'P2', plan_p2, marker_name)
            g1 = check_cell(session, drc, 'P2_UPPER', 'P2_CHECK1',
                            marker_name)
            g2 = check_cell(session, drc, 'P2_UPPER', 'P2_CHECK2',
                            marker_name)
            RESULTS['CLEAN_REPEAT_STABLE'] = (g1 == g2 == ('clean', None, None))
            print(f'CLEAN_REPEAT_STABLE: {g1 == g2} g1={g1} g2={g2}',
                  flush=True)
        h5 = check_cell(session, drc, 'P1_UPPER', 'P1_CHECK5_AFTER_P2',
                        marker_name)
        RESULTS['FAR_OBJECT_STABLE'] = (h5 == h1)
        print(f'FAR_OBJECT_STABLE: {h5 == h1} h5={h5}', flush=True)

        # ---- STAGE 2: order swap -----------------------------------------
        print('STAGE2: order swap (y0=450 upper-first vs y0=470 '
              'lower-first)', flush=True)
        va = vb = None
        plan_a = plan(450, DELTA_WIN)
        plan_b = plan(470, DELTA_WIN)
        if plan_a is not None and plan_b is not None:
            create_pair(session, drc, padstack, 'ORD_A', plan_a, marker_name,
                        lower_first=False)
            va = check_cell(session, drc, 'ORD_A_UPPER', 'ORD_A_CHECK',
                            marker_name)
            create_pair(session, drc, padstack, 'ORD_B', plan_b, marker_name,
                        lower_first=True)
            vb = check_cell(session, drc, 'ORD_B_UPPER', 'ORD_B_CHECK',
                            marker_name)
            cyA = TRACK['ORD_A_UPPER']['com']['cy']
            cyB = TRACK['ORD_B_UPPER']['com']['cy']
            rA = TRACK['ORD_A_UPPER']['com']['r']
            rB = TRACK['ORD_B_UPPER']['com']['r']
            print(f'ORDER_SWAP: verdictA={va} verdictB={vb}', flush=True)
            print(f'ORDER_SWAP: dcy(committed)-20={Decimal(cyB) - Decimal(cyA) - 20} '
                  f'dr={Decimal(rB) - Decimal(rA)}', flush=True)
            RESULTS['ORDER_SWAP_CONSISTENT'] = (
                va[0] == vb[0] == 'FLAGGED' and va[1] == vb[1])
        else:
            RESULTS['ORDER_SWAP_CONSISTENT'] = 'SCAN_FAILED'

        # ---- STAGE 3: equivalent representation ---------------------------
        print('STAGE3: forward y0=490 vs reversed y0=510 (S/E swap + cw '
              'flip, identical center offset)', flush=True)
        vf = vr = None
        plan_f = plan(490, DELTA_WIN)
        if plan_f is not None:
            create_pair(session, drc, padstack, 'FWD', plan_f, marker_name)
            vf = check_cell(session, drc, 'FWD_UPPER', 'FWD_CHECK',
                            marker_name)
            # offset from the COMMITTED FWD center (mirrors probe_c FLIP_HI
            # construction): keeps the two cells exact 20 mm translates
            cy1_rev = float(Decimal(TRACK['FWD_UPPER']['com']['cy'])
                            + Decimal(20))
            plan_r = plan(510, DELTA_WIN, cy1_override=cy1_rev)
            if plan_r is not None:
                create_pair(session, drc, padstack, 'REV', plan_r,
                            marker_name, reverse_upper=True)
                vr = check_cell(session, drc, 'REV_UPPER', 'REV_CHECK',
                                marker_name)
                fC = TRACK['FWD_UPPER']['com']
                rC = TRACK['REV_UPPER']['com']
                print(f'REVERSED_EQUIV: verdictF={vf} verdictR={vr}',
                      flush=True)
                print(f'REVERSED_EQUIV: dcx={Decimal(rC["cx"]) - Decimal(fC["cx"])} '
                      f'dcy-20={Decimal(rC["cy"]) - Decimal(fC["cy"]) - 20} '
                      f'dr={Decimal(rC["r"]) - Decimal(fC["r"])} '
                      f'dlength={Decimal(rC["length"]) - Decimal(fC["length"])}',
                      flush=True)
                print(f'REVERSED_EQUIV: cw fwd={fC["cw"]!r} rev={rC["cw"]!r} '
                      f'r_bits_equal={orc.bits(rC["r"]) == orc.bits(fC["r"])} '
                      f'len_bits_equal={orc.bits(rC["length"]) == orc.bits(fC["length"])}',
                      flush=True)
                cf = committed_clear('FWD')
                cr = committed_clear('REV')
                print(f'REVERSED_EQUIV: clear_fwd={cf} clear_rev={cr} '
                      f'dclear={cr - cf}', flush=True)
                RESULTS['REVERSED_EQUIVALENT'] = (
                    vf[0] == vr[0] and vf[1] == vr[1]
                    and orc.bits(rC['r']) == orc.bits(fC['r']))
            else:
                RESULTS['REVERSED_EQUIVALENT'] = 'SCAN_FAILED'
        else:
            RESULTS['REVERSED_EQUIVALENT'] = 'SCAN_FAILED'

        # ---- STAGE 4: delete-recreate canary ------------------------------
        print('STAGE4: delete-recreate P1 upper (raw SKILL canary)',
              flush=True)
        stage4_delete_recreate(session, drc, padstack, ws, marker_name)

        # ---- STAGE 5a: pre-save snapshot + save F1 + post-save ------------
        print('STAGE5: save/reopen round-trip', flush=True)
        s1_pre = snap(session, 'S1_PRE')
        v1_pre = verdict_snapshot(session, drc, 'S1_PRE_CHECK', marker_name)
        c1_pre = marker_count(drc, 'S1_PRE')
        try:
            save1 = ws['axlSaveDesign'](design=f1.as_posix(), no_confirm=True)
            print(f'SAVE F1: result={save1!r} exists={f1.exists()} '
                  f'size={f1.stat().st_size if f1.exists() else None}',
                  flush=True)
        except Exception as exc:
            save1 = None
            print(f'SAVE F1: FAILED {exc!r}', flush=True)
        RESULTS['SAVE_F1'] = ('OK' if f1.exists() else f'FAILED result={save1!r}')
        if f1.exists():
            print(f'F1_SHA256 {sha256(f1)}', flush=True)
        session.refresh()          # axlSaveDesign cleared all dbid handles
        s1_post = snap(session, 'S1_POST')
        RESULTS['BITS_S1_POST_SAVE'] = snap_compare('S1_SAVE_INMEMORY',
                                                    s1_pre, s1_post)
        v1_post = verdict_snapshot(session, drc, 'S1_POST_CHECK', marker_name)
        verdict_compare('S1_SAVE_INMEMORY', v1_pre, v1_post, VTAGS)
        c1_post = marker_count(drc, 'S1_POST')
        print(f'BOARD_COPY_SHA256_AFTER_SAVE {sha256(board)}', flush=True)

    state.update(marker_name=marker_name, s1_pre=s1_pre, v1_pre=v1_pre,
                 c1_pre=c1_pre, c1_post=c1_post)
    return _sync_state(state)


# ======================================================================
# SESSION 2: reopen F1, compare, update, save F2
# ======================================================================

def run_s2(state: dict) -> None:
    f1, f2 = state['f1'], state['f2']
    s1_pre, v1_pre = state['s1_pre'], state['v1_pre']
    c1_pre, c1_post = state['c1_pre'], state['c1_post']
    marker_name = state['marker_name']
    if not f1.exists():
        print('SESSION2: SKIP (F1 missing)', flush=True)
        _sync_state(state)
        return
    with open_verified(f1, _free_port(), 'S2') as allegro2:
        session2 = allegro2.session
        ws2 = session2.workspace
        drc2 = session2.drc
        print('SESSION2: opened F1', flush=True)
        c2_persist = marker_count(drc2, 'S2_PERSISTED')
        s2 = snap(session2, 'S2')
        RESULTS['BITS_S2_REOPEN'] = snap_compare('S2_REOPEN', s1_pre, s2)
        v2 = verdict_snapshot(session2, drc2, 'S2_CHECK', marker_name)
        bad2 = verdict_compare('S2_REOPEN', v1_pre, v2, VTAGS)
        RESULTS['VERDICTS_S2_STABLE'] = not bad2
        print(f'COUNT S1_PRE={c1_pre} S1_POST={c1_post} S2_PERSISTED={c2_persist}',
              flush=True)
        try:
            upd2 = drc2.update()
            print(f'S2_UPDATE: markers_returned={len(upd2)}', flush=True)
            c2_regen = marker_count(drc2, 'S2_AFTER_UPDATE')
            v2u = verdict_snapshot(session2, drc2, 'S2_POST_UPDATE_CHECK',
                                   marker_name, tags=('P1_UPPER',))
            verdict_compare('S2_AFTER_UPDATE', v2, v2u, ('P1_UPPER',))
            print(f'COUNT S2_PERSISTED={c2_persist} S2_REGENERATED={c2_regen}',
                  flush=True)
        except Exception as exc:
            print(f'S2_UPDATE: FAILED {exc!r}', flush=True)
        try:
            save2 = ws2['axlSaveDesign'](design=f2.as_posix(), no_confirm=True)
            print(f'SAVE F2: result={save2!r} exists={f2.exists()} '
                  f'size={f2.stat().st_size if f2.exists() else None}',
                  flush=True)
        except Exception as exc:
            print(f'SAVE F2: FAILED {exc!r}', flush=True)
        if f2.exists():
            h1s, h2s = sha256(f1), sha256(f2)
            print(f'F2_SHA256 {h2s}', flush=True)
            print(f'F1_SHA256 {h1s}', flush=True)
            RESULTS['F1_F2_IDENTICAL'] = (h1s == h2s
                                          and f1.stat().st_size
                                          == f2.stat().st_size)
    _sync_state(state)


# ======================================================================
# SESSION 3: reopen F2 (snapshot-level compare)
# ======================================================================

def run_s3(state: dict) -> None:
    f2 = state['f2']
    s1_pre, v1_pre = state['s1_pre'], state['v1_pre']
    marker_name = state['marker_name']
    if f2.exists():
        with open_verified(f2, _free_port(), 'S3') as allegro3:
            session3 = allegro3.session
            drc3 = session3.drc
            print('SESSION3: opened F2', flush=True)
            c3 = marker_count(drc3, 'S3_PERSISTED')
            s3 = snap(session3, 'S3')
            RESULTS['BITS_S3_F2_REOPEN'] = snap_compare('S3_F2_REOPEN',
                                                        s1_pre, s3)
            v3 = verdict_snapshot(session3, drc3, 'S3_CHECK', marker_name,
                                  tags=('P1_UPPER', 'REV_UPPER'))
            bad3 = verdict_compare(
                'S3_F2_REOPEN', v1_pre, v3, ('P1_UPPER', 'REV_UPPER'))
            RESULTS['VERDICTS_S3_STABLE'] = not bad3
    else:
        print('SESSION3: SKIP (F2 missing)', flush=True)
    _sync_state(state)


def _summary() -> None:
    print('SUMMARY', flush=True)
    for k, v in RESULTS.items():
        print(f'RESULT {k}={v!r}', flush=True)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()
