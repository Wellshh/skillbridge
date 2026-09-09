# Project instructions

- Preserve unrelated work, existing conventions, and explicit compatibility requirements.
- Reuse existing implementations. Add dependencies or abstractions only for demonstrated needs; validate at trust boundaries rather than repeating established invariants.
- Propose a short plan for major architectural changes and respect explicit approval stages. Continue routine authorized work without redundant confirmation.
- Commits, pushes, publishing, messages, application restarts, and persistent memory writes require authorization for that action. Use Conventional Commits when a commit is authorized.

## Architectural constraints

- Target Allegro 17.2-2016 S048. A SKILL transaction mark belongs to one command/RPC; never carry it across calls.
- Transactional writes and `Session.batch()` are atomic; raw `Workspace.transaction.batch()` uses savepoints and permits partial success.
- `drc.check()` and CLI-only `routes.connect()` are immediate operations whose effects cannot reliably be rolled back. Do not give them preview or batch semantics.
- Never automatically replay a failed write. A transport or result-validation error does not establish that the database was rolled back.
- Destructive integration tests use disposable board copies, owned Allegro processes, and unique ports. Do not mutate a user's manual session or close resources the test does not own.

## Evidence and validation

- For Cadence API or SKILL work, use `.agents/skills/cadence-skill-agent/SKILL.md`. For other external API, version, or configuration assumptions, verify relevant documentation; prefer Context7 for third-party libraries and official OpenAI documentation for OpenAI products. Reuse evidence already obtained for this task.
- Use nearby tests and project tools to validate observable behavior. Bug fixes need a regression that fails on the previous implementation. Do not add production branches or artificial tests just to satisfy coverage.
- Explain non-obvious ownership, platform behavior, and invariants in concise comments where useful.
- Report what changed, validation evidence, and remaining limits. Distinguish local/static checks from Windows Allegro, GUI, hardware, or production validation.

## Sources and workflows

- `docs/architecture.md` describes the layers; verify current behavior against implementation and callers. `allegrobridge/PLAN.md` contains historical decisions, not an unconditional implementation mandate.
- `docs/skill-testing.md` contains validation and isolation guidance; `pyproject.toml`, `.github/workflows/pythonpackage.yml`, and `tests/skill/run.ils` define the executable checks and coverage thresholds.
- `benchmark/README.md` defines comparable Windows performance evidence.
- `.agents/skills/cadence-skill-agent` is the canonical shared Cadence source. Use its synchronization workflow; do not hand-edit generated indexes, pagination manifests, or agent copies.
