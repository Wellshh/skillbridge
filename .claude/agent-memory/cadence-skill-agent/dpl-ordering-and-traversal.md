---
name: dpl-ordering-and-traversal
description: Disembodied property list (DPL) ordering is unspecified for ->?/->??/propNames; DPL storage is LIFO; walk raw list with cddr for deterministic order
metadata:
  type: reference
---

Findings when authoring SKILL `.il` code that traverses a disembodied property list `(nil k1 v1 k2 v2 ...)` in a defined order.

**`->?` / `->??` / `propNames` order is NOT guaranteed.**
- `propNames(g_propList)` — the dedicated function to list DPL property names — explicitly states: "Order of returned property names is unspecified." Source: `algroskill/27langexten.md:359` (entry starts :347).
- `struct->?` for defstructs returns slot names only (NOT values), and the documented examples come out reversed from definition order: `struct->? => (slot3 slot2 slot1)` (`sklangref/datastruct.md:253`), `aCard->? => (faceUp suit rank)` vs defstruct `(card rank suit faceUp)` (`sklanguser/chap4.md:793`). So even for defstructs the order is not construction order.
- `->` / `getq` DO work on a DPL: `x = '(nil a 3 b 4); x->a => 3; get(x 'a) => 3` (`sklangref/dataoperator.md:204`, `get` entry :170, `getq`/`->` entry :248).

**DPL physical storage is LIFO (reverse-insertion).**
- `complex1 = trMakeComplex(?real 2 ?imaginary 3) => (nil imaginary 3 real 2)` — `real` assigned first but appears AFTER `imaginary` in the list (`sklanguser/chap4.md:237`, DPL section starts :223). New `->` assignments push the pair to the front (right after the head).

**Implication for deterministic traversal.** Walk the RAW list with `car`/`cadr`/`cddr` (step one pair = one `cddr`). This yields physical storage order (deterministic), which for a `->`-built DPL is reverse-insertion; for a literal `list(nil 'k1 v1 'k2 v2)` it is the literal/construction order. Do NOT rely on `->?`/`->??`/`propNames` for ordering.

**Supporting API locations (sklangref):**
- `while` syntax form — `sklangref/controlflow.md:1511` (signature :1513, stops when condition is nil, always returns `t`). Both `while(...)` and `(while ...)` forms are used in golden `.il` examples.
- `let` SKILL mode — `sklangref/funcprog.part01.md:1317`; bindings list of `(s_variable g_value)`; body any number of exprs. `=` (infix setq) assignment to a let-bound local inside the body is legal/idiomatic (e.g. `result = ncons(nil)` inside `let((result)...)` at `sklanguser/chap4.md:233`).
- `cddr` exists directly — part of `ca|d[a|d][a|d][a|d]r` family, all combos up to 4 chars, `sklangref/list.md:98` (enumeration at :104).
- `append` — non-destructive of `l_list1` (duplicates top-level cells), shares `l_list2`; slow, `sklangref/list.md:9` (note at :21).
- `nconc` — destructive; modifies last cdr of `l_arg1`; `nconc(x x)` forms infinite structure; `sklangref/list.md:545` (warnings :553, example :576).
- `%s` prints string without quotes — `sklangref/inputoutput.part01.md:524`; `%L` adds quotes (default format) — `sklangref/typeconv.md:258`, format-table row `inputoutput.part01.md:530`; `lsprintf` is lambda version of `sprintf` — `sklangref/stringfunc.part01.md:167` (example :193 shows `%s`→`hello`, `%L`→`("world")`).

Related: [[skill-path-handling-apis]].
