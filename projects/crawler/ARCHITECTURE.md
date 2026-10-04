# Architecture

## 1. Purpose

This project is a configurable crawler framework.

The framework separates:

- application bootstrapping
- configuration
- spider workflow
- request/response processing
- transport
- browser runtime
- session state
- template/expression resolution
- middleware
- infrastructure

The architecture is intentional.

Existing abstractions and responsibility boundaries must not be
simplified, merged, bypassed, or relocated merely to make an
implementation easier.

---

## 2. Architectural Principles

### 2.1 Separation of Responsibilities

Each component owns a specific kind of behavior.

A component must not take ownership of behavior belonging to
another component merely because it is convenient.

### 2.2 Dependency Direction

Higher-level workflow components may depend on lower-level
abstractions.

Lower-level infrastructure must not depend on higher-level
workflow components.

### 2.3 Framework Abstractions

Framework-level code must use framework abstractions instead of
leaking third-party implementation types across architectural
boundaries.

Examples include:

- Request
- RequestResponse
- ResponseAdapter
- Session
- Cookie
- CookieJar
- Downloader
- ResolveExpression
- ResolveStrategy
- RuntimeContext

Third-party types such as Playwright, Scrapy, and Httpx types
should remain inside their respective integration boundaries.

### 2.4 Explicit Ownership

Lifecycle, state, workflow, transport, and resolution responsibilities
must have explicit owners.

Do not create implicit shared ownership.

---

# 3. Major Components

## 3.1 Application

Responsible for:

- loading application configuration
- constructing application dependencies
- initializing framework components
- starting the application

Must not:

- implement spider workflow
- implement downloader behavior
- implement browser interaction behavior
- contain domain-specific crawling logic

---

## 3.2 Configuration

Configuration is responsible for representing and resolving
application configuration.

Configuration objects describe behavior.

They should not become service objects.

Configuration must not:

- execute requests
- access Playwright
- access Scrapy
- access Httpx
- perform crawling

---

## 3.3 Spider

Spider owns crawler workflow.

Responsible for:

- defining crawling behavior
- coordinating crawler-level operations
- creating framework requests
- coordinating request steps
- interpreting crawler results

Spider must not:

- directly construct infrastructure implementations
- manage Playwright lifecycle
- implement HTTP transport
- directly manage cookie persistence
- implement generic expression resolution

---

## 3.4 Services

Services coordinate framework capabilities.

Services may compose multiple lower-level abstractions.

Services must not become generic containers for unrelated functionality.

A service should have a clear responsibility.

---

# 4. Browser Runtime

## 4.1 BrowserRuntimeManager

BrowserRuntimeManager owns browser runtime lifecycle.

Responsible for:

- Playwright lifecycle
- Browser lifecycle
- BrowserContext lifecycle
- browser session lifecycle
- page registration/lifecycle where applicable
- transport-level cookie synchronization

BrowserRuntimeManager must not:

- execute business workflows
- interpret crawler templates
- resolve expressions
- implement spider-specific actions
- become a general-purpose browser automation service

BrowserRuntimeManager provides runtime capabilities to higher-level
components.

---

## 4.2 BrowserInteractionEngine

BrowserInteractionEngine owns browser interaction execution.

Responsible for:

- executing browser interaction workflows
- executing browser actions
- coordinating pages within an existing browser runtime
- producing interaction outputs

BrowserInteractionEngine must not:

- create the browser runtime
- own Browser lifecycle
- own BrowserContext lifecycle
- implement CookieJar
- implement generic expression resolution
- implement spider workflow

BrowserInteractionEngine uses BrowserRuntimeManager rather than
owning browser lifecycle itself.

---

# 5. Session and Cookie Architecture

## 5.1 Session

Session represents logical crawler session state.

Session owns:

- session identity
- logical session metadata
- CookieJar

Session must not depend directly on:

- Playwright
- Scrapy
- Httpx

---

## 5.2 Cookie

Cookie is the framework-level representation of a cookie.

Cookie must preserve cookie semantics required by the framework,
including the distinction between:

- explicit domain
- host-only cookie

Do not collapse host-only semantics into `domain=None`.

---

## 5.3 CookieJar

CookieJar owns logical cookie storage and lookup.

Responsible for:

- storing cookies
- replacing cookies
- querying cookies
- URL-based cookie matching
- preserving cookie domain/path/name semantics

CookieJar must not depend on:

- Playwright
- Scrapy
- Httpx

CookieJar is transport-independent.

---

## 5.4 Cookie Extractors

Extractors convert third-party cookie representations into
framework Cookie objects.

Examples:

- PlaywrightCookieExtractor
- ScrapyCookieExtractor
- HttpxCookieExtractor

An extractor owns conversion.

It does not own cookie storage.

---

## 5.5 Cookie Serializers

Serializers convert framework Cookie objects into third-party
representations.

Examples:

- PlaywrightCookieSerializer
- ScrapyCookieSerializer
- HttpxCookieSerializer

A serializer owns conversion.

It does not own cookie storage.

---

# 6. Downloader Architecture

## 6.1 Downloader

Downloader owns transport execution.

Responsible for:

- accepting framework requests
- performing transport operations
- producing RequestResponse
- adapting transport-specific responses into framework abstractions

Downloader must not:

