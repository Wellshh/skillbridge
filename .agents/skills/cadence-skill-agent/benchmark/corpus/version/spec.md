# Task: __abpBenchVersion

Write a SKILL proc `__abpBenchVersion` that takes no arguments and returns the full Allegro version string via `(axlVersion 'fullVersion)`. The proc must be loadable on Allegro 17.2 and return a string.

This is a benchmark corpus task. The oracle (`oracle.il`) is the known-good implementation. To produce `agent.il`, run the cadence-skill-agent against this spec and save its output as `agent.il` in this directory; the Tier C harness verifies whichever of `agent.il` / `oracle.il` is present.
