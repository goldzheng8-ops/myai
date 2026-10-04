# Agent Instructions

## Project Rules

This repository is an intentionally designed crawler framework.

Read:

- `ARCHITECTURE.md`
- `CHANGE_POLICY.md`
- `AI_WORKFLOW.md`

before making non-trivial changes.

The architecture is intentional.

Do not silently redesign it.

---

## Before Coding

For any non-trivial task:

1. Identify the relevant subsystem.
2. Identify the component responsible for the behavior.
3. Check the relevant architectural boundary.
4. Determine whether the requested change is Level 1, Level 2,
   or Level 3 according to `CHANGE_POLICY.md`.
5. Prefer the smallest valid change.

---

## Architecture

Responsibilities defined in `ARCHITECTURE.md` are authoritative.

Do not:

- move responsibilities for convenience
- merge components to reduce code
- bypass existing abstractions
- introduce parallel extension mechanisms
- leak third-party types across framework boundaries
- turn context objects into service locators
- turn managers into general-purpose services

---

## Bug Fixes

Fix behavior in the component that owns it.

Do not move responsibility merely because the current implementation
is inconvenient.

If the correct fix requires an architecture change:

STOP and explain the conflict before implementing it.

---

## Implementation

Prefer:

- existing abstractions
- existing registries
- existing providers
- existing services
- existing configuration mechanisms

Avoid unnecessary abstractions.

Avoid unrelated refactoring.

---

## Validation

After making changes:

1. run relevant tests
2. run type checking
3. run linting
4. inspect the final diff
5. verify architectural boundaries

If a validation step cannot be run, report it explicitly.

---

## Communication

For non-trivial changes, report:

- root cause
- responsible component
- changed files
- architectural reasoning
- validation performed

Do not claim a change is complete if validation was not performed.