---
kind: overlay
parent_track: typescript
name: prisma
display_name: Prisma
target_version: "7.x"
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
---

# Prisma — Overlay (on the TypeScript core)

> Audience: a learner who has completed the relevant TypeScript core (typing, generics,
> typed async, testing). Prisma is a **data-layer** overlay — orthogonal to the HTTP
> frameworks (Express, NestJS) and composable with either. It does not map onto the
> routing/validation/di spine; only the `:testing` anchor is shared. SQLite is used so a
> learner needs no external database server. Prisma 7 generates the client into a local
> output dir (`generator client { provider = "prisma-client" }`) and accesses SQLite via
> a driver adapter — the teach skill pulls the exact current setup via Context7.

## Modules

### o01 — Schema & modeling
- id: o01
- concepts: [prisma:schema-modeling]
- prerequisites: [parent:type-system]
- ecosystem:
    libs: [prisma, "@prisma/client"]
    files: [schema.prisma]
- resources:
    - https://www.prisma.io/docs/orm/prisma-schema/overview
    - https://www.prisma.io/docs/orm/overview/databases/sqlite
- mastery:
    - writes a `schema.prisma` with a `generator` (client output dir) and a SQLite `datasource`
    - models a table with scalar fields and attributes (`@id`, `@unique`, `@default`)
    - runs `prisma generate` and imports the generated, typed client
    - materialises the database with `prisma migrate dev` and explains what the migration created
- exercise_seeds:
    - "model an `Item` (`id`, `name`, `price`, `createdAt`) in `schema.prisma`, generate the client, run the first migration, and prove the generated types are imported"

### o02 — Typed client & queries
- id: o02
- concepts: [prisma:client-queries]
- prerequisites: [o01, parent:async-await-ts]
- ecosystem:
    libs: ["@prisma/client"]
- resources:
    - https://www.prisma.io/docs/orm/prisma-client/queries/crud
    - https://www.prisma.io/docs/orm/prisma-client/queries/select-fields
- mastery:
    - instantiates a `PrismaClient` and runs CRUD with `create`/`findMany`/`findUnique`/`update`/`delete`
    - narrows results with `select` and filters with `where`
    - observes that results are fully typed end-to-end (no `any`, `findUnique` returns `T | null`)
    - awaits queries correctly and disconnects the client when appropriate
- exercise_seeds:
    - "write typed functions `createItem`/`listItems`/`getItem`/`deleteItem` against the client; `getItem` returns `Item | null`"

### o03 — Relations & transactions
- id: o03
- concepts: [prisma:relations]
- prerequisites: [o02, parent:generics-ts]
- ecosystem:
    libs: ["@prisma/client"]
    files: [schema.prisma]
- resources:
    - https://www.prisma.io/docs/orm/prisma-schema/data-model/relations
    - https://www.prisma.io/docs/orm/prisma-client/queries/relation-queries
    - https://www.prisma.io/docs/orm/prisma-client/queries/transactions
- mastery:
    - models a 1-n relation (e.g. `User` has many `Item`) and migrates it
    - loads related rows with `include` and creates related rows with a nested write
    - wraps a multi-step write in `$transaction` and explains the atomicity guarantee
    - reasons about the typed shape returned when `include` is used
- exercise_seeds:
    - "add a `User` model owning items (a new migration); create a user with two items in one nested write; list a user with `include: { items: true }`; move an item between users inside a `$transaction`"

### o04 — Testing
- id: o04
- concepts: [prisma:testing]
- prerequisites: [o03, parent:testing]
- ecosystem:
    libs: [vitest, prisma]
- resources:
    - https://www.prisma.io/docs/orm/prisma-client/testing/integration-testing
    - https://vitest.dev/guide/
- mastery:
    - seeds a known dataset before tests (a seed script or per-test setup)
    - runs the query/relation functions against a throwaway SQLite file
    - resets/isolates state between tests so cases do not leak into each other
    - asserts the relation queries from o03 and the `T | null` contract from o02
- exercise_seeds:
    - "add a seed script and vitest tests that run against a temp SQLite file, asserting the relation queries from o03 and cleaning up between cases"
