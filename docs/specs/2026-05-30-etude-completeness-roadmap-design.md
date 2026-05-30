# Étude — Completeness Roadmap (vision & decomposition)

- **Date:** 2026-05-30
- **Status:** Approved (brainstorming) — master design doc; spawns per-thread specs.
- **Scope:** Define what "a complete repo" and "a complete engineer" mean for Étude, fix the
  curated-vs-on-demand boundary, and sequence the work into independently shippable threads.
  This document does **not** implement anything; each thread below gets its own spec → plan →
  implementation cycle.

---

## 1. Problem & framing

The request: make Étude "really more complete", clean, coherent, with complete and
well-organised tracks that make learners "truly complete".

Taken literally, "more complete" pulls against Étude's own stated philosophy — *curated
curricula cover each language's stable **core**; everything else is generated on demand*
(`README.md:75`) — and against the project's own YAGNI note (don't curate what on-demand
already covers). Piling on curated content is the **least** leveraged way to improve Étude:
content is the cheap part (Context7 generates it on demand at teach-time, `README.md:27`),
while the value and the moat live in the *engine* — the `assess → teach → exercise → grade →
track → revise` loop, the integrity hook (`.claude/hooks/protect_solutions.py`), and the
owned `progress/` state.

The resolution (the key design decision of this roadmap): **we do not curate everything. We
make the agent know *when* to propose the rest.** The curated spine stays thin and honest;
a **nudge engine** opens doors into the infinite on-demand space at pedagogically opportune
moments. This turns the "we don't contain everything" limitation into a feature.

### 1.1 Definitions

- **"Complete repo"** ≠ contains every topic. It means: *(1)* the engine is guarded (CI runs
  the linters and hook tests that already exist), *(2)* the curated spine is honest (no
  mislabeled stubs, clear "what is a flagship track" bar), *(3)* the agent bridges to
  on-demand content intelligently (nudge engine).
- **"Complete engineer"** = language mastery **plus** transversal engineering competencies
  (algorithms, software design, databases, networking, security, …). A learner who knows a
  language's syntax and concurrency primitives but cannot reason about complexity, design a
  system, or read a query plan is not complete.

### 1.2 The curated-vs-on-demand boundary (decision rule)

Curate **only**:

- **(a)** stable language cores (`tracks/<lang>/curriculum.md`);
- **(b)** a small number of high-traffic overlays, kept as **quality exemplars** for
  on-demand generation (e.g. the existing backend overlays);
- **(c)** transversal engineering tracks that are **universal and gradable**.

Everything else — niche frameworks, one-off libraries, "cool" deep-dive topics — stays
**on-demand**, and is **surfaced by the nudge engine** rather than pre-written. This rule is
the contract every future "should we add X?" decision is measured against.

---

## 2. Decomposition (threads)

The work is too large for a single spec. It decomposes into one framing doc (this one) plus
three independently shippable threads:

| # | Thread | Size | Rationale for ordering |
|---|--------|------|------------------------|
| 0 | **Roadmap / vision** (this doc) | small | Fixes definitions + the curated/on-demand boundary; hosts the other three. |
| 1 | **Coherence + tooling** | small | CI guards everything else; honest labels; removes the "stub" incoherence. Quick win, unblocks confidence in later changes. |
| 2 | **Nudge engine** | medium | The connective tissue between the curated spine and on-demand. Pure design, zero new content. High differentiation. |
| 3 | **Transversal "complete-engineer" tracks** | large, ongoing | The long arc. Needs a taxonomy first, then an executable pilot track. |

**Sequence:** `#0 → #1 → #2 → #3`. Each of #1/#2/#3 gets its own spec in `docs/specs/`,
its own plan, and its own implementation cycle (isolated worktree, PR to `main`, with the
`revise-claude-md` step included in the definition of done per the repo workflow).

---

## 3. Thread 1 — Coherence + tooling

