# AllegroBridge Quickstart

## Goal

Connect to an Allegro SKILL server, inspect the local API catalog, run a few read-only calls, and close the workspace cleanly.

## Setup

Start python_server.ils in Allegro before running this notebook. The default workspace is 7777 on Windows and default on Unix. Set ALLEGROBRIDGE_WORKSPACE_ID when your server uses another id.

```python
from os import getenv
from sys import platform

from allegrobridge import Workspace

default_workspace_id = "7777" if platform == "win32" else "default"
workspace_id = getenv("ALLEGROBRIDGE_WORKSPACE_ID", default_workspace_id)
ws = Workspace.open(workspace_id)
```

## Local and live discovery

Python dir() uses the bundled catalog and sends no RPC. The explicit .dir() call queries the live SKILL process once.

```python
assert "get_design" in dir(ws.db)
db_functions = ws.db.dir()
assert "get_design" in db_functions
db_functions[:10]
```

## Read the open design

Remote objects are safe to display in a notebook. Reading a property is an explicit RPC.

```python
design = ws.db.get_design()
design_bbox = design.b_box
repr(design), design_bbox
```

## Compose before executing

.expr() builds an expression locally. ws.eval() is the single execution point.

```python
design_expr = ws.db.get_design.expr()
same_design = ws.eval(design_expr)
same_design
```

## Checks

These assertions make the notebook self-checking without assuming a particular board.

```python
assert design.skill_parent_type == "db"
assert same_design == design
summary = {
    "workspace_id": workspace_id,
    "db_function_count": len(db_functions),
    "design_bbox": design_bbox,
}
summary
```

## Clean up

```python
ws.close()
print("quickstart complete")
```

## Next steps

Use the typed Session APIs for board-level workflows and the raw workspace when you need direct access to an AXL procedure.
