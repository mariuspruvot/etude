---
name: interview
description: Use when the learner wants to simulate a technical interview for a track. Runs a verbal round plus a graded live-coding round.
---

# Interview

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

1. Confirm the track and scope (concepts to target). Create
   `progress/<track>/exercises/NNN-interview-<slug>/prompt.md` for the live-coding problem,
   using the same YAML frontmatter convention as `exercise`:
   ```
   ---
   solution_file: solution.go
   concepts: [concurrency, error-handling]
   ---
   ```
   `solution_file` is the single canonical filename the candidate will create and write their
   solution in; the `grader` agent reads this field to locate the solution.
2. Dispatch the `interviewer` agent to run the session (verbal + live-coding). The
   live-coding solution is written by the candidate (named per the `prompt.md` `solution_file`
   field) and scored by the `grader` agent.
3. Write `feedback.md` with the debrief (verbal score, coding score, communication,
   next steps) and update `skills.md` for the assessed concepts. Completing an interview is a
   **palier point**: you MAY apply the nudge policy (`.claude/nudge.md`) to offer one next step
   under its guardrail.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