**Goal:** make the foundation honest and self-guarding before adding anything on top.

### 3.1 CI

Add a GitHub Action (no `.github/workflows/` exists yet) that runs on PRs touching
`tracks/`, `tools/`, or `.claude/hooks/`:

- `uv run --script tools/lint_curriculum.py tracks/*/curriculum.md`
- `uv run --script tools/lint_overlay.py tracks/*/overlays/*.md`
- the hook + tool test suites (`uv run --with pyyaml --with pytest pytest tools/ .claude/hooks/`)

Invocation must use `uv run --script` (PEP 723 metadata), per `tools/CLAUDE.md`.
`lint_curriculum.py` is declared **closed / byte-for-byte frozen** there — CI must call it,
not modify it.

### 3.2 Flagship bar + TypeScript promotion

Define a **"flagship track" bar** (proposed, to be ratified in the Thread-1 spec):
- ≥ 6 modules covering tooling → syntax → type system → errors → concurrency/async → testing;
- a `## Capstones` section (mini_app + interview);
- `transfer_note` blocks on modules where cross-language transfer applies;
- passes `lint_curriculum.py`.

TypeScript already meets this (6 modules + capstones, `tracks/typescript/curriculum.md`) yet
`README.md:66` calls it a "stub". **Fix the label** and add TS to the flagship list. No new
modules strictly required; the Thread-1 spec will sanity-check depth parity against Go/Python.

### 3.3 SQL — honest labeling now, harness later (approved)

SQL is non-executable today; grading is qualitative (`tracks/sql/curriculum.md:14`). Decision:
- **Now:** label it honestly as a **review-only track** (mastery checked by reading the query
  + explaining the plan), keep its 2 modules.
- **Later (deferred):** a lightweight Postgres execution harness (e.g. dockerised `psql`)
  would promote it toward flagship. Tracked as future work, not blocking.

### 3.4 Plugin packaging (future)

Native Claude Code plugin packaging for distribution remains **deferred** (consistent with
prior project state). Noted here so the roadmap is complete; not part of Thread 1's first cut.

---

## 4. Thread 2 — Nudge engine

**Goal:** the tutor proactively proposes the *next worthwhile thing* — a branch (overlay), a
deep-dive, a transversal track, a mini-app, or a mock interview — at the right moments, and
**never spams**.

### 4.1 Triggers (all four approved)

1. **Palier points** — when a concept moves to `proficient`/`mastered` in `skills.md`, or at
   the end of a capstone. Never mid-exercise.
2. **On-demand** — at `/status` and in the session-start greeting. Non-intrusive: appears
   only when the learner comes to "see where they are".
