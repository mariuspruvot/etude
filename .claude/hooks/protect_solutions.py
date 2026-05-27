"""PreToolUse hook: block Claude from writing the learner's solution files.

Runtime dependency-free (python3 stdlib only). Reads a PreToolUse JSON payload on
stdin. Contract:
  - exit 2 (with a reason on stderr) = BLOCK a disallowed Write/Edit/MultiEdit/NotebookEdit.
  - exit 0 = ALLOW. This includes any malformed input (unparseable JSON, non-dict
    payload, missing/wrong-typed fields): the hook fails OPEN and never crashes, so a
    malformed payload can never accidentally exit 1 (a non-blocking error that would let
    the write proceed unannounced). Claude Code always sends well-formed payloads.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
ALLOWED_IN_EXERCISES = {"prompt.md", "feedback.md"}


def is_protected(tool_name: str, file_path: str) -> bool:
    """True if Claude must not write file_path (a learner solution file)."""
    if tool_name not in WRITE_TOOLS:
        return False
    if not file_path:
        return False
    p = Path(file_path)
    if "progress" in p.parts and "exercises" in p.parts:
        return p.name not in ALLOWED_IN_EXERCISES
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict):
        return 0
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    raw_path = tool_input.get("file_path") or tool_input.get("notebook_path", "")
    file_path = raw_path if isinstance(raw_path, str) else ""
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
