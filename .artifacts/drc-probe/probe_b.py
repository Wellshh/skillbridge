# Phase 2/3/4/5: Line-ARC critical DRC probe.  Disposable board copy, owned
# Allegro process, unique port.  No production code modified.
#
# Calibrated by probe A (same directory, completed):
#   - center is STORED; the on-bisector component of the requested center is
#     preserved BIT-EXACTLY (A1/A2).  Off-bisector components are projected
#     away (A5/A6) -> all perturbations here are in cy (bisector direction).
#   - radius is DERIVED by Allegro from the stored center, with an arithmetic
#     noise envelope |r_committed - |S-C|_exact| <= 1.5e-14 (all A cases).
#     Every L below is computed from the COMMITTED r (self-calibration), so
#     this noise never reaches the window margins (>= 3e-7).
#   - clockwise=False => math-CCW (y-up) => the BOTTOM arc for C above the
#     chord; bottom_in_span(math_ccw)=True (A4).  Probe A showed the scan's
#     original cw=True config is the TOP arc (bottom NOT in span) - all
#     critical rungs here use cw=False.
#   - re-query returns bit-identical center/radius/length => stored state.
#
# Stages (one Allegro run):
#   STAGE 1  y0=400 natural-center arc + line ~0.01mm below -> learn rule R
#            and the arc-line marker name (NEVER hardcode 0.06).
#   STAGE 2  critical rungs, each an independent 10mm-separated cell:
#     FLIP_LO y0=410  phi in FLIP window, below-placement:
#                     clearance = R - delta, delta ~ 2.5e-6.
#                     Model A: FLAGGED with actual display == expected
#                     (Phase 3 gold case).  Model B/C: clean.
#     FLIP_HI y0=420  cy = cy_lo + 10 + 3.5e-6 (dp/dcy ~ 0.876 -> crosses R
#                     by ~ +0.6e-6), above-placement: clearance = R + ~6e-7.
#                     Clean under ALL models.  FLIP_LO/HI pair = Phase 4:
#                     identical construction; the only non-grid difference is
#                     3.5e-6 in cy.  Verdict flip => DRC sees sub-grid center.
#     GOLD    y0=430  delta ~ 4.9e-5 below R (wide-margin A-vs-B/C discriminator;
#                     also bounds any hypothetical epsilon band).
#     ABOVE   y0=440  phi ~ 1.5e-5, above-placement: clearance = R + 1.5e-5,
#                     clean control, round4 == R.
#     BELOW   y0=450  same phi window, below-placement: clearance = R - 8.5e-5
#                     -> FLAGGED with actual '0.0599 MM' != expected (ordinary
#                     violation control: marker mechanics + display rounding).
#     GRID_EQ   y0=460 grid-exact 3-4-5 arc (bottom on grid), clearance == R
#                     exactly -> clean (equality precedent from line ladder).
#     GRID_FLAG y0=470 same arc, clearance == R - 1e-4 -> FLAGGED '0.0599 MM'.
#     STAIR     y0=480..580 (11 rungs) grid arcs, clearance R+5g ... R-5g
#                     (Phase 5 staircase; requested AND committed L recorded).
#   STAGE 3  per-rung 4-model oracle (FULL / BINARY64 / GRID / DISTANCE-ROUND)
#            computed from COMMITTED geometry, vs actual drc.check verdict.
#   STAGE 4  re-query all arcs: bit-identity (storage stability in-session).
#
# Model discrimination (lines always commit on-grid, so for Line-ARC
# B and C are observationally equivalent - separating them needs ARC-ARC,
# which is Probe C):
#   FLIP_LO or GOLD FLAGGED            => model A (full-precision measurement)
#   both clean + GRID_FLAG flagged     => model B/C (distance or geometry is
#                                         quantized to the grid before compare)
#   GOLD flagged + FLIP_LO clean       => epsilon-band model, band in
#                                         (2.5e-6, 4.9e-5)
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

from collections import Counter
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

import arc_oracle as orc
from scan_window import CX_NAT, CY_OFF, EX, SX, exact_case, phi_float
from allegrobridge import Allegro
from allegrobridge.client.api.geometry import ArcTo
from allegrobridge.util import ASSETS_DIR

