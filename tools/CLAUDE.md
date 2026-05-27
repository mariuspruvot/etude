# tools/ — dev-tooling notes

The lint scripts (`lint_curriculum.py`, `lint_overlay.py`) ship with PEP 723
inline script metadata (`# /// script` … `dependencies = ["pyyaml"]`). They
MUST be invoked via:

- `uv run --script tools/lint_overlay.py <path>` — NOT `uv run python tools/...`
  (the latter bypasses metadata and fails with `ModuleNotFoundError: yaml`).
- Tests: `uv run --with pyyaml --with pytest pytest tools/test_lint_overlay.py`
  (the tests import the lint module directly, so pyyaml must be in the env).

`lint_curriculum.py` is **closed** and must stay byte-for-byte unchanged
(verified in PR reviews; the overlay linter intentionally duplicates the
frontmatter parser instead of importing it).
