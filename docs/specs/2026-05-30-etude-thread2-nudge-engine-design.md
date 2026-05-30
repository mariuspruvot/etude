# Étude — Thread 2: Nudge Engine (design)

- **Date:** 2026-05-30
- **Status:** Approved (brainstorming) — ready for plan + implementation.
- **Parent:** `docs/specs/2026-05-30-etude-completeness-roadmap-design.md` §4.
- **Goal:** Let the tutor *proactively propose* the next worthwhile thing — a branch (overlay),
  a deep-dive, a transversal track, a mini-app, or a mock interview — **at the right moments**
  and **never spammily**. This is what turns "we don't curate everything" from a limitation
  into a feature: the curated spine stays thin; the agent opens doors into on-demand content
  when it is pedagogically opportune. **Pure behavior design — zero new curriculum content.**

---

## 1. Decisions locked (in this spec)

| Topic | Decision | Note |
|-------|----------|------|
| Triggers | palier points · on-demand · interest signal · guardrail | roadmap §4.1, all four |
| Memory | **reuse `progress/<track>/log.md`** | **deviates from roadmap §4.4** (no `suggestions.md`); see §5 |
| Policy location | **hybrid:** minimal gate in `CLAUDE.md` + detailed `.claude/nudge.md` read on demand | optimised for context cost; see §3 |
| Setting | `suggestions: off \| rare \| normal` in `profile.md` (default `normal`) | roadmap §4.2 |
| Cooldown | declined target not re-proposed for **3 sessions**, judged over `log.md` | default; cheap to tune |

### 1.1 Why reuse `log.md` instead of a new `suggestions.md` (roadmap deviation)

`progress/README.md` shows the repo deliberately avoids new progress files/fields: revision
reuses `log.md`'s dated entries as `last_visited` and states *"No new field"*
(`progress/README.md:64-66`), and `teach` detects repeated niches by *judgment over the
free-text log* (`.claude/skills/teach/SKILL.md:29-33`). A structured `suggestions.md` would
introduce a convention the codebase has consciously resisted. Logging nudges as dated `log.md`
entries and judging the cooldown the same way `revise`/`teach` already judge the log is the
coherent choice.

---

## 2. Behavior contract

### 2.1 Triggers (when the tutor MAY nudge)

1. **Palier points** — when `grade` raises a concept to `proficient`/`mastered`, or when a
   capstone (mini-app / interview) is completed. Never mid-exercise, never mid-lesson.
2. **On-demand** — inside `/status`, and in the session-start greeting
   (`CLAUDE.md` "On every session start").
