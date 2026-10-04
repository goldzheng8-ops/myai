---
name: Resolution architecture
description: Rules for ResolveEngine, ResolveStrategy, RuntimeContext,
  and expression resolution.
applyTo: "src/**/resolve/**/*.py,src/**/resolution/**/*.py,src/**/template/**/*.py"
---

# Resolution Rules

## ResolveEngine

ResolveEngine:

- receives RuntimeContext
- receives ResolveExpression
- selects ResolveStrategy
- returns the resolved result

ResolveEngine must not:

- execute browser actions
- access Playwright
- access downloader implementations
- implement spider workflow
- become a service locator

## ResolveStrategy

Each strategy should represent one coherent resolution behavior.

Prefer:

    ResolveExpression
        +
    ResolveStrategy
        +
    ResolveRegistry

over adding type-specific branching directly to ResolveEngine.

## RuntimeContext

RuntimeContext is a resolution context.

Do not turn it into:

- a service locator
- a dependency container
- a global application state object
- a general-purpose service registry

## Template Execution

Template/value resolution and browser action execution are separate
responsibilities.

Resolve values first.

Execute browser actions in the browser interaction layer.