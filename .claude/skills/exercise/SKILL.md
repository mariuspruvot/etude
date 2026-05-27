---
name: exercise
description: Use to generate a calibrated exercise for the current module and write it to progress/<track>/exercises/. Never writes the solution.
---

# Exercise

1. Pick an `exercise_seed` from the current module (or generate one at the right difficulty
   given `progress/skills.md`). Calibrate: harder if the learner is senior/transferring.
2. Create `progress/<track>/exercises/NNN-<slug>/` (NNN = next zero-padded index).
3. Write `prompt.md` ONLY, containing:
   - the problem statement and constraints,
   - the concept(s) it exercises (must match curriculum tags),
   - **starter code as a fenced code block** inside prompt.md (the learner copies it into
     their own solution file — you must NOT create the solution file),
   - acceptance criteria (what "done" means), and, if testable, the reference test the
     `grade` step will run (as a code block in prompt.md).
4. Tell the learner the exact filename to create for their solution (e.g. `solution.go`)
   and that you will not write it for them. Append a line to `progress/<track>/log.md`.

Remember: the integrity hook blocks you from writing solution files. Put everything the
learner needs in `prompt.md`.
