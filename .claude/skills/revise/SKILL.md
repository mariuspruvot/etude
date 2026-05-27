---
name: revise
description: Use for spaced-repetition review. Re-tests concepts that are due based on skills.md level + last_graded date, to fight forgetting.
---

# Revise

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Read `progress/skills.md`. Compute "due" concepts using a simple interval by level:
   `learning` → 3 days, `proficient` → 14 days, `mastered` → 45 days (days since `last_graded`).
2. Pick the most-overdue concept(s). Generate a SHORT recall exercise via the `exercise`
   skill flow (statement in `prompt.md`, learner writes the solution).
3. Grade via the `grade` flow (which already updates `skills.md` + `last_graded`). What
   revise adds: on success keep/raise the level; on struggle, lower the level one step and
   schedule the concept sooner. A revision struggle IS the documented reason that
   authorizes downgrading a `mastered` concept (the note `grade` requires = "failed
   revision on <date>").
4. If nothing is due, say so and suggest learning new material instead.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
