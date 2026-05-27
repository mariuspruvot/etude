---
name: teach
description: Use to deliver a focused lesson on the current module's concept(s) before exercises. Pulls current docs/library usage via Context7.
---

# Teach

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Read the current module from `tracks/<track>/curriculum.md` (objectives, concepts, resources).
2. For any library/API/tooling involved, fetch CURRENT usage via Context7 — do not rely on
   recollection. Prefer the `freshness_source` declared in the curriculum frontmatter.
3. Deliver a SHORT lesson (≈ one screen): the idea, one idiomatic example, the top 2–3
   pitfalls. If the learner already knows the concept in another language (per
   `progress/skills.md`), teach by CONTRAST, not from scratch, using the module's `transfer_note`.
4. End by offering an exercise (hand off to `exercise`). Append a one-line note to
   `progress/<track>/log.md`.

Never dump a wall of text. One concept at a time.
