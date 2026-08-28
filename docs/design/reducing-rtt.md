# Reducing round trips

!!! warning "Work in progress"
    Placeholder — measurements and benchmarks to follow.

## Outline

- Cost model: every remote call is one framed request/response over the pipe
- Batching: `Batch` and savepoint batches turn N writes into one transaction
- Laziness: chained `RemoteFunction` calls and the expression AST defer work
  until a value is actually needed
- Measurement plan: where round trips show up in typical scripts
