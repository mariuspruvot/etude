---
kind: overlay
parent_track: typescript
name: nestjs
display_name: NestJS
target_version: "11.x"
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
---

# NestJS — Overlay (on the TypeScript core)

> Audience: a learner who has completed the relevant TypeScript core (typing, generics,
> typed async, testing) and ideally the Express overlay (NestJS abstracts the same
> HTTP foundations). NestJS is decorator- and DI-driven; this overlay is intentionally a
> 1:1 mirror of the FastAPI overlay (routing → validation → di → testing) so the
> cross-framework transfer is explicit. Curated; freshness pulled via Context7 at teach-time.

## Modules

### o01 — Modules & controllers
- id: o01
- concepts: [nestjs:routing]
- prerequisites: [parent:type-system]
- ecosystem:
    libs: ["@nestjs/common", "@nestjs/core"]
    tools: ["@nestjs/cli"]
- resources:
    - https://docs.nestjs.com/modules
    - https://docs.nestjs.com/controllers
- mastery:
    - wires a feature with `@Module` (declaring controllers and providers)
    - declares a `@Controller` and exposes routes with `@Get`/`@Post`/`@Param`/`@Body`
    - returns typed DTOs and sets status with `@HttpCode` where it differs from the default
    - explains the module graph (imports / providers / controllers / exports)
- exercise_seeds:
    - "an `ItemsModule` with an `ItemsController` exposing in-memory CRUD — typed DTOs, correct HTTP verbs (store kept in the controller for now)"

### o02 — Validation & pipes
- id: o02
- concepts: [nestjs:validation]
- prerequisites: [o01, parent:generics-ts]
- ecosystem:
    libs: ["@nestjs/common", class-validator, class-transformer]
- resources:
    - https://docs.nestjs.com/techniques/validation
    - https://docs.nestjs.com/pipes
- mastery:
    - applies a `ValidationPipe` (global or per-route) with `whitelist`/`forbidNonWhitelisted`
    - models inputs with `class-validator` DTOs (`@IsString`, `@Min`, etc.)
    - separates input and output DTOs (e.g. `CreateItemDto` vs `ItemDto`)
    - produces a 422 (or 400) with the validation errors on an invalid payload
- exercise_seeds:
    - "add a `CreateItemDto` with `@IsString`/`@Min(0)` constraints and a `whitelist` ValidationPipe; return 422 with the validation errors; keep an `ItemDto` for output"

### o03 — Dependency injection
- id: o03
- concepts: [nestjs:di]
- prerequisites: [o02, parent:dependency-management]
- ecosystem:
    libs: ["@nestjs/common"]
- resources:
    - https://docs.nestjs.com/providers
    - https://docs.nestjs.com/fundamentals/custom-providers
- mastery:
    - moves logic into an `@Injectable` service injected by constructor
    - registers the service as a provider and explains the default singleton scope
    - composes a sub-dependency (a service depending on another provider)
    - leaves no business state in the controller (it delegates to the service)
- exercise_seeds:
    - "extend o02 — introduce an `ItemsService` (holds the in-memory store), injected into the controller; no state left in the controller"

### o04 — Testing
- id: o04
- concepts: [nestjs:testing]
- prerequisites: [o03, parent:testing]
- ecosystem:
    libs: ["@nestjs/testing", supertest, vitest]
- resources:
    - https://docs.nestjs.com/fundamentals/testing
    - https://docs.nestjs.com/fundamentals/testing#end-to-end-testing
- mastery:
    - builds a test module with `Test.createTestingModule` and resolves a provider
    - unit-tests `ItemsService` in isolation
    - overrides a provider with `overrideProvider(...).useValue(...)` to isolate the controller
    - runs an e2e test with `supertest` over the Nest app, asserting the 422 path
- exercise_seeds:
    - "unit-test `ItemsService` in isolation, then an e2e test of the controller with a mocked service via `overrideProvider`, asserting the 422 path"
