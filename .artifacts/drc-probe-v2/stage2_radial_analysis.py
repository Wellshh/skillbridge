"""Offline derivation for the accepted II-B radial probe; never writes raw runs."""
from __future__ import annotations
from decimal import Decimal, localcontext
from fractions import Fraction
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "results" / "stage2-radial" / "run-20260912-224358-093" / "manifest.json"
OUT = ROOT / "results" / "stage2-radial-analysis-v4"
NOMINAL_VIA_LINE = Fraction(65, 1000)

def fwire(row: dict) -> Fraction:
    return Fraction.from_float(float(row["value"]))

def dec(q: Fraction) -> Decimal:
    return Decimal(q.numerator) / Decimal(q.denominator)

def dfloat(x: Decimal) -> float:
    return float(x)

def marker_has_target(marker: dict, kind: str, net: str, layer: str, target: tuple[float, float]) -> bool:
    for fig in marker["data"].get("figures") or []:
        if fig.get("obj_type") != kind or (kind != "via" and fig.get("layer") != layer): continue
        if (fig.get("net") or {}).get("name") != net: continue
        if kind == "via":
            loc = fig.get("location") or {}
            if abs(float(loc.get("x", {}).get("value")) - target[0]) < 1e-12 and abs(float(loc.get("y", {}).get("value")) - target[1]) < 1e-12: return True
        else:
            st, en = fig.get("start") or {}, fig.get("end") or {}
            a = (float(st.get("x", {}).get("value")), float(st.get("y", {}).get("value")))
            b = (float(en.get("x", {}).get("value")), float(en.get("y", {}).get("value")))
            if a == target[0] and b == target[1] or a == target[1] and b == target[0]: return True
    return False

def analyze(case: dict) -> dict:
    arc = next(o["dto"] for o in case["objects"] if o["name"] == "arcA")
    via = next(o["dto"] for o in case["objects"] if o["name"] == "viaB")
    pad = case["target_pad_1"]["value"]["pad"]
    c = arc["center"]; v = [via["x"], via["y"]]
    cx, cy = fwire(c[0]), fwire(c[1]); vx, vy = fwire(v[0]), fwire(v[1])
    radius, width = fwire(arc["radius"]), fwire(arc["width"])
    pad_r = (fwire(pad["bBox"][1]["x"]) - fwire(pad["bBox"][0]["x"])) / 2
    dx, dy = vx - cx, vy - cy
    with localcontext() as ctx:
        ctx.prec = 100
        d = (dec(dx * dx + dy * dy)).sqrt()
        radial = d - dec(radius) - dec(pad_r) - dec(width) / 2
        y_arc = dec(cy) + (dec(radius * radius - dx * dx)).sqrt()
        vertical_at_x = abs(dec(vy) - y_arc) - dec(pad_r) - dec(width) / 2
        vertical_extremum = abs(dec(vy - cy)) - dec(radius) - dec(pad_r) - dec(width) / 2
        api_q = fwire(case["settings"]["spacing_via_line"]["value"])
        expected = "FLAGGED" if radial < dec(api_q) else "CLEAN"
        arc_markers = [m for m in case["drc"]["arc_1"]["value"]["markers"] if m["data"]["name"] == "Line to Thru Via Spacing" and marker_has_target(m, "arc", "NFC_SWP", "ETCH/TOP", ((float(arc["start"][0]["value"]), float(arc["start"][1]["value"])), (float(arc["end"][0]["value"]), float(arc["end"][1]["value"]))))]
        via_markers = [m for m in case["drc"]["target_via_1"]["value"]["markers"] if m["data"]["name"] == "Line to Thru Via Spacing" and marker_has_target(m, "via", "FINGER_SPI_MISO", "ETCH/TOP", (float(v[0]["value"]), float(v[1]["value"])))]
        observed_arc = bool(arc_markers); observed_via = bool(via_markers)
        return {"label": case["label"], "input_bits": {"x": str(v[0]["bits"]), "y": str(v[1]["bits"])},
            "exact_input_fraction": {"dx": str(dx), "dy": str(dy)},
            "decimal100": {"center_distance": format(d, "f"), "radial_gap": format(radial, "f"),
                            "vertical_at_x_gap": format(vertical_at_x, "f"), "vertical_extremum_gap": format(vertical_extremum, "f")},
            "model_prediction": {"threshold_api_b64": format(dec(api_q), "f"), "threshold_nominal": format(dec(NOMINAL_VIA_LINE), "f"), "radial": expected,
                                 "vertical_at_x": "FLAGGED" if vertical_at_x < dec(api_q) else "CLEAN",
                                 "vertical_extremum": "FLAGGED" if vertical_extremum < dec(api_q) else "CLEAN"},
            "observed": {"arc_flagged": observed_arc, "target_via_flagged": observed_via,
                         "arc_count": case["drc"]["arc_1"]["value"]["count"], "target_via_count": case["drc"]["target_via_1"]["value"]["count"],
                         "arc_markers": [m["data"]["name"] for m in arc_markers],
                         "target_via_markers": [m["data"]["name"] for m in via_markers]},
            "raw_source": str(RAW)}

def main() -> None:
    manifest = json.loads(RAW.read_text(encoding="utf-8")); rows = [analyze(c) for c in manifest["cases"]]
    OUT.mkdir(parents=True, exist_ok=False)
    result = {"source_manifest": str(RAW), "raw_status": manifest["status"], "case_count": len(rows), "cases": rows,
              "audit_conclusion": {"observed_arc_pattern": [r["observed"]["arc_flagged"] for r in rows],
                "observed_target_via_pattern": [r["observed"]["target_via_flagged"] for r in rows],
                "radial_model_matches_observation": all(r["observed"]["arc_flagged"] == (r["model_prediction"]["radial"] == "FLAGGED") for r in rows),
                "vertical_at_x_rejected": [r["observed"]["arc_flagged"] != (r["model_prediction"]["vertical_at_x"] == "FLAGGED") for r in rows],
                "vertical_extremum_rejected": [r["observed"]["arc_flagged"] != (r["model_prediction"]["vertical_extremum"] == "FLAGGED") for r in rows]}}
    (OUT / "analysis.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"out": str(OUT / "analysis.json"), "case_count": len(rows)}))

if __name__ == "__main__": main()
