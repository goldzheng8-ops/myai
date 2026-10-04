---
name: Spider architecture
description: Rules for spider workflow implementations.
applyTo: "src/**/spider/**/*.py,src/**/spiders/**/*.py"
---

# Spider Rules

Spider owns crawler workflow.

Spider may coordinate:

- requests
- request steps
- framework services
- browser interaction
- extraction
- pagination

Spider must not directly own:

- browser lifecycle
- transport implementation
- cookie storage
- generic expression resolution
- infrastructure construction

Use existing framework services and abstractions.

Do not directly instantiate concrete infrastructure implementations
when an existing provider, registry, or service exists.