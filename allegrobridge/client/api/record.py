# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, FiniteFloat, NonNegativeInt, field_validator

from allegrobridge.client.api.geometry import BBox, Point
from allegrobridge.client.base import BaseRecord, SessionRecord

_OptionalString = str | None
_Width = Annotated[float, Field(gt=0, allow_inf_nan=False)]


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


class Board(SessionRecord):
    path: str
    units: str
    component_count: NonNegativeInt
    symbol_count: NonNegativeInt
    net_count: NonNegativeInt


class Component(_OptionalLocated):
    refdes: str
    device_type: str
    package: str
    component_class: str
    placement: Literal['placed', 'unplaced']


class ComponentRef(BaseRecord):
    kind: Literal['component']
    refdes: str


class NetRef(BaseRecord):
    kind: Literal['net']
    name: str


class PinRef(BaseRecord):
    kind: Literal['pin']
    refdes: str
    number: str


DrcObjectRef = ComponentRef | NetRef | PinRef


class Drc(SessionRecord):
    name: str
    category: str
    source: str
    expected: str
    actual: str
    layer: str
    location: Point
    bbox: BBox
    objects: list[DrcObjectRef]

    @field_validator('objects', mode='before')
    @classmethod
    def _normalize_empty_objects(cls, value: object) -> object:
        # Allegro encodes an empty SKILL list as nil, while the public model uses []
        # so callers can rely on the list contract without weakening other validation.
        return [] if value is None else value


class Layer(SessionRecord):
    name: str
    class_name: str
    subclass: str
    number: int

    @property
    def is_etch(self) -> bool:
        return self.class_name == 'ETCH'


class Net(SessionRecord):
    name: str
    branch_count: NonNegativeInt
    unconnected_count: NonNegativeInt
    unplaced_pin_count: NonNegativeInt


class Padstack(SessionRecord):
    name: str
    type: str
    usage: str
    start_layer: _OptionalString
    end_layer: _OptionalString


class Pin(_OptionalLocated):
    refdes: str
    number: str  # pin number
    net: _OptionalString
    padstack: _OptionalString
    placement: Literal['placed', 'unplaced']
    start_layer: _OptionalString
    end_layer: _OptionalString


class Route(SessionRecord):
    net: _OptionalString
    layer: str
    obj_type: str
    start: Point
    end: Point
    width: _Width
    length: FiniteFloat

    # optional Arc attributes
    radius: FiniteFloat | None
    is_clockwise: bool | None
    center: Point | None


class Shape(SessionRecord):
    net: _OptionalString
    layer: str
    dynamic: Literal['dynamic', 'static']
    bbox: BBox


class PcbSymbol(_Located):
    name: str
    type: str
    refdes: _OptionalString


# Alias for domain API usage
Symbol = PcbSymbol


class Via(_Located):
    padstack: str
    net: _OptionalString
    mirroring: Literal['mirrored', 'unmirrored']
    start_layer: str
    end_layer: str


# Backward-compatible aliases
AbBoard = Board
AbComponent = Component
AbComponentRef = ComponentRef
AbNetRef = NetRef
AbPinRef = PinRef
AbDrcObjectRef = DrcObjectRef
AbDrc = Drc
AbLayer = Layer
AbNet = Net
AbPadstack = Padstack
AbPin = Pin
AbRoute = Route
AbShape = Shape
AbSymbol = PcbSymbol
AbVia = Via

__all__ = [
    'AbBoard',
    'AbComponent',
    'AbComponentRef',
    'AbDrc',
    'AbDrcObjectRef',
    'AbLayer',
    'AbNet',
    'AbNetRef',
    'AbPadstack',
    'AbPin',
    'AbPinRef',
    'AbRoute',
    'AbShape',
    'AbSymbol',
    'AbVia',
    'Board',
    'Component',
    'ComponentRef',
    'Drc',
    'DrcObjectRef',
    'Layer',
    'Net',
    'NetRef',
    'Padstack',
    'PcbSymbol',
    'Pin',
    'PinRef',
    'Route',
    'Shape',
    'Symbol',
    'Via',
]
