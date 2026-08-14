# SkillBridge refactor v2

This version adds explicit SKILL response framing and safe late-response
recovery while retaining the original line protocol as a compatibility mode.

## Modes

### Existing SKILL code, no protocol change

```bash
python -m skillbridge.server 5000 DEBUG --force-tcp --timeout 30 \
  --skill-protocol line
```

A response timeout is fail-closed and requires a bridge restart.

### Framed protocol with recoverable timeouts

Load/adapt `skill/skillbridge_framing.il`, then run:

```bash
python -m skillbridge.server 5000 DEBUG --force-tcp --timeout 30 \
  --skill-protocol framed --recover-timeouts --drain-timeout 30
```

Framed responses are:

```
STX + success payload + RS
NAK + error payload + RS
```

A timeout moves the channel to `DRAINING`.  No new command is written until one
complete late frame is discarded.  The channel then returns to `READY`.  If the
late frame never arrives before `drain-timeout`, the channel becomes
`DESYNCHRONIZED` and must be restarted.

## Tests

```bash
PYTHONPATH=src pytest
pytest tests/unit
pytest -m integration
```

The integration suite uses real TCP sockets and a real subprocess with text
pipes.  GitHub Actions runs the suite on Windows, macOS, and Linux with Python
3.10 and 3.13.
