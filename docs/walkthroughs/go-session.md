# Walkthrough — Go session (manual runtime verification, Task 21)

- **Date**: 2026-05-27
- **Environment**: Claude Code 2.1.152, Opus 4.7, repo opened at the `feat/etude-v1` worktree.
- **Purpose**: confirm the assembled engine *behaves* in a real interactive session (the
  feasibility spike already proved the components *load*).

## Verdict: PASS

The full loop works end-to-end, and the integrity guarantee holds on both layers
(instruction-level refusal **and** the hook backstop). Two non-blocking findings recorded
below.

## What was verified

| Check | Result | Notes |
|-------|--------|-------|
| Folder-trust prompt on first open | ✅ | Accepted once (the one-time gate from the spike). |
| Slash-command discovery (`/`) | ✅ (with finding B) | All 9 Étude commands present, but interleaved with the user's personal/global commands. |
| Persistence / resume | ✅ | A prior session had run `assess`; on re-entry `assess` detected existing `progress/profile.md` + `skills.md` and **did not re-quiz** — it resumed at the recorded position. This is the "Claude knows where you are" promise. |
| Entry-point selection | ✅ | Entered at **m01 (Tooling)**, correctly — Go modules are unknown even though dependency-management transfers from Python. (Earlier checklist text said "m02"; the curriculum orders tooling→syntax, so m01 is right.) |
| `teach` + Context7 freshness | ✅ | Pulled current Go **1.24** module/tooling docs via Context7 and taught m01 *by contrast with Python* (`go.mod`≈`pyproject.toml`, `go.sum`≈`uv.lock`), including the 1.24 `go get -tool` note. |
| `exercise` artifact | ✅ | Created `progress/go/exercises/001-cli-module-scaffold/prompt.md` with frontmatter `solution_file: main.go`, `concepts: [go-modules, dependency-management]`, `module: m01`. Did **not** write the solution; starter code placed in `prompt.md`; told the learner to create `main.go`. Index `001` computed correctly. |
| `grade` judgment on a non-attempt | ✅✅ | Given a deliberately-empty `main.go` (`print("hello")`, no `go.mod`), `grade` **refused to stamp a grade**, left `skills.md` untouched, and wrote an honest `feedback.md` ("Not yet attempted — not graded"). It also detected that `go` is not installed before attempting to build. |
| Integrity — "do the exercise for me" | ✅✅✅ | Claude **refused** ("that's the one thing I won't do"), cited the integrity hook, and pivoted to **graduated hints** (Level 1 shape → Level 2 sequence), never writing the solution. |
| Integrity — hook backstop | ✅ (by script) | The PreToolUse hook was verified to block `Write`/`Edit`/`MultiEdit`/`NotebookEdit` of a solution file under `progress/*/exercises/*` (exit 2), and allow `prompt.md`/`feedback.md` (exit 0). In-session the hook didn't need to fire because the instruction layer held (Claude declined to attempt the write) — both layers confirmed. |

## Findings (non-blocking)

- **A — toolchain requirement was undocumented.** Running a Go exercise needs `go` on
  `PATH`; the machine didn't have it, and the README only listed `python3`. **Fixed**: the
  README Requirements section now states the learner must install the track's toolchain
  (e.g. `go`, `node`) for executable exercises/grading.
- **B — command discoverability.** The 9 Étude commands appear interleaved with the user's
  personal/global slash commands, making them harder to spot. **Decision for v1**: keep the
  flat, documented names (`/learn`, `/next`, …) since that is the validated UX. **Roadmap**:
  consider namespacing under `.claude/commands/etude/` → `/etude:learn` if users report
  clutter.

## Conclusion

The engine is runtime-validated and ready to merge. Nothing observed would embarrass on an
HN launch; the headline guarantee (Claude guides, the learner writes the code) holds.
