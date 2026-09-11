# Shared high-precision oracle utilities for the ARC DRC probes.
#
# Model suite (task spec section 12):
#   FULL           - Decimal-60 geometry on the committed binary64 values
#   BINARY64       - plain Python float arithmetic
#   GRID           - quantize center/radius to the 1e-4 grid FIRST, then measure
#   DISTANCE-ROUND - full-precision clearance rounded to 1e-4 AFTER measuring
#
# Verdict rule proven by the line ladder: violation iff measured < rule
# (strict), evaluated in whatever domain the model computes in.
from __future__ import annotations

import math
import struct
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction

getcontext().prec = 60

GRID = Decimal('0.0001')  # accuracy=4, units=millimeters


def bits(value: float) -> str:
    """binary64 bit pattern, big-endian hex."""
    return struct.pack('>d', value).hex()


def quant4(value: float) -> float:
    """Round-to-nearest 1e-4, returned as the nearest double."""
    return float(Decimal(value).quantize(GRID, rounding=ROUND_HALF_EVEN))


def on_grid(value: float) -> bool:
    """True iff value is the nearest double to a 4-decimal quantity."""
    return quant4(value) == value


def frac_grid(value: float) -> Decimal:
    """Exact offset of the binary64 value from the nearest 1e-4 grid point."""
    return Decimal(value) - Decimal(quant4(value))


def circumcenter(S, M, E) -> tuple[Fraction, Fraction, Fraction]:
    """Exact circumcenter + radius^2 of three points (Fraction arithmetic)."""
    ax, ay = (Fraction(v) for v in S)
    bx, by = (Fraction(v) for v in M)
    cx, cy = (Fraction(v) for v in E)
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / d
    uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / d
    r2 = (ax - ux) ** 2 + (ay - uy) ** 2
    return ux, uy, r2


def dec_sqrt(r2: Fraction) -> Decimal:
    """High-precision sqrt of an exact rational."""
    return (Decimal(r2.numerator) / Decimal(r2.denominator)).sqrt()


def angle_deg(center, point) -> float:
    """Angle of point from center, degrees in [0, 360), y-up math convention."""
    return math.degrees(math.atan2(point[1] - center[1], point[0] - center[0])) % 360.0


def sweep_deg(S, E, C, clockwise: bool) -> float:
    """Sweep from S to E; clockwise means decreasing angle (y-up math sense).

    NOTE: Allegro's is_clockwise convention is calibrated empirically (probe A
    grid-exact arc, committed length vs both-direction predictions).
    """
    th_s = angle_deg(C, S)
    th_e = angle_deg(C, E)
    if clockwise:
        return (th_s - th_e) % 360.0
    return (th_e - th_s) % 360.0


def bottom_in_span(S, E, C, clockwise: bool) -> bool:
    """Is the circle bottom (angle 270 deg) inside the arc's angular span?"""
    th_s = angle_deg(C, S)
    sweep = sweep_deg(S, E, C, clockwise)
    if clockwise:
        return ((th_s - 270.0) % 360.0) <= sweep + 1e-9
    return ((270.0 - th_s) % 360.0) <= sweep + 1e-9


def arc_length(radius: float, sweep: float) -> float:
    return radius * math.radians(sweep)


# --- clearance models: arc bottom vs horizontal line below -----------------
# All return the copper-edge clearance (centerline distance minus half widths).

def clearance_full(bottom_y: Decimal, line_y: Decimal,
                   w_arc: Decimal, w_line: Decimal) -> Decimal:
    return (bottom_y - line_y) - (w_arc + w_line) / 2


def model_FULL(C, r, line_y, w_arc, w_line) -> Decimal:
    """Decimal-60 on exact expansions of the committed binary64 values."""
    bottom_y = Decimal(C[1]) - r
    return clearance_full(bottom_y, Decimal(line_y), Decimal(w_arc), Decimal(w_line))


def model_BINARY64(C, r, line_y, w_arc, w_line) -> float:
    return (C[1] - r - line_y) - (w_arc + w_line) / 2.0


def model_GRID(C, r, line_y, w_arc, w_line) -> Decimal:
    """Quantize center and radius to the 1e-4 grid first, then measure."""
    cy_g = Decimal(quant4(C[1]))
    r_g = Decimal(quant4(float(r)))
    return clearance_full(cy_g - r_g, Decimal(line_y),
                          Decimal(w_arc), Decimal(w_line))


def model_DISTANCE_ROUND(clearance: Decimal) -> Decimal:
    return clearance.quantize(GRID, rounding=ROUND_HALF_EVEN)


def verdict(clearance, rule) -> str:
    """Strict measured < rule, in the model's own domain."""
    return 'FLAGGED' if clearance < rule else 'clean'
