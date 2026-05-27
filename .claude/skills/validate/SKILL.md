---
name: validate
description: Use when the learner wants to prove mastery of a concept/track without re-learning it (exam mode). No teaching, just a graded assessment.
---

# Validate

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Confirm the concept(s) or whole track to validate. Do NOT teach or give hints.
2. Generate 1–3 assessment exercises (via the `exercise` flow) covering the target
   concepts at `proficient`/`mastered` difficulty. Learner writes solutions.
3. Grade strictly via the `grader` agent. Aggregate into a pass/fail per concept.
4. Update `skills.md`: set passed concepts to `proficient` (or `mastered` if already
   proficient and the assessment was hard), with `last_graded` = today and evidence.
   Report a clear verdict ("validated: concurrency, error-handling; not yet: testing").
