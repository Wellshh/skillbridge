# Batching writes

Compose several writes into one transaction. Each added command hands back a
result handle you read after the `with` block:

```python
with pcb.batch("align caps") as batch:
    c1 = batch.add(pcb.components.move.command("C101", x=120.0, y=45.0))
    c2 = batch.add(pcb.components.move.command("C102", x=130.0, y=45.0))
    c3 = batch.add(pcb.components.move.command("C103", x=140.0, y=45.0))

for result in (c1, c2, c3):
    print(result.value.refdes, result.value.x)
```

*Skill equivalent:* one `__abRunTransaction` running all three moves.

## Rules

- Commands are built with `.command(...)` — the form that defers execution.
  Calling `move(...)` inside the `with` body would execute immediately, once
  per call, defeating the batch.
- `result.value` is only valid after the block exits. Reading it earlier
  raises `RuntimeError('batch result is pending')`.
- If any command fails, the whole batch rolls back, the exception propagates
  out of the `with` block, and reading any `result.value` re-raises it.
- An exception raised by *your* code inside the `with` body aborts the batch:
  nothing is executed at all.
- A batch is single-use; re-entering it raises `RuntimeError`.

## Dry-run a whole batch

```python
with pcb.batch("align caps", dry_run=True) as batch:
    c1 = batch.add(pcb.components.move.command("C101", x=120.0, y=45.0))

print(c1.value.rotation)  # reported, but nothing was committed
```

Every command goes through the dry transaction; the results describe what
would have happened.

## Partial success with savepoints

An all-or-nothing batch is not always what you want — a big fanout move
should keep the nets that work and report the ones that do not. The raw
workspace's savepoint batch does exactly that; see
[`ws.transaction.batch(...)`](../guide/transactions.md#hand-written-skill-wstransaction).
