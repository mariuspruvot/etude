# Nudge policy — proactive suggestions

The tutor may proactively **offer** the learner a worthwhile next step. Read this file only
when a trigger has fired and you are about to compose a suggestion (the `CLAUDE.md` gate tells
you when). A nudge is always an **offer the learner opts into**, never an action you take.

Design intent: the curated curriculum is a thin spine. This is how the tutor opens doors into
the on-demand space (frameworks, deep-dives, transversal subjects) at the right moment —
turning "we don't curate everything" into a feature, without spamming.

## Triggers (when you MAY nudge)
- **Palier point** — a concept just reached `proficient`/`mastered` in `skills.md`, or a
  capstone (mini-app / interview) was just completed. Never mid-exercise or mid-lesson.
- **On-demand** — inside `/status`, or in the session-start greeting.
- **Interest signal** — the learner showed curiosity or asked an off-topic "why/how" question
  this turn. Offer a one-line deep-dive; do not auto-generate a lesson.

## Guardrail (always enforced)
- **At most ONE proactive suggestion per session.**
- **Obey the `suggestions` setting** in `progress/profile.md` (missing field ⇒ `normal`):
  - `normal` — all triggers active.
  - `rare` — palier points only.
  - `off` — no proactive nudges; `/status` MAY still show a single quiet "want to branch?" line.
- **Cooldown** — do not re-propose a target the learner `declined` within the last **3
  sessions**. Judge this from recent `progress/<track>/log.md` entries (same free-text
  judgment `revise` and `teach` use; a session ≈ a dated `##` heading).
- Never nudge mid-exercise. Declining costs the learner nothing.

## What to propose (pick exactly ONE)
| kind | when it fits | routes to |
|------|--------------|-----------|
| branch / overlay | a relevant framework/library on the current track | `teach` / `exercise` |
| deep-dive | internals, trade-offs, cross-language contrast | `deep-dive` |
| transversal track | a "complete-engineer" subject (algorithms, databases, system design, …) | `assess` / `learn` |
| mini-app | learner has enough mastered concepts for a guided project | `mini-app` |
| mock interview | learner is consolidating a track and wants pressure-testing | `interview` |

## How to pick (relevance)
Use `skills.md` (what just got mastered, what is weak/unknown), recent `log.md` activity
(and what was already offered/declined), and `profile.md` `goals`. Prefer the one step that
best advances the stated goal or shores up a weak spot adjacent to what was just mastered.

## How to phrase
- **One line**, opt-in, concrete: name the target and the payoff, end with a yes/no offer.
  e.g. "You've mastered TS generics — want to branch into a typed React overlay next? (y/n)"
- Written in the learner's `profile.md` `language` (prose only; keep target names, concept
  tags, and CLI in English).
- If declined, acknowledge briefly and drop it. Do not re-pitch.

## Logging (reuses `log.md`, no new file)
Append one dated entry to `progress/<track>/log.md` when you offer, and record the outcome:

```
- Nudge: <kind> "<target>" → offered
- Nudge: <kind> "<target>" → accepted   # or → declined
```

This is what the cooldown reads. No counter field, no separate file.
