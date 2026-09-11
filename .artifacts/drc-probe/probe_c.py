# Phase 6/7: ARC-ARC and ARC-Via generalization probe.  Disposable board
# copy, owned Allegro process, unique port.  No production code modified.
#
# Context (Probe A + Probe B, completed):
#   - Model A CONFIRMED for Line-ARC: full-precision measurement on committed
#     binary64 arc geometry (center stored bit-exact on bisector, r derived
#     with <=1.5e-14 noise), strict `measured < rule` comparison, on-grid
#     quantities exact (DBU-like), marker display TRUNCATES toward zero at
#     accuracy digits (FLIP_LO 0.0599975 -> '0.0599').
#   - Models B (quantize geometry first) and C (round distance first) are
#     EXCLUDED by Probe B FLIP_LO/GOLD, so the original B-vs-C discrimination
#     purpose of this probe is MOOT.  Phase 6 now verifies that model A
#     generalizes to a pair where BOTH objects are non-grid arcs (kills the
#     residual "only the line/DBU side does the work" reading); Phase 7
#     extends to ARC-Via (radial distance; pad radius rp learned in-run since
#     padstack geometry is not exposed by the client API).
#
# Phase 6 geometry (per rung, cell y0):
#   upper arc NET_A: S=(300,y0) E=(302.0001,y0) C=(301.00005, y0+0.124975+eps)
#                    cw=False -> bottom arc; bottom p1 = cy1 - r1 in span.
#   lower arc NET_B: S=(300,y1) E=(302.0001,y1) C=(301.00005, y1-0.124975)
#                    cw=True  -> TOP arc (center below chord; math-CW from
#                    theta_S~172.9deg decreasing through 90deg to ~7.1deg);
#                    top t2 = cy2 + r2 in span.
#   Both extrema at x=301.00005; centers share cx -> circle-center distance
#   is vertical: min curve distance = (cy1-cy2) - r1 - r2 = p1 - t2.
#   clearance = p1 - t2 - w_total(0.15).  y1 = y0 - DELTA (DELTA on-grid,
#   computed at runtime from learned R); eps along the bit-preserved bisector
#   is the fine knob, slope d(clear)/d(eps) = 1 - (cy-y0)/r ~ 0.876.
#   CC_FLIP_HI = CC_FLIP_LO cell +10mm with eps_hi = eps_lo + 3.5e-6
#   (mirrors Probe B PHASE4 pair: committed dcy1-10 must record ~3.5e-6).
#
# Phase 7 geometry:
#   cal arc y0=500 natural center, cw=False, NET_A (anchor via at S).
#   Via ladder NET_B at x=301.0 (on-grid), yv descending below p1; radial
#   clear_j = d_j - r1 - rp - w/2, d_j = hypot(cx1-301.0, cy1-yv_j).
#   Pass 1 (0.1 step, 13 vias) -> flip bracket j* by verdicts only (display
#   semantics for negatives unknown, verdicts robust).  Pass 2 (0.007 step,
#   14 vias inside bracket) -> guaranteed several markers with clear in
#   (0, R_via): positive actuals are unambiguous under BOTH floor and
#   truncate display -> rp pinned to a 1e-4-wide half-open interval -> unique
#   on-grid candidate.  Then critical rungs CV_FLIP_LO y0=540 / CV_FLIP_HI
#   y0=550 with the same eps knob; via y chosen on-grid AFTER arc commit from
#   committed values (radial correction ~8e-10 included exactly), adjusted by
#   +-1e-4 steps until the window assert passes (warn-don't-crash).
#   Via committed positions read back bit-level via session.vias(net=NET_B).
#   Region note: diag_y700.py proved via creation FAILS for y>=700 across
#   x=292..308 on an otherwise EMPTY region (extent boundary ->
#   VIA_CREATE_FAILED, not a DRC); y<=698 and 480..560 OK.  Phase 7 relocated
#   from y=700/720/730 to 500/540/550 accordingly (>=37mm clear of Phase 6).
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import math
import sys
from collections import Counter
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

import arc_oracle as orc
from scan_window import CX_NAT, CY_OFF, EX, SX
from allegrobridge import Allegro
from allegrobridge.client.api.geometry import ArcTo
from allegrobridge.util import ASSETS_DIR

NET_A = 'NFC_SWP'
NET_B = 'FINGER_SPI_MISO'
LAYER = 'ETCH/TOP'
WIDTH = 0.15
W_TOTAL = Decimal('0.15')          # (0.15+0.15)/2 exact
W_HALF = Decimal('0.075')          # arc half-width for ARC-Via
GRID = Decimal('0.0001')
CY_OFF_DEC = Decimal('0.124975')
DX_NAT = Decimal(CX_NAT) - Decimal(SX)     # exact 1.00005... expansion
R_NAT_F = math.hypot(CX_NAT - SX, CY_OFF)  # ~1.0078287320398126
NOMINAL_TIGHT = Decimal('0.01')            # stage-1 rule learning, like Probe B
XV = 301.0                                 # via column (on-grid)
ARCS_CREATED: list = []                    # (tag, committed row) of every probe arc


def floor_grid(x: Decimal) -> Decimal:
    return x.quantize(GRID, rounding=ROUND_FLOOR)


def trunc_disp(dec: Decimal) -> str:
    """Probe B display model: truncate toward zero at 4 decimals, strip
    trailing zeros, ' MM' suffix.  (FLIP_LO 0.0599975 -> '0.0599 MM'.)"""
    q = dec.quantize(GRID, rounding=ROUND_FLOOR).normalize()
    return f'{q} MM'


def _f(value) -> str:
    if value is None:
        return 'None'
    v = float(value)
    return f'{v!r} bits={orc.bits(v)} on_grid={orc.on_grid(v)}'


def _quantity(text: str) -> str:
    return text.split()[0]


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

def top_in_span(S, E, C) -> bool:
    """True if 90deg (top of circle, y-up) lies inside the math-CW sweep."""
    th_s = orc.angle_deg(C, S)
    sw = orc.sweep_deg(S, E, C, True)
    return ((th_s - 90.0) % 360.0) <= sw + 1e-9


