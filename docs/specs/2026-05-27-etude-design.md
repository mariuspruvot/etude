# Étude — Design Spec

- **Date**: 2026-05-27
- **Status**: Approved for spec review
- **Author**: Marius Pruvot (brainstormed with Claude)

## 1. Summary

**Étude** is a public, clone-and-go GitHub repository that turns Claude Code into a
personal programming tutor. The user clones the repo, opens Claude Code, says *"I want
to learn Go"*, and the repo becomes a tutor that:

- assesses the user's level through conversation,
- delivers short lessons,
- generates exercises calibrated to the user's level,
- executes the user's code and grades it,
- tracks competencies over time,
- and scales up to guided mini-apps and mock technical interviews.

The repo ships an **engine** (skeletons + instructions), **not** a bank of pre-written
courses or exercises. All exercise content is generated on the fly. Personal progress
lives locally and is never committed.

Pitch (HN framing): *"git clone, launch Claude, say 'I want to learn Go' — from zero to
the technical interview."*

## 2. Goals & Non-Goals

### Goals
- A polished, credible learning loop for a senior dev who transfers existing knowledge.
- Clone-and-go: zero account, zero setup beyond cloning + Claude Code.
- Community-extensible: adding a language = writing a skeleton, not authoring exercises.
- Pedagogical integrity: the tutor guides, it does not solve.

### Non-Goals (v1)
- Not multi-LLM. Étude targets **Claude Code fully** (skills, hooks, agents, slash
  commands, memory). Portability to other tools is explicitly out of scope for v1.
- Not a monetized product. Personal + community tool, open-source.
- No hosted backend, no accounts, no telemetry.

## 3. Key Decisions (from brainstorming)

| # | Decision | Choice |
|---|----------|--------|
| 1 | Target LLM | Claude Code, fully (no portability compromise) |
| 2 | Content source | Hybrid: repo ships the **engine** (concept skeletons + instructions); exercises are **100% generated on the fly** |
| 3 | Structure axis | **Language on the surface, concept tags in depth** — navigate by language, track by transverse competency |
| 4 | Progress storage | `progress/` is the **source of truth**, gitignored, local-only; Claude Code memory is a **convenience cache** |
| 5 | Session piloting | **Hybrid**: natural language (root `CLAUDE.md` router) + slash-command shortcuts |
| 6 | Grading | **Execution when relevant** — run code/tests if testable, otherwise qualitative review |
| 7 | Tutor integrity | **Hook (hard guard) + graduated hints** — a PreToolUse hook blocks Claude from writing solution files; the skill reveals hints by tiers |
| 8 | v1 scope | 6 modes (course, exercise, mini-app, interview, revise, validate); Go + Python as full flagships; JS + SQL as stubs |
| 8b | Track abstraction | Unit is a **track** (prog language or adjacent tech subject); `tracks/` dir; engine subject-agnostic, v1 positioning stays programming/tech |
| 9 | Name | **Étude** (musical étude = progressively harder practice pieces, repeated to master) |

## 4. Entry Door

v1 has a single entry door, backed by the engine:

1. **Path** (broad): *"I want to learn Go"* → full curriculum, skipping concepts already
   mastered (detected via transverse competency tags — prior Python knowledge counts).

**Roadmap — targeted drill** (narrow): *"I'm struggling with goroutines"* / *"drill my
weak spots"* → Claude jumps straight to a concept (or picks low-scoring concepts from
`skills.md`) and generates focused exercises, without replaying the whole path. Deferred
to keep v1 focused; it is an additional entry path inside `assess`/`exercise`, not a new
mode, so it slots in cheaply later.

## 5. Repo / Personal Split (architecture keystone)

- **The repo = the engine** (versioned, community-maintained): per-track competency
  skeletons + skills/hooks/agents/instructions. **No exercises are pre-written.**

