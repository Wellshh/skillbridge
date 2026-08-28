# Writing Extensions

Extensions add your own domain APIs to `Session` without touching the core
package. They are lazily imported, bound to the session, and cached.

## Contract

1. **Location** — create `allegrobridge/client/api/extensions/<name>.py`
   (`<name>` must be a lowercase Python identifier).
2. **Implementation** — subclass `SessionApi` and mark the class with
   `@extension`.
3. **Constraint** — exactly one `@extension` class per module. Classes merely
   imported into the module are ignored (`__module__` must match).
4. **Usage** — access via `session.ext.<name>`. The first access imports the
   module, loads the server-side SKILL file if needed, and caches the instance.

## Server side

If the extension calls SKILL procedures that are not part of the core runtime,
declare them with `@read` / `@write` and provide
`allegrobridge/server/extensions/<name>.il` defining those procedures. On first
use, `Workspace._ensure_extension` loads the `.il` file and verifies every
declared procedure is callable, raising `ExtensionError` otherwise. An
extension whose methods only compose existing procedures needs no `.il` file.

## Example

`allegrobridge/client/api/extensions/stackup.py`:

```python
from __future__ import annotations

from pydantic import TypeAdapter

from allegrobridge.client.base import RpcArgs, SessionApi, extension, read

_MATERIALS = TypeAdapter(list[str])


@extension
class StackupApi(SessionApi):
    @read('__abListMaterials', _MATERIALS)
    def materials(self) -> RpcArgs:
        return ()
```

`allegrobridge/server/extensions/stackup.il`:

```skill
(defun __abListMaterials ()
  ;; return a list of material names
  ...)
```

Usage:

```python
mats = session.ext.stackup.materials()
```

!!! note

    A SKILL procedure that returns an empty list yields `nil` on the wire,
    which decodes as Python `None`. List-typed reads coerce that back to `[]`
    automatically — you do not need a special adapter for empty results.

## Failure semantics

- Unknown name → `KeyError`/`AttributeError` (not cached, retried each time).
- Import error, missing `.il`, or failed readiness check → `ExtensionError`,
  cached: subsequent accesses re-raise the same error. Restart the session to
  retry after fixing the extension.
- Loading is serialized by a lock, so concurrent first access from multiple
  threads loads the extension exactly once.
