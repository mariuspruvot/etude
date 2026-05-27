import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from protect_solutions import is_protected

HOOK = Path(__file__).parent / "protect_solutions.py"


def _run_raw(stdin: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


def _run(payload: Any) -> subprocess.CompletedProcess[str]:
    return _run_raw(json.dumps(payload))


def test_blocks_solution_file_in_exercise_dir() -> None:
    assert (
        is_protected("Write", "/x/progress/go/exercises/001-slices/solution.go") is True
    )


def test_blocks_any_extension_solution() -> None:
    assert (
        is_protected("Edit", "/x/progress/python/exercises/004-async/main.py") is True
    )


def test_blocks_notebook_solution() -> None:
    assert (
        is_protected("NotebookEdit", "/x/progress/go/exercises/001/solution.ipynb")
        is True
    )


def test_allows_prompt_md() -> None:
    assert (
        is_protected("Write", "/x/progress/go/exercises/001-slices/prompt.md") is False
    )


def test_allows_feedback_md() -> None:
    assert (
        is_protected("Write", "/x/progress/go/exercises/001-slices/feedback.md")
        is False
    )


def test_allows_tracking_files_outside_exercises() -> None:
    assert is_protected("Write", "/x/progress/skills.md") is False
    assert is_protected("Write", "/x/progress/go/log.md") is False


def test_ignores_non_write_tools() -> None:
    assert is_protected("Read", "/x/progress/go/exercises/001/solution.go") is False
    assert is_protected("Bash", "/x/progress/go/exercises/001/solution.go") is False


def test_ignores_files_outside_progress() -> None:
    assert is_protected("Write", "/x/tracks/go/curriculum.md") is False


def test_cli_blocks_with_exit_2() -> None:
    r = _run(
        {
            "tool_name": "Write",
            "tool_input": {"file_path": "/x/progress/go/exercises/001/solution.go"},
        }
    )
    assert r.returncode == 2
    assert "integrity guard" in r.stderr


def test_cli_blocks_notebook_with_exit_2() -> None:
    r = _run(
        {
            "tool_name": "NotebookEdit",
            "tool_input": {
                "notebook_path": "/x/progress/go/exercises/001/solution.ipynb"
            },
        }
    )
    assert r.returncode == 2
    assert "integrity guard" in r.stderr


def test_cli_allows_feedback() -> None:
    r = _run(
        {
            "tool_name": "Write",
            "tool_input": {"file_path": "/x/progress/go/exercises/001/feedback.md"},
        }
    )
    assert r.returncode == 0


def test_cli_allows_empty_stdin() -> None:
    assert _run_raw("").returncode == 0


def test_cli_allows_non_json_text() -> None:
    assert _run_raw("not json at all").returncode == 0


def test_cli_allows_top_level_null() -> None:
    assert _run({"x": 1}).returncode == 0  # warm-up sanity (well-formed dict, no path)
    assert _run(None).returncode == 0


def test_cli_allows_top_level_list() -> None:
    assert _run([1, 2, 3]).returncode == 0


def test_cli_allows_null_tool_input() -> None:
    assert _run({"tool_name": "Write", "tool_input": None}).returncode == 0


def test_cli_allows_non_string_file_path() -> None:
    r = _run({"tool_name": "Write", "tool_input": {"file_path": 123}})
    assert r.returncode == 0