def pair_clear_exact(cy1, r1, cy2, r2) -> Decimal:
    """FULL model clearance for the vertical ARC-ARC pair (Decimal-60 on the
    exact binary64 expansions of the committed doubles)."""
    return (Decimal(cy1) - Decimal(r1)) - (Decimal(cy2) + Decimal(r2)) - W_TOTAL


def pair_clear_float(cy1, r1, cy2, r2) -> float:
    return (cy1 - r1) - (cy2 + r2) - 0.15


def cv_clear_exact(cx1, cy1, r1, xv, yv, rp: Decimal) -> Decimal:
    dx = Decimal(cx1) - Decimal(xv)
    dy = Decimal(cy1) - Decimal(yv)
    d = (dx * dx + dy * dy).sqrt()
    return d - Decimal(r1) - rp - W_HALF


def cv_clear_float(cx1, cy1, r1, xv, yv, rp: float) -> float:
    return math.hypot(cx1 - xv, cy1 - yv) - r1 - rp - 0.075


# --------------------------------------------------------------------------
# eps scans (offline exact math on the doubles that would go over the wire)
# --------------------------------------------------------------------------

def find_eps_pair(y0: float, y1_f: float, cy2_f: float, r2_f: float,
                  R_dec: Decimal, kind: str, lo: Decimal, hi: Decimal):
    """Scan eps in [-1.5e-4, +1.5e-4] step 1e-8 for the upper-arc center
    cy1=(y0+CY_OFF)+eps so that delta=R-clear (kind='delta') or
    margin=clear-R (kind='margin') lands in [lo,hi].  Float prefilter with
    1e-9 slack, then exact Decimal verify.  Returns (cy1, val) or None."""
    base = y0 + CY_OFF
    R_f = float(R_dec)
    lo_f, hi_f = float(lo), float(hi)
    n = 0
    while n <= 30000:
        eps = -1.5e-4 + n * 1e-8
        cy1 = base + eps
        r1_f = math.hypot(CX_NAT - SX, cy1 - y0)
        clear_f = pair_clear_float(cy1, r1_f, cy2_f, r2_f)
        val_f = R_f - clear_f if kind == 'delta' else clear_f - R_f
        if lo_f - 1e-9 <= val_f <= hi_f + 1e-9:
            clear = pair_clear_exact(cy1, r1_f, cy2_f, r2_f)
            val = R_dec - clear if kind == 'delta' else clear - R_dec
            if lo <= val <= hi:
                return cy1, val
        n += 1
    return None


def find_eps_cv(y0: float, yv_dec_fn, rp: Decimal, R_dec: Decimal,
                kind: str, lo: Decimal, hi: Decimal):
    """Same knob for ARC-Via.  yv_dec_fn(cy1: float) -> Decimal via y for the
    placement (below-R: floor_grid(k)+GRID; above-R: floor_grid(k)), where
    k = cy1 - r1 - W_HALF - rp - R.  Scan eps; exact verify includes the
    radial sqrt.  Returns (cy1, yv_dec, val) or None."""
    base = y0 + CY_OFF
    R_f = float(R_dec)
    rp_f = float(rp)
    lo_f, hi_f = float(lo), float(hi)
    n = 0
    while n <= 30000:
        eps = -1.5e-4 + n * 1e-8
        cy1 = base + eps
        r1_f = math.hypot(CX_NAT - SX, cy1 - y0)
        yv_dec = yv_dec_fn(cy1, r1_f)
        yv_f = float(yv_dec)
        val_f = (R_f - cv_clear_float(CX_NAT, cy1, r1_f, XV, yv_f, rp_f)
                 if kind == 'delta'
                 else cv_clear_float(CX_NAT, cy1, r1_f, XV, yv_f, rp_f) - R_f)
        if lo_f - 2e-8 <= val_f <= hi_f + 2e-8:
            clear = cv_clear_exact(CX_NAT, cy1, r1_f, XV, yv_f, rp)
            val = R_dec - clear if kind == 'delta' else clear - R_dec
            if lo <= val <= hi:
                return cy1, yv_dec, val
        n += 1
    return None


# --------------------------------------------------------------------------
# Allegro object creation with requested/committed bit records
# --------------------------------------------------------------------------

def create_arc_net(session, padstack: str, net: str, S, E, C, cw: bool,
                   tag: str):
    print(f'CREATE_ARC {tag} net={net} cw={cw!r}', flush=True)
    print(f'   requested S=({_f(S[0])} | {_f(S[1])})', flush=True)
    print(f'   requested E=({_f(E[0])} | {_f(E[1])})', flush=True)
    print(f'   requested C=({_f(C[0])} | {_f(C[1])})', flush=True)
    session.vias.create(padstack, at=(S[0], S[1]), net=net)
    rows = session.routes.create(
        net, [S, ArcTo(end=E, center=C, clockwise=cw)], LAYER, WIDTH)
    arcs = [r for r in rows if r.obj_type == 'arc']
    if not arcs:
        print(f'   {tag}: NO ARC ROW CREATED rows={len(rows)}', flush=True)
        return None
    row = arcs[0]
    cx_c, cy_c = float(row.center.x), float(row.center.y)
    r_c = float(row.radius)
    print(f'   committed C=({_f(row.center.x)} | {_f(row.center.y)})', flush=True)
    print(f'   committed r={_f(row.radius)} length={_f(row.length)} '
          f'is_clockwise={row.is_clockwise!r}', flush=True)
    bit_c = (orc.bits(cx_c) == orc.bits(C[0]) and orc.bits(cy_c) == orc.bits(C[1]))
    print(f'   center_bit_preserved={bit_c} '
          f'dcy={Decimal(cy_c) - Decimal(C[1])} '
          f'dcx={Decimal(cx_c) - Decimal(C[0])}', flush=True)
    dS = ((Decimal(cx_c) - Decimal(S[0])) ** 2
          + (Decimal(cy_c) - Decimal(S[1])) ** 2).sqrt()
    print(f'   r_committed - |S-C|_exact = {Decimal(r_c) - dS}', flush=True)
    if cw:
        print(f'   top_in_span(math_cw)={top_in_span(S, E, (cx_c, cy_c))}',
              flush=True)
    else:
        print(f'   bottom_in_span(math_ccw)='
              f'{orc.bottom_in_span(S, E, (cx_c, cy_c), False)}', flush=True)
    ARCS_CREATED.append((tag, row))
    return row


