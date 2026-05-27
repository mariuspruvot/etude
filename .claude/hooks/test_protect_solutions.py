from protect_solutions import is_protected


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
