# Raw AXL recipes

For anything the typed domains do not cover, drop to the
[raw workspace](../guide/raw-axl.md):

```python
ws = allegro.workspace
```

**Calling a function and reading properties**

```python
>>> design = ws.axl.db.get_design()
>>> design.units
'mil'
```

*Skill equivalent:* `axlDBGetDesign()->units`

**Creating objects**

```python
via = ws.axl.db.create_via("VIA_DEFAULT", (100.0, 50.0), "GND")
```

*Skill equivalent:* `axlDBCreateVia("VIA_DEFAULT" 100:50 "GND")`

**Keyword arguments**

SKILL key parameters map to Python keyword arguments:

```python
ws.axl.db.create_text("hello", (10.0, 20.0), rotation=90.0)
```

*Skill equivalent:* `axlDBCreateText("hello" 10:20 ?rotation 90.0)`

Use your IDE's hover hints: every `axl*` function carries its Cadence
reference documentation, including which parameters are positional and which
are key arguments.

**Passing symbols and literal code**

```python
from skillbridge import Symbol, SkillCode

ws.axl.db.set_variable(Symbol('no_dynamic_fill'), True)
ws['evalstring'](SkillCode('axlVersion()'))
```

*Skill equivalent:* `axlSetVariable('no_dynamic_fill t)` and
`evalstring("axlVersion()")`

**Atomic raw writes**

Raw calls execute as-is. Wrap them in a transaction when the write must be
all-or-nothing:

```python
from skillbridge import SkillCode

ws.transaction(SkillCode('axlDBCreateVia("VIA_DEFAULT" 100:50 "GND" nil 0.0)'))
```

See [Transactions](../guide/transactions.md) for preview and savepoint
variants.
