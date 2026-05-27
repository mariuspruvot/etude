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
- concepts: [error-handling]
### m02 — Concurrency
- concepts: [concurrency, goroutines]
"""


def test_valid_curriculum_has_no_errors():
    assert lint_text(VALID) == []


def test_missing_frontmatter_key_reported():
    text = VALID.replace("target_version: \"1.23\"\n", "")
    errors = lint_text(text)
    assert any("target_version" in e for e in errors)


def test_undeclared_concept_reported():
    text = VALID.replace("- concepts: [concurrency, goroutines]",
                         "- concepts: [concurency]")  # typo
    errors = lint_text(text)
    assert any("concurency" in e for e in errors)


def test_no_frontmatter_reported():
    errors = lint_text("# Go\nno frontmatter here")
    assert any("frontmatter" in e.lower() for e in errors)
