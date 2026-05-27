---
language: python
display_name: Python
target_version: "3.13"
freshness_source: context7
maintainers: [community]

concepts:
  transverse:
    - error-handling
    - concurrency
    - type-system
    - testing
    - interfaces-polymorphism
    - dependency-management
    - io-streams
    - memory-model
  language_specific:
    - python-syntax
    - comprehensions
    - decorators
    - context-managers
    - dataclasses
    - asyncio
    - typing-generics
---

# Python — Curriculum

> Audience: developers comfortable in at least one language. `assess` establishes the
> transverse level first, then enters at the right module.

## Modules

### m01 — Tooling & environments
- id: m01
- concepts: [dependency-management]
- prerequisites: []
- ecosystem:
    tools: [uv, ruff]
    files: [pyproject.toml]
- resources:
    - https://docs.astral.sh/uv/
    - https://docs.astral.sh/uv/concepts/projects/
- mastery:
    - creates a project with uv, adds/removes a dependency, runs a script via `uv run`
    - configures and runs ruff clean via pyproject.toml
- exercise_seeds:
    - "scaffold a uv project exposing one CLI entry point that runs ruff clean"

### m02 — Syntax & primitives
- id: m02
- concepts: [python-syntax, comprehensions]
- prerequisites: [m01]
- ecosystem:
    libs: [builtins, collections]
- resources:
    - https://docs.python.org/3/tutorial/introduction.html
    - https://docs.python.org/3/tutorial/datastructures.html
- mastery:
    - uses list/dict/set comprehensions idiomatically; understands truthiness, slicing, unpacking
- exercise_seeds:
    - "transform nested data with comprehensions (group, filter, invert a mapping)"
- transfer_note: |
    Syntax does NOT transfer. A senior dev new to Python still learns this module — fast,
    by contrast with their known language. assess skips it only if python-syntax is proficient.

### m03 — Types & the type system
- id: m03
- concepts: [type-system, typing-generics, dataclasses]
- prerequisites: [m02]
- ecosystem:
    tools: [mypy]
    libs: [typing, dataclasses]
- resources:
    - https://docs.python.org/3/library/typing.html
    - https://mypy.readthedocs.io/
- mastery:
    - annotates functions fully; models data with dataclasses; uses generics; passes mypy --strict
- exercise_seeds:
    - "model a domain with dataclasses + a generic container, fully typed, mypy --strict clean"

### m04 — Errors & exceptions
- id: m04
- concepts: [error-handling]
- prerequisites: [m02]
- ecosystem:
    libs: [builtins]
- resources:
    - https://docs.python.org/3/tutorial/errors.html
- mastery:
    - raises/handles specific exceptions, uses context in messages, avoids bare except
- exercise_seeds:
    - "build a parser that raises a custom exception hierarchy and is unit-tested"

### m05 — Idioms: decorators & context managers
- id: m05
- concepts: [decorators, context-managers, interfaces-polymorphism]
- prerequisites: [m03, m04]
- ecosystem:
    libs: [contextlib, functools]
- resources:
    - https://docs.python.org/3/reference/datamodel.html
    - https://docs.python.org/3/library/contextlib.html
- mastery:
    - writes a parametrized decorator and a context manager; explains the protocol
- exercise_seeds:
    - "implement a retry decorator and a timing context manager"

### m06 — Concurrency & asyncio
- id: m06
- concepts: [concurrency, asyncio, io-streams, memory-model]
- prerequisites: [m04]
- ecosystem:
    libs: [asyncio, concurrent.futures]
- resources:
    - https://docs.python.org/3/library/asyncio.html
- mastery:
    - chooses asyncio vs threads vs processes appropriately; cancels tasks; avoids blocking the loop
    - explains the GIL and Python's object model (is vs ==, mutability)
- exercise_seeds:
    - "build an async bounded fetcher with a semaphore and graceful cancellation"
- transfer_note: |
    If concurrency is mastered (e.g. Go channels, JS event loop), skip the intro and
    contrast models: cooperative async/await, the GIL, when to reach for processes.

### m07 — Testing
- id: m07
- concepts: [testing]
- prerequisites: [m04]
- ecosystem:
    tools: [pytest, coverage]
    libs: [pytest]
- resources:
    - https://docs.pytest.org/
- mastery:
    - writes parametrized tests + fixtures; measures coverage; uses test doubles (no unittest.mock)
- exercise_seeds:
    - "convert a function to parametrized pytest cases and add a fixture-backed test double"

## Capstones
- mini_app: "an async CLI that fetches N URLs with bounded concurrency, typed, pytest-covered"
  — concepts: [concurrency, asyncio, type-system, testing, io-streams]
- interview: "live-coding: implement an LRU cache with a decorator API; verbal: explain the
  GIL and async vs threads" — concepts: [concurrency, type-system, decorators]
