# Phase 0/1: ARC persistence probe.  Disposable board copy, owned Allegro.
#
# Questions (task spec Phase 0):
#   Q1  Which arc fields are grid-quantized at commit and which keep binary64?
#       (start/end vs center vs radius vs length), %.17g + bit patterns.
#   Q1b Is the center STORED as requested, or re-derived (from endpoints, from
#       quantized endpoints, etc.)?  A2 (sub-grid dy) and A5 (inconsistent
#       |S-C| != |E-C|) discriminate.
#   Q1c Which radius does Allegro commit for an inconsistent center? |S-C|,
#       |E-C|, something else?
#   Q1d is_clockwise convention: A3/A4 are grid-exact 3-4-5 arcs where the two
#       sweep directions have very different lengths (2.3182 vs 5.5358) -
#       committed length calibrates the convention.
#   Q1e Does an independent re-query (session.routes) return bit-identical
#       center/radius/length, or is any of it derived at projection time?
#
# Net anchoring: isolated etch gets no net (probe-verified), so each arc starts
# on a net-assigned via -> arcs inherit NET_A and drc.check() can target them.
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import math
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

import arc_oracle as orc
from allegrobridge import Allegro
from allegrobridge.client.api.geometry import ArcTo
from allegrobridge.util import ASSETS_DIR

NET_A = 'NFC_SWP'
LAYER = 'ETCH/TOP'
WIDTH = 0.15
X0 = 300.0


def _f(value) -> str:
    """Full-fidelity scalar dump."""
    if value is None:
        return 'None'
    v = float(value)
    return (f'{v!r} bits={orc.bits(v)} on_grid={orc.on_grid(v)} '
            f'frac_g={orc.frac_grid(v)}')


def _point(tag: str, p) -> str:
    if p is None:
        return f'{tag}=None'
    if isinstance(p, (tuple, list)):
        x, y = float(p[0]), float(p[1])
    else:
        x, y = float(p.x), float(p.y)
    return (f'{tag}=({x!r},{y!r}) bits=({orc.bits(x)},{orc.bits(y)}) '
            f'on_grid=({orc.on_grid(x)},{orc.on_grid(y)})')


def _dist_dec(a, b) -> Decimal:
    """Exact 60-digit distance between two committed doubles."""
    dx = Decimal(a[0]) - Decimal(b[0])
    dy = Decimal(a[1]) - Decimal(b[1])
    return (dx * dx + dy * dy).sqrt()


def dump_row(tag: str, row) -> tuple:
    print(f'   {tag}: net={row.net!r} obj_type={row.obj_type!r} layer={row.layer!r}',
          flush=True)
    print(f'      start: {_f(row.start.x)} | {_f(row.start.y)}', flush=True)
    print(f'      end:   {_f(row.end.x)} | {_f(row.end.y)}', flush=True)
    w = row.width
    if hasattr(w, 'x'):
        print(f'      width: {_f(w.x)} | {_f(w.y)}', flush=True)
    else:
        print(f'      width: {_f(w)}', flush=True)
    print(f'      length: {_f(row.length)}', flush=True)
    print(f'      radius: {_f(row.radius)}', flush=True)
    print(f'      is_clockwise={row.is_clockwise!r}', flush=True)
    print(f'      center: ' + (_f(row.center.x) + ' | ' + _f(row.center.y)
                               if row.center is not None else 'None'), flush=True)
    key = (row.start.x, row.start.y, row.end.x, row.end.y)
    return key


