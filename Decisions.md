## `DECISIONS.md` 

# Technical Decisions

## Circular Dependency Detection

Circular dependencies are detected using a Depth-First Search (DFS) traversal.

When adding a dependency A → B:
- The system checks whether B already reaches A
- If a path exists, adding the dependency would create a cycle
- The full cycle path is returned in the error response

This approach treats tasks as nodes and dependencies as directed edges.

### Time Complexity
- O(V + E) in the worst case
- Suitable for the expected scale (20–30 tasks)

---

## Why DFS Over BFS

DFS was chosen because:
- It naturally tracks traversal paths
- Easier to return the exact cycle path
- Simple recursive implementation

---

## Automatic Status Updates

Task status is derived from dependency states:
- All dependencies completed → `in_progress`
- Any dependency blocked → `blocked`
- Dependencies exist but not all completed → `pending`
- Completing a task triggers cascade updates to dependent tasks

Cascade updates ensure consistency across the dependency graph.

---

## Graph Visualization Choice

SVG was chosen over Canvas because:
- Easier to reason about positions
- Declarative structure
- No external libraries required
- Sufficient for small-to-medium graphs

The layout is intentionally simple to prioritize correctness over visual polish.

---

## Trade-offs

- No automatic layout algorithm (manual positioning)
- No optimistic UI updates (backend remains source of truth)
- Focused on correctness and clarity over animations