NET_A = 'NFC_SWP'
NET_B = 'FINGER_SPI_MISO'
LAYER = 'ETCH/TOP'
WIDTH = 0.15
W_TOTAL = Decimal('0.15')      # (w_arc + w_line)/2 exact in decimal
GRID = Decimal('0.0001')
NOMINAL_TIGHT = Decimal('0.01')  # stage-1 rule-probe clearance

PHI_FLIP = (Decimal('0.0000975'), Decimal('0.0000995'))
PHI_GOLD = (Decimal('0.000051'), Decimal('0.000095'))
PHI_ABOVE = (Decimal('0.0000005'), Decimal('0.000025'))


def floor_grid(x: Decimal) -> Decimal:
    return x.quantize(GRID, rounding=ROUND_FLOOR)


def disp(dec: Decimal) -> str:
    """Predicted marker display: round-to-nearest at accuracy, zeros stripped."""
    q = dec.quantize(GRID, rounding=orc.ROUND_HALF_EVEN).normalize()
    return f'{q} MM'


def _f(value) -> str:
    if value is None:
        return 'None'
    v = float(value)
    return (f'{v!r} bits={orc.bits(v)} on_grid={orc.on_grid(v)} '
            f'frac_g={orc.frac_grid(v)}')


def _quantity(text: str) -> str:
    """Marker quantity strings like '0.06 MM' -> numeric part as str."""
    return text.split()[0]


def find_cy(y0: float, window) -> float | None:
    """Scan cy around the natural circumcenter for phi inside window."""
    lo, hi = window
    cy_nat = y0 + CY_OFF
    cy = cy_nat - 1.5e-4
    for _ in range(40000):
        if float(lo) <= phi_float(cy, y0) <= float(hi):
            case = exact_case(cy, y0)
            if lo <= case['phi'] <= hi:
                return cy
        cy += 1e-8
    return None


def create_arc(session, padstack, S, E, C, cw, tag):
    """Via-anchor at S (net inheritance), create arc, dump requested vs
    committed center/radius at bit level.  Returns the committed arc row."""
    print(f'--- {tag}: ARC requested S={S!r} E={E!r} C={C!r} cw={cw!r}',
          flush=True)
    print(f'    requested C bits=({orc.bits(C[0])},{orc.bits(C[1])})', flush=True)
    session.vias.create(padstack, at=(S[0], S[1]), net=NET_A)
    rows = session.routes.create(
        NET_A, [S, ArcTo(end=E, center=C, clockwise=cw)], LAYER, WIDTH)
    arcs = [r for r in rows if r.obj_type == 'arc']
    if len(arcs) != 1:
        print(f'    UNEXPECTED ROWS={len(rows)} arcs={len(arcs)}', flush=True)
        for r in rows:
            print(f'    row: obj_type={r.obj_type!r} net={r.net!r} '
                  f'({r.start.x!r},{r.start.y!r})->({r.end.x!r},{r.end.y!r})',
                  flush=True)
        if not arcs:
            return None
    row = arcs[0]
    cc = (float(row.center.x), float(row.center.y))
    print(f'    committed net={row.net!r} is_clockwise={row.is_clockwise!r}',
          flush=True)
    print(f'    committed center: {_f(row.center.x)} | {_f(row.center.y)}',
          flush=True)
    print(f'    committed radius: {_f(row.radius)}', flush=True)
    print(f'    committed length: {_f(row.length)}', flush=True)
    same = (orc.bits(cc[0]) == orc.bits(C[0]) and orc.bits(cc[1]) == orc.bits(C[1]))
    print(f'    center bit-preserved: {same}  '
          f'dC=({Decimal(cc[0]) - Decimal(C[0])}, {Decimal(cc[1]) - Decimal(C[1])})',
          flush=True)
    r_exact = ((Decimal(cc[0]) - Decimal(S[0])) ** 2
               + (Decimal(cc[1]) - Decimal(S[1])) ** 2).sqrt()
    print(f'    r_committed - |S-C|_exact = {Decimal(float(row.radius)) - r_exact}',
          flush=True)
    in_span = orc.bottom_in_span(S, E, cc, clockwise=False)
    print(f'    bottom_in_span(math_ccw): {in_span}', flush=True)
    return row


