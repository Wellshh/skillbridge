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
    points, a `LineTo`/`ArcTo` step in the first position (the start must be a
    plain coordinate), adjacent duplicate points, a malformed or non-finite
    coordinate, or a non-positive width each raise `ValueError` immediately.
    Allegro itself silently drops zero-length segments, so rejecting adjacent
    duplicates surfaces caller bugs instead of hiding them.

!!! warning "Net assignment"

    The net name must exist in the design: a nonexistent name fails with
    `ROUTE_CREATE_FAILED` and the transaction rolls back. `net=""` is accepted
    and creates unassigned copper (Allegro's dummy net). Even with an existing
    net, Allegro attaches the net name only to etch connected to a pin, via, or
    shape — segments placed away from that net's copper come back as `Route`
    rows with `net=None`. Each row's `net` is therefore the database's own
    assignment, not an echo of the requested name.

## Connecting two points (interactive router)

`routes.connect` drives Allegro's interactive `add connect` command through
the CLI, so it requires a CLI-mode session:

```python
result = pcb.routes.connect("SCLK", (100.0, 50.0), (120.0, 80.0), "ETCH/TOP", 0.2)
```

The result is a `RouteConnectResult` describing what changed on the target
net, re-projected from the database after the command ran:

- `result.added` — `Route` segments that newly appeared on the net. They
  belong to the refreshed session generation.
- `result.removed` — segments that existed before and disappeared. They are a
  historical snapshot, stale immediately (`RecordIDError` on reuse).

The delta is a multiset (duplicate segments are preserved) and covers the
target net only — collateral changes on other nets are excluded. It reports
projection differences, not Allegro DBID creation/deletion identity: `added`
may contain split, direction-flipped, or re-materialized old copper rather
than a brand-new main chain. Both lists being empty is a legal outcome (e.g.
the two points were already connected and the router declined to act).

!!! warning "No connectivity guarantee"

    `connect()` executes a structured `add connect` command and reports the
    observable database delta. Allegro snaps picks to pins/copper/grid, moves
    points beyond the database resolution, and silently no-ops on unanchored
    coordinates — a non-empty `added` does **not** prove the two requested
    coordinates became electrically connected.

!!! warning "Immediate, non-idempotent operation"

    `add connect` mutates the database outside a transaction, so
    `routes.connect` has no `.preview(...)`, `.command(...)`, or batch
    semantics, and a failed call is never replayed automatically. Repeated
    calls with the same arguments may re-route existing copper or change
    nothing. The session is refreshed even if the command fails: previously
    queried records become stale and raise `RecordIDError` on reuse.

`layer` and `width` are hints: in probe evidence Allegro placed copper on its
own current layer regardless of the requested one, and constraint widths
overrode the requested width. The authoritative values are whatever the
returned `Route` rows carry.

Coordinates and `width` are transmitted with full IEEE-754 double round-trip
precision (`%.17g`; SKILL's default float rendering keeps only ~7 significant
digits) and are never pre-quantized. Allegro rounds the committed geometry by
the design's own units/accuracy, so the returned `Route` coordinates are the
authoritative database values.

Pre-command checks raise `RuntimeError` carrying a SKILL marker before
anything is executed — the database is untouched:

- `ROUTE_CONNECT_NET_NOT_FOUND` — no such net in the design.
- `ROUTE_CONNECT_LAYER_NOT_FOUND` — no such layer.

Because both names are interpolated into a shell command, they are validated
first. `net` reaches the CLI quoted via SKILL `%L`, so it may contain inner
ASCII spaces (e.g. `"NET 24"`); empty or pure-whitespace names, edge
whitespace, `;`, quotes, and control characters still raise `ValueError`
before reaching Allegro. `layer` reaches the CLI unquoted and must contain no
whitespace at all.

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
