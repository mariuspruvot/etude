from lint_curriculum import lint_text

VALID = """---
language: go
display_name: Go
target_version: "1.23"
concepts:
  transverse: [concurrency, error-handling]
  language_specific: [go-syntax, goroutines]
---
# Go
### m01 — Tooling
- concepts: [error-handling, go-syntax]
### m02 — Concurrency
- concepts: [concurrency, goroutines]
"""

FRONTMATTER_ONLY = """---
language: go
display_name: Go
target_version: "1.23"
concepts:
  transverse: [concurrency, error-handling]
  language_specific: [go-syntax, goroutines]
---"""

UNGROUNDED = """---
language: go
display_name: Go
target_version: "1.23"
concepts:
  transverse: [concurrency, error-handling]
  language_specific: [go-syntax, goroutines]
---
# Go
### m01 — Tooling
- concepts: [error-handling]
### m02 — Concurrency
- concepts: [concurrency]
## Capstones
- interview: "x" — concepts: [goroutines, go-syntax]
"""


def test_valid_curriculum_has_no_errors() -> None:
    assert lint_text(VALID) == []


def test_missing_frontmatter_key_reported() -> None:
    text = VALID.replace('target_version: "1.23"\n', "")
    errors = lint_text(text)
    assert any("target_version" in e for e in errors)


def test_undeclared_concept_reported() -> None:
    text = VALID.replace(
        "- concepts: [concurrency, goroutines]", "- concepts: [concurency]"
    )  # typo
    errors = lint_text(text)
    assert any("concurency" in e for e in errors)


def test_no_frontmatter_reported() -> None:
    errors = lint_text("# Go\nno frontmatter here")
    assert any("frontmatter" in e.lower() for e in errors)


def test_frontmatter_without_trailing_newline_parses() -> None:
    # Frontmatter must be recognized even with no trailing newline / no body;
    # grounding errors are expected here (no modules), but never a parse failure.
    errors = lint_text(FRONTMATTER_ONLY)
    assert not any("frontmatter" in e.lower() for e in errors)


def test_ungrounded_declared_concept_reported() -> None:
    errors = lint_text(UNGROUNDED)
    assert any(
        "declared concept never grounded in a module: goroutines" in e for e in errors
    )
    assert any(
        "declared concept never grounded in a module: go-syntax" in e for e in errors
    )
