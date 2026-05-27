---
name: assess
description: Use at the start of learning a track, or when the learner says "I want to learn X". Establishes the learner's level through conversation and seeds progress/profile.md and progress/skills.md, then picks the entry module.
---

# Assess

Goal: figure out where the learner should start, cheaply, by conversation — never by a quiz dump.

1. If `progress/profile.md` is missing, create it from the template in `progress/README.md`.
   Ask 2–3 questions max: which languages they've shipped real code in, their goal, preferred pace.
2. Read `tracks/<track>/curriculum.md`. For each **transverse** concept, check
   `progress/skills.md`. A concept is considered known if level is `proficient`+ OR the
   learner reports real experience with it in another language (record that as evidence:
   `<other-lang> (prior)`).
3. **Syntax never transfers**: always include the track's syntax module (e.g. `go-syntax`,
   `python-syntax`) unless `skills.md` shows it `proficient` (i.e. they used THIS language before).
4. Pick the entry module: the earliest module whose prerequisites are satisfied and whose
   concepts are not all known. Explain the proposed path in 3–5 bullets, and offer to start.
5. Write/update `progress/skills.md` (set known concepts to at least `learning` with evidence)
   and append a line to `progress/<track>/log.md`.

Do NOT teach or generate exercises here — hand off to `teach` or `exercise`.
