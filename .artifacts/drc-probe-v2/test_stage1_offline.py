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
        "length17": "3.1000000000000001",
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
            "rotation": 0.0,
        "start_layer": "ETCH/TOP", "end_layer": "ETCH/BOTTOM", "mirroring": "unmirrored"}}
    row = Via(x=100.03125, y=200.09375, rotation=0.0, padstack="VIA1", net="NFC_SWP",
              mirroring="unmirrored", start_layer="ETCH/TOP", end_layer="ETCH/BOTTOM")
    stage1.assert_requery_bits("via", committed, row)


def test_echo_schema_and_quantized_commit_are_distinct() -> None:
    inputs = {"start": [stage1.wire(100.03125), stage1.wire(200.09375)],
              "end": [stage1.wire(102.03125), stage1.wire(201.09375)],
              "width": stage1.wire(0.15), "center": [stage1.wire(101.03125), stage1.wire(200.84375)]}
    committed = {"request": {"start": {"x17": "100.03125", "y17": "200.09375"},
                              "end": {"x17": "102.03125", "y17": "201.09375"},
                              "width17": "0.14999999999999999",
                              "center": {"x17": "101.03125", "y17": "200.84375"}}}
    stage1.assert_echo_inputs("arc", committed, inputs)
    assert stage1.parent_status([0, 0, 0]) == "RUNTIME_PENDING_ALL_CASES"
    assert stage1.parent_status([0, 1]) == "FAILED_RUNTIME"


def test_echo_bits_reject_wrong_wire() -> None:
    inputs = {"start": [stage1.wire(1.0), stage1.wire(2.0)], "end": [stage1.wire(3.0), stage1.wire(4.0)],
              "width": stage1.wire(0.15), "center": [stage1.wire(2.0), stage1.wire(2.5)]}
    bad = {"request": {"start": {"x17": "1.0000000000000002", "y17": "2"},
                        "end": {"x17": "3", "y17": "4"}, "width17": "0.15",
                        "center": {"x17": "2", "y17": "2.5"}}}
    try:
        stage1.assert_echo_inputs("arc", bad, inputs)
    except RuntimeError:
        return
    raise AssertionError("wrong echo wire was accepted")
