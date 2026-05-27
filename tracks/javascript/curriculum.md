---
language: javascript
display_name: JavaScript
target_version: "ES2024"
freshness_source: context7
maintainers: [community]

concepts:
  transverse: [type-system, concurrency, testing, error-handling, io-streams]
  language_specific: [js-syntax, closures, prototypes, event-loop, modules-esm]
---

# JavaScript — Curriculum (stub)

> Stub track: skeleton is valid and usable; modules will be expanded by the community.

## Modules

### m01 — Syntax & primitives
- id: m01
- concepts: [js-syntax]
- prerequisites: []
- ecosystem:
    tools: [node, npm]
- resources:
    - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
- mastery:
    - declares with const/let, uses arrow functions, destructuring, template literals
- exercise_seeds:
    - "transform arrays with map/filter/reduce"

### m02 — Closures & the event loop
- id: m02
- concepts: [closures, event-loop, concurrency]
- prerequisites: [m01]
- ecosystem:
    libs: [Promise]
- resources:
    - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop
- mastery:
    - explains closures and the microtask/macrotask queue; uses async/await correctly
- exercise_seeds:
    - "build an async function that batches requests with Promise.all and a concurrency cap"
