# Vias and routes

Both are transactional writes and support `.preview(...)` and
`.command(...)` like any other write.

```python
from allegrobridge.client.api import Point
```

## Placing a via

```python
via = pcb.vias.create("VIA_DEFAULT", at=Point(100.0, 50.0), net="GND")
```

*Skill equivalent:* `axlDBCreateVia("VIA_DEFAULT" 100:50 "GND" nil 0.0)`

```python
>>> via.location
Point(x=100.0, y=50.0)
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
    [Point(100.0, 50.0), Point(120.0, 50.0), Point(120.0, 80.0)],
    "ETCH/TOP",
    0.2,
)
```

*Skill equivalent:* creating a path on `"ETCH/TOP"` through the three points
and assigning it to net `SCLK` with width `0.2`.

`Point` supports unpacking and indexing like a tuple. Plain `(x, y)` tuples
are accepted too. Coordinates use the design's units; the layer name is the
fully-qualified etch subclass name (`"CLASS/SUBCLASS"`, e.g. `"ETCH/TOP"`) as
reported by the `name` field of `pcb.layers()`. The result is a
list of `Route` records, one per created segment:

```python
>>> for segment in route:
...     print(segment.layer, segment.start, segment.end)
```

!!! note "Input validation"

    `routes.create` validates before anything reaches Allegro: fewer than two
    points, a malformed or non-finite coordinate, or a non-positive width each
    raise `ValueError` immediately.

## Connecting two points (interactive router)

`routes.connect` drives Allegro's interactive `add connect` command through
the CLI, so it requires a CLI-mode session:

```python
added = pcb.routes.connect("SCLK", (100.0, 50.0), (120.0, 80.0), "ETCH/TOP", 0.2)
```

The result is the list of `Route` segments that were actually added,
re-projected from the database after the command ran — so it reflects
Allegro's own routing decisions (grid snapping, layer changes) rather than the
requested geometry.

!!! warning "Immediate operation"

    `add connect` mutates the database outside a transaction, so
    `routes.connect` has no `.preview(...)`, `.command(...)`, or batch
    semantics, and a failed call is never replayed automatically. The session
    is refreshed even if the command fails: previously queried records become
    stale and raise `RecordIDError` on reuse.

Failures raise `RuntimeError` carrying a SKILL marker. Pre-command checks run
before anything is executed — the database is untouched:

- `ROUTE_CONNECT_NET_NOT_FOUND` — no such net in the design.
- `ROUTE_CONNECT_LAYER_NOT_FOUND` — no such layer.

Post-command failures happen after `add connect` already ran; the database
may have changed and nothing is rolled back:

- `ROUTE_CONNECT_NO_CHANGE` — no new segments appeared on the net (e.g. the
  two points were already connected).
- `ROUTE_CONNECT_AMBIGUOUS` — the new segments do not form a single chain from
  `start` to `end` (e.g. the command also touched other copper, or Allegro
  snapped the picks away from the requested points).

Because `net` and `layer` are interpolated into a shell command, both must be
non-empty names without whitespace, `;`, quotes, or control characters —
anything else raises `ValueError` before reaching Allegro.

## Finding DRC violations afterwards

```python
pcb.drc.update()  # re-run checks (transactional write)
violations = pcb.drc()  # list[AbDrc]
```

Each DRC record keeps `objects` as stable business references (components,
nets, and pins). `figures` is the ordered snapshot of Allegro's one or two
violation figures; each `DrcFigure` may include a net/reference plus optional
layer, location, and bounding box. Line and arc figures also expose optional
`start`, `end`, `width`, `radius`, `is_clockwise`, and `center` geometry. Figure
geometry is diagnostic snapshot data, not a persistent route-segment identity.

Or check a single object without touching global state:

```python
pcb.drc.check(pcb.nets["SCLK"])
```

`check()` also accepts a current `Route` returned by `pcb.routes()`. The route
is resolved back to exactly one Allegro line or arc using its net and geometry;
no match raises `DRC_TARGET_NOT_FOUND`, while duplicate matching copper raises
`DRC_TARGET_AMBIGUOUS`. A route without a net cannot be checked this way.
