---
name: deep-dive
description: Use when the learner wants to explore a concept or topic in depth — internals, trade-offs, cross-language contrasts, history, edge cases — in an open Socratic discussion rather than the short teach lesson.
---

# Deep-dive

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`). The topic may be ANY topic, with or without a curated module.

1. Open, back-and-forth discussion that goes as deep as the learner wants: internals,
   trade-offs, "why is it designed this way", cross-language contrasts, edge cases. Pull
   current docs via Context7 — do not rely on recollection for libraries/APIs.
2. You MAY write example code in the chat for exposition. You must NOT write into
   `progress/*/exercises/*` (the hook blocks it), and you must not solve a pending exercise.
3. Log what was covered in `progress/<track>/explorations.md` (topic, date, key points).
   You may nudge a related concept to `learning` in `skills.md` if genuinely demonstrated.
4. Promotion: OFFER to promote this niche to a personal module when the SAME niche appears
   for the 2nd time in `progress/<track>/explorations.md` (topic matching is by judgment),
   OR when the learner asks. Never impose. Append a module to
   `progress/<track>/extensions.md` (id `xNN`, `personal:` concept, mastery, exercise_seeds);
   mention it can later be PR'd to share it — as a curated overlay
   (`tracks/<track>/overlays/<name>.md`, see `tracks/OVERLAYS.md`) for a framework/library,
   or into `curriculum.md` for a true core-language gap.
5. End by offering a relevant exercise (hand to `exercise`) when it would help.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
