# Your progress lives here

This directory is **local-only** (gitignored). Étude creates and updates files here as
you learn. It is the **source of truth** for your progress — Claude Code memory is only a
cache. Back it up by copying this folder.

## Files Claude maintains
- `profile.md` — who you are, prior experience, goals.
- `skills.md` — competency map: each concept's level, last-graded date, and evidence.
- `<track>/log.md` — session journal per track.
- `<track>/exercises/NNN-<slug>/` — one folder per exercise:
  - `prompt.md` — the exercise statement + starter code (written by Claude).
  - your solution file, e.g. `solution.go` (**you** write this — Claude is blocked from it).
  - `feedback.md` — Claude's evaluation (written by Claude).

## Level scale
`unknown → learning → proficient → mastered`

## Template: `profile.md`
```markdown
---
display_name: <name or alias>
known_languages: [python]        # languages the learner has shipped real code in
goals: "<what the learner wants to achieve>"
language: en                     # learner's preferred prose language (bcp47); code stays English
active_track: <track>            # the track currently being learned (e.g. go)
suggestions: normal              # proactive-nudge frequency: off | rare | normal (missing ⇒ normal)
created: <YYYY-MM-DD>
---

# Profile
Free-form notes the tutor keeps: strengths, weak spots, preferences (pace, depth).
```
`suggestions` controls proactive nudges (offers to branch, deep-dive, try a transversal track,
etc.): `normal` = all triggers, `rare` = only after mastering something, `off` = none. See
`.claude/nudge.md`.

## Template: `skills.md`
```markdown
# Competency map
<!-- level: unknown | learning | proficient | mastered -->

| concept            | level      | last_graded | evidence                         |
|--------------------|------------|-------------|----------------------------------|
| concurrency        | proficient | 2026-05-27  | python (prior), go/exercises/005 |
| error-handling     | learning   | 2026-05-27  | go/exercises/003                 |
```
`last_graded` may be `—` for levels inferred from prior experience (not yet graded).

Personal concepts (from `extensions.md`) are written with a `personal:` prefix in the
concept column and are **track-local** (not counted as transverse transfer).

## Template: `<track>/log.md`
```markdown
# Go — session log
## 2026-05-27
- Entered at m02 (syntax) — known_languages=[python], go-syntax unknown.
- Completed exercise 001 (slices/maps). Score 8/10. concurrency untouched.
```

## Template: `<track>/explorations.md`
```markdown
# Explorations — off-curriculum digressions (track-local log)
## 2026-05-27 — goroutine scheduler internals
- Discussed GMP model, work-stealing. Not a graded module. Follow-up: maybe promote.
```

> Revision: `revise` treats the latest dated entry for a topic as its `last_visited` and
> resurfaces a topic not revisited in > 30 days as an optional light recall. A `learning`
> concept in `skills.md` with `last_graded: —` (deep-dive nudge) is always due. No new field.

## Template: `<track>/extensions.md`
```markdown
# Personal modules — promoted from repeated exploration (NOT shared/linted)
### x01 — Goroutine scheduler internals
- id: x01
- concepts: [personal:go-scheduler]
- prerequisites: [m06]
- mastery:
    - explains GMP, work-stealing, GOMAXPROCS effects
- exercise_seeds:
    - "trace why a CPU-bound goroutine starves others without runtime.Gosched"
```

> Promotion: a personal extension module that proves valuable can graduate to a **shared
> curated overlay** under `tracks/<parent>/overlays/<name>.md` (ids `xNN`→`oNN`, concepts
> `personal:foo`→`<name>:foo`, then linted by `tools/lint_overlay.py`). See `tracks/OVERLAYS.md`.
