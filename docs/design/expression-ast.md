# Expression AST

!!! warning "Work in progress"
    This note is a placeholder — the full write-up lands with the AST
    refactor. The outline below is the contract for what it will cover.

## Outline

- Why interpolating SKILL snippets as strings does not scale: quoting,
  precedence, and composition bugs
- The expression tree in `skillbridge/client/expr.py`: nodes mirror SKILL
  operators, evaluation stays lazy
- Compilation into SKILL source by the translator; interaction with
  `RemoteFunction` chaining and `Var` bindings
- What this buys: composable queries and a single round trip per evaluation
