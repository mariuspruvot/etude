---
name: revise
description: Use for spaced-repetition review. Re-tests due concepts (skills.md level + last_graded) and resurfaces stale deep-dive explorations, to fight forgetting.
---

# Revise

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Read `progress/skills.md` AND `progress/<track>/explorations.md`. Compute "due" items:
   - Graded concepts: interval by level — `learning` → 3 days, `proficient` → 14 days,
     `mastered` → 45 days (days since `last_graded`).
   - A concept at `learning` with `last_graded: —` (nudged by a deep-dive, never graded) is
     ALWAYS due — testing it is the point.
   - Explorations: the latest dated entry for a topic is its `last_visited`; a topic not
     revisited in > 30 days (flat interval — explorations are ungraded) is due as an optional
     LIGHT recall (a short conceptual question, or an offer to re-`deep-dive`). Acting on it
     writes a new dated entry to `explorations.md`, which resets `last_visited`.
2. Pick the most-overdue concept(s). Generate a SHORT recall exercise via the `exercise`
   skill flow (statement in `prompt.md`, learner writes the solution).
3. Grade via the `grade` flow (which already updates `skills.md` + `last_graded`). What
   revise adds: on success keep/raise the level; on struggle, lower the level one step and
   schedule the concept sooner. A revision struggle IS the documented reason that
   authorizes downgrading a `mastered` concept (the note `grade` requires = "failed
   revision on <date>").
4. If nothing is due, say so and suggest learning new material instead.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
