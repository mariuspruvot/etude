# Étude — Tracks roadmap (backlog)

A living backlog of tracks to add next. This is **not** a commitment — it is the working map,
ordered by leverage. Each item gets its own spec → plan → PR when picked up (see
[`README.md` → Contributing](../README.md) and `docs/specs/`).

## The decision rule (curate vs on-demand)

Before adding anything, check it against the boundary fixed in the completeness roadmap
(`docs/specs/2026-05-30-etude-completeness-roadmap-design.md` §1.2):

> Curate **only** (a) stable language cores, (b) a few high-traffic overlays as quality
> exemplars, (c) transversal engineering tracks that are **universal and gradable**.
> Everything else stays **on-demand** and is surfaced by the nudge engine (`.claude/nudge.md`).

So the bar for a new curated track is: *would on-demand generation handle this just as well?*
If yes, don't curate it — let the nudge engine offer it. If it is a universal, gradable
foundation, it earns a curated track.

---

## 1. Transversal "complete-engineer" tracks (highest leverage)

The non-language axis that makes a learner well-rounded. Schema: `kind: transversal`, linted by
`tools/lint_transversal.py`. Taxonomy from
`docs/specs/2026-05-30-etude-thread3-transversal-tracks-design.md` §2.

| track (`name`) | scope (one line) | gradable? | priority | status |
|----------------|------------------|-----------|----------|--------|
| `algorithms` | complexity, data structures, graphs, sorting, DP | yes (exec) | — | **shipped** (pilot, PR #13) |
| `databases` | relational modelling, indexing, query plans, transactions | yes (needs Postgres harness) | **next** | not started |
| `system-design` | scaling, caching, queues, data-flow, trade-offs | partial (design review) | high | not started |
| `networking-http` | TCP/TLS, HTTP semantics, REST, status/headers | partial (mixed) | high | not started |
| `security` | OWASP top-10, auth/authz, common vulns, secure defaults | partial (exec + review) | high | not started |
| `git` | branching, rebase/merge, history surgery, workflows | yes (exec on a sandbox repo) | medium | not started |
| `observability-debugging` | logging, metrics, traces, systematic debugging | partial (exercise-driven) | medium | not started |
| `software-design` | patterns, SOLID, refactoring, boundaries | yes (refactor exercises) | medium | not started |

**Recommended next:** `databases` — it is the natural second foundation and reactivates the
deferred SQL/Postgres execution harness (see §4), upgrading SQL from review-only toward a
gradable transversal track.

Notes:
- "partial" gradability means some modules execute (e.g. write a query, fix a vuln) and some are
  design/review (e.g. "sketch a system"). The grader already supports qualitative review.
- Each transversal track declares `languages: [...]`; the learner picks one and the grader runs
  in it (the `databases` track's "language" axis is SQL dialects / an ORM, to design in its spec).

---

## 2. Language tracks (lower priority than the transversal axis)

The engine + the transversal axis matter more than a 5th language. Add only on real demand.

| track | rationale | priority | status |
|-------|-----------|----------|--------|
| `sql` → flagship | give it a Postgres execution harness (§4) so it grades by running, not just review | medium | review-only today |
| `rust` | strong demand; rich contrast (ownership/borrow checker) for the existing audience | low | not started |
| `java` | enterprise reach; contrast with Go/Python typing & concurrency | low | not started |
| `c` / `c++` | systems foundations (memory, pointers) — also feeds `algorithms` depth | low | not started |

*[claude-guessed: the specific language picks beyond SQL are indicative — driven by demand, not committed.]*

---

## 3. Overlays (curate only when high-traffic; otherwise on-demand)

Overlays are framework/library paths on a parent track (`tracks/<parent>/overlays/<name>.md`,
see `tracks/OVERLAYS.md`). The promotion path is: on-demand → personal extension → curated
overlay. Curate one only when it is high-traffic enough to be worth a quality exemplar.

| overlay | parent | rationale | priority | status |
|---------|--------|-----------|----------|--------|
| `react` | typescript | front-end demand; pairs with the backend→front goal | medium | on-demand |
| `vue` | typescript | same, second front framework | low | on-demand |
| `next` | typescript | full-stack React meta-framework | low | on-demand |
| `sqlalchemy` | python | dominant Python ORM; complements the FastAPI overlay | low | on-demand |
| `django` | python | batteries-included web framework | low | on-demand |

Shipped overlays today (exemplars): `fastapi` (python), `nethttp` (go), `express`/`nestjs`/
`prisma` (typescript). Don't curate a new overlay unless on-demand demand is clearly repeated —
the nudge engine is meant to surface these, not the repo to pre-contain them.

---

## 4. Cross-cutting enablers (unlock several tracks)

- **SQL/Postgres execution harness** (deferred). A dockerised `psql` runner would let `sql`
  become flagship and `databases` grade by execution. Blocks/upgrades both. See completeness
  roadmap §3.3.
- **Nudge → track surfacing.** Once a transversal track exists, ensure the nudge engine offers
  it to relevant learners (it already lists "transversal track" as a suggestion kind in
  `.claude/nudge.md`). No code; just confirm the relevance heuristic points at new tracks.

---

## How to add a track

1. Open an issue to discuss scope (Contributing convention).
2. Write a design spec in `docs/specs/YYYY-MM-DD-<name>-design.md`.
3. Author the curriculum:
   - language track → `tracks/<lang>/curriculum.md` (lint `lint_curriculum.py`);
   - transversal track → `tracks/<name>/curriculum.md` with `kind: transversal`
     (lint `lint_transversal.py`);
   - overlay → `tracks/<parent>/overlays/<name>.md` (lint `lint_overlay.py`, see `OVERLAYS.md`).
4. Make the skills aware if a new track *kind* is introduced (as Threads 1.3/3 did).
5. PR to `main`; CI lints + tests on every PR.
