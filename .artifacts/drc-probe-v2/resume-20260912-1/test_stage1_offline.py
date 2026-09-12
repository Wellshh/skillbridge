"""Offline tests for Stage I matching and binary64 evidence gates."""
from __future__ import annotations

import importlib.util
from pathlib import Path

from allegrobridge.client.api.geometry import Point
from allegrobridge.client.api.record import Route, Via

SPEC = importlib.util.spec_from_file_location("stage1_smoke", Path(__file__).with_name("stage1_smoke.py"))
assert SPEC and SPEC.loader
stage1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stage1)


def test_route_dict_and_real_dto_bits() -> None:
    committed = {"committed": {"objType": "arc", "net": "NFC_SWP", "layer": "ETCH/TOP",
        "start": {"x": 100.03125, "y": 200.09375, "x17": "100.03125", "y17": "200.09375"},
        "end": {"x": 102.03125, "y": 201.09375, "x17": "102.03125", "y17": "201.09375"},
        "width": 0.15, "width17": "0.14999999999999999", "length": 3.1,
        "radius": 1.25, "radius17": "1.25", "clockwise": False,
        "center": {"x": 101.03125, "y": 200.84375, "x17": "101.03125", "y17": "200.84375"}}}
    row = Route(net="NFC_SWP", layer="ETCH/TOP", obj_type="arc",
                start=Point(100.03125, 200.09375), end=Point(102.03125, 201.09375),
                width=0.15, length=3.1, radius=1.25, is_clockwise=False,
                center=Point(101.03125, 200.84375))
    stage1.assert_requery_bits("arc", committed, row)


def test_via_dict_and_real_dto_bits() -> None:
    committed = {"committed": {"padstack": "VIA1", "net": "NFC_SWP", "x": 100.03125,
        "y": 200.09375, "x17": "100.03125", "y17": "200.09375",
        "start_layer": "ETCH/TOP", "end_layer": "ETCH/BOTTOM", "mirroring": "unmirrored"}}
    row = Via(x=100.03125, y=200.09375, rotation=0.0, padstack="VIA1", net="NFC_SWP",
              mirroring="unmirrored", start_layer="ETCH/TOP", end_layer="ETCH/BOTTOM")
    stage1.assert_requery_bits("via", committed, row)
