---
name: Middleware architecture
description: Rules for crawler middleware.
applyTo: "src/**/middleware/**/*.py,src/**/middlewares/**/*.py"
---

# Middleware Rules

Middleware implements cross-cutting request, response, and session
behavior.

Middleware may:

- inspect request state
- transform request state
- inspect response state
- transform response state
- interact with framework session state

Middleware must not:

- implement spider-specific workflows
- directly construct infrastructure implementations
- bypass framework abstractions
- depend on concrete Spider implementations

Preserve middleware priority semantics.

Do not move workflow logic into middleware merely because middleware
has convenient access to request/response state.