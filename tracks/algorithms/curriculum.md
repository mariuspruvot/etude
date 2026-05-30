---
kind: transversal               # NEW schema — linted by tools/lint_transversal.py, not lint_curriculum.py
name: algorithms                # also the concept namespace prefix
display_name: Algorithms & Data Structures
languages: [python, go, typescript]   # impl languages the learner may pick; the grader executes in the chosen one
freshness_source: context7
maintainers: [community]

# Transversal track: language-agnostic but gradable. Concepts are namespaced `algorithms:`
# and track-local (they never drive a language track's cross-skip logic).
concepts:
  transversal:
    - algorithms:complexity
    - algorithms:arrays-hashing
    - algorithms:linked-structures
    - algorithms:trees-heaps
    - algorithms:graphs
    - algorithms:sorting-searching
    - algorithms:recursion-dp
---

# Algorithms & Data Structures — Transversal track

> Audience: developers comfortable in at least one language who want the engineering axis a
> language track does not teach. Pick an impl language from `languages` at the start; the tutor
> teaches the concept language-agnostically and shows one idiomatic example in your language
> (current stdlib via Context7). The `grader` runs your solution in the language you chose.

## Modules

### t01 — Complexity & Big-O
- id: t01
- concepts: [algorithms:complexity]
- prerequisites: []
- resources:
    - https://wiki.python.org/moin/TimeComplexity
    - https://docs.python.org/3/tutorial/datastructures.html
- mastery:
    - states time/space complexity of a loop/recursion in Big-O; distinguishes worst/average/amortized
    - explains why a hash lookup is O(1) average but O(n) worst, and dynamic-array append amortized O(1)
- exercise_seeds:
    - "given 3 short functions, annotate each with tight Big-O and justify in one line"
    - "debug: a function claimed O(n) is actually O(n^2) — find the hidden quadratic and fix it"
- transfer_note: |
    Complexity is fully language-agnostic. If the learner reasons about Big-O already (any
    language), make this a fast calibration, not a lesson.

### t02 — Arrays, strings & hashing
- id: t02
- concepts: [algorithms:arrays-hashing]
- prerequisites: [t01]
- resources:
    - https://docs.python.org/3/library/collections.html
    - https://docs.python.org/3/tutorial/datastructures.html
- mastery:
    - applies two-pointer and sliding-window patterns; uses a hash map/set to trade space for time
- exercise_seeds:
    - "find the longest substring without repeating characters (sliding window), with tests"
    - "two-sum and group-anagrams using a hash map; analyze the complexity you achieved"

### t03 — Linked structures: lists, stacks, queues
- id: t03
- concepts: [algorithms:linked-structures]
- prerequisites: [t01]
- resources:
    - https://docs.python.org/3/library/collections.html#collections.deque
    - https://pkg.go.dev/container/list
- mastery:
    - implements a singly-linked list and a stack/queue; reverses a list in place
    - knows when a deque/array beats a linked list (cache locality, O(1) ends)
- exercise_seeds:
    - "implement a queue using two stacks; tests cover interleaved push/pop"
    - "detect a cycle in a linked list with Floyd's two pointers"

### t04 — Trees & heaps
- id: t04
- concepts: [algorithms:trees-heaps]
- prerequisites: [t03]
- resources:
    - https://docs.python.org/3/library/heapq.html
    - https://pkg.go.dev/container/heap
- mastery:
    - traverses a binary tree (pre/in/post, level-order); explains BST invariants
    - uses a heap/priority queue for top-k and explains its O(log n) operations
- exercise_seeds:
    - "validate a BST and compute its height; tests include skewed and balanced trees"
    - "find the k largest elements of a stream using a heap"

### t05 — Graphs
- id: t05
- concepts: [algorithms:graphs]
- prerequisites: [t04]
- resources:
    - https://docs.python.org/3/library/collections.html#collections.deque
    - https://docs.python.org/3/library/heapq.html
- mastery:
    - represents a graph (adjacency list); implements BFS and DFS; detects a cycle
    - implements one shortest-path (BFS for unweighted or Dijkstra with a heap) and topological sort
- exercise_seeds:
    - "BFS shortest path on an adjacency list; tests cover a disconnected graph and no-path case"
    - "topological sort of a DAG; debug a version that loops forever on a cycle"

### t06 — Sorting & searching
- id: t06
- concepts: [algorithms:sorting-searching]
- prerequisites: [t01, t02]
- resources:
    - https://docs.python.org/3/library/bisect.html
    - https://pkg.go.dev/sort
- mastery:
    - implements binary search correctly (no off-by-one); explains O(n log n) comparison sorts
    - implements quickselect or merge sort and reasons about stability and worst case
- exercise_seeds:
    - "binary search + its variants (leftmost/rightmost insertion point), fully tested"
    - "debug: a binary search that infinite-loops on the midpoint — find the boundary bug"

### t07 — Recursion, backtracking & dynamic programming
- id: t07
- concepts: [algorithms:recursion-dp]
- prerequisites: [t03, t04]
- resources:
    - https://docs.python.org/3/library/functools.html
    - https://docs.python.org/3/tutorial/controlflow.html
- mastery:
    - converts a recursive solution to memoized then bottom-up DP; identifies overlapping subproblems
    - solves one backtracking problem (subsets/permutations) and bounds its complexity
- exercise_seeds:
    - "coin-change: recursive → memoized → tabulated; tests assert all three agree"
    - "generate all subsets via backtracking; analyze the 2^n bound"

## Capstones (feed the mini-app and interview modes)
- mini_app: "implement an LRU cache (hash map + doubly-linked list) with O(1) get/put and tests"
  — concepts: [algorithms:linked-structures, algorithms:complexity]
- interview: "live-coding: a graph traversal or a DP problem; verbal: justify the complexity
  trade-offs and why you chose the data structure" — concepts: [algorithms:graphs,
  algorithms:recursion-dp, algorithms:complexity]
