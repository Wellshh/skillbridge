# AllegroBridge

A Python bridge to **Cadence Allegro PCB Editor** (AXL/SKILL), derived from
[skillbridge](https://github.com/unihd-cag/skillbridge).

AllegroBridge lets you drive a running Allegro session from Python: query the
design database, move components, place vias, and compose edits inside atomic
SKILL transactions — through a typed, pydantic-validated API.

```python
from allegrobridge import Allegro

with Allegro.launch("designs/demo.brd") as allegro:
    pcb = allegro.session

    board = pcb.board()  # BoardInfo(path, units, component_count, ...)
    r101 = pcb.components["R101"]  # ComponentInfo(refdes, x, y, rotation, ...)

    pcb.components.move("R101", x=120.0, y=45.0, rotation=90.0)
```

## Features

- [Launch Allegro from Python, or attach to a running session](guide/lifecycle.md)
- [Every write runs in an atomic transaction](guide/transactions.md), with
  savepoint batches and dry-run previews
- [Typed domain APIs](guide/session.md) — board, components, layers, nets,
  padstacks, pins, symbols, vias — return frozen pydantic models
- [All 792 documented `axl*` APIs on the raw workspace](guide/raw-axl.md), with
  snake_case names and generated type stubs
- [Extend the session with your own API domains](guide/extensions.md)
- [SKILL-side testing](skill-testing.md) with the vendored qtest framework plus
  qcover, our branch-coverage instrumenter for classic SKILL

The generated stubs give every `axl*` function autocompletion, signature hints,
and docstrings in a PEP 561-aware IDE:

![IDE autocompletion demo](assets/ide_completion.gif)

## Where to next

- [Install AllegroBridge](getting-started/installation.md) and
  [connect your first session](getting-started/quickstart.md)
- Read the [User Guide](guide/session.md) for sessions, transactions, and raw
  AXL access
- Browse the [Examples](examples/index.md) for task-oriented recipes
- Look up classes in the [Reference](reference/index.md)