3. **Interest signal** — when, in the current turn, the learner shows curiosity or asks an
   off-topic "why/how" question. The nudge is a **one-line offer** (e.g. "want a deep-dive on
   the event loop?"), not auto-generation — it still counts against the guardrail.

### 2.2 Guardrail (the "not all the time" — always enforced)

- **At most 1 proactive suggestion per session.**
- **Respect the `suggestions` setting** in `profile.md`:
  - `normal` (default) — all triggers active.
  - `rare` — palier points only.
  - `off` — no proactive nudges at all; `/status` MAY still render a single quiet
    "want to branch?" line (because the learner came to look).
- **Cooldown:** a declined target is not re-proposed for **3 sessions** (judged over recent
  `log.md` entries, by the same free-text judgment `revise`/`teach` use).
- A nudge is an **offer**, never an action: the tutor proposes, the learner opts in. Declining
  costs nothing and is logged so it is not repeated.

### 2.3 What it proposes (taxonomy — exactly one per nudge)

- a **branch / overlay** (e.g. a front-end framework on the TS track) → routes to `teach`/`exercise`;
- a **deep-dive** (internals, trade-offs, cross-language contrast) → routes to `deep-dive`;
- a **transversal track** (a Thread-3 "complete-engineer" track) → routes to `assess`/`learn`;
- a **mini-app** (guided multi-file project) → routes to `mini-app`;
- a **mock interview** → routes to `interview`.

### 2.4 Relevance (how the tutor picks the one thing)

Computed from: `skills.md` state (what just got mastered, what's weak/unknown), recent
`log.md` activity (what the learner has been doing, what was already proposed/declined), the
learner's `goals` in `profile.md`, and any curiosity signal in the current turn. Prefer the
suggestion that best advances the learner's stated goal or shores up a weak spot adjacent to
what they just mastered.

---

## 3. Architecture & wiring

The policy is split for context efficiency: a tiny always-loaded **gate** and a detailed
**on-demand** doc.

### 3.1 `CLAUDE.md` — minimal gate (always loaded, ~6 lines)

Add a short section establishing that proactive suggestions exist and bounding them, e.g.:

> **Proactive suggestions (nudge).** At palier points, in `/status`, in the session-start
> greeting, or on a clear interest signal, you MAY offer **one** next step (branch, deep-dive,
> transversal track, mini-app, interview). Hard limits: **max 1 per session**; obey
> `suggestions: off|rare|normal` in `profile.md` (default `normal`); never mid-exercise; an
> offer is opt-in, never an action. **Before composing one, read `.claude/nudge.md`** for the
> taxonomy, cooldown, and log format.

This is the only always-loaded cost. Most turns never read `.claude/nudge.md`.

### 3.2 `.claude/nudge.md` — detailed policy (read on demand)

New file. Contains: the full trigger definitions (§2.1), the guardrail + cooldown judgment
rules (§2.2), the taxonomy + routing table (§2.3), the relevance heuristic (§2.4), the
**phrasing rules** (one line, opt-in, localized to the learner's `language`), and the
**`log.md` entry format**:

```
- Nudge: <kind> "<target>" → <offered|accepted|declined>
```

Read only when a trigger fires AND the guardrail/cooldown/setting would allow a suggestion.

### 3.3 Skill touch-points (one short step each, pointing at the gate/policy)

- **`grade`** — after step 4 (level update) / step 5 (log + "offer the next step"): if a
  concept reached `proficient`/`mastered` (palier), apply the nudge policy. Folds into the
  existing "Offer the next step" line (`.claude/skills/grade/SKILL.md:34`) rather than adding
  a separate prompt.
- **`status`** — extend the existing "a suggested next action" line
  (`.claude/skills/status/SKILL.md:18`) to apply the nudge policy (on-demand trigger). `status`
  stays read-only EXCEPT it may append the single nudge `log.md` entry if it makes an offer
  (explicitly carve this out, since `status` is currently "do not modify any files").
- **`interview`** / **`mini-app`** — capstone-completion palier: apply the same policy where
  the capstone is scored. Minimal addition; reuse the policy doc.

### 3.4 Setting plumbing

- **`assess`** — when creating/updating `profile.md` (step 1,
  `.claude/skills/assess/SKILL.md:10-13`), include `suggestions: normal` in the frontmatter by
  default.
- **`progress/README.md`** — add `suggestions: off | rare | normal` to the `profile.md`
  template (`progress/README.md:19-32`) with a one-line explanation.
- **Absence = `normal`:** any skill reading the setting treats a missing field as `normal`, so
  existing profiles keep working without migration.

---

## 4. Localization

Nudge prose is learner-facing prose → written in the learner's `profile.md` `language`, like
every other skill's output (the standard `**Language:**` footer rule). The taxonomy keys,
routing targets, and `log.md` entry keywords (`Nudge:`, `accepted`/`declined`) stay English.

---

## 5. Memory model (reused `log.md`)

- **Write:** when a nudge is offered, append one dated `log.md` entry (format in §3.2). When
  the learner accepts/declines in the same or a later turn, append/update the outcome.
- **Cooldown read:** before offering, scan recent `log.md` entries (by judgment, like
  `revise`'s `last_visited` and `teach`'s niche-repeat detection); if the same target was
  `declined` within the last 3 sessions, do not re-propose it.
- **Session counting:** "1 per session" and "3 sessions" are judged from dated `log.md`
  entries (a session ≈ a dated heading / contiguous run), consistent with how `revise` reads
  the log. No counter field is stored.

---

## 6. Testing & verification

Following the repo's guard-test pattern (`tools/test_agents_language.py` greps instruction
files for required markers), add `tools/test_nudge_wiring.py` asserting:

- `.claude/nudge.md` exists and documents the guardrail (`max 1`, the three setting values,
  the `log.md` entry format keyword `Nudge:`).
- `CLAUDE.md` contains the nudge gate and points to `.claude/nudge.md`.
- `grade` and `status` SKILL.md reference the nudge policy.
- `progress/README.md` `profile.md` template documents the `suggestions` field.

These are static wiring guards (cheap, deterministic, CI-friendly via Thread 1). Behavioral
quality (does it nudge *well*?) is validated by a **manual walkthrough** (a HUMAN step, as
prior threads did): drive a palier point, a `/status`, an interest signal, and an `off`
profile, and confirm the offers appear/suppress correctly. No attempt to unit-test model
judgment.

---

## 7. Definition of done

- `.claude/nudge.md` written; `CLAUDE.md` gate added.
- `grade`, `status` (+ `interview`/`mini-app`) reference the policy; `status`'s read-only
  carve-out for the single log entry is explicit.
- `assess` writes `suggestions: normal`; `progress/README.md` template updated.
- `tools/test_nudge_wiring.py` passes; all existing linters + tests still green in CI.
- `lint_curriculum.py` untouched (frozen).
- Manual walkthrough done (palier / status / interest / `off`).
- `revise-claude-md` step run.
- Lands via isolated worktree + PR to `main`.

---

## 8. Assumptions

- **Reusing `log.md` is sufficient for the cooldown.** — Based on `revise`/`teach` already
  judging the free-text log (`progress/README.md:64`, `.claude/skills/teach/SKILL.md:29`). If
  judgment proves too unreliable in the walkthrough, a structured `suggestions.md` is the
  fallback (the roadmap's original proposal).
- **The hybrid policy split is the most context-efficient option.** — Always-loaded cost is a
  ~6-line gate; the ~detailed doc loads only when a suggestion is actually composed (≤1/session,
  often 0). Chosen over a fully-in-`CLAUDE.md` policy to keep every session lean.
- **`status` may make one file write (the nudge log entry).** — Deviates from its current
  "read-only" rule (`.claude/skills/status/SKILL.md:19`); carved out explicitly. Alternative:
  `status` offers but does not log until the learner acts — rejected because then declines
  in `status` would not feed the cooldown.
- **Missing `suggestions` field = `normal`.** — Chosen so existing local profiles need no
  migration.
- **Capstone-completion nudges belong in `interview`/`mini-app`.** — Inferred from where
  capstones are scored; the implementation confirms these skills are the right insertion point.
- **Session boundary is judged from dated `log.md` headings.** — Same basis `revise` uses; no
  explicit session id is stored.

---

## 9. Out of scope

- Any change to `lint_curriculum.py` (frozen) or new curriculum content.
- A structured `suggestions.md` (explicitly rejected here; fallback only).
- The Thread-3 transversal tracks the nudge can point to (designed separately; the nudge
  simply references them by name once they exist).
- Any enforcement hook — the nudge advises, it never blocks (hooks remain enforcement-only).
