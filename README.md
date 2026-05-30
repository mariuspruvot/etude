# Étude

Étude turns Claude Code into a programming tutor that runs inside a repo on your machine.
Pick a track (a language or a technical subject) and it assesses your level, teaches one
concept at a time, sets exercises calibrated to you, runs and grades the code you write, and
keeps track of what you've learned across sessions.

The point is that *you* write the code. A hook stops the tutor from writing your solution
files, and hints come in steps rather than as a finished answer — it's a teacher with office
hours, not a chatbot that completes your homework.

## What it does

- Assesses your level by conversation and skips what you already know (know Python? the Go
  track teaches by contrast instead of from zero).
- Teaches in two registers: a short focused lesson when you just need the concept (the idea,
  one idiomatic example, the common pitfalls), or an open, go-as-deep-as-you-want discussion
  (`/deep-dive`) — internals, trade-offs, cross-language contrasts, edge cases — when you want
  to really dig in.
- Generates exercises calibrated to your level, varying the format (implement, debug,
  refactor, extend, write tests).
- On executable tracks, runs your solution and grades it against the module's criteria, then
  records the result as evidence in `progress/`.
- Resumes where you left off next session, and re-tests concepts on a spaced schedule so they
  don't fade.
- Isn't limited to the bundled curricula: ask for a framework or a niche topic and it builds
  a path from current docs (via Context7).
- Teaches in the language you pick; code, identifiers, and CLI stay in English.
- Runs mock interviews when you want them — verbal questions plus a graded live-coding round.

## What's tracked
Everything lives in `progress/` (local, gitignored):

- **Competencies** — per concept, a level (`unknown → learning → proficient → mastered`) with
  the date and the exercise that proved it. Graded exercises move these levels; `revise`
  re-tests them on a spaced schedule.
- **Explorations** — deep-dive sessions are logged (topic, date, what was covered). They can
  nudge a concept to `learning` and resurface later for review, but they record that you
  *explored* something, not that you can *do* it — a graded exercise is what proves the skill.
- **Personal modules** — a niche you keep returning to can be promoted into your own module,
  and later shared back as a curated overlay.

`/status` renders all of this; `/revise` uses it to fight forgetting.

## Quickstart
1. `git clone <repo> && cd etude`
2. Open Claude Code: `claude`
3. **Accept the "trust this folder?" prompt** once — it enables the tutor's skills and the
   integrity guard. (See `docs/specs/2026-05-27-etude-feasibility-spike.md` for why.)
4. Say what you want to learn (e.g. `/learn go`) and follow along.

Your progress lives in `progress/` (gitignored, local-only, the source of truth). Back it
up by copying that folder.

## Modes
`/learn` · `/next` · `/hint` · `/grade` · `/status` · `/mini-app` · `/interview` · `/revise` · `/validate` · `/deep-dive` · `/language`

You can also just say what you want in plain language ("give me an exercise", "I'm stuck",
"where am I?", "interview me") — the tutor routes to the right mode.

## Integrity
Claude is a tutor, not a solver: a hook blocks it from writing your solution files, and
hints are graduated. You write the code; Claude guides and grades.

## Tracks
Go, Python and TypeScript are full flagship tracks; SQL is a review-only track
(JavaScript is taught as a subset of TypeScript). A track is a
programming language or an adjacent technical subject. Adding one = writing a
`tracks/<track>/curriculum.md` skeleton — contributions welcome. See the **flagship
bar** under Contributing for what separates a full track from a review-only one.

## Teaching language
Étude teaches in your preferred language — say it (or run `/language fr`) and explanations,
exercises, and feedback switch. Code, identifiers, and CLI commands stay in their original
(usually English) form.

## How coverage works (you're not limited to the modules)
Curated curricula cover each language's stable **core**. Everything else — frameworks
(FastAPI, Django, React, Vue), libraries, niche topics — is **generated on demand** using
current docs (Context7) when you ask, and remembered in your `progress/` as personal
modules. Ask for anything: `/deep-dive "Go escape analysis"`, "teach me FastAPI", etc.

