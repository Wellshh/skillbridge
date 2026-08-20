---
name: write-protect-mocking-builtins
description: How to redefine already write-protected SKILL built-ins (e.g. ipcBeginProcess) in tests — debugMode, not writeProtect or setFnWriteProtect
metadata:
  type: reference
---

To mock/replace an already write-protected built-in (e.g. `ipcBeginProcess`, `ipcKillProcess`, `ipcWait`) in a test, the only documented mechanism is `sstatus(debugMode t)` — "Allows you to redefine write-protected SKILL functions" (`sklangref/core.md:829`).

**Wrong tools (common mistakes):**
- `setFnWriteProtect( s_name ) => t | nil` (`sklangref/funcprog.part02.md:307`) — unary, only SETS the bit; returns `nil` if already protected. No "clear" variant exists; no `remFnWriteProtect`/`clearFnWriteProtect` in any index.
- `(sstatus writeProtect nil)` — governs only FIRST-TIME definitions ("all functions being defined for the first time are not write-protected", `sklangref/core.md:835`). Does NOT lift the existing per-function bit on built-ins. The `let`/`sstatus writeProtect nil` pattern in `sklanguser/chap10.md:547` is for letting new `procedure` defs be unprotected, not for redefining existing protected ones.

**Canonical save/mock/restore sequence:**
1. `origFn = getd('ipcBeginProcess)` — funobj
2. `priorDebug = status(debugMode)`
3. `sstatus(debugMode t)`
4. `putd('ipcBeginProcess <lambda>)`
5. run test
6. `putd('ipcBeginProcess origFn)`
7. `sstatus(debugMode priorDebug)`

**Caveat:** `debugMode` does not change `getFnWriteProtect`'s return (still `t`); it only suppresses the redefinition guard in `def`/`putd`. So a preflight guard like `(when (getFnWriteProtect name) error)` is the wrong predicate — it rejects mocks that would actually succeed under debugMode. Gate on `(status debugMode)` instead, or just attempt the `putd`.

`getFnWriteProtect` signals an error if the symbol has no function definition — safe for real built-ins, wrap for unknown symbols.

Related: [[skill-ils-value-slot-globals]]
