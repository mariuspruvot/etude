from lint_overlay import lint_overlay_text, parent_declared_concepts

PARENT = """---
language: python
display_name: Python
target_version: "3.13"
concepts:
  transverse: [async-await, type-system, testing]
  language_specific: [python-syntax]
---
# Python
### m01 — x
- concepts: [async-await, type-system, testing, python-syntax]
"""

PARENT_CONCEPTS = {"async-await", "type-system", "testing", "python-syntax"}

VALID = """---
kind: overlay
parent_track: python
name: fastapi
display_name: FastAPI
concepts:
  overlay: [fastapi:routing, fastapi:di]
  requires_parent: [async-await, type-system]
---
# FastAPI
### o01 — Routing
- id: o01
- concepts: [fastapi:routing]
- prerequisites: [parent:async-await]
### o02 — DI
- id: o02
- concepts: [fastapi:di]
- prerequisites: [o01]
"""


def test_parent_declared_concepts_extracts_both_groups() -> None:
    assert parent_declared_concepts(PARENT) == PARENT_CONCEPTS


def test_valid_overlay_has_no_errors() -> None:
    assert lint_overlay_text(VALID, PARENT_CONCEPTS) == []


def test_kind_must_be_overlay() -> None:
    text = VALID.replace("kind: overlay", "kind: curriculum")
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any("kind must be 'overlay'" in e for e in errors)


def test_overlay_concept_must_be_namespaced() -> None:
    text = VALID.replace("fastapi:di", "di")
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any("not namespaced 'fastapi:': di" in e for e in errors)


def test_transverse_is_forbidden() -> None:
    text = VALID.replace(
        "  overlay: [fastapi:routing, fastapi:di]",
        "  transverse: [x]\n  overlay: [fastapi:routing, fastapi:di]",
    )
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any("must not declare transverse" in e for e in errors)


def test_requires_parent_must_exist_in_parent() -> None:
    text = VALID.replace(
        "requires_parent: [async-await, type-system]",
        "requires_parent: [async-await, nonexistent]",
    )
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any("requires_parent concept not in parent track: nonexistent" in e for e in errors)


def test_module_concept_must_be_declared() -> None:
    text = VALID.replace("- concepts: [fastapi:routing]", "- concepts: [fastapi:typo]")
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any("o01 references undeclared overlay concept: fastapi:typo" in e for e in errors)


def test_module_prereq_must_be_earlier_module_or_parent() -> None:
    text = VALID.replace("- prerequisites: [parent:async-await]", "- prerequisites: [o02]")
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any(
        "o01 prerequisite not a parent: concept or an earlier module: o02" in e
        for e in errors
    )


def test_parent_prereq_must_be_in_requires_parent() -> None:
    text = VALID.replace("- prerequisites: [parent:async-await]", "- prerequisites: [parent:testing]")
    errors = lint_overlay_text(text, PARENT_CONCEPTS)
    assert any("o01 parent prerequisite not in requires_parent: testing" in e for e in errors)
