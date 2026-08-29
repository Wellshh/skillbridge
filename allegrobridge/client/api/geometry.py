# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import NamedTuple

from pydantic import FiniteFloat, TypeAdapter

from allegrobridge.client.base import SessionRecord
from skillbridge.client.hints import SkillCode
from skillbridge.client.translator import python_value_to_skill


class Point(NamedTuple):
    x: FiniteFloat
    y: FiniteFloat

    def __repr_skill__(self) -> SkillCode:
        point = _coerce_point(self)
        return python_value_to_skill(tuple(point))


class BBox(NamedTuple):
    ll: Point
    ur: Point

    def __repr_skill__(self) -> SkillCode:
        bbox = _BBOX.validate_python(self, strict=True)
        return python_value_to_skill((tuple(bbox.ll), tuple(bbox.ur)))


class _Located(SessionRecord):
    x: FiniteFloat
    y: FiniteFloat
    rotation: FiniteFloat

    @property
    def location(self) -> Point:
        return Point(self.x, self.y)


class _OptionalLocated(SessionRecord):
    x: FiniteFloat | None
    y: FiniteFloat | None
    rotation: FiniteFloat | None

    @property
    def location(self) -> Point | None:
        if self.x is None or self.y is None:
            return None
        return Point(self.x, self.y)


_POINT = TypeAdapter(Point)
_BBOX = TypeAdapter(BBox)
_FINITE_FLOAT = TypeAdapter(FiniteFloat)


def _coerce_point(value: Point | tuple[float, float]) -> Point:
    return _POINT.validate_python(value, strict=True)


def _coerce_finite_float(value: float) -> float:
    return _FINITE_FLOAT.validate_python(value, strict=True)