- execute spider workflows
- resolve templates
- implement business logic
- manage browser lifecycle
- directly manipulate Spider

---

## 6.2 Downloader Implementations

Examples:

- HttpxDownloader
- ScrapyDownloader
- PlaywrightDownloader
- Aria2Downloader

Each downloader implements the common downloader abstraction.

Third-party APIs must remain behind the downloader boundary.

---

## 6.3 Downloader Registry

Downloader implementations are discovered and constructed through
the framework registry/provider mechanism.

Do not introduce ad-hoc downloader construction in application,
spider, or service code.

---

# 7. Middleware Architecture

Middleware implements cross-cutting request/session/response behavior.

Examples:

- AuthMiddleware
- CacheMiddleware
- CookieMiddleware
- DeduplicateMiddleware
- FingerprintMiddleware
- ProxyMiddleware
- RetryMiddleware
- SessionMiddleware
- ThrottleMiddleware

Middleware may:

- inspect request state
- transform request state
- transform response state
- interact with framework session state

Middleware must not:

- implement spider workflow
- directly instantiate infrastructure implementations
- bypass framework abstractions
- introduce business-specific workflow logic

Middleware execution order is determined by middleware priority.

Default priority belongs to middleware implementation/configuration
rather than requiring every YAML entry to repeat it.

---

# 8. Resolution Architecture

## 8.1 ResolveExpression

ResolveExpression represents a request to resolve a value.

An expression describes what should be resolved.

It does not perform resolution itself.

---

## 8.2 ResolveStrategy

ResolveStrategy implements resolution behavior for a particular
expression type.

A strategy:

- receives RuntimeContext
- receives its corresponding ResolveExpression
- returns the resolved value

A strategy must not become a general-purpose service.

---

## 8.3 ResolveRegistry

ResolveRegistry maps ResolveExpression types to ResolveStrategy
implementations.

New resolution behavior should normally be added by:

1. defining an expression
2. implementing its strategy
3. registering the strategy

Avoid adding large type-dispatch chains to ResolveEngine.

---

## 8.4 ResolveEngine

ResolveEngine is the entry point for expression resolution.

It is responsible for:

- receiving RuntimeContext
- receiving ResolveExpression
- selecting the appropriate strategy
- returning the resolved result

ResolveEngine must not:

- execute browser actions
- access Playwright
- access downloader implementations
- implement spider workflow
- become a service locator

---

## 8.5 RuntimeContext

RuntimeContext provides context required during resolution.

RuntimeContext must remain a context object.

Do not turn RuntimeContext into:

- a service locator
- a dependency container
- a global application state object
- a general-purpose service registry

---

# 9. Template Architecture

Templates describe configurable workflow behavior.

Template processing may use:

- template expressions
- ResolveEngine
- RuntimeContext
- framework template extensions

Template resolution must remain separate from browser execution.

The template system determines values and actions.

The browser interaction layer executes browser actions.

Do not merge these responsibilities.

---

# 10. Registry and Provider Architecture

Registries provide explicit extension points.

Examples include:

- DownloaderRegistry
- ResolveRegistry
- TemplateExtensionRegistry

Providers are responsible for controlled construction and lifecycle
management.

Do not bypass the registry/provider architecture with direct
construction when an existing extension point exists.

---

# 11. Dependency Rules

The following dependencies are forbidden.

ResolveEngine
    -> Playwright                         FORBIDDEN

ResolveEngine
    -> Scrapy                             FORBIDDEN

CookieJar
    -> Playwright                         FORBIDDEN

CookieJar
    -> Scrapy                             FORBIDDEN

CookieJar
    -> Httpx                              FORBIDDEN

BrowserRuntimeManager
    -> Spider implementation              FORBIDDEN

Downloader
    -> Spider implementation              FORBIDDEN

Middleware
    -> concrete Spider implementation     FORBIDDEN

Infrastructure
    -> application workflow               FORBIDDEN

Lower-level transport
    -> higher-level crawler workflow      FORBIDDEN

---

# 12. Third-Party Boundary

Third-party framework types should not leak across framework
boundaries unless explicitly justified.

Examples:

Playwright Page
Playwright BrowserContext
Scrapy Request
Scrapy Response
Httpx Response

should normally be translated into framework abstractions before
crossing subsystem boundaries.

Integration-specific code belongs in integration-specific components.

---

# 13. Extension Rules

When adding a new capability, prefer an existing extension point.

Examples:

New downloader:

    Downloader
        ↓
    implementation
        ↓
    registry/provider

New resolver:

    ResolveExpression
        +
    ResolveStrategy
        ↓
    ResolveRegistry

New middleware:

    Middleware
        ↓
    middleware implementation
        ↓
    middleware chain

New template extension:

    TemplateExtension
        ↓
    TemplateExtensionRegistry

Do not create parallel extension mechanisms unless the existing
mechanism is demonstrably incapable of representing the new behavior.

---

# 14. Architecture Change

Architecture changes are explicit design decisions.

The following are architecture changes:

- changing component responsibility
- merging components
- splitting major components
- changing dependency direction
- changing lifecycle ownership
- changing Session/Cookie ownership
- replacing framework-level abstractions
- replacing the registry/provider model
- introducing a new architectural subsystem

An AI agent must not perform such changes implicitly while fixing
an implementation bug.