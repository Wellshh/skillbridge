"""Read-only same-process axlOpenDesignForBatch/requery smoke."""
from __future__ import annotations

import hashlib
import json
import os
import socket
from collections import Counter
from pathlib import Path
from shutil import copy2
from typing import Any

from allegrobridge import Allegro, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "reopen-smoke"


def scalar(v: Any) -> Any:
    if isinstance(v, (str, int, bool)) or v is None:
        return v
    if isinstance(v, float):
        return {"value": v, "hex": v.hex()}
    return repr(v)


def pt(v: Any) -> list[Any] | None:
    if v is None:
        return None
    if hasattr(v, "x"):
        return [scalar(float(v.x)), scalar(float(v.y))]
    return [scalar(float(v[0])), scalar(float(v[1]))]


def snapshot(session: Any) -> dict[str, Any]:
    routes = []
    for r in session.routes(layer="ETCH/TOP"):
        routes.append({"obj_type": r.obj_type, "net": r.net, "layer": r.layer,
                       "start": pt(r.start), "end": pt(r.end),
                       "width": scalar(float(r.width)), "length": scalar(float(r.length)),
                       "radius": None if r.radius is None else scalar(float(r.radius)),
                       "clockwise": r.is_clockwise,
                       "center": pt(r.center) if r.center is not None else None})
    vias = []
    for v in session.vias(layer="ETCH/TOP"):
        vias.append({"x": scalar(float(v.x)), "y": scalar(float(v.y)), "net": v.net,
                     "padstack": v.padstack, "rotation": scalar(float(v.rotation)),
                     "mirroring": v.mirroring, "start_layer": v.start_layer,
                     "end_layer": v.end_layer})
    routes.sort(key=lambda x: json.dumps(x, sort_keys=True))
    vias.sort(key=lambda x: json.dumps(x, sort_keys=True))
    body = {"routes": routes, "vias": vias}
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return {"routes_count": len(routes), "vias_count": len(vias),
            "fingerprint_sha256": hashlib.sha256(encoded).hexdigest()}


def main() -> int:
    os.environ.setdefault("CDSROOT", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("Sigrity_EDA_DIR", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("CDS_LIC_FILE", "5280@localhost")
    source = ASSETS_DIR / "route" / "EL5_MIAN_FPC.brd"
    OUT.mkdir(parents=True, exist_ok=True)
    run = OUT / f"run-{os.getpid()}-{time_ns()}"
    run.mkdir()
    work = run / "work"
    work.mkdir()
    board = Path(copy2(source, work))
    with socket.socket() as listener:
        listener.bind(("localhost", 0))
        port = str(listener.getsockname()[1])
    os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"] = str(work)
    report: dict[str, Any] = {"status": "INCOMPLETE", "phase": "reopen-smoke",
                              "run_dir": str(run), "board": str(board), "port": port,
                              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                              "reopen_api": "axlOpenDesignForBatch(board, 'wf')"}
    try:
        with Allegro.open(mode="cli", board=board, workspace_id=port, timeout=300.0) as opened:
            ws, session = opened.workspace, opened.session
            report["pid"] = opened._runtime.process.pid
            report["version"] = ws["axlVersion"](Symbol("fullVersion"))
            report["initial"] = snapshot(session)
            padstack = Counter(v.padstack for v in session.vias()).most_common(1)[0][0]
            report["padstack"] = padstack
            report["write_reset_rounds"] = []
            for i, xy in enumerate(((-620.0, -70.0), (-618.0, -70.0)), 1):
                created = session.vias.create(padstack, at=xy, net="NFC_SWP")
                changed = snapshot(session)
                if changed == report["initial"]:
                    raise RuntimeError(f"round {i}: create did not change fingerprint")
                result = ws["axlOpenDesignForBatch"](board.resolve().as_posix(), "wf")
                session.refresh()
                current = snapshot(session)
                report["write_reset_rounds"].append({"index": i, "requested_xy": list(xy),
                                                     "create_return": created.model_dump(mode="json") if hasattr(created, "model_dump") else repr(created),
                                                     "changed": changed,
                                                     "raw_reopen_return": result,
                                                     "restored": current == report["initial"],
                                                     "after_reopen": current})
            report["status"] = "PASS" if all(x["restored"] and x["changed"] != report["initial"] for x in report["write_reset_rounds"]) else "FAILED"
    except Exception as exc:
        report["status"] = "FAILED"
        report["error"] = repr(exc)
    report["board_hash_after"] = hashlib.sha256(board.read_bytes()).hexdigest()
    report["owned_process_poll_after_context"] = opened._runtime.process.poll() if "opened" in locals() else None
    (run / "report.json").write_text(json.dumps(report, indent=2, default=repr), encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(run / "report.json"), "pid": report.get("pid"), "port": port}, indent=2))
    return 0 if report["status"] == "PASS" else 1


def time_ns() -> int:
    import time
    return time.time_ns()


if __name__ == "__main__":
    raise SystemExit(main())
