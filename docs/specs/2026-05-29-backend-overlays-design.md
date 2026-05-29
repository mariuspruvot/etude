# Backend overlays batch (net/http, Express, NestJS, Prisma) — design

**Status:** draft / awaiting user review
**Date:** 2026-05-29
**Predecessors:**
- `docs/specs/2026-05-27-etude-v1.3-overlays-design.md` — the overlay **mechanism**
  (schema + `tools/lint_overlay.py` + skill awareness).
- `docs/specs/2026-05-28-fastapi-overlay-design.md` — the first overlay **content**
  (FastAPI on Python, PR #9). This batch reuses that quality bar and template.

---

## 1. Purpose

Ship four curated backend overlays in one batch, covering the employable backend
surface of two tracks that currently have **zero** backend overlays:

- **`tracks/go/overlays/nethttp.md`** — net/http stdlib (Go 1.22+ routing).
- **`tracks/typescript/overlays/express.md`** — Express (HTTP foundations).
- **`tracks/typescript/overlays/nestjs.md`** — NestJS (structured/enterprise framework).
- **`tracks/typescript/overlays/prisma.md`** — Prisma (data layer / ORM).

Each mirrors the proven **4-module arc** of the FastAPI overlay (`o01`→`o04`), where
each `exercise_seed` extends the previous module's artifact. Selection rationale
(captured during brainstorming): the user prioritised **employability** over
modern-but-niche choices (Hono ruled out for now), and chose the **stdlib foundation**
for Go deliberately. Prisma is kept a **standalone overlay** (orthogonal data axis,
reusable by both Express and NestJS) rather than folded into NestJS.

Success = the four files lint, the skills (`assess`, `teach`, `exercise`, `status`)
resolve their overlay concepts without any code change, and a learner who finished the
relevant core modules can be routed into any of them seamlessly.

## 2. Non-goals

- No change to `tools/lint_overlay.py` or its schema (closed since v1.3).
- No change to the parent `tracks/go/curriculum.md` or `tracks/typescript/curriculum.md`
  (closed schema; we only **read** their concepts to populate `requires_parent`).
- No change to the integrity hook (`progress/*/exercises/*` stays write-protected
  except `prompt.md`/`feedback.md`).
- No starter exercise files written in advance — `exercise` generates them on demand.
- No overlay capstone — the schema defines none; the four `exercise_seeds` chain into a
  single toy artifact per overlay and that is enough.
- No improvement to the TypeScript **core** curriculum (the "advanced types" gap noted
  in conversation is a separate, deferred change — see §8).
- No second wave of overlays (Fastify, Gin/Echo/chi, SQLAlchemy, Drizzle) — out of scope.

## 3. Deliverables

All four files share the same shape: `kind: overlay` frontmatter, `concepts.overlay`
namespaced by `name`, `requires_parent` ⊆ the parent track's declared concepts, and four
modules whose `prerequisites` are either `parent:<c>` (with `c` ∈ `requires_parent`) or an
**earlier** `oNN` in document order (lint rule: document order ⇒ no cycles).

`target_version` and all `resources` URLs are pulled **via Context7 at write-time**, not
guessed in this spec (consistent with the FastAPI overlay). `mastery` bullets below are
the design intent; each must be observable/gradable by the `grader` agent.

### Cross-overlay concept map (maximised isomorphism)

A deliberate design constraint: keep the four-module spine **as parallel as honestly
possible** so a learner sees the same roles recur and cross-framework transfer is
visible. The shared spine (with FastAPI as the reference):

| slot | role            | fastapi      | nethttp     | express      | nestjs       | prisma          |
|------|-----------------|--------------|-------------|--------------|--------------|-----------------|
| o01  | structure       | `routing`    | `routing`   | `routing`    | `routing`    | `schema-modeling` |
| o02  | data / validate | `validation` | `json`      | `validation` | `validation` | `client-queries`  |
| o03  | composition     | `di`         | `middleware`| `middleware` | `di`         | `relations`       |
| o04  | verify          | `testing`    | `testing`   | `testing`    | `testing`    | `testing`         |

- **`<name>:testing` is universal** (5/5) — every overlay's o04 is literally `:testing`.
- **`<name>:routing` is the o01 for every HTTP overlay** (4/5).
- Where a framework genuinely lacks a role, the name stays **honest** rather than forced:
  net/http has no validation library (o02 is `json` marshalling) and no DI container (o03
  is `middleware`); Express has middleware, not DI (o03 `middleware`); Prisma is a **data
  axis**, not HTTP, so o01–o03 don't map to routing/validation/di — only the `:testing`
  anchor is shared.
- **NestJS is intentionally a 1:1 mirror of FastAPI** (`routing`/`validation`/`di`/`testing`,
  same order) — both are "structured framework" overlays, so the parallel is exact.

---

### A. `tracks/go/overlays/nethttp.md` — net/http (stdlib)

**Frontmatter:**

```yaml
kind: overlay
parent_track: go
name: nethttp
display_name: net/http
target_version: "1.24"   # confirm via Context7 at write-time; Go 1.22+ routing required
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - nethttp:routing
    - nethttp:json
    - nethttp:middleware
    - nethttp:testing
  requires_parent:
    - interfaces-polymorphism
    - io-streams
    - error-handling
    - go-error-wrapping
    - testing
```

**Parent concepts — verified citation.** All five `requires_parent` items exist in
`tracks/go/curriculum.md:9-32` (transverse: `interfaces-polymorphism`, `io-streams`,
`error-handling`, `testing`; language_specific: `go-error-wrapping`).

**Concept-naming rationale.** Role-based (`routing`, `json`, `middleware`, `testing`)
rather than API-based, leaving room for a future `chi`/`gin` overlay without collision.

**Module dependency graph:**

| id  | concepts             | prerequisites                              |
|-----|----------------------|--------------------------------------------|
| o01 | `nethttp:routing`    | `parent:interfaces-polymorphism`           |
| o02 | `nethttp:json`       | `o01, parent:io-streams`                   |
| o03 | `nethttp:middleware` | `o02, parent:error-handling`               |
| o04 | `nethttp:testing`    | `o03, parent:testing`                      |

**Module bodies (mastery intent + seed):**

- **o01 — Routing & handlers.** Register routes on `http.ServeMux` using Go 1.22+
  method+pattern syntax (`"GET /items/{id}"`); implement `http.Handler` and
  `http.HandlerFunc`; read `r.PathValue("id")`; configure and start an `http.Server`
  (not `ListenAndServe` defaults).
  Seed: *"An in-memory `/items` API — 4 routes (GET list, GET by id, POST, DELETE) on a
  `ServeMux`, correct status codes via `w.WriteHeader`."*
- **o02 — Request/response & JSON.** Decode a request body with `json.Decoder`; encode
  responses with `json.Encoder`; set `Content-Type`; map invalid input to 400, missing
  resource to 404; reject unknown fields (`DisallowUnknownFields`).
  Seed: *"Extend o01 — POST accepts a typed JSON body, validates a required field, returns
  a clean 400 with a JSON error envelope; GET-by-id returns 404 when absent."*
- **o03 — Middleware & composition.** Write middleware as
  `func(http.Handler) http.Handler`; chain several; carry a request-scoped value via
  `context.Context`; centralise error/recovery handling.
  Seed: *"Add a logging middleware and a `requestID` middleware (stored in `r.Context()`),
  applied to all routes; a recovery middleware turns a panic into a 500."*
- **o04 — Testing.** Use `net/http/httptest` — `httptest.NewRecorder` for handler-level
  tests and `httptest.NewServer` for end-to-end; table-driven cases asserting status +
  JSON body; assert the 400/404 paths.
  Seed: *"Cover the previous modules' API with table-driven tests — happy-path CRUD, 400
  on invalid body, 404 on missing id, and assert the `requestID` header is set."*

---

### B. `tracks/typescript/overlays/express.md` — Express

**Frontmatter:**

```yaml
kind: overlay
parent_track: typescript
name: express
display_name: Express
target_version: "4.x"   # confirm via Context7 at write-time (note: 5.x is now stable)
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - express:routing
    - express:middleware
    - express:validation
    - express:testing
  requires_parent:
    - type-system
    - async-await-ts
    - error-handling
    - modules-esm
    - testing
```

**Parent concepts — verified citation.** All five exist in
`tracks/typescript/curriculum.md:8-10` (transverse: `type-system`, `error-handling`,
`testing`; language_specific: `async-await-ts`, `modules-esm`).

**Module dependency graph:**

| id  | concepts             | prerequisites                                       |
|-----|----------------------|-----------------------------------------------------|
| o01 | `express:routing`    | `parent:type-system`                                |
| o02 | `express:validation` | `o01`                                               |
| o03 | `express:middleware` | `o02, parent:async-await-ts, parent:error-handling` |
| o04 | `express:testing`    | `o03, parent:testing`                               |

**Module bodies (mastery intent + seed):**

- **o01 — Routing.** Compose an app with `Router`; read params/query/body; type
  `Request`/`Response` (via `@types/express`); set status codes explicitly; mount
  routers under a prefix.
  Seed: *"An in-memory `/items` CRUD — 4 typed routes mounted via a `Router`, correct
  status codes."*
- **o02 — Validation.** Validate body/params with **Zod**; infer the request type from
  the schema (`z.infer`); return a clean 400/422 with the parse errors (inline at first).
  Seed: *"Validate the POST body with a Zod schema (`name`, `price > 0`), respond 422 with
  field errors on failure, and use the inferred type in the handler — no `any`."*
- **o03 — Middleware & errors.** Understand the `(req, res, next)` signature and the
  4-arg error-handler `(err, req, res, next)`; propagate async errors to the handler
  (wrap or `next(err)`); refactor o02's inline 422 and a `NotFoundError` into a centralised
  error middleware; order matters.
  Seed: *"Extend o02 — add a logging middleware and a centralised error handler that maps a
  thrown `NotFoundError` to 404, a Zod error to 422, and anything else to 500."*
- **o04 — Testing.** Use `supertest` + `vitest` against the `app` instance (no live
  port); assert status + JSON body; cover the 404 and 422 paths.
  Seed: *"Cover the API with supertest — happy-path CRUD, 422 on invalid body, 404 on
  missing id."*

---

### C. `tracks/typescript/overlays/nestjs.md` — NestJS

**Frontmatter:**

```yaml
kind: overlay
parent_track: typescript
name: nestjs
display_name: NestJS
target_version: "11.x"   # confirm via Context7 at write-time
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - nestjs:routing
    - nestjs:validation
    - nestjs:di
    - nestjs:testing
  requires_parent:
    - type-system
    - generics-ts
    - async-await-ts
    - dependency-management
    - testing
```

**Parent concepts — verified citation.** All five exist in
`tracks/typescript/curriculum.md:8-10` (transverse: `type-system`,
`dependency-management`, `testing`; language_specific: `generics-ts`, `async-await-ts`).

**Concept-naming rationale.** NestJS is a **1:1 mirror of FastAPI** —
`routing`/`validation`/`di`/`testing`, same order — because both are structured
framework overlays. Identical concept suffixes make the cross-framework transfer
explicit in the learner's `skills.md`. Module *titles* stay descriptive (e.g. o01 is
"Modules & controllers") even though the *concept* is `nestjs:routing`.

