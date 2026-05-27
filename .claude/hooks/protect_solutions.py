"""PreToolUse hook: block Claude from writing the learner's solution files.

Runtime dependency-free (python3 stdlib only). Reads a PreToolUse JSON payload on
stdin; exits 2 (with a reason on stderr) to block a disallowed Write/Edit.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}
ALLOWED_IN_EXERCISES = {"prompt.md", "feedback.md"}


def is_protected(tool_name: str, file_path: str) -> bool:
    """True if Claude must not write file_path (a learner solution file)."""
    if tool_name not in WRITE_TOOLS:
        return False
    if not file_path:
        return False
    parts = Path(file_path).parts
    if "progress" in parts and "exercises" in parts:
        return Path(file_path).name not in ALLOWED_IN_EXERCISES
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_name = payload.get("tool_name", "")
    file_path = payload.get("tool_input", {}).get("file_path", "")
    if is_protected(tool_name, file_path):
        sys.stderr.write(
            "Étude integrity guard: solution files in progress/.../exercises/ must be "
            "written by the learner, not Claude. Give a graduated hint, or write the "
            "exercise into prompt.md / your evaluation into feedback.md instead.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