def create_line(session, padstack: str, y: float, tag: str):
    """Stage-1 tight line (NET_B), like Probe B.  Records requested AND
    committed y (endpoints quantize to grid at commit)."""
    print(f'CREATE_LINE {tag} requested y={_f(y)}', flush=True)
    S = (SX - 1.0, y)
    E = (EX + 1.0, y)
    session.vias.create(padstack, at=S, net=NET_B)
    session.vias.create(padstack, at=E, net=NET_B)
    session.routes.create(NET_B, [S, E], LAYER, WIDTH)
    rows = [r for r in session.routes(net=NET_B, layer=LAYER)
            if r.obj_type == 'line' and abs(float(r.start.y) - y) < 0.5]
    if rows:
        print(f'   committed y={_f(rows[-1].start.y)}', flush=True)
    return rows[-1] if rows else None


def readback_vias(session, wanted: list, tag: str) -> dict:
    """Read committed via positions; match by proximity.  wanted is a list of
    (key, x, y).  Returns {key: (xc, yc)} committed floats.  Records
    requested vs committed (via DBU-quantization evidence)."""
    all_vias = session.vias(net=NET_B)
    out = {}
    for key, x, y in wanted:
        best, bd = None, 1e-3
        for v in all_vias:
            p = v.location if hasattr(v, 'location') else v.start
            d = abs(float(p.x) - x) + abs(float(p.y) - y)
            if d < bd:
                best, bd = p, d
        if best is None:
            print(f'VIA_READBACK {tag} {key}: NOT FOUND req=({x!r},{y!r})',
                  flush=True)
            out[key] = (x, y)
            continue
        xc, yc = float(best.x), float(best.y)
        print(f'VIA_READBACK {tag} {key}: req=({x!r},{y!r}) '
              f'committed=({xc!r},{yc!r}) bits=({orc.bits(xc)},{orc.bits(yc)}) '
              f'dx={Decimal(xc) - Decimal(x)} dy={Decimal(yc) - Decimal(y)} '
              f'on_grid=({orc.on_grid(xc)},{orc.on_grid(yc)})', flush=True)
        out[key] = (xc, yc)
    return out


# --------------------------------------------------------------------------
# oracles: 4 models per case (never confuse measurement vs comparison)
# --------------------------------------------------------------------------

def oracle_pair(tag: str, cy1, r1, cy2, r2, R_dec: Decimal):
    full = pair_clear_exact(cy1, r1, cy2, r2)
    b64 = pair_clear_float(cy1, r1, cy2, r2)
    q = orc.quant4   # returns float -> wrap in Decimal for exact grid algebra
    grid = ((Decimal(q(cy1)) - Decimal(q(r1)))
            - (Decimal(q(cy2)) + Decimal(q(r2))) - W_TOTAL)
    dround = full.quantize(GRID, rounding=orc.ROUND_HALF_EVEN)
    R_f = float(R_dec)
    print(f'ORACLE {tag} (ARC-ARC, committed values):', flush=True)
    print(f'   FULL      clear={full} verdict={orc.verdict(full, R_dec)}',
          flush=True)
    print(f'   BINARY64  clear={b64!r} verdict={orc.verdict(Decimal(b64), R_dec)}'
          f' (naive float<{R_f}: {b64 < R_f})', flush=True)
    print(f'   GRID      clear={grid} verdict={orc.verdict(grid, R_dec)}',
          flush=True)
    print(f'   DROUND    round4(FULL)={dround} '
          f'verdict={orc.verdict(dround, R_dec)}', flush=True)
    print(f'   DISPLAY_PREDICTED(trunc4)={trunc_disp(full)!r}', flush=True)
    return full


def oracle_cv(tag: str, cx1, cy1, r1, xv, yv, rp: Decimal, R_dec: Decimal):
    full = cv_clear_exact(cx1, cy1, r1, xv, yv, rp)
    b64 = cv_clear_float(cx1, cy1, r1, xv, yv, float(rp))
    q = orc.quant4   # returns float -> wrap in Decimal for exact grid algebra
    dxg = Decimal(q(cx1)) - Decimal(q(xv))
    dyg = Decimal(q(cy1)) - Decimal(q(yv))
    dg = (dxg * dxg + dyg * dyg).sqrt()
    grid = dg - Decimal(q(r1)) - rp - W_HALF
    dround = full.quantize(GRID, rounding=orc.ROUND_HALF_EVEN)
    print(f'ORACLE {tag} (ARC-Via, committed values, rp={rp}):', flush=True)
    print(f'   FULL      clear={full} verdict={orc.verdict(full, R_dec)}',
          flush=True)
    print(f'   BINARY64  clear={b64!r} verdict={orc.verdict(Decimal(b64), R_dec)}'
          f' (naive float<{float(R_dec)}: {b64 < float(R_dec)})', flush=True)
    print(f'   GRID      clear={grid} verdict={orc.verdict(grid, R_dec)}',
          flush=True)
    print(f'   DROUND    round4(FULL)={dround} '
          f'verdict={orc.verdict(dround, R_dec)}', flush=True)
    print(f'   DISPLAY_PREDICTED(trunc4)={trunc_disp(full)!r}', flush=True)
    return full


# --------------------------------------------------------------------------
# DRC check with verdict/actual/figure recording (Probe B pattern)
# --------------------------------------------------------------------------

def _fig_dicts(m) -> list:
    figs = []
    for f in (m.figures or []):
        figs.append(dict(
            obj_type=f.obj_type, layer=f.layer,
            net=(f.net.name if f.net is not None else None),
            start=(float(f.start.x), float(f.start.y)) if f.start else None,
            end=(float(f.end.x), float(f.end.y)) if f.end else None,
            center=(float(f.center.x), float(f.center.y)) if f.center else None,
            radius=float(f.radius) if f.radius is not None else None,
            width=f.width,
            location=(float(f.location.x), float(f.location.y))
            if getattr(f, 'location', None) else None))
    return figs


