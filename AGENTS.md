# AI Coding Agent Instructions — Juhi

These instructions are the central operating rules for AI coding agents working on Juhi. Follow them for every task. Repository-specific instructions in a nearer `AGENTS.md` file may add detail, but must not silently weaken security, privacy, or validation requirements here.

## 1. Project Context

- **Project:** Juhi AI Companion
- **Purpose:** Build an Android-first AI companion application that supports natural conversation, personalized companion personas, user-controlled long-term memory, multilingual text, and staged rollout of voice and image-generation experiences.
- **Primary users:** Adults using Juhi for AI companionship, conversation, personalization, and creative interaction. Enforce the product's documented age eligibility and safety requirements.
- **Client:** Flutter / Dart for Android-first mobile experiences, unless the repository documents a different implementation.
- **Backend:** Python / FastAPI, unless the existing repository architecture establishes another service boundary.
- **Data:** PostgreSQL as the durable application source of truth; vector search, object storage, Firebase services, or other infrastructure only as specified by the current architecture and deployment configuration.
- **AI integrations:** Use the project's provider abstraction and configured model providers. Never hard-code a provider, model, credential, or endpoint where configuration or an adapter is expected.
- **Product priorities:** Reliable memory, natural multilingual conversation, a consistent and configurable companion personality, trustworthy voice/image experiences, user privacy and safety, and predictable operating costs.

Do not infer additional product requirements from this summary. The PRD and current approved implementation decisions govern feature behavior.

## 2. Source of Truth

Before a significant change, read the relevant documentation under `docs/` and inspect the current implementation. Core documents are:

- `docs/PRD.md` — product scope, user stories, priorities, business rules, and acceptance criteria.
- `docs/DESIGN_SYSTEM.md` — visual tokens, components, interaction patterns, accessibility, and localization UX.
- `docs/ARCHITECTURE.md` — system boundaries, module responsibilities, data flows, integrations, and deployment.
- `docs/DATABASE.md` — schema, relationships, constraints, indexes, migrations, retention, and data lifecycle.
- `docs/SECURITY.md` — threat model, authentication, authorization, privacy, AI safety, secrets, and operational security.
- `docs/CODE_STYLE.md` — naming, project structure, language conventions, code quality, and review standards.
- `docs/TESTING.md` — test strategy, test fixtures, coverage expectations, evaluation criteria, and release gates.

If a document is absent at the specified path, search the repository for the matching file, including lowercase variants such as `prd.md`, `design_system.md`, `architecture.md`, `database.md`, `security.md`, `code_style.md`, and `testing.md`. Do not assume a file exists or claim to have read it when it does not. If documentation appears in multiple locations, identify the most relevant/current version and call out ambiguity when it affects the task.

Also inspect relevant local instructions, such as a nearer `AGENTS.md`, package-level README, contribution guide, or module-specific documentation. Use this precedence when requirements disagree:

1. Applicable law, platform policy, and explicit user-approved security/privacy constraints.
2. Root and nearer agent instructions, as applicable; more-specific instructions may add detail but cannot override higher-priority safety constraints.
3. Approved product requirements and architecture decisions.
4. Relevant design, database, security, code-style, and testing standards.
5. Existing code and established patterns, provided they do not violate requirements above.

Do not contradict the core documents silently. State the exact conflict and its impact in the task response or implementation plan. If the conflict blocks a material decision, stop that part and ask for clarification rather than guessing. For minor, reversible choices, use the most consistent documented convention and record the assumption.

## 3. General Rules

