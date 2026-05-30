# Étude — Thread 3: Transversal "complete-engineer" Tracks (design)

- **Date:** 2026-05-30
- **Status:** Approved (brainstorming) — ready for plan + implementation.
- **Parent:** `docs/specs/2026-05-30-etude-completeness-roadmap-design.md` §5.
- **Goal:** Add the non-language axis that actually makes a learner *complete*: engineering
  subjects that a language track does not teach (algorithms, system design, databases, …).
  This spec defines the **taxonomy** (the target map) and fully designs the **pilot track**
  — Algorithms & Data Structures — plus the schema/linter/grading machinery all transversal
  tracks will share. Only the pilot is built now; the rest are balisé future work.

---

## 1. Why this thread

A language track teaches a *language*. It does not teach you to be an *engineer*. A learner
who knows Go's goroutines but cannot reason about complexity, model data structures, or pick
the right algorithm is not complete (roadmap §1.1). Transversal tracks are the missing axis,
and they are the kind of curated content the project SHOULD own (roadmap §1.2c: "universal and
gradable") — unlike niche frameworks, which stay on-demand.

The nudge engine (Thread 2) already lists "transversal track" as a suggestion kind
(`.claude/nudge.md`); once a transversal track exists, the tutor can proactively point a
language learner to it.

---

## 2. Taxonomy (the "complete engineer" map)

Intended target set (the full axis). **Only the pilot is designed/built in this thread.**

| track (`name`) | status in this thread |
|----------------|------------------------|
| `algorithms` — Algorithms & Data Structures | **PILOT — fully designed + built** |
| `databases` — relational modelling, indexing, query plans | future (natural 2nd; overlaps the deferred SQL harness) |
| `system-design` | future |
| `networking-http` | future |
| `git` — version control | future |
| `security` — OWASP, auth, common vulns | future |
| `observability-debugging` | future |
| `software-design` — patterns, SOLID, refactoring | future |

The set is **not frozen** — it is the working map; each future track gets its own spec.
*[claude-guessed: ordering/membership beyond the pilot is indicative.]*

---

## 3. Schema — `kind: transversal` (new, mirrors the overlay precedent)

A transversal track is **language-agnostic but gradable**. The current `curriculum.md` schema
assumes one toolchain (`language`, `target_version`) and its linter `lint_curriculum.py` is
**frozen byte-for-byte** (`tools/CLAUDE.md`). So — exactly as overlays did
(`tools/lint_overlay.py:7-11`: "A NEW schema, distinct from curriculum.md — the closed-core
lint_curriculum.py is left untouched") — transversal tracks get a **new schema + a new linter**.

### 3.1 Location & shape

`tracks/<name>/curriculum.md` (top-level track, like `go`/`python`), with:

```markdown
---
kind: transversal             # required, must be exactly "transversal"
name: algorithms              # required; also the concept namespace prefix
display_name: Algorithms & Data Structures
languages: [python, go, typescript]   # required, non-empty; impl languages the learner may pick
freshness_source: context7
maintainers: [community]
concepts:
  transversal: [algorithms:complexity, algorithms:arrays-hashing, ...]  # required, non-empty; every id "<name>:"
---

# Algorithms & Data Structures — Transversal track

### t01 — Complexity & Big-O
- id: t01
- concepts: [algorithms:complexity]
- prerequisites: []
- mastery: [...]
- exercise_seeds: [...]
### t02 — Arrays, strings & hashing
- id: t02
- concepts: [algorithms:arrays-hashing]
- prerequisites: [t01]
```

### 3.2 Rules the new linter (`tools/lint_transversal.py`) enforces

Modeled on `lint_overlay.py` (duplicate the frozen-core's frontmatter parser; do **not** import
from `lint_curriculum.py`):

- `kind` present and exactly `transversal`; `name`, `display_name` present; `languages` a
  non-empty list of strings.
- `concepts.transversal` is a non-empty list; **every** concept id is namespaced `<name>:`.
- **Must NOT** declare `transverse` or `language_specific` (those are language-track keys —
  analogous to the overlay rule "overlays must not declare transverse concepts",
  `lint_overlay.py:89-90`). Transversal concepts are namespaced and **track-local** for
  transfer (see §4).
- Modules are `tNN`; each module's `concepts` entries are declared transversal concepts; each
  `prerequisites` entry references an **earlier** `tNN` module in document order (⇒ the module
  DAG is acyclic without a graph check, same trick as `lint_overlay.py:110-112`). No `parent:`
  prerequisites (transversal tracks have no parent — they are top-level).
- A `## Capstones` section is expected (consistency with language tracks; the linter may warn
  but the hard requirement is the `tNN` integrity above).

### 3.3 Why namespaced + track-local (not `transverse`)

Language-track cross-skip logic in `assess` keys off a track's declared **transverse**
concepts. `algorithms:*` concepts are not in any language track's vocabulary, so they could
never satisfy a skip anyway; namespacing keeps `skills.md` clean and signals provenance. This
mirrors how overlay and `personal:` concepts are treated as shared-but-track-local
(`.claude/skills/grade/SKILL.md:32`, `assess/SKILL.md:32`).

---

## 4. Grading model — learner picks a supported language (approved)

A transversal exercise (e.g. "implement BFS") is solved in a language the learner chooses from
the track's `languages: [...]`. The existing `grader` agent already "executes tests when the
track is executable" — for a transversal track it is executable **in the chosen language**.

Flow:
- When `exercise` generates a transversal exercise, it asks the learner which supported
  language to use (default: the learner's `active_track` language if it is in `languages`,
  else their strongest `known_languages` entry that is in `languages`, else ask).
- The chosen language sets the `prompt.md` frontmatter `solution_file` (e.g. `solution.py`),
  exactly as `exercise`/`interview` already do (`.claude/skills/interview/SKILL.md:14-21`).
- `grade` dispatches the `grader` against that solution file in that language's toolchain.
- `skills.md` records the namespaced concept (`algorithms:graphs`) with the exercise as
  evidence; the evidence note includes the language used (e.g. `algorithms/exercises/003 (go)`).

This keeps execution-based proof (the engine's moat) while honoring the learner's
multi-language profile.

---

## 5. Pilot — Algorithms & Data Structures (`tracks/algorithms/curriculum.md`)

Proposed 7-module spine (depth comparable to the language flagships). Concepts namespaced
`algorithms:`. *(Module set is a proposal — reviewable.)*

| id | module | concept |
|----|--------|---------|
| t01 | Complexity & Big-O (time/space, amortized, how to reason) | `algorithms:complexity` |
| t02 | Arrays, strings & hashing (two-pointer, sliding window, hash maps) | `algorithms:arrays-hashing` |
| t03 | Linked structures: lists, stacks, queues | `algorithms:linked-structures` |
| t04 | Trees & heaps (binary trees, BST, heaps, traversals) | `algorithms:trees-heaps` |
| t05 | Graphs (BFS/DFS, shortest paths, topological sort) | `algorithms:graphs` |
| t06 | Sorting & searching (comparison sorts, binary search, quickselect) | `algorithms:sorting-searching` |
| t07 | Recursion, backtracking & dynamic programming | `algorithms:recursion-dp` |

- **Prerequisites:** linear chain t01→t07 except t06 depends on t01 (sorting needs complexity)
  and t07 depends on t03+t04 (recursion over linked/tree structures). All earlier-in-document.
- **`mastery` / `exercise_seeds`:** every module gets concrete, executable seeds (e.g. t05:
  "implement BFS shortest path on an adjacency list; tests cover a disconnected graph").
- **Resources:** official/canonical references only (per the contributing rule); pull current
  language-specific stdlib usage via Context7 at teach-time.
- **Capstones:**
  - `mini_app`: "implement an LRU cache (hashmap + doubly-linked list) with tests" — concepts
    `[algorithms:linked-structures, algorithms:complexity]`.
  - `interview`: "live-coding: a graph or DP problem; verbal: justify complexity trade-offs" —
    concepts `[algorithms:graphs, algorithms:recursion-dp, algorithms:complexity]`.
- **Completeness criterion for a transversal track** (distinct from the language flagship bar,
  which is syntax/tooling-shaped): ≥ 6 modules covering the subject's core spine + a
  `## Capstones` section + lints clean under `lint_transversal.py`. Documented in README
  Contributing alongside the flagship bar.

---

## 6. Skill & tooling wiring

Transversal-awareness, mirroring how v1.3 made the skills overlay-aware:

- **`assess`** — recognize a `kind: transversal` track: there is no syntax module to force and
  no transverse-skip to compute; build the path from `tNN` prerequisites. Set `active_track` to
  the transversal track. Ask which impl language (from `languages`) the learner will use; record
  it in the profile notes.
- **`teach`** — read `tracks/<name>/curriculum.md` for `kind: transversal`; teach the concept
  language-agnostically, then show one idiomatic example in the learner's chosen language (via
  Context7 for current stdlib usage).
- **`exercise`** — set `solution_file` per the chosen language (§4); seeds come from the `tNN`
  module.
- **`grade`** — execute in the chosen language; record the namespaced concept + language in
  evidence (§4).
- **`status`** — render transversal tracks like any track; their concepts are namespaced and
  track-local.
- **CI (`.github/workflows/ci.yml`)** — add a **lint transversal** step:
  `uv run --script tools/lint_transversal.py tracks/*/curriculum.md` is wrong (it would also
  hit language curricula). Instead the linter must **detect `kind`**: `lint_transversal.py`
  lints only files whose frontmatter `kind == transversal` and ignores others (so it can be
  pointed at `tracks/*/curriculum.md` safely), OR CI globs only known transversal dirs. Decision:
  **the linter self-selects by `kind`** (robust, no glob maintenance) — it prints `skip` for
  non-transversal curricula. Mirror this tolerance in `lint_curriculum.py`? No — that file is
  frozen; instead CI keeps pointing `lint_curriculum.py` at all curricula (a transversal file has
  no `language`/`target_version`, so it would FAIL the frozen linter). **Therefore CI must lint
  language curricula and transversal curricula with separate, kind-targeted globs** — see §6.1.

### 6.1 CI globbing (resolved)

To avoid the frozen `lint_curriculum.py` choking on `kind: transversal` files (no `language`/
`target_version`), CI must not pass transversal curricula to it. Options:
- **(chosen)** `lint_transversal.py` self-selects by `kind` and CI points it at
  `tracks/*/curriculum.md`; `lint_curriculum.py` is pointed at the **language tracks only**, via
  an explicit list or by excluding transversal dirs. Simplest robust form: keep a tiny
  `tracks/LANGUAGE_TRACKS` convention OR have a one-line shell that greps frontmatter `kind`.
- The implementation plan picks the least-magic mechanism; the **constraint** is: the frozen
  linter never receives a transversal file. This is the one genuinely fiddly bit of the thread.

---

## 7. Testing & verification

- **`tools/test_lint_transversal.py`** — unit tests for the new linter (valid file passes; each
  rule violation is caught), mirroring `tools/test_lint_overlay.py` (9 cases) in style/coverage.
- **Lint the pilot** — `tracks/algorithms/curriculum.md` lints clean.
- **Existing suites stay green**; `lint_curriculum.py` unchanged (frozen) and still passes on the
  language tracks (it must NOT be fed the transversal file — §6.1).
- **Manual walkthrough (HUMAN step)** — `/learn algorithms`, pick a language, teach t01, generate
  an exercise, write a solution, grade it, confirm `skills.md` records `algorithms:complexity`
  with the language in evidence. Confirms the multi-language grading path end-to-end.

---

## 8. Definition of done

- `tools/lint_transversal.py` + `tools/test_lint_transversal.py` written and green.
- `tracks/algorithms/curriculum.md` (7 modules + capstones) lints clean.
- Skills (`assess`/`teach`/`exercise`/`grade`/`status`) are transversal-aware.
- CI lints transversal curricula without feeding the frozen linter a transversal file (§6.1).
- README Contributing documents the transversal completeness criterion + `kind: transversal`.
- `lint_curriculum.py` unchanged (frozen).
- Manual walkthrough done.
- `revise-claude-md` step run.
- Lands via isolated worktree + PR to `main`.

---

## 9. Assumptions

- **A new schema+linter is the coherent choice (vs bending curriculum.md).** — Chosen to mirror
  the overlay precedent and keep `lint_curriculum.py` frozen; the alternative (placeholder
  `language`/`target_version`) is semantically false and was rejected.
- **The grader can execute a learner-chosen language per exercise.** — Based on the grader
  "executes tests when the track is executable"; the implementation confirms it can be told which
  language/toolchain to use via the `prompt.md` `solution_file` extension.
- **Transversal concepts should be namespaced + track-local, not `transverse`.** — They are not
  in any language track's vocabulary, so they cannot drive cross-skip; namespacing keeps
  `skills.md` clean (mirrors overlay/`personal:`).
- **CI can keep the frozen linter away from transversal files cleanly.** — §6.1 names this the
  one fiddly bit; the plan picks the least-magic mechanism. If no clean mechanism exists, the
  fallback is putting transversal tracks under a distinct dir (e.g. `tracks/_transversal/<name>/`)
  so globs separate them — noted, not chosen, to avoid a non-standard layout.
- **7 modules is the right pilot depth.** — Proposal; reviewable. Fewer is fine if a module is
  genuinely redundant.
- **`name: algorithms` (namespace `algorithms:`).** — Default; `dsa` is the alternative if a
  shorter prefix is preferred.

---

## 10. Out of scope

- Any change to `lint_curriculum.py` (frozen) or `lint_overlay.py`.
- The non-pilot transversal tracks (each gets its own spec).
- The SQL/Postgres execution harness (deferred; `databases` track will revisit it).
- Auto-generating exercises beyond the pilot's `exercise_seeds`.
