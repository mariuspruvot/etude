---
name: assess
description: Use at the start of learning a track, or when the learner says "I want to learn X". Establishes the learner's level through conversation and seeds progress/profile.md and progress/skills.md, then picks the entry module.
---

# Assess

Goal: figure out where the learner should start, cheaply, by conversation — never by a quiz dump.

1. If `progress/profile.md` is missing, create it from the template in `progress/README.md`.
   Ask 2–3 questions max: which languages they've shipped real code in, their goal, preferred pace.
   Record the track being learned as an `active_track: <track>` field in the profile frontmatter
   (create or update it).
2. Read `tracks/<track>/curriculum.md`. For each **transverse** concept, check
   `progress/skills.md`. A concept is considered known if level is `proficient`+ OR the
   learner reports real experience with it in another language (record that as evidence:
   `<other-lang> (prior)`).
3. **Syntax never transfers**: always include the track's syntax module (e.g. `go-syntax`,
   `python-syntax`) unless `skills.md` shows it `proficient` (i.e. they used THIS language before).
4. Pick the entry module: the earliest module whose prerequisites are satisfied and whose
   concepts are not all known. Explain the proposed path in 3–5 bullets, and offer to start.
5. Write/update `progress/skills.md`. Set the level by reported depth: `learning` by default;
   `proficient` if the learner describes substantive real-world use; `mastered` only with
   specific advanced evidence. For entries inferred from prior experience (not a graded
   exercise), set `last_graded` to `—` and evidence to `<lang> (prior)`. Then append a line
   to `progress/<track>/log.md`.

Do NOT teach or generate exercises here — hand off to `teach` or `exercise`.
