"""Stage I three-case wire/commit/requery smoke.

The parent process only forks one child per case.  Each child owns a disposable
board copy and Allegro process.  No DRC call is made here: this stage measures
the create/serialization boundary only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import struct
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path
from shutil import copy2
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "stage1-smoke"
CASES = ("line", "via", "arc")
LAYER = "ETCH/TOP"
NET = "NFC_SWP"
WIDTH = 0.15


def bits(value: float) -> str:
    return struct.pack(">d", float(value)).hex()


def wire(value: Any) -> dict[str, str]:
    value = float(value)
    return {"%.17g": format(value, ".17g"), "bits": bits(value)}


def point(value: Any) -> tuple[float, float]:
    if hasattr(value, "location"):
        value = value.location
    return (float(value.x), float(value.y)) if hasattr(value, "x") else (float(value[0]), float(value[1]))


def jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return jsonable(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, float):
        return {"value": value, **wire(value)}
    return value


def field(value: Any, name: str) -> Any:
    if isinstance(value, dict):
        return value[name]
    if isinstance(value, list):
        return value[value.index(name) + 1]
    raise TypeError(f"expected returned alist/dict, got {type(value).__name__}")


def extent_box(value: Any) -> tuple[tuple[float, float], tuple[float, float]]:
    box = field(value, "bBox")
    if not box or len(box) != 2:
        raise RuntimeError("paramDesign bBox missing")
    ll, ur = point(box[0]), point(box[1])
    if ur[0] <= ll[0] or ur[1] <= ll[1]:
        raise RuntimeError(f"invalid paramDesign bBox: {box!r}")
    return ll, ur


def route_key(row: Any) -> tuple[Any, ...]:
    start, end = point(row.start), point(row.end)
    center = point(row.center) if getattr(row, "center", None) is not None else None
    return (row.obj_type, row.net, row.layer, start, end, float(row.width), center,
            None if row.radius is None else float(row.radius))


def alist_point(value: Any) -> tuple[float, float]:
    return (float(field(value, "x")), float(field(value, "y")))


def assert_requery_bits(case: str, committed: Any, row: Any) -> None:
    native = field(committed, "committed")
    if case == "via":
        expected = (float(field(native, "x")), float(field(native, "y")))
        for name in ("x", "y"):
            if bits(float(field(native, f"{name}17"))) != bits(float(field(native, name))):
                raise RuntimeError(f"native {name}17 does not round-trip")
        actual = point(row)
        if tuple(bits(v) for v in actual) != tuple(bits(v) for v in expected):
            raise RuntimeError(f"via requery bits differ: expected={expected!r} actual={actual!r}")
        if (row.padstack != field(native, "padstack") or row.net != field(native, "net")
                or row.start_layer != field(native, "start_layer")
                or row.end_layer != field(native, "end_layer")
                or row.mirroring != field(native, "mirroring")):
            raise RuntimeError("via non-coordinate fields differ")
        return
    for label, expected, actual in (("start", alist_point(field(native, "start")), point(row.start)),
                                    ("end", alist_point(field(native, "end")), point(row.end))):
        raw_point = field(native, label)
        for name in ("x", "y"):
            if bits(float(field(raw_point, f"{name}17"))) != bits(float(field(raw_point, name))):
                raise RuntimeError(f"native {label}.{name}17 does not round-trip")
        if tuple(bits(v) for v in actual) != tuple(bits(v) for v in expected):
            raise RuntimeError(f"{label} requery bits differ: expected={expected!r} actual={actual!r}")
    if bits(float(row.width)) != bits(float(field(native, "width"))):
        raise RuntimeError("width requery bits differ")
    if bits(float(field(native, "width17"))) != bits(float(field(native, "width"))):
        raise RuntimeError("native width17 does not round-trip")
    if bits(float(row.length)) != bits(float(field(native, "length"))):
        raise RuntimeError("length requery bits differ")
    if row.layer != field(native, "layer") or row.obj_type != field(native, "objType"):
        raise RuntimeError("route layer/obj_type requery differs")
    if row.net != field(native, "net"):
        raise RuntimeError(f"route net requery differs: {row.net!r} != {field(native, 'net')!r}")
    if row.is_clockwise != field(native, "clockwise"):
        raise RuntimeError("direction requery differs")
    if case == "arc":
        center = field(native, "center")
        for name in ("x", "y"):
            if bits(float(field(center, f"{name}17"))) != bits(float(field(center, name))):
                raise RuntimeError(f"native center.{name}17 does not round-trip")
        if tuple(bits(v) for v in point(row.center)) != tuple(bits(v) for v in alist_point(center)):
            raise RuntimeError("center requery bits differ")
        if bits(float(row.radius)) != bits(float(field(native, "radius"))):
            raise RuntimeError("radius requery bits differ")
        if bits(float(field(native, "radius17"))) != bits(float(field(native, "radius"))):
            raise RuntimeError("native radius17 does not round-trip")


def choose_padstack(session: Any) -> str:
    vias = session.vias()
    if not vias:
        raise RuntimeError("no existing via padstack available on source board")
    return Counter(v.padstack for v in vias).most_common(1)[0][0]


def skill_string(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def assert_request_wire(command: str, inputs: dict[str, Any]) -> None:
    for pair in (inputs["start"], inputs.get("end") or [], inputs.get("center") or [], [inputs["width"]]):
        for value in pair:
            if value["%.17g"] not in command:
                raise RuntimeError(f"request wire missing {value['%.17g']}")


def child(case: str, run_dir: Path) -> dict[str, Any]:
    source = ASSETS_DIR / "route" / "EL5_MIAN_FPC.brd"
    work = run_dir / "work"
    work.mkdir(parents=True, exist_ok=False)
    board = Path(copy2(source, work))
    with socket.socket() as listener:
        listener.bind(("localhost", 0))
        port = str(listener.getsockname()[1])
    os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"] = str(work)
    helper = run_dir / "stage1_smoke.il"
    report: dict[str, Any] = {
        "case": case, "port": port, "board": str(board),
        "board_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "helper_sha256": hashlib.sha256(helper.read_bytes()).hexdigest(),
        "purpose": "ordinary in-bounds coordinate serialization smoke; no DRC or rule assertion",
        "status": "FAILED",
    }
    report["git_head"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT.parent.parent,
                                        capture_output=True, text=True, check=False).stdout.strip()
    report["git_dirty"] = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT.parent.parent,
                                               capture_output=True, text=True, check=False).stdout.strip())
    with Allegro.open(mode="cli", board=board, workspace_id=port, timeout=300.0) as opened:
        ws, session = opened.workspace, opened.session
        report["pid"] = opened._runtime.process.pid
        report["allegro_version"] = jsonable(ws["axlVersion"](Symbol("fullVersion")))
        report["units_accuracy"] = jsonable(ws["axlDBGetDesignUnits"]())
        loaded = ws["load"](helper.resolve().as_posix())
        report["helper_load"] = jsonable(loaded)
        pre_extent = ws["__v2DesignExtent"]()
        report["pre_extent"] = jsonable(pre_extent)
        ll, ur = extent_box(pre_extent)
        padstack = choose_padstack(session)
        x = ll[0] + (ur[0] - ll[0]) * 0.45
        y = ll[1] + (ur[1] - ll[1]) * 0.45
        x = round(x, 5)
        y = round(y, 5)
        report["geometry_bounds"] = {"start_in_extent": ll[0] <= x <= ur[0] and ll[1] <= y <= ur[1],
                                     "end_in_extent": None, "center_in_extent": None}
        before_routes = session.routes(net=None, layer=LAYER)
        before_vias = session.vias(net=None, layer=LAYER)
        if case == "via":
            command = (f'__v2Stage1Create(\'via {skill_string(NET)} '
                       f'{skill_string(LAYER)} {skill_string(padstack)} '
                       f'{x:.17g}:{y:.17g} nil {WIDTH:.17g} nil nil)')
        else:
            kind = "arc" if case == "arc" else "line"
            end = (x + 2.0, y + (1.0 if case == "arc" else 0.0))
            center = (x + 1.0, y + 0.75) if case == "arc" else None
            report["geometry_bounds"]["end_in_extent"] = ll[0] <= end[0] <= ur[0] and ll[1] <= end[1] <= ur[1]
            report["geometry_bounds"]["center_in_extent"] = (center is None or
                (ll[0] <= center[0] <= ur[0] and ll[1] <= center[1] <= ur[1]))
            center_expr = f"{center[0]:.17g}:{center[1]:.17g}" if center else "nil"
            command = (f'__v2Stage1Create(\'{kind} {skill_string(NET)} '
                       f'{skill_string(LAYER)} nil {x:.17g}:{y:.17g} '
                       f'{end[0]:.17g}:{end[1]:.17g} {WIDTH:.17g} '
                       f'nil {center_expr})')
        request_inputs = {"start": [wire(x), wire(y)], "end": [wire(end[0]), wire(end[1])] if case != "via" else None,
                                     "width": wire(WIDTH), "center": [wire(v) for v in center] if case == "arc" else None,
                                     "clockwise": False if case == "arc" else None, "net": NET, "layer": LAYER}
        report["request_inputs"] = request_inputs
        report["skill_request_text"] = command
        assert_request_wire(command, request_inputs)
        committed = ws.transaction(SkillCode(command))
        report["transaction_return"] = jsonable(committed)
        if case == "via":
            rows = session.vias(net=None, layer=LAYER, padstack=padstack)
            before_locations = {point(r) for r in before_vias if r.padstack == padstack}
            native = field(committed, "committed")
            expected = (float(field(native, "x")), float(field(native, "y")))
            matched = [r for r in rows if point(r) == expected and point(r) not in before_locations]
            if len(matched) != 1:
                raise RuntimeError(f"via requery expected one exact row, got {len(matched)} of {len(rows)}")
            report["requery"] = jsonable(matched[0])
            assert_requery_bits(case, committed, matched[0])
        else:
            rows = session.routes(net=None, layer=LAYER)
            result = field(committed, "committed")
            cstart, cend = field(result, "start"), field(result, "end")
            before_route_keys = {route_key(r) for r in before_routes}
            expected_start, expected_end = alist_point(cstart), alist_point(cend)
            candidates = [r for r in rows if r.obj_type == case and route_key(r) not in before_route_keys
                          and point(r.start) == expected_start and point(r.end) == expected_end
                          and float(r.width) == WIDTH]
            if case == "arc":
                cc = field(result, "center")
                expected_center = alist_point(cc)
                candidates = [r for r in candidates if point(r.center) == expected_center]
            if len(candidates) != 1:
                raise RuntimeError(f"route requery expected one exact {case}, got {len(candidates)} of {len(rows)}")
            report["requery"] = jsonable(candidates[0])
            assert_requery_bits(case, committed, candidates[0])
        report["requery_count"] = len(rows)
        report["status"] = "PASS"
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES)
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    if args.case:
        if args.run_dir is None:
            raise SystemExit("--run-dir is required for a child")
        try:
            print(json.dumps(child(args.case, args.run_dir), default=str), flush=True)
            return 0
        except Exception as exc:
            print(json.dumps({"case": args.case, "status": "FAILED", "error": repr(exc),
                              "traceback": traceback.format_exc(), "pid": os.getpid(),
                              "cleanup": "context_manager_or_partial_startup"}), flush=True)
            return 1
    RESULTS.mkdir(parents=True, exist_ok=True)
    manifest = {"status": "PENDING_RUNTIME", "cases": list(CASES), "runs": []}
    for case in CASES:
        run_dir = RESULTS / f"{case}-{os.getpid()}-{len(manifest['runs'])}"
        run_dir.mkdir()
        (run_dir / "stage1_smoke.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")
        (run_dir / "stage1_smoke.il").write_text((ROOT / "stage1_smoke.il").read_text(encoding="utf-8"), encoding="utf-8")
        cmd = [sys.executable, str((run_dir / "stage1_smoke.py").resolve()), "--case", case, "--run-dir", str(run_dir)]
        env = os.environ.copy()
        repo_root = ROOT.parent.parent
        env["PYTHONPATH"] = str(repo_root) + os.pathsep + env.get("PYTHONPATH", "")
        completed = subprocess.run(cmd, cwd=run_dir, env=env, capture_output=True, text=True, check=False)
        (run_dir / "stdout.log").write_text(completed.stdout, encoding="utf-8")
        (run_dir / "stderr.log").write_text(completed.stderr, encoding="utf-8")
        try:
            child_result = json.loads(completed.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            child_result = {"status": "NO_JSON_RESULT"}
        (run_dir / "case.json").write_text(json.dumps(child_result, indent=2), encoding="utf-8")
        manifest["runs"].append({"case": case, "run_dir": str(run_dir), "returncode": completed.returncode,
                                  "cleanup": "child_context_exit_attempted"})
        if completed.returncode:
            manifest["status"] = "FAILED_RUNTIME"
            break
    (RESULTS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if len(manifest["runs"]) == len(CASES) and all(r["returncode"] == 0 for r in manifest["runs"]):
        manifest["status"] = "RUNTIME_PENDING_ALL_CASES"
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