The most-used generated paths can graduate to **curated overlays** shipped in the repo
(`tracks/<lang>/overlays/<name>.md`, e.g. FastAPI on Python) — shared and linted. See
`tracks/OVERLAYS.md`. This is the "personal → community" promotion path.

## Contributing
Étude grows by **curriculum** (a full language/tech track), by **overlay**
(a framework/library on top of a parent track, e.g. FastAPI on Python), or by **transversal
track** (a language-agnostic engineering subject, e.g. Algorithms & Data Structures). All go
through the same loop: open an issue first to discuss scope, then a PR.

**The flagship bar.** A track is **flagship** (vs a review-only track) when it has:
- ≥ 6 modules spanning tooling → syntax → type system → errors → concurrency/async → testing;
- a `## Capstones` section (a `mini_app` and an `interview`);
- `transfer_note` blocks on modules where cross-language transfer applies;
- and it passes `lint_curriculum.py`.

A **review-only track** (e.g. SQL) has no execution harness yet, so mastery is checked by
reading the solution and explaining it rather than by running tests. This bar is a human
review criterion, not a lint rule.

**The transversal-track bar.** A **transversal track** (`kind: transversal`, e.g. Algorithms &
Data Structures) teaches a language-agnostic engineering subject. It is *complete* when it has
≥ 6 `tNN` modules covering the subject's core spine, a `## Capstones` section, and lints clean
under `lint_transversal.py`. It declares `languages: [...]` (the impl languages a learner may
pick); the grader runs the learner's solution in their chosen one. Concepts are namespaced
`<name>:` and track-local. This bar is a human criterion, distinct from the (syntax/tooling-
shaped) flagship bar above.

**A new curriculum** (`tracks/<lang>/curriculum.md`):
- Read an existing track (e.g. `tracks/python/curriculum.md`) — same frontmatter,
  same module shape (`mNN`, `concepts`, `prerequisites`, `mastery`, `exercise_seeds`,
  `resources`).
- Lint locally: `uv run --script tools/lint_curriculum.py tracks/<lang>/curriculum.md`.
- Keep `transverse` concepts truly transverse (they must apply across languages).

**A new overlay** (`tracks/<parent>/overlays/<name>.md`):
- Schema and rules: `tracks/OVERLAYS.md`.
- Lint locally: `uv run --script tools/lint_overlay.py tracks/<parent>/overlays/<name>.md`.
- Namespace every concept `<name>:`. No `transverse` block (frameworks don't claim
  cross-track transfer). Prereqs are either `parent:<concept>` (declared in
  `requires_parent`) or an **earlier** `oNN` module in the same file.
- If a learner already has the topic as a `personal:` extension in their
  `progress/<track>/extensions.md`, follow the promotion path in `OVERLAYS.md`.

**A new transversal track** (`tracks/<name>/curriculum.md` with `kind: transversal`):
- Read `tracks/algorithms/curriculum.md` as the reference. Frontmatter: `kind: transversal`,
  `name`, `display_name`, `languages: [...]`, and `concepts.transversal` (every id namespaced
  `<name>:`). No `transverse`/`language_specific` blocks, no syntax module.
- Modules are `tNN`; prereqs reference an **earlier** `tNN` (document order ⇒ acyclic).
- Lint locally: `uv run --script tools/lint_transversal.py tracks/<name>/curriculum.md`
  (it self-selects by `kind`, so it is safe to point at every `tracks/*/curriculum.md`).

Resources must be official docs (project site, language reference). Étude pulls
current usage via Context7 at teach-time — don't pin minor versions in
`target_version` unless the API genuinely diverges.

## Requirements
- Claude Code, with Context7 available (for current library docs).
- `python3` (for the integrity hook — stdlib only, no install).
- The **toolchain of the track you're learning**, installed and on your `PATH`, so the
  tutor can actually run and grade your code (e.g. `go` for the Go track, a recent Python
  for Python, `node` for TypeScript). Review-only tracks (e.g. SQL) are reviewed
  qualitatively and need no toolchain.
