---
name: Testing conventions
description: Testing rules for the crawler framework.
applyTo: "tests/**/*.py"
---

# Testing Rules

Tests should verify behavior and architectural contracts.

Prefer tests that validate:

- public framework behavior
- component responsibilities
- registry/provider behavior
- request/response contracts
- session/cookie semantics
- resolution behavior
- downloader behavior
- middleware behavior

When fixing a bug:

1. reproduce the bug with a focused test
2. implement the fix
3. keep the regression test

Do not weaken a test merely to make an implementation pass.

If an implementation conflicts with an architectural contract,
prefer correcting the implementation rather than weakening the
contract.