---
name: exercise
description: Use to generate a calibrated exercise for the current module and write it to progress/<track>/exercises/. Never writes the solution.
---

# Exercise

Determine the active track from what the learner just said, else from `progress/profile.md`
(`active_track`).

You are not limited to the curated modules: if the learner names a topic with no module
(a framework, a library, a niche), generate the lesson/exercise for it using Context7 for
current docs, and log it in `progress/<track>/explorations.md`.

Personal modules in `progress/<track>/extensions.md` (ids like `x01`) are first-class —
teach/generate from them exactly as from curated modules.

Curated overlays live in `tracks/<track>/overlays/*.md` — if present for the active track, read them too: their modules (`oNN`, concepts namespaced `<overlay>:`) are first-class once their `parent:` prerequisites are met.

For a transversal track (`kind: transversal`, e.g. `algorithms`): seeds come from the `tNN`
module and concepts are namespaced `<name>:`. Set `solution_file` per the learner's chosen impl
language (from the track's `languages: [...]`, e.g. `solution.py`) so the grader runs it in that
language.

1. Pick an `exercise_seed` from the current module (or generate one at the right difficulty
   given `progress/skills.md`). Calibrate: harder if the learner is senior/transferring.

Vary the exercise FORMAT to keep practice fresh — choose the one that best fits the concept:
`implement` · `debug` (give broken code in prompt.md, learner fixes it) · `refactor` ·
`read-and-explain` · `extend` (add a feature to working code in prompt.md) · `write-tests`.
Check recent entries in `progress/<track>/log.md` and avoid repeating the last format/topic.
For debug/extend/refactor, the starter (broken/partial code) goes in `prompt.md`; the
learner still writes their answer in their own `solution_file`.

2. Create `progress/<track>/exercises/NNN-<slug>/` (NNN = zero-padded 3-digit index; compute
   it by globbing existing `progress/<track>/exercises/` folders, taking the max NNN prefix + 1
   — start at `001`).
3. Write `prompt.md` ONLY, containing:
   - a small YAML frontmatter block at the very top recording the canonical solution filename
     and concepts, e.g.:
     ```
     ---
     solution_file: solution.go
     concepts: [concurrency, goroutines]
     ---
     ```
     `solution_file` is the single canonical name the learner will create and that `grade`
     will read back to locate the solution.
   - the problem statement and constraints,
   - the concept(s) it exercises (must match curriculum tags),
   - **starter code as a fenced code block** inside prompt.md (the learner copies it into
     their own solution file — you must NOT create the solution file),
   - acceptance criteria (what "done" means), and, if testable, the reference test the
     `grade` step will run (as a code block in prompt.md).
4. Tell the learner in chat the exact filename to create for their solution — it must be
   exactly the `solution_file` recorded in the frontmatter (e.g. `solution.go`) — and that
   you will not write it for them. Append a line to `progress/<track>/log.md`.

Remember: the integrity hook blocks you from writing solution files. Put everything the
learner needs in `prompt.md`.

**Language:** write prose in the learner's `progress/profile.md` `language`; keep code, identifiers, CLI, and concept tags in English.
