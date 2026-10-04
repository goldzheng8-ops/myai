---
name: Downloader architecture
description: Rules for downloader implementations.
applyTo: "src/**/downloader/**/*.py,src/**/downloaders/**/*.py"
---

# Downloader Rules

Downloaders are transport implementations.

A downloader:

- accepts framework requests
- performs transport execution
- produces RequestResponse
- adapts transport-specific results into framework abstractions

A downloader must not:

- implement spider workflow
- resolve templates
- manage browser lifecycle
- directly manipulate Spider
- introduce business-specific behavior

When adding a downloader:

1. implement the existing Downloader abstraction
2. reuse existing request/response abstractions
3. use the existing registry/provider mechanism
4. keep third-party types inside the integration boundary