def analyze(case: dict, row) -> None:
    """Predictions vs committed: radius derivation, direction, bottom point."""
    S = (float(row.start.x), float(row.start.y))
    E = (float(row.end.x), float(row.end.y))
    C = (float(row.center.x), float(row.center.y)) if row.center else None
    r = float(row.radius) if row.radius is not None else None
    length = float(row.length)
    reqC = case['C']
    print('   ANALYSIS:', flush=True)
    if C is None or r is None:
        print('      no center/radius committed - arc fields missing!', flush=True)
        return
    # center preservation vs requested
    dc = _dist_dec(C, reqC)
    print(f'      |C_committed - C_requested| = {dc} '
          f'(sub-grid preserved: {dc != 0})', flush=True)
    # radius derivation: compare against both endpoint distances
    dS = _dist_dec(S, C)
    dE = _dist_dec(E, C)
    print(f'      |S-C| = {dS}', flush=True)
    print(f'      |E-C| = {dE}', flush=True)
    print(f'      r_committed - |S-C| = {Decimal(r) - dS}', flush=True)
    print(f'      r_committed - |E-C| = {Decimal(r) - dE}', flush=True)
    # direction convention via length
    cw = bool(row.is_clockwise)
    sw_cw = orc.sweep_deg(S, E, C, clockwise=True)    # math-CW (y-up)
    sw_ccw = orc.sweep_deg(S, E, C, clockwise=False)
    len_cw = orc.arc_length(r, sw_cw)
    len_ccw = orc.arc_length(r, sw_ccw)
    print(f'      length_committed={length!r}', flush=True)
    print(f'      pred math-CW:  sweep={sw_cw:.4f} deg length={len_cw!r}', flush=True)
    print(f'      pred math-CCW: sweep={sw_ccw:.4f} deg length={len_ccw!r}', flush=True)
    near = 'math-CW' if abs(length - len_cw) < abs(length - len_ccw) else 'math-CCW'
    print(f'      committed length matches {near}; is_clockwise={cw!r}', flush=True)
    # bottom point (for later Line-ARC clearance work)
    bottom_y = Decimal(C[1]) - Decimal(r)
    print(f'      bottom=(Decimal {C[0]!r}, {bottom_y}) '
          f'float={float(bottom_y)!r} on_grid={orc.on_grid(float(bottom_y))}',
          flush=True)
    for direction in (True, False):
        print(f'      bottom_in_span(math_cw={direction}): '
              f'{orc.bottom_in_span(S, E, C, direction)}', flush=True)


def run_case(session, case: dict, padstack: str):
    cid = case['id']
    S, E, C, cw = case['S'], case['E'], case['C'], case['cw']
    print(f'CASE {cid}', flush=True)
    print(f'   requested {_point("S", S)}', flush=True)
    print(f'   requested {_point("E", E)}', flush=True)
    print(f'   requested {_point("C", C)}  cw={cw!r}', flush=True)
    if 'exact' in case:
        cx, cy, r2 = case['exact']
        print(f'   exact circumcenter: cx={cx} cy={cy} r2={r2}', flush=True)
        print(f'   exact r = {orc.dec_sqrt(r2)}', flush=True)
        cxd = Decimal(cx.numerator) / Decimal(cx.denominator)
        cyd = Decimal(cy.numerator) / Decimal(cy.denominator)
        print(f'   float(C) - exact(C): dx={Decimal(C[0]) - cxd} '
              f'dy={Decimal(C[1]) - cyd}', flush=True)
    try:
        session.vias.create(padstack, at=(S[0], S[1]), net=NET_A)
        rows = session.routes.create(
            NET_A, [S, ArcTo(end=E, center=C, clockwise=cw)], LAYER, WIDTH)
    except Exception as exc:  # creation may legitimately fail (A5) - record it
        print(f'   CREATE_FAILED: {exc!r}', flush=True)
        return None
    print(f'   ROWS={len(rows)}', flush=True)
    arc_rows = [r for r in rows if r.obj_type == 'arc']
    for i, row in enumerate(rows):
        dump_row(f'committed[{i}]', row)
    if arc_rows:
        analyze(case, arc_rows[0])
    return rows


