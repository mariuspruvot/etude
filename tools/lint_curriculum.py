# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Lint a track's curriculum.md: frontmatter shape + concept-tag integrity."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
_CONCEPTS_LINE = re.compile(r"(?<!\w)concepts:\s*\[([^\]]*)\]")
_CAPSTONES = re.compile(r"^##\s+Capstones\b", re.IGNORECASE | re.MULTILINE)
REQUIRED_TOP = ("language", "display_name", "target_version")


def _concept_tags(text: str) -> list[str]:
    """All concept ids referenced by `concepts: [...]` lists in text."""
    tags: list[str] = []
    for raw in _CONCEPTS_LINE.findall(text):
        tags.extend(t.strip() for t in raw.split(",") if t.strip())
    return tags


def lint_text(text: str) -> list[str]:
    errors: list[str] = []
    m = _FRONTMATTER.match(text)
    if not m:
        return ["missing YAML frontmatter (--- ... --- at top of file)"]
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"invalid YAML frontmatter: {exc}"]

    for key in REQUIRED_TOP:
        if key not in fm:
            errors.append(f"frontmatter missing required key: {key}")

    concepts = fm.get("concepts", {})
    transverse = concepts.get("transverse", []) if isinstance(concepts, dict) else []
    specific = (
        concepts.get("language_specific", []) if isinstance(concepts, dict) else []
    )
    if not isinstance(transverse, list) or not transverse:
        errors.append("concepts.transverse must be a non-empty list")
    if not isinstance(specific, list):
        errors.append("concepts.language_specific must be a list")
    declared = set(transverse or []) | set(specific or [])

    body = text[m.end() :]
    for tag in _concept_tags(body):
        if tag not in declared:
            msg = f"module references undeclared concept: {tag}"
            if msg not in errors:
                errors.append(msg)

    cap = _CAPSTONES.search(body)
    grounding_region = body[: cap.start()] if cap else body
    grounded = set(_concept_tags(grounding_region))
    for concept in (*(transverse or []), *(specific or [])):
        if concept not in grounded:
            msg = f"declared concept never grounded in a module: {concept}"
            if msg not in errors:
                errors.append(msg)
    return errors


def main(paths: list[str]) -> int:
    failed = False
    for p in paths:
        errors = lint_text(Path(p).read_text(encoding="utf-8"))
        if errors:
            failed = True
            print(f"FAIL {p}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"ok   {p}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