**Module dependency graph:**

| id  | concepts             | prerequisites                          |
|-----|----------------------|----------------------------------------|
| o01 | `nestjs:routing`     | `parent:type-system`                   |
| o02 | `nestjs:validation`  | `o01, parent:generics-ts`              |
| o03 | `nestjs:di`          | `o02, parent:dependency-management`    |
| o04 | `nestjs:testing`     | `o03, parent:testing`                  |

**Module bodies (mastery intent + seed):**

- **o01 — Modules & controllers.** Wire a feature with `@Module`; declare a
  `@Controller` with `@Get`/`@Post`/`@Param`/`@Body`; return typed DTOs; understand the
  module graph (imports/providers/controllers). (Store kept in the controller for now.)
  Seed: *"An `ItemsModule` with an `ItemsController` exposing in-memory CRUD — typed DTOs,
  correct HTTP verbs."*
- **o02 — Validation & pipes.** Apply `ValidationPipe` (global or per-route) with
  `class-validator`/`class-transformer` DTOs; separate input vs output DTOs; produce a
  422 on invalid payload.
  Seed: *"Add a `CreateItemDto` with `@IsString`/`@Min(0)` constraints and a `whitelist`
  ValidationPipe; return 422 with the validation errors; keep an `ItemDto` for output."*