def create_line(session, padstack, x0, x1, L, tag):
    """NET_B horizontal line anchored on its own via.  Records requested AND
    committed positions (task requirement)."""
    print(f'--- {tag}: LINE requested y={L!r} bits={orc.bits(L)} '
          f'on_grid={orc.on_grid(L)}', flush=True)
    session.vias.create(padstack, at=(x0, L), net=NET_B)
    rows = session.routes.create(NET_B, [(x0, L), (x1, L)], LAYER, WIDTH)
    if len(rows) != 1:
        print(f'    UNEXPECTED LINE ROWS={len(rows)}', flush=True)
    row = rows[0]
    yc = float(row.start.y)
    print(f'    committed net={row.net!r} y={_f(row.start.y)} '
          f'(end y={float(row.end.y)!r})', flush=True)
    print(f'    committed - requested dy = {Decimal(yc) - Decimal(L)}', flush=True)
    return row


def oracle(C, r, line_y, w_arc, w_line, R_dec, R_float, tag):
    """4-model predictions from COMMITTED geometry.  Returns dict of verdicts."""
    full = orc.model_FULL(C, Decimal(r), line_y, w_arc, w_line)
    b64 = orc.model_BINARY64(C, r, line_y, w_arc, w_line)
    grid = orc.model_GRID(C, r, line_y, w_arc, w_line)
    dround = orc.model_DISTANCE_ROUND(full)
    # tie check for the display/distance rounding (exact half-grid)
    tie = (full / GRID) % 1 == Decimal('0.5')
    print(f'    MODELS[{tag}] (R={R_dec}):', flush=True)
    print(f'      FULL       clearance={full}', flush=True)
    print(f'                 verdict={orc.verdict(full, R_dec)}', flush=True)
    print(f'      BINARY64   clearance={b64!r} (<R_float: {b64 < R_float}) '
          f'verdict={orc.verdict(b64, R_float)}', flush=True)
    print(f'      GRID       quant4(cy)={orc.quant4(C[1])!r} '
          f'quant4(r)={orc.quant4(r)!r} clearance={grid} '
          f'verdict={orc.verdict(grid, R_dec)}', flush=True)
    print(f'      DROUND     round4(FULL)={dround} (half-even; exact_tie={tie}) '
          f'verdict={orc.verdict(dround, R_dec)}', flush=True)
    print(f'      predicted display if flagged: {disp(full)!r}', flush=True)
    return dict(full=orc.verdict(full, R_dec), b64=orc.verdict(b64, R_float),
                grid=orc.verdict(grid, R_dec), dround=orc.verdict(dround, R_dec),
                clearance_full=full)


def run_drc(drc, arc_row, tag, marker_name):
    """drc.check the arc; classify markers.  Returns spacing-marker list."""
    try:
        markers = drc.check(arc_row)
    except Exception as exc:
        print(f'    DRC_CHECK_FAILED[{tag}]: {exc!r}', flush=True)
        return None
    if marker_name is None:  # stage 1: discover
        for m in markers:
            print(f'    MARKER[{tag}]: category={m.category!r} name={m.name!r} '
                  f'expected={m.expected!r} actual={m.actual!r} '
                  f'figures={[f.obj_type for f in m.figures]}', flush=True)
        cand = [m for m in markers
                if any(f.obj_type == 'arc' for f in m.figures)
                and m.name.lower().endswith('spacing')]
        return cand
    spacing = [m for m in markers if m.name.lower() == marker_name]
    other = [m for m in markers if m.name.lower() != marker_name]
    verdict = 'FLAGGED' if spacing else 'clean'
    expected = repr(spacing[0].expected) if spacing else ''
    actual = repr(spacing[0].actual) if spacing else ''
    print(f'    DRC[{tag}]: {verdict} expected={expected} actual={actual}',
          flush=True)
    if spacing:
        for figure in spacing[0].figures:
            print('      FIGURE:', figure.obj_type, figure.layer,
                  'net=', figure.net,
                  'start=', figure.start, 'end=', figure.end,
                  'center=', getattr(figure, 'center', None),
                  'radius=', getattr(figure, 'radius', None),
                  'w=', figure.width, flush=True)
    for m in other:
        print('      OTHER:', m.category, '|', m.name,
              '| expected=', repr(m.expected), '| actual=', repr(m.actual),
              flush=True)
    return spacing


