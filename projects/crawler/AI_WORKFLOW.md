# AI Workflow

## Phase 1 — Understand

Before editing:

- inspect the relevant code
- inspect related interfaces
- inspect registrations/providers
- inspect relevant tests
- read relevant architecture rules

Do not edit yet.

---

## Phase 2 — Diagnose

Identify:

- symptom
- root cause
- responsible component
- violated invariant
- affected interfaces

---

## Phase 3 — Classify

Classify the change:

- Level 1: implementation
- Level 2: interface
- Level 3: architecture

Follow `CHANGE_POLICY.md`.

---

## Phase 4 — Implement

For Level 1:

implement directly.

For Level 2:

explain the interface impact before implementation.

For Level 3:

stop and request explicit approval.

---

## Phase 5 — Validate

Run:

- focused tests
- broader relevant tests
- type checking
- linting

Inspect the final diff.

---

## Phase 6 — Report

Report:

- root cause
- solution
- files changed
- tests run
- type checking result
- linting result
- architectural impact
- remaining risks