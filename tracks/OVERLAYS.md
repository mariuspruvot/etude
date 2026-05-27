# Curated overlays — contributor reference

An **overlay** adds a framework/library path on top of a language track's core (e.g. FastAPI
on Python). It is a **separate schema** from `curriculum.md` and is validated by
`tools/lint_overlay.py` (the core `lint_curriculum.py` never sees overlay files). Overlays are
how a popular **personal extension** (`progress/<track>/extensions.md`) graduates to shared,
linted content. Full design: `docs/specs/2026-05-27-etude-v1.3-overlays-design.md`.

## Location & schema

`tracks/<parent_track>/overlays/<name>.md`:

```markdown
---
kind: overlay                 # required, must be exactly "overlay"
parent_track: python          # required, must match tracks/<parent_track>/curriculum.md
name: fastapi                 # required; also the concept namespace prefix
display_name: FastAPI
target_version: "0.11x"
freshness_source: context7
maintainers: [community]
concepts:
  overlay: [fastapi:routing, fastapi:di]   # required, non-empty; every id starts with "<name>:"
  requires_parent: [async-await, type-system]  # parent concepts this builds on (must exist in parent)
---

# FastAPI — Overlay (on the Python core)

### o01 — Routing
- id: o01
- concepts: [fastapi:routing]
- prerequisites: [parent:async-await]   # parent:<c> (c in requires_parent) or an earlier oNN
### o02 — Dependency injection
- id: o02
- concepts: [fastapi:di]
- prerequisites: [o01]
```

## Rules the linter enforces
- `kind: overlay`, `parent_track`, `name` present; `parent_track` resolves to a real core curriculum.
- `concepts.overlay` is a non-empty list; every concept is namespaced `<name>:`.
- Overlays **must not** declare `transverse` concepts (frameworks claim no cross-track transfer).
- `requires_parent` concepts must exist in the parent track's declared concepts.
- Each module `concepts:` entry is a declared overlay concept.
- Each module `prerequisites:` entry is either `parent:<concept>` (in `requires_parent`) or an
  **earlier** `oNN` module in the file (document order ⇒ no cycles).

## Promotion: personal extension → overlay
| `progress/<track>/extensions.md` | `tracks/<lang>/overlays/<name>.md` |
|---|---|
| ids `xNN`, concepts `personal:foo`, not linted | ids `oNN`, concepts `<name>:foo`, linted |

Rename the `personal:` prefix to `<name>:`, switch ids to `oNN`, add the `kind`/`parent_track`/`requires_parent` frontmatter, fill `resources` with current docs, open a PR.
