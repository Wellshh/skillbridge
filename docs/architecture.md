# Architecture

AllegroBridge is two layers in one repository:

```
┌─────────────────────────────────────────────────────────┐
│ allegrobridge/                                          │
│  Allegro (lifecycle) → Workspace → Session → Domain APIs │
│  board · components · layers · nets · padstacks · pins   │
│  symbols · vias · ext.<custom>          (pydantic DTOs)  │
├─────────────────────────────────────────────────────────┤
│ skillbridge/  (kernel, derived from unihd-cag/skillbridge)│
│  Workspace/RemoteFunction → Translator → Channel → Pipe  │
├─────────────────────────────────────────────────────────┤
│ Allegro PCB Editor process                              │
│  python_server.il (IPC) + allegro_server.il (txn kernel) │
└─────────────────────────────────────────────────────────┘
```

## Kernel (`skillbridge/`)

The kernel is a hardened fork of the skillbridge Virtuoso bridge. It knows
nothing about Allegro; it moves SKILL code strings to the editor and values
back.

- **Framed transport** (`protocol/socket.py`): 10-byte length header plus
  payload, capped at 64 MiB, over TCP (Windows) or Unix sockets (Linux).
- **Response protocol** (`protocol/response.py`): server replies are control-
  character framed (`STX … ETX` success, `NAK` failure, `RST` interruption),
  so partial reads and stream desynchronization are detectable.
- **Serialized pipe** (`server/_pipe.py`): exactly one in-flight request per
  server. Cross-platform timeouts, draining of late responses after a timeout,
  and explicit `DESYNCHRONIZED` / `BROKEN` / `CLOSED` terminal states.
- **Structured errors** (`exception.py`): every failure carries a machine-
  readable code, a hint, and the offending wire payload.
- **Subclassing hooks** used by allegrobridge: `Workspace._create_workspace()`
  factory, keyed workspace cache `(class, id)`, `force_tcp`, translator
  function-name hooks, and lazy `RemoteFunction` chaining.

## Allegro layer (`allegrobridge/`)

### Lifecycle

`Allegro.launch()` builds a startup script that loads `python_server.il` and
`allegro_server.il` inside a fresh `allegro.exe`, plants a random launch token,
and polls until the workspace answers — then verifies the token so a client
never attaches to the wrong window. `Allegro.connect()` attaches to a session
the user started manually. Closing an `Allegro` closes the workspace and, for
launched sessions, tears down the whole process tree.

### Transactions

All state-changing calls go through the SKILL transaction kernel in
`allegro_server.il`:

| Mode | SKILL entry point | Semantics |
| --- | --- | --- |
| Direct write | `__abRunTransaction` | atomic: commit all or roll back everything |
| Batch | `__abRunSavepointBatch` | per-command savepoints; partial success possible |
| Preview | `__abRunDryTransaction` | runs the change, reports the result, rolls back |

Before any transaction the server checks `axlOKToProceed` and fails fast with
`BUSY_ACTIVE_COMMAND` instead of queueing behind an interactive command.

### Session and domain APIs

`Session` is the facade over the raw workspace. Domain APIs
(`board`, `components`, `layers`, `nets`, `padstacks`, `pins`, `symbols`,
`vias`) are thin classes whose methods are declared with two decorators:

- `@read(procedure, adapter)` — call the SKILL procedure, validate the payload
  into frozen pydantic models (`strict=True`), stamp `session_generation`.
- `@write(procedure, adapter)` — returns a bound operation with three forms:
  `api.op(...)` (execute), `api.op.preview(...)` (dry-run),
  `api.op.command(...)` (defer into a `Batch`).

### Three-tier loading

1. **Core runtime** — `allegro_server.il` is loaded automatically whenever a
   `Workspace` connects and any procedure of `_TRANSACTION_FUNCTIONS` or a
   `@_core_api`-registered API is missing.
2. **Lazy bundled domains** — heavy/optional domains (e.g. `vias`) register
   their procedures but load their server-side `.il` only on first use via
   `Workspace._ensure_extension`.
3. **Custom extensions** — user modules under
   `allegrobridge/client/api/extensions/` loaded through `session.ext.<name>`
   (see [extensions.md](guide/extensions.md)).

Loading is idempotent, thread-safe, and failures are cached so a broken
extension raises the same error on every access instead of retrying blindly.
