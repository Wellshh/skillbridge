# Domain APIs and DTOs

One API class per domain, one frozen pydantic record per result. You never
construct these yourself — reach them through
[`Session`](../guide/session.md) (`pcb.components`, `pcb.vias`, ...).

## Board

::: allegrobridge.client.api.board.BoardApi

::: allegrobridge.client.api.record.AbBoard

## Components

::: allegrobridge.client.api.components.ComponentsApi

::: allegrobridge.client.api.record.AbComponent

## Layers

::: allegrobridge.client.api.layers.LayersApi

::: allegrobridge.client.api.record.AbLayer

## Nets

::: allegrobridge.client.api.nets.NetsApi

::: allegrobridge.client.api.record.AbNet

## Padstacks

::: allegrobridge.client.api.padstacks.PadstacksApi

::: allegrobridge.client.api.record.AbPadstack

## Pins

::: allegrobridge.client.api.pins.PinsApi

::: allegrobridge.client.api.record.AbPin

## Symbols

::: allegrobridge.client.api.symbols.SymbolsApi

::: allegrobridge.client.api.record.AbSymbol

## Vias

::: allegrobridge.client.api.vias.ViasApi

::: allegrobridge.client.api.record.AbVia

## Routes

::: allegrobridge.client.api.routes.RoutesApi

::: allegrobridge.client.api.record.Route

::: allegrobridge.client.api.record.RouteConnectResult

::: allegrobridge.client.api.geometry.Point

## Shapes

::: allegrobridge.client.api.shapes.ShapesApi

::: allegrobridge.client.api.record.AbShape

::: allegrobridge.client.api.geometry.BBox

## DRC

::: allegrobridge.client.api.drc.DrcApi

::: allegrobridge.client.api.record.AbDrc

::: allegrobridge.client.api.record.AbComponentRef

::: allegrobridge.client.api.record.AbNetRef

::: allegrobridge.client.api.record.AbPinRef
