# Protocols

## Client ↔ Python daemon

The existing socket protocol is retained:

```
10-byte right-aligned ASCII decimal length + UTF-8 payload
```

Both header and payload are read exactly; writes use `sendall()`.

## Python daemon ↔ SKILL

### Compatibility mode: `line`

One command line produces exactly one response line.  Because a late line
cannot be distinguished safely from the next response, a response timeout moves
the channel to `DESYNCHRONIZED` permanently.

### Framed mode: `framed`

```
STX (0x02) + success payload + RS (0x1E)
NAK (0x15) + error payload   + RS (0x1E)
```

The payload may contain newlines.  A NAK response raises `SkillExecutionError`
but returns the channel to `READY`.

After a response timeout, the state becomes `DRAINING`.  The next complete
frame is known to belong to the timed-out request, so it is discarded.  The
state then becomes `READY`; no new command is written before that transition.
If no late frame arrives before `drain_timeout`, the channel becomes
`DESYNCHRONIZED` and must be restarted.
