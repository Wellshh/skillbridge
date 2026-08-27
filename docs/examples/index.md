# Examples

Task-oriented recipes, each one page. All of them assume a connected session:

```python
from allegrobridge import Allegro

with Allegro.launch("designs/demo.brd") as allegro:
    pcb = allegro.session
    ...
```

- [Basic queries](basic.md) — board info, components, nets, and pins
- [Moving a component](move-component.md) — direct writes and dry-run previews
- [Batching writes](batch.md) — several edits in one transaction
- [Vias and routes](vias-routes.md) — placing vias and creating routes
- [Raw AXL recipes](raw-axl.md) — when the typed APIs do not cover your call
