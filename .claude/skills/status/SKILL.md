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
   - curated overlays (from `tracks/<track>/overlays/*.md`) the active track has, if any,
   - weak spots (lowest levels) and concepts due for revision (oldest `last_graded`),
   - a suggested next action — here you MAY apply the nudge policy (`.claude/nudge.md`) to
     offer one branch/deep-dive/transversal/mini-app/interview, under its guardrail
     (max 1/session, `suggestions` setting, cooldown). This is the on-demand trigger.
Read-only EXCEPT: if you make a nudge offer, append the single `Nudge:` entry to
`progress/<track>/log.md` (so the cooldown sees it). Otherwise modify no files.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
