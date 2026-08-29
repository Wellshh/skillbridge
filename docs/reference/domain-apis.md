# Domain APIs and DTOs

One API class per domain, one frozen pydantic record per result. You never
construct these yourself — reach them through
[`Session`](../guide/session.md) (`pcb.components`, `pcb.vias`, ...).

## Board

::: allegrobridge.client.api.board.BoardApi

::: allegrobridge.client.api.board.BoardInfo

## Components

::: allegrobridge.client.api.components.ComponentsApi

::: allegrobridge.client.api.components.ComponentInfo

## Layers

::: allegrobridge.client.api.layers.LayersApi

::: allegrobridge.client.api.layers.LayerInfo

## Nets

::: allegrobridge.client.api.nets.NetsApi

::: allegrobridge.client.api.nets.NetInfo

## Padstacks

::: allegrobridge.client.api.padstacks.PadstacksApi

::: allegrobridge.client.api.padstacks.PadstackInfo

## Pins

::: allegrobridge.client.api.pins.PinsApi

::: allegrobridge.client.api.pins.PinInfo

## Symbols

::: allegrobridge.client.api.symbols.SymbolsApi

::: allegrobridge.client.api.symbols.SymbolInfo

## Vias

::: allegrobridge.client.api.vias.ViasApi

::: allegrobridge.client.api.vias.ViaInfo

## Routes

::: allegrobridge.client.api.routes.RoutesApi

::: allegrobridge.client.api.routes.RouteInfo

::: allegrobridge.client.api.geometry.Point

## Shapes

::: allegrobridge.client.api.shapes.ShapesApi

::: allegrobridge.client.api.shapes.ShapeInfo

::: allegrobridge.client.api.geometry.BBox

## DRC

::: allegrobridge.client.api.drc.DrcApi

::: allegrobridge.client.api.drc.DrcInfo

::: allegrobridge.client.api.drc.ComponentRef

::: allegrobridge.client.api.drc.NetRef

::: allegrobridge.client.api.drc.PinRef
