# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Lint a transversal track (tracks/<name>/curriculum.md with `kind: transversal`).

A NEW schema, distinct from a language curriculum.md — the closed-core lint_curriculum.py is
left untouched (same precedent as lint_overlay.py). A transversal track is a top-level,
language-agnostic but gradable subject (algorithms, databases, …): `kind: transversal`,
`languages: [...]` (impl languages the learner may pick), concepts namespaced `<name>:`,
modules `tNN`, prerequisites referencing an EARLIER `tNN` module (document order ⇒ acyclic).

Self-selecting: files whose frontmatter `kind` is not `transversal` are skipped, so this can be
pointed at `tracks/*/curriculum.md` without choking on language tracks.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Frontmatter parsing is intentionally duplicated from lint_curriculum.py, not shared:
# the core linter is a closed artifact that must stay byte-for-byte unchanged.
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
_MODULE_HEADER = re.compile(r"^###\s+(t\d+)\b", re.MULTILINE)
_LIST_FIELD = re.compile(r"^-\s*(concepts|prerequisites):\s*\[([^\]]*)\]", re.MULTILINE)
REQUIRED_TOP = ("kind", "name", "display_name", "languages")


def _items(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


def _modules(body: str) -> list[tuple[str, list[str], list[str]]]:
    """(module_id, concepts, prerequisites) for each `### tNN` block, in document order."""
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


def is_transversal(text: str) -> bool:
    """True if the file's frontmatter declares `kind: transversal`."""
    m = _FRONTMATTER.match(text)
    if not m:
        return False
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return False
    return isinstance(fm, dict) and fm.get("kind") == "transversal"


def lint_transversal_text(text: str) -> list[str]:
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
    if "kind" in fm and fm.get("kind") != "transversal":
        errors.append("frontmatter kind must be 'transversal'")

    languages = fm.get("languages", [])
    if not isinstance(languages, list) or not languages:
        errors.append("languages must be a non-empty list of impl languages")
    elif not all(isinstance(x, str) and x.strip() for x in languages):
        errors.append("languages entries must be non-empty strings")

    name = fm.get("name")
    concepts = fm.get("concepts", {})
    if not isinstance(concepts, dict):
        errors.append("concepts must be a mapping with a 'transversal' list")
        concepts = {}
    for forbidden in ("transverse", "language_specific"):
        if forbidden in concepts:
            errors.append(
                f"transversal tracks must not declare '{forbidden}' concepts"
            )
    transversal = concepts.get("transversal", [])
    if not isinstance(transversal, list) or not transversal:
        errors.append("concepts.transversal must be a non-empty list")
        transversal = []

    declared = {str(c) for c in transversal}
    if isinstance(name, str) and name:
        for c in sorted(declared):
            if not c.startswith(f"{name}:"):
                errors.append(f"transversal concept not namespaced '{name}:': {c}")

    # Prerequisites must reference an EARLIER module. Enforcing document order makes forward
    # references impossible, which keeps the module DAG acyclic without a separate graph check.
    body = text[m.end() :]
    seen: set[str] = set()
    for mid, mod_concepts, prereqs in _modules(body):
        for c in mod_concepts:
            if c not in declared:
                errors.append(f"module {mid} references undeclared concept: {c}")
        for p in prereqs:
            if p.startswith("parent:"):
                errors.append(
                    f"module {mid} uses parent: prerequisite — transversal tracks have no parent: {p}"
                )
            elif p not in seen:
                errors.append(
                    f"module {mid} prerequisite not an earlier module: {p}"
                )
        seen.add(mid)
    return errors


def main(paths: list[str]) -> int:
    failed = False
    for p in paths:
        text = Path(p).read_text(encoding="utf-8")
        if not is_transversal(text):
            print(f"skip {p}")
            continue
        errors = lint_transversal_text(text)
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
