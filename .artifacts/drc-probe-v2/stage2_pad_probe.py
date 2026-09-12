"""One-via Stage II-B pad geometry probe; source only until reviewed."""
from __future__ import annotations

import argparse, hashlib, json, os, socket, struct, subprocess, sys, time
from pathlib import Path
from shutil import copy2
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT = Path(__file__).resolve().parent
VERIFIED = ROOT / "results" / "stage0-gate" / "run-37248-1789193361092813400"
LAYER = "ETCH/TOP"
NET = "NFC_SWP"
XY = (300.0, 400.0)
PADSTACK = "VIA_ALL_0103"

def bits(x: Any) -> str:
    return struct.pack(">d", float(x)).hex()

def wire(x: Any) -> dict[str, str]:
    f = float(x); s = format(f, ".17g")
    if all(c not in s for c in ".eE"): s += ".0"
    return {"%.17g": s, "bits": bits(f)}

def skill_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def skill_num(x: Any) -> str:
    s = format(float(x), ".17g")
    return s if any(c in s for c in ".eE") else s + ".0"

def jsonable(x: Any) -> Any:
    if hasattr(x, "model_dump"): return jsonable(x.model_dump(mode="python"))
    if isinstance(x, dict): return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, float): return {"value": x, **wire(x)}
    return x

def field(x: Any, name: str) -> Any:
    if isinstance(x, dict): return x[name]
    if isinstance(x, list): return x[x.index(name) + 1]
    raise TypeError(f"expected alist/dict, got {type(x).__name__}")

def raw_probe(ws: Any, padstack: str, xy: tuple[float, float]) -> Any:
    return ws["__v2PadProbeFind"](padstack, NET, xy[0], xy[1])

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--run-dir", type=Path, required=True)
    a = ap.parse_args(); run = a.run_dir.resolve(); run.mkdir(parents=True, exist_ok=False)
    os.chdir(run)
    source = ASSETS_DIR / "route" / "EL5_MIAN_FPC.brd"; board = run / "work" / source.name
    (run / "work").mkdir(); copy2(source, board)
    helper = run / "stage1_smoke.il"; helper_py = run / "stage1_smoke.py"; pad_il = run / "stage2_pad_probe.il"
    copy2(VERIFIED / "stage1_smoke.il", helper); copy2(VERIFIED / "stage1_smoke.py", helper_py)
    copy2(ROOT / "stage2_pad_probe.il", pad_il); copy2(Path(__file__).resolve(), run / "stage2_pad_probe.py")
    report: dict[str, Any] = {"status": "FAILED", "purpose": "VIA_ALL_0103 TOP REGULAR pad geometry",
        "net": NET, "layer": LAYER, "requested_xy": [wire(x) for x in XY],
        "padstack": PADSTACK, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "helper_sha256": hashlib.sha256(helper.read_bytes()).hexdigest(),
        "pad_probe_sha256": hashlib.sha256(pad_il.read_bytes()).hexdigest()}
    report["argv"] = sys.argv; report["cwd"] = str(run)
    with socket.socket() as s:
        s.bind(("localhost", 0)); port = str(s.getsockname()[1])
    report["port"] = port
    os.environ.setdefault("CDSROOT", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("Sigrity_EDA_DIR", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("CDS_LIC_FILE", "5280@localhost")
    os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"] = str(run / "bridge-logs")
    (run / "bridge-logs").mkdir()
    owned = None
    try:
        with Allegro.open(mode="cli", board=board, workspace_id=port, timeout=300.0) as opened:
            owned = opened._runtime.process; ws, session = opened.workspace, opened.session
            report["pid"] = owned.pid; report["version"] = jsonable(ws["axlVersion"](Symbol("fullVersion")))
            report["units_accuracy"] = jsonable(ws["axlDBGetDesignUnits"]())
            report["helper_load"] = jsonable(ws["load"](helper.resolve().as_posix()))
            report["pad_probe_load"] = jsonable(ws["load"](pad_il.resolve().as_posix()))
            command = ("__v2Stage1Create('via " + skill_string(NET) + " " + skill_string(LAYER) + " "
                       + skill_string(PADSTACK) + " " + skill_num(XY[0]) + ":" + skill_num(XY[1])
                       + " nil 0.15 nil nil)")
            report["request"] = {"command": command, "xy": [wire(x) for x in XY], "net": NET,
                                 "layer": LAYER, "padstack": PADSTACK, "rotation": 0, "mirroring": "unmirrored"}
            committed = ws.transaction(SkillCode(command)); report["transaction_return"] = jsonable(committed)
            report["request_echo"] = jsonable(field(committed, "request"))
            import importlib.util
            spec = importlib.util.spec_from_file_location("stage1_smoke_snapshot", helper_py)
            smoke = importlib.util.module_from_spec(spec); assert spec and spec.loader
            spec.loader.exec_module(smoke)
            inputs = {"start": [wire(XY[0]), wire(XY[1])], "end": None,
                      "width": wire(0.15), "center": None, "clockwise": None,
                      "net": NET, "layer": LAYER}
            smoke.assert_echo_inputs("via", committed, inputs)
            native = field(committed, "committed")
            actual_xy = (float(field(native, "x")), float(field(native, "y")))
            rows = [v for v in session.vias(net=None, layer=LAYER, padstack=PADSTACK)
                    if v.net == NET and v.padstack == PADSTACK
                    and tuple(smoke.bits(z) for z in smoke.point(v)) == tuple(smoke.bits(z) for z in actual_xy)]
            if len(rows) != 1: raise RuntimeError(f"unique via DTO match failed: {len(rows)}")
            report["dto_requery"] = jsonable(rows[0]); smoke.assert_requery_bits("via", committed, rows[0])
            session.refresh(); first = raw_probe(ws, PADSTACK, actual_xy)
            session.refresh(); second = raw_probe(ws, PADSTACK, actual_xy)
            if first is None or second is None: raise RuntimeError("pad probe returned nil")
            for key in ("via", "pad", "viaPolys"):
                if field(first, key) is None: raise RuntimeError(f"pad probe missing {key}")
            report["pad_probe_1"] = jsonable(first); report["pad_probe_2"] = jsonable(second)
            if jsonable(first) != jsonable(second): raise RuntimeError("independent pad getter values differ")
            report["status"] = "PASS"
    except Exception as exc:
        report["error"] = repr(exc); report["traceback"] = __import__("traceback").format_exc()
        return_code = 1
    else:
        return_code = 0
    report["owned_process_poll_after_context"] = None if owned is None else owned.poll()
    (run / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return return_code

if __name__ == "__main__": raise SystemExit(main())
