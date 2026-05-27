---
name: grade
description: Use when the learner has written a solution and wants it evaluated. Runs the grader agent, writes feedback.md, and updates skills.md + log.md.
---

# Grade

1. Locate the exercise folder and the learner's solution file. If no solution file exists,
   tell them to write one (you cannot — the hook blocks solution writes).
2. Dispatch the `grader` agent on the folder. Execution happens when relevant; otherwise
   qualitative review (decision: "execution when relevant").
3. Write `feedback.md` in the exercise folder: score, what passed, strengths, concrete
   improvements (graduated — never paste a full solution).
4. Update `progress/skills.md`: for each concept, set the new level per the grader's
   verdict and set `last_graded` to today (ISO date), with the exercise path as evidence.
   Never downgrade a `mastered` concept on a single weak exercise without a note.
5. Append a dated entry to `progress/<track>/log.md`. Offer the next step (next module,
   another exercise, or `revise`).