1. **Understand before editing.** Inspect the relevant source files, call sites, tests, configuration, and recent local patterns before changing code.
2. **Reuse established building blocks.** Prefer existing widgets, design tokens, services, repositories, validators, provider adapters, error types, and utilities over parallel implementations.
3. **Respect boundaries.** Keep presentation, domain/business logic, persistence, external providers, and orchestration in their documented layers. Do not bypass an abstraction for convenience.
4. **Follow the design system.** Use semantic tokens and shared components. Do not introduce arbitrary colors, typography, spacing, animation, or one-off UI patterns when a documented pattern exists.
5. **Follow the architecture.** Avoid circular dependencies, cross-layer shortcuts, unrelated refactors, and premature microservices.
6. **Follow database conventions.** Use migrations for schema changes, explicit constraints, safe transactions, and the documented data lifecycle. Never alter production data manually as a substitute for a migration.
7. **Follow security and privacy requirements.** Enforce authorization on the server, isolate users' data, validate untrusted inputs, minimize collection, and avoid logging sensitive content. Client-side checks are not authorization controls.
8. **Protect secrets.** Do not add API keys, tokens, private certificates, service-account files, passwords, or production data to source control, logs, examples, screenshots, or test fixtures.
9. **Do not invent requirements.** Implement documented behavior and acceptance criteria. If a requirement is unclear and the choice materially affects behavior, privacy, cost, or compatibility, identify the ambiguity.
10. **Keep dependencies lean.** Prefer the standard library and existing packages. Before adding a dependency, verify that it is needed, maintained, compatible with the supported runtime, and acceptable under security/license policies.
11. **Keep changes scoped.** Do not reformat or rewrite unrelated files. Preserve existing behavior unless the task explicitly changes it.
12. **Fail safely.** Handle timeouts, provider errors, invalid outputs, retries, cancellation, and partial failure explicitly. Avoid exposing internal exceptions or sensitive details to users.
13. **Make behavior observable.** Use structured, privacy-safe logs, metrics, and traces consistent with project conventions. Never emit secrets, authentication headers, raw payment data, or private conversation/memory content into general logs.
14. **Do not claim validation that did not happen.** Report commands run, results, skipped checks, and blockers accurately.

## 4. Planning Before Non-Trivial Work

Before implementation, perform the following steps. For a trivial, isolated change, use judgment and keep planning proportionate.

1. Read the relevant documentation and any applicable local agent instructions.
2. Inspect the repository structure and the existing implementation of the feature.
3. Identify expected behavior and acceptance criteria from the PRD or issue.
4. Identify affected modules, files, interfaces, and dependency boundaries.
5. Identify API, database, event, configuration, prompt, or model-contract changes.
6. Identify privacy, security, abuse, cost, performance, localization, and backward-compatibility risks.
7. Define the tests and validation commands needed to prove the change works.
8. Produce a concise implementation plan before making substantial edits.

Do not spend time producing a lengthy plan for a one-line, low-risk fix. Do not begin a broad rewrite while the scope is unresolved.

## 5. Implementation Rules

### 5.1 General implementation

- Make the smallest coherent change that satisfies the requirement.
- Follow patterns already used by neighboring modules unless they conflict with documented standards.
- Keep functions and classes focused; name them for intent rather than implementation trivia.
- Prefer explicit data contracts and typed models over loosely structured dictionaries or unvalidated JSON.
- Validate data at trust boundaries. Do not duplicate validation everywhere; put shared invariants in the appropriate domain or service layer.
- Use configuration for environment-specific settings. Provide safe defaults and fail clearly for missing required production settings.
- Maintain backward compatibility for public APIs and persisted data unless a breaking change is approved and coordinated.
- Avoid hidden side effects in constructors, imports, getters, and UI build methods.
- Make retries bounded and safe. Use idempotency keys for operations that could otherwise double-charge, duplicate messages, or repeat external side effects.
- Never swallow exceptions silently. Translate them at appropriate boundaries and preserve enough context for privacy-safe diagnosis.

### 5.2 Flutter / Dart

- Follow `docs/CODE_STYLE.md`, `analysis_options.yaml`, and the repository's pinned Dart/Flutter versions.
- Use shared design tokens and components; support system text scaling, accessibility labels, localization, and reduced-motion settings where applicable.
- Keep widgets presentational where practical and move business rules into the documented state/domain layer.
- Avoid network, database, or expensive AI work directly inside widget build methods.
- Represent loading, empty, success, error, retry, and offline states intentionally.
- Dispose controllers, streams, subscriptions, and focus resources correctly; guard against updates after disposal.
- Do not store long-lived secrets in plain preferences or embed server-side provider credentials in the app.
- Treat every client-provided user ID, entitlement, price, credit balance, and permission as untrusted. The backend is authoritative.

### 5.3 Python / FastAPI

