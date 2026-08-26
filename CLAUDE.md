Implementation 

- Always use TDD (Test Driven Development) - write test before any new features / fixes.
- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.
- For any Cadence API or .il script authoring/modification, strictly follow `cadence-skill-agent` to query local API reference indexes and example codes before writing code.
- DO NOT ADD comments unless the user asks to -- if asked, always provide with the minimum, brief doctstring for function / class defnition or block comment for code snippets.


Testing rules
> For each file respectively, both integration and unit tests needed to reach 100% coverage.
- Before writing tests, inspect the nearest existing unit and integration tests. Match their structure, naming, fixtures, assertions, and style; do not invent a new testing style.
- Organize related tests consistently with `tests/test_integration`. Use test classes only for coherent behavior groups, not merely because the production code uses classes.
- Use fixtures for shared setup, state, or resource lifecycle. Keep pure actions, builders, and assertion utilities as normal helper functions.
- Prefer real dependencies when they are cheap and deterministic. For socket behavior, prefer `socket.socketpair()`; use fakes/mocks only for failure injection or behavior that cannot be reproduced reliably.
- Test observable behavior and protocol contracts, not implementation details such as internal call counts or buffer strategy.
- Concurrency and I/O tests must be deterministic: avoid `time.sleep()` for synchronization, use synchronization primitives, and ensure every potentially blocking operation has a bounded timeout.
- Always clean up sockets, threads, subprocesses, and other resources, including when a test fails.
- For bug fixes and protocol edge cases, add a regression test that would fail with the previous implementation.
- Do not change production APIs solely to make tests easier to write.
- When using unfamiliar or version-sensitive pytest APIs, check the current pytest documentation with Context7 instead of guessing.
- Run the smallest relevant test set first, then the broader affected test suite. Do not weaken or delete existing tests just to make a change pass.

---- 

For both

- Do not add defensive checks for states or inputs already guaranteed by the current contract, types, or callers. Validate only at external/trust boundaries or when explicitly required by the behavior.
- Before adding input validation or an error branch, inspect the actual call sites. Do not speculate about inputs that the current system cannot produce.
- Internal code may rely on established invariants. Do not repeatedly revalidate the same invariant at every layer.
- Do not add guards, exceptions, fallback paths, production branches, or artificial tests solely to satisfy coverage.
- Use the lightest abstraction that preserves the required semantics and type safety. Introduce classes or wrappers only when they provide meaningful behavior, invariants, ownership, or lifecycle management.


---- 

Commit messages

- Follow Conventional Commits, enforced by a commit-msg hook: `type(scope): subject` with type in feat, fix, docs, refactor, test, chore, perf, build, ci, style, revert. Scope is optional; separate any body from the subject with a blank line; keep the Co-Authored-By trailer last.


---- 
Specifically, every time writing .il / .ils code, use local `cadence-skill-agent` first to query local api docs.