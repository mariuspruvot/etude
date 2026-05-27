---
language: sql
display_name: SQL
target_version: "PostgreSQL 16"
freshness_source: context7
maintainers: [community]

concepts:
  transverse: [data-modeling, query-design, performance]
  language_specific: [joins, aggregation, window-functions, indexing, transactions]
---

# SQL — Curriculum (stub)

> Stub track. Exercises are reviewed qualitatively in v1 (no DB execution harness yet);
> see roadmap. Mastery is checked by reading the query + explaining the plan.

## Modules

### m01 — SELECT, filtering, joins
- id: m01
- concepts: [query-design, joins]
- prerequisites: []
- resources:
    - https://www.postgresql.org/docs/current/tutorial-join.html
- mastery:
    - writes correct INNER/LEFT joins; filters with WHERE vs HAVING appropriately
- exercise_seeds:
    - "given a 3-table schema, write a query joining them with correct cardinality"

### m02 — Aggregation & window functions
- id: m02
- concepts: [aggregation, window-functions]
- prerequisites: [m01]
- resources:
    - https://www.postgresql.org/docs/current/tutorial-window.html
- mastery:
    - uses GROUP BY + window functions; explains the difference
- exercise_seeds:
    - "compute a running total per group with a window function"
