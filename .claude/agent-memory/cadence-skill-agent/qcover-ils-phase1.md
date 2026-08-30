---
name: qcover-ils-phase1
description: Reusable Phase 1 lessons for qcover instrumentation and transactional SKILL++ .ils loading on Windows Allegro
metadata:
  type: reference
---

# qcover `.ils` Phase 1 lessons

- Load transformed `.ils` text with `infile` and `loadPort ?langMode 'ils` inside
  `unwindProtect`, closing the input port on every path. This avoids the Windows
  handle leak observed with the simpler `(load tempFile)` path.
- A saved nil function slot must be represented by a one-element list, such as
  `(list (getd name))`; restore the exact prior slot with `(car snapshot)`.
- `.ils` attempts use attempt-local candidate tables, slot snapshots, and owned
  temp tracking. Rollback restores only the current attempt and old references,
  and must not call the global `reset`, which would undo earlier successful
  sources.
- Reserve `.qcover-*` candidates in the source directory, preserve collision
  safety, and add only successfully loaded candidates to persistent ownership.
  The `.ils` instrumentation/load lifecycle is serial; concurrent qcover loads
  or runs are unsupported.
- The `setof` filter used for candidate-temp differences is correct. A prior
  `setofs` diagnosis was not causal and must not be retained as a fix.
- If `?checkPubFuncs t` cannot load the installation's `cdsFuncs.cxt`, report the
  check as UNAVAILABLE; do not invent or stub the missing context. Use the
  strongest available default/Allegro lint fallback and state its limits.
- Validate each repair round in a fresh Allegro process with a fresh numeric
  port, and express exact expected-red behavior before changing production code.
  Stop after the bounded repair loop when the same failure fingerprint repeats.
- A coverage gate can expose a pre-existing HEAD gap. If the missing outcome is
  reachable through an existing test, add the smallest test extension and state
  that it is coverage completion rather than a production regression fix.
