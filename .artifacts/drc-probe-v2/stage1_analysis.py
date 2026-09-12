"""Offline derivation for the completed Stage-I evidence sets.

This reads preserved JSONL only.  It never opens Allegro or changes source data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import subprocess
import re
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RUNS = {
    "ia_quantizer_60": RESULTS / "ia-quantizer-60/run-64000-1789189177779421800",
    "ia_scalar_120": RESULTS / "ia-scalar-120/run-51340-1789190383784285200",
    "ib_center_40": RESULTS / "ib-center-40/run-66284-1789189802536493400",
    "ib_alpha_36": RESULTS / "ib-alpha-36/run-11788-1789189996641797000",
    "save_reopen_4": RESULTS / "save-reopen-4/run-49468-1789191093882788300",
}


def fbits(x: float) -> str:
    return struct.pack(">d", float(x)).hex()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def scalar_from_case(row: dict) -> tuple[float, float]:
    req = row["transaction_return"]["request"]
    role = row["role"]
    if role.startswith("via"):
        p = req["x17"] if role.endswith("x") else req["y17"]
    else:
        p = req["start"]["x17"] if role.endswith("x") else req["start"]["y17"]
    committed = row["transaction_return"]["committed"]
    axis = "x" if role.endswith("x") else "y"
    numeric = committed[axis] if role.startswith("via") else committed["start"][axis]
    if isinstance(numeric, dict):
        numeric = numeric["value"]
    return float(p), float(numeric)


def rounding_modes(x: Fraction) -> dict[str, int]:
    # Exact integer rounding modes, including signed toward-zero and away-zero.
    floor = x.numerator // x.denominator
    ceil = -((-x.numerator) // x.denominator)
    trunc = floor if x >= 0 else ceil
    away = ceil if x >= 0 else floor
    n = floor if x - floor < Fraction(1, 2) else (ceil if x - floor > Fraction(1, 2) else (floor if floor % 2 == 0 else ceil))
    frac = x - floor
    if frac < Fraction(1, 2):
        nearest_away = nearest_toward = ties_plus = ties_minus = floor
    elif frac > Fraction(1, 2):
        nearest_away = nearest_toward = ties_plus = ties_minus = ceil
    else:
        nearest_away = ceil if x >= 0 else floor
        nearest_toward = floor if x >= 0 else ceil
        ties_plus, ties_minus = ceil, floor
    return {"floor": floor, "ceil": ceil, "toward_zero": trunc,
            "nearest_ties_even": n, "nearest_ties_away_zero": nearest_away,
            "nearest_ties_toward_zero": nearest_toward,
            "ties_plus_inf": ties_plus, "ties_minus_inf": ties_minus}


def q_analysis(rows: list[dict], g: Fraction) -> dict:
    models = {"RAW_exact_actualEcho_over_g": lambda h: Fraction.from_float(h) / g,
              "MUL10000_B64": lambda h: Fraction.from_float(h * float(1 / g)),
              "DIV_B64": lambda h: Fraction.from_float(h / float(g))}
    out = {name: {mode: {"survives": True, "counterexample": None} for mode in rounding_modes(Fraction(0)).keys()} for name in models}
    for row in rows:
        h, committed = scalar_from_case(row)
        for model, fn in models.items():
            q = fn(h)
            for mode, k in rounding_modes(q).items():
                predicted = float(Fraction(k) * g)
                if fbits(predicted) != fbits(committed):
                    out[model][mode]["survives"] = False
                    if out[model][mode]["counterexample"] is None:
                        out[model][mode]["counterexample"] = {
                            "case": row["index"], "role": row["role"], "label": row.get("label"),
                            "H": row.get("H"), "actual_echo": h, "actual_echo_bits": fbits(h),
                            "committed": committed, "committed_bits": fbits(committed),
                            "predicted": predicted, "predicted_bits": fbits(predicted), "k": str(k)}
    return {"grid_g": str(g), "models": out}


def assert_rounding_modes() -> None:
    expected = {"floor": -2, "ceil": -1, "toward_zero": -1,
                "nearest_ties_even": -2, "nearest_ties_away_zero": -2,
                "nearest_ties_toward_zero": -1, "ties_plus_inf": -1,
                "ties_minus_inf": -2}
    assert rounding_modes(Fraction(-3, 2)) == expected
    assert rounding_modes(Fraction(1, 10))["nearest_ties_even"] == 0
    assert rounding_modes(Fraction(9, 10))["nearest_ties_even"] == 1
    assert rounding_modes(Fraction(1, 2))["nearest_ties_even"] == 0
    assert rounding_modes(Fraction(3, 2))["nearest_ties_even"] == 2


def point(v: dict) -> tuple[float, float]:
    if isinstance(v, dict) and "x" in v and "y" in v:
        x, y = v["x"], v["y"]
        return float(x["value"] if isinstance(x, dict) else x), float(y["value"] if isinstance(y, dict) else y)
    return float(v[0]["value"]), float(v[1]["value"])


def point17(v: dict) -> tuple[Decimal, Decimal]:
    return Decimal(str(v["x17"])), Decimal(str(v["y17"]))


def decimal_fraction(q: Fraction) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 100
        return Decimal(q.numerator) / Decimal(q.denominator)


def decimal_sub(a: Decimal, b: Decimal) -> str:
    with localcontext() as ctx:
        ctx.prec = 100
        return str(a - b)


def ib_metrics(rows: list[dict]) -> dict:
    metrics = []
    for row in rows:
        tx = row.get("transaction_return", {}); c = tx.get("committed", {}); req = tx.get("request", {})
        if not c or not c.get("center") or not req.get("center"):
            continue
        s, e, dbcenter = point(c["start"]), point(c["end"]), point(c["center"])
        c0text = point17(req["center"]); stext = point17(req["start"]); etext = point17(req["end"])
        s17 = tuple(float(z) for z in stext); e17 = tuple(float(z) for z in etext); c0 = tuple(float(z) for z in c0text)
        sx, sy = (Fraction.from_float(z) for z in s17); ex, ey = (Fraction.from_float(z) for z in e17)
        cx, cy = (Fraction.from_float(z) for z in c0)
        vx, vy = ex-sx, ey-sy; mx, my = (sx+ex)/2, (sy+ey)/2
        t = ((cx-mx)*vx + (cy-my)*vy) / (vx*vx + vy*vy)
        px, py = cx-t*vx, cy-t*vy
        with localcontext() as ctx:
            ctx.prec = 100
            dsx,dsy,dex,dey,dcx,dcy = [decimal_fraction(q) for q in (sx,sy,ex,ey,cx,cy)]
            dx0, dy0 = dsx-dcx, dsy-dcy
            dx1, dy1 = dex-dcx, dey-dcy
            rsd = (dx0*dx0+dy0*dy0).sqrt(); red = (dx1*dx1+dy1*dy1).sqrt(); mean_d = (rsd+red)/Decimal(2)
            exported_d = Decimal.from_float(float(c["radius"]["%.17g"])) if isinstance(c.get("radius"), dict) else Decimal.from_float(float(c.get("radius")))
            cdbtext = point17(c["center"]); cdbf = tuple(float(z) for z in cdbtext)
            dcdb = [decimal_fraction(Fraction.from_float(z)) for z in cdbf]
            db_res = [dcdb[i]-[dcx,dcy][i] for i in (0,1)]
            v2d = Decimal(vx.numerator) / Decimal(vx.denominator) * (Decimal(1)) * (Decimal(vx.numerator) / Decimal(vx.denominator)) + Decimal(vy.numerator) / Decimal(vy.denominator) * (Decimal(vy.numerator) / Decimal(vy.denominator))
            perp_len = v2d.sqrt(); half2 = v2d/Decimal(4)
            rem = mean_d*mean_d - half2
            mxd = (dsx+dex)/Decimal(2); myd = (dsy+dey)/Decimal(2)
            vxd = Decimal(vx.numerator)/Decimal(vx.denominator); vyd = Decimal(vy.numerator)/Decimal(vy.denominator)
            recenter = [] if rem < 0 else [[str(mxd + sign*(-vyd/perp_len)*rem.sqrt()), str(myd + sign*(vxd/perp_len)*rem.sqrt())] for sign in (-1,1)]
        rs, radius_end, exported = float(rsd), float(red), float(exported_d)
        mean_r = (rs + radius_end) / 2
        pcenter = [str(decimal_fraction(mx)), str(decimal_fraction(my))]
        p_dec = [decimal_fraction(px), decimal_fraction(py)]
        c0_dec = [decimal_fraction(cx), decimal_fraction(cy)]
        recenter_res = [[str(dcdb[i]-Decimal(z)) for i,z in enumerate(candidate)] for candidate in recenter]
        intent = row.get("intent") or {}
        htext = str(row.get("H", ""))
        hparts = [Fraction(int(a), int(b)) for a,b in re.findall(r"Fraction\((-?\d+),\s*(\d+)\)", htext)]
        alpha = intent.get("alpha") if isinstance(intent, dict) else None
        if not intent:
            alpha = str(hparts[2]) if len(hparts) > 2 else None
            beta = str(hparts[3]) if len(hparts) > 3 else None
        else:
            beta = intent.get("beta")
        metrics.append({"index": row.get("index"), "label": row.get("label"), "beta": beta,
                        "alpha": alpha, "coefficient_source": "intent" if isinstance(intent, dict) and "alpha" in intent else "H tuple", "M": pcenter,
                        "P_C0": [str(p_dec[0]), str(p_dec[1])], "C0_request": [str(c0_dec[0]), str(c0_dec[1])], "C_db": [str(dcdb[0]), str(dcdb[1])],
                        "r_start": rs, "r_end": radius_end, "mean_endpoint_radius": mean_r,
                        "mean_radius_decimal": str(mean_d), "exported_radius_decimal": str(exported_d), "mean_minus_exported": decimal_sub(mean_d, exported_d),
                        "C0_to_P_C": [decimal_sub(c0_dec[0],p_dec[0]), decimal_sub(c0_dec[1],p_dec[1])],
                        "P_C0_to_Cdb": [decimal_sub(dcdb[0],p_dec[0]), decimal_sub(dcdb[1],p_dec[1])],
                        "Cdb_minus_recenter": recenter_res,
                        "Cdb_minus_C0": [str(z) for z in db_res], "recenter_candidates": recenter,
                        "recenter_feasible": bool(recenter)})
    return {"count": len(metrics), "samples": metrics,
            "interpretation": "descriptive residuals; no orthogonal-projection claim"}


def save_summary(rows: list[dict]) -> dict:
    checks = []
    for r in rows:
        save, reopen = r.get("save"), r.get("reopen")
        required = isinstance(save, dict) and isinstance(reopen, dict) and all(k in save for k in ("ok", "fresh_requery_count", "fresh_requery_all_target_dto", "fresh_dto", "observable_state")) and all(k in reopen for k in ("routes_count", "all_arc_dto", "target_match_count", "target_dto", "observable_state", "process_poll"))
        checks.append(required and r.get("status") == "PASS" and save["ok"] is True and save["fresh_requery_count"] == 1 and len(save["fresh_requery_all_target_dto"]) == 1 and reopen["target_match_count"] == 1 and save["observable_state"] == reopen["observable_state"] == "STABLE" and reopen["process_poll"] == 1)
    return {"count": len(rows), "statuses": {s: sum(r.get("status") == s for r in rows) for s in {r.get("status") for r in rows}},
            "explicit_field_checks": checks, "all_fields_bits_stable": bool(checks) and all(checks),
            "does_not_prove": "internal Allegro storage semantics"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=ROOT / "results/stage1-analysis")
    args = ap.parse_args()
    assert_rounding_modes()
    args.output.mkdir(parents=True, exist_ok=False)
    source_hashes = {}
    for name, folder in RUNS.items():
        for f in sorted(folder.iterdir()):
            if f.is_file() and f.name in {"cases.jsonl", "manifest.json", "stage1_smoke.il", "stage1_smoke.py", "save_reopen_4.py", "ia_quantizer_60.py", "ia_scalar_120.py", "ib_center_40.py", "ib_alpha_36.py"}:
                source_hashes[str(f)] = hashlib.sha256(f.read_bytes()).hexdigest()
    ia60 = read_jsonl(RUNS["ia_quantizer_60"] / "cases.jsonl")
    ia120 = read_jsonl(RUNS["ia_scalar_120"] / "cases.jsonl")
    ia = ia60 + ia120
    ibc = read_jsonl(RUNS["ib_center_40"] / "cases.jsonl")
    iba = read_jsonl(RUNS["ib_alpha_36"] / "cases.jsonl")
    roles = sorted({r["role"] for r in ia})
    by_role = {role: q_analysis([r for r in ia if r["role"] == role], Fraction(1,10000)) for role in roles}
    assert len(roles) == 6 and all(len([r for r in ia if r["role"] == role]) == 30 for role in roles)
    result = {"status": "INCOMPLETE_DERIVED_ANALYSIS", "source_hashes": source_hashes,
              "ia_quantizer_60": q_analysis(ia, Fraction(1, 10000)), "ia_by_role": by_role,
              "rounding_unit_tests": "PASS", "ia_observed_cases": len(ia), "ia_60_cases": len(ia60), "ia_120_cases": len(ia120),
              "ia_roles": sorted({r["role"] for r in ia}),
              "ib_center_40": ib_metrics(ibc), "ib_alpha_36": ib_metrics(iba),
              "save_reopen_4": save_summary(read_jsonl(RUNS["save_reopen_4"] / "cases.jsonl")),
              "limits": ["Q uses actual request echo, not intended H", "Decimal-100 is approximation, not exact", "no DRC/internal comparator conclusion"]}
    (args.output / "analysis.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output / "analysis.json"), "ia_cases": len(ia)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