def _partner_match(figs, partner) -> bool:
    """True if one of the marker's figures matches the partner spec.
    ('via',)                  -> any via figure
    ('arc', net, (px, py))    -> arc figure, that net, start within 1e-9;
                                 if the figure exposes no start point, the
                                 net+type match alone is accepted (recorded)."""
    if partner is None:
        return True
    kind = partner[0]
    for f in figs:
        if kind == 'via' and f['obj_type'] == 'via':
            return True
        if kind == 'arc' and f['obj_type'] == 'arc' and f['net'] == partner[1]:
            st = f['start']
            if st is None:
                return True
            px, py = partner[2]
            if abs(st[0] - px) < 1e-9 and abs(st[1] - py) < 1e-9:
                return True
    return False


def run_drc(drc, row, tag: str, marker_name: str | None, partner=None):
    """drc.check(row) is immediate.  marker_name None -> discovery: returns
    list of (name, expected, actual, figs) for ALL *spacing* markers.
    Otherwise returns the same tuples for markers whose name matches
    (case-insensitive) AND whose figures contain `partner`; same-name markers
    without the partner are printed as SAME_NAME_OTHER and EXCLUDED (they
    belong to other object pairs).  Returns None on check failure."""
    try:
        markers = drc.check(row)
    except Exception as exc:
        print(f'DRC {tag}: CHECK_FAILED {exc!r}', flush=True)
        return None
    hits = []
    for m in markers:
        name = m.name or ''
        figs = _fig_dicts(m)
        if marker_name is None:
            if name.lower().endswith('spacing'):
                print(f'DRC {tag}: MARKER name={name!r} expected={m.expected!r} '
                      f'actual={m.actual!r} layer={m.layer!r}', flush=True)
                for i, f in enumerate(figs):
                    print(f'   FIG[{i}] {f}', flush=True)
                hits.append((name, m.expected, m.actual, figs))
            else:
                print(f'DRC {tag}: OTHER name={name!r} expected={m.expected!r} '
                      f'actual={m.actual!r}', flush=True)
            continue
        if name.lower() != marker_name.lower():
            print(f'DRC {tag}: OTHER name={name!r} expected={m.expected!r} '
                  f'actual={m.actual!r}', flush=True)
            continue
        if not _partner_match(figs, partner):
            print(f'DRC {tag}: SAME_NAME_OTHER name={name!r} '
                  f'expected={m.expected!r} actual={m.actual!r} '
                  f'(partner {partner} absent from figures - EXCLUDED)',
                  flush=True)
            continue
        print(f'DRC {tag}: MARKER name={name!r} expected={m.expected!r} '
              f'actual={m.actual!r} layer={m.layer!r}', flush=True)
        for i, f in enumerate(figs):
            print(f'   FIG[{i}] {f}', flush=True)
        hits.append((name, m.expected, m.actual, figs))
    if marker_name is not None:
        verdict = 'FLAGGED' if hits else 'clean'
        print(f'DRC {tag}: VERDICT={verdict} hits={len(hits)}', flush=True)
    return hits


# --------------------------------------------------------------------------
# Phase 6 rung execution
# --------------------------------------------------------------------------

def run_cc_rung(session, drc, padstack, spec, R_dec, marker_name, delta_dec):
    tag = spec['tag']
    y0 = float(spec['y0'])
    y1_dec = Decimal(int(spec['y0'])) - delta_dec
    y1_f = float(y1_dec)
    cy2_f = float(y1_dec - CY_OFF_DEC)
    r2_f = math.hypot(CX_NAT - SX, cy2_f - y1_f)
    print(f'=== {tag} y0={y0!r} DELTA={delta_dec} y1={y1_f!r} '
          f'(on_grid={orc.on_grid(y1_f)})', flush=True)

    if 'cy1' in spec:                      # FLIP_HI: constructed from LO
        cy1 = spec['cy1']
        val = spec['val']
    else:
        found = find_eps_pair(y0, y1_f, cy2_f, r2_f, R_dec,
                              spec['kind'], spec['lo'], spec['hi'])
        if found is None:
            print(f'{tag}: EPS_SCAN_FAILED window={spec["kind"]}'
                  f'[{spec["lo"]},{spec["hi"]}] - rung SKIPPED', flush=True)
            return None
        cy1, val = found
    print(f'   PLANNED cy1={cy1!r} bits={orc.bits(cy1)} eps={Decimal(cy1) - Decimal(y0) - CY_OFF_DEC} '
          f'predicted {spec["kind"]}={val}', flush=True)

    upper = create_arc_net(session, padstack, NET_A, (SX, y0), (EX, y0),
                           (CX_NAT, cy1), False, tag + '_UPPER')
    lower = create_arc_net(session, padstack, NET_B, (SX, y1_f), (EX, y1_f),
                           (CX_NAT, cy2_f), True, tag + '_LOWER')
    if upper is None or lower is None:
        return None

    # recompute from COMMITTED geometry (requested/committed strictly separate)
    cy1c, r1c = float(upper.center.y), float(upper.radius)
    cy2c, r2c = float(lower.center.y), float(lower.radius)
    clear_c = pair_clear_exact(cy1c, r1c, cy2c, r2c)
    val_c = R_dec - clear_c if spec['kind'] == 'delta' else clear_c - R_dec
    in_window = spec['lo'] <= val_c <= spec['hi']
    print(f'   COMMITTED clear={clear_c} {spec["kind"]}={val_c} '
          f'in_window={in_window}', flush=True)
    if not in_window:
        print(f'   {tag}: WINDOW_ASSERT_FAILED (recorded, continuing)',
              flush=True)

    full = oracle_pair(tag, cy1c, r1c, cy2c, r2c, R_dec)
    hits = run_drc(drc, upper, tag, marker_name,
                   partner=('arc', NET_B, (SX, y1_f)))
    verdict = 'FLAGGED' if hits else ('clean' if hits is not None else 'ERROR')
    actual = hits[0][2] if hits else None
    display_match = (actual == trunc_disp(full)) if actual is not None else None
    print(f'RESULT {tag}: verdict={verdict} expected={hits[0][1] if hits else None!r} '
          f'actual={actual!r} display_match={display_match}', flush=True)
    return dict(tag=tag, y0=y0, cy1_req=cy1, cy2_req=cy2_f,
                cy1c=cy1c, r1c=r1c, cy2c=cy2c, r2c=r2c,
                upper=upper, lower=lower,
                clear_committed=clear_c, val=val_c, in_window=in_window,
                verdict=verdict, actual=actual,
                figures=[h[3] for h in hits] if hits else [])


