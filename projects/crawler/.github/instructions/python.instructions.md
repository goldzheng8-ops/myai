---
name: Python conventions
description: Python implementation conventions for this repository.
applyTo: "**/*.py"
---

# Python Conventions

- Preserve existing type annotations.
- Prefer precise types over `Any`.
- Preserve existing dataclass `frozen` and `slots` semantics.
- Follow existing dependency injection patterns.
- Follow existing registry/provider patterns.
- Do not introduce global mutable state.
- Do not suppress Pylance/type-checking errors without understanding
  the underlying issue.
- Prefer existing project abstractions over duplicate utilities.
- Keep public interfaces stable unless the task explicitly requires
  an interface change.