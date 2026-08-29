# Transactions

All state-changing calls go through the SKILL transaction kernel in
`allegro_server.il`. Three modes exist:

| Mode | SKILL entry point | Semantics |
| --- | --- | --- |
| Direct write | `__abRunTransaction` | atomic: commit all or roll back everything |
| Batch | `__abRunSavepointBatch` | per-command savepoints; partial success possible |
| Preview | `__abRunDryTransaction` | runs the change, reports the result, rolls back |

!!! note

    Before any transaction the server checks `axlOKToProceed` and fails fast
    with `BUSY_ACTIVE_COMMAND` instead of queueing behind an interactive
    command you started in the Allegro window.

## The three forms of a write

Every transactional write operation supports three forms. Take
`components.move` as the example:

```python
# execute now, inside an atomic transaction
pcb.components.move("R101", x=120.0, y=45.0, rotation=90.0)

# dry-run: the change is made, the result reported, then rolled back
preview = pcb.components.move.preview("R101", x=120.0, y=45.0)

# defer: build a command for a batch
cmd = pcb.components.move.command("C101", x=120.0, y=45.0)
```

All three return the validated result record (here a fresh `ComponentInfo`);
the direct form additionally raises if the transaction fails.

## Batching

A `Batch` runs its commands in one transaction and gives you a result handle
per command:

```python
with pcb.batch("align caps") as batch:
    c1 = batch.call(pcb.components.move.command, "C101", x=120.0, y=45.0)
    c2 = batch.call(pcb.components.move.command, "C102", x=130.0, y=45.0)

print(c1.value.rotation)
```

- `batch.call(operation.command, ...)` constructs and adds a command while
  preserving the operation's argument types. `batch.add(command)` remains the
  lower-level entry point. Both return a `CmdResult` that resolves when the
  `with` block exits. Reading `.value` before that raises `RuntimeError`; if
  the batch failed, `.value` re-raises the error.
- An exception inside the `with` body aborts the batch; nothing is executed.
- A batch object is single-use: re-entering it raises `RuntimeError`.
- Adding a command built from a *different* session raises `ValueError`.
- `pcb.batch("...", dry_run=True)` runs the whole batch through the preview
  path — results are reported, nothing is committed.

## Hand-written SKILL: `ws.transaction`

For code the domain APIs do not cover, the raw workspace exposes the same
kernel directly:

```python
from skillbridge import SkillCode

ws = allegro.workspace
ws.transaction(SkillCode('axlDBCreateVia("VIA" 100:200 "GND" t 0.0 nil)'))
ws.transaction.preview(SkillCode('...'))  # dry-run
results = ws.transaction.batch([SkillCode('...'), SkillCode('...')])
```

`batch()` takes several commands and runs each under its own savepoint:
successes commit, failures roll back — partial success is possible. Each item
of the result list is either

```python
{"index": 0, "status": "success", "value": ...}
{"index": 1, "status": "failure", "error": "..."}
```

*Skill equivalent:* `__abRunTransaction(...)`, `__abRunDryTransaction(...)`,
`__abRunSavepointBatch(list(...))`.
