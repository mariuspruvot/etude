# Go track — tutor notes

When teaching Go, prefer current idioms over legacy patterns. Pull current stdlib/library
usage via Context7 rather than relying on recollection (see `target_version` / `freshness_source`).

- Emphasize: zero values, value vs pointer receivers, composition over inheritance,
  small consumer-defined interfaces, explicit error returns (no exceptions), `errors.Is`/`As`.
- Tooling the learner must touch: `go mod`, `go test`, `go test -race`, `go vet`, `gofmt`.
- For concurrency exercises, always require `go test -race` to pass.
- Solution files are learner-written; never write `.go` solution files (the hook blocks it).
