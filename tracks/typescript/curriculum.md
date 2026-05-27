---
language: typescript
display_name: TypeScript
target_version: "5.x"
freshness_source: context7
maintainers: [community]

concepts:
  transverse: [type-system, concurrency, testing, error-handling, io-streams, dependency-management]
  language_specific: [ts-syntax, structural-typing, generics-ts, narrowing, async-await-ts, modules-esm]
---

# TypeScript — Curriculum

> Audience: developers comfortable in at least one language. Plain JavaScript is treated as
> a subset — TS is the default. Front-end frameworks (React, Vue) are on-demand extensions.

## Modules

### m01 — Tooling & project setup
- id: m01
- concepts: [dependency-management]
- prerequisites: []
- ecosystem:
    tools: [node, npm, tsc, ts-node, vitest]
    files: [package.json, tsconfig.json]
- resources:
    - https://www.typescriptlang.org/docs/handbook/intro.html
    - https://nodejs.org/en/learn
- mastery:
    - initializes a project with package.json + tsconfig, runs tsc clean
- exercise_seeds:
    - "scaffold a typed Node CLI with strict tsconfig that compiles clean"

### m02 — Syntax & primitives
- id: m02
- concepts: [ts-syntax]
- prerequisites: [m01]
- ecosystem:
    libs: [console]
- resources:
    - https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
- mastery:
    - declares typed variables/functions, uses arrays/tuples/objects, template literals
- exercise_seeds:
    - "implement typed array/record transforms (group, filter, map)"
- transfer_note: |
    Syntax does not transfer. Teach fast by contrast with the learner's known language.

### m03 — The type system (structural typing, narrowing)
- id: m03
- concepts: [type-system, structural-typing, narrowing]
- prerequisites: [m02]
- ecosystem:
    tools: [tsc]
- resources:
    - https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- mastery:
    - models data with interfaces/types; uses unions + narrowing; explains structural typing
- exercise_seeds:
    - "model a discriminated union and exhaustively narrow it (no any)"
- transfer_note: |
    If type-system is mastered (e.g. mypy-typed Python, Go), contrast structural vs nominal
    typing and TS-specific narrowing.

### m04 — Generics
- id: m04
- concepts: [generics-ts]
- prerequisites: [m03]
- resources:
    - https://www.typescriptlang.org/docs/handbook/2/generics.html
- mastery:
    - writes generic functions + constrained generics; avoids `any`
- exercise_seeds:
    - "implement a generic Result<T, E> with type-safe helpers"

### m05 — Errors & async
- id: m05
- concepts: [error-handling, async-await-ts, concurrency, io-streams]
- prerequisites: [m04]
- ecosystem:
    libs: [Promise, fetch]
- resources:
    - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-1.html
    - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
- mastery:
    - types async functions/Promises; handles errors without swallowing; bounds concurrency
- exercise_seeds:
    - "build a typed async fetcher with Promise.all and a concurrency cap"
- transfer_note: |
    If concurrency/async is mastered (Python asyncio, Go), contrast the single-threaded
    event loop and microtask queue.

### m06 — Modules & testing
- id: m06
- concepts: [modules-esm, testing]
- prerequisites: [m04]
- ecosystem:
    tools: [vitest]
    files: [package.json]
- resources:
    - https://vitest.dev/guide/
- mastery:
    - structures ESM imports/exports; writes typed unit tests; measures coverage
- exercise_seeds:
    - "convert a module to ESM and cover it with typed vitest cases"

## Capstones
- mini_app: "a typed Node CLI that fetches N URLs with bounded concurrency and vitest tests"
  — concepts: [async-await-ts, type-system, testing, io-streams]
- interview: "live-coding: implement a typed LRU cache; verbal: structural typing & narrowing"
  — concepts: [type-system, generics-ts, async-await-ts]
