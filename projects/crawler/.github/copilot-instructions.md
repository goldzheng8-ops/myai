# Copilot Instructions

This repository contains an intentionally layered crawler framework.

Read `AGENTS.md` and `ARCHITECTURE.md` before making non-trivial
changes.

## Core Rule

Make the smallest change that correctly solves the requested problem.

Do not redesign existing architecture unless explicitly requested.

## Responsibility

Before modifying code, determine which component owns the behavior.

Do not solve a problem by moving responsibility to another component
merely because that implementation is easier.

## Architecture Protection

Preserve:

- component responsibilities
- dependency direction
- framework abstractions
- registry/provider mechanisms
- lifecycle ownership
- Session/Cookie ownership
- resolution boundaries

Do not leak:

- Playwright types
- Scrapy types
- Httpx types

across framework boundaries unless explicitly required.

## Bug Fix Mode

When fixing a bug:

1. identify the root cause
2. identify the responsible component
3. identify the violated invariant
4. implement the smallest valid fix
5. validate the result

Do not perform unrelated refactoring.

## Architecture Conflict

If the apparently correct fix requires:

- moving responsibility
- changing dependency direction
- changing lifecycle ownership
- changing a public framework abstraction
- merging/splitting major components

stop and explain the architectural conflict.

Do not silently implement the architecture change.

## Python

Preserve the existing:

- typing conventions
- dataclass semantics
- dependency injection patterns
- registry/provider patterns
- naming conventions

Do not suppress type-checking errors without understanding the cause.

## Final Response

After completing a task, summarize:

- root cause
- solution
- files changed
- tests/type checking/linting performed
- any remaining concerns