- **o03 — Dependency injection.** Move logic into an `@Injectable` service; inject by
  constructor; register it as a provider; understand provider scope (default singleton).
  Seed: *"Extend o02 — introduce an `ItemsService` (holds the in-memory store), injected
  into the controller; no state left in the controller."*
- **o04 — Testing.** Use `@nestjs/testing` `Test.createTestingModule`; override a
  provider for isolation; e2e with `supertest` over the Nest app; assert 422.
  Seed: *"Unit-test `ItemsService` in isolation, then an e2e test of the controller with a
  mocked service via `overrideProvider`, asserting the 422 path."*

---

### D. `tracks/typescript/overlays/prisma.md` — Prisma

**Frontmatter:**

```yaml
kind: overlay
parent_track: typescript
name: prisma
display_name: Prisma
target_version: "6.x"   # confirm via Context7 at write-time
freshness_source: context7
maintainers: [community]
concepts:
  overlay:
    - prisma:schema-modeling
    - prisma:client-queries
    - prisma:relations
    - prisma:testing
  requires_parent:
    - type-system
    - generics-ts
    - async-await-ts
    - testing
```

**Parent concepts — verified citation.** All four exist in
`tracks/typescript/curriculum.md:8-10` (transverse: `type-system`, `testing`;
language_specific: `generics-ts`, `async-await-ts`).

