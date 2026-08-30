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

`skillbridge/server/_pipe.py` — exactly one request is in flight per server.
Every call has a timeout; a late answer arriving after its timeout is drained
and discarded instead of corrupting the next response. The pipe is a state
machine with three terminal states:

- `DESYNCHRONIZED` — a reply could not be matched to a request
- `BROKEN` — an unrecoverable protocol violation
- `CLOSED` — shut down cleanly

Once terminal, every further call raises the matching `SkillPipe*Error`
immediately instead of hanging.

## Structured errors

`skillbridge/exception.py` — every failure carries a machine-readable `code`,
a human-readable hint, and the offending wire payload. AllegroBridge adds its
own subclasses on top; see [Exceptions](exceptions.md).
