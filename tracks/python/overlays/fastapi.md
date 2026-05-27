---
kind: overlay
parent_track: python
name: fastapi
display_name: FastAPI
target_version: "0.11x"
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - fastapi:routing
    - fastapi:validation
    - fastapi:di
    - fastapi:testing
  requires_parent:
    - type-system
    - typing-generics
    - decorators
    - asyncio
    - testing
    - concurrency
    - dependency-management
    - dataclasses
---

# FastAPI — Overlay (on the Python core)

> Audience: a learner who has completed the relevant Python core (typing, decorators,
> asyncio, dataclasses, testing). FastAPI is async-first and type-driven — the parent
> concepts are not optional. Curated; freshness pulled via Context7 at teach-time.

## Modules

### o01 — Routing
- id: o01
- concepts: [fastapi:routing]
- prerequisites: [parent:decorators, parent:type-system]
- ecosystem:
    libs: [fastapi, uvicorn]
- resources:
    - https://fastapi.tiangolo.com/tutorial/path-params/
    - https://fastapi.tiangolo.com/tutorial/query-params/
    - https://fastapi.tiangolo.com/tutorial/body/
    - https://fastapi.tiangolo.com/tutorial/bigger-applications/
- mastery:
    - declares an APIRouter and exposes GET/POST/PUT/DELETE with typed parameters
    - reads path / query / body via annotations (no manual parsing)
    - sets `status_code` and `response_model` explicitly on each route
    - structures an app by composing routers with `include_router(prefix=...)`
- exercise_seeds:
    - "in-memory `/items` CRUD: 4 routes, correct status codes, typed response_model"

### o02 — Validation
- id: o02
- concepts: [fastapi:validation]
- prerequisites: [o01, parent:typing-generics, parent:dataclasses]
- ecosystem:
    libs: [pydantic]
- resources:
    - https://docs.pydantic.dev/latest/concepts/models/
    - https://docs.pydantic.dev/latest/concepts/validators/
    - https://fastapi.tiangolo.com/tutorial/response-model/
- mastery:
    - models inputs and outputs with `BaseModel`, applies constraints via `Field(...)`
    - separates input and output models (e.g. `ItemCreate` vs `ItemOut`)
    - writes a `model_validator` or `field_validator` for a business rule
    - articulates why Pydantic differs from a stdlib dataclass in this context
- exercise_seeds:
    - "extend o01: split `ItemCreate` / `ItemOut`, validate `price > 0` and `name <= 80 chars`, return a clean 422"

### o03 — Dependency injection
- id: o03
- concepts: [fastapi:di]
- prerequisites: [o02, parent:asyncio]
- ecosystem:
    libs: [fastapi]
- resources:
    - https://fastapi.tiangolo.com/tutorial/dependencies/
    - https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- mastery:
    - factors a dependency with `Depends` and composes sub-dependencies
    - uses `yield` to manage open/close lifecycle (DB session, file)
    - injects an async dependency without changing the route signature
    - explains the per-request lifecycle of a dependency
- exercise_seeds:
    - "add `get_db()` (yields an in-memory dict), a `get_current_user()` reading `X-User-Id`, and an endpoint `/me/items` combining both"

### o04 — Testing
- id: o04
- concepts: [fastapi:testing]
- prerequisites: [o03, parent:testing]
- ecosystem:
    libs: [pytest, httpx]
- resources:
    - https://fastapi.tiangolo.com/tutorial/testing/
    - https://fastapi.tiangolo.com/advanced/async-tests/
- mastery:
    - writes pytest tests with `TestClient`, asserting status codes and JSON bodies
    - overrides dependencies via `app.dependency_overrides` to isolate units under test
    - asserts expected 4xx responses (422 on invalid payload, 401 on missing auth)
    - chooses `httpx.AsyncClient` over `TestClient` for async-only routes when relevant
- exercise_seeds:
    - "cover the previous modules' API: happy-path CRUD, 422 on invalid payload, 401 without `X-User-Id`, with `get_current_user` overridden"
