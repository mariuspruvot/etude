import json
import subprocess
import sys
from pathlib import Path

from protect_solutions import is_protected

HOOK = Path(__file__).parent / "protect_solutions.py"


def _run(payload: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )


def test_blocks_solution_file_in_exercise_dir():
    assert is_protected("Write", "/x/progress/go/exercises/001-slices/solution.go") is True


def test_blocks_any_extension_solution():
    assert is_protected("Edit", "/x/progress/python/exercises/004-async/main.py") is True


def test_allows_prompt_md():
    assert is_protected("Write", "/x/progress/go/exercises/001-slices/prompt.md") is False


def test_allows_feedback_md():
    assert is_protected("Write", "/x/progress/go/exercises/001-slices/feedback.md") is False


def test_allows_tracking_files_outside_exercises():
    assert is_protected("Write", "/x/progress/skills.md") is False
    assert is_protected("Write", "/x/progress/go/log.md") is False


def test_ignores_non_write_tools():
    assert is_protected("Read", "/x/progress/go/exercises/001/solution.go") is False
    assert is_protected("Bash", "/x/progress/go/exercises/001/solution.go") is False


def test_ignores_files_outside_progress():
    assert is_protected("Write", "/x/tracks/go/curriculum.md") is False


def test_cli_blocks_with_exit_2():
    r = _run({"tool_name": "Write",
              "tool_input": {"file_path": "/x/progress/go/exercises/001/solution.go"}})
    assert r.returncode == 2
    assert "integrity guard" in r.stderr


def test_cli_allows_feedback():
    r = _run({"tool_name": "Write",
              "tool_input": {"file_path": "/x/progress/go/exercises/001/feedback.md"}})
    assert r.returncode == 0
