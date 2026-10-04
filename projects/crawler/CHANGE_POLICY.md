# Change Policy

## 1. Purpose

This document defines what an AI agent may change autonomously.

The goal is to allow AI agents to maintain and extend the project
without silently changing established architecture.

---

# 2. Change Levels

## Level 1 — Implementation Change

AI may perform these changes autonomously.

Examples:

- bug fixes
- implementation corrections
- local refactoring
- test additions
- type annotation improvements
- error handling improvements
- performance improvements that preserve architecture
- internal algorithm replacement
- implementation cleanup

Requirements:

- preserve public interfaces unless necessary
- preserve responsibility boundaries
- preserve dependency direction
- preserve existing extension points

---

## Level 2 — Interface Change

Requires explicit explanation before implementation.

Examples:

- changing a public method signature
- changing a protocol/interface
- changing configuration schema
- changing Request/Response contracts
- changing Session/Cookie APIs
- changing registry/provider contracts

Before implementation, AI must explain:

1. why the change is necessary
2. which components are affected
3. whether backward compatibility is affected
4. whether an alternative Level 1 change exists

---

## Level 3 — Architecture Change

AI must stop before implementation.

Examples:

- moving responsibility between components
- merging components
- splitting major components
- changing lifecycle ownership
- changing dependency direction
- replacing core framework abstractions
- introducing a new architectural layer
- removing an established abstraction

AI must:

1. identify the architectural conflict
2. explain the proposed change
3. identify affected components
4. explain alternatives
5. wait for explicit approval

---

# 3. Bug Fixing Policy

A bug fix must first determine:

1. What behavior is incorrect?
2. Which component owns that behavior?
3. Which invariant is being violated?
4. What is the smallest valid change?

The preferred fix is:

    existing owner
        ↓
    correction

not:

    existing owner
        ↓
    move responsibility
        ↓
    another component

If a bug appears difficult to fix within the existing architecture,
the difficulty must not itself be treated as justification for an
architecture change.

---

# 4. Scope Control

AI must not perform unrelated refactoring while fixing a bug.

Do not:

- rename unrelated classes
- reorganize unrelated modules
- replace unrelated abstractions
- change formatting across unrelated files
- upgrade dependencies without necessity
- redesign configuration
- simplify architecture

unless explicitly requested.

---

# 5. New Abstractions

Do not introduce an abstraction merely because:

- the current code is repetitive
- the implementation could be "cleaner"
- another project uses the abstraction
- the abstraction makes the current patch shorter

Introduce a new abstraction only when:

- the responsibility is clearly identified
- multiple concrete implementations genuinely exist
- the abstraction represents a stable concept
- an existing abstraction cannot represent the behavior

---

# 6. Dependency Changes

Adding a new dependency between major components is an architectural
change unless it is clearly within an existing dependency direction.

Before introducing a new dependency, identify:

- source component
- target component
- reason
- dependency direction
- whether an existing abstraction can avoid the dependency

---

# 7. Third-Party Dependencies

Do not introduce a third-party dependency merely to simplify a local
implementation.

Before adding a dependency:

1. determine whether the standard library is sufficient
2. inspect existing project dependencies
3. determine whether the dependency belongs to the relevant layer
4. consider long-term maintenance cost

---

# 8. Deletion Policy

Do not delete an abstraction merely because it currently appears
unused.

Before deletion, determine:

- whether it is an extension point
- whether configuration references it
- whether registry/provider discovery references it
- whether external code may depend on it
- whether it represents an intentional architectural boundary

---

# 9. Compatibility

When changing a public framework abstraction, prefer backward-compatible
changes where practical.

If compatibility cannot be preserved, explicitly report the breaking
change.

---

# 10. Final Validation

After every non-trivial change:

- run relevant tests
- run type checking
- run linting
- inspect changed files
- verify dependency direction
- verify architecture invariants

The implementation is not considered complete merely because the
original failing test passes.