- Follow `docs/CODE_STYLE.md`, the existing formatter/linter/type-checker configuration, and the supported Python version.
- Keep route handlers thin. Put business rules in services/domain modules and persistence behind repository/data-access conventions where documented.
- Add request/response types and validation for public interfaces. Return stable, documented error shapes without stack traces or secrets.
- Use async APIs correctly; do not block the event loop with synchronous network, filesystem, database, or model operations.
- Apply explicit timeouts, bounded retries, cancellation behavior, and concurrency limits to external calls.
- Verify authentication and authorization at every protected server boundary. Do not rely on UI visibility or client-side route guards.
- Use parameterized SQL or safe ORM/query APIs. Never interpolate untrusted input into SQL, shell commands, or provider configuration.
- Keep dependencies injected and tests deterministic; avoid hidden calls to live providers during unit tests.

### 5.4 AI prompts, models, and memory

- Treat system prompts, persona definitions, safety policies, and model routing as versioned assets governed by the architecture—not ad hoc strings scattered through application code.
- Separate trusted instructions from untrusted user text, retrieved memory, uploaded content, and tool output. Retrieved content must never be promoted to system-level instructions.
- Validate model outputs against the expected schema before using them for state changes, tool calls, memory writes, billing, or user-visible media.
- Treat model-generated summaries and memory candidates as untrusted suggestions. Apply documented extraction, validation, provenance, consent, and deletion rules before persisting them.
- Enforce story/roleplay isolation and per-user memory ownership. Do not leak one conversation's fictional state into another context unless the product explicitly supports it.
- Use the provider adapter and routing configuration. Do not bind core domain logic to a single provider response format.
- Add regression evaluations when changing prompts, model settings, retrieval, moderation, language handling, or tool behavior.
- Do not assume a model refusal, generated text, or model classifier alone is a sufficient security boundary for sensitive actions.

### 5.5 Database and migrations

- Create a versioned migration for every schema change. Review both upgrade and rollback/recovery implications.
- Add appropriate primary keys, foreign keys, uniqueness rules, check constraints, and indexes based on documented invariants and query paths.
- Make migrations safe for deployed data and the expected application rollout sequence. Prefer expand–migrate–contract for breaking changes.
- Avoid destructive migrations or mass data rewrites without an approved plan, backups, verification queries, and recovery steps.
- Use transactions for coupled state changes, particularly entitlements, credit reservations, ledger entries, and memory lifecycle operations.
- Never trust a client-supplied ownership identifier; derive the authorized user scope from verified server-side identity.
- Test migrations against a clean database and a representative prior schema version where feasible.

### 5.6 Security and privacy

- Apply least privilege to users, service accounts, database roles, storage access, model tools, and CI credentials.
- Store media in private object storage and issue scoped, short-lived access URLs where the documented design requires them.
- Validate file type, size, and content as appropriate; never trust filenames or client-provided MIME types alone.
- Redact personal data and conversation content from logs by default. Use synthetic fixtures in tests and development documentation.
- Ensure account deletion and retention jobs cover primary records, derived memory, embeddings, media, caches, analytics identifiers, and provider-side data as required by policy.
- Do not weaken authentication, authorization, moderation, age controls, rate limits, or audit behavior to make a test pass. Use safe test doubles and test-only configuration.
- When a change introduces a new data category or third-party processor, review consent, minimization, retention, deletion, and disclosure requirements before merging.

## 6. Testing and Validation

Every behavior change requires proportionate validation. Use the specific commands configured in the repository; do not invent commands if project scripts already define them.

1. **Tests:** Run focused tests first, then relevant integration or full-suite tests.
2. **Lint and formatting:** Run the configured formatter and linter, or verify that formatting checks pass.
3. **Type checking and static analysis:** Run the configured Dart analyzer, Python type checker, and other applicable analyzers.
4. **Build:** Build the affected target (and production configuration when relevant).
5. **Security checks:** Run the relevant secret, dependency, static security, authorization, and input-validation checks for the change.
6. **Database checks:** Validate migrations and important transaction/concurrency invariants when the schema or persistence path changes.
7. **AI evaluations:** Run relevant regression tests for prompts, memory, model output, language quality, safety, or tool use when the AI behavior changes.
8. **Diff review:** Inspect the final diff for debug code, accidental files, generated artifacts, secrets, unrelated formatting, and missing documentation.

If a check cannot run due to unavailable credentials, infrastructure, model endpoints, tools, or time, record it as **not run** with the reason. Do not replace this with a claim that tests pass.

### Minimum regression considerations

Depending on the affected area, verify:

