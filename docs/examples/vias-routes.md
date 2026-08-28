# Vias and routes

Both are transactional writes and support `.preview(...)` and
`.command(...)` like any other write.

## Placing a via

```python
via = pcb.vias.create("VIA_DEFAULT", at=(100.0, 50.0), net="GND")
```

*Skill equivalent:* `axlDBCreateVia("VIA_DEFAULT" 100:50 "GND" nil 0.0)`

```python
>>> via
ViaInfo(padstack='VIA_DEFAULT', net='GND', x=100.0, y=50.0, ...)
```

Optional arguments: `rotation` in degrees (default `0.0`) and `mirrored`
(default `False`). Omit `net` for a stand-alone via:

```python
pcb.vias.create("VIA_DEFAULT", at=(100.0, 50.0))
```

List existing vias with the same filters:

```python
pcb.vias()  # everything
pcb.vias(net="GND")  # GND vias only
pcb.vias(layer="TOP", padstack="VIA_DEFAULT")
```

## Creating a route

```python
route = pcb.routes.create(
    "SCLK",
    [(100.0, 50.0), (120.0, 50.0), (120.0, 80.0)],
    "TOP",
    0.2,
)
```

*Skill equivalent:* creating a path on `"TOP"` through the three points and
assigning it to net `SCLK` with width `0.2`.

The points are `(x, y)` tuples in the design's units; the layer name is a
subclass name as reported by `pcb.layers()` (e.g. `"TOP"`). The result is a
list of `RouteInfo` records, one per created segment:

```python
>>> for segment in route:
...     print(segment.layer, segment.start, segment.end)
```

!!! note "Input validation"

    `routes.create` validates before anything reaches Allegro: fewer than two
    points, a malformed point, or a non-positive width each raise `ValueError`
    immediately.

## Finding DRC violations afterwards

```python
pcb.drc.update()  # re-run checks (transactional write)
violations = pcb.drc()  # list[DrcInfo]
```

Or check a single object without touching global state:

```python
pcb.drc.check(pcb.nets["SCLK"])
```