def main() -> None:
    # ---- case construction (all math exact where possible) ----------------
    cases = []

    # A1: task's natural 3-point spec: grid S/E, off-grid mid -> natural
    # non-grid circumcenter.  math-CW passes through M (verified below).
    S1, M1, E1 = (300.0, 300.0), (300.5, 301.0), (302.0001, 300.0)
    cx, cy, r2 = orc.circumcenter(S1, M1, E1)
    C1 = (float(cx), float(cy))
    cases.append(dict(id='A1_NATURAL', S=S1, E=E1, C=C1, cw=True,
                      exact=(cx, cy, r2), M=M1))

    # A2: same geometry +10mm in y, center nudged +1e-6 (sub-grid, wire-exact).
    S2, M2, E2 = (300.0, 310.0), (300.5, 311.0), (302.0001, 310.0)
    cx2, cy2, r22 = orc.circumcenter(S2, M2, E2)
    C2 = (float(cx2), float(cy2) + 1e-6)
    cases.append(dict(id='A2_SUBGRID_CY', S=S2, E=E2, C=C2, cw=True,
                      exact=(cx2, cy2 + Fraction(1, 10**6), r22)))

    # A3/A4: grid-exact 3-4-5 arc, r=1.25 exact, both cw values.
    # math-CCW = bottom arc (sweep 106.26 deg, length 2.31824);
    # math-CW  = top arc    (sweep 253.74 deg, length 5.53576).
    cases.append(dict(id='A3_GRID_CW', S=(300.0, 320.0), E=(302.0, 320.0),
                      C=(301.0, 320.75), cw=True))
    cases.append(dict(id='A4_GRID_CCW', S=(300.0, 330.0), E=(302.0, 330.0),
                      C=(301.0, 330.75), cw=False))

    # A5: over-constrained - explicit center NOT equidistant from S/E.
    # |S-C| vs |E-C| differ ~4e-5; which does the committed radius follow?
    cases.append(dict(id='A5_OFFGRID_INCONSISTENT', S=(300.0, 340.0),
                      E=(302.0, 340.0), C=(301.00002, 340.75003), cw=False))

    # A6: two rungs, centers differing by 4e-6 in x (both sub-grid offsets
    # from a common nominal).  Verifies sub-grid center DIFFERENCES persist
    # (persistence half of Phase 4; the DRC half needs Probe B/C).
    cases.append(dict(id='A6_SUBGRID_PAIR_LO', S=(300.0, 350.0),
                      E=(302.0, 350.0), C=(301.00001 - 2e-6, 350.75), cw=False))
    cases.append(dict(id='A6_SUBGRID_PAIR_HI', S=(300.0, 360.0),
                      E=(302.0, 360.0), C=(301.00001 + 2e-6, 360.75), cw=False))

    # sanity: A1 arc passes through M under math-CW?
    th_s = orc.angle_deg(C1, S1)
    th_m = orc.angle_deg(C1, M1)
    th_e = orc.angle_deg(C1, E1)
    print(f'A1 angles: S={th_s:.4f} M={th_m:.4f} E={th_e:.4f} '
          f'sweep_cw={orc.sweep_deg(S1, E1, C1, True):.4f} '
          f'M_in_cw_span={(th_s - th_m) % 360.0 <= orc.sweep_deg(S1, E1, C1, True)}',
          flush=True)

    # ---- Allegro run -------------------------------------------------------
    work = Path(mkdtemp(prefix='drc-probe-arca-'))
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    with socket() as listener:
        listener.bind(('localhost', 0))
        port = str(listener.getsockname()[1])

    with Allegro.open(mode='cli', board=board, workspace_id=port, timeout=300.0) as allegro:
        session = allegro.session
        existing = session.vias()
        padstack = Counter(v.padstack for v in existing).most_common(1)[0][0]
        print('PADSTACK:', padstack, flush=True)

        committed = {}
        for case in cases:
            rows = run_case(session, case, padstack)
            if rows:
                for row in rows:
                    if row.obj_type == 'arc':
                        committed[case['id']] = row

        # ---- independent re-query: are center/radius/length stored or derived?
        print('REQUERY: session.routes(net=NET_A, layer=LAYER)', flush=True)
        requeried = [r for r in session.routes(net=NET_A, layer=LAYER)
                     if r.obj_type == 'arc']
        print(f'REQUERY_ARC_COUNT: {len(requeried)} (created: {len(committed)})',
              flush=True)
        for cid, row in committed.items():
            match = [q for q in requeried
                     if (q.start.x, q.start.y, q.end.x, q.end.y)
                     == (row.start.x, row.start.y, row.end.x, row.end.y)]
            if len(match) != 1:
                print(f'REQUERY {cid}: MATCH_COUNT={len(match)} (AMBIGUOUS/MISSING)',
                      flush=True)
                continue
            q = match[0]
            same_c = (q.center is not None and row.center is not None
                      and orc.bits(q.center.x) == orc.bits(row.center.x)
                      and orc.bits(q.center.y) == orc.bits(row.center.y))
            same_r = (q.radius is not None and row.radius is not None
                      and orc.bits(q.radius) == orc.bits(row.radius))
            same_l = orc.bits(q.length) == orc.bits(row.length)
            print(f'REQUERY {cid}: center_identical={same_c} '
                  f'radius_identical={same_r} length_identical={same_l}', flush=True)
            if not (same_c and same_r and same_l):
                dump_row(f'requery[{cid}]', q)

        print('DONE', flush=True)


if __name__ == '__main__':
    main()
