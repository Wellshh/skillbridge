"""Stage 0 checker gate and minimal Stage I-A matrix.

Every invocation owns a fresh board copy/process. Raw constraint calls are
diagnostic evidence only; a DEFAULT value is never treated as effective
without recording its cset/layer provenance.
"""
from __future__ import annotations

import json
import hashlib
import math
import os
import struct
from collections import Counter
from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

from allegrobridge import Allegro, Symbol
from allegrobridge.util import ASSETS_DIR

OUT = Path(__file__).with_name("results")
OUT.mkdir(exist_ok=True)
NET_A, NET_B = "NFC_SWP", "FINGER_SPI_MISO"
LAYER, WIDTH = "ETCH/TOP", 0.15


def bits(x: float) -> str:
    return struct.pack(">d", float(x)).hex()


def wire(x: float) -> str:
    return f"{float(x):.17g} bits={bits(x)}"


def evidence(value):
    if hasattr(value, "model_dump"):
        return evidence(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(k): evidence(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [evidence(v) for v in value]
    if isinstance(value, float):
        return {"value": value, "bits": bits(value), "repr": repr(value)}
    return value


def point(p):
    return [float(p.x), float(p.y)] if hasattr(p, "x") else [float(p[0]), float(p[1])]


def row(r):
    return evidence(r)


def route_row(r):
    out = {"obj_type": r.obj_type, "net": r.net, "layer": r.layer,
           "start": point(r.start), "end": point(r.end),
           "width": float(r.width.x) if hasattr(r.width, "x") else float(r.width),
           "length": float(r.length)}
    for name in ("radius", "is_clockwise", "center"):
        value = getattr(r, name, None)
        out[name] = point(value) if name == "center" and value is not None else (float(value) if name == "radius" and value is not None else value)
    return evidence(out)


def marker(m):
    # model_dump retains objects, figures, centers/radii and references; repr is
    # reserved for non-JSON values, never used as the primary evidence.
    return evidence(m.model_dump(mode="python"))


def raw(ws, name, *args):
    try:
        return {"ok": True, "value": evidence(ws[name](*args))}
    except Exception as exc:
        return {"ok": False, "error": repr(exc)}


def main():
    os.environ.setdefault("CDSROOT", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("Sigrity_EDA_DIR", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("CDS_LIC_FILE", "5280@localhost")
    work = None
    board = None
    report = {"status": "INCOMPLETE", "phase": "stage0-checker", "board": board.as_posix(),
              "wire_format": "%.17g plus binary64 hex", "cases": [], "constraint": {}}
    with socket() as listener:
        listener.bind(("localhost", 0))
        port = str(listener.getsockname()[1])
    report["port"] = port
    run_dir = OUT / f"run-{os.getpid()}-{port}"
    run_dir.mkdir(exist_ok=False)
    copy2(Path(__file__), run_dir / Path(__file__).name)
    copy2(Path(__file__).with_name("drc_gate.il"), run_dir / "drc_gate.il")
    work = run_dir / "work"
    work.mkdir()
    board = Path(copy2(ASSETS_DIR / "route" / "EL5_MIAN_FPC.brd", work))
    os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"] = work.as_posix()
    report["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report["board_source_sha256"] = hashlib.sha256((ASSETS_DIR / "route" / "EL5_MIAN_FPC.brd").read_bytes()).hexdigest()
    try:
        with Allegro.open(mode="cli", board=board, workspace_id=port, timeout=300.0) as opened:
            ws, session = opened.workspace, opened.session
            report["pid"] = opened._runtime.process.pid
            report["version"] = ws["axlVersion"](Symbol("fullVersion"))
            helper = Path(__file__).with_name("drc_gate.il")
            report["helper_sha256"] = hashlib.sha256(helper.read_bytes()).hexdigest()
            report["helper_load"] = raw(ws, "load", helper.resolve().as_posix())
            report["controls_before"] = {name: raw(ws, "axlDBControl", Symbol(name)) for name in ("drcEnable", "activeLayer")}
            report["drc_count_before"] = raw(ws, "axlDRCGetCount")
            report["waived_count_before"] = raw(ws, "axlDRCWaiveGetCount")
            report["constraint"]["domains"] = raw(ws, "axlCnsList", None)
            report["constraint"]["spacing_csets"] = raw(ws, "axlCnsList", "spacing")
            report["constraint"]["supported_spacing"] = raw(ws, "axlCNSGetSpacing", None, None, None)
            # Enumerate DEFAULT and every cset on TOP; these are candidates,
            # never silently promoted to effective target context.
            csets = [""]
            if report["constraint"]["spacing_csets"].get("ok") and isinstance(report["constraint"]["spacing_csets"]["value"], list):
                csets += [str(x) for x in report["constraint"]["spacing_csets"]["value"]]
            report["constraint"]["values"] = {c: raw(ws, "axlCNSGetSpacing", c, "TOP", None, True) for c in dict.fromkeys(csets)}
            report["board_observed"] = session.board().model_dump(mode="json")
            report["observed_units_accuracy"] = raw(ws, "axlDBGetDesignUnits")
            extent = raw(ws, "axlDBGetExtents", ws["axlDBGetDesign"](), True)
            report["observed_extents"] = extent
            report["extent_validation"] = "VALIDATED" if extent.get("ok") and extent.get("value") not in (None, [[0, 0], [0, 0]]) else "NOT_VALIDATED"
            vias = session.vias()
            padstack = Counter(v.padstack for v in vias).most_common(1)[0][0]

            # Positive control: edge spacing deliberately well below any
            # plausible rule. This establishes that item/list checking works.
            va = session.vias.create(padstack, at=(300.0, 300.0), net=NET_A)
            vb = session.vias.create(padstack, at=(302.0, 300.01 + WIDTH), net=NET_B)
            ra = session.routes.create(NET_A, [(300.0, 300.0), (302.0, 300.0)], LAYER, WIDTH)[0]
            rb = session.routes.create(NET_B, [(300.0, 300.01 + WIDTH), (302.0, 300.01 + WIDTH)], LAYER, WIDTH)[0]
            report["positive_control"] = {"via_a": evidence(va), "via_b": evidence(vb), "route_a": route_row(ra), "route_b": route_row(rb),
                                           "requested_wire": {"route_a": [wire(300.0), wire(300.0), wire(302.0), wire(300.0)],
                                                               "route_b": [wire(300.0), wire(300.01 + WIDTH), wire(302.0), wire(300.01 + WIDTH)]},
                                           "skill_pre_call_echo": "NOT_CAPTURED_BY_PUBLIC_RPC"}
            before = session.drc()
            hits1 = session.drc.check(ra)
            route_args = ("route", NET_A, None, LAYER, ra.obj_type,
                          ra.start, ra.end, ra.width, ra.radius,
                          ra.is_clockwise, ra.center)
            native1 = raw(ws, "__v2DrcItemCount", *route_args)
            hits2 = session.drc.check(ra)
            native2 = raw(ws, "__v2DrcItemCount", *route_args)
            update = raw(ws, "axlDRCUpdate", True)
            after = session.drc()
            report["checker_gate"] = {"before_markers": [marker(m) for m in before],
                                      "item_hits_first": [marker(m) for m in hits1],
                                      "item_hits_second": [marker(m) for m in hits2],
                                      "native_item_first": native1,
                                      "native_item_second": native2,
                                      "full_update": {"mode": True, "raw_return": update, "marker_snapshot": [marker(m) for m in after]},
                                      "after_markers": [marker(m) for m in after],
                                      "count_after": raw(ws, "axlDRCGetCount"),
                                      "waived_after": raw(ws, "axlDRCWaiveGetCount"),
                                      "repeat_list_equal": hits2 == hits1,
                                      "positive_control_has_spacing": any("spacing" in m.name.lower() for m in hits1),
                                      "clean_gate": "PENDING_ATTRIBUTION_AND_SETTINGS"}
            report["controls_after"] = {name: raw(ws, "axlDBControl", Symbol(name)) for name in ("drcEnable", "activeLayer")}
            report["status"] = "INCOMPLETE"
    except Exception as exc:
        report["status"] = "FAILED"
        report["error"] = repr(exc)
    path = run_dir / "stage0_checker.json"
    # Preserve a byte-for-byte copy of the executed Python/SKILL inputs in the
    # run folder; never overwrite a prior run's output.
    copy2(Path(__file__), run_dir / Path(__file__).name)
    copy2(Path(__file__).with_name("drc_gate.il"), run_dir / "drc_gate.il")
    path.write_text(json.dumps(report, indent=2, default=repr), encoding="utf-8")
    print(json.dumps({"status": report["status"], "result": path.as_posix(), "port": port}, indent=2))
    if report["status"] == "FAILED":
        raise RuntimeError(report["error"])


if __name__ == "__main__":
    main()
