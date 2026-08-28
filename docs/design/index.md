# Design Notes

Short design memos on how AllegroBridge is built and why — the trade-offs
behind the implementation, with pointers into the code. Written for
contributors and curious users; none of this is required for using the
library.

- [Expression AST](expression-ast.md) — how remote expressions become a lazy
  tree that compiles to SKILL
- [Reducing round trips](reducing-rtt.md) — what a remote call costs, and how
  the API is shaped to amortize IPC
