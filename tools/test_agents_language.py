"""Guard: both sub-agents must instruct localization of their prose.

The workflow requires a test whenever a localized agent is edited. Agents read
`progress/profile.md` for the learner's `language` and localize prose; code,
identifiers, CLI, and concept tags stay English.
"""

from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "agents"
LOCALIZED_AGENTS = ("grader.md", "interviewer.md")


def _agent_text(name: str) -> str:
    return (AGENTS_DIR / name).read_text(encoding="utf-8")


def test_localized_agents_exist() -> None:
    for name in LOCALIZED_AGENTS:
        assert (AGENTS_DIR / name).is_file(), f"missing agent: {name}"


def test_agents_read_profile_language() -> None:
    for name in LOCALIZED_AGENTS:
        text = _agent_text(name)
        assert "progress/profile.md" in text, f"{name} must read progress/profile.md"
        assert "language" in text, f"{name} must reference the language field"


def test_agents_carry_language_footer() -> None:
    needle = "**Language:**"
    for name in LOCALIZED_AGENTS:
        assert needle in _agent_text(name), f"{name} must carry the Language footer"