> **Track generality.** The engine is subject-agnostic — a `curriculum.md` is just
> "objectives + concept tags + mastery criteria + exercise seeds", which fits any
> technical subject. The unit is a **track**: a programming language (Go, Python) *or* an
> adjacent technical subject (SQL, design systems, DevOps, AWS). Executable tracks run
> tests in `grade`; non-executable ones (e.g. design systems) degrade gracefully to
> qualitative review (decision #6). **v1 positioning stays programming/tech**; nothing in
> the architecture bakes in "programming only", so new tracks slot in without engine
> changes. Broader non-tech subjects (math, languages, history) are a long-term
> possibility, explicitly out of v1 scope.
- **`progress/` = the user** (gitignored, source of truth): profile, competency map,
  generated exercises, corrections. Claude Code memory is a comfort cache only.

Consequence: `git pull` pulls engine improvements without ever touching personal
progress, and adding a language is cheap (write a skeleton, not an exercise bank).

## 6. Repository Layout

```
etude/
├── README.md                 # pitch + quickstart
├── CLAUDE.md                 # root router: detect intent, load progress/, route to a mode
├── .gitignore                # ignores progress/ (except progress/README.md)
├── tracks/                   # the curated part (lightweight). A track = a prog language
│   │                         # OR an adjacent technical subject (SQL, design-systems...)
│   ├── go/
│   │   ├── curriculum.md      # ordered objectives + concept tags + ecosystem/libs + external resources
│   │   └── CLAUDE.md          # track-specific tutor notes (idioms, tooling: go test, modules)
│   ├── python/
│   │   ├── curriculum.md
│   │   └── CLAUDE.md
│   ├── javascript/           # stub (skeleton present, lightly filled)
│   └── sql/                  # stub
├── .claude/
│   ├── skills/               # assess · teach · exercise · grade · hint · mini-app · interview · status · revise · validate
│   ├── agents/               # grader (runs tests + evaluates) · interviewer (conducts mock interview)
│   ├── hooks/                # protect-solutions (PreToolUse)
│   └── commands/             # /learn /next /grade /hint /status /interview /mini-app /revise /validate
└── progress/                 # GITIGNORED — local only, created on first session
    ├── README.md             # the ONE tracked file (explains the folder)
    ├── profile.md            # who you are, known concepts, goals
    ├── skills.md             # competency map: concept → level + last-graded date + evidence
    └── go/
        ├── log.md            # session journal
        └── exercises/001-goroutines/{prompt.md, solution.go, feedback.md}
```

> **Assumption / to finalize at implementation:** exact slash-command names, file paths,
> directory names, and the PreToolUse hook matcher are proposals here, marked
> `[claude-guessed]`. They are not verified against a working Claude Code config yet.

### `.gitignore` mechanism

```gitignore
progress/*
!progress/README.md   # tracked: explains the folder; everything else is local-only
```

The `progress/` directory physically lives at the root of the clone (everything under the
user's eyes), but its contents are ignored by Git. Claude creates it on first session. It
never appears in `git status`, is never committed, and never conflicts on `git pull`.

## 7. The Engine: Skills, Agents, Hooks, Commands

### Skills
- **assess** — detect level through conversation; seed/update `profile.md` and
  `skills.md`. Two entry doors (path vs targeted drill).
- **teach** — deliver a focused lesson on a concept; pull fresh docs/library usage via
  Context7.
- **exercise** — generate a calibrated exercise into `progress/<lang>/exercises/NNN/`
  (statement + starter + hidden/reference tests when testable); tag it with concept(s).
- **grade** — evaluate a solved exercise (execution when relevant, else review); write
  `feedback.md`; update `skills.md` (level + evidence) and `log.md`.
- **hint** — graduated hints (orientation → lead → pseudo-code), never the full solution.
- **mini-app** — guided multi-file project mode.
- **interview** — mock technical interview mode. Includes a **live-coding segment**: the
  candidate writes code under interview conditions, which the `grader` agent executes and
  scores (correctness + reasoning), in addition to verbal Q&A.
- **status** — render a progress dashboard from `progress/`.
- **revise** — spaced-repetition review: re-tests concepts whose `skills.md` entry is due
  (based on last-graded date + level), to fight forgetting before re-learning is needed.
- **validate** — exam mode: no teaching, just prove mastery of a concept/track via a
  graded assessment (uses the `grade`/`grader` path). Useful to certify an existing skill
  without replaying its path.

### Agents (subagents)
- **grader** — runs tests / executes code in isolation, returns structured evaluation.
- **interviewer** — conducts the mock interview as a focused persona; for the live-coding
  segment it hands the candidate's code to the `grader` agent for execution and scoring.

### Hooks
- **protect-solutions** (PreToolUse) — blocks Write/Edit on user solution files (e.g.
  `progress/**/solution.*`). Claude may read, execute, comment, and write `prompt.md` /
  `feedback.md`, but the solution must be typed by the user. Hard guard, not bypassable by
  prompt. `[claude-guessed: exact matcher path]`

### Commands
`/learn <lang>`, `/next`, `/grade`, `/hint`, `/status`, `/interview`, `/mini-app`.
Natural language always works in parallel via the root `CLAUDE.md` router.
`[claude-guessed: command names]`

## 8. The Learning Loop (data flow)

1. **Session start** → `CLAUDE.md` reads `progress/profile.md` + `skills.md` → greets the
   user at their current position.
2. **"learn Go"** (path) or **"drill goroutines"** (targeted) → `assess` (if new) → reads
   `tracks/go/curriculum.md` → proposes a plan, **skipping mastered concepts** (using
   transverse tags — prior knowledge in other languages counts).
3. **teach** → Context7 for fresh docs/libs → short lesson.
4. **/next** → `exercise` generates a calibrated exercise into
   `progress/go/exercises/NNN/` (statement + starter + tests), concept-tagged.
5. **User writes `solution.go`** — the **protect-solutions hook blocks** Claude from
   writing it.
6. **/grade** → `grader` agent runs tests (if relevant) else reviews → writes
   `feedback.md`, updates `skills.md` and `log.md`.
7. **/hint** → graduated hints.
8. Advanced modes: **/mini-app** (guided multi-file project), **/interview** (mock
   interview via the `interviewer` agent).

## 9. Edge Cases & Error Handling

- **No progress yet** → onboarding via `assess`; create `progress/` scaffold.
- **Unknown track** (not in `tracks/`) → Claude can **bootstrap a skeleton on the
  fly**, marked experimental; user can later contribute it upstream.
- **Hook false positives** → the matcher must scope tightly to solution files so Claude
  can still write `prompt.md` / `feedback.md`.
- **Stale freshness** → Context7 is the source for current library/API usage; the tutor
  prefers it over its own recollection for ecosystem questions.
- **git pull** → no conflicts by construction (progress is gitignored).

## 10. v1 Scope vs Roadmap

### v1 (publishable on HN)
- Polished engine: 6 modes (course, exercise, mini-app, interview, **revise**,
  **validate**).
- **Go + Python** as full flagship tracks (including ecosystem/libs: uv/pytest/ruff for
  Python, modules/stdlib/`go test` for Go).
- **JS + SQL** as stub tracks (skeleton present, lightly filled) to prove the multi-track
  model.
- Integrity hook + graduated hints.
- Context7 wired in for freshness.
- On-the-fly skeleton bootstrap for unknown tracks (experimental).
- Engine is track-agnostic (positioning stays programming/tech for v1).

### Roadmap (post-v1)
- **Targeted drill** entry door (concept-first / weak-spots-first practice).
- More community-contributed tracks — first the adjacent tech ones (design systems,
  DevOps, AWS), since they slot into the existing engine.
- Non-tech subjects (math, languages, history) — longer-term, validates full generality.
- Progress export/sharing (e.g. `git init` inside `progress/` to push to a private repo).
- Dated challenges.

## 11. Testing / Verification

This is primarily a prompt/content repo, so "tests" are mostly behavioral:
- **Hook smoke test**: attempting to write a `progress/**/solution.*` file is blocked.
- **Walkthrough transcripts**: a documented end-to-end session (assess → teach → exercise
  → grade) per flagship language, kept in `docs/` as living examples.
- **Skeleton lint**: each `tracks/<track>/curriculum.md` declares concept tags in a
  consistent frontmatter shape (so transverse tracking works).

## 12. Assumptions

- *Claude Code supports repo-local skills/hooks/agents/commands that ship inside the cloned
  repo and activate on session start* — core premise of the whole design; needs a
  confirming spike before heavy investment. `[claude-guessed]`
- *Context7 skill/MCP is available in the user's Claude Code setup* — used for library
  freshness; if absent, the tutor degrades to its own knowledge. `[claude-guessed]`
- *A PreToolUse hook can reliably scope a matcher to solution files only* — load-bearing
  for the integrity guard. `[claude-guessed]`
- *Concept tags can stay a lightweight frontmatter list, not a maintained graph DB* —
  chosen for low maintenance; revisit if cross-language inference proves too weak.
- *Slash-command names, directory names, and file paths in §6–7* — proposed defaults, not
  yet validated. `[claude-guessed]`
- *Generated exercises are good enough without a human-curated bank* — central bet of the
  "engine, not content" model; the flagship walkthroughs are how we validate it.
- *Name "Étude" is available on GitHub* — not yet checked. `[claude-guessed]`

## 13. Resolved & Open Questions

Resolved during brainstorming:
- Mock interviews → **verbal Q&A + a live-coding segment** graded by the `grader` agent.
- Targeted drill → **roadmap**, not v1 (single "path" entry door at launch).
- `git init` inside `progress/` for multi-machine persistence → **roadmap**, not v1.
- Engine unit → **track** (prog language or adjacent tech subject); v1 positioning stays
  programming/tech, architecture stays subject-agnostic.
- Revise + validate modes → **v1** (6 modes total).

Open:
- How much of the flagship `curriculum.md` is hand-written vs generated-then-reviewed?

## Appendix A — `curriculum.md` reference example

This is the most important file format in the repo: the per-track **skeleton** the
engine reads. It is curated and lightweight — it contains **objectives, concept tags,
ecosystem pointers, resources, and mastery criteria**, but **no lessons and no
exercises** (those are generated on the fly). The example below is a realistic
`tracks/go/curriculum.md` that an implementer can copy as the canonical shape.

### A.1 File contract

- **Frontmatter** declares language metadata + the concept vocabulary this curriculum
  uses, split into `transverse` (shared across languages, the keys that drive
  `progress/skills.md`) and `language_specific` (Go-only nuances).
- **Modules** are an ordered list. Each module declares: `id`, `title`, `concepts`
  (referencing the vocabulary), `prerequisites` (module ids), `ecosystem` (libs/tools the
  module touches), `resources` (external links), `mastery` (observable criteria the
  `grade` skill checks before marking the concept advanced), and `exercise_seeds`
  (high-level prompts the `exercise` skill expands — NOT full exercises).
- The `assess` skill reads `concepts.transverse`, cross-references the learner's
  `skills.md`, and **skips or fast-forwards** modules whose transverse concepts are
  already mastered.
- **Syntax never transfers.** Language syntax/primitives is modeled as a
  `language_specific` concept (`go-syntax`), so a learner who is senior elsewhere but new
  to this language still gets the syntax module — taught fast and by contrast, not from
  scratch. `assess` only skips it if the learner has used *this* language before.

### A.2 Example: `tracks/go/curriculum.md`

```markdown
---
language: go
display_name: Go
target_version: "1.23"          # tutor calibrates to this; Context7 fetches current docs
freshness_source: context7      # prefer Context7 over model recollection for libs/APIs
maintainers: [community]

# Concept vocabulary. transverse keys are the canonical ids written to progress/skills.md.
concepts:
  transverse:                   # shared across languages — drive cross-language transfer
    - error-handling
    - concurrency
    - type-system
    - testing
    - interfaces-polymorphism
    - memory-model
    - dependency-management
    - io-streams
  language_specific:            # Go-only nuance, tracked but not transferred
    - go-syntax                 # variables, control flow, slices/maps, range — NEVER transfers
    - goroutines
    - channels
    - go-modules
    - struct-embedding
    - defer-panic-recover
    - go-error-wrapping
---

# Go — Curriculum

> Target audience: developers comfortable in at least one language. The `assess` skill
> establishes the learner's transverse level first, then enters at the right module.

## Modules

### m01 — Tooling & project layout
- id: m01
- concepts: [dependency-management, go-modules]
- prerequisites: []
- ecosystem:
    tools: [go build, go run, go vet, gofmt]
    libs: []
    files: [go.mod, go.sum]
- resources:
    - https://go.dev/doc/tutorial/getting-started
    - https://go.dev/ref/mod
- mastery:
    - initializes a module and adds/removes a dependency without help
    - explains the role of go.mod vs go.sum
- exercise_seeds:
    - "scaffold a CLI module that imports one third-party lib and runs `go vet` clean"

### m02 — Syntax & primitives
- id: m02
- concepts: [go-syntax]
- prerequisites: [m01]
- ecosystem:
    tools: [gofmt, go run]
    libs: [fmt]
- resources:
    - https://go.dev/tour/basics/1
    - https://go.dev/tour/flowcontrol/1
- mastery:
    - declares variables (var, :=), writes loops/conditionals, and functions idiomatically
    - uses slices and maps correctly (length vs capacity, range, nil map pitfalls)
- exercise_seeds:
    - "implement small pure functions over slices and maps (group, filter, count)"
- transfer_note: |
    This module does NOT transfer across languages — being senior elsewhere does not mean
    you know Go's syntax. assess only skips m02 if skills.md shows go-syntax already
    proficient (i.e. the learner has used Go before). For a paradigm-experienced newcomer,
    teach syntax fast but DO teach it: contrast with their known language ("Go's slices
    are not Python lists: ...") rather than from scratch.

### m03 — Types, structs & the type system
- id: m03
- concepts: [type-system, struct-embedding]
- prerequisites: [m02]
- ecosystem:
    tools: [go vet]
    libs: [encoding/json]
- resources:
    - https://go.dev/tour/moretypes/2
    - https://go.dev/blog/json
- mastery:
    - models a domain with structs + composition (not inheritance)
    - marshals/unmarshals JSON with correct struct tags
- exercise_seeds:
    - "model an order with nested structs and round-trip it through JSON"
- transfer_note: |
    If type-system is already mastered (e.g. from a typed language), compress the
    primitives lesson and emphasize Go specifics: zero values, value vs pointer
    receivers, struct embedding instead of inheritance.

### m04 — Errors & error handling
- id: m04
- concepts: [error-handling, go-error-wrapping]
- prerequisites: [m03]
- ecosystem:
    libs: [errors, fmt]
- resources:
    - https://go.dev/blog/error-handling-and-go
    - https://go.dev/blog/go1.13-errors
- mastery:
    - returns and checks errors idiomatically (no panic for control flow)
    - wraps with %w and inspects with errors.Is / errors.As
- exercise_seeds:
    - "build a parser that wraps low-level errors with context and is testable with errors.Is"

### m05 — Interfaces & polymorphism
- id: m05
- concepts: [interfaces-polymorphism]
- prerequisites: [m03]
- ecosystem:
    libs: [io, sort]
- resources:
    - https://go.dev/tour/methods/9
    - https://go.dev/doc/effective_go#interfaces
- mastery:
    - defines small interfaces at the consumer, not the producer
    - explains the empty interface / any and when to avoid it
- exercise_seeds:
    - "implement io.Writer for a custom sink and plug it into the standard library"

### m06 — Concurrency: goroutines & channels
- id: m06
- concepts: [concurrency, goroutines, channels, memory-model]
- prerequisites: [m04]
- ecosystem:
    tools: [go test -race]
    libs: [sync, context]
- resources:
    - https://go.dev/tour/concurrency/1
    - https://go.dev/blog/pipelines
    - https://go.dev/ref/mem
- mastery:
    - chooses channels vs sync primitives appropriately
    - cancels work with context and avoids goroutine leaks
    - code passes `go test -race`
- exercise_seeds:
    - "build a bounded worker pool with graceful shutdown via context"
- transfer_note: |
    If concurrency is mastered (e.g. Python asyncio, JS event loop), skip the conceptual
    intro and contrast models directly: CSP/channels vs async-await, the race detector,
    the Go memory model's happens-before guarantees.

### m07 — Testing & benchmarks
- id: m07
- concepts: [testing]
- prerequisites: [m04]
- ecosystem:
    tools: [go test, go test -bench, go test -cover]
    libs: [testing, testify]
- resources:
    - https://go.dev/doc/tutorial/add-a-test
    - https://pkg.go.dev/testing
- mastery:
    - writes table-driven tests
    - measures coverage and writes a benchmark
- exercise_seeds:
    - "convert an existing function to table-driven tests and add a benchmark"

## Capstones (feed the mini-app and interview modes)
- mini_app: "a concurrent CLI that fetches N URLs with a worker pool, bounded
  concurrency, context cancellation, and table-driven tests" — concepts: [concurrency,
  error-handling, testing, io-streams]
- interview: "live-coding: implement an LRU cache; verbal: explain the Go memory model
  and when a mutex beats a channel" — concepts: [concurrency, type-system, memory-model]
```

### A.3 How this drives the engine

- **`assess`** reads `concepts.transverse`, compares against `progress/skills.md`, and
  picks the entry module. A senior Python dev mastering concurrency does **not** skip to
  `m06`: `language_specific` concepts like `go-syntax` (m02) gate the path, so they still
  cover syntax (fast, by contrast) before the concurrency module compresses what they
  already know. `transfer_note` blocks tell the tutor how to compress known ground.
- **Level granularity** — `skills.md` tracks each concept on a fixed scale so the skip
  logic is deterministic: `unknown → learning → proficient → mastered`. `assess` skips a
  module only when every one of its concepts is `proficient`+ (transverse) or the language
  was used before (`language_specific`). `grade` is what promotes a concept up the scale,
  with the graded exercise recorded as evidence.
- **`teach`** expands a module into a lesson, pulling current API/lib usage via Context7
  (`freshness_source`), not the module's static links alone.
- **`exercise`** expands an `exercise_seed` into a concrete, calibrated exercise written to
  `progress/go/exercises/NNN/`, tagging it with the module's `concepts`.
- **`grade`** checks the solution against the module's `mastery` criteria (executing tests
  when relevant) and updates the matching `concepts` in `skills.md` with a level + the
  exercise as evidence.
- **mini-app / interview** modes seed from the `## Capstones` block.

> Authoring note (open question §13): flagship `curriculum.md` files are intended to be
> hand-written for quality, but the format is deliberately simple enough that a draft can
> be generated and then human-reviewed before merging.
