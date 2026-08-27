# Basic queries

Connect and look around the design:

```python
from allegrobridge import Allegro

with Allegro.open(mode="manual", workspace_id="7777") as allegro:
    pcb = allegro.session

    print(pcb.board())
    print(pcb.components["R101"])
```

**Reading board information**

```python
>>> pcb.board()
BoardInfo(path='.../demo.brd', units='mil', component_count=214, ...)
```

**Listing and finding components**

```python
>>> len(pcb.components())
214
>>> pcb.components["R101"]
ComponentInfo(refdes='R101', package='R0603', x=100.0, y=45.0, ...)
>>> pcb.components["R999"]
Traceback (most recent call last):
KeyError: 'R999'
```

Unplaced components are included by default; pass
`include_unplaced=False` to skip them. Unplaced records have
`placement='unplaced'` and `x`/`y`/`rotation` set to `None`.

**Nets and their pins**

```python
>>> gnd = pcb.nets["GND"]
>>> gnd.unconnected_count
3
>>> pcb.pins(net="GND")
[PinInfo(refdes='R101', number='1', net='GND', ...), ...]
>>> pcb.pins["R101", "1"]
PinInfo(refdes='R101', number='1', ...)
```

**Layers**

```python
>>> pcb.layers(etch_only=True)
[LayerInfo(name='TOP', ...), LayerInfo(name='GND', ...), ...]
>>> pcb.layers["TOP"].is_etch
True
```

*Skill equivalent:* these reads project `axlDBGetDesign()` and its attached
objects into typed records instead of handing you `dbid` handles.

!!! hint

    Everything returned here is an immutable snapshot. To change the design,
    use the [write operations](move-component.md) — records never update
    themselves.
