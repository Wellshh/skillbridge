"""Offline regression for v2 DRC oracle errata.

Grid cases are represented as integer DBU/Fraction throughout. Decimal values
are only high precision approximations of explicit binary64 observations.
"""
from __future__ import annotations
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "drc-probe"))
import arc_oracle

getcontext().prec = 100
OUT = Path(__file__).with_name("oracle_regression.json")
R = Fraction(6, 100)

def dec(q: Fraction) -> str:
    return format(Decimal(q.numerator) / Decimal(q.denominator), "f")

def verdict(c: Fraction, rule: Fraction) -> str:
    return "FLAGGED" if c < rule else "CLEAN"

def main() -> None:
    b_grid = (Fraction("460.75") - Fraction("1.25") - Fraction("459.29") - (Fraction(".15") + Fraction(".15"))/2)
    b_stair = (Fraction("540.75") - Fraction("1.25") - Fraction("539.2901") - (Fraction(".15") + Fraction(".15"))/2)
    cases = [
        {"case_id":"B_GRID_EQ", "geometry":"Line-ARC", "clearance_dbu":600,
         "exact_clearance":b_grid, "historical_float_decimal":"0.0599999999999795419203252322404296137392520904541015625",
         "historical_actual":"CLEAN", "source":"prompt fixture"},
        {"case_id":"B_STAIR_n6", "geometry":"Line-ARC", "clearance_dbu":599,
         "exact_clearance":b_stair, "historical_float_decimal":"0.0598999999999478005552333570449263788759708404541015625",
         "historical_actual":"FLAGGED", "source":"prompt fixture"},
        {"case_id":"C_CC_GOLD", "geometry":"ARC-ARC", "clearance_dbu":600,
         "exact_clearance":None, "historical_float_decimal":"0.05999999999998575361814800999127328395843505859375",
         "historical_actual":"FLAGGED", "source":"probe_c.run2 log"},
    ]
    result = {"status":"OFFLINE_REGRESSIONS_PASS", "rule_fraction":str(R), "rule_decimal":dec(R),
              "numeric_semantics":"exact grid uses Fraction; Decimal-100 is high-precision approximation, not mathematical exact",
              "cases":[]}
    for c in cases:
        if c["case_id"] == "C_CC_GOLD":
            cy1 = Decimal("620.12492759"); r1 = Decimal("1.0078228540984784")
            cy2 = Decimal("617.899325"); r2 = Decimal("1.0078287320398243")
            q1 = cy1.quantize(Decimal("0.0001")); q2 = cy2.quantize(Decimal("0.0001"))
            qr1 = r1.quantize(Decimal("0.0001")); qr2 = r2.quantize(Decimal("0.0001"))
            exact = q1 - q2 - qr1 - qr2 - Decimal("0.15")
            exact_fraction = None
        else:
            exact = c["exact_clearance"]
            exact_fraction = exact
        raw = Decimal(c["historical_float_decimal"])
        item = {k:v for k,v in c.items() if k not in ("exact_clearance",)}
        item.update({"exact_clearance":dec(exact_fraction) if exact_fraction is not None else str(exact), "exact_verdict":verdict(exact,R) if isinstance(exact, Fraction) else ("FLAGGED" if exact < Decimal("0.06") else "CLEAN"),
                     "raw_float_decimal":str(raw), "raw_float_verdict":"FLAGGED" if raw < Decimal("0.06") else "CLEAN",
                     "raw_minus_exact":str(raw - (Decimal(dec(exact_fraction)) if exact_fraction is not None else exact))})
        result["cases"].append(item)
    result["errata"] = [
        "B GRID_EQ error is about -2.0458e-14 mm, not -2.05e-11 mm.",
        "B STAIR_n7 is flagged on both sides; it is not a float false-negative counterexample.",
        "C CC_GOLD old report text conflicts with the raw run log; raw log says FLAGGED and is retained as such.",
        "A grid oracle predicting FLAGGED while the historical target marker was CLEAN is a false positive, not a false negative.",
        "Historical empty-marker observations are not this run's reliable CLEAN gate."
    ]
    # The model_GRID historical implementation must reproduce the known
    # binary64 contamination on GRID_EQ, while exact grid arithmetic is clean.
    grid_model = arc_oracle.model_GRID((301.0,460.75), 1.25, 459.29, .15, .15)
    result["old_model_grid_check"] = {"value":str(grid_model), "verdict":arc_oracle.verdict(grid_model, Decimal("0.06")), "expected":"FLAGGED"}
    assert b_grid == R and b_stair == Fraction("0.0599")
    assert result["old_model_grid_check"]["verdict"] == "FLAGGED"
    assert result["old_model_grid_check"]["verdict"] != verdict(b_grid, R)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status":result["status"],"output":OUT.as_posix()}))

if __name__ == "__main__":
    main()
