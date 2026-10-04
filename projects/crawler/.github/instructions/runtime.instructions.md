---
name: Runtime architecture
description: Rules for browser runtime and browser interaction code.
applyTo: "src/**/runtime/**/*.py,src/**/browser/**/*.py"
---

# Runtime Rules

Read the browser runtime section of `ARCHITECTURE.md` before making
non-trivial changes.

## BrowserRuntimeManager

Owns:

- Playwright lifecycle
- Browser lifecycle
- BrowserContext lifecycle
- browser session lifecycle
- transport-level cookie synchronization

Must not own:

- business workflows
- expression resolution
- spider-specific actions

## BrowserInteractionEngine

Owns:

- browser interaction execution
- browser action sequences

Must not own:

- Browser lifecycle
- BrowserContext lifecycle
- CookieJar
- generic expression resolution

## Rule

Do not move behavior between BrowserRuntimeManager and
BrowserInteractionEngine merely to simplify a bug fix.