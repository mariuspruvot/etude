# Étude — Thread 1: Coherence + Tooling (design)

- **Date:** 2026-05-30
- **Status:** Approved (brainstorming) — ready for plan + implementation.
- **Parent:** `docs/specs/2026-05-30-etude-completeness-roadmap-design.md` §3.
- **Goal:** Make the foundation honest and self-guarding before any content is added — add CI
  that runs the existing linters and tests, fix the mislabeled TypeScript "stub", and label
  SQL honestly as review-only. No new curriculum content.

---

## 1. Motivation

Three concrete coherence/tooling gaps exist today:

1. **The linters never run.** `tools/lint_curriculum.py` and `tools/lint_overlay.py` exist,
   plus ~35 tests across `tools/` and `.claude/hooks/`, but there is **no `.github/`** in the
   repo — nothing executes them on a PR, so curricula/overlays can rot silently.
2. **TypeScript is mislabeled.** `README.md:66` lists "TypeScript and SQL are stubs", yet
   `tracks/typescript/curriculum.md` has 6 full modules + a `## Capstones` section — it is
   already flagship-shaped. The label is wrong and undermines the "is this track real?" signal.
3. **SQL's status is muddy.** It is genuinely non-executable (grading is qualitative,
   `tracks/sql/curriculum.md:14`, `README.md:115`) but is lumped with TS under "stub" rather
   than labeled honestly for what it is.

---

## 2. Deliverable A — CI workflow

Create `.github/workflows/ci.yml`.

### 2.1 Triggers (approved)
- `pull_request` (all PRs)
- `push` to `main`

No path filters: the whole suite (lint + ~35 tests) is small and fast; simplicity beats
micro-optimisation.

### 2.2 Steps
1. `actions/checkout`.
2. Install uv via `astral-sh/setup-uv` (pins a recent uv; Python provided by uv per the
   PEP 723 `requires-python = ">=3.13"` in the lint scripts).
3. **Lint curricula:** `uv run --script tools/lint_curriculum.py tracks/*/curriculum.md`
4. **Lint overlays:** `uv run --script tools/lint_overlay.py tracks/*/overlays/*.md`
5. **Tests:** `uv run --with pyyaml --with pytest pytest tools/ .claude/hooks/`

### 2.3 Constraints
- Linters MUST be invoked with `uv run --script` (PEP 723 inline metadata pulls `pyyaml`);
  `uv run python tools/...` fails with `ModuleNotFoundError: yaml` (`tools/CLAUDE.md`).
- Tests import the lint modules directly, so the test step needs `--with pyyaml --with pytest`
  (`tools/CLAUDE.md`).
- The shell globs (`tracks/*/curriculum.md`, `tracks/*/overlays/*.md`) must match the current
  layout: `tracks/{go,python,typescript,sql}/curriculum.md` and
  `tracks/{go,python,typescript}/overlays/*.md`. If a glob matches nothing the step must not
  silently pass — overlays glob currently matches (go/python/typescript have overlays); guard
  by failing on `nullglob`-empty only if it becomes a real risk (documented, not implemented
  unless a track without overlays breaks the glob).

### 2.4 Out of scope for CI
- `lint_curriculum.py` is **frozen byte-for-byte** (`tools/CLAUDE.md`); CI calls it, never
  edits it.
- No new lint rules. No coverage gate. No matrix — single Python (3.13 via uv).

---

## 3. Deliverable B — Flagship bar (documented criterion)

Add a short **"flagship track" bar** to the README Contributing section (it is a **human
criterion, NOT a lint rule** — the curriculum linter is frozen):

A track is **flagship** (vs review-only stub) when it has:
- ≥ 6 modules spanning tooling → syntax → type system → errors → concurrency/async → testing;
- a `## Capstones` section (mini_app + interview);
- `transfer_note` blocks on modules where cross-language transfer applies;
- and it passes `lint_curriculum.py`.

This makes "stub vs flagship" a checkable, written standard rather than a vibe.

---

## 4. Deliverable C — TypeScript relabel (stub → flagship)

`tracks/typescript/curriculum.md` already satisfies the §3 bar: 6 modules
(m01 tooling → m02 syntax → m03 type system → m04 generics → m05 errors+async →
m06 modules+testing) + a `## Capstones` section + `transfer_note` blocks on m02/m03/m05.

Changes:
- `README.md:66` — move TypeScript out of "stubs": *"Go, Python and TypeScript are full
  flagship tracks; SQL is a review-only track."*
- No new modules. The Thread-1 implementation **verifies depth parity** against Go/Python
  (7 modules each) and notes any genuinely missing concept as a follow-up — it does **not**
  pad modules to hit 7.

---

## 5. Deliverable D — SQL honest label (review-only)

SQL stays 2 modules; it is relabeled honestly rather than promoted.

Changes:
- `README.md:66` — SQL described as a **"review-only track"** (not a "stub").
- `README.md:115` already states non-executable tracks are reviewed qualitatively — keep,
  align wording ("review-only").
- `tracks/sql/curriculum.md:13-14` already says "Stub track … reviewed qualitatively" — align
  to "review-only track" wording for consistency.
- A Postgres execution harness (dockerised `psql`) that would promote SQL toward flagship is
  **deferred** (roadmap §3.3) — referenced, not built.

---

## 6. Testing & verification

- **CI itself is the test** for Deliverable A: open the Thread-1 PR and confirm the workflow
  goes green (lint + ~35 tests pass).
- **Local pre-PR check** (same commands CI runs):
  - `uv run --script tools/lint_curriculum.py tracks/*/curriculum.md`
  - `uv run --script tools/lint_overlay.py tracks/*/overlays/*.md`
  - `uv run --with pyyaml --with pytest pytest tools/ .claude/hooks/`
- **No new test code.** The relabels (B/C/D) are prose edits to `README.md` and one wording
  alignment in `tracks/sql/curriculum.md`; they are covered by existing linting (the curricula
  still must lint clean) and by human review of the README. Adding a test that greps the
  README for the word "flagship" would be brittle coupling — explicitly **not** done.

---

## 7. Definition of done

- `.github/workflows/ci.yml` exists and is green on its own PR.
- README Contributing carries the flagship bar; README track summary lists Go/Python/TS as
  flagship and SQL as review-only.
- `tracks/sql/curriculum.md` wording aligned to "review-only".
- All linters + tests pass locally and in CI.
- `lint_curriculum.py` unchanged (diff shows zero bytes touched).
- `revise-claude-md` step run to capture lessons (repo workflow requirement).
- Lands via isolated worktree + PR to `main`.

---

## 8. Assumptions

- **`astral-sh/setup-uv` provides Python 3.13.** — uv can install the interpreter declared in
  the scripts' `requires-python`; if the action needs an explicit `actions/setup-python`
  step, add it at implementation time. Cheap to adjust.
- **The overlay glob always matches at least one file.** — True today (go/python/typescript
  have overlays); if a future track has none, the glob could error — flagged in §2.3, handled
  only if it actually breaks.
- **TypeScript needs no new modules to be flagship.** — Based on reading
  `tracks/typescript/curriculum.md` against the §3 bar; implementation verifies parity and
  records (does not pad) any gap.
- **No root `pyproject.toml` is wanted.** — The repo deliberately uses PEP 723 inline scripts
  + `uv run --with` (`tools/CLAUDE.md`); CI follows that convention rather than introducing a
  project file.

---

## 9. Out of scope

- Native plugin packaging (deferred, roadmap §3.4).
- SQL execution harness (deferred, roadmap §3.3).
- Any change to `lint_curriculum.py` (frozen).
- New curriculum content or new tracks.
