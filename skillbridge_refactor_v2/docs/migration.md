# Migration from the line-only server

## Phase 1: drop-in replacement

Run with `--skill-protocol line`.  No SKILL-side change is required.  Windows
now supports timeout, all requests are serialized across write and response,
and socket framing uses exact reads plus `sendall()`.

A response timeout remains fail-closed in this phase.  Restart the bridge before
sending another command.

## Phase 2: explicit SKILL frames

1. Load or merge `skill/skillbridge_framing.il` into the existing SKILL startup
   file.
2. In the current IPC data callback, replace the old one-line response write
   with `SBWriteSuccess(ipcId result)` and use `SBWriteFailure(...)` on error.
3. Start the Python server with `--skill-protocol framed`.
4. Leave timeout recovery at its framed default, or pass
   `--recover-timeouts --drain-timeout 30` explicitly.

Do not enable recovery while the SKILL side still emits line responses.  The
CLI rejects that combination because a late line has no reliable frame
boundary.

## Operational behavior

- `READY`: a command may start.
- `EXECUTING`: one command is in flight.
- `DRAINING`: the caller timed out; no new command is written while the daemon
  waits for and discards the late frame.
- `DESYNCHRONIZED`: recovery failed or unsolicited protocol data appeared;
  restart is required.
- `BROKEN`: the pipe or frame parser failed; restart is required.

The reserved socket command `$health` returns a JSON snapshot without touching
SKILL.  It is useful for a daemon monitor or readiness probe.
