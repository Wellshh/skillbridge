"""Offline finite-arc analysis for the accepted Stage-II raw runs."""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "results" / "stage2-sweep" / "run-54268-1789223811387679300" / "manifest.json"
DIAG = ROOT / "results" / "stage2-sweep-diag" / "run-63160-1789225091207869200" / "manifest.json"
OUT = ROOT / "results" / "stage2-analysis"

def marker_summary(case):
    # Preserve only target identity fields; the complete raw marker remains in its run.
    out = []
    for key in ("snapshot_before", "snapshot_after"):
        v = case["drc"].get(key, {}).get("value", {})
        for m in v.get("markers", []) or []:
            d = m.get("data") or {}
            if d.get("name") == "Line to Line Spacing":
                figs = d.get("figures") or []
                nets = sorted({(f.get("net") or {}).get("name") for f in figs if f.get("net")})
                if "NFC_SWP" in nets or "FINGER_SPI_MISO" in nets:
                    out.append({"phase": key, "name": d.get("name"), "category": d.get("category"), "figures_nets": nets, "figures": len(figs)})
    return out

def main():
    raw = json.loads(RUN.read_text())
    diag = json.loads(DIAG.read_text())
    cases = {c["label"]: c for c in raw["cases"]}
    cases["ccw_lower_diag"] = diag["cases"][0]
    cx, cy, r = 305.0, 403.75, 6.25
    a0 = math.degrees(math.atan2(400.0-cy, 300.0-cx)) % 360
    a1 = math.degrees(math.atan2(400.0-cy, 310.0-cx)) % 360
    ccw = (a1-a0) % 360
    cw = 360.0-ccw
    # For the horizontal finite line x in [295,315], both extrema x=305 are in range.
    rows=[]
    for label,y,clockwise in (("ccw_lower",397.3,False),("ccw_upper",410.2,False),("cw_lower",397.3,True),("cw_upper",410.2,True)):
        # CCW minor has its interior radial extremum at y=cy-r; CW major at
        # y=cy+r.  The opposite finite-sweep nearest point is an endpoint,
        # y=400, rather than the opposite infinite-circle extremum.
        radial = abs(y-(cy-r)) if not clockwise else abs(y-(cy+r))
        endpoint = abs(y-400.0)
        near = radial if ((not clockwise and y < 400.0) or (clockwise and y > 400.0)) else endpoint
        far = endpoint if near == radial else radial
        rows.append({"case":label,"clockwise":clockwise,"line_y":y,"arc_radius":r,"centerline_near_gap":near,"copper_near_gap":near-0.15,"copper_far_gap":far-0.15,"sweep_deg":cw if clockwise else ccw,"extremum_x":305.0,"line_x_range":[295.0,315.0],"extremum_in_finite_line":True,"marker_summary":marker_summary(cases[label])})
    result={"sources":{"stage2":str(RUN),"diag":str(DIAG),"oracle":str(ROOT/"oracle_regression.json")},"arc":{"center":[cx,cy],"radius":r,"start":[300.0,400.0],"end":[310.0,400.0],"ccw_minor_deg":ccw,"cw_major_deg":cw},"rows":rows,"interpretation":{"finite_arc_only":True,"fullcircle_gap":0.05,"expected_pattern":"ccw_lower FLAGGED, ccw_upper CLEAN; cw_lower CLEAN, cw_upper FLAGGED","coverage_note":"run54268 clean cases and positive cw_upper plus run63160 ccw_lower; run63160 fresh path is stable but does not causally repair the old duplicate/null anomaly"}}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"stage2_sweep_analysis.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"rows":len(rows),"out":str(OUT/"stage2_sweep_analysis.json")}))
if __name__ == "__main__": main()
