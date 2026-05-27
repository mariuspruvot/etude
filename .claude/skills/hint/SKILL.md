---
name: hint
description: Use when the learner is stuck on the current exercise and asks for help. Gives graduated hints, never the full solution.
---

# Hint

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

Reveal help in TIERS, one tier per request. Record the current tier in
`progress/<track>/log.md` so a later `/hint` continues at the next tier. This is a
continuity/learner record only — it does not automatically change the grade.

- Tier 1 — orientation: restate the goal, point to the relevant concept/doc.
- Tier 2 — lead: name the approach or data structure, without code.
- Tier 3 — pseudo-code / partial structure: outline steps, leave the code to the learner.

NEVER write the solution file (the hook blocks it) and NEVER paste a complete working
solution in chat. If the learner insists, escalate at most to tier 3 and explain that
solving it themselves is the point.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
