# FastAPI overlay (on the Python track) — design

**Status:** draft / awaiting user review
**Date:** 2026-05-28
**Predecessors:** `docs/specs/2026-05-27-etude-v1.3-overlays-design.md` (the overlay
**mechanism** — schema + linter + skill awareness — landed in PR #5; this spec is the
first **content** that exercises it).

---

## 1. Purpose

Ship the first real curated overlay in Étude — **FastAPI on the Python track** — and
add a short `## Contributing` section to the README so external contributors know how
to propose a new curriculum or a new overlay.

This is the v1.3 mechanism's first real-conditions test. Success = the file lints,
the skills (`assess`, `teach`, `exercise`, `status`) resolve overlay concepts
correctly without any code change, and a learner who already finished the relevant
Python modules can be routed into FastAPI seamlessly.

## 2. Non-goals

- No change to `tools/lint_overlay.py` or its schema (closed since v1.3).
- No change to the parent `tracks/python/curriculum.md` (closed schema; we only
  **read** its concepts to populate `requires_parent`).
- No change to the integrity hook (`progress/*/exercises/*` stays write-protected
  except `prompt.md`/`feedback.md`).
- No starter exercise files written in advance — `exercise` generates them on demand.
- No second overlay (SQLAlchemy, Pytest plugins, Pydantic-as-library) — out of scope.
- No overlay capstone — the schema does not define one; the four module
  `exercise_seeds` chain into a single toy API and that is enough.

## 3. Deliverables

### A. `tracks/python/overlays/fastapi.md`

A single overlay file with 4 modules (`o01`–`o04`), validated by `tools/lint_overlay.py`.

**Frontmatter:**

```yaml
kind: overlay
parent_track: python
name: fastapi
display_name: FastAPI
target_version: "0.11x"
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - fastapi:routing
    - fastapi:validation
    - fastapi:di
    - fastapi:testing
  requires_parent:
    - type-system
    - typing-generics
    - decorators
    - asyncio
    - testing
    - concurrency
    - dependency-management
    - dataclasses
```

**Concept naming rationale.** `fastapi:validation` (not `fastapi:pydantic-models`)
because the role of Pydantic *inside FastAPI* is validation + serialization
(`response_model`). Keeping the name role-based leaves room for a future standalone
`pydantic` overlay without collision.

**Parent concepts — verified citation.** All eight items in `requires_parent` exist
in the parent `tracks/python/curriculum.md:8-26` (transverse: `type-system`,
`testing`, `concurrency`, `dependency-management`; language_specific:
`typing-generics`, `decorators`, `asyncio`, `dataclasses`).

**Module dependency graph (document order ⇒ no cycles, lint rule 8):**

| id  | concepts             | prerequisites                                    |
|-----|----------------------|--------------------------------------------------|
| o01 | `fastapi:routing`    | `parent:decorators, parent:type-system`          |
| o02 | `fastapi:validation` | `o01, parent:typing-generics, parent:dataclasses`|
| o03 | `fastapi:di`         | `o02, parent:asyncio`                            |
| o04 | `fastapi:testing`    | `o03, parent:testing`                            |

**Module bodies (mastery + exercise_seeds + resources):**

- **o01 — Routing.** Declare an `APIRouter`; expose GET/POST/PUT/DELETE with typed
  params; read `path`/`query`/`body` via annotations; set `status_code` and
  `response_model`; structure with `include_router(prefix=...)`.
  Seed: *"An in-memory `/items` CRUD — 4 routes, correct status codes, typed
  response_model."*
  Resources: tiangolo path-params, query-params, body, bigger-applications.
- **o02 — Validation.** Model inputs/outputs with `BaseModel`; constraints via
  `Field(..., gt=0, max_length=...)`; split input vs output models
  (`ItemCreate`/`ItemOut`); `model_validator`/`field_validator` for business rules;
  know why Pydantic ≠ dataclass *in this context*.
  Seed: *"Extend o01's API — split `ItemCreate`/`ItemOut`, validate `price > 0` and
  `name ≤ 80 chars`, return clean 422."*
  Resources: pydantic models, pydantic validators, tiangolo response-model.
- **o03 — Dependency injection.** Factor a dep with `Depends`; compose
  sub-dependencies; per-request lifecycle; `yield` for open/close (DB session, file);
  inject an async dep without changing the route.
  Seed: *"Add `get_db()` (yields an in-memory dict), a `get_current_user()` reading
  `X-User-Id`, an endpoint `/me/items` combining both."*
  Resources: tiangolo dependencies, dependencies-with-yield.
- **o04 — Testing.** pytest + `TestClient`; override deps via
  `app.dependency_overrides`; assert expected 4xx; know when to prefer
  `httpx.AsyncClient` for async-only routes.
  Seed: *"Cover the previous modules' API — happy-path CRUD, 422 on invalid payload,
  401 without `X-User-Id`, with `get_current_user` overridden."*
  Resources: tiangolo testing, async-tests.

