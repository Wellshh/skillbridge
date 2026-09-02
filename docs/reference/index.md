# Reference

The public surface, importable names first.

## Top level

```python
from allegrobridge import Allegro, OpenMode, Session, Workspace
```

| Name | Purpose |
| --- | --- |
| [`Allegro`](allegro.md) | an open Allegro window connected to a workspace |
| [`OpenMode`](allegro.md) | `'cli' \| 'manual'` literal for `Allegro.open` |
| [`Session`](session.md) | the typed facade over the raw workspace |
| [`Workspace`](workspace.md) | the raw workspace: all 792 `axl*` functions |

## Domain APIs and records

```python
from allegrobridge.client.api import (
    Batch,
    Cmd,
    CmdResult,
    BoardApi,
    AbBoard,
    ComponentsApi,
    AbComponent,
    DrcApi,
    AbDrc,
    LayersApi,
    AbLayer,
    NetsApi,
    AbNet,
    PadstacksApi,
    AbPadstack,
    PinsApi,
    AbPin,
    RoutesApi,
    AbRoute,
    Point,
    ShapesApi,
    AbShape,
    BBox,
    SymbolsApi,
    AbSymbol,
    ViasApi,
    AbVia,
)
```

See [Domain APIs and DTOs](domain-apis.md) and
[Batch and commands](batch.md).

## Exceptions

```python
from allegrobridge.exceptions import AllegroError, ExtensionError, ...
```

See [Exceptions](exceptions.md).

## Kernel internals

The vendored skillbridge kernel, documented as concept pages:
[Protocol](protocol.md) and [Remote objects](remote-objects.md). The wrappers
for SKILL values come from the kernel and are re-exported by `skillbridge`:

```python
from skillbridge import Symbol, Key, SkillCode
```
