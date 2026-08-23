---
name: context7-docs-first
description: Use before implementing or modifying code that depends on external library APIs, especially CGAL, pybind11, CMake, Boost, Catch2, nlohmann/json, or Codex plugin/skill configuration.
---

# Context7 Docs First

Before writing code or config that depends on a library API, ground the task in current official docs.

## Required process

1. Identify each external library or tool involved.
2. Use Context7 MCP `resolve-library-id` to find the library ID.
3. Use Context7 MCP `query-docs` for the precise topic, version, and API.
4. Record a short docs note before editing code:
   - library/version if known
   - package/class/function names to use
   - constraints and pitfalls
   - docs source used
5. If Context7 cannot retrieve the docs, use the official upstream docs and say so in the task summary.

## Required for these keywords

Always trigger for:

- CGAL, EPECK, EPICK, Polygon_set_2, General_polygon_set_2, Arrangement_2, Straight_skeleton_2, Minkowski_sum_2, Polygon_repair, AABB_tree
- pybind11, py::class_, py::enum_, GIL, Python extension module
- CMake, find_package, FetchContent, install target, export target
- Boost R-tree, nlohmann/json, Catch2, GoogleTest
- Codex skill, plugin, AGENTS.md, MCP config

## Output format for docs notes

```text
Docs checked:
- Library:
- Context7 library id:
- Topic:
- APIs confirmed:
- Constraints/pitfalls:
- If docs unavailable, official fallback used:
```
