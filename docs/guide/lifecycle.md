# Process lifecycle

An `Allegro` instance owns one Allegro window and the workspace connected to
it. There are three ways in:

```python
Allegro.launch(board=None, *, workspace_id=None, executable="allegro.exe",
               timeout=120.0, force_tcp=False)
Allegro.connect(workspace_id=None, *, board=None, force_tcp=False)
Allegro.open(mode=..., ...)   # dispatches: "cli" -> launch, "manual" -> connect
```

Use `open()` when the choice comes from configuration; call `launch()` or
`connect()` directly otherwise.

## Launching

`Allegro.launch()` resolves the executable, builds a startup script that loads
both SKILL servers, plants a random launch token, starts the process, and polls
until the workspace answers.

- `board` — a `.brd` to open right away. `None` starts Allegro without a
  design. A missing file raises `AllegroFileNotFoundError` before anything is
  launched.
- `executable` — default `allegro.exe`. Resolved against `PATH` and the
  `tools/bin` directory of a Cadence installation found via the `CDSROOT` or
  `Sigrity_EDA_DIR` environment variables. If nothing matches,
  `AllegroFileNotFoundError` tells you to pass the full path.
- `timeout` — seconds to wait for the server to come up (default 120). On
  expiry, `AllegroTimeoutError`. If Allegro exits before the server is ready,
  `AllegroLaunchError` carries the exit code.

!!! note "Identity token"

    Each launch plants a random token inside the Allegro process. Before the
    workspace is handed to you, the client reads the token back and compares —
    if another client already attached, or you hit a stale server on the same
    workspace id, `AllegroServerIdentityError` is raised instead of silently
    driving the wrong window.

## Attaching

`Allegro.connect()` (and `open(mode="manual")`) attaches to a server you
started yourself with `pyStartServer`. The board argument is optional and only
recorded on the object — attaching never opens designs.

## Workspace id and transport

The workspace id selects the channel. On Windows the id is a TCP port and
defaults to `"7777"`; on Linux it is a Unix socket name and defaults to
`"default"`. Pass `force_tcp=True` to use TCP on Linux as well.

*Skill equivalent:* `pyStartServer(?id "7777")` on the Allegro side,
`Allegro.open(mode="manual", workspace_id="7777")` on the Python side.

## Closing

`Allegro` is a context manager; prefer it. `close()` shuts the workspace down
and, for launched sessions, tears down the whole Allegro process tree.
Attached sessions only close the connection — your Allegro window stays open.

```python
with Allegro.launch("designs/demo.brd") as allegro:
    ...
# process gone here

allegro = Allegro.connect()
...
allegro.close()  # window keeps running
```
