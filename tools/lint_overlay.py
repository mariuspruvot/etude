# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Lint a curated overlay (tracks/<lang>/overlays/<x>.md).

A NEW schema, distinct from curriculum.md — the closed-core lint_curriculum.py is left
untouched. An overlay is a child of a language track: `kind: overlay`, `parent_track: <lang>`,
concepts namespaced `<name>:`, modules `oNN`, prerequisites referencing an earlier `oNN`
module or `parent:<concept>` where the concept is declared in `requires_parent`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Frontmatter parsing is intentionally duplicated from lint_curriculum.py, not shared:
# the core linter is a closed artifact that must stay byte-for-byte unchanged.
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
_MODULE_HEADER = re.compile(r"^###\s+(o\d+)\b", re.MULTILINE)
_LIST_FIELD = re.compile(r"^-\s*(concepts|prerequisites):\s*\[([^\]]*)\]", re.MULTILINE)
REQUIRED_TOP = ("kind", "parent_track", "name")


def _items(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


def parent_declared_concepts(parent_text: str) -> set[str]:
    """Transverse + language_specific concepts declared in a parent curriculum's frontmatter."""
    m = _FRONTMATTER.match(parent_text)
    if not m:
        return set()
    fm = yaml.safe_load(m.group(1)) or {}
    concepts = fm.get("concepts", {})
    if not isinstance(concepts, dict):
        return set()
    out: set[str] = set()
    for key in ("transverse", "language_specific"):
        val = concepts.get(key, [])
        if isinstance(val, list):
            out |= {str(x) for x in val}
    return out


def _modules(body: str) -> list[tuple[str, list[str], list[str]]]:
    """(module_id, concepts, prerequisites) for each `### oNN` block, in document order."""
    headers = list(_MODULE_HEADER.finditer(body))
    mods: list[tuple[str, list[str], list[str]]] = []
    for i, h in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        block = body[h.end() : end]
        concepts: list[str] = []
        prereqs: list[str] = []
        for field, raw in _LIST_FIELD.findall(block):
            if field == "concepts":
                concepts = _items(raw)
            else:
                prereqs = _items(raw)
        mods.append((h.group(1), concepts, prereqs))
    return mods


def lint_overlay_text(text: str, parent_concepts: set[str]) -> list[str]:
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
    if "kind" in fm and fm.get("kind") != "overlay":
        errors.append("frontmatter kind must be 'overlay'")

    name = fm.get("name")
    concepts = fm.get("concepts", {})
    if not isinstance(concepts, dict):
        errors.append("concepts must be a mapping with an 'overlay' list")
        concepts = {}
    if "transverse" in concepts:
        errors.append("overlays must not declare transverse concepts")
    overlay = concepts.get("overlay", [])
    requires_parent = concepts.get("requires_parent", [])
    if not isinstance(overlay, list) or not overlay:
        errors.append("concepts.overlay must be a non-empty list")
        overlay = []
    if not isinstance(requires_parent, list):
        errors.append("concepts.requires_parent must be a list")
        requires_parent = []

    declared_overlay = {str(c) for c in overlay}
    if isinstance(name, str) and name:
        for c in sorted(declared_overlay):
            if not c.startswith(f"{name}:"):
                errors.append(f"overlay concept not namespaced '{name}:': {c}")
    for c in requires_parent:
        if str(c) not in parent_concepts:
            errors.append(f"requires_parent concept not in parent track: {c}")
    req_parent_set = {str(c) for c in requires_parent}

    # Prerequisites must reference an EARLIER module (or a parent: concept). Enforcing
    # document order makes forward references impossible, which subsumes spec rule 8
    # (the overlay module DAG is acyclic) without a separate graph check.
    body = text[m.end() :]
    seen: set[str] = set()
    for mid, mod_concepts, prereqs in _modules(body):
        for c in mod_concepts:
            if c not in declared_overlay:
                errors.append(
                    f"module {mid} references undeclared overlay concept: {c}"
                )
        for p in prereqs:
            if p.startswith("parent:"):
                pc = p[len("parent:") :]
                if pc not in req_parent_set:
                    errors.append(
                        f"module {mid} parent prerequisite not in requires_parent: {pc}"
                    )
            elif p not in seen:
                errors.append(
                    f"module {mid} prerequisite not a parent: concept or an earlier module: {p}"
                )
        seen.add(mid)
    return errors


def main(paths: list[str]) -> int:
    failed = False
    for p in paths:
        path = Path(p)
        text = path.read_text(encoding="utf-8")
        m = _FRONTMATTER.match(text)
        fm = (yaml.safe_load(m.group(1)) or {}) if m else {}
        parent_track = fm.get("parent_track")
        parent_concepts: set[str] = set()
        if isinstance(parent_track, str):
            parent_file = path.resolve().parents[2] / parent_track / "curriculum.md"
            if not parent_file.is_file():
                print(f"FAIL {p}")
                print(f"  - parent_track '{parent_track}' has no {parent_file}")
                failed = True
                continue
            parent_concepts = parent_declared_concepts(
                parent_file.read_text(encoding="utf-8")
            )
        errors = lint_overlay_text(text, parent_concepts)
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
