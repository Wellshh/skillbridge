# Protocol

The kernel moves SKILL code strings to Allegro and values back over a framed
socket. This page describes the wire format; you normally never see it.

## Transport frames

`skillbridge/protocol/socket.py` — every message is a 10-byte ASCII length
header followed by the payload:

```text
0000000031axlDBGetDesign()->name
└──┬───┘└──────────┬──────────┘
  header        payload (31 bytes)
```

Payloads are capped at 64 MiB (`DEFAULT_MAX_PAYLOAD_SIZE`); a longer frame
raises `FrameTooLargeError` before anything is sent. The channel is TCP on
Windows and a Unix socket on Linux (`force_tcp=True` selects TCP everywhere).
Unix endpoints use a stable advisory `.lock` held for the server lifetime.
Active endpoints are never unlinked; only a same-identity stale socket that
returns a bounded `ECONNREFUSED` probe may be reclaimed. The lock file is
intentionally retained after shutdown and must not be manually removed while
a cooperating server may still be running.
An oversized or malformed response header is a framing failure: the old
connection is discarded and reconnection is attempted, while the original
protocol exception is returned and the failed command is never replayed.
Local send-side size rejection occurs before transmission and does not trigger
reconnection.

## Response framing

`allegrobridge/_kernel/protocol/response.py` — the server wraps each reply in
control characters so partial reads and stream desynchronization are detectable:

| Frame | Meaning |
| --- | --- |
| `STX … RS` | success payload |
| `NAK … RS` | failure payload |
| `RST … RS` | success payload followed by a server restart |

Within a payload, `ESC` and `RS` are byte-stuffed as `ESC ESC` and `ESC RS`.
Only an unescaped `RS` ends the frame.

A reply that does not start with a known marker raises `InvalidResponseError`.

## The serialized pipe

`allegrobridge/_kernel/server/_pipe.py` — exactly one request is in flight per server.
Each command must be one non-empty logical line. A single terminal `LF` (or
`CRLF`) is accepted and normalized; embedded or extra newlines are rejected as
`<invalid-command>` before anything is written to the SKILL pipe.
Each call accepts a finite timeout; `timeout=None` waits indefinitely. A late
answer arriving after a finite timeout is drained and discarded instead of
corrupting the next response. The pipe is a state
machine with four terminal states:

- `DESYNCHRONIZED` — a reply could not be matched to a request
- `BROKEN` — an unrecoverable protocol violation
- `RESTARTING` — a restart response was delivered; new requests are refused
- `CLOSED` — shut down cleanly

`RESTARTING` is a terminal state after a normal or late `RST`; it rejects new
requests. The reader stops after the complete `RST`, and the shared watcher
waits for active requests to finish (up to a one-second grace period) before
exiting. A local `close()` remains distinct and does not exit the process.

Command writes have a single owning worker. If a write or flush misses its
deadline, the pipe becomes `BROKEN`; the command is not retried, and a later
completion cannot make the pipe usable again. `close()` requests logical
shutdown without promising immediate OS-handle closure; `wait_closed(timeout)`
may remain false while the peer or writer is still draining, and an owning
process may need to terminate or restart when that bounded wait cannot finish.
Closing does not retract bytes already sent or undo a command whose execution
may already have started, so its final result can remain uncertain.

Before the first `execute()` or `close()`, startup notification writes are
owned exclusively by the startup thread; the first command or close transfers
the command stream to the pipe writer worker. No additional notification API
is required.

Once terminal, every further call raises the matching `SkillPipe*Error`
immediately instead of hanging.

## Structured errors

`allegrobridge/_kernel/exception.py` — every failure carries a machine-readable `code`,
a human-readable hint, and the offending wire payload. AllegroBridge adds its
own subclasses on top; see [Exceptions](exceptions.md).
