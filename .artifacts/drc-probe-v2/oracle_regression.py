"""Offline historical oracle regression from raw probe logs.

This artifact deliberately separates three models:
ALL_B64_WIDTH, B64_GEOMETRY_IDEAL_WIDTH, and GRID_NORMALIZED.
It does not claim a generic finite-geometry kernel or an Allegro gate.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 100
ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / ".artifacts" / "drc-probe" / "logs"
B_LOG = LOG_DIR / "probe_b.b9phteksv.log"
C_LOG = LOG_DIR / "probe_c.run2-full-success.bvc57j0lt.log"
OUT = Path(__file__).with_name("oracle_regression.json")
RUN_ROOT = Path(__file__).with_name("results") / "historical-oracle"
RULE = Fraction(3, 50)
GRID = Fraction(1, 10000)
IDEAL_W = Fraction(3, 20)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def b64(s: str) -> Fraction:
    """Parse a logged decimal field as the binary64 value actually sent/stored."""
    return Fraction.from_float(float(s))


def exact(s: str) -> Fraction:
    return Fraction(s)


def dec(q: Fraction) -> str:
    return format(Decimal(q.numerator) / Decimal(q.denominator), "f")


def verdict(c: Fraction, rule: Fraction = RULE) -> str:
    return "FLAGGED" if c < rule else "CLEAN"


def grid_round(q: Fraction) -> Fraction:
    """Nearest, ties-to-even integer DBU without float/Decimal round-trip."""
    scaled = q / GRID
    n, d = scaled.numerator, scaled.denominator
    sign = -1 if n < 0 else 1
    n = abs(n)
    k, rem = divmod(n, d)
    twice = rem * 2
    if twice > d or (twice == d and k % 2):
        k += 1
    return Fraction(sign * k) * GRID


def line_arc(cy: Fraction, radius: Fraction, line_y: Fraction,
             wa: Fraction, wl: Fraction) -> Fraction:
    return cy - radius - line_y - (wa + wl) / 2


def arc_arc(c1: tuple[Fraction, Fraction], r1: Fraction,
            c2: tuple[Fraction, Fraction], r2: Fraction,
            w1: Fraction, w2: Fraction) -> Fraction:
    # C_CC_GOLD is intentionally axis-aligned in the logged raw geometry.
    if c1[0] != c2[0]:
        raise AssertionError("fixture requires axis-aligned centers")
    center_distance = abs(c1[1] - c2[1])
    return center_distance - r1 - r2 - (w1 + w2) / 2


def source(path: Path, start: int, end: int) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    raw = lines[start - 1:end]
    return {"path": path.as_posix(), "sha256": sha256(path),
            "line_start": start, "line_end": end,
            "raw": raw}


def block(path: Path, start: int, end: int) -> str:
    return "\n".join(path.read_text(encoding="utf-8").splitlines()[start - 1:end])


def cap(pattern: str, text: str, label: str) -> str:
    m = re.search(pattern, text, re.S)
    if not m:
        raise AssertionError(f"missing raw field {label}")
    return m.group(1)


def parse_b_fixture(path: Path, start: int, end: int, tag: str) -> dict[str, str]:
    text = block(path, start, end)
    p = re.escape(tag)
    return {
        "sx": cap(rf"{p}: ARC requested S=\(([^,]+),", text, "S.x"),
        "sy": cap(rf"{p}: ARC requested S=\([^,]+, ([^)]+)\)", text, "S.y"),
        "ex": cap(rf"{p}: ARC requested S=\([^)]*\) E=\(([^,]+),", text, "E.x"),
        "ey": cap(rf"{p}: ARC requested S=\([^)]*\) E=\([^,]+, ([^)]+)\)", text, "E.y"),
        "cx": cap(rf"{p}: ARC requested .*? C=\(([^,]+),", text, "C.x"),
        "cy": cap(rf"{p}: ARC requested .*? C=\([^,]+, ([^)]+)\)", text, "C.y"),
        "cw": cap(rf"{p}: ARC requested .* cw=([^\s]+)", text, "clockwise"),
        "radius": cap(r"committed radius: ([^ ]+)", text, "radius"),
        "line_y": cap(rf"{p}: LINE requested y=([^ ]+)", text, "line.y"),
        # The GRID_EQ clean block has no target FIGURE. Width is the shared
        # constructor input in probe_b.py, so it is intentionally not inferred
        # from the neighboring GRID_FLAG marker.
        "width": "0.15",
    }


def parse_c_fixture(path: Path, start: int, end: int) -> dict[str, str]:
    text = block(path, start, end)
    centers = re.findall(r"committed C=\(([-0-9.]+) bits=.*?\| ([-0-9.]+) bits=", text)
    radii = re.findall(r"committed r=([-0-9.]+) bits=", text)
    widths = re.findall(r"'width': ([0-9.]+)", text)
    if len(centers) != 2 or len(radii) != 2 or len(widths) < 2:
        raise AssertionError("incomplete C_CC_GOLD raw fields")
    return {"upper_cx": centers[0][0], "upper_cy": centers[0][1],
            "lower_cx": centers[1][0], "lower_cy": centers[1][1],
            "upper_radius": radii[0], "lower_radius": radii[1],
            # In the raw marker, FIG[0] is lower FINGER_SPI_MISO and FIG[1]
            # is upper NFC_SWP; retain that identity even though both are .15.
            "upper_width": widths[1], "lower_width": widths[0],
            "upper_cw": cap(r"CREATE_ARC CC_GOLD_UPPER net=NFC_SWP cw=([^\n]+)", text, "upper clockwise"),
            "lower_cw": cap(r"CREATE_ARC CC_GOLD_LOWER net=FINGER_SPI_MISO cw=([^\n]+)", text, "lower clockwise")}


def main() -> int:
    # Source anchors are checked before any numerical assertion.
    assert B_LOG.is_file() and C_LOG.is_file()
    src_b_grid = source(B_LOG, 157, 180)
    src_b_stair = source(B_LOG, 351, 376)
    src_c_gold = source(C_LOG, 86, 118)
    src_b_grid["field_map"] = {"S/E/C": "log:158-164", "radius": "log:162",
                                "line_y": "log:168-170", "width": "probe_b.py:79,133,171 (constructor input; no GRID_EQ target FIGURE)"}
    src_b_stair["field_map"] = {"S/E/C": "log:352-355", "radius": "log:356",
                                 "line_y": "log:362-363", "width": "log:373-374 FIGURE and probe_b.py:79"}
    src_c_gold["field_map"] = {"upper_C/radius": "log:89-95", "lower_C/radius": "log:98-104",
                                "width": "log:114-115 FIGURE (FIG0 lower, FIG1 upper)", "cw": "log:88,97"}

    # Parse every model input from the anchored raw log text first.
    bg_raw = parse_b_fixture(B_LOG, 157, 180, "GRID_EQ")
    bs_raw = parse_b_fixture(B_LOG, 351, 376, "STAIR_n6")
    cg_raw = parse_c_fixture(C_LOG, 86, 118)
    # Actual logged fields, reconstructed from their raw decimal spellings.
    # Every ALL_B64 field goes through Fraction.from_float(float(...)).
    bg = {
        "S": (b64(bg_raw["sx"]), b64(bg_raw["sy"])), "E": (b64(bg_raw["ex"]), b64(bg_raw["ey"])),
        "C": (b64(bg_raw["cx"]), b64(bg_raw["cy"])), "radius": b64(bg_raw["radius"]),
        "line_y": b64(bg_raw["line_y"]), "arc_width": b64(bg_raw["width"]), "line_width": b64(bg_raw["width"]),
    }
    bs = {
        "S": (b64(bs_raw["sx"]), b64(bs_raw["sy"])), "E": (b64(bs_raw["ex"]), b64(bs_raw["ey"])),
        "C": (b64(bs_raw["cx"]), b64(bs_raw["cy"])), "radius": b64(bs_raw["radius"]),
        "line_y": b64(bs_raw["line_y"]), "arc_width": b64(bs_raw["width"]), "line_width": b64(bs_raw["width"]),
    }
    cg = {
        "upper_C": (b64(cg_raw["upper_cx"]), b64(cg_raw["upper_cy"])),
        "lower_C": (b64(cg_raw["lower_cx"]), b64(cg_raw["lower_cy"])),
        "upper_radius": b64(cg_raw["upper_radius"]), "lower_radius": b64(cg_raw["lower_radius"]),
        "upper_width": b64(cg_raw["upper_width"]), "lower_width": b64(cg_raw["lower_width"]),
    }

    def b_models_line(row: dict[str, Fraction], grid_cy: str,
                      grid_r: str, grid_y: str) -> dict[str, object]:
        all_b64 = line_arc(row["C"][1], row["radius"], row["line_y"],
                           row["arc_width"], row["line_width"])
        ideal = line_arc(row["C"][1], row["radius"], row["line_y"],
                         IDEAL_W, IDEAL_W)
        normalized = line_arc(grid_round(row["C"][1]), grid_round(row["radius"]),
                              grid_round(row["line_y"]), IDEAL_W, IDEAL_W)
        return {
            "ALL_B64_WIDTH": {"fraction": str(all_b64), "decimal100": dec(all_b64), "verdict": verdict(all_b64)},
            "B64_GEOMETRY_IDEAL_WIDTH": {"fraction": str(ideal), "decimal100": dec(ideal), "verdict": verdict(ideal)},
            "GRID_NORMALIZED": {"fraction": str(normalized), "decimal100": dec(normalized), "verdict": verdict(normalized),
                                 "grid_rule": "nearest_ties_even_integer_DBU"},
            "all_minus_ideal": str(all_b64 - ideal),
        }

    bg_m = b_models_line(bg, "460.75", "1.25", "459.29")
    bs_m = b_models_line(bs, "540.75", "1.25", "539.2901")

    all_c = arc_arc(cg["upper_C"], cg["upper_radius"], cg["lower_C"],
                    cg["lower_radius"], cg["upper_width"], cg["lower_width"])
    ideal_c = arc_arc(cg["upper_C"], cg["upper_radius"], cg["lower_C"],
                      cg["lower_radius"], IDEAL_W, IDEAL_W)
    normalized_c = arc_arc((grid_round(cg["upper_C"][0]), grid_round(cg["upper_C"][1])), grid_round(cg["upper_radius"]),
                           (grid_round(cg["lower_C"][0]), grid_round(cg["lower_C"][1])), grid_round(cg["lower_radius"]),
                           IDEAL_W, IDEAL_W)
    # The GRID model uses the logged four-decimal normalized center/radius values.
    c_models = {
        "ALL_B64_WIDTH": {"fraction": str(all_c), "decimal100": dec(all_c), "verdict": verdict(all_c)},
        "B64_GEOMETRY_IDEAL_WIDTH": {"fraction": str(ideal_c), "decimal100": dec(ideal_c), "verdict": verdict(ideal_c)},
        "GRID_NORMALIZED": {"fraction": str(normalized_c), "decimal100": dec(normalized_c), "verdict": verdict(normalized_c),
                             "grid_rule": "nearest_ties_even_integer_DBU"},
        "all_minus_ideal": str(all_c - ideal_c),
    }

    result: dict[str, object] = {
        "status": "RUNNING",
        "numeric_semantics": "Fraction exact algebra; Decimal-100 display only; no generic-kernel claim",
        "rule": {"fraction": str(RULE), "decimal100": dec(RULE)},
        "sources": {"B_GRID_EQ": src_b_grid, "B_STAIR_n6": src_b_stair, "C_CC_GOLD": src_c_gold},
        "fixtures": {
            "B_GRID_EQ": {"source_case": "historical raw log", "models": bg_m,
                          "historical_observation": "target marker absent; HISTORICAL_ABSENCE_ONLY"},
            "B_STAIR_n6": {"source_case": "historical raw log", "models": bs_m,
                           "historical_observation": "FLAGGED, expected='0.06 MM', actual='0.0599 MM'"},
            "C_CC_GOLD": {"source_case": "historical raw log", "models": c_models,
                          "historical_observation": "FLAGGED, expected='0.06 MM', actual='0.0599 MM'",
                          "polluted_grid_artifact": {"label": "historical polluted GRID", "log_line": 110,
                                                     "value": "0.05999999999998575361814800999127328395843505859375",
                                                     "verdict": "FLAGGED"},
        },
    }
    }

    # Exact expected fractions from the reviewed fixtures.
    assert bg_m["ALL_B64_WIDTH"]["fraction"] == "2161727821137101/36028797018963968"
    assert bg_m["B64_GEOMETRY_IDEAL_WIDTH"]["fraction"] == "5277655813323/87960930222080"
    assert bg_m["GRID_NORMALIZED"]["fraction"] == "3/50"
    assert bs_m["ALL_B64_WIDTH"]["fraction"] == "2158124941434061/36028797018963968"
    assert bs_m["B64_GEOMETRY_IDEAL_WIDTH"]["fraction"] == "2634429860149/43980465111040"
    assert bs_m["GRID_NORMALIZED"]["fraction"] == "599/10000"
    assert c_models["ALL_B64_WIDTH"]["fraction"] == "2159962549216005/36028797018963968"
    assert c_models["B64_GEOMETRY_IDEAL_WIDTH"]["fraction"] == "1349976593260003/22517998136852480"
    assert c_models["GRID_NORMALIZED"]["fraction"] == "3/50"
    # Every parsed raw field must agree with the reviewed fixture spelling.
    assert bg_raw == {"sx":"300.0","sy":"460.0","ex":"302.0","ey":"460.0","cx":"301.0","cy":"460.75","cw":"False","radius":"1.25","line_y":"459.29","width":"0.15"}
    assert bs_raw == {"sx":"300.0","sy":"540.0","ex":"302.0","ey":"540.0","cx":"301.0","cy":"540.75","cw":"False","radius":"1.25","line_y":"539.2901","width":"0.15"}
    assert cg_raw == {"upper_cx":"301.00005","upper_cy":"620.12492759","lower_cx":"301.00005","lower_cy":"617.899325","upper_radius":"1.0078228540984784","lower_radius":"1.0078287320398243","upper_width":"0.15","lower_width":"0.15","upper_cw":"False","lower_cw":"True"}
    delta = "1/180143985094819840"
    assert bg_m["all_minus_ideal"] == delta and bs_m["all_minus_ideal"] == delta and c_models["all_minus_ideal"] == delta
    assert bg_m["ALL_B64_WIDTH"]["verdict"] == "FLAGGED"
    assert bg_m["B64_GEOMETRY_IDEAL_WIDTH"]["verdict"] == "FLAGGED"
    assert bg_m["GRID_NORMALIZED"]["verdict"] == "CLEAN"
    assert bs_m["ALL_B64_WIDTH"]["verdict"] == bs_m["B64_GEOMETRY_IDEAL_WIDTH"]["verdict"] == bs_m["GRID_NORMALIZED"]["verdict"] == "FLAGGED"
    assert c_models["ALL_B64_WIDTH"]["verdict"] == "FLAGGED"
    assert c_models["B64_GEOMETRY_IDEAL_WIDTH"]["verdict"] == "FLAGGED"
    assert c_models["GRID_NORMALIZED"]["verdict"] == "CLEAN"

    # Historical polluted binary64 GRID oracle: known B_GRID_EQ false positive.
    sys.path.insert(0, str(ROOT / ".artifacts" / "drc-probe"))
    import arc_oracle  # type: ignore
    polluted = arc_oracle.model_GRID((301.0, 460.75), 1.25, 459.29, .15, .15)
    result["old_model_GRID_check"] = {
        "input": "B_GRID_EQ logged geometry",
        "value_decimal100": str(polluted),
        "verdict": arc_oracle.verdict(polluted, Decimal("0.06")),
        "expected_verdict": "FLAGGED",
        "against_GRID_NORMALIZED": "CLEAN",
        "classification": "false_positive",
    }
    assert result["old_model_GRID_check"]["verdict"] == "FLAGGED"
    assert result["old_model_GRID_check"]["verdict"] != bg_m["GRID_NORMALIZED"]["verdict"]

    # Specialized finite-extrema checks only; no generic finite-arc kernel claim.
    assert bg_raw["cw"] == bs_raw["cw"] == "False"
    assert cg_raw["upper_cw"] == "False" and cg_raw["lower_cw"] == "True"
    assert bg["C"][0] > bg["S"][0] and bg["C"][0] < bg["E"][0]
    assert bg["C"][1] - bg["radius"] < bg["S"][1]
    assert cg["upper_C"][0] > b64("300.0") and cg["upper_C"][0] < b64("302.0001")
    assert cg["lower_C"][0] > b64("300.0") and cg["lower_C"][0] < b64("302.0001")
    result["finite_extrema_checks"] = {
        "B_GRID_EQ": "bottom radial extremum (270deg) has x inside finite chord/line span",
        "C_CC_GOLD": "upper cw=False bottom (270deg) and lower cw=True top (90deg) extrema have x inside finite chord span",
        "scope": "specialized coordinate/sign inequalities only",
    }

    result["status"] = "OFFLINE_REGRESSIONS_PASS"
    run_dir = RUN_ROOT / f"run-{time.time_ns()}"
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    result["run_dir"] = run_dir.as_posix()
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    (run_dir / "oracle_regression.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": OUT.as_posix(), "run_dir": run_dir.as_posix()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

