---
name: teach
description: Use to deliver a focused lesson on the current module's concept(s) before exercises. Pulls current docs/library usage via Context7.
---

# Teach

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

You are not limited to the curated modules: if the learner names a topic with no module
(a framework, a library, a niche), generate the lesson/exercise for it using Context7 for
current docs, and log it in `progress/<track>/explorations.md`.

Personal modules in `progress/<track>/extensions.md` (ids like `x01`) are first-class —
teach/generate from them exactly as from curated modules.

1. Read the current module from `tracks/<track>/curriculum.md` (objectives, concepts, resources).
2. For any library/API/tooling involved, fetch CURRENT usage via Context7 — do not rely on
   recollection. Prefer the `freshness_source` declared in the curriculum frontmatter.
3. Deliver a SHORT lesson (≈ one screen): the idea, one idiomatic example, the top 2–3
   pitfalls. If the learner already knows the concept in another language (per
   `progress/skills.md`), teach by CONTRAST, not from scratch, using the module's `transfer_note`.
4. End by offering an exercise (hand off to `exercise`). Append a one-line note to
   `progress/<track>/log.md`.

Never dump a wall of text. One concept at a time.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