URLs will be verified live (HEAD or WebFetch) before commit; if any has moved, adjust
to the current canonical URL.

### B. README — `## Contributing` section

Placed before `## Requirements` (currently the last section of the README), ~15–20
lines. Single section covers both curriculum and overlay contributions — most of the
process is shared (issue → schema → lint → PR), and the overlay-specific detail lives
in `tracks/OVERLAYS.md` (single source of truth).

Outline:

- One-paragraph intro: Étude grows by **curriculum** or by **overlay**; both go
  through the same loop.
- New curriculum: read an existing track, run `tools/lint_curriculum.py`, keep
  transverse concepts truly transverse.
- New overlay: schema in `tracks/OVERLAYS.md`, run `tools/lint_overlay.py`,
  `<name>:` namespace, no `transverse`, prereqs are `parent:<c>` or earlier `oNN`,
  follow the promotion path from `personal:` extensions when relevant.
- Resources must be official docs; Étude pulls current usage via Context7 at
  teach-time, so don't pin minor versions in `target_version` unless the API
  genuinely diverges.

## 4. Validation / Definition of done

1. `uv run python tools/lint_overlay.py tracks/python/overlays/fastapi.md` passes.
2. `uv run pytest tools/test_lint_overlay.py` still passes (no linter change).
3. `assess` lists FastAPI as an available overlay on the Python track (manual check
   in an empty workdir).
4. `teach` can produce a lesson on `fastapi:routing` (Context7 fetch succeeds).
5. README renders correctly on GitHub (no broken markdown, the section appears
   between "How coverage works" and "Requirements").
6. `revise-claude-md` invoked at the end if anything non-obvious surfaced during
   implementation.

## 5. Workflow

Same as v1.1–v1.3:

1. Isolated worktree off `main` (per `~/.claude/CLAUDE.md` discipline).
2. Plan with explicit Assumptions section.
3. Subagent-driven implementation: write the overlay file, run lint, write the
   README section, manual walkthrough.
4. PR to `main`.
5. Clean up worktree post-merge.

## 6. Risks

- **Skills overlay-awareness untested in the wild.** v1.3 wired
  `assess/teach/exercise/status` to read overlays, but this file will be the first
  real input. If a skill resolves a `fastapi:routing` query against the parent track
  instead of the overlay, that is a skill bug (out of scope to fix here) — isolate
  and file separately, do not patch the overlay to work around it.
- **Resource URL drift.** FastAPI and Pydantic documentation sites occasionally move
  pages. Verify URLs at write-time; if a URL 404s post-merge later, a community PR
  can fix it.
- **`target_version: "0.11x"` interpretation.** This is a wide floor. Context7
  drives actual freshness at teach-time. The risk is null as long as no versioned
  snippet is hardcoded — and we hardcode none (only `mastery`, `exercise_seeds`,
  resource URLs).

## 7. Assumptions (to verify at review)

- **The skills `assess`/`teach`/`exercise`/`status` correctly resolve `fastapi:*`
  concepts to this overlay's modules** — claimed by the v1.3 design, but this file
  is the first real exercise of that wiring. Verify manually before closing the PR.
  *To confirm:* run `assess` in a clean workdir and confirm FastAPI appears as an
  available path on Python.
- **CI already runs `lint_overlay.py` on every `tracks/*/overlays/*.md`** — claimed
  by the v1.3 memory. *To confirm:* read `.github/workflows/*.yml` when opening the
  implementation plan; if not wired, add it as a separate change.
- **Naming `fastapi:validation` is the right choice** — chosen over
  `fastapi:pydantic-models` / `fastapi:models` for the reasons in §3 (role-based,
  leaves room for a future `pydantic` overlay). Falsifiable. If you prefer
  another label, change it now — renaming later is a breaking change for any
  learner's `progress/python/skills.md`.
- **No starter `prompt.md` is needed pre-merge** — the `exercise` skill generates
  per-learner prompts on demand, consistent with the rest of the repo. *To confirm:*
  no existing module ships pre-baked `prompt.md` files under `tracks/`.
- **A single `## Contributing` section in the README is the right level of
  detail** — could grow into a `CONTRIBUTING.md` later; deliberately deferred to
  avoid YAGNI.
- **All four `mastery` bullets per module are observable / gradable** — i.e. the
  `grader` agent can pass/fail them on a learner submission. If any bullet is too
  vague (e.g. "understands why X"), rewrite it as a check.

## 8. Out of scope (explicit)

- Other overlays (SQLAlchemy, Pytest plugins, Pydantic-as-library).
- A `CONTRIBUTING.md` file (the README section is sufficient for now).
- Issue / PR templates.
- Changes to the curriculum lint or schema.
- Changes to the integrity hook.
