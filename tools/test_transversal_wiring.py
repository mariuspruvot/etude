"""Guard: the transversal-track machinery is wired into the pilot, the skills, README, and CI.

Static wiring checks (behavior is covered by a manual walkthrough). Mirrors test_nudge_wiring.py.
"""

from pathlib import Path

from lint_transversal import is_transversal

ROOT = Path(__file__).resolve().parent.parent
PILOT = ROOT / "tracks" / "algorithms" / "curriculum.md"
SKILLS = ROOT / ".claude" / "skills"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"


def test_pilot_track_exists_and_is_transversal() -> None:
    assert PILOT.is_file(), "missing tracks/algorithms/curriculum.md"
    assert is_transversal(PILOT.read_text(encoding="utf-8")), "pilot must be kind: transversal"


def test_consuming_skills_are_transversal_aware() -> None:
    for skill in ("assess", "teach", "exercise", "grade"):
        text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
        assert "transversal" in text, f"{skill} must be transversal-aware"


def test_readme_documents_transversal_tracks() -> None:
    text = README.read_text(encoding="utf-8")
    assert "kind: transversal" in text, "README must document the kind: transversal schema"
    assert "lint_transversal" in text, "README must mention the transversal linter"


def test_ci_lints_transversal_tracks() -> None:
    text = CI.read_text(encoding="utf-8")
    assert "lint_transversal.py" in text, "CI must run the transversal linter"
    # The frozen core linter must not be fed transversal files (kind-split via grep -L).
    assert "grep -LE" in text, "CI must split language curricula away from the frozen linter"
