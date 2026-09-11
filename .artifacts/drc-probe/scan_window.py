# Offline critical-window scan for Probe B (Line-ARC DRC).
#
# Geometry: arc with chord S=(300,y0) -> E=(302.0001,y0); center C on the
# chord's perpendicular bisector (cx = 301.00005), cy scanned.  Horizontal
# NET_B line below at grid y=L.  Bottom point (cx, cy-r) is the closest
# approach when it lies in span (checked).
#
# Clearance (copper edge) = p - L - w_total, p = cy - r.
# L is on the 1e-4 grid, w_total = (w_arc+w_line)/2 = 0.15 exactly, so
#     clearance mod 1e-4 = phi := (p - w_total) mod 1e-4
# is fixed by the ARC alone; the line only shifts clearance by whole grid
# steps.  phi is therefore the knob: scanning cy moves phi ~0.876:1.
#
# Windows (R = probed rule, assumed on-grid; delta = R - clearance):
#   FLIP  delta in (0.5e-6, 2.5e-6)  -> phi in (9.75e-5, 9.95e-5)
#           clearance_full < R (model A: FLAGGED) but round4(clearance)==R
#           (model C: clean) AND display shows actual=='0.06 MM'.
#           A cy pair +/-1e-6 straddles the boundary -> Phase 4 flip.
#   GOLD  delta in (5e-6, 4.9e-5)   -> phi in (5.1e-5, 9.5e-5)
#           same display/verdict logic, wider margin against r-derivation
#           differences between our model and Allegro's commit.
#   ABOVE clearance just ABOVE R (phi in (0.5e-6, 2.5e-5)) -> clean control
#           whose display also rounds to R.
#
# Radius hypothesis: committed r = nearest double to hypot(C-S) (A2/A3/A5
# decide |S-C| vs |E-C|; for bisector centers they differ <=1 ulp, and the
# script prints both so the choice can be re-verified after probe A).
#
# phi computed in float for the coarse pass (resolution ~5e-10 mm, ample vs
# 5e-6 windows), then re-verified with exact Decimal expansions of the same
# doubles that go over the wire (json.dumps repr round-trips binary64).
from __future__ import annotations

import math
from decimal import Decimal

import arc_oracle as orc

W_ARC = 0.15
W_LINE = 0.15
W_TOTAL = Decimal('0.15')          # (0.15+0.15)/2 exact in decimal
R_PLACEHOLDER = Decimal('0.06')    # re-derive L after rule probe; phi is R-independent
GRID = Decimal('0.0001')
SX, EX = 300.0, 302.0001
CX_NAT = 301.00005                 # (SX+EX)/2 in decimal
CY_OFF = 0.124975                  # circumcenter cy offset for M=(300.5, y0+1)

WINDOWS = {
    'FLIP':  (Decimal('0.0000975'), Decimal('0.0000995')),
    'GOLD':  (Decimal('0.000051'),  Decimal('0.000095')),
    'ABOVE': (Decimal('0.0000005'), Decimal('0.000025')),
}


def phi_float(cy: float, y0: float) -> float:
    r = math.hypot(CX_NAT - SX, cy - y0)
    p = cy - r
    return (p * 1e4) % 1.0 / 1e4   # frac mod 1e-4, float


def exact_case(cy: float, y0: float) -> dict:
    """Exact Decimal recomputation on the wire doubles."""
    r_s = math.hypot(CX_NAT - SX, cy - y0)
    r_e = math.hypot(CX_NAT - EX, cy - y0)
    p = Decimal(cy) - Decimal(r_s)
    phi = (p - W_TOTAL) % GRID
    # grid line L placing clearance just below R: clearance = p - L - w_total
    L_dec = (p - W_TOTAL - R_PLACEHOLDER).quantize(GRID, rounding='ROUND_FLOOR')
    L_dec += GRID                  # floor then +1 grid -> clearance < R, within 1 grid
    clearance = p - Decimal(L_dec) - W_TOTAL
    delta = R_PLACEHOLDER - clearance
    return dict(cy=cy, y0=y0, r_s=r_s, r_e=r_e, p=p, phi=phi,
                L=float(L_dec), clearance=clearance, delta=delta,
                r_ambiguity=Decimal(r_s) - Decimal(r_e))


def main() -> None:
    for y0 in (400.0, 410.0, 420.0):
        cy_nat = y0 + CY_OFF
        print(f'=== y0={y0}  cy_nat={cy_nat!r}  cx={CX_NAT!r}', flush=True)
        found = {k: [] for k in WINDOWS}
        # coarse scan: +-1.5e-4 around the natural circumcenter cy, 1e-8 step
        n = 0
        cy = cy_nat - 1.5e-4
        while cy <= cy_nat + 1.5e-4 and n < 40000:
            ph = phi_float(cy, y0)
            for name, (lo, hi) in WINDOWS.items():
                if float(lo) <= ph <= float(hi) and len(found[name]) < 4:
                    case = exact_case(cy, y0)
                    if lo <= case['phi'] <= hi:
                        found[name].append(case)
            cy += 1e-8
            n += 1
        print(f'   scanned {n} cy values', flush=True)
        for name, cases in found.items():
            print(f'   --- window {name} ({len(cases)} kept)', flush=True)
            for c in cases:
                print(f"   cy={c['cy']!r} bits={orc.bits(c['cy'])}", flush=True)
                print(f"      r_S={c['r_s']!r} bits={orc.bits(c['r_s'])}", flush=True)
                print(f"      r_E={c['r_e']!r}  |r_S-r_E|={c['r_ambiguity']}",
                      flush=True)
                print(f"      p=cy-r exact={c['p']}", flush=True)
                print(f"      phi={c['phi']}  delta={c['delta']}", flush=True)
                print(f"      L={c['L']!r} on_grid={orc.on_grid(c['L'])} "
                      f"clearance={c['clearance']}", flush=True)
                b64 = float(c['clearance'])
                print(f"      BINARY64 clearance={b64!r} "
                      f"(float<0.06: {b64 < 0.06})", flush=True)
                dr = c['clearance'].quantize(GRID, rounding='ROUND_HALF_EVEN')
                print(f"      DISTANCE-ROUND -> {dr} "
                      f"(== R: {dr == R_PLACEHOLDER})", flush=True)
                print(f"      GRID-model: quant4(cy)={orc.quant4(c['cy'])!r} "
                      f"quant4(r)={orc.quant4(c['r_s'])!r}", flush=True)


if __name__ == '__main__':
    main()
