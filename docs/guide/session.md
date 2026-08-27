# Session and domain APIs

`Session` is the typed facade over the raw workspace. You get it from
`allegro.session`; it is usually bound to a short name:

```python
with Allegro.launch("designs/demo.brd") as allegro:
    pcb = allegro.session
```

## The domain APIs

Eleven domains, one attribute each:

| Attribute | Reads | Writes |
| --- | --- | --- |
| `pcb.board` | `board()` → `BoardInfo` | — |
| `pcb.components` | `components()`, `components["R101"]` | `move(...)` |
| `pcb.layers` | `layers(etch_only=False)`, `layers["TOP"]` | — |
| `pcb.nets` | `nets()`, `nets["GND"]` | — |
| `pcb.padstacks` | `padstacks()`, `padstacks["VIA_DEFAULT"]` | — |
| `pcb.pins` | `pins(component=..., net=...)`, `pins["R101", "1"]` | — |
| `pcb.symbols` | `symbols()` | — |
| `pcb.vias` | `vias(net=..., layer=..., padstack=...)` | `create(...)` |
| `pcb.routes` | `routes(net=..., layer=...)` | `create(...)` |
| `pcb.shapes` | `shapes(net=..., layer=..., dynamic=...)` | — |
| `pcb.drc` | `drc()`, `drc.check(target)` | `update()` |

## Reading

Calling a domain returns a list; subscripting returns one item:

```python
pcb.components()             # list[ComponentInfo], placed and unplaced
pcb.components["R101"]       # ComponentInfo
```

*Skill equivalent:* projecting `axlDBGetDesign()->components` and friends into
typed records.

Subscripting a name that does not exist raises `KeyError`:

```python
pcb.components["R999"]
# KeyError: 'R999'
```

The optional filters are keyword-only and combine freely:

```python
pcb.pins(net="GND")                     # all GND pins
pcb.vias(layer="TOP", padstack="VIA")   # matching vias only
```

## The returned records

Every read validates its payload into a frozen pydantic model
(`strict=True`, extra keys forbidden). Records are immutable snapshots:

```python
>>> pcb.components["R101"]
ComponentInfo(refdes='R101', device_type='...', package='...', ...)
```

Each record is stamped with the session it came from and the
`session.generation` at fetch time, so writes can detect stale data.

## Escape hatches

- `pcb.raw` — the underlying [raw workspace](raw-axl.md) with all 792 `axl*`
  functions.
- `pcb.ext.<name>` — lazily loaded [custom extensions](extensions.md).
- `pcb.batch(...)` — compose several writes into one
  [transaction](transactions.md).

!!! note

    Domain attributes are `cached_property` objects: the API instance is
    created once per session and reused. Reads themselves always hit Allegro —
    nothing is cached between calls.
