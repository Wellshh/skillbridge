---
name: context7-docs-first
description: Verify external library API, version, or configuration assumptions when they materially affect implementation, debugging, or review.
---

# Documentation checks

Check documentation when the task depends on unfamiliar API behavior or a version-sensitive assumption. A technical keyword alone is not a reason to query.

- Identify the relevant dependency version from the project.
- Reuse documentation already obtained for that version and behavior during this task.
- For third-party libraries, use Context7 `resolve-library-id` and `query-docs` for the specific question. If unavailable or insufficient, use official upstream documentation and identify the fallback.
- For OpenAI products, use official OpenAI documentation; for Cadence, use the local reference routes in `cadence-skill-agent`.
- Record the source and any constraint that affects the decision. A short note is enough; do not repeat a fixed template for every call.
- If evidence remains inconclusive, identify the unresolved assumption and use a focused check where possible. Do not invent signatures or version compatibility.