**Concept-naming rationale.** `prisma:*` does not map to the HTTP spine
(routing/validation/di) — Prisma is a **data axis**. Only the universal `:testing`
anchor is shared. `prisma migrate dev` lives in o01 (it materialises the schema you just
wrote), which keeps o04 pure `prisma:testing`, consistent with every other overlay.

**Module dependency graph:**

| id  | concepts                  | prerequisites                       |
|-----|---------------------------|-------------------------------------|
| o01 | `prisma:schema-modeling`  | `parent:type-system`                |
| o02 | `prisma:client-queries`   | `o01, parent:async-await-ts`        |
| o03 | `prisma:relations`        | `o02, parent:generics-ts`           |
| o04 | `prisma:testing`          | `o03, parent:testing`               |

**Module bodies (mastery intent + seed):**

- **o01 — Schema & modeling.** Write `schema.prisma` — `datasource` (SQLite for the
  exercise), `generator`, a `model` with scalar fields, `@id`, `@unique`, `@default`;
  run `prisma generate`; materialise the DB with `prisma migrate dev`.
  Seed: *"Model an `Item` (`id`, `name`, `price`, `createdAt`) in `schema.prisma`,
  generate the client, run the first migration, and prove the generated types are imported."*
- **o02 — Typed client & queries.** Instantiate `PrismaClient`; CRUD with
  `create`/`findMany`/`findUnique`/`update`/`delete`; use `select`/`where`; observe that
  results are fully typed (no `any`).
  Seed: *"Write typed functions `createItem`/`listItems`/`getItem`/`deleteItem` against the
  client; `getItem` returns `Item | null`."*
- **o03 — Relations & transactions.** Model a 1-n relation (`User` has many `Item`);
  query with `include`; nested `create`; wrap multi-step writes in `$transaction`.
  Seed: *"Add a `User` model owning items (a new migration); create a user with two items
  in one nested write; list a user with `include: { items: true }`; move an item between
  users inside a `$transaction`."*
- **o04 — Testing.** Seed a known dataset; test the query/relation functions against a
  throwaway SQLite DB; reset/isolate state between tests.
  Seed: *"Add a seed script and vitest tests that run against a temp SQLite file, asserting
  the relation queries from o03 and cleaning up between cases."*

## 4. Validation / Definition of done

1. `uv run --script tools/lint_overlay.py tracks/go/overlays/nethttp.md` passes.
2. `uv run --script tools/lint_overlay.py tracks/typescript/overlays/express.md` passes.
3. `uv run --script tools/lint_overlay.py tracks/typescript/overlays/nestjs.md` passes.
4. `uv run --script tools/lint_overlay.py tracks/typescript/overlays/prisma.md` passes.
   (PEP 723 invocation — `uv run python tools/...` fails with `ModuleNotFoundError: yaml`,
   per `tools/CLAUDE.md`.)
5. `uv run --with pyyaml --with pytest pytest tools/test_lint_overlay.py` still passes
   (no linter change).
6. `assess` lists all four overlays under their parent tracks (manual check in an empty
   workdir): net/http on Go; Express/NestJS/Prisma on TypeScript.
