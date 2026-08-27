# Testing SKILL code with qtest and qcover

The server-side SKILL code is tested where it runs: inside Allegro. The test
suite lives in `tests/skill/` and is built from two parts:

- **qtest** (`tests/skill/qtest/src/qtest/`) — a unittest-style framework,
  vendored from MatthewLoveQUB's SKILL Tools (MIT).
- **qcover** (`tests/skill/qtest/src/qcover/`) — our extension that adds branch
  coverage for classic SKILL. Written in SKILL++, it instruments `.il` function
  bodies by rewriting every `if`/`when`/`unless`/`cond` condition into a
  counting decision point, then re-loading the transformed definition.

Tests are SKILL++ files (`test_*.ils`). Loading a test file runs its tests.

## Writing a test

```lisp
;;; test_widget.ils - Unit tests for widget.il using qtest

(qcover::load (strcat (qub::scriptDir) "/../../allegrobridge/server/extensions/widget.il"))

(qtest::runSuites
  (qtest::TestSuite ()
    (qtest::TestCase test_widget_projects_name
      (qtest::assertEqual "W1" (__abProjectWidgetName (list nil 'name "W1"))
                          ?msg "name must project"))
    (qtest::TestCase test_widget_known_gap
      (qtest::assertNil nil ?msg "documented gap")
      ?expect_fail t)))
```

- `qtest::TestSuite (bindings) tests...` groups cases; the binding list is
  usually `()`.
- `qtest::TestCase name body...` runs each form in order and stops at the
  first failed assertion. `?skip t` marks the case skipped; `?expect_fail t`
  turns a failure into an expected one (xfail).
- Assertions: `assertEqual`, `assertNotEqual`, `assertTrue`, `assertNil`,
  `assertEq`, `assertMember`, `assertIsInstance`, `assertRaises`,
  `assertAlmostEqual` (`?rel_tol` / `?abs_tol`). All accept `?msg`.
- Uncaught errors inside a case are caught and recorded as failures; they do
  not abort the run.
- To stub a SKILL function, save it with `getd`, replace with `putd`, and
  restore in an `unwindProtect` cleanup form.

## Coverage

- Load the file under test with `qcover::load` instead of `load`. Never load
  it both ways.
- Both outcomes of every condition count, so reaching 100% means exercising
  the true and false branch of each `if`/`when`/`unless`/`cond`.
- Quoted forms (`quote`, backquote) are not instrumented, and the `t` clause
  of `cond` is left alone.
- `qcover::report ?minimum 100.0` prints `covered/total branches` plus one
  line per unhit branch, and errors if the percentage is below the threshold.
  The threshold lives only in `run.ils`, not in individual test cases.
- `qcover::reset` restores the original function definitions.

## Running

`tests/skill/run.ils` is the entry point. It opens the test board
(`allegrobridge/assets/shape1.brd`), loads the framework self-tests and each
project test file, prints the summary table, and fails if any test failed or
coverage is below 100%.

- From the Allegro SKILL console: `load("<repo>/tests/skill/run.ils")`.
- From pytest on Windows: `pytest tests/allegrobridge/test_integration.py -k
  TestSkill` — this copies the suite into a temp dir, launches Allegro, runs
  the suite, and checks the report from Python.

New test files are **not** auto-discovered: add a `load` line for your
`test_*.ils` to the load list in `run.ils`.

## Gotchas

- **Load order matters.** `qtest::` / `qcover::` symbols are resolved when a
  file is *read*, so the framework must be fully loaded before any file that
  references it. `run.ils` handles this with a bootstrap phase that puts
  `qtest/src` on the SKILL path first.
- In SKILL++, write `(f ?port p)`, never `(f(?port p))` — the outer parens
  would re-evaluate the result as a function.
- Helper functions at the top of a test file are fine; cases in one file run
  before the next file is loaded.
