# Étude — Feasibility Spike: Claude Code repo-local loading

- **Date**: 2026-05-27
- **Goal**: Validate the riskiest assumption in the design spec (§12): *a cloned repo can
  ship skills + hooks + agents + commands + CLAUDE.md and have them work at session start.*
- **Method**: (1) authoritative review of official Claude Code docs (code.claude.com),
  (2) empirical inspection of the local Claude Code config (`~/.claude.json`).

## Verdict

**Clone-and-go is VIABLE.** Every engine component (commands, agents, skills, CLAUDE.md,
project settings, hooks) loads from a cloned repo. The only friction is a **single,
one-time per-directory trust dialog** on first launch in the cloned folder — which gates
everything (including hooks) at once. This is acceptable UX, not a blocker.

## Findings

| Component | Location (committed) | Auto-discovered after clone? | Gate |
|-----------|----------------------|------------------------------|------|
| Slash commands | `.claude/commands/*.md` | Yes | none beyond dir trust |
| Subagents | `.claude/agents/*.md` | Yes (walks up from cwd) | none beyond dir trust |
| Skills | `.claude/skills/<name>/SKILL.md` | Yes (project skills, no install) | none beyond dir trust |
| Root CLAUDE.md | `CLAUDE.md` | Yes, at session start | none beyond dir trust |
| Nested CLAUDE.md | `tracks/<t>/CLAUDE.md` | Yes, **on-demand** when files in that subtree are read | none |
| Project settings | `.claude/settings.json` | Yes, applied automatically | none beyond dir trust |
| **Hooks** | `.claude/settings.json` | Yes, execute at lifecycle events | **per-directory trust dialog** |

### The trust model (the crux)

- Claude Code tracks trust **per project directory** via `hasTrustDialogAccepted` in
  `~/.claude.json`. **Empirically confirmed on this machine**: the key exists per project,
  with at least one entry set to `false` (i.e. an un-trusted directory).
- On first launch in a freshly cloned repo, the user gets a **"Do you trust the files in
  this folder?"** prompt. Accepting it trusts the directory and everything it ships,
  including hooks. There is **no separate per-component approval** — one dialog covers all.
- Consequence: hooks are **not** a hard blocker. They run after the single trust
  acceptance. The protect-solutions PreToolUse hook works as designed once trusted.
- Permission prompts for individual dangerous operations (Bash, edits, WebFetch) still
  follow the normal allow/ask/deny rules regardless of trust.

### Nested CLAUDE.md (relevant to per-track tutor notes)

- Root `CLAUDE.md` loads at session start.
- Nested `tracks/<track>/CLAUDE.md` loads **on-demand**, when Claude reads files in that
  subtree — not at launch. Design implication: the **root** `CLAUDE.md` must be the
  router/orchestrator (always loaded); per-track notes can live nested and will load once
  the session touches that track's files.

### CLAUDE.md external includes (newly discovered nuance)

- The per-project config also has `hasClaudeMdExternalIncludesApproved` /
  `hasClaudeMdExternalIncludesWarningShown`. If `CLAUDE.md` uses `@path` includes of
  external files, that triggers a **separate one-time approval**.
- **Design decision**: avoid `@include` in the router `CLAUDE.md`; have Claude **read**
  `tracks/<t>/curriculum.md` and `progress/*` via tools instead, to avoid an extra prompt.

## Settings precedence (highest → lowest)

1. Managed (enterprise) · 2. CLI args · 3. `.claude/settings.local.json` (gitignored) ·
4. `.claude/settings.json` (committed) · 5. `~/.claude/settings.json` (user).

So shipped project settings apply after clone but a user can still override locally.

## Implications for Étude

1. **Architecture holds.** No redesign needed. Commands/agents/skills/CLAUDE.md ship in
   the repo and work; the protect-solutions hook works after the one-time trust.
2. **README must set expectations.** Document the single trust prompt on first open ("yes,
   you'll be asked to trust this folder — that's expected, it enables the tutor's
   guardrails"). This is the entire "setup step".
3. **Router lives in root `CLAUDE.md`.** Per-track `CLAUDE.md` is supplementary (loads
   on-demand).
4. **No `@include` in CLAUDE.md.** Read curriculum/progress files via tools.
5. **Honesty for HN**: "clone, open Claude Code, accept the folder-trust prompt once,
   start learning" — not literally zero-click, but one expected click.

## Residual risks (lower priority)

- Exact YAML frontmatter shapes for project skills/agents/commands should be validated by
  building one real example of each during implementation (cheap, fixture-level).
- Behavior under headless `-p` mode disables trust verification — not relevant to the
  interactive learner flow, but note it if any CI/automation is added later.

## Sources

Official docs reviewed: `claude-directory`, `settings`, `hooks`, `security`, `memory`,
`sub-agents`, `skills` (code.claude.com/docs/en/*). Local evidence: `~/.claude.json`
project entries (`hasTrustDialogAccepted`, `hasClaudeMdExternalIncludesApproved`).