7. `teach` can produce a lesson on one concept per overlay (Context7 fetch succeeds).
8. All `resources` URLs resolve (HEAD/WebFetch) before commit.
9. `revise-claude-md` invoked at the end (definition of done per `~/.claude/CLAUDE.md`).

## 5. Workflow

1. Isolated worktree off `main` (per `~/.claude/CLAUDE.md` discipline).
2. Implementation plan with explicit Assumptions section.
3. Per overlay: pull current docs via Context7 → write the file → lint → fix.
   The four files are independent and can be written in parallel.
4. Update README/`tracks/OVERLAYS.md` only if the contributing docs need a backend
   example (likely not — the FastAPI overlay already serves as the example).
5. PR to `main`. Clean up worktree post-merge.

## 6. Risks

- **Skill overlay-awareness across two tracks.** The FastAPI overlay only exercised the
  Python track. These are the first overlays on Go and TypeScript. If a skill resolves a
  `nethttp:*` / `express:*` concept against the parent core instead of the overlay, that
  is a skill bug (out of scope to fix here) — isolate and file separately.
- **Express 4.x vs 5.x.** Express 5 is now stable; error-handling for async and some
  middleware behaviours differ. `target_version` and the `async error` mastery bullet in
  o02 must be pinned to whichever major Context7 reports current at write-time, and the
  seed must not assume 4.x auto-catch behaviour.
- **Go routing version floor.** The method+pattern `ServeMux` syntax in o01 requires Go
  1.22+. If `target_version` were ever lowered below 1.22 the o01 mastery would be
  invalid — keep the floor explicit.
- **Resource URL drift.** Verify URLs at write-time; community PRs fix later 404s.
- **Batch size.** Four overlays (~16 modules) in one PR is larger than the FastAPI PR.
  Mitigation: identical schema, independent files, one linter — if review drags, the PR
  can be split by file without rework.

## 7. Assumptions (to verify at review)

- **Skills resolve `nethttp:*`/`express:*`/`nestjs:*`/`prisma:*` to these overlays' modules** —
  claimed by the v1.3 design and validated once (FastAPI). *To confirm:* run `assess` in a
  clean workdir against Go and TypeScript and confirm each overlay appears.
- **CI runs `lint_overlay.py` on every `tracks/*/overlays/*.md`** — memory says there is
  **no** `.github/workflows/` yet. *To confirm:* if CI is absent, linting is manual
  (step §4.1–4.4) and wiring CI is a separate change.
- **Concept names are final** — driven by the maximised-isomorphism map in §3: every o04
  is `<name>:testing` (universal); `<name>:routing` is the o01 for all HTTP overlays;
  **NestJS mirrors FastAPI exactly** (`routing`/`validation`/`di`/`testing`). Honest
  divergences: `nethttp:json` (stdlib has no validation lib), `nethttp:middleware` /
  `express:middleware` (no DI container), and `prisma:*` stays on the data axis. Renaming
  after a learner records them in `progress/<track>/skills.md` is a breaking change — fix now.
- **Prisma belongs on the TypeScript track, not its own track** — it is a TS-first ORM;
  treating it as a TS overlay (data axis) is consistent with the overlay definition
  ("a framework/**library** path on top of a language track's core").
- **SQLite is an acceptable exercise datastore for Prisma** — zero-setup, file-based,
  supported by `prisma migrate`. Avoids requiring Postgres/Docker for a learner exercise.
- **No starter `prompt.md` pre-merge** — `exercise` generates per-learner prompts, like the
  rest of the repo.
- **All `mastery` bullets are observable/gradable** — the `grader` agent must pass/fail
  each on a learner submission; rewrite any "understands why X" bullet as a check.

## 8. Out of scope (explicit)

- TypeScript **core** curriculum improvements (advanced types module, `.d.ts`, the
  missing `interfaces-polymorphism` transverse concept) — noted in conversation, deferred
  to a separate spec.
- A second wave of overlays: Fastify, Gin/Echo/chi, Drizzle, SQLAlchemy.
- Hono (ruled out for now — niche job market vs Express/NestJS).
- Changes to the curriculum/overlay lint or schema.
- Changes to the integrity hook.
- CI wiring for overlay linting (separate change if CI is introduced).
- A `CONTRIBUTING.md` file (the README section from PR #9 is sufficient).
