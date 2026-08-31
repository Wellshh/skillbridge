# AllegroBridge

![build](https://github.com/Wellshh/allegrobridge/actions/workflows/pythonpackage.yml/badge.svg)

A Python bridge to Cadence Allegro PCB Editor 17.2. Query the design database,
move components, place vias, and compose edits inside atomic SKILL
transactions, through a typed, pydantic-validated API.

### Prerequisites

- Python 3.10 or higher
- pip
- Cadence Allegro PCB Editor 17.2 (Windows is the primary target; Linux works over TCP)

### Features

- Run Allegro's AXL/SKILL functions from Python
- Process lifecycle: launch Allegro from Python, or attach to a running session with an identity-checked handshake
- Atomic transactions: every write runs in an atomic transaction, with savepoint batches and dry-run previews
- Typed domain APIs (board, components, layers, nets, padstacks, pins, symbols, vias, routes, shapes, drc) returned as frozen pydantic models
- Raw AXL access: all 792 documented `axl*` functions with snake_case names; PEP 561 type stubs ship pre-generated (autocompletion, signature hints, and docstrings in the IDE, no user-side generation step)
- Extensions: bind typed API classes whose packaged SKILL modules load lazily on first use
- SKILL-side testing: vendored qtest framework plus qcover, a branch-coverage instrumenter for classic SKILL

The generated stubs give every `axl*` function autocompletion, signature hints,
and docstrings in the IDE:

![IDE autocompletion demo](docs/assets/ide_completion.gif)

Read more in the [full documentation](https://github.com/Wellshh/allegrobridge).

### Installation

```bash
pip install git+https://github.com/Wellshh/allegrobridge.git
```

AllegroBridge vendors a modified `skillbridge` package and cannot coexist with
the upstream `pip install skillbridge` in the same environment — uninstall the
upstream package first.

Before you can use the bridge you must load the server scripts in Allegro.

1. Type `allegrobridge path` into your shell to acquire the correct `PATH-TO-SERVER`
2. Open Allegro PCB Editor
3. Type these commands into the SKILL console
    - `load("PATH-TO-SERVER/python_server.ils")`
    - `load("PATH-TO-SERVER/allegro_server.il")`
    - `pyStartServer(?id "7777")`

### Updating

In order to update the python package type this

```bash
pip install git+https://github.com/Wellshh/allegrobridge.git --upgrade
```

### Examples

**_Note:_** All these examples assume that the SKILL server is running. You can
start it by typing `pyStartServer(?id "7777")` into the SKILL console after
loading the server scripts.

##### Attaching to a running server

```python
from allegrobridge import Allegro

with Allegro.open(mode="manual", workspace_id="7777") as allegro:
    ...
```

##### Launching Allegro from Python

```python
from allegrobridge import Allegro

with Allegro.launch("designs/demo.brd") as allegro:
    pcb = allegro.session
```

##### Reading the board and moving a component

```python
board = pcb.board()  # frozen pydantic model
r101 = pcb.components["R101"]
pcb.components.move("R101", x=120.0, y=45.0, rotation=90.0)  # atomic transaction
```

##### Raw workspace: call any SKILL function

```python
from allegrobridge import Workspace

ws = Workspace.open("7777")
>>> ws['plus'](3, 4)
7
```

*equivalent to:*

```lisp
(plus 3 4)
```
