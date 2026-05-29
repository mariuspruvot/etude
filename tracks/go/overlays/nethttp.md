---
kind: overlay
parent_track: go
name: nethttp
display_name: net/http
target_version: "1.24"
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
---

# net/http — Overlay (on the Go core)

> Audience: a learner who has completed the relevant Go core (interfaces, errors,
> io, testing). This overlay uses **only the standard library** — no framework. The
> Go 1.22+ `ServeMux` (method + wildcard patterns, `r.PathValue`) is required; do not
> target a Go below 1.22. Curated; freshness pulled via Context7 at teach-time.

## Modules

### o01 — Routing & handlers
- id: o01
- concepts: [nethttp:routing]
- prerequisites: [parent:interfaces-polymorphism]
- ecosystem:
    libs: [net/http]
- resources:
    - https://pkg.go.dev/net/http
    - https://go.dev/blog/routing-enhancements
- mastery:
    - registers routes on a `http.ServeMux` using Go 1.22+ method+pattern syntax (e.g. `"GET /items/{id}"`)
    - distinguishes `http.Handler` (the interface) from `http.HandlerFunc` (the adapter) and implements both
    - reads a path wildcard with `r.PathValue("id")` instead of manual URL parsing
    - configures and starts an explicit `http.Server{}` (addr, timeouts) rather than `http.ListenAndServe` defaults
- exercise_seeds:
    - "an in-memory `/items` API — 4 routes (GET list, GET by id, POST, DELETE) on a `ServeMux`, correct status codes via `w.WriteHeader`"

### o02 — Request/response & JSON
- id: o02
- concepts: [nethttp:json]
- prerequisites: [o01, parent:io-streams]
- ecosystem:
    libs: [net/http, encoding/json]
- resources:
    - https://pkg.go.dev/encoding/json
    - https://pkg.go.dev/net/http#Request
- mastery:
    - decodes a request body with `json.NewDecoder(r.Body)` and encodes responses with `json.NewEncoder(w)`
    - sets `Content-Type: application/json` and writes the status code before the body
    - rejects unknown fields with `Decoder.DisallowUnknownFields()` and maps a bad body to 400
    - returns 404 for a missing resource with a consistent JSON error envelope
- exercise_seeds:
    - "extend o01 — POST accepts a typed JSON body, validates a required field, returns a clean 400 with a JSON error envelope; GET-by-id returns 404 when absent"

### o03 — Middleware & composition
- id: o03
- concepts: [nethttp:middleware]
- prerequisites: [o02, parent:error-handling]
- ecosystem:
    libs: [net/http, context]
- resources:
    - https://pkg.go.dev/net/http#Handler
    - https://pkg.go.dev/context
- mastery:
    - writes middleware as `func(http.Handler) http.Handler` and chains several around a mux
    - carries a request-scoped value (e.g. a request id) via `context.WithValue` / `r.Context()`
    - centralises panic recovery in a middleware that turns a panic into a 500
    - explains why middleware order matters and where logging vs recovery sit in the chain
- exercise_seeds:
    - "add a logging middleware and a `requestID` middleware (stored in `r.Context()`) applied to all routes; a recovery middleware turns a panic into a 500"

### o04 — Testing
- id: o04
- concepts: [nethttp:testing]
- prerequisites: [o03, parent:testing]
- ecosystem:
    libs: [net/http/httptest, testing]
- resources:
    - https://pkg.go.dev/net/http/httptest
    - https://go.dev/doc/tutorial/add-a-test
- mastery:
    - tests a handler in isolation with `httptest.NewRecorder` and a constructed `*http.Request`
    - exercises the full stack end-to-end with `httptest.NewServer`
    - writes table-driven cases asserting status code and decoded JSON body
    - covers the failure paths (400 on invalid body, 404 on missing id) and asserts the `requestID` header is set
- exercise_seeds:
    - "cover the previous modules' API with table-driven tests — happy-path CRUD, 400 on invalid body, 404 on missing id, and assert the `requestID` header is set"
