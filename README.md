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
- Teaches short lessons: one concept, one idiomatic example, the common pitfalls.
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
Go and Python are full flagship tracks; TypeScript and SQL are stubs (JavaScript is taught as a subset of TypeScript). A track is a
programming language or an adjacent technical subject. Adding one = writing a
`tracks/<track>/curriculum.md` skeleton — contributions welcome.

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

## Requirements
- Claude Code, with Context7 available (for current library docs).
- `python3` (for the integrity hook — stdlib only, no install).
- The **toolchain of the track you're learning**, installed and on your `PATH`, so the
  tutor can actually run and grade your code (e.g. `go` for the Go track, a recent Python
  for Python, `node` for TypeScript). Non-executable tracks (e.g. SQL in v1) are reviewed
  qualitatively and need no toolchain.
