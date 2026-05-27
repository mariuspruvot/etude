---
name: status
description: Use when the learner asks where they are, their progress, or their weak spots. Renders a dashboard from progress/.
---

# Status

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Read `progress/profile.md` and `progress/skills.md`.
2. Render a compact dashboard:
   - per active track: current module, % of modules touched,
   - competency table grouped by level (mastered / proficient / learning / unknown),
   - personal modules (from `extensions.md`) and recent explorations (from `explorations.md`),
   - weak spots (lowest levels) and concepts due for revision (oldest `last_graded`),
   - a suggested next action.
Read-only: do not modify any files.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
