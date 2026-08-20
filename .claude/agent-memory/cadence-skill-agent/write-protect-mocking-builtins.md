---
name: write-protect-mocking-builtins
description: SKILL cannot redefine internal (C-built-in) functions even under debugMode; the only mock path is a user-defined wrapper the SUT calls instead of the built-in
metadata:
  type: reference
---

SKILL has TWO distinct redefinition guards on built-ins, and they are NOT the same flag:

1. **Write-protect bit** — settable per-function via `setFnWriteProtect( s_name ) => t | nil` (`sklangref/funcprog.part02.md:307`). Unary, only SETS the bit; no clear variant, no `remFnWriteProtect`/`clearFnWriteProtect` in any index. `getFnWriteProtect` reads it (`sklangref/funcprog.part01.md:1059`).
2. **"internal" / C-built-in attribute** — a SEPARATE, undocumented, non-clearable flag on C-level primitives (`ipcBeginProcess`, `ipcKillProcess`, `ipcWait`, `plus`, etc.). `putd` checks this BEFORE the write-protect bit and errors: `*Error* putd: given function is internal and can not be redefined - ipcBeginProcess`. No SKILL function is documented to read or clear this attribute.

`sstatus(debugMode t)` ("Allows you to redefine write-protected SKILL functions", `sklangref/core.md:829`) lifts ONLY guard #1 (the write-protect bit). It does NOT touch the "internal" attribute (guard #2). Verified: `putd('ipcBeginProcess mock)` STILL fails with the "internal" error under debugMode. `(sstatus writeProtect nil)` is likewise useless here — it governs only first-time definitions (`sklangref/core.md:835`).

**No advice/wrapper facility exists in SKILL.** Confirmed by searching `sklang_api_index.part*.md`, `api_index.part*.md`, and `skoopref/`:
- No `defadvice`, `fset`, `beforeMethod`/`afterMethod`/`aroundMethod`, no CLOS-style method combination. SKILL++ generic methods support `defmethod` primary methods only — no qualifiers.
- The only "trace" family is debug-observation: `tracef`/`untrace`/`tracev`/`tracep`/`tracelevlimit` (`skdevref/skdevref.part04.md:631+`). `tracef` "Shows the functions called with their evaluated arguments and return values" — pure instrumentation, NOT behavior substitution. Cannot be used to mock.
- `alias( s_aliasName s_functionName )` (`sklangref/funcprog.part01.md:49`) only creates a NEW name pointing at an existing function; it cannot redirect an existing built-in symbol to a new definition, and the docs warn "Use alias only to speed up interactive command entry and never in programs."
- No `traceFunc`/`hiRegTraceFunc`/`funconv`/`hook`/`registerFunc` in any index (Allegro `axl*` or generic `sk*`).

**Definitive conclusion:** Mocking/intercepting/redefining an internal C-built-in is IMPOSSIBLE in SKILL. The ONLY way to make such a call mockable is to refactor the SUT to call a user-defined thin wrapper, e.g. `defun(__pyIpcBeginProcess @rest args apply('ipcBeginProcess args))`, which the test CAN `putd` (user-defined functions are not "internal"). This is the required testability pattern for any code that calls `ipcBeginProcess`/`ipcKillProcess`/`ipcWait` directly.

Related: [[skill-ils-value-slot-globals]]
