---
hide:
  - toc
---

<div class="ab-hero" markdown>

# AllegroBridge

Drive **Cadence Allegro PCB Editor** from Python — query the design database,
move components, place vias, and compose edits inside atomic SKILL
transactions, through a typed, pydantic-validated API.

[Get started](getting-started/installation.md){ .md-button .md-button--primary }
[GitHub](https://github.com/Wellshh/allegrobridge){ .md-button }

</div>

```python
from allegrobridge import Allegro

with Allegro.launch("designs/demo.brd") as allegro:
    pcb = allegro.session

    board = pcb.board()  # BoardInfo(path, units, component_count, ...)
    r101 = pcb.components["R101"]  # ComponentInfo(refdes, x, y, rotation, ...)

    pcb.components.move("R101", x=120.0, y=45.0, rotation=90.0)
```

## Features

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Process lifecycle**

    ---

    Launch Allegro from Python, or attach to a running session with an
    identity-checked handshake.

    [:octicons-arrow-right-24: Process lifecycle](guide/lifecycle.md)

-   :material-atom-variant:{ .lg .middle } **Atomic transactions**

    ---

    Every write runs in an atomic transaction, with savepoint batches and
    dry-run previews.

    [:octicons-arrow-right-24: Transactions](guide/transactions.md)

-   :material-puzzle:{ .lg .middle } **Typed domain APIs**

    ---

    Board, components, layers, nets, padstacks, pins, symbols, vias — all
    returned as frozen pydantic models.

    [:octicons-arrow-right-24: Session and domain APIs](guide/session.md)

-   :material-power-plug:{ .lg .middle } **Raw AXL access**

    ---

    All 792 documented `axl*` APIs on the workspace, with snake_case names
    and generated type stubs.

    [:octicons-arrow-right-24: Raw AXL access](guide/raw-axl.md)

-   :material-toolbox:{ .lg .middle } **Extensions**

    ---

    Extend the session with your own API domains, loaded lazily on first
    access.

    [:octicons-arrow-right-24: Writing extensions](guide/extensions.md)

-   :material-check-decagram:{ .lg .middle } **SKILL-side testing**

    ---

    Vendored qtest framework plus qcover, a branch-coverage instrumenter for
    classic SKILL.

    [:octicons-arrow-right-24: SKILL testing](skill-testing.md)

</div>

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
