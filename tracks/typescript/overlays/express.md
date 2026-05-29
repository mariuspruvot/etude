---
kind: overlay
parent_track: typescript
name: express
display_name: Express
target_version: "5.x"
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - express:routing
    - express:validation
    - express:middleware
    - express:testing
  requires_parent:
    - type-system
    - async-await-ts
    - error-handling
    - modules-esm
    - testing
---

# Express — Overlay (on the TypeScript core)

> Audience: a learner who has completed the relevant TypeScript core (typed async,
> error handling, ESM, testing). Express is the minimal, ubiquitous Node HTTP layer —
> this overlay teaches the foundations every higher-level framework abstracts. Target
> Express 5.x (5 forwards rejected promises from handlers to the error middleware
> automatically — a key change from 4.x). Curated; freshness pulled via Context7 at
> teach-time.

## Modules

### o01 — Routing
- id: o01
- concepts: [express:routing]
- prerequisites: [parent:type-system]
- ecosystem:
    libs: [express, "@types/express"]
    files: [package.json, tsconfig.json]
- resources:
    - https://expressjs.com/en/5x/api.html
    - https://expressjs.com/en/guide/routing.html
- mastery:
    - composes an app from one or more `Router` instances mounted under a prefix
    - reads `req.params` / `req.query` / `req.body` and types the handler via `Request`/`Response`
    - sets status codes explicitly (`res.status(201).json(...)`) rather than relying on defaults
    - enables JSON body parsing with `express.json()` and explains where it sits in the chain
- exercise_seeds:
    - "an in-memory `/items` CRUD — 4 typed routes mounted via a `Router`, correct status codes"

### o02 — Validation
- id: o02
- concepts: [express:validation]
- prerequisites: [o01]
- ecosystem:
    libs: [zod]
- resources:
    - https://zod.dev/
    - https://zod.dev/?id=safeparse
- mastery:
    - models the request body/params with a Zod schema and validates with `safeParse`
    - derives the handler's input type from the schema with `z.infer` (no hand-written duplicate, no `any`)
    - returns a clean 422 (or 400) with the flattened field errors on failure
    - keeps the parsed, typed value flowing into the handler logic
- exercise_seeds:
    - "validate the POST body with a Zod schema (`name`, `price > 0`), respond 422 with field errors on failure, and use the inferred type in the handler — no `any`"

### o03 — Middleware & errors
- id: o03
- concepts: [express:middleware]
- prerequisites: [o02, parent:async-await-ts, parent:error-handling]
- ecosystem:
    libs: [express]
- resources:
    - https://expressjs.com/en/guide/using-middleware.html
    - https://expressjs.com/en/guide/error-handling.html
- mastery:
    - writes ordinary middleware with the `(req, res, next)` signature and explains ordering
    - writes a centralised error handler with the 4-arg `(err, req, res, next)` signature
    - relies on Express 5 auto-forwarding of rejected promises (no manual `try/catch` + `next(err)` in every handler)
    - maps domain errors to status codes (`NotFoundError` → 404, a Zod error → 422, anything else → 500)
- exercise_seeds:
    - "extend o02 — add a logging middleware and a centralised error handler that maps a thrown `NotFoundError` to 404, a Zod error to 422, and anything else to 500"

### o04 — Testing
- id: o04
- concepts: [express:testing]
- prerequisites: [o03, parent:testing]
- ecosystem:
    libs: [supertest, vitest]
- resources:
    - https://github.com/ladjs/supertest
    - https://vitest.dev/guide/
- mastery:
    - exports the `app` separately from the listen call so tests run without binding a port
    - drives the app with `supertest`, asserting status code and JSON body
    - covers the failure paths (422 on invalid body, 404 on missing id)
    - structures tests so each case is independent of the others' state
- exercise_seeds:
    - "cover the API with supertest — happy-path CRUD, 422 on invalid body, 404 on missing id"
