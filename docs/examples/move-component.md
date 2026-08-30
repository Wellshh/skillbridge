# Moving a component

`components.move` is a transactional write: it either commits fully or rolls
back, and returns the updated record.

=== "Python"

    ```python
    updated = pcb.components.move("R101", x=120.0, y=45.0, rotation=90.0)
    ```

=== "SKILL"

    ```skill
    ;;; via __abRunTransaction — move the dbid, refresh attributes
    (axlDBMoveProp refdes "R101" 120.0 45.0 90.0)
    ```

=== "Wire"

    ```text
    STX {"cmd":"__abRunTransaction","fn":"move","args":["R101",120.0,45.0,90.0]} ETX
    ```

*Skill equivalent:* moving the component attached to `R101`'s `dbid`, then
refreshing its attributes.

```python
>>> updated.rotation
90.0
```

`rotation` is optional — omit it to keep the current orientation:

```python
pcb.components.move("R101", x=120.0, y=45.0)
```

## Move several components by one delta

Use `move_by` when several existing component records need the same relative
translation:

```python
components = pcb.components(include_unplaced=False)[:3]
moved = pcb.components.move_by(components, dx=10.0, dy=-5.0)
```

This is one RPC, one Allegro list transform, and one atomic transaction. The
returned records follow the input order. The input records must belong to the
current session and generation, and each reference designator may appear only once.

## Preview before committing

Use `.preview(...)` to run the change, see the result, and roll it back:

```python
preview = pcb.components.move.preview("R101", x=0.0, y=0.0)
print(preview.x, preview.y)  # the would-be position
# the design itself is unchanged
```

This is the same code path as the real write — the SKILL kernel runs the move
inside a dry transaction and reports what would have happened.

## Failure modes

```python
pcb.components.move("R999", x=0.0, y=0.0)
```

!!! note

    Moving a refdes that does not exist fails inside the transaction; the
    error surfaces as a structured bridge exception and nothing is committed.
    Reads behave differently: `pcb.components["R999"]` raises `KeyError`
    without touching the database.

For different absolute destinations or rotations, use a [batch](batch.md).
