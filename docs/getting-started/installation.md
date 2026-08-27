# Installation

## Requirements

- Cadence **Allegro PCB Editor 17.2** (Windows is the primary target; Linux
  works over TCP)
- Python **>= 3.10**

## From the repository

```bash
pip install git+https://github.com/Wellshh/allegrobridge.git
```

!!! warning "Conflicts with `pip install skillbridge`"

    AllegroBridge vendors a modified `skillbridge` package. It cannot coexist
    with the upstream package in the same environment — uninstall the upstream
    package first.

## Verify the installation

```bash
allegrobridge path
```

This prints the two `load("...")` lines you need on the Allegro side (see the
[quickstart](quickstart.md)).

## Development install

```bash
git clone https://github.com/Wellshh/allegrobridge.git
cd allegrobridge
poetry install
pytest -m "not allegro"          # everything except on-machine Allegro tests
pytest -m allegro --allegro      # requires a running Allegro instance
```

To build this documentation locally:

```bash
pip install -e ".[doc]"
mkdocs serve
```
