# Domain APIs and DTOs

One API class per domain, one frozen pydantic record per result. You never
construct these yourself — reach them through
[`Session`](../guide/session.md) (`pcb.components`, `pcb.vias`, ...).

## Board

::: allegrobridge.client.api.board.BoardApi

::: allegrobridge.client.api.board.AbBoard

## Components

::: allegrobridge.client.api.components.ComponentsApi

::: allegrobridge.client.api.components.AbComponent

## Layers

::: allegrobridge.client.api.layers.LayersApi

::: allegrobridge.client.api.layers.AbLayer

## Nets

::: allegrobridge.client.api.nets.NetsApi

::: allegrobridge.client.api.nets.AbNet

## Padstacks

::: allegrobridge.client.api.padstacks.PadstacksApi

::: allegrobridge.client.api.padstacks.AbPadstack

## Pins

::: allegrobridge.client.api.pins.PinsApi

::: allegrobridge.client.api.pins.AbPin

## Symbols

::: allegrobridge.client.api.symbols.SymbolsApi

::: allegrobridge.client.api.symbols.AbSymbol

## Vias

::: allegrobridge.client.api.vias.ViasApi

::: allegrobridge.client.api.vias.AbVia

## Routes

::: allegrobridge.client.api.routes.RoutesApi

::: allegrobridge.client.api.routes.AbRoute

::: allegrobridge.client.api.geometry.Point

## Shapes

::: allegrobridge.client.api.shapes.ShapesApi

::: allegrobridge.client.api.shapes.AbShape

::: allegrobridge.client.api.geometry.BBox

## DRC

::: allegrobridge.client.api.drc.DrcApi

::: allegrobridge.client.api.drc.AbDrc

::: allegrobridge.client.api.drc.AbComponentRef

::: allegrobridge.client.api.drc.AbNetRef

::: allegrobridge.client.api.drc.AbPinRef
