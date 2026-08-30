# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import NamedTuple

from pydantic import FiniteFloat, TypeAdapter

from allegrobridge._kernel.client.hints import SkillCode
from allegrobridge._kernel.client.translator import python_value_to_skill
from allegrobridge.client.base import SessionRecord


class Point(NamedTuple):
    x: FiniteFloat
    y: FiniteFloat

    @classmethod
    def of(cls, value: Point | tuple[float, float]) -> Point:
        if isinstance(value, Point):
            return value
        return _POINT.validate_python(value, strict=True)

    def __repr_skill__(self) -> SkillCode:
        point = _POINT.validate_python(self, strict=True)
        return python_value_to_skill(tuple(point))


class LineTo(NamedTuple):
    end: Point

    def __repr_skill__(self) -> SkillCode:
        return python_value_to_skill({'type': 'line', 'end': self.end})


class ArcTo(NamedTuple):
    end: Point
    center: Point
    clockwise: bool

    def __repr_skill__(self) -> SkillCode:
        return python_value_to_skill({
            'type': 'arc',
            'end': self.end,
            'center': self.center,
            'clockwise': self.clockwise,
        })


class PathStep:
    @staticmethod
    def of(item: LineTo | ArcTo | Point | tuple[float, float]) -> LineTo | ArcTo:
        if isinstance(item, ArcTo):
            return ArcTo(Point.of(item.end), Point.of(item.center), item.clockwise)
        if isinstance(item, LineTo):
            return LineTo(Point.of(item.end))
        return LineTo(Point.of(item))


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


def finite(value: float) -> float:
    return _FINITE_FLOAT.validate_python(value, strict=True)
