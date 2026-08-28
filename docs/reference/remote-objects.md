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

## Tables, vectors, and list expressions

- `RemoteTable` — a SKILL hash table, exposed as a Python `MutableMapping`.
- `RemoteVector` — a SKILL array, indexable like a list.
- `ListExpr` — a local expression for filtering, mapping, or iterating a remote
  SKILL list; evaluation is explicit through `Workspace.eval()`.

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
them sends the request immediately; `.expr(...)` builds an expression without
sending it:

```python
expr = ws.axl.db.get_design.expr()
# nothing has reached Allegro yet
design = ws.eval(expr)
```

Remote objects can start the same expression chain:

```python
components = design.expr().components.as_list()
placed = components.where(lambda component: component.placed)
snapshot = ws.eval(placed)
```

Use `ws["function"].expr(...)` for normal calls. `Expr.call(...)` is the
low-level constructor when no workspace proxy is available, and
`Expr.raw_skill(...)` is the explicit source-code escape hatch.

The Python API names `render`, `as_list`, `raw_skill`, `wrap`, and `call` are
reserved on `Expr`; `where`, `each`, `map`, and `for_each` are additionally
reserved on `ListExpr`. Use string indexing for a SKILL property with one of
those names, for example `expr["call"]`. Parenthesize comparisons combined
with `&` or `|`, as required by Python operator precedence:

```python
condition = (component.enabled == True) & (component.layer == "TOP")
```
