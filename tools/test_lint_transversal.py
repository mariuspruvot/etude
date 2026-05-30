from lint_transversal import is_transversal, lint_transversal_text

VALID = """---
kind: transversal
name: algorithms
display_name: Algorithms & Data Structures
languages: [python, go, typescript]
concepts:
  transversal: [algorithms:complexity, algorithms:graphs]
---
# Algorithms
### t01 — Complexity
- id: t01
- concepts: [algorithms:complexity]
- prerequisites: []
### t02 — Graphs
- id: t02
- concepts: [algorithms:graphs]
- prerequisites: [t01]
"""

LANGUAGE_CURRICULUM = """---
language: python
display_name: Python
target_version: "3.13"
concepts:
  transverse: [testing]
---
# Python
### m01 — x
- concepts: [testing]
"""


def test_valid_transversal_has_no_errors() -> None:
    assert lint_transversal_text(VALID) == []


def test_is_transversal_selects_by_kind() -> None:
    assert is_transversal(VALID) is True
    assert is_transversal(LANGUAGE_CURRICULUM) is False


def test_kind_must_be_transversal() -> None:
    text = VALID.replace("kind: transversal", "kind: curriculum")
    errors = lint_transversal_text(text)
    assert any("kind must be 'transversal'" in e for e in errors)


def test_languages_must_be_non_empty() -> None:
    text = VALID.replace("languages: [python, go, typescript]", "languages: []")
    errors = lint_transversal_text(text)
    assert any("languages must be a non-empty list" in e for e in errors)


def test_transverse_is_forbidden() -> None:
    text = VALID.replace(
        "  transversal: [algorithms:complexity, algorithms:graphs]",
        "  transverse: [x]\n  transversal: [algorithms:complexity, algorithms:graphs]",
    )
    errors = lint_transversal_text(text)
    assert any("must not declare 'transverse'" in e for e in errors)


def test_language_specific_is_forbidden() -> None:
    text = VALID.replace(
        "  transversal: [algorithms:complexity, algorithms:graphs]",
        "  language_specific: [x]\n  transversal: [algorithms:complexity, algorithms:graphs]",
    )
    errors = lint_transversal_text(text)
    assert any("must not declare 'language_specific'" in e for e in errors)


def test_concepts_transversal_must_be_non_empty() -> None:
    text = VALID.replace(
        "  transversal: [algorithms:complexity, algorithms:graphs]",
        "  transversal: []",
    )
    errors = lint_transversal_text(text)
    assert any("concepts.transversal must be a non-empty list" in e for e in errors)


def test_concept_must_be_namespaced() -> None:
    text = VALID.replace("algorithms:graphs", "graphs")
    errors = lint_transversal_text(text)
    assert any("not namespaced 'algorithms:': graphs" in e for e in errors)


def test_module_concept_must_be_declared() -> None:
    text = VALID.replace(
        "- concepts: [algorithms:complexity]", "- concepts: [algorithms:typo]"
    )
    errors = lint_transversal_text(text)
    assert any("t01 references undeclared concept: algorithms:typo" in e for e in errors)


def test_module_prereq_must_be_earlier_module() -> None:
    text = VALID.replace("- prerequisites: []", "- prerequisites: [t02]")
    errors = lint_transversal_text(text)
    assert any("t01 prerequisite not an earlier module: t02" in e for e in errors)


def test_parent_prereq_is_rejected() -> None:
    text = VALID.replace("- prerequisites: [t01]", "- prerequisites: [parent:complexity]")
    errors = lint_transversal_text(text)
    assert any("transversal tracks have no parent" in e for e in errors)
