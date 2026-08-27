# Quickstart

There are two ways to get a connected session: let Python launch Allegro for
you, or attach to an Allegro window you already have open.

## Launch Allegro from Python

```python
from allegrobridge import Allegro

with Allegro.launch("designs/demo.brd") as allegro:
    pcb = allegro.session
    print(pcb.board())
```

`Allegro.launch()` starts `allegro.exe`, loads the SKILL server, and blocks
until the bridge answers (verified with a per-launch identity token, so you
never attach to the wrong window). Leaving the `with` block closes the
workspace and terminates the process tree.

## Attach to a running Allegro

Start the server once, in the Allegro SKILL console:

```text
load(".../skillbridge/server/python_server.il")
load(".../allegrobridge/server/allegro_server.il")
pyStartServer(?id "7777")
```

You can obtain the exact `load(...)` lines for your installation from a
terminal:

```bash
allegrobridge path
```

Then connect from Python:

```python
with Allegro.open(mode="manual", workspace_id="7777") as allegro:
    pcb = allegro.session
    print(pcb.board())
```

*Skill equivalent:* the Python side talks to the server started by
`pyStartServer(?id "7777")`.

## First queries

```python
board = pcb.board()             # BoardInfo for the open design
r101 = pcb.components["R101"]   # one component by refdes
count = len(pcb.nets())         # all nets
```

Reads return frozen pydantic models; writes go through
[atomic transactions](../guide/transactions.md):

```python
pcb.components.move("R101", x=120.0, y=45.0, rotation=90.0)
```

## Where to next

- [Process lifecycle](../guide/lifecycle.md) — launch options, timeouts,
  workspace ids
- [Session and domain APIs](../guide/session.md) — the typed facade
- [Raw AXL access](../guide/raw-axl.md) — all 792 `axl*` functions