- Authentication, authorization, and cross-user data isolation.
- Conversation ordering, duplicate requests, streaming cancellation, and retry behavior.
- Memory provenance, user correction, deletion, retrieval boundaries, and story isolation.
- Structured model output validation, prompt-injection resistance, provider timeout/failure, and fallback behavior.
- Image/voice job lifecycle, private media access, moderation, and failed-job recovery.
- Payment webhook verification, idempotency, concurrent credit spending, refunds, and ledger reconciliation.
- Localization, text scaling, accessibility, offline/error states, and Android lifecycle behavior.

See `docs/TESTING.md` for the complete test strategy, identifiers, tooling, and release thresholds.

## 7. Documentation Updates

Update relevant documentation whenever an implementation changes:

- User-visible behavior, user stories, or business rules → `docs/PRD.md`.
- UI patterns, tokens, components, interaction states, or accessibility behavior → `docs/DESIGN_SYSTEM.md`.
- Module boundaries, service responsibilities, integrations, request flows, or deployment → `docs/ARCHITECTURE.md`.
- Tables, columns, constraints, indexes, migrations, retention, or deletion behavior → `docs/DATABASE.md`.
- Threat mitigations, permissions, data collection, processors, security controls, or incident operations → `docs/SECURITY.md`.
- Coding conventions, project structure, tooling, or reusable implementation patterns → `docs/CODE_STYLE.md`.
- Test strategy, fixtures, automation, evaluation criteria, or release gates → `docs/TESTING.md`.

Update API schemas, OpenAPI examples, environment-variable templates, runbooks, and module READMEs when applicable. Keep docs specific and actionable. Never put real secrets, personal data, production conversation samples, or credentials in documentation.

Do not create a second conflicting source of truth. Prefer updating the existing canonical document over repeating the same policy in multiple places. If implementation has intentionally changed a documented decision, update the authoritative documentation in the same change and call out the change.

## 8. Conflict and Ambiguity Handling

- Do not guess when requirements materially conflict.
- Report the documents or code paths in conflict, the exact differing requirements, and the impact on user behavior, schema, API compatibility, security, or cost.
- If safe to do so, continue independent work while leaving the blocked decision untouched.
- Ask for clarification when an unresolved choice is irreversible, externally visible, security-sensitive, privacy-sensitive, materially costly, or changes a public contract.
- For a small and reversible implementation detail not covered by the docs, follow the closest established pattern, state the assumption in the handoff, and avoid turning the assumption into a new product requirement.
- Never silently reduce test coverage, relax a security control, delete user data, add a paid dependency, or change pricing/entitlement semantics to resolve a conflict.

## 9. Completion Criteria

A task is complete only when all applicable criteria are met:

- [ ] Documented requirements and acceptance criteria are satisfied.
- [ ] The implementation follows architecture, design, database, security, and code-style standards.
- [ ] Relevant tests are added or updated and have been run where feasible.
- [ ] Linting, formatting, type checking, static analysis, and the affected build pass where configured and feasible.
- [ ] Security, privacy, authorization, and data-isolation implications have been reviewed.
- [ ] Schema/API/configuration changes are compatible, migrated, and documented.
- [ ] Relevant AI evaluations have been run for prompt, model, memory, retrieval, or tool behavior changes.
- [ ] Documentation has been updated where behavior or implementation decisions changed.
- [ ] The final diff contains no secrets, accidental artifacts, debug leftovers, or unrelated changes.
- [ ] Any checks not run, known limitations, assumptions, or remaining risks are clearly reported.
- [ ] The handoff summarizes what changed, important decisions, files touched, validation performed, and any follow-up required.

Do not claim completion if a material acceptance criterion remains unverified. Clearly label partial work and state what is outstanding.

## 10. Standard Workflow for Every Task

Use this workflow as the default operating procedure:

1. **Context:** Find and read the relevant docs and local instructions.
2. **Inspect:** Trace the existing feature and its dependencies before editing.
3. **Plan:** Define the smallest safe change, files affected, risks, and tests.
4. **Implement:** Follow existing patterns and keep the diff focused.
5. **Validate:** Run tests, static checks, build steps, and domain-specific evaluations.
6. **Review:** Inspect the diff and verify security/privacy boundaries and backward compatibility.
7. **Document:** Update the canonical docs and migrations/contracts where required.
8. **Report:** State the changes, validation results, skipped checks, assumptions, and known risks accurately.

These instructions apply to code generation, refactoring, bug fixes, dependency updates, schema changes, prompt/model changes, infrastructure changes, and automated edits.