def main() -> None:
    # ---- offline: window scan for critical cy candidates (R-independent) ----
    cy_flip_lo = find_cy(410.0, PHI_FLIP)
    cy_gold = find_cy(430.0, PHI_GOLD)
    cy_above = find_cy(440.0, PHI_ABOVE)
    cy_below = find_cy(450.0, PHI_ABOVE)
    print(f'SCAN cy_flip_lo(410)={cy_flip_lo!r}', flush=True)
    if cy_flip_lo is not None:
        cy_flip_hi = cy_flip_lo + 10.0 + 3.5e-6
        print(f'SCAN cy_flip_hi(420)={cy_flip_hi!r} (= cy_lo + 10 + 3.5e-6)',
              flush=True)
        for nm, cy in (('flip_lo', cy_flip_lo), ('flip_hi', cy_flip_hi),
                       ('gold', cy_gold), ('above', cy_above), ('below', cy_below)):
            y0 = {
                'flip_lo': 410.0, 'flip_hi': 420.0, 'gold': 430.0,
                'above': 440.0, 'below': 450.0,
            }[nm]
            if cy is None:
                print(f'SCAN {nm}: NOT FOUND', flush=True)
                continue
            c = exact_case(cy, y0)
            print(f"SCAN {nm}: cy={cy!r} phi={c['phi']} "
                  f"delta_below={GRID - c['phi']} r_s={c['r_s']!r}", flush=True)
    else:
        print('SCAN: FLIP window not found - aborting', flush=True)
        return
    if None in (cy_gold, cy_above, cy_below):
        print('SCAN: a window was not found - aborting', flush=True)
        return

    # ---- Allegro run --------------------------------------------------------
    work = Path(mkdtemp(prefix='drc-probe-arcb-'))
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    with socket() as listener:
        listener.bind(('localhost', 0))
        port = str(listener.getsockname()[1])

    with Allegro.open(mode='cli', board=board, workspace_id=port,
                      timeout=300.0) as allegro:
        session = allegro.session
        drc = session.drc
        padstack = Counter(v.padstack for v in session.vias()).most_common(1)[0][0]
        print('PADSTACK:', padstack, flush=True)

        # ================= STAGE 1: learn rule R and marker name =============
        print('===== STAGE 1: rule probe (y0=400, natural center, tight pair)',
              flush=True)
        y0 = 400.0
        S1, E1 = (SX, y0), (EX, y0)
        C1 = (CX_NAT, y0 + CY_OFF)
        arc1 = create_arc(session, padstack, S1, E1, C1, False, 'STAGE1')
        if arc1 is None:
            print('STAGE1: arc creation failed - aborting', flush=True)
            return
        p1 = Decimal(float(arc1.center.y)) - Decimal(float(arc1.radius))
        L1 = floor_grid(p1 - W_TOTAL - NOMINAL_TIGHT)
        line1 = create_line(session, padstack, SX, EX, float(L1), 'STAGE1')
        spacing = run_drc(drc, arc1, 'STAGE1', None)
        if not spacing:
            print('STAGE1: no arc-figure spacing marker - aborting', flush=True)
            return
        marker_name = spacing[0].name.lower()
        R_str = _quantity(spacing[0].expected)
        R_dec = Decimal(R_str)
        R_float = float(R_str)
        print(f'RULE: name={spacing[0].name!r} R={R_str} '
              f'on_grid={orc.on_grid(R_float)}', flush=True)
        print(f'STAGE1 clearance_full={p1 - Decimal(float(line1.start.y)) - W_TOTAL}',
              flush=True)

        # ================= STAGE 2/3: rungs ==================================
        # rung spec: (tag, y0, center-spec, placement)
        #   placement 'below': L = floor_grid(k) + 1g  -> clearance = R - (1g - phi)
        #   placement 'above': L = floor_grid(k)        -> clearance = R + phi
        #   placement 'grid' : explicit target clearance (grid-exact arcs)
        rungs = [
            dict(tag='FLIP_LO', y0=410.0, cy=cy_flip_lo, place='below',
                 window=('delta', Decimal('0.0000005'), Decimal('0.0000025'))),
            dict(tag='FLIP_HI', y0=420.0, cy=cy_flip_hi, place='above',
                 window=('margin', Decimal('0.0000001'), Decimal('0.000002'))),
            dict(tag='GOLD', y0=430.0, cy=cy_gold, place='below',
                 window=('delta', Decimal('0.000005'), Decimal('0.000049'))),
            dict(tag='ABOVE', y0=440.0, cy=cy_above, place='above',
                 window=('margin', Decimal('0.0000005'), Decimal('0.000025'))),
            dict(tag='BELOW', y0=450.0, cy=cy_below, place='below',
                 window=('delta', Decimal('0.000075'), Decimal('0.0000995'))),
        ]
        results = {}
        committed_centers = {}
        for rung in rungs:
            tag, y0 = rung['tag'], rung['y0']
            print(f'===== RUNG {tag} (y0={y0})', flush=True)
            S, E = (SX, y0), (EX, y0)
            C = (CX_NAT, rung['cy'])
            arc = create_arc(session, padstack, S, E, C, False, tag)
            if arc is None:
                results[tag] = 'CREATE_FAILED'
                continue
            cc = (float(arc.center.x), float(arc.center.y))
            rr = float(arc.radius)
            committed_centers[tag] = (cc, rr)
            k = Decimal(cc[1]) - Decimal(rr) - W_TOTAL - R_dec
            if rung['place'] == 'below':
                L = floor_grid(k) + GRID
            else:
                L = floor_grid(k)
            clearance = Decimal(cc[1]) - Decimal(rr) - L - W_TOTAL
            delta = R_dec - clearance
            kind, lo, hi = rung['window']
            check = delta if kind == 'delta' else -delta
            ok = lo <= check <= hi
            print(f'    PLANNED[{tag}]: place={rung["place"]} L={L} '
                  f'clearance={clearance} delta={delta} '
                  f'{kind}_in_window={ok}', flush=True)
            if not ok:
                print(f'    WARN[{tag}]: {kind}={check} outside ({lo},{hi}) - '
                      f'recording and continuing', flush=True)
            line = create_line(session, padstack, SX, EX, float(L), tag)
            line_yc = float(line.start.y)
            preds = oracle(cc, rr, line_yc, WIDTH, WIDTH, R_dec, R_float, tag)
            spacing = run_drc(drc, arc, tag, marker_name)
            actual = ('FLAGGED' if spacing else 'clean') if spacing is not None \
                else 'DRC_ERROR'
            actual_str = repr(spacing[0].actual) if spacing else ''
            expected_str = repr(spacing[0].expected) if spacing else ''
            display_match = (not spacing) or (
                _quantity(spacing[0].actual)
                == _quantity(disp(preds['clearance_full'])))
            results[tag] = dict(actual=actual, actual_str=actual_str,
                                expected_str=expected_str,
                                display_match=display_match, **preds)
            print(f'    RESULT[{tag}]: actual={actual} '
                  f'FULL={preds["full"]} B64={preds["b64"]} '
                  f'GRID={preds["grid"]} DROUND={preds["dround"]} '
                  f'display_match={display_match}', flush=True)

        # ---- Phase 4 analysis: committed center difference of the flip pair
        if 'FLIP_LO' in committed_centers and 'FLIP_HI' in committed_centers:
            (c_lo, r_lo) = committed_centers['FLIP_LO']
            (c_hi, r_hi) = committed_centers['FLIP_HI']
            print('===== PHASE4 PAIR ANALYSIS', flush=True)
            print(f'    dcy(committed) - 10mm = '
                  f'{Decimal(c_hi[1]) - Decimal(c_lo[1]) - Decimal(10)}',
                  flush=True)
            print(f'    dcx(committed) - 0    = '
                  f'{Decimal(c_hi[0]) - Decimal(c_lo[0])}', flush=True)
            print(f'    dr(committed)         = {Decimal(r_hi) - Decimal(r_lo)}',
                  flush=True)
            print(f'    requested dcy - 10mm  = '
                  f'{Decimal(cy_flip_hi) - Decimal(cy_flip_lo) - Decimal(10)}',
                  flush=True)

        # ---- grid-exact control rungs (equality + one-grid flip) ------------
        grid_rungs = [('GRID_EQ', 460.0, R_dec),
                      ('GRID_FLAG', 470.0, R_dec - GRID)]
        stair_rungs = [(f'STAIR_n{n}', 480.0 + 10.0 * n,
                        R_dec + (5 - n) * GRID) for n in range(11)]
        for tag, y0, target in grid_rungs + stair_rungs:
            print(f'===== RUNG {tag} (y0={y0}, target clearance={target})',
                  flush=True)
            S, E = (300.0, y0), (302.0, y0)
            C = (301.0, y0 + 0.75)
            arc = create_arc(session, padstack, S, E, C, False, tag)
            if arc is None:
                results[tag] = 'CREATE_FAILED'
                continue
            cc = (float(arc.center.x), float(arc.center.y))
            rr = float(arc.radius)
            bottom = Decimal(cc[1]) - Decimal(rr)
            L = bottom - W_TOTAL - target
            print(f'    bottom={bottom} on_grid={orc.on_grid(float(bottom))} '
                  f'L={L}', flush=True)
            line = create_line(session, padstack, 300.0, 302.0, float(L), tag)
            preds = oracle(cc, rr, float(line.start.y), WIDTH, WIDTH,
                           R_dec, R_float, tag)
            spacing = run_drc(drc, arc, tag, marker_name)
            actual = ('FLAGGED' if spacing else 'clean') if spacing is not None \
                else 'DRC_ERROR'
            actual_str = repr(spacing[0].actual) if spacing else ''
            display_match = (not spacing) or (
                _quantity(spacing[0].actual)
                == _quantity(disp(preds['clearance_full'])))
            results[tag] = dict(actual=actual, actual_str=actual_str,
                                display_match=display_match, **preds)
            print(f'    RESULT[{tag}]: actual={actual} FULL={preds["full"]} '
                  f'B64={preds["b64"]} display_match={display_match} '
                  f'actual_str={actual_str}', flush=True)

        # ================= STAGE 4: re-query bit-identity ====================
        print('===== STAGE 4: re-query', flush=True)
        requeried = [r for r in session.routes(net=NET_A, layer=LAYER)
                     if r.obj_type == 'arc']
        print(f'REQUERY_ARC_COUNT: {len(requeried)}', flush=True)
        for tag, (cc, rr) in committed_centers.items():
            match = [q for q in requeried
                     if q.center is not None
                     and orc.bits(float(q.center.x)) == orc.bits(cc[0])
                     and orc.bits(float(q.center.y)) == orc.bits(cc[1])]
            same_r = bool(match) and orc.bits(float(match[0].radius)) == orc.bits(rr)
            print(f'REQUERY {tag}: center_matches={len(match)} '
                  f'radius_identical={same_r}', flush=True)

        # ================= summary ===========================================
        print('===== SUMMARY', flush=True)
        for tag, res in results.items():
            if isinstance(res, str):
                print(f'  {tag}: {res}', flush=True)
            else:
                print(f'  {tag}: actual={res["actual"]} '
                      f'actual_str={res.get("actual_str", "")!r} '
                      f'FULL={res["full"]} B64={res["b64"]} '
                      f'GRID={res["grid"]} DROUND={res["dround"]} '
                      f'display_match={res.get("display_match")}', flush=True)
        print('TOTAL_MARKERS:', len(drc()), flush=True)
        print('DONE', flush=True)


if __name__ == '__main__':
    main()
