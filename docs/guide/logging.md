# Logging

AllegroBridge routes all Python-side output through the standard `logging`
module under a single `allegrobridge.*` namespace. One call to
`setup_logging()` gives you a colorized console via [rich][].

[rich]: https://rich.readthedocs.io/

## Quickstart

```python
from allegrobridge import setup_logging

setup_logging()  # rich console handler at INFO
```

`setup_logging()` is **explicit** — AllegroBridge never configures logging
behind your back, so it cannot fight a handler you already installed. Until you
call it, the library installs only a `NullHandler` (the recommended behavior for
libraries); call `setup_logging()` (or `logging.basicConfig()`) to see output.

```python
setup_logging(level="DEBUG", file="allegrobridge.log")  # console + file
setup_logging(console=False, file="allegrobridge.log")  # file only
```

`setup_logging()` replaces **only** the handlers it added (closing the previous
ones); any handler you installed yourself is left untouched. While it owns
handlers it sets `propagate = False` on the `allegrobridge` logger, so records do
not also reach the root logger — no double output in Jupyter.

## Loggers

| Logger | What lands here |
| --- | --- |
| `allegrobridge` | namespace root; owns the handlers from `setup_logging()` |
| `allegrobridge.cadence` | **SKILL** output captured during an RPC — `printf` (INFO), `warn` (WARNING) |
| `allegrobridge.server` | the in-Allegro Python daemon (startup, framing, pipe state) |
| `allegrobridge.allegro` / `allegrobridge._runtime` / `allegrobridge._kernel.*` | launch/attach/close, spawned process, workspace/pipe |

Tune a single channel:

```python
import logging

logging.getLogger("allegrobridge.cadence").setLevel(logging.WARNING)
```

The SKILL channel emits only INFO (`printf`) and WARNING (`warn`) — there is no
DEBUG path, so `setLevel(DEBUG)` shows the same records as INFO.

### Unconfigured behavior

With only the library `NullHandler` in place, INFO records are dropped, but
WARNING+ surfaces through stdlib `lastResort` to stderr. SKILL lines also raise
a `UserWarning` regardless of logging config (see below).

## SKILL output (printf / warn)

SKILL `printf` and `warn` produced during an RPC are captured and routed to
`allegrobridge.cadence` — `printf` lines at INFO, `warn` lines at WARNING. Logs
arrive with the RPC response (not streamed mid-call; SKILL is single-threaded
and runs each call to completion first).

Each SKILL line emits **both** a logging record **and** a `UserWarning` (the
`warning(msg, value)` wire contract pins the latter). To keep only the logging
side:

```python
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
```

## Server-side log files

| File | Contents | Owner |
| --- | --- | --- |
| `allegrobridge_server.log` | Python daemon: startup, framing, timeouts, pipe state | `setup_logging(file=…)` in the daemon |
| `allegrobridge_skill.log` | SKILL-side IPC server log | `pyShowLog` |
| `allegrobridge_script.log` | stdout/stderr of an IPC-spawned script | `pyRunScript` |

All three are written to `ALLEGROBRIDGE_LOG_DIRECTORY` (default: Allegro's
working directory).

The daemon's level comes from the CLI:

```text
pyStartServer(?id "7777" ?logLevel "DEBUG")
```

The server log records every request, timeout, and pipe state transition — the
first place to look when a call hangs or the connection drops.

## Don't mix configs

Use `setup_logging()` **or** `logging.basicConfig()`, not both — otherwise
records can be emitted twice. `setup_logging()` is the recommended path (richer
console, per-channel levels, no root pollution).
