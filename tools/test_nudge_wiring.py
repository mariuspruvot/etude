"""Guard: the nudge engine is wired into the policy doc, the router, and the skills.

Static wiring checks (no model behavior tested — that is covered by a manual walkthrough).
Mirrors the style of test_agents_language.py: grep instruction files for required markers.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUDGE = ROOT / ".claude" / "nudge.md"
CLAUDE_MD = ROOT / "CLAUDE.md"
SKILLS = ROOT / ".claude" / "skills"
PROGRESS_README = ROOT / "progress" / "README.md"


def test_nudge_policy_documents_guardrail() -> None:
    text = NUDGE.read_text(encoding="utf-8")
    assert NUDGE.is_file(), "missing .claude/nudge.md"
    assert "per session" in text, "nudge.md must state the per-session cap"
    assert "Nudge:" in text, "nudge.md must define the log.md entry keyword"
    for mode in ("off", "rare", "normal"):
        assert mode in text, f"nudge.md must document the '{mode}' setting"


def test_router_gate_points_to_policy() -> None:
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert "nudge" in text.lower(), "CLAUDE.md must carry the nudge gate"
    assert ".claude/nudge.md" in text, "CLAUDE.md gate must point to .claude/nudge.md"


def test_consuming_skills_reference_policy() -> None:
    for skill in ("grade", "status"):
        text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
        assert ".claude/nudge.md" in text, f"{skill} must reference the nudge policy"


def test_profile_template_documents_suggestions_field() -> None:
    text = PROGRESS_README.read_text(encoding="utf-8")
    assert "suggestions" in text, "progress/README.md profile template must document 'suggestions'"
