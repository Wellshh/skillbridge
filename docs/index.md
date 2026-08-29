---
hide:
  - toc
---

<div class="ab-workbench" markdown>

<div class="ab-wb-title">
<span>AllegroBridge</span>
<span>DEV</span>
<span class="ab-wb-dot">● CONNECTED</span>
<span>demo.brd</span>
<span>TCP:7777</span>
<span class="ab-wb-rtt">RTT 12 ms</span>
</div>

<div class="ab-wb-panel ab-wb-domains" markdown>
<h2>Domains / Visibility</h2>
<div class="ab-wb-domain" data-active>BOARD <span class="ab-caps">READ</span></div>
<div class="ab-wb-domain">COMPONENTS <span class="ab-caps">R·W·P·B</span></div>
<div class="ab-wb-domain">LAYERS <span class="ab-caps">READ</span></div>
<div class="ab-wb-domain">NETS <span class="ab-caps">READ</span></div>
<div class="ab-wb-domain">PADSTACKS <span class="ab-caps">READ</span></div>
<div class="ab-wb-domain">PINS <span class="ab-caps">READ</span></div>
<div class="ab-wb-domain">SYMBOLS <span class="ab-caps">READ</span></div>
<div class="ab-wb-domain">VIAS <span class="ab-caps">R·W·P·LAZY</span></div>
<div class="ab-wb-domain">ROUTES <span class="ab-caps">R·W·P·LAZY</span></div>
<div class="ab-wb-domain">SHAPES <span class="ab-caps">R·W·LAZY</span></div>
<div class="ab-wb-domain">DRC <span class="ab-caps">READ·UPDATE·LAZY</span></div>
<div class="ab-wb-domain">RAW AXL <span class="ab-caps">RAW</span></div>
<div class="ab-wb-layers" markdown>
<label><input type="checkbox" data-layer="etch" checked> ETCH</label>
<label><input type="checkbox" data-layer="routes" checked> ROUTES</label>
<label><input type="checkbox" data-layer="vias" checked> VIAS</label>
<label><input type="checkbox" data-layer="drc" checked> DRC</label>
</div>
</div>

<div class="ab-wb-canvas" markdown>
<svg viewBox="0 0 400 260" role="img" aria-label="Board canvas">
  <g data-layer-group="etch" stroke="#4FD8E0" fill="none" stroke-width="1.5">
    <path d="M 40 40 L 120 120 L 240 120" opacity="0.6"/>
    <path d="M 60 200 L 140 140 L 240 140" opacity="0.4"/>
  </g>
  <g data-layer-group="vias">
    <circle cx="240" cy="120" r="7" fill="none" stroke="#E8A33D" stroke-width="2.5"/>
    <circle cx="240" cy="120" r="2.5" fill="#E8A33D"/>
  </g>
  <g class="ab-obj-r101" data-layer-group="components" transform="translate(0,0)">
    <rect x="150" y="170" width="70" height="44" rx="2" fill="rgba(232,163,61,0.12)" stroke="#E8A33D" stroke-width="2.5"/>
    <text x="185" y="196" fill="#D7DCE5" font-size="13" text-anchor="middle" font-family="JetBrains Mono,monospace">R101</text>
  </g>
  <g data-layer-group="drc">
    <circle class="ab-drc-marker" cx="300" cy="70" r="9" stroke-width="2" style="display:none"/>
  </g>
  <rect class="ab-sel-box" x="142" y="162" width="86" height="60" stroke-width="1.5" style="display:none"/>
  <g stroke="rgba(178,190,209,0.35)" stroke-width="1">
    <line x1="200" y1="0" x2="200" y2="260"/>
    <line x1="0" y1="130" x2="400" y2="130"/>
  </g>
</svg>
</div>

<div class="ab-wb-panel ab-wb-inspector" markdown>
<h2>Inspector</h2>
<dl>
<dt>Object</dt><dd class="ab-dto">ComponentInfo</dd>
<dt>refdes</dt><dd>R101</dd>
<dt>x / y</dt><dd>120.0 / 45.0</dd>
<dt>rotation</dt><dd>90.0</dd>
<dt>session_generation</dt><dd data-gen>3</dd>
</dl>
<div class="ab-modes">
<span class="ab-mode ab-mode-write" data-on>WRITE</span>
<span class="ab-mode ab-mode-preview" data-on>PREVIEW</span>
<span class="ab-mode ab-mode-batch" data-on>BATCH</span>
</div>
<div class="ab-wb-actions">
<button type="button" data-act="preview">Preview</button>
<button type="button" data-act="commit">Commit</button>
<button type="button" data-act="rollback">Rollback</button>
</div>
</div>

<div class="ab-wb-status">
<span class="ab-prompt">skill&gt;</span>
<span class="ab-cmd">READY</span>
<span class="ab-state">READY</span>
<span class="ab-coords">X 120.000 Y 45.000 mm</span>
</div>

</div>

Drive **Cadence Allegro PCB Editor** from Python — query the design database,
move components, place vias, and compose edits inside atomic SKILL
transactions, through a typed, pydantic-validated API.

[Get started](getting-started/installation.md){ .md-button .md-button--primary }
[GitHub](https://github.com/Wellshh/allegrobridge){ .md-button }

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

    Board, components, layers, nets, padstacks, pins, symbols, vias, routes,
    shapes, drc — all returned as frozen pydantic models.

    [:octicons-arrow-right-24: Session and domain APIs](guide/session.md)

-   :material-power-plug:{ .lg .middle } **Raw AXL access**

    ---

    All 792 documented `axl*` APIs on the workspace, with snake_case names
    and generated type stubs.

    [:octicons-arrow-right-24: Raw AXL access](guide/raw-axl.md)

-   :material-toolbox:{ .lg .middle } **Extensions**

    ---

    Bind typed API classes whose packaged SKILL modules load lazily on first
    use.

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
