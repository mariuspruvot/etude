---
name: mini-app
description: Use when the learner is ready for a guided multi-file project. Scaffolds the spec and milestones; the learner writes all source files.
---

# Mini-app

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Pick a project from the track's `## Capstones` `mini_app` (or propose one matching the
   learner's mastered concepts).

Equally valid: the learner proposes their OWN project ("a TUI file browser", "a rate
limiter"). Accept it, scope it to their mastered + target concepts, and proceed the same way.

2. Create `progress/<track>/exercises/NNN-miniapp-<slug>/prompt.md` with:
   - a small YAML frontmatter block at the very top recording the concepts and file layout,
     e.g.:
     ```
     ---
     concepts: [concurrency, asyncio, type-system, testing, io-streams]
     ---
     ```
     (`solution_file` does NOT apply here — a mini-app spans multiple files.)
   - the project goal and motivation,
   - a milestone checklist,
   - the file layout the learner should create (list every source file by name — these are
     the files the learner will write; you must not create them, the hook blocks writes under
     `exercises/` except `prompt.md`/`feedback.md`),
   - any starter snippets INSIDE prompt.md as fenced code blocks (do not create source files),
   - and acceptance criteria per milestone.
3. Guide milestone by milestone: as the learner completes each file, dispatch the `grader`
   agent on the exercise folder for a milestone review; give graduated hints, never write
   their code.
4. On completion, write `feedback.md` and update `skills.md` for the involved concepts.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
