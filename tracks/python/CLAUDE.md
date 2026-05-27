# Python track — tutor notes

Target Python 3.13+. Enforce the modern stack: uv (never bare `python`/`pip`), ruff,
mypy --strict, pytest. Pull current library usage via Context7.

- Emphasize: full type annotations, dataclasses over dicts, comprehensions, context
  managers, specific exceptions (no bare except), pathlib over os.path.
- Forbid in graded solutions: `Any`, `# type: ignore`, `unittest.mock` (use test doubles),
  imports inside functions.
- Solution files are learner-written; never write `.py` solution files (the hook blocks it).
