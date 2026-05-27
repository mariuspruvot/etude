---
language: go
display_name: Go
target_version: "1.24"          # tutor calibrates to this; Context7 fetches current docs
freshness_source: context7      # prefer Context7 over model recollection for libs/APIs
maintainers: [community]

# Concept vocabulary. transverse keys are the canonical ids written to progress/skills.md.
concepts:
  transverse:                   # shared across languages — drive cross-language transfer
    - error-handling
    - concurrency
    - type-system
    - testing
    - interfaces-polymorphism
    - memory-model
    - dependency-management
    - io-streams
  language_specific:            # Go-only nuance, tracked but not transferred
    - go-syntax                 # variables, control flow, slices/maps, range — NEVER transfers
    - goroutines
    - channels
    - go-modules
    - struct-embedding
    - defer-panic-recover
    - go-error-wrapping
---

# Go — Curriculum

> Target audience: developers comfortable in at least one language. The `assess` skill
> establishes the learner's transverse level first, then enters at the right module.

## Modules

### m01 — Tooling & project layout
- id: m01
- concepts: [dependency-management, go-modules]
- prerequisites: []
- ecosystem:
    tools: [go build, go run, go vet, gofmt]
    libs: []
    files: [go.mod, go.sum]
- resources:
    - https://go.dev/doc/tutorial/getting-started
    - https://go.dev/ref/mod
- mastery:
    - initializes a module and adds/removes a dependency without help
    - explains the role of go.mod vs go.sum
- exercise_seeds:
    - "scaffold a CLI module that imports one third-party lib and runs `go vet` clean"

### m02 — Syntax & primitives
- id: m02
- concepts: [go-syntax]
- prerequisites: [m01]
- ecosystem:
    tools: [gofmt, go run]
    libs: [fmt]
- resources:
    - https://go.dev/tour/basics/1
    - https://go.dev/tour/flowcontrol/1
- mastery:
    - declares variables (var, :=), writes loops/conditionals, and functions idiomatically
    - uses slices and maps correctly (length vs capacity, range, nil map pitfalls)
- exercise_seeds:
    - "implement small pure functions over slices and maps (group, filter, count)"
- transfer_note: |
    This module does NOT transfer across languages — being senior elsewhere does not mean
    you know Go's syntax. assess only skips m02 if skills.md shows go-syntax already
    proficient (i.e. the learner has used Go before). For a paradigm-experienced newcomer,
    teach syntax fast but DO teach it: contrast with their known language ("Go's slices
    are not Python lists: ...") rather than from scratch.

### m03 — Types, structs & the type system
- id: m03
- concepts: [type-system, struct-embedding]
- prerequisites: [m02]
- ecosystem:
    tools: [go vet]
    libs: [encoding/json]
- resources:
    - https://go.dev/tour/moretypes/2
    - https://go.dev/blog/json
- mastery:
    - models a domain with structs + composition (not inheritance)
    - marshals/unmarshals JSON with correct struct tags
- exercise_seeds:
    - "model an order with nested structs and round-trip it through JSON"
- transfer_note: |
    If type-system is already mastered (e.g. from a typed language), compress the
    primitives lesson and emphasize Go specifics: zero values, value vs pointer
    receivers, struct embedding instead of inheritance.

### m04 — Errors & error handling
- id: m04
- concepts: [error-handling, go-error-wrapping, defer-panic-recover]
- prerequisites: [m03]
- ecosystem:
    libs: [errors, fmt]
- resources:
    - https://go.dev/blog/error-handling-and-go
    - https://go.dev/blog/go1.13-errors
- mastery:
    - returns and checks errors idiomatically (no panic for control flow)
    - wraps with %w and inspects with errors.Is / errors.As
- exercise_seeds:
    - "build a parser that wraps low-level errors with context and is testable with errors.Is"
    - "debug: a function swallows errors with `_ =` — fix it to wrap and propagate with %w"
    - "read-and-explain: why does this errors.Is check fail across a fmt.Errorf boundary?"

### m05 — Interfaces & polymorphism
- id: m05
- concepts: [interfaces-polymorphism, io-streams]
- prerequisites: [m03]
- ecosystem:
    libs: [io, sort]
- resources:
    - https://go.dev/tour/methods/9
    - https://go.dev/doc/effective_go#interfaces
- mastery:
    - defines small interfaces at the consumer, not the producer
    - explains the empty interface / any and when to avoid it
- exercise_seeds:
    - "implement io.Writer for a custom sink and plug it into the standard library"

### m06 — Concurrency: goroutines & channels
- id: m06
- concepts: [concurrency, goroutines, channels, memory-model]
- prerequisites: [m04]
- ecosystem:
    tools: [go test -race]
    libs: [sync, context]
- resources:
    - https://go.dev/tour/concurrency/1
    - https://go.dev/blog/pipelines
    - https://go.dev/ref/mem
- mastery:
    - chooses channels vs sync primitives appropriately
    - cancels work with context and avoids goroutine leaks
    - code passes `go test -race`
- exercise_seeds:
    - "build a bounded worker pool with graceful shutdown via context"
    - "debug: a goroutine leaks because its channel is never closed — find and fix the leak"
    - "refactor: replace a shared-counter mutex with a channel-based worker pool"
- transfer_note: |
    If concurrency is mastered (e.g. Python asyncio, JS event loop), skip the conceptual
    intro and contrast models directly: CSP/channels vs async-await, the race detector,
    the Go memory model's happens-before guarantees.

### m07 — Testing & benchmarks
- id: m07
- concepts: [testing]
- prerequisites: [m04]
- ecosystem:
    tools: [go test, go test -bench, go test -cover]
    libs: [testing, testify]
- resources:
    - https://go.dev/doc/tutorial/add-a-test
    - https://pkg.go.dev/testing
- mastery:
    - writes table-driven tests
    - measures coverage and writes a benchmark
- exercise_seeds:
    - "convert an existing function to table-driven tests and add a benchmark"

## Capstones (feed the mini-app and interview modes)
- mini_app: "a concurrent CLI that fetches N URLs with a worker pool, bounded
  concurrency, context cancellation, and table-driven tests" — concepts: [concurrency,
  error-handling, testing, io-streams]
- interview: "live-coding: implement an LRU cache; verbal: explain the Go memory model
  and when a mutex beats a channel" — concepts: [concurrency, type-system, memory-model]
