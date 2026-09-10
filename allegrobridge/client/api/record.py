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


class DrcFigure(BaseRecord):
    """One Allegro marker violation figure, captured without stable identity."""

    obj_type: str
    layer: str | None = None
    location: Point | None = None
    bbox: BBox | None = None
    net: NetRef | None = None
    reference: DrcObjectRef | None = None
    start: Point | None = None
    end: Point | None = None
    width: _Width | None = None
    radius: FiniteFloat | None = None
    is_clockwise: bool | None = None
    center: Point | None = None


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
    figures: list[DrcFigure] = Field(default_factory=list)

    @field_validator('objects', mode='before')
    @classmethod
    def _normalize_empty_objects(cls, value: object) -> object:
        # Allegro encodes an empty SKILL list as nil, while the public model uses []
        # so callers can rely on the list contract without weakening other validation.
        return [] if value is None else value

    @field_validator('figures', mode='before')
    @classmethod
    def _normalize_empty_figures(cls, value: object) -> object:
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


class RouteConnectResult(BaseRecord):
    """Projection delta observed on the target net after ``routes.connect()``.

    ``added`` rows belong to the refreshed Session generation; ``removed`` rows are
    a historical snapshot that is immediately stale. Both deltas are multisets
    (duplicate segments preserved) and report projection differences only - they
    carry no promise about Allegro DBID creation/deletion identity, and both being
    empty is a legal outcome.
    """

    added: list[Route]
    removed: list[Route]


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
AbDrcFigure = DrcFigure
AbDrc = Drc
AbLayer = Layer
AbNet = Net
AbPadstack = Padstack
AbPin = Pin
AbRoute = Route
AbRouteConnectResult = RouteConnectResult
AbShape = Shape
AbSymbol = PcbSymbol
AbVia = Via

__all__ = [
    'AbBoard',
    'AbComponent',
    'AbComponentRef',
    'AbDrc',
    'AbDrcFigure',
    'AbDrcObjectRef',
    'AbLayer',
    'AbNet',
    'AbNetRef',
    'AbPadstack',
    'AbPin',
    'AbPinRef',
    'AbRoute',
    'AbRouteConnectResult',
    'AbShape',
    'AbSymbol',
    'AbVia',
    'Board',
    'Component',
    'ComponentRef',
    'Drc',
    'DrcFigure',
    'DrcObjectRef',
    'Layer',
    'Net',
    'NetRef',
    'Padstack',
    'PcbSymbol',
    'Pin',
    'PinRef',
    'Route',
    'RouteConnectResult',
    'Shape',
    'Symbol',
    'Via',
]
