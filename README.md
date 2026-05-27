# Étude

Clone this repo, open it with Claude Code, and say *"I want to learn Go"* — it becomes your
personal programming tutor: assesses your level, teaches, generates exercises calibrated to
you, runs your code, grades it, and tracks your progress over time. From zero to the
technical interview.

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

## Requirements
- Claude Code, with Context7 available (for current library docs).
- `python3` (for the integrity hook — stdlib only, no install).
- The **toolchain of the track you're learning**, installed and on your `PATH`, so the
  tutor can actually run and grade your code (e.g. `go` for the Go track, a recent Python
  for Python, `node` for TypeScript). Non-executable tracks (e.g. SQL in v1) are reviewed
  qualitatively and need no toolchain.
