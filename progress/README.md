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
active_track: <track>            # the track currently being learned (e.g. go)
created: <YYYY-MM-DD>
---

# Profile
Free-form notes the tutor keeps: strengths, weak spots, preferences (pace, depth).
```

## Template: `skills.md`
```markdown
# Competency map
<!-- level: unknown | learning | proficient | mastered -->

| concept            | level      | last_graded | evidence                         |
|--------------------|------------|-------------|----------------------------------|
| concurrency        | proficient | 2026-05-27  | python (prior), go/exercises/005 |
| error-handling     | learning   | 2026-05-27  | go/exercises/003                 |
```

## Template: `<track>/log.md`
```markdown
# Go — session log
## 2026-05-27
- Entered at m02 (syntax) — known_languages=[python], go-syntax unknown.
- Completed exercise 001 (slices/maps). Score 8/10. concurrency untouched.
```
