# Writing Extensions

Extensions are ordinary typed `SessionApi` classes. The API class declares
its packaged SKILL resource with `SkillModule`; applications attach it
explicitly with `session.bind(ApiType)`.

## Contract

1. Subclass `SessionApi`.
2. Set `module = SkillModule(package, resource)` on the class.
3. Declare remote operations with `@read`, `@direct`, or `@write`.
4. Bind the class with `session.bind(ApiType)`. Binding returns the precise API
   type and caches one instance per session.

## Example

`my_plugin/api.py`:

```python
from pydantic import TypeAdapter

from allegrobridge import SkillModule
from allegrobridge.client.api import RpcArgs, SessionApi, read

_MATERIALS = TypeAdapter(list[str])


class StackupApi(SessionApi):
    module = SkillModule('my_plugin', 'server/stackup.il')

    @read('__abListMaterials', _MATERIALS)
    def materials(self) -> RpcArgs:
        return ()
```

`my_plugin/server/stackup.il`:

```skill
(defun __abListMaterials ()
  ...)
```

Usage:

```python
from my_plugin.api import StackupApi

stackup = session.bind(StackupApi)
materials = stackup.materials()
```

The package must include the `.il` resource. AllegroBridge checks all declared
procedures in one RPC, loads the resource synchronously when needed, then
checks readiness again. The temporary path from `importlib.resources` is never
cached.

!!! note

    A SKILL procedure that returns an empty list yields `nil` on the wire.
    List-typed reads coerce that back to `[]` automatically.

## Failure semantics

- Missing resource, load failure, or failed readiness check raises
  `ExtensionError`.
- Module load state is shared by `SkillModule`; two API classes may reuse one
  resource while checking their own procedures independently.
- Instances and readiness errors are cached per API class and session.
- Binding is serialized, so concurrent calls return the same API instance.
