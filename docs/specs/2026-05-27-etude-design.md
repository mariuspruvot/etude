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
| 8 | v1 scope | All 4 modes (course, exercise, mini-app, interview); Go + Python as full flagships; JS + SQL as stubs |
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

- **The repo = the engine** (versioned, community-maintained): per-language competency
  skeletons + skills/hooks/agents/instructions. **No exercises are pre-written.**
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
├── languages/                # the curated part (lightweight)
│   ├── go/
│   │   ├── curriculum.md      # ordered objectives + concept tags + ecosystem/libs + external resources
│   │   └── CLAUDE.md          # language-specific tutor notes (idioms, tooling: go test, modules)
│   ├── python/
│   │   ├── curriculum.md
│   │   └── CLAUDE.md
│   ├── javascript/           # stub (skeleton present, lightly filled)
│   └── sql/                  # stub
├── .claude/
│   ├── skills/               # assess · teach · exercise · grade · hint · mini-app · interview · status
│   ├── agents/               # grader (runs tests + evaluates) · interviewer (conducts mock interview)
│   ├── hooks/                # protect-solutions (PreToolUse)
│   └── commands/             # /learn /next /grade /hint /status /interview /mini-app
└── progress/                 # GITIGNORED — local only, created on first session
    ├── README.md             # the ONE tracked file (explains the folder)
    ├── profile.md            # who you are, known concepts, goals
    ├── skills.md             # competency map: concept → level + evidence
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
   `languages/go/curriculum.md` → proposes a plan, **skipping mastered concepts** (using
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
- **Unknown language** (not in `languages/`) → Claude can **bootstrap a skeleton on the
  fly**, marked experimental; user can later contribute it upstream.
- **Hook false positives** → the matcher must scope tightly to solution files so Claude
  can still write `prompt.md` / `feedback.md`.
- **Stale freshness** → Context7 is the source for current library/API usage; the tutor
  prefers it over its own recollection for ecosystem questions.
- **git pull** → no conflicts by construction (progress is gitignored).

## 10. v1 Scope vs Roadmap

### v1 (publishable on HN)
- Polished engine: 4 modes (course, exercise, mini-app, interview).
- **Go + Python** as full flagships (including ecosystem/libs: uv/pytest/ruff for Python,
  modules/stdlib/`go test` for Go).
- **JS + SQL** as stubs (skeleton present, lightly filled) to prove the multi-tech model.
- Integrity hook + graduated hints.
- Context7 wired in for freshness.
- On-the-fly skeleton bootstrap for unknown languages (experimental).

### Roadmap (post-v1)
- **Targeted drill** entry door (concept-first / weak-spots-first practice).
- More community-contributed languages.
- Spaced repetition over weak concepts.
- Progress export/sharing (e.g. `git init` inside `progress/` to push to a private repo).
- Dated challenges.

## 11. Testing / Verification

This is primarily a prompt/content repo, so "tests" are mostly behavioral:
- **Hook smoke test**: attempting to write a `progress/**/solution.*` file is blocked.
- **Walkthrough transcripts**: a documented end-to-end session (assess → teach → exercise
  → grade) per flagship language, kept in `docs/` as living examples.
- **Skeleton lint**: each `languages/<lang>/curriculum.md` declares concept tags in a
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

Open:
- Should `progress/` optionally support `git init` inside it for multi-machine persistence
  in v1, or is that strictly roadmap?
- How much of the flagship `curriculum.md` is hand-written vs generated-then-reviewed?