def run_cc_grid_pair(session, drc, padstack, tag, y0, y1_dec, R_dec,
                     marker_name, expect_verdict):
    """On-grid ARC-ARC controls: r=1.25 exact, extrema at whole-grid y.
    clear = (y0-0.5) - (y1+0.5) - 0.15 = y0 - y1 - 1.15."""
    y1_f = float(y1_dec)
    print(f'=== {tag} (grid pair) y0={y0} y1={y1_f!r} '
          f'(on_grid={orc.on_grid(y1_f)})', flush=True)
    upper = create_arc_net(session, padstack, NET_A, (SX, float(y0)), (302.0, float(y0)),
                           (301.0, float(y0) + 0.75), False, tag + '_UPPER')
    lower = create_arc_net(session, padstack, NET_B, (SX, y1_f), (302.0, y1_f),
                           (301.0, y1_f - 0.75), True, tag + '_LOWER')
    if upper is None or lower is None:
        return None
    cy1c, r1c = float(upper.center.y), float(upper.radius)
    cy2c, r2c = float(lower.center.y), float(lower.radius)
    clear_c = pair_clear_exact(cy1c, r1c, cy2c, r2c)
    print(f'   COMMITTED clear={clear_c} (R-clear={R_dec - clear_c})', flush=True)
    full = oracle_pair(tag, cy1c, r1c, cy2c, r2c, R_dec)
    hits = run_drc(drc, upper, tag, marker_name,
                   partner=('arc', NET_B, (SX, y1_f)))
    verdict = 'FLAGGED' if hits else ('clean' if hits is not None else 'ERROR')
    actual = hits[0][2] if hits else None
    match_expect = (verdict == expect_verdict)
    print(f'RESULT {tag}: verdict={verdict} expected_verdict={expect_verdict} '
          f'match={match_expect} actual={actual!r} '
          f'display_pred={trunc_disp(full)!r}', flush=True)
    return dict(tag=tag, verdict=verdict, actual=actual, clear=clear_c,
                upper=upper, in_window=match_expect)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> None:
    selftest = '--selftest' in sys.argv

    # ---- offline self-test: verify all eps windows are reachable with the
    # ---- Probe-B-calibrated R=0.06 / assumed R_via=0.065, rp=0.5 (no Allegro)
    if selftest:
        R = Decimal('0.06')
        delta = floor_grid(R + 2 * Decimal(R_NAT_F) + W_TOTAL - 2 * CY_OFF_DEC)
        print(f'SELFTEST DELTA={delta}', flush=True)
        rungs = [('CC_FLIP_LO', 600, 'delta', Decimal('1.5e-6'), Decimal('2.5e-6')),
                 ('CC_GOLD', 620, 'delta', Decimal('5e-6'), Decimal('4.9e-5')),
                 ('CC_ABOVE', 630, 'margin', Decimal('5e-7'), Decimal('2.5e-5')),
                 ('CC_BELOW', 640, 'delta', Decimal('7.5e-5'), Decimal('9.95e-5'))]
        for tag, y0, kind, lo, hi in rungs:
            y1_dec = Decimal(y0) - delta
            y1_f = float(y1_dec)
            cy2_f = float(y1_dec - CY_OFF_DEC)
            r2_f = math.hypot(CX_NAT - SX, cy2_f - y1_f)
            got = find_eps_pair(float(y0), y1_f, cy2_f, r2_f, R, kind, lo, hi)
            print(f'SELFTEST {tag}: {"FOUND cy1=%r val=%s" % got if got else "NOT FOUND"}',
                  flush=True)
        # FLIP_HI from LO
        y1_dec = Decimal(600) - delta
        got = find_eps_pair(600.0, float(y1_dec), float(y1_dec - CY_OFF_DEC),
                            math.hypot(CX_NAT - SX, float(y1_dec - CY_OFF_DEC) - float(y1_dec)),
                            R, 'delta', Decimal('1.5e-6'), Decimal('2.5e-6'))
        if got:
            cy1_hi = float(Decimal(got[0]) + Decimal(10) + Decimal('0.0000035'))
            y1_dec_hi = Decimal(610) - delta
            cy2_hi = float(y1_dec_hi - CY_OFF_DEC)
            r2_hi = math.hypot(CX_NAT - SX, cy2_hi - float(y1_dec_hi))
            r1_hi = math.hypot(CX_NAT - SX, cy1_hi - 610.0)
            m = pair_clear_exact(cy1_hi, r1_hi, cy2_hi, r2_hi) - R
            print(f'SELFTEST CC_FLIP_HI: cy1={cy1_hi!r} margin={m}', flush=True)
        # CV scan self-test with assumed rp/R_via
        rp, Rv = Decimal('0.5'), Decimal('0.065')

        def below(cy1, r1f):
            k = Decimal(cy1) - Decimal(r1f) - W_HALF - rp - Rv
            return floor_grid(k) + GRID

        got = find_eps_cv(540.0, below, rp, Rv, 'delta',
                          Decimal('1.5e-6'), Decimal('2.5e-6'))
        print(f'SELFTEST CV_FLIP_LO: '
              f'{"FOUND cy1=%r yv=%s val=%s" % got if got else "NOT FOUND"}',
              flush=True)
        print('SELFTEST DONE', flush=True)
        return

    work = Path(mkdtemp(prefix='drc-probe-arc-'))
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    with socket() as listener:
        listener.bind(('localhost', 0))
        port = str(listener.getsockname()[1])

    with Allegro.open(mode='cli', board=board, workspace_id=port,
                      timeout=300.0) as allegro:
        session = allegro.session
        drc = session.drc
        existing = session.vias()
        padstack = Counter(v.padstack for v in existing).most_common(1)[0][0]
        print('PADSTACK:', padstack, flush=True)

        # ---- STAGE 1: learn the arc-line spacing rule R in THIS session ----
        print('STAGE1: rule learning (natural arc y0=390 + tight line)',
              flush=True)
        cy_nat = 390.0 + CY_OFF
        s1_arc = create_arc_net(session, padstack, NET_A, (SX, 390.0),
                                (EX, 390.0), (CX_NAT, cy_nat), False,
                                'STAGE1_ARC')
        if s1_arc is None or s1_arc.center is None:
            print('STAGE1: ARC CREATION FAILED - ABORT', flush=True)
            return
        cy1c = float(s1_arc.center.y)
        r1c = float(s1_arc.radius)
        p1 = Decimal(cy1c) - Decimal(r1c)
        L_dec = floor_grid(p1 - W_TOTAL - NOMINAL_TIGHT)
        create_line(session, padstack, float(L_dec), 'STAGE1_LINE')
        found = run_drc(drc, s1_arc, 'STAGE1', None)
        if not found:
            print('STAGE1: NO SPACING MARKER - cannot learn R; ABORT',
                  flush=True)
            return
        if len(found) > 1:
            pref = [t for t in found
                    if t[0].lower() == 'line to line spacing']
            if pref:
                print(f'STAGE1: {len(found)} spacing markers; preferring '
                      f'Line to Line Spacing', flush=True)
                found = pref
        marker_name, expected, actual, _ = found[0]
        R_dec = Decimal(_quantity(expected))
        print(f'STAGE1: marker_name={marker_name!r} R={R_dec} '
              f'(actual={actual!r}) on_grid={orc.on_grid(float(R_dec))}',
              flush=True)

        # ---- PHASE 6: ARC-ARC critical rungs -------------------------------
        delta_dec = floor_grid(R_dec + 2 * Decimal(R_NAT_F) + W_TOTAL
                               - 2 * CY_OFF_DEC)
        print(f'PHASE6: DELTA={delta_dec} (clear(eps=0) ~ R - residual)',
              flush=True)
        results = []
        spec_lo = dict(tag='CC_FLIP_LO', y0=600, kind='delta',
                       lo=Decimal('1.5e-6'), hi=Decimal('2.5e-6'))
        res_lo = run_cc_rung(session, drc, padstack, spec_lo, R_dec,
                             marker_name, delta_dec)
        results.append(res_lo)
        if res_lo is not None:
            cy1_hi = float(Decimal(res_lo['cy1c']) + Decimal(10)
                           + Decimal('0.0000035'))
            spec_hi = dict(tag='CC_FLIP_HI', y0=610, kind='margin',
                           lo=Decimal('1e-7'), hi=Decimal('2e-6'),
                           cy1=cy1_hi, val=None)
            results.append(run_cc_rung(session, drc, padstack, spec_hi, R_dec,
                                       marker_name, delta_dec))
        for spec in (dict(tag='CC_GOLD', y0=620, kind='delta',
                          lo=Decimal('5e-6'), hi=Decimal('4.9e-5')),
                     dict(tag='CC_ABOVE', y0=630, kind='margin',
                          lo=Decimal('5e-7'), hi=Decimal('2.5e-5')),
                     dict(tag='CC_BELOW', y0=640, kind='delta',
                          lo=Decimal('7.5e-5'), hi=Decimal('9.95e-5'))):
            results.append(run_cc_rung(session, drc, padstack, spec, R_dec,
                                       marker_name, delta_dec))

        # PHASE4-style pair analysis on committed values
        lo = next((r for r in results if r and r['tag'] == 'CC_FLIP_LO'), None)
        hi = next((r for r in results if r and r['tag'] == 'CC_FLIP_HI'), None)
        if lo and hi:
            dcy1 = Decimal(hi['cy1c']) - Decimal(lo['cy1c']) - Decimal(10)
            dcy2 = Decimal(hi['cy2c']) - Decimal(lo['cy2c']) - Decimal(10)
            dr1 = Decimal(hi['r1c']) - Decimal(lo['r1c'])
            dr2 = Decimal(hi['r2c']) - Decimal(lo['r2c'])
            print(f'PHASE6_PAIR: dcy1(committed)-10={dcy1} dcy2-10={dcy2} '
                  f'dr1={dr1} dr2={dr2}', flush=True)
            print(f'PHASE6_PAIR: verdicts LO={lo["verdict"]} HI={hi["verdict"]} '
                  f'(designed: FLAGGED/clean)', flush=True)

        # grid-pair controls, y1 derived from learned R (never hardcode 0.06)
        y1_eq = Decimal(660) - Decimal('1.15') - R_dec
        results.append(run_cc_grid_pair(session, drc, padstack, 'CC_GRID_EQ',
                                        660.0, y1_eq, R_dec, marker_name,
                                        'clean'))
        results.append(run_cc_grid_pair(session, drc, padstack, 'CC_GRID_FLAG',
                                        680.0,
                                        Decimal(680) - Decimal('1.15') - R_dec + GRID,
                                        R_dec, marker_name, 'FLAGGED'))

        # ---- PHASE 7: ARC-Via ----------------------------------------------
        print('PHASE7: ARC-Via (rp learned in-run from marker actuals)',
              flush=True)
        cv_res: dict = {}     # hoisted: SUMMARY reports it even on skip paths
        cal = create_arc_net(session, padstack, NET_A, (SX, 500.0),
                             (EX, 500.0), (CX_NAT, 500.0 + CY_OFF), False,
                             'CV_CAL_ARC')
        cx1c = float(cal.center.x)
        cy1_cal = float(cal.center.y)
        r1_cal = float(cal.radius)
        p1_cal = Decimal(cy1_cal) - Decimal(r1_cal)

        # pass 1: 0.1-step ladder, offsets 0.05..1.25 below p1
        wanted = []
        for j in range(13):
            yv_dec = floor_grid(p1_cal - W_HALF - Decimal('0.05')) - Decimal(j) / Decimal(10)
            yv = float(yv_dec)
            session.vias.create(padstack, at=(XV, yv), net=NET_B)
            wanted.append((f'p1_j{j}', XV, yv))
        via_com = readback_vias(session, wanted, 'CV_PASS1')
        run_drc(drc, cal, 'CV_PASS1', None)   # discovery: learn via marker name + R_via

        # identify via-spacing markers from the global check on cal arc
        try:
            markers = drc.check(cal)
        except Exception as exc:
            print(f'CV: recheck failed {exc!r}', flush=True)
            markers = []
        via_name, R_via = None, None
        via_markers = []
        for m in markers:
            name = (m.name or '')
            if 'via' in name.lower() and name.lower().endswith('spacing'):
                via_name = name
                R_via = Decimal(_quantity(m.expected))
                via_markers.append(m)
        if via_name is None:
            print('CV: NO ARC-VIA SPACING MARKERS - Phase 7 critical rungs '
                  'SKIPPED (recorded)', flush=True)
        else:
            print(f'CV: via_marker={via_name!r} R_via={R_via} '
                  f'flagged_count={len(via_markers)}', flush=True)
            # attribution by figure location (fallback: flagged set is the
            # prefix of vias sorted by yv DESCENDING - clear strictly
            # increases as yv decreases)
            yv_sorted = sorted(((k, v[1]) for k, v in via_com.items()),
                               key=lambda t: -t[1])
            flagged_keys = set()
            attrib_failed = 0
            for m in via_markers:
                locs = [f.location for f in (m.figures or [])
                        if f.obj_type == 'via' and getattr(f, 'location', None)]
                if locs:
                    key = min(yv_sorted,
                              key=lambda t: abs(t[1] - float(locs[0].y)))[0]
                    flagged_keys.add(key)
                else:
                    attrib_failed += 1
            if attrib_failed:
                print(f'CV: attribution missing for {attrib_failed} markers; '
                      f'using monotone prefix fallback', flush=True)
                flagged_keys = {k for k, _ in yv_sorted[:len(via_markers)]}
            print(f'CV_PASS1 flagged: {sorted(flagged_keys)}', flush=True)
            jstar = max((int(k.split("j")[1]) for k in flagged_keys),
                        default=-1)
            # bracket guard: clamp so p1_j{jstar} and p1_j{jstar+1} exist.
            # A degenerate ladder (all flagged / all clean) then yields an
            # empty or ambiguous rp interval -> the unique-candidate check
            # below skips the critical rungs (recorded, no crash).
            jstar = min(max(jstar, 0), 11)
            # pass 2: 0.007-step refinement between yv_{j*+1} and yv_{j*}
            yv_hi = via_com[f'p1_j{jstar}'][1]      # flagged (closer)
            yv_lo = via_com[f'p1_j{jstar + 1}'][1]  # clean (farther)
            wanted2 = []
            for mstep in range(1, 15):
                yv_dec = Decimal(yv_lo) + Decimal(mstep) * Decimal('0.007')
                yv_dec = floor_grid(yv_dec)
                yv = float(yv_dec)
                session.vias.create(padstack, at=(XV, yv), net=NET_B)
                wanted2.append((f'p2_m{mstep}', XV, yv))
            via_com2 = readback_vias(session, wanted2, 'CV_PASS2')
            markers2 = drc.check(cal)
            via_markers2 = [m for m in markers2
                            if (m.name or '').lower() == via_name.lower()]
            print(f'CV_PASS2: total via markers now {len(via_markers2)}',
                  flush=True)
            # rp intervals from POSITIVE actuals (unambiguous floor==trunc)
            rp_lo, rp_hi = Decimal(-10), Decimal(10)
            used = 0
            all_vias = dict(via_com)
            all_vias.update(via_com2)
            yv_all = sorted(((k, v[1]) for k, v in all_vias.items()),
                            key=lambda t: -t[1])
            flagged2 = set()
            for m in via_markers2:
                locs = [f.location for f in (m.figures or [])
                        if f.obj_type == 'via' and getattr(f, 'location', None)]
                if locs:
                    key = min(yv_all,
                              key=lambda t: abs(t[1] - float(locs[0].y)))[0]
                else:
                    key = None
                if key is None:
                    continue
                flagged2.add(key)
                a = Decimal(_quantity(m.actual))
                if a > 0:
                    xc, yc = all_vias[key]
                    X = ((Decimal(cx1c) - Decimal(xc)) ** 2
                         + (Decimal(cy1_cal) - Decimal(yc)) ** 2).sqrt() \
                        - Decimal(r1_cal) - W_HALF
                    rp_lo = max(rp_lo, X - a - GRID)
                    rp_hi = min(rp_hi, X - a)
                    used += 1
            if not flagged2:
                # prefix fallback over combined ladder (monotone in yv)
                flagged2 = {k for k, _ in yv_all[:len(via_markers2)]}
            print(f'CV: rp interval from {used} positive actuals: '
                  f'({rp_lo}, {rp_hi}]', flush=True)
            cands = []
            g = floor_grid(rp_lo) + GRID
            while g <= rp_hi:
                cands.append(g)
                g += GRID
            print(f'CV: on-grid rp candidates in interval: {[str(c) for c in cands]}',
                  flush=True)
            rp = cands[0] if len(cands) == 1 else None
            if rp is None:
                print('CV: rp NOT UNIQUE ON GRID - critical rungs SKIPPED '
                      '(recorded; interval and candidates above)', flush=True)
            else:
                print(f'CV: rp={rp} (learned)', flush=True)
                # consistency: predict flagged set from rp + R_via
                mism = 0
                for k, (xc, yc) in all_vias.items():
                    cl = cv_clear_exact(cx1c, cy1_cal, r1_cal, xc, yc, rp)
                    pred = cl < R_via
                    obs = k in flagged2
                    if pred != obs:
                        mism += 1
                        print(f'CV_CONSISTENCY MISMATCH {k}: pred={pred} '
                              f'obs={obs} clear={cl}', flush=True)
                print(f'CV_CONSISTENCY: mismatches={mism} '
                      f'viacom={len(all_vias)} flagged={len(flagged2)}',
                      flush=True)

                # ---- CV critical rungs ---------------------------------
                def yv_below(cy1, r1f, rp=rp, R_via=R_via):
                    k = Decimal(cy1) - Decimal(r1f) - W_HALF - rp - R_via
                    return floor_grid(k) + GRID

                cv_specs = [('CV_FLIP_LO', 540, 'delta', Decimal('1.5e-6'),
                             Decimal('2.5e-6'), yv_below),
                            ('CV_FLIP_HI', 550, 'margin', Decimal('1e-7'),
                             Decimal('2e-6'), None)]
                for tag, y0, kind, lo, hi, fn in cv_specs:
                    if fn is None:               # HI from LO eps + 3.5e-6
                        prev = cv_res.get('CV_FLIP_LO')
                        if prev is None:
                            print(f'{tag}: LO missing - SKIPPED', flush=True)
                            continue
                        cy1 = float(Decimal(prev['cy1_req']) + Decimal(10)
                                    + Decimal('0.0000035'))
                    else:
                        got = find_eps_cv(float(y0), fn, rp, R_via, kind,
                                          lo, hi)
                        if got is None:
                            print(f'{tag}: EPS_SCAN_FAILED - SKIPPED',
                                  flush=True)
                            continue
                        cy1, _yv_plan, _val_plan = got
                    print(f'=== {tag} y0={y0} cy1={cy1!r} '
                          f'bits={orc.bits(cy1)}', flush=True)
                    arc = create_arc_net(session, padstack, NET_A,
                                         (SX, float(y0)), (EX, float(y0)),
                                         (CX_NAT, cy1), False, tag)
                    if arc is None:
                        continue
                    cxc, cyc, rc = (float(arc.center.x),
                                    float(arc.center.y), float(arc.radius))
                    # Via y placed from COMMITTED arc values: yv0 below is
                    # where clear==R_via exactly; delta -> one grid CLOSER
                    # (+GRID), margin -> floor side.  +-1e-4 nudge until the
                    # window holds (warn-don't-crash).
                    yv_cur = floor_grid(Decimal(cyc) - Decimal(rc) - W_HALF
                                        - rp - R_via) \
                        + (GRID if kind == 'delta' else Decimal(0))
                    val = None
                    for _attempt in range(6):
                        yv_f = float(yv_cur)
                        cl = cv_clear_exact(cxc, cyc, rc, XV, yv_f, rp)
                        val = R_via - cl if kind == 'delta' else cl - R_via
                        if lo <= val <= hi:
                            break
                        # delta:  val>hi => via too close => move DOWN (-GRID)
                        # margin: val>hi => via too far   => move UP   (+GRID)
                        yv_cur += (GRID if (val > hi) == (kind == 'margin')
                                   else -GRID)
                    else:
                        print(f'{tag}: YV_ADJUST_FAILED val={val} (recorded, '
                              f'continuing)', flush=True)
                    yv_f = float(yv_cur)
                    session.vias.create(padstack, at=(XV, yv_f), net=NET_B)
                    vcom = readback_vias(session, [(tag, XV, yv_f)], tag)
                    xvc, yvc = vcom[tag]
                    cl = cv_clear_exact(cxc, cyc, rc, xvc, yvc, rp)
                    val = R_via - cl if kind == 'delta' else cl - R_via
                    in_window = lo <= val <= hi
                    print(f'   COMMITTED clear={cl} {kind}={val} '
                          f'in_window={in_window}', flush=True)
                    full = oracle_cv(tag, cxc, cyc, rc, xvc, yvc, rp, R_via)
                    hits = run_drc(drc, arc, tag, via_name, partner=('via',))
                    verdict = ('FLAGGED' if hits
                               else ('clean' if hits is not None else 'ERROR'))
                    actual = hits[0][2] if hits else None
                    dm = (actual == trunc_disp(full)) if actual else None
                    print(f'RESULT {tag}: verdict={verdict} actual={actual!r} '
                          f'display_match={dm}', flush=True)
                    cv_res[tag] = dict(cy1_req=cy1, verdict=verdict,
                                       actual=actual, clear=cl, arc=arc,
                                       in_window=in_window)
                if 'CV_FLIP_LO' in cv_res and 'CV_FLIP_HI' in cv_res:
                    print(f'CV_PAIR: LO={cv_res["CV_FLIP_LO"]["verdict"]} '
                          f'HI={cv_res["CV_FLIP_HI"]["verdict"]} '
                          f'(designed FLAGGED/clean)', flush=True)

        # ---- STAGE 4: re-query bit identity for all committed arcs ---------
        print('STAGE4: re-query', flush=True)
        requeried = [r for r in session.routes(layer=LAYER)
                     if r.obj_type == 'arc']
        print(f'REQUERY count={len(requeried)} created={len(ARCS_CREATED)}',
              flush=True)
        for tag, row in ARCS_CREATED:
            match = [q for q in requeried
                     if (q.start.x, q.start.y, q.end.x, q.end.y)
                     == (row.start.x, row.start.y, row.end.x, row.end.y)]
            if len(match) == 1:
                q = match[0]
                same = (orc.bits(q.center.x) == orc.bits(row.center.x)
                        and orc.bits(q.center.y) == orc.bits(row.center.y)
                        and orc.bits(q.radius) == orc.bits(row.radius))
                print(f'REQUERY {tag}: identical={same}', flush=True)
            else:
                print(f'REQUERY {tag}: MATCH_COUNT={len(match)}', flush=True)

        # ---- SUMMARY --------------------------------------------------------
        print('SUMMARY', flush=True)
        for r in results:
            if r:
                print(f'   {r["tag"]}: verdict={r["verdict"]} '
                      f'actual={r.get("actual")!r} in_window={r["in_window"]}',
                      flush=True)
        for tag in sorted(cv_res):
            r = cv_res[tag]
            print(f'   {tag}: verdict={r["verdict"]} '
                  f'actual={r.get("actual")!r} in_window={r["in_window"]}',
                  flush=True)
        try:
            total = len(drc())
        except Exception as exc:
            total = f'ERROR {exc!r}'
        print(f'TOTAL_MARKERS: {total}', flush=True)
        print('DONE', flush=True)


if __name__ == '__main__':
    main()
