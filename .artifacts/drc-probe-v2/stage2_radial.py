"""II-B four-case radial/vertical discrimination probe; one fresh board per case."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, os, socket, struct, sys, time, traceback
from pathlib import Path
from shutil import copy2
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT = Path(__file__).resolve().parent
SRC = ASSETS_DIR / "route" / "EL5_MIAN_FPC.brd"
SNAP = ROOT / "results" / "stage0-gate" / "run-37248-1789193361092813400"
PAD_SNAP = ROOT / "results" / "stage2-pad-probe" / "run-20260912-222619-975"
LAYER, NET_A, NET_B, PAD, W = "ETCH/TOP", "NFC_SWP", "FINGER_SPI_MISO", "VIA_ALL_0103", 0.15
CASES = (("gap004_a", 306.159, 408.212, 0.04), ("gap004_b", 308.212, 406.159, 0.04),
         ("gap020_a", 306.255, 408.340, 0.20), ("gap020_b", 308.340, 406.255, 0.20))
# II-B quarter arc: center, start, end are intentionally distinct from II-A.
C, S, E = (300.0, 400.0), (310.0, 400.0), (300.0, 410.0)

def validate_geometry() -> None:
    for label, x, y, gap in CASES:
        distance = math.hypot(x - C[0], y - C[1])
        angle = math.degrees(math.atan2(y - C[1], x - C[0]))
        expected = 10.0 + 0.15 + 0.075 + gap
        if not (0.0 <= angle <= 90.0) or abs(distance - expected) > 2e-3:
            raise AssertionError(f"{label}: quarter-span/radial distance mismatch")

def bits(x: Any) -> str: return struct.pack(">d", float(x)).hex()
def wire(x: Any) -> dict[str, Any]:
    f = float(x); s = format(f, ".17g")
    return {"value": f, "%.17g": s if any(c in s for c in ".eE") else s + ".0", "bits": bits(f)}
def sn(x: Any) -> str:
    s = format(float(x), ".17g"); return s if any(c in s for c in ".eE") else s + ".0"
def ss(x: str) -> str: return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'
def js(x: Any) -> Any:
    if hasattr(x, "model_dump"): return js(x.model_dump(mode="python"))
    if isinstance(x, dict): return {str(k): js(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [js(v) for v in x]
    if isinstance(x, float): return wire(x)
    return x
def fld(x: Any, n: str) -> Any: return x[n] if isinstance(x, dict) else x[x.index(n) + 1]
def pt(x: Any) -> tuple[float, float]: return (float(x.x), float(x.y)) if hasattr(x, "x") else (float(x[0]), float(x[1]))
def port() -> str:
    with socket.socket() as s: s.bind(("localhost", 0)); return str(s.getsockname()[1])
def via_cmd(net: str, xy: tuple[float, float]) -> str:
    return f"__v2Stage1Create('via {ss(net)} {ss(LAYER)} {ss(PAD)} {sn(xy[0])}:{sn(xy[1])} nil {sn(W)} nil nil)"
def arc_cmd(cw: bool) -> str:
    return f"__v2Stage1Create('arc {ss(NET_A)} {ss(LAYER)} nil {sn(S[0])}:{sn(S[1])} {sn(E[0])}:{sn(E[1])} {sn(W)} {'t' if cw else 'nil'} {sn(C[0])}:{sn(C[1])})"
def raw(ws: Any, name: str, *args: Any) -> dict[str, Any]:
    try: return {"ok": True, "value": js(ws[name](*args))}
    except Exception: return {"ok": False, "traceback": traceback.format_exc()}
def require_raw(record: dict[str, Any], label: str) -> Any:
    if not record.get("ok") or record.get("value") is None: raise RuntimeError(f"{label} raw call failed")
    return record["value"]

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-dir", type=Path, required=True)
    validate_geometry()
    base = ap.parse_args().run_dir.resolve(); base.mkdir(parents=True, exist_ok=False); os.chdir(base)
    source_sha = hashlib.sha256(SRC.read_bytes()).hexdigest(); snapshot = {}
    for name in ("stage1_smoke.py", "stage1_smoke.il", "stage0_gate.il", "context_probe.il"):
        src = SNAP / name; dst = base / name; copy2(src, dst); snapshot[name] = hashlib.sha256(dst.read_bytes()).hexdigest()
    copy2(PAD_SNAP / "stage2_pad_probe.il", base / "stage2_pad_probe.il")
    snapshot["stage2_pad_probe.il"] = hashlib.sha256((base / "stage2_pad_probe.il").read_bytes()).hexdigest()
    copy2(ROOT / "stage2_radial.il", base / "stage2_radial.il")
    script_copy = base / "stage2_radial.py"; copy2(Path(__file__).resolve(), script_copy)
    rep: dict[str, Any] = {"status": "RUNNING", "source_sha256": source_sha, "argv": sys.argv,
        "cwd": str(base), "script_sha256": hashlib.sha256(script_copy.read_bytes()).hexdigest(),
        "snapshots": snapshot, "cases": []}
    for label, vx, vy, gap in CASES:
        case_dir = base / label; case_dir.mkdir(); board = Path(copy2(SRC, case_dir / SRC.name)); p = port()
        os.chdir(case_dir)
        os.environ.setdefault("CDSROOT", r"D:\Cadence\Cadence_SPB_17.2-2016")
        os.environ.setdefault("Sigrity_EDA_DIR", r"D:\Cadence\Cadence_SPB_17.2-2016")
        os.environ.setdefault("CDS_LIC_FILE", "5280@localhost")
        os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"] = str(case_dir / "bridge-logs"); (case_dir / "bridge-logs").mkdir()
        distance = math.hypot(vx - C[0], vy - C[1])
        angle = math.degrees(math.atan2(vy - C[1], vx - C[0]))
        case: dict[str, Any] = {"label": label, "board_sha256": hashlib.sha256(board.read_bytes()).hexdigest(), "gap": wire(gap), "target_xy": [wire(vx), wire(vy)],
            "arc_intent": {"center": [wire(C[0]), wire(C[1])], "start": [wire(S[0]), wire(S[1])],
                           "end": [wire(E[0]), wire(E[1])], "radius": wire(10.0), "clockwise": False,
                           "width": wire(W)}, "target_geometry": {"center_distance": wire(distance), "angle_deg": wire(angle)},
            "status": "INCOMPLETE"}
        opened = None
        try:
            with Allegro.open(mode="cli", board=board, workspace_id=p, timeout=300.0) as op:
                opened = op; ws, session = op.workspace, op.session
                case["process"] = {"pid": op._runtime.process.pid, "port": p,
                    "version": js(ws["axlVersion"](Symbol("fullVersion"))), "units_accuracy": js(ws["axlDBGetDesignUnits"]())}
                for helper in ("stage1_smoke.il", "stage0_gate.il", "context_probe.il", "stage2_pad_probe.il", "stage2_radial.il"):
                    case.setdefault("loads", {})[helper] = js(ws["load"]((base / helper).resolve().as_posix()))
                session.drc()
                spec = importlib.util.spec_from_file_location("stage1_smoke_snapshot", base / "stage1_smoke.py"); smoke = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(smoke)
                case["settings"] = {"drc_enable": raw(ws, "axlDBControl", Symbol("drcEnable")),
                    "spacing_line_line": raw(ws, "axlCNSGetSpacing", "", "TOP", Symbol("line_line"), None),
                    "spacing_via_line": raw(ws, "axlCNSGetSpacing", "", "TOP", Symbol("via_line"), None),
                    "spacing_via_line_text": raw(ws, "axlCNSGetSpacing", "", "TOP", Symbol("via_line"), True),
                    "spacing_mode_all": raw(ws, "axlCNSSpacingModeGet", Symbol("all")),
                    "design_mode_all": raw(ws, "axlCNSDesignModeGet", Symbol("all")),
                    "waived_before": raw(ws, "axlDRCWaiveGetCount"), "context": raw(ws, "__v2DrcContextPure", NET_A, NET_B)}
                objects = (("viaA", via_cmd(NET_A, S), NET_A, "via", S), ("arcA", arc_cmd(False), NET_A, "arc", S),
                           ("viaB", via_cmd(NET_B, (vx, vy)), NET_B, "via", (vx, vy)))
                arc_dto = None; target_via_dto = None
                for name, command, net, kind, start in objects:
                    ret = ws.transaction(SkillCode(command)); session.refresh(); native = fld(ret, "committed")
                    inp = {"start": [wire(start[0]), wire(start[1])], "end": None, "width": wire(W), "center": None, "clockwise": None, "net": net, "layer": LAYER}
                    if kind == "arc": inp.update({"end": [wire(E[0]), wire(E[1])], "center": [wire(C[0]), wire(C[1])], "clockwise": False})
                    smoke.assert_echo_inputs(kind, ret, inp)
                    if kind == "via":
                        exp = (float(fld(native, "x")), float(fld(native, "y"))); pool = session.vias(net=None, layer=LAYER, padstack=PAD)
                        hits = [r for r in pool if r.net == net and r.padstack == PAD and tuple(bits(z) for z in pt(r)) == tuple(bits(z) for z in exp)]
                    else:
                        st, en = fld(native, "start"), fld(native, "end"); exp = ((float(fld(st, "x")), float(fld(st, "y"))), (float(fld(en, "x")), float(fld(en, "y"))))
                        hits = [r for r in session.routes(net=None, layer=LAYER) if r.net == net and r.obj_type == kind and pt(r.start) == exp[0] and pt(r.end) == exp[1]]
                    if len(hits) != 1: raise RuntimeError(f"{name} unique requery={len(hits)}")
                    smoke.assert_requery_bits(kind, ret, hits[0]); case.setdefault("objects", []).append({"name": name, "command": command, "return": js(ret), "dto": js(hits[0])})
                    if name == "arcA": arc_dto = hits[0]
                    if name == "viaB": target_via_dto = hits[0]
                actual_target_xy = pt(target_via_dto)
                case["target_pad_1"] = raw(ws, "__v2PadProbeFind", PAD, NET_B, *actual_target_xy); case["target_pad_2"] = raw(ws, "__v2PadProbeFind", PAD, NET_B, *actual_target_xy)
                pad1 = require_raw(case["target_pad_1"], "target_pad_1"); pad2 = require_raw(case["target_pad_2"], "target_pad_2")
                for key in ("via", "pad", "viaPolys"):
                    if fld(pad1, key) is None: raise RuntimeError(f"target pad missing {key}")
                if pad1 != pad2: raise RuntimeError("target pad getter differs")
                args = ("route", NET_A, None, LAYER, "arc", arc_dto.start, arc_dto.end, float(arc_dto.width), arc_dto.radius, arc_dto.is_clockwise, arc_dto.center)
                case["drc"] = {"arc_1": raw(ws, "__v2DrcItemCount", *args), "arc_2": raw(ws, "__v2DrcItemCount", *args),
                    "target_via_1": raw(ws, "__v2DrcViaItemCount", PAD, NET_B, *actual_target_xy), "target_via_2": raw(ws, "__v2DrcViaItemCount", PAD, NET_B, *actual_target_xy),
                    "snapshot_before": raw(ws, "__v2DrcSnapshot"), "update": raw(ws, "axlDRCUpdate", True), "snapshot_after": raw(ws, "__v2DrcSnapshot"),
                    "waived_after": raw(ws, "axlDRCWaiveGetCount"), "drc_enable_after": raw(ws, "axlDBControl", Symbol("drcEnable")),
                    "spacing_mode_all_after": raw(ws, "axlCNSSpacingModeGet", Symbol("all"))}
                case["status"] = "CAPTURED"
        except Exception:
            case["error"] = repr(sys.exc_info()[1]); case["traceback"] = traceback.format_exc()
        case["process_poll_after_context"] = None if opened is None else opened._runtime.process.poll(); rep["cases"].append(case)
        (case_dir / "report.json").write_text(json.dumps(case, indent=2), encoding="utf-8")
        (base / "manifest.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    rep["status"] = "CAPTURED" if len(rep["cases"]) == 4 and all(c["status"] == "CAPTURED" for c in rep["cases"]) else "INCOMPLETE"
    (base / "manifest.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return 0 if rep["status"] == "CAPTURED" else 1

if __name__ == "__main__": raise SystemExit(main())
