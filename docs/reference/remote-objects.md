# Remote objects

Functions that return SKILL database objects give you `RemoteObject` handles
(`skillbridge/client/objects.py`). A handle is a proxy: attribute access and
method calls are forwarded to the object inside Allegro.

## Reading properties

SKILL properties are plain Python attributes:

```python
>>> design = ws.axl.db.get_design()
>>> design.b_box
[[0, 0], [14400, 9600]]
>>> design.units
'mil'
```

*Skill equivalent:* `design->bBox`, `design->units`

Properties that are objects themselves come back as further `RemoteObject`
handles, so access chains naturally:

```python
>>> pcb.modules          # a SKILL table
<remote table ...>
```

## Assigning properties

Assignment writes through to the SKILL side:

```python
>>> design.some_prop = 123
>>> design.some_prop
123
```

*Skill equivalent:* `design->some_prop = 123`

!!! warning

    List values are snapshots, not live views. Mutating a fetched list does
    not change the SKILL side — assign the modified list back:

    ```python
    data = design.data
    data.append(4)
    design.data = data
    ```

## Inspecting

`dir()` lists the SKILL properties and powers tab completion in IPython and
Jupyter:

```python
>>> dir(design)
['b_box', 'units', ...]
```

*Skill equivalent:* `design->?`

## Tables, vectors, and lazy lists

- `RemoteTable` — a SKILL hash table, exposed as a Python `MutableMapping`.
- `RemoteVector` — a SKILL array, indexable like a list.
- `LazyList` — a long SKILL list fetched in chunks; slicing pulls only the
  pages you touch.

## Identity

Two handles to the same SKILL object compare equal:

```python
a = ws.axl.db.get_design()
b = ws.axl.db.get_design()
assert a == b
```

## Calling methods on objects

SKILL functions whose first argument is an object can be called as methods on
its handle. The method name keeps the function's prefix to avoid collisions:

```python
>>> design.db_full_path()
'.../demo.brd'
```

*Skill equivalent:* `dbFullPath(design)`

## Remote functions

Attribute access on the workspace returns `RemoteFunction` objects. Calling
them sends the request immediately; `.lazy(...)` instead builds the SKILL
expression without sending it — this is how the
[batch framework](batch.md) defers commands:

```python
expr = ws.axl.db.create_via.lazy("VIA", (100.0, 50.0))
# nothing has reached Allegro yet
```
