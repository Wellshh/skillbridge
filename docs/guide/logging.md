# Logging

AllegroBridge uses the standard `logging` module on both sides of the bridge.

## Python side

Enable debug output to see process launches, workspace connections, and
SKILL module loads:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

The client-side loggers are:

- `allegrobridge.allegro` — launch, attach, close
- `allegrobridge._runtime` — the spawned Allegro process
- `skillbridge.client.workspace` — workspace open/close

## Server side

The Python server running inside Allegro writes to `skillbridge_server.log`
in Allegro's working directory (override with the `SKILLBRIDGE_LOG_DIRECTORY`
environment variable). Set its level when starting the server:

```text
pyStartServer(?id "7777" ?logLevel "DEBUG")
```

*Skill equivalent:* `pyStartServer(?id "7777" ?logLevel "DEBUG")`

The server log records every request, timeout, and pipe state transition —
the first place to look when a call hangs or the connection drops.