3. **Interest signals** — when the learner asks an off-topic / curiosity question (e.g. "why
   is this so slow?" → offer a perf deep-dive). Opportunistic, learner-driven.
4. **Frequency guardrail** (always on, see 4.2).

### 4.2 Frequency guardrail (the "not all the time")

- **Max 1 suggestion per session.**
- **Cooldown after a decline:** a declined branch is not re-proposed for N sessions
  (N ratified in the Thread-2 spec; default proposal: 3).
- **Profile setting:** `suggestions: off | rare | normal` in `progress/profile.md`
  (default `normal`; `rare` ≈ palier-points only; `off` disables proactive nudges entirely
  but `/status` may still show a single quiet "want to branch?" line).

### 4.3 What it proposes (next-step taxonomy)

A suggestion resolves to exactly one of:
- a **branch / overlay** (e.g. a front-end framework on the TS track);
- a **deep-dive** (internals, trade-offs, cross-language contrast);
- a **transversal track** (a Thread-3 "complete-engineer" track relevant to current state);
- a **mini-app** (guided multi-file project);
- a **mock interview**.

Relevance is computed from `skills.md` state (what's mastered, what's weak), recent activity
(`log.md`), and any curiosity signal in the current turn.

### 4.4 Memory & wiring

- **Journal:** `progress/<track>/suggestions.md` records each suggestion (kind, target, date,
  outcome: proposed/accepted/declined). This feeds the cooldown and prevents repetition.
- **Wiring:** **not a hook** (hooks enforce; this advises). Implemented as a shared reference
  doc (proposed path `.claude/skills/_shared/nudge.md` — exact location ratified in the
  Thread-2 spec) that `teach`, `grade`, `status`, and `assess` consult, plus the
  `profile.md` setting. Pure design; introduces **zero** new curriculum content.

---

## 5. Thread 3 — Transversal "complete-engineer" tracks

**Goal:** add the non-language axis that actually makes learners complete. Designed in its own
spec; only framed here.

### 5.1 Candidate taxonomy (proposed)

`algorithms-data-structures`, `system-design`, `databases`, `networking-http`, `git`,
`security`, `observability-debugging`, `software-design`.
*(Proposed set — the exact list and ordering are arbitrated in the Thread-3 spec.
[claude-guessed: this taxonomy is a starting point, not a committed scope].)*

### 5.2 Pilot: Algorithms & Data Structures (approved)

Chosen as the pilot because it is **universal**, **executable/gradable in any language** (so
it works with the existing grader agent), and feeds the `interview` mode directly. Databases
is the natural second pilot but depends on the SQL execution harness (§3.3, deferred).

### 5.3 Schema question to resolve in the Thread-3 spec

A transversal track may be **language-agnostic** or **multi-language gradable**, unlike the
current language-bound `tracks/<lang>/curriculum.md` schema (which assumes one toolchain per
track). This likely requires a **schema extension** (e.g. a `kind: transversal` marker, or a
`languages: [...]` field letting the learner pick the implementation language). This is a
Thread-3 design decision — explicitly **out of scope** for this roadmap.

---

## 6. Definition of done (per thread)

Each thread (#1–#3) is done when:
- its own spec is written to `docs/specs/` and approved;
- implementation lands via an isolated worktree and a PR to `main`;
- all linters and tests pass (locally and in CI once Thread 1 lands);
- the `revise-claude-md` step has run to capture lessons (repo workflow requirement).

---

## 7. Assumptions

- **The engine is the moat, not the content.** — Inferred from the architecture (integrity
  hook + owned `progress/` + on-demand generation via Context7); load-bearing for the whole
  "don't curate, nudge instead" thesis. If the user actually wants a content library, the
  ordering flips.
- **TypeScript already meets the flagship bar.** — Based on reading
  `tracks/typescript/curriculum.md` (6 modules + capstones); the Thread-1 spec will verify
  depth parity rather than assume it.
- **CI does not exist yet.** — No `.github/workflows/` was found in the repo tree; prior
  project state corroborates. To confirm at Thread-1 implementation time.
- **A shared reference doc (not a hook) is the right vehicle for the nudge engine.** — Chosen
  because hooks enforce/block and the nudge only advises; the exact path and the
  consult-from-skills mechanism are ratified in the Thread-2 spec.
- **Cooldown N = 3 sessions and `suggestions` defaults to `normal`.** — Defaults picked for
  lack of a specified value; cheap to change in the Thread-2 spec.
- **Algorithms & Data Structures is gradable language-agnostically with the current grader.**
  — Assumed from the grader agent's description (executes tests when the track is executable);
  the Thread-3 spec must confirm the grader can target a learner-chosen language.
- **The transversal-track schema needs extending.** — Inferred from the single-toolchain
  assumption baked into the current curriculum schema; to be designed, not yet proven.

---

## 8. Out of scope (for this roadmap doc)

- Any implementation (each thread implements under its own spec).
- The exact transversal-track taxonomy and schema extension (Thread 3).
- The SQL execution harness (deferred).
- Native plugin packaging (deferred).
- Adding new *languages* (lower priority than the engine and the transversal axis).
