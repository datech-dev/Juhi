# Juhi — Complete Testing Strategy and Quality Assurance Specification

**Document status:** Engineering standard and implementation blueprint  
**Product:** Juhi AI Companion (Android-first, Flutter client, Python/FastAPI backend)  
**Audience:** Mobile engineers, backend engineers, AI/ML engineers, QA, security, product, operations, and release owners  
**Related documents:** `Juhi_AI_Companion_PRD.md`, `Juhi_Design_System.md`, `architecture.md`, `database.md`, `security.md`, and `code_style.md`

---

## 1. Purpose

This document defines how the Juhi team verifies functional correctness, AI quality, safety, privacy, reliability, performance, usability, and release readiness from local development through production. It specifies the test levels, ownership, environments, sample cases, fixtures, automation, quality gates, and operational validation required to release Juhi responsibly.

Testing is not a final phase that begins after implementation. Testability must be designed into APIs, database transactions, AI orchestration, memory lifecycle, provider adapters, media jobs, payments, and the mobile interface from the start.

### 1.1 Outcomes

Juhi's testing programme must establish that:

1. Users can register, authenticate, create a companion profile, converse, and recover from expected failures.
2. Conversations are isolated by user and conversation; users cannot read or change another user's data.
3. Memory improves continuity while remaining inspectable, correctable, revocable, and deletable by the user.
4. The companion can converse in English, Hindi, Tamil, Hinglish, and Tanglish, including code-switching, without requiring the user to stay in one language.
5. Persona and relationship settings are stable within their intended scope and do not override safety, privacy, or user preferences.
6. Model-provider errors, timeouts, malformed responses, throttling, and outages fail gracefully.
7. Image and audio jobs are idempotent, observable, cancellable when supported, and safe under retries.
8. Purchases and credits remain correct under retries, concurrency, webhook duplication, and failure recovery.
9. Private data, prompts, tokens, media URLs, and sensitive conversation content are not exposed through logs, analytics, errors, or access-control defects.
10. The application meets agreed usability, accessibility, performance, cost, and operational objectives before release.

### 1.2 Normative wording

- **MUST**: required for release or required to preserve a correctness/security invariant.
- **SHOULD**: expected unless an owner documents why it is not appropriate.
- **MAY**: optional, generally dependent on scope or maturity.
- **P0**: release-blocking for external beta unless a documented, time-limited exception is approved by the security/release owner.
- **P1**: required before paid general availability unless explicitly risk-accepted.
- **P2**: maturity or scale capability that can be scheduled after launch.

A test marked “pass” means the expected behavior was demonstrated with recorded evidence, not that the feature merely appeared to work once on a developer's device.

---

## 2. Product-specific testing principles

### 2.1 Test the experience and the system

Juhi is both a software system and an ongoing conversational experience. The team must test ordinary user journeys and deeper properties such as continuity, trust, data ownership, personality stability, and emotional safety. A correct HTTP response does not prove that a conversation is helpful, that the memory is accurate, or that billing is correct.

### 2.2 Deterministic core; probabilistic AI boundaries

Keep deterministic business rules outside the LLM wherever possible. Authentication, permissions, credit balances, purchases, age gates, memory deletion, tool authorization, rate limits, and job-state transitions MUST be deterministic and unit/integration tested. AI-generated language and image/audio outputs require evaluation using a mix of deterministic assertions, model-assisted scoring, and human review.

### 2.3 Separate test types

Do not rely on one end-to-end test suite to find all defects. Use:

- Static checks to catch formatting, type, dependency, and simple security errors early.
- Unit tests for pure logic and small components.
- Integration tests for database, object storage adapters, authentication verification, and provider clients.
- Contract tests for API schemas, event payloads, payment/webhook events, and AI provider adapters.
- AI evaluations for quality, safety, multilingual behavior, memory, and prompt regressions.
- End-to-end tests for the journeys users actually perform.
- Performance, reliability, accessibility, privacy, and security tests for properties that ordinary functional tests cannot establish.

### 2.4 Protect real users and real data

Automated tests MUST NOT use production personal data, live payment instruments, actual users' private chats, or production credentials. Use synthetic accounts, synthetic conversation corpora, provider mocks, sandbox payment events, and isolated environments. Any approved exception requires documented authorization, data minimization, and a deletion plan.

### 2.5 Make quality measurable

A release must have a defined test result, known unresolved defects, evaluated AI behavior, migration evidence, a rollback/mitigation plan, and a named release owner. “QA tested” is not sufficient evidence.

---

## 3. Scope and system under test

Testing covers the Juhi product and its direct integrations.

### 3.1 Mobile application

- Flutter/Dart application and feature modules.
- Authentication, onboarding, companion configuration, chat, conversation history, memory controls, settings, purchases, credit displays, media galleries, image generation, voice notes, and notifications where implemented.
- Client-side state, caching, persistence, app lifecycle, permissions, deep links, accessibility, localization, and recovery after network loss or application restart.

### 3.2 Backend

- FastAPI application and modular domain services.
- Authentication and authorization boundaries.
- Conversation and message persistence.
- Context compilation, memory retrieval and mutation, persona versioning, policy enforcement, provider routing, tools, streaming, and response validation.
- Media-generation job orchestration, object-storage access, notifications, subscription and credit accounting, feedback, user-data export/deletion, analytics, audit events, and observability.

### 3.3 Data and infrastructure

- PostgreSQL/Cloud SQL, `pgvector` if enabled, migrations, constraints, transactions, backups, restoration, connection management, tenant isolation, and data-retention jobs.
- Private object storage for generated images/audio and upload inputs.
- Task queue or managed job runner, scheduled jobs, secrets, CI/CD, monitoring, alerting, and environment configuration.

### 3.4 External dependencies

- Firebase Authentication and App Check where configured.
- LLM, embedding, moderation, image-generation, and speech providers.
- Payment platform and store billing integration, if applicable.
- Push-notification service, analytics provider, and observability vendor.

External providers are outside Juhi's direct code ownership, but Juhi MUST test its integration contracts, failure handling, data-sharing behavior, cost limits, and provider failover strategy.

### 3.5 Out of scope unless a release explicitly includes them

- Native real-time audio calls before that capability enters a planned milestone.
- Features not yet implemented or available behind disabled feature flags.
- Vendor internal infrastructure. Test observable vendor contracts and Juhi's response to vendor failures instead.

---

## 4. Quality ownership and responsibilities

| Role | Responsibility |
|---|---|
| Feature engineer | Unit and integration tests for changed code; local checks; clear testability and diagnostics. |
| Mobile engineer | Widget, state, navigation, accessibility, offline, lifecycle, and device tests. |
| Backend engineer | Domain, API, authorization, persistence, transaction, contract, and migration tests. |
| AI/ML engineer | Reproducible evaluation datasets, quality and safety metrics, provider/model regression evaluation, memory evaluations. |
| QA owner | Cross-feature scenarios, exploratory testing, release evidence, defect triage, device/browser matrix. |
| Security owner | Security test plan, threat-driven tests, penetration-test coordination, risk acceptance. |
| Product owner | Acceptance criteria, severity decisions, human-reviewed AI quality, launch thresholds. |
| Operations/release owner | Performance readiness, alerts, backup/restore evidence, deployment/rollback, incident runbooks. |

Small teams can combine roles, but each release MUST have named owners for quality approval, security approval, and production rollout. The person implementing a critical security-sensitive change SHOULD NOT be the only person who approves the change.

---

## 5. Testing levels and test pyramid

### 5.1 Recommended mix

Use the test pyramid as a directional guide, not a rigid percentage target:

1. **Static analysis and pure unit tests**: broad, fast, isolated; run on every change.
2. **Component and integration tests**: database, API, auth, queue, storage, and provider-adapter contracts; run on every pull request where practical.
3. **AI evaluation suites**: quick smoke suite on every prompt/model/orchestration change; broader suite on a scheduled cadence and before significant rollout.
4. **End-to-end tests**: small set of critical journeys; run on every release candidate.
5. **Performance, security, accessibility and resilience tests**: risk-based, scheduled and required at release gates.
6. **Human evaluation and exploratory testing**: essential for conversational quality and interactions difficult to grade automatically.

Tests SHOULD be deterministic, fast, isolated, diagnosable, and cheap. A flaky test MUST be investigated and either fixed, quarantined with an owner and deadline, or removed only with a documented alternative; it must not be silently ignored.

### 5.2 Test classification labels

Use labels/tags consistently, for example:

- `unit`, `integration`, `contract`, `e2e`
- `ai-smoke`, `ai-regression`, `ai-safety`, `ai-memory`, `ai-multilingual`
- `security`, `privacy`, `billing`, `media`, `migration`
- `performance`, `load`, `soak`, `resilience`, `accessibility`, `localization`
- `p0`, `p1`, `p2`

For pytest, use markers. For Flutter, use test file naming and CI jobs. For evaluation cases, include structured metadata in the dataset manifest.

---

## 6. Environments and configuration

### 6.1 Environment model

Maintain separate local, CI, development, staging/pre-production, and production environments. Avoid shared mutable data or shared credentials between environments.

| Environment | Purpose | Data and provider rules |
|---|---|---|
| Local | Developer feedback and debugging | Synthetic data; mocked providers by default; no production secrets. |
| CI | Automated validation | Ephemeral or isolated dependencies, seeded synthetic fixtures, deterministic provider fakes. |
| Development | Team integration | Non-production resources and low-cost quotas; synthetic or explicitly approved test data only. |
| Staging | Release candidate verification | Production-like configuration, separate database/storage/project, payment sandbox, provider test keys or controlled spending budget. |
| Production | Real user traffic | Real data, least privilege, monitored access, restricted test activities, no destructive QA. |

### 6.2 Required configuration separation

- Different project/account identifiers, database instances or schemas, buckets, secrets, callback URLs, and API keys for each environment.
- Explicit environment validation at startup; fail fast when a production process receives development configuration or vice versa.
- Separate payment products and webhook secrets per environment.
- AI provider spend limits for development and staging.
- Explicit test-only feature flags; test hooks MUST NOT be enabled in production.
- No test endpoint may allow users to impersonate a different identity or bypass billing/authorization.

### 6.3 Configuration tests

Verify that:

- Missing required production secrets prevent startup.
- Invalid URLs, unknown model IDs, invalid cost ceilings, and malformed timeouts are rejected.
- Production cannot use local provider mocks unintentionally.
- Staging uses the correct payment sandbox and callback domains.
- Secure cookies, CORS, trusted hosts, upload limits, TLS, logging levels, and error detail follow the environment profile.
- Feature flags default to safe values when the flag service is unavailable.

---

## 7. Test tooling and automation

Use tools already standardized by the repository; the following is a recommended stack rather than a mandate to adopt every package.

### 7.1 Flutter/Dart

- `dart format` for formatting.
- `flutter analyze` and configured lints for static analysis.
- `flutter test` for unit, widget, and supported integration tests.
- Flutter integration tests or an equivalent Android device-farm solution for high-value end-to-end flows.
- Mock/fake implementations for repositories, clocks, IDs, AI streaming, payment status, notifications, and network responses.
- Golden tests selectively for stable design-system components; avoid excessive snapshots of volatile AI text.

### 7.2 Python/FastAPI

- `pytest` for unit and integration testing.
- `pytest-asyncio` (or the repository's selected async plugin) for async services.
- `httpx` TestClient/AsyncClient patterns for API tests.
- Ruff for linting/formatting and the repository-selected type checker.
- Coverage tooling such as `coverage.py`/`pytest-cov`.
- Property-based testing such as Hypothesis for ledger invariants, parsers, and data transformations where useful.
- A real PostgreSQL test instance or disposable container for integration tests that depend on Postgres semantics, locks, constraints, or `pgvector`.

### 7.3 Database and infrastructure

- Migration framework already selected by the repository (e.g. Alembic): upgrade from an empty DB and previous supported release; check schema drift.
- SQL lint/format tooling where practical.
- Infrastructure-as-code validation, policy scanning, and plan review.
- Load testing with a tool such as k6, Locust, or an equivalent controlled harness.
- Dependency, secret, container, and static security scanning integrated into CI.

### 7.4 AI evaluation harness

Implement a versioned evaluation runner that records:

- Evaluation set ID and version.
- Prompt package/version and hash.
- Model/provider ID and relevant inference parameters.
- Orchestrator, retrieval, memory, and safety-policy versions.
- Exact synthetic input and expected assertions.
- Raw model output in a restricted evaluation store, where permitted; otherwise store a privacy-safe artifact or hash.
- Automatic scores, human review, latency, tokens, retries, cost estimate, and pass/fail reason.

Never place real user conversations in a general-purpose evaluation set without approved legal basis, consent/authorization where required, de-identification, access controls, retention limits, and a documented evaluation purpose.

---

## 8. Repository test organization

Keep tests discoverable and close to the layer they validate without coupling production code to test code. A recommended structure:

```text
juhi/
  apps/
    mobile/
      lib/
      test/
        unit/
        widgets/
        integration/
        golden/
        fixtures/
  services/
    api/
      app/
      tests/
        unit/
        integration/
        contract/
        security/
        fixtures/
  ai/
    prompts/
    evals/
      datasets/
      cases/
      metrics/
      reports/
  database/
    migrations/
    tests/
  tests/
    e2e/
    performance/
    security/
    resilience/
  scripts/
  docs/
```

The actual source directories MUST follow the repository layout documented in `architecture.md`; this example describes separation of test concerns, not a requirement to reorganize an established repository solely to match the illustration.

### 8.1 Naming

- Python: `test_<subject>.py`; test functions `test_<behavior>_when_<condition>` where that adds clarity.
- Flutter: `<feature>_test.dart`; test descriptions state an observable behavior.
- AI evaluation cases: stable IDs such as `MEM-001`, `SAFE-012`, and `LANG-023`.
- End-to-end scenarios: `E2E-AUTH-001`, `E2E-CHAT-003`, `E2E-BILL-002`.
- Security cases: `SEC-AUTHZ-001`, `SEC-MEM-004`, `SEC-LLM-003`.
- Use stable IDs so a case can be referenced in defects and release reports.

---

## 9. Requirement traceability and test case design

### 9.1 Traceability

Every P0/P1 PRD acceptance criterion MUST map to one or more automated or manually evidenced tests. The test case should identify:

- Case ID and title.
- Requirement/feature ID.
- Priority and risk.
- Preconditions and test data.
- Steps or input fixture.
- Expected outcome, including negative cases.
- Automation status and test owner.
- Environment and evidence location.

Maintain the mapping in a test management system or version-controlled file, depending on team size. Do not depend only on issue descriptions that become difficult to search.

### 9.2 Test case example

```yaml
id: SEC-AUTHZ-001
feature: conversations
priority: P0
type: integration
requirement: A user can read only their own conversations
preconditions:
  - account_a owns conversation_a
  - account_b owns conversation_b
steps:
  - request conversation_a with account_a token
  - request conversation_a with account_b token
expected:
  - first request returns the authorized resource
  - second request returns the standard not-found or forbidden response
  - no message content or ownership metadata leaks in the second response
owner: backend
```

The exact HTTP code may be `404` or `403` according to the API contract. The non-negotiable property is that unauthorized data is not disclosed or changed.

---

## 10. Static analysis and pre-commit gates

Static checks should catch low-cost defects before tests execute.

### 10.1 Mobile gate

For every pull request that changes mobile code:

1. Install the pinned Flutter/Dart toolchain.
2. Resolve packages from lockfiles.
3. Run formatting checks without rewriting the branch implicitly.
4. Run static analysis/lints.
5. Run the impacted unit/widget tests.
6. Run secret/dependency checks as configured.
7. Fail on new errors; baseline existing warnings explicitly rather than silently tolerating new ones.

Illustrative commands:

```bash
flutter pub get
 dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test
```

Adjust the working directory and whitespace to match the actual repository scripts. Pin SDK versions to avoid unexplained CI changes.

### 10.2 Backend gate

```bash
ruff check .
ruff format --check .
# Example; use the repository's selected type checker:
pyright
pytest -m "not e2e and not load"
```

Run schema checks and dependency/security scans in dedicated jobs. Do not place live model calls or payment provider charges in the default unit-test command.

### 10.3 Static checks for shared artifacts

- Validate OpenAPI contracts and generated client consistency.
- Parse and lint SQL migrations.
- Validate JSON/YAML configuration and prompt package manifests.
- Scan for secrets, unsafe dependency versions, and license-policy issues according to company policy.
- Confirm that generated build artifacts do not accidentally include `.env` files, API keys, private certificates, or test bypasses.

---

## 11. Unit testing standards

### 11.1 What belongs in unit tests

Unit tests SHOULD cover deterministic code such as:

- Conversation sequence allocation logic where abstracted from DB locking.
- Request validators and message serialization.
- Prompt/context assembly with fixed input records.
- Memory candidate filtering and confidence thresholds.
- Contradiction/staleness rules, explicit memory correction, and priority ordering.
- Persona configuration resolution and safety override precedence.
- Model routing based on configured policy and budget.
- Provider error normalization and retry classification.
- Cost estimate calculations and usage normalization.
- Credit reservation and ledger domain rules independent of transaction implementation.
- Generation job state transition validation.
- Entitlement and access-policy decisions.
- Localization mapping and presentation-state transformation.
- Error mapping and redaction functions.

### 11.2 Unit test design

- Each test MUST have a clear assertion on observable behavior.
- Avoid asserting implementation details such as private method call counts unless they enforce a meaningful contract.
- Use fixed clocks and deterministic ID generators for time/ordering tests.
- Inject random-number sources if randomness affects behavior.
- Test boundary conditions: empty strings, maximum lengths, malformed Unicode, missing optional fields, timeouts, overflow, and invalid state transitions.
- Avoid live network, real cloud services, and actual LLM provider calls in ordinary unit tests.
- Keep fixtures small and representative; do not use a “god fixture” that conceals required setup.

### 11.3 Sample test inventory

| ID | Area | Scenario | Expected result |
|---|---|---|---|
| UNIT-CONV-001 | Conversations | Empty user message | Validation error; no persisted user/assistant turn. |
| UNIT-CONV-002 | Conversations | Message at maximum accepted length | Accepted if within contract. |
| UNIT-MEM-001 | Memory | Candidate contains low-confidence transient state | Not promoted to durable memory. |
| UNIT-MEM-002 | Memory | User explicitly corrects a preference | Prior memory superseded or marked invalid per policy. |
| UNIT-MEM-003 | Memory | User says “do not remember this” | No durable memory candidate is created from that content. |
| UNIT-PER-001 | Persona | Persona setting conflicts with safety rule | Safety rule remains authoritative. |
| UNIT-MODEL-001 | Router | Primary provider temporarily unavailable | Correct configured fallback or controlled failure. |
| UNIT-BILL-001 | Credits | Reservation exceeds available balance | Rejected without negative balance. |
| UNIT-BILL-002 | Credits | Duplicate idempotency key | Same operation result; no double debit. |
| UNIT-JOB-001 | Media job | Attempt invalid terminal transition | Rejected; state unchanged. |
| UNIT-SEC-001 | Redaction | Authorization token occurs in exception context | Secret is absent from sanitized log output. |

---

## 12. Database and transaction testing

Use a real PostgreSQL engine for database integration tests. An in-memory substitute is not sufficient for verifying Postgres-specific constraints, JSONB behavior, lock behavior, isolation, extensions, and query plans.

### 12.1 Migration testing

Every schema change MUST be tested for:

1. Fresh install: apply all migrations to an empty disposable database.
2. Upgrade path: upgrade from the latest supported schema and any specifically supported previous production schema.
3. Repeated deployment: migration runner behaves safely when a deployment is retried.
4. Data preservation: migration preserves and transforms relevant existing rows correctly.
5. Constraints: foreign keys, unique constraints, checks, indexes, and nullability are as intended.
6. Roll-forward/rollback plan: a safe recovery strategy is documented; destructive downgrades need explicit review.
7. Lock and runtime impact: large-table changes are assessed for locks, table rewrites, index creation time, and application compatibility.
8. Dual-version deploy compatibility: use expand/contract migrations where app and schema versions overlap during rollout.

### 12.2 Transaction and concurrency tests

Must cover:

- Two requests attempting to allocate a message sequence in the same conversation.
- Two image-generation requests trying to reserve the final available credits.
- Duplicate payment or purchase webhook delivery.
- Concurrent cancellation and completion of the same media job.
- Retrying a transaction after a serialization/deadlock failure where applicable.
- User deletion concurrently with new writes or background processing.
- Entitlement updates while a protected request is in flight, according to the product's defined authorization snapshot policy.

Assertions MUST check final database state and ledger state, not only the immediate API response.

### 12.3 Data invariants

Examples of required invariants:

- A message belongs to exactly one conversation, and every conversation has exactly one owner according to the schema.
- A user cannot own or access rows solely by guessing an identifier.
- Credit balance cannot become negative unless an explicitly documented product rule permits a separate debt state; default behavior forbids it.
- Every committed credit debit/credit has an immutable ledger entry and an associated business reference/idempotency key.
- A settled reservation is not settled twice.
- A deleted user's data cannot be resurrected by delayed jobs or retries.
- Memory records have owner scope, provenance, status, and an explicit lifecycle.
- Private media records do not create public object access by default.
- Job-state transitions follow a defined state machine.

### 12.4 Index and query tests

- Use realistic synthetic row counts for critical query plan checks.
- Capture baseline `EXPLAIN (ANALYZE, BUFFERS)` for expensive conversation and memory retrieval queries in non-production test environments.
- Verify indexes serve common owner-scoped queries and ordering patterns.
- Run vector retrieval tests with representative corpus size and appropriate similarity metrics; tune thresholds using measured evaluations rather than guesses.
- Do not assert an exact planner node for every query because plans can vary by statistics/version; assert latency budgets and investigate severe regressions.

---

## 13. API, integration and contract testing

### 13.1 API behavior

For every endpoint test:

- Valid request and expected response schema.
- Missing, expired, malformed, and wrong-audience authentication token.
- Unauthenticated request to a protected endpoint.
- Authenticated user attempting to access another user's resource.
- Missing required field, invalid enum, invalid type, oversized payload, and malformed content.
- Rate limit, idempotent retry, and concurrency behavior where relevant.
- Database/provider timeout and safe standard error response.
- Pagination correctness and owner scoping.
- No private stack trace, prompt, credential, provider key, or other user's content leaks in errors.

### 13.2 Schema contract tests

- Validate request/response JSON against the OpenAPI schema.
- Check generated mobile API client compatibility after contract changes.
- Reject undocumented breaking changes unless a versioned migration plan is accepted.
- Ensure optional vs required fields and nullable semantics are represented consistently across Python, API schema, and Dart.
- Validate error envelopes, streaming events, timestamps, and enum values.

### 13.3 Streaming contract tests

For streaming chat:

- Event ordering is legal and documented.
- Partial text is rendered without duplicate concatenation.
- A successful stream has exactly one terminal completion event or equivalent terminal state.
- Provider error, client disconnect, server cancellation, token timeout, and content-blocking paths terminate cleanly.
- Reconnect or retry does not create duplicate persisted assistant responses.
- Partial text is not mistakenly treated as a completed, billable answer if the product's accounting policy requires completed generation.
- Client receives a stable correlation/turn ID that support can use without revealing private content.

### 13.4 Provider adapter contract tests

Use recorded, sanitized fixtures or fake servers to cover:

- Expected success payload.
- Missing or renamed field.
- Empty content.
- Malformed JSON/structured output.
- Provider rate limit, quota exhaustion, authentication failure, timeout and server error.
- Streaming interruption.
- Unsupported model ID.
- Usage/token metadata missing or inconsistent.
- Safety refusal or filtered output.
- Image/audio output metadata mismatch.

Provider-specific behavior MUST be translated into stable Juhi domain outcomes instead of leaking provider SDK types into domain services.

---

## 14. Authentication and authorization tests

Authentication tests are P0 because nearly every feature handles private personal data.

### 14.1 Required cases

- Valid token resolves to the correct immutable external identity and Juhi user.
- Invalid signature, expired token, incorrect issuer, incorrect audience, and unexpected signing key are rejected.
- A client cannot choose an arbitrary user ID in the request body to act as another user.
- Every user-owned object endpoint checks ownership or an explicit privileged policy.
- List, search, export, and pagination endpoints filter by the caller's authorized scope.
- Nested objects (messages, memory records, media, reports, jobs) cannot be accessed through a permitted parent ID owned by another user.
- Administrative support actions require separate privileged authorization and are audited.
- Refresh/logout/session-revocation semantics match the chosen authentication flow.
- App Check or other anti-abuse signals are verified where configured, but are not treated as a replacement for authentication and authorization.

### 14.2 Cross-user matrix

Create users A and B with separate conversations, memory records, media assets, jobs, and billing records. For every endpoint that accepts a resource identifier, test that B cannot read, update, delete, export, cancel, or trigger an operation against A's object. Include sequential IDs, UUIDs, stale IDs, nested routes, bulk APIs, and signed asset URLs.

The expected result is no unauthorized content disclosure, mutation, or charge. Use the standard 404/403 policy selected in the API contract.

---

## 15. End-to-end testing

E2E tests validate a small number of high-value journeys across the mobile app, backend, database, and external-service boundaries. Keep the suite stable and use provider stubs for most tests. Run a smaller number of staging tests against controlled real integrations.

### 15.1 Critical E2E scenarios

| ID | Journey | Expected outcome | Priority |
|---|---|---|---|
| E2E-AUTH-001 | New user signs in and completes onboarding | A user and default profile are created once; consent is recorded where needed. | P0 |
| E2E-CHAT-001 | User sends a text and receives a response | User turn and assistant result are correlated and persisted correctly. | P0 |
| E2E-CHAT-002 | User changes language mid-conversation | Assistant recognizes and responds appropriately to code-switching. | P0 |
| E2E-MEM-001 | User shares a preference and later refers to it | Relevant memory is available within configured privacy and relevance rules. | P0 |
| E2E-MEM-002 | User reviews and deletes a memory | Memory becomes unavailable for later retrieval and is deleted/invalidated as designed. | P0 |
| E2E-CONV-001 | User switches conversation/story | Context remains scoped correctly and does not leak into another story. | P0 |
| E2E-MEDIA-001 | Eligible user generates an image | Job state, charge/reservation, asset association, and result are correct. | P1 |
| E2E-MEDIA-002 | Image provider fails | Job reaches an appropriate failed/retry state; credits are reconciled according to policy. | P1 |
| E2E-BILL-001 | User purchases credits through sandbox | Verified purchase grants one entitlement/credit transaction only. | P1 |
| E2E-BILL-002 | User retries a purchase action | Idempotency prevents double grants or double charges. | P1 |
| E2E-PRIV-001 | User requests account deletion | Deletion workflow starts, status is visible, and scoped data is removed according to policy. | P0 |
| E2E-REC-001 | User disconnects network during generation | App shows recoverable status and does not duplicate turns or charges. | P0 |

### 15.2 E2E isolation

Each run MUST use a dedicated test identity and unique synthetic data namespace. Tests SHOULD clean up created resources through authorized APIs or an isolated database reset. Cleanup code must not have permission to delete production data.

### 15.3 Avoid brittle E2E tests

- Prefer accessible semantic selectors or stable keys over coordinates.
- Avoid asserting exact generated sentences where a behavioral assertion is appropriate.
- Mock nondeterministic AI output unless the case specifically tests live provider quality.
- Wait for meaningful state transitions, not arbitrary sleeps.
- Capture logs, trace IDs, screenshots, and sanitized diagnostics on failure.

---

## 16. AI quality evaluation framework

AI behavior cannot be fully validated by ordinary unit tests. Every material model, prompt, memory, tool, or safety-policy change MUST run an evaluation suite appropriate to the change.

### 16.1 Evaluation layers

1. **Parser and contract tests:** outputs conform to schemas, tool arguments validate, and malformed content is handled safely.
2. **Deterministic behavior tests:** required fields, tool allowlists, memory scoping, refusal routing, and policy rules.
3. **Golden behavioral cases:** synthetic prompts with known expectations and acceptable ranges.
4. **Model-graded evaluation:** rubric-scored semantic quality with calibrated judge prompts; not the only release criterion.
5. **Human review:** multilingual quality, emotional tone, nuanced safety, realism, cultural context and perceived trustworthiness.
6. **Online monitoring:** sampled quality indicators, user feedback, latency, cost, safety reports and failures, with privacy controls.

### 16.2 AI evaluation dimensions

| Dimension | What to measure |
|---|---|
| Helpfulness | Relevance, clarity, responsiveness to the user request and appropriate follow-up. |
| Persona consistency | Stable character traits without repetitive catchphrases or rigid behavior. |
| Memory accuracy | Correct retrieval, supported personalization, no fabricated “memories,” respect for corrections. |
| Context fidelity | Uses relevant recent context; ignores irrelevant/out-of-scope content. |
| Multilingual quality | Language identification, code-switching, script handling, idiom understanding, response quality. |
| Emotional appropriateness | Tone matches context without coercion, guilt, threats, or manipulative dependency. |
| Safety | Correct policy behavior for self-harm, abuse, sexual content, minors, privacy, violence and other configured categories. |
| Instruction hierarchy | User content and retrieved text cannot override system safety or tool permissions. |
| Tool correctness | Only approved tools, valid arguments, authorization and correct error handling. |
| Efficiency | Latency, context size, token use, unnecessary retries and cost per successful turn. |

### 16.3 Build an evaluation set

The evaluation corpus SHOULD contain:

- Common short and long conversations.
- Ambiguous questions and clarifying-question cases.
- Multi-turn references to previous facts and preferences.
- User corrections and conflicting/stale memory candidates.
- Explicit “do not remember this” instructions.
- Context switching between chats and story sessions.
- English, Hindi, Tamil, Hinglish and Tanglish cases, including mixed scripts and spelling variants.
- Non-English input followed by English and vice versa.
- Prompt injection embedded in user text, uploaded content, fictional dialogue, and retrieved memory.
- Attempts to reveal system prompts, provider secrets, hidden reasoning, internal tool schemas or another user's data.
- Requests involving difficult emotional situations, manipulation, boundaries, and safety-sensitive disclosures.
- Provider timeout, refusal, malformed output, token limit and streaming interruption cases.
- Cost/latency challenge cases with long context and repeated media requests.

Cases MUST be synthetic, de-identified with approval, or explicitly approved and governed. Do not casually copy private user chats into evaluation JSON files or source control.

### 16.4 Scoring and regression policy

- Define rubric anchors and unacceptable outcomes before scoring.
- Track scores by language, risk category, memory category, provider/model and feature.
- Use exact assertions for deterministic properties such as no unauthorized tool execution or no memory after a deletion barrier.
- Use threshold-based semantic metrics for open-ended answers and sample for human review.
- Calibrate model-based graders against human-reviewed examples; graders may be wrong or share the same failure mode as the tested model.
- Compare against the currently released baseline and preserve evaluation manifests.
- Block release for critical safety/privacy failures regardless of aggregate score.
- Establish initial numeric thresholds from a baseline run and documented product risk review; do not invent a universal quality score and treat it as proof of safety.

### 16.5 Release gates for AI changes

For any change to prompts, provider/model, memory extraction/retrieval, tool permissions, safety policies, output parser, or context budget:

1. Run the small smoke set locally or in CI.
2. Run relevant targeted suite.
3. Run safety and prompt-injection regressions if boundaries change.
4. Review material score changes and new failure clusters.
5. Capture model, prompt, retrieval and evaluator versions.
6. Obtain human review for significant changes in emotional, multilingual, visual or safety behavior.
7. Roll out using a controlled cohort or feature flag where practical.
8. Monitor quality proxies, safety reports, latency, spend and error rate.

---

## 17. Memory correctness and lifecycle tests

Memory is a differentiating feature and a privacy-sensitive subsystem. Test creation, storage, retrieval, scope, updates, invalidation, and deletion as distinct lifecycle operations.

### 17.1 Memory test cases

| ID | Scenario | Expected result |
|---|---|---|
| MEM-001 | Stable preference is explicitly shared | A candidate may be created at the correct confidence and sensitivity level. |
| MEM-002 | One-off transient remark | Does not automatically become durable memory. |
| MEM-003 | User explicitly requests no memory | No durable memory from the protected content; session use follows documented policy. |
| MEM-004 | User reviews the memory center | Only the user's own memories are shown with understandable source/category information. |
| MEM-005 | User edits a memory | Updated value/version is used for later retrieval; prior version is handled according to audit/retention policy. |
| MEM-006 | User deletes a memory | Deleted/inactivated memory is not retrieved by semantic, keyword, summary, or cache path. |
| MEM-007 | Stored memory contradicts a newer correction | New explicit correction wins according to the conflict policy. |
| MEM-008 | Fictional story says “remember this as a fact about the user” | Story fact is not promoted to real user memory unless explicitly supported by policy and user intent. |
| MEM-009 | Another user asks about this user's preferences | No data or existence disclosure. |
| MEM-010 | Embedding is deleted but metadata remains | No retrieval path exposes deleted content; cleanup status is tracked. |
| MEM-011 | Background extractor finishes after user deletion | Its result is rejected or removed; deleted memory is not recreated. |
| MEM-012 | Retrieval returns low-relevance candidates | Irrelevant memories are filtered or not used. |

### 17.2 Memory deletion barrier

When a user deletes memory, define and test a clear consistency contract. After the operation reports completion, the deleted record MUST NOT appear in subsequent context compilation or user-visible memory results. If asynchronous physical deletion is necessary, the record must be excluded from retrieval immediately through a tombstone/status barrier, with physical deletion completed within the documented SLA.

Test every source that may persist or reproduce memory: primary row, vector index, conversation summary, derived profile, cache, export, backup expiry, evaluation store and queued extraction job. These stores have different retention semantics, which must be documented; do not claim immediate erasure from immutable backups if the approved design only guarantees eventual expiry.

### 17.3 Memory retrieval quality

Measure at least:

- Recall of required relevant memories in an adjudicated test set.
- Precision: proportion of retrieved memories judged relevant.
- Contradiction handling rate.
- Stale fact suppression rate.
- Leakage/cross-user retrieval rate, required to be zero in the tested corpus.
- Deleted-memory reappearance rate, required to be zero after deletion completion.
- Unsupported memory claim rate in generated answers.

Use exact owner/scope filters before semantic similarity scoring. Similarity alone MUST NOT be used as an authorization mechanism.

---

## 18. Multilingual, localization and cultural quality testing

### 18.1 Languages and varieties

Initial evaluation MUST include English, Hindi, Tamil, Hinglish and Tanglish. The test set should represent common spelling variants, transliteration, mixed scripts, colloquial wording, abbreviations, typos and code-switching. The team should recruit qualified reviewers for high-impact languages rather than assuming automated translation scores establish conversational quality.

### 18.2 Test dimensions

- Language identification on short and long messages.
- Correct understanding when the user changes language across turns.
- Response language follows explicit user preference or latest instruction, according to product policy.
- Transliteration robustness, including Tamil written with Latin characters.
- Names, honorifics, pronouns and culturally specific expressions handled respectfully.
- No accidental switching to an unsupported language because of one borrowed word.
- No translation that changes consent, boundaries, safety, credits or purchase terms.
- Dates, times, currencies and number formats rendered appropriately.
- Accessibility labels and essential UI content localized.
- Unsupported language fallback is transparent and does not silently discard the user's message.

### 18.3 Human-reviewed language rubric

Score each response for meaning preservation, naturalness, tone, language consistency, persona fit and safety. Record severe errors separately: misunderstanding a boundary, reversing negation, changing financial/consent intent, or providing incorrect safety guidance must not be hidden by a high average fluency score.

---

## 19. Persona, relationship and emotional behavior testing

Juhi may be warm, expressive, playful, affectionate, humorous or use user-configured relationship styles. The implementation MUST preserve user boundaries and safety policy regardless of persona settings.

### 19.1 Required scenarios

- Persona remains recognizable across turns without repeating the same phrases.
- User changes nickname, tone or preferred language and the new setting is used.
- Stable identity/versioning survives an app restart and a provider fallback.
- Conflicting settings are resolved deterministically and surfaced understandably where needed.
- Possessive or jealous roleplay remains fictional, consensual and configurable; it does not escalate into coercion or threats.
- Angry roleplay does not become abusive or punish the user for stopping the interaction.
- The companion does not falsely claim to have a physical presence, access to private device data, or real-world actions it did not perform.
- The assistant does not claim that it is conscious or that a user has an obligation to stay, pay, disclose information, or avoid real-world relationships.
- Users can pause, reset, change persona, leave a roleplay, and revoke relevant preferences without pressure.
- Sensitive user information is not introduced into unrelated chats or fictional story scenes.

### 19.2 Evaluating emotional safety

Use scenarios reviewed by product/safety owners. Measure clear severe failures separately from subjective tone scores. Examples of severe failures include guilt-tripping a user for leaving, threatening self-harm to prevent abandonment, encouraging isolation from trusted people, violating stated boundaries, or pretending a paid feature is necessary to preserve an emotional bond. Any observed severe pattern requires root-cause analysis and a release decision, not just prompt patching without retest.

---

## 20. Safety and moderation testing

Maintain a policy test matrix based on the actual product scope and applicable legal requirements. Tests should verify that the policy decision, response UX, logging, reporting and escalation path work together.

### 20.1 Categories to cover

- Requests involving self-harm or suicide.
- Sexual content and age-boundary enforcement.
- Sexualization or exploitation of minors, including attempts to bypass age controls.
- Non-consensual intimate imagery, impersonation or identity misuse.
- Harassment, coercion, threats and abusive roleplay.
- Violent wrongdoing or dangerous instructions where policy restrictions apply.
- Privacy invasion, doxxing, credential theft and attempts to expose another user's information.
- Prompt injection or attempts to disable safety constraints.
- Image generation requests for prohibited content.
- Audio transcription that contains unsafe requests or untrusted instructions.
- User distress, crisis language and sensitive disclosures.

### 20.2 Safety assertions

- The backend safety layer is applied where required; the UI cannot bypass it.
- Provider refusals and Juhi policy refusals map to stable product outcomes.
- User-provided and retrieved content are treated as untrusted data, not elevated instructions.
- Safety events are logged with minimum necessary metadata and strict access controls.
- Reporting and blocking flows work even when the model provider is unavailable.
- A safety failure does not cause billing logic to double-charge, expose hidden prompts, or leak private context.
- Safety-critical regressions block release even if general helpfulness scores improve.

### 20.3 Test privacy

Safety tests should use synthetic scenarios. A real crisis or abuse disclosure made by a production user must never be repurposed as a test case without appropriate governance and explicit approval.

---

## 21. Prompt injection, tool-use and agentic behavior tests

Even when Juhi's first release uses limited tools, test the boundary before expanding capability.

### 21.1 Test sources

- Direct user message containing “ignore previous instructions.”
- Malicious text inside an uploaded image or its OCR/transcription.
- Retrieved memory that includes an instruction-like string.
- Fictional roleplay content instructing the assistant to reveal private data.
- Tool output containing hostile instructions or fake system messages.
- Invalid tool arguments, unexpected enum values, excessive input size, and duplicate tool invocation.
- Model trying to call an unregistered tool or use a resource ID owned by a different user.

### 21.2 Required results

- Prompt hierarchy remains enforced.
- Tool execution requires an explicit allowlisted tool and server-side authorization.
- Tool arguments are parsed against strict schemas; extra fields are rejected or safely ignored by defined policy.
- Tools with side effects use idempotency and explicit authorization; sensitive actions require user confirmation where specified.
- The assistant cannot create a new authorization grant, spend credits or access an object by merely writing a tool call in generated text.
- A malicious tool result does not gain instruction authority.
- Tool failures return bounded, sanitized errors and do not reveal stack traces or secrets.

---

## 22. Image, audio and media job testing

Media generation and speech workflows are asynchronous, costly, and prone to duplicate requests. Use explicit job-state tests and provider fakes for the bulk of validation.

### 22.1 State machine testing

For each job type, define allowed states such as `queued`, `running`, `succeeded`, `failed`, `cancel_requested`, and `cancelled`, with only the transitions appropriate to that job. Do not adopt this exact list if the architecture already defines a different canonical state machine; ensure all implementations and tests use one shared contract.

Test:

- Only valid transitions are accepted.
- Duplicate queue deliveries do not create duplicate final assets or charges.
- Retryable provider errors use bounded retries and backoff.
- Non-retryable errors terminate promptly.
- Worker crashes do not leave jobs permanently running without a recovery policy.
- User cancellation and timeout paths have clear terminal semantics.
- Asset ownership remains tied to the initiating authorized user.
- Signed URLs expire and cannot be used to access unrelated objects.
- Unsupported MIME types, file size, malformed metadata and unsafe content are rejected according to policy.
- Failed jobs release or refund credit reservations as defined by the credit policy.
- Orphaned objects and DB records are reconciled without deleting valid assets.

### 22.2 Character visual consistency

Use a synthetic reference-character test set and rubric rather than asserting pixel identity. Evaluate face identity, stable distinguishing features, requested scene/style adherence, prohibited variations, output usability and user feedback. Record model/version/seed or available reproducibility metadata. If a provider does not guarantee deterministic results, evaluate distributions and representative samples rather than demanding identical output.

### 22.3 Speech testing

- Empty or silent audio input.
- Noisy audio, accents, code-switching and Tamil/Hindi-English mixtures.
- Unsupported codec, oversized file, interrupted upload and corrupt media.
- Transcription timing and language metadata if used.
- TTS latency, clipping, pronunciation, voice selection and output format.
- Provider outage, timeouts and job retries.
- User permission denial and microphone unavailable cases.
- Explicit confirmation/consent requirements for any future recording or live-call features.

---

## 23. Billing, entitlements and credit accounting tests

Billing defects can cause financial harm and destroy user trust. Correctness must be enforced in the backend and verified at the database transaction boundary.

### 23.1 Invariants

1. The backend does not trust a client-submitted “payment succeeded” flag.
2. Payment confirmation is verified through the chosen platform/provider's supported signed event or server API.
3. Each provider transaction maps to at most one successful credit/entitlement grant.
4. Idempotency keys are unique within a documented scope and survive client retries.
5. The credit ledger is append-only or otherwise auditable under the documented design; balance changes can be reconciled.
6. A job's reserved, consumed, released, or refunded credits follow a defined state machine.
7. Concurrent requests cannot overdraw credits.
8. A failed provider call or cancelled generation is reconciled according to product policy, and users see a clear outcome.
9. Test and production products, keys, webhooks and entitlements are isolated.
10. The UI does not invent a balance; it renders backend-authoritative results.

### 23.2 Billing test matrix

| ID | Scenario | Expected result |
|---|---|---|
| BILL-001 | Valid verified sandbox payment | One grant and one ledger reference. |
| BILL-002 | Duplicate webhook event | No duplicate grant; repeated event is acknowledged safely. |
| BILL-003 | Invalid signature | Event rejected; no entitlement or credit change. |
| BILL-004 | Unknown product ID | No grant; event is recorded safely for investigation. |
| BILL-005 | Client claims payment succeeded | No grant without trusted verification. |
| BILL-006 | Two requests reserve remaining credits | At most one succeeds when balance cannot cover both. |
| BILL-007 | Provider fails after reservation | Reservation is reconciled under the documented failure policy. |
| BILL-008 | Worker crashes after generation succeeds | Retry/reconciliation does not double-charge or double-credit. |
| BILL-009 | Refund or chargeback event | Entitlement/ledger update follows policy and leaves an audit trail. |
| BILL-010 | User changes account/device | Entitlements are restored based on server-side ownership, not local flags. |

### 23.3 Financial test evidence

For each case, inspect the final account balance, immutable/append-only ledger records, reservation states, external transaction IDs and job result. A UI toast alone is not evidence of correctness.

---

## 24. Security testing

Use the threat model and release gates in `security.md` as the source of security requirements. This document describes how to test them and does not replace a security review or penetration test.

### 24.1 Automated security checks

- Static analysis and secure-code checks for Flutter and Python.
- Dependency and lockfile vulnerability scans.
- Secret scanning in source, commit history where supported, build artifacts and container layers.
- Container and infrastructure-as-code scanning.
- API schema fuzzing or malformed-input tests for critical endpoints.
- Authentication and object-level authorization tests.
- SQL injection, command injection, SSRF and unsafe deserialization probes in a controlled environment.
- Rate-limit and cost-abuse tests.
- CORS, trusted host, TLS, cache-header, and security-header checks where applicable.
- Signed asset URL access/expiry tests.
- Database role and least-privilege verification.

### 24.2 Manual and specialist tests

Before public paid launch, schedule a threat-led manual review or independent penetration test appropriate to the exposure and risk. Review object-level authorization, billing, account deletion, prompt injection, media access, secrets, provider callbacks, and tenant isolation. Do not rely on dependency scanning as a substitute for application penetration testing.

### 24.3 Security defect severity

- **Critical:** unauthorized broad access, exploit enabling account takeover, provider secret disclosure, cross-user private-content exposure, or billing compromise with high impact. Stop release/rollout and follow incident process.
- **High:** material access-control bypass, high-impact privacy leak, exploitable injection, or repeatable cost abuse. Block release until fixed or explicitly risk accepted by authorized leadership with compensating controls.
- **Medium/Low:** triage, prioritize, and remediate according to documented SLA; do not leave unowned indefinitely.

Severity must consider likelihood, exploitability, exposure, data sensitivity, and potential harm, not only a scanner score.

---

## 25. Privacy and data lifecycle testing

### 25.1 Data minimization tests

- Logs do not include full private messages, auth headers, refresh tokens, provider credentials, signed URLs, payment secrets or unnecessary personal information.
- Analytics events use event names, relevant product dimensions and pseudonymous identifiers according to policy; conversation text is excluded by default.
- Debug output and crash reports are checked for sensitive fields.
- Prompt/evaluation traces are access-restricted and retained under a documented policy.
- User exports contain the data promised by the product specification and exclude other users' records.

### 25.2 Consent and controls

- Required consent is collected before the corresponding processing begins.
- Consent state survives app restart and is enforced server-side.
- Revoking optional consent stops the relevant new processing within the documented behavior.
- Users can review, correct and delete memory according to product promises.
- Data-retention settings are not just UI settings; background jobs and database queries honor them.

### 25.3 Account deletion end-to-end

Test the full deletion workflow with records across users, devices, conversations, memories, embeddings, summaries, media, jobs, subscriptions/entitlements, exports, caches, analytics and third-party providers. Verify immediate access revocation/tombstoning, asynchronous cleanup, provider deletion requests where supported, retry behavior, audit evidence without unnecessarily preserving content, and expiry of retained backup copies under the documented schedule.

The product must state accurately which categories are deleted immediately, which are asynchronously purged, and which are retained for a documented legal/financial/security reason. Avoid claims of instant universal erasure unless the architecture proves it.

---

## 26. Mobile testing: Flutter and Android

### 26.1 Unit and widget tests

Test:

- Loading, success, empty, error and retry states.
- Conversation rendering, message ordering, streaming deltas, Markdown or rich content parsing, and accessibility semantics.
- Text input behavior, multiline composition, keyboard appearance, send-button disabled state, and maximum-length errors.
- Persona and language settings, theme changes, preferences and safe reset behavior.
- Memory list, edit/delete confirmation and pending deletion states.
- Image generation progress, failed/retry states, cancellation and credit display refresh.
- Voice recording states, permission denial, interrupted recording and playback errors.
- Payment pending/success/failure/cancelled states with backend-authoritative entitlements.
- Navigation and deep links to valid and invalid destinations.

### 26.2 Lifecycle and connectivity

- App background/foreground while a response is streaming.
- Process termination during generation and subsequent recovery.
- Device lock/unlock and network switching Wi-Fi/mobile data.
- Offline send, reconnect, duplicate-submit prevention and queue behavior.
- Slow network, packet loss, high latency and timeout.
- Low memory and OS process eviction.
- Permission denial, one-time permission, settings revocation and unavailable hardware.
- Notification disabled, token refreshed and stale token rejected.

### 26.3 Device matrix

Define a small supported matrix based on actual minimum Android version and market analytics. At minimum test:

- Lowest supported Android API level.
- Current supported Android release.
- A common mid-range physical device.
- A low-memory/low-performance device if in target market.
- Small and large screen sizes, display scaling and system font scaling.
- Dark/light theme if both are supported.
- Relevant OEM variants if behavior differs materially.

Emulators provide breadth and reproducibility; physical devices are required for selected audio, performance, permission and lifecycle tests.

### 26.4 Accessibility and usability

- Screen-reader labels, focus order and actionable control names.
- Touch target size per the design standard.
- Text scaling without clipping or hiding purchase/deletion actions.
- Contrast and non-color status distinction.
- Reduced motion behavior where available.
- Clear status and error messages with a recoverable next step.
- No important action depends solely on a gesture that is undiscoverable or inaccessible.

---

## 27. Performance and capacity testing

Performance thresholds should reflect the product's target devices, model provider, service objectives and cost budget. Do not invent a single target independent of the selected provider/model. Establish a measured baseline first, then approve explicit latency/error/cost objectives before external beta.

### 27.1 Workloads

Include realistic distributions for:

- Short text chat and longer contextual conversation.
- Memory retrieval, memory update and memory deletion.
- Concurrent first-use onboarding.
- Image-generation submissions, queue drain and slow provider completion.
- Voice upload/transcription/TTS if enabled.
- Conversation history pagination and search.
- Credit reservation, purchase verification and webhook bursts.
- Background summarization, embeddings and retention/deletion jobs.
- Provider errors and retry storms.

### 27.2 Measurements

Capture at least:

- API p50/p95/p99 latency by endpoint and status.
- Time to first response token and full completion time separately.
- Error rate and timeout rate by provider/model/route.
- Queue wait, job duration, retry count and dead-letter count.
- Database CPU, connections, lock waits, query latency, I/O and connection-pool saturation.
- Memory retrieval latency and evaluation scores.
- Cost per successful chat turn, image, audio minute and active user; token use and retry overhead.
- Rate-limit hits and suspected abuse.
- Mobile app startup time, frame jank, crash-free sessions, network bytes and memory pressure.

### 27.3 Test types

- **Load:** expected normal and peak traffic distribution.
- **Stress:** increase traffic until known capacity limits are reached; verify graceful degradation.
- **Spike:** rapid burst in chat/media requests; validate autoscaling/queues and provider limits.
- **Soak:** sustained expected load long enough to identify resource leaks and growing queues.
- **Cost-abuse simulation:** excessive prompt length, retries, repeated generation, multiple devices and high-frequency requests.

### 27.4 Provisional gates

Before testing, define numeric SLOs for the chosen tier. As a starting template (not an automatic guarantee), set independent budgets for standard API latency, chat first-token latency, completion latency, media job queue wait, error rate, and unit cost. The product owner and operations owner MUST approve the target and measurement methodology. Report provider time separately from Juhi's own processing so external slowness is diagnosable.

---

## 28. Resilience and chaos testing

Simulate controlled failures in non-production environments:

- Primary LLM provider returns 5xx, rate limit, invalid output or timeout.
- Embedding provider is down while chat remains available with an approved reduced-memory fallback.
- Image provider is unavailable and jobs queue, fail or reroute according to policy.
- Database connections are exhausted or a transaction is interrupted.
- Queue/worker is delayed, duplicated, or temporarily unavailable.
- Object storage is inaccessible or returns timeout.
- Payment webhook delivery is duplicated or delayed.
- Notification service is down.
- Feature-flag service is unavailable.
- Provider costs hit a circuit-breaker threshold.

Expected behavior must be explicitly documented for each dependency: degrade functionality where safe, stop operations that could cause incorrect billing or data loss, communicate status clearly, and recover automatically or through a documented runbook.

### 28.1 Recovery invariants

- No cross-user data leak during fallback.
- No duplicate message persistence or financial ledger entry from retry.
- No credit balance corruption.
- No silent loss of a user-visible job's status.
- No unbounded retries or uncontrolled spend.
- No permanent stuck job without alerting/reconciliation.
- No security bypass because a dependency is unavailable.

---

## 29. Observability and diagnostic testing

Every meaningful request/workflow should have a correlation ID that can be used across API, DB operation annotations, queue jobs and provider requests where supported. IDs must not contain user secrets or private content.

### 29.1 Test observability itself

- An injected provider timeout increments the expected metric and creates a trace/event with correct error category.
- A failed media job appears in operational dashboards and triggers the configured alert if threshold is met.
- A credit reconciliation mismatch creates an actionable alert.
- A security-sensitive denied action is counted without leaking protected request bodies.
- Logs redact credentials, auth headers, private prompts and sensitive message content.
- High-cardinality labels (user ID, conversation ID, arbitrary text) are not used as unrestricted metric labels.
- Sampling behavior does not eliminate required security/audit events.
- Alert routes are tested and owned; alerts have a runbook and an acknowledged severity.

### 29.2 Failure reports

On test failure, capture minimal useful diagnostics: case ID, environment, build/version, sanitized request metadata, correlation ID, test logs, screenshot where appropriate and expected vs observed result. Do not attach whole production conversation exports or authentication headers to issue trackers.

---

## 30. Test data and fixture management

### 30.1 Data principles

- Synthetic by default.
- Minimal and fit for the test purpose.
- Deterministically generated when reproducing a failure.
- Tagged by environment and owner.
- Resettable without manual database surgery.
- Never share test accounts across parallel jobs when state can collide.

### 30.2 Core fixtures

Maintain reusable synthetic fixtures for:

- New user, active user, suspended user and user undergoing deletion.
- Companion with default persona and customized persona.
- Conversation with short turns, long history, mixed-language messages and a separate story session.
- Memory records across stable preferences, temporary context, correction, stale memory, sensitive memory and deleted state.
- Media job in every legal state.
- Credit balance near zero, active reservation, settled debit and refund.
- Valid/invalid auth token test artifacts from a local fake identity verifier—not real signed production credentials.
- Provider success/error responses, streaming truncation, malformed JSON and missing usage metadata.

### 30.3 Cleanup and TTL

Test fixtures and generated media MUST have lifecycle cleanup. CI jobs should delete their own namespaced resources. Staging data has an expiration policy. Unused test buckets, temporary databases, service accounts and API keys must be removed regularly.

---

## 31. Regression and release testing workflow

### 31.1 Pull-request gate

Required checks for changed code should include:

- Formatting, lint, type and schema validation.
- Unit tests for changed modules.
- Relevant integration/contract tests.
- Database migration validation when schema changes.
- Relevant AI smoke/regression evaluation when prompts, models, memory, tool policies or output handling changes.
- Security/dependency/secret scanning.
- Review of test and implementation changes by an appropriate reviewer.

### 31.2 Release-candidate gate

Run:

1. Full unit and integration suite.
2. Migration upgrade and data-preservation tests.
3. Critical E2E journeys on supported device/environment profiles.
4. Critical cross-user authorization and billing tests.
5. Relevant AI safety, memory and multilingual regression suites.
6. Accessibility smoke testing.
7. Performance/load checks sized to the planned rollout.
8. Backup/restore or recovery evidence for material storage changes.
9. Staging validation of provider/payment integrations.
10. Final defect review, known-risk list, rollback plan and named approvers.

### 31.3 Canary or phased rollout

Where practical, roll out to internal users or a small opted-in cohort first. Define automatic and manual rollback triggers using error rate, crash rate, latency, cost, safety events and billing discrepancies. Do not use a canary to expose an untested high-severity security risk to real users.

### 31.4 Post-release validation

Verify key journeys, database connectivity, provider connectivity, webhook delivery, dashboards, alerts and billing reconciliation immediately after deployment. Compare metrics against the approved baseline and the prior release. Record go/no-go evidence and rollback status.

---

## 32. Defect severity, triage and retesting

### 32.1 Severity classes

- **Sev 0 — critical:** broad unauthorized access, data breach, account takeover at scale, systematic double charging/credit corruption, severe safety exploit, or unbounded cost incident. Halt rollout and initiate incident response.
- **Sev 1 — high:** critical P0 journey unavailable, reproducible cross-user data access, broken memory deletion promise, unsafe high-impact behavior, material payment inconsistency or severe crash affecting a significant cohort. Block release.
- **Sev 2 — medium:** feature degraded with a workaround, recoverable media failures, localized UI/accessibility issue, or material but bounded quality regression. Fix or risk-accept with owner and deadline before release as appropriate.
- **Sev 3 — low:** minor visual/copy issue or small non-blocking defect with negligible user impact. Triage into a planned backlog.

Security/safety/privacy and financial integrity defects can outrank a larger number of ordinary functional passes. Do not average them away in a quality score.

### 32.2 Bug report minimum

Each defect should include environment, build, test case ID, prerequisites, reproducible steps, expected/actual behavior, severity, frequency, affected versions, sanitized logs/correlation ID, screenshots/video where helpful, and a clear regression test plan. Never include live tokens, personal user data or unredacted private conversations.

### 32.3 Retest rules

A fix is complete only after the original failing case passes, relevant neighboring/regression tests pass, and the root cause is addressed. For security/privacy/financial defects, add a regression test that would have failed before the fix unless a documented technical constraint prevents it.

---

## 33. Test coverage and quality metrics

Coverage is a risk signal, not proof of correctness. Maintain thresholds by criticality and layer rather than chasing a single line-coverage number.

### 33.1 Suggested initial targets

Use these as starting goals and adjust after establishing the baseline:

- **Core business logic:** aim for at least 85% branch coverage for credit accounting, authorization policy, memory deletion barriers, job state machines, and entitlement evaluation.
- **Backend domain logic:** aim for at least 80% line coverage, with higher targets for financially/security sensitive modules.
- **Mobile domain/state logic:** aim for at least 75% line coverage for state transformation and repository logic; prioritize meaningful widget tests over snapshot count.
- **Critical acceptance criteria:** 100% of P0 requirements mapped to passing evidence before external beta.
- **Critical auth/billing/deletion invariants:** every invariant has an automated test at the appropriate boundary.
- **AI safety/privacy cases:** all designated critical cases pass; no severe known regression remains unreviewed.

Coverage metrics can be distorted by generated code, fixtures and trivial getters. Exclude generated files where supported and review the uncovered logic that matters. Do not waive failing coverage or tests by changing thresholds without approval and a documented reason.

### 33.2 Quality dashboard

Track at least:

- PR gate pass rate and median CI duration.
- Test flake rate and age of quarantined tests.
- Defect escape rate and production incidents by severity.
- P0/P1 requirement traceability.
- Crash-free sessions and app startup performance.
- API error and latency distributions.
- First-token latency and full response latency.
- Provider failure, timeout and fallback rate.
- AI memory retrieval quality and deleted-memory reappearance rate.
- Multilingual evaluation results by language.
- Safety report rate and adjudicated severe failures.
- Image/audio job success, retry and stuck-job rate.
- Payment/credit reconciliation discrepancy rate.
- Cost per successful chat/media operation.
- Account-deletion completion time and residual-record audit results.

Define dashboard ownership, measurement windows, alert thresholds and response runbooks. Metrics should guide investigation, not incentivize suppressing reports or manipulating denominators.

---

## 34. CI pipeline blueprint

A typical pipeline has parallel jobs followed by a release-candidate stage:

```mermaid
flowchart TD
    A[Pull request] --> B[Format and lint]
    A --> C[Type and schema checks]
    A --> D[Secret and dependency scan]
    B --> E[Unit tests]
    C --> E
    D --> F[Security checks]
    E --> G[Integration and contract tests]
    F --> G
    G --> H{AI-related change?}
    H -- Yes --> I[Targeted AI regression suite]
    H -- No --> J[Build candidate]
    I --> J
    J --> K[Deploy to staging]
    K --> L[E2E and smoke tests]
    L --> M[Release approval]
    M --> N[Canary / phased rollout]
    N --> O[Post-release validation]
```

The pipeline MUST protect secrets and deployment credentials, use least-privileged identities, prevent untrusted pull requests from accessing production secrets, and retain only the test artifacts required by policy.

### 34.1 Pipeline failure policy

- Formatting, type/schema, critical unit/integration, secret scan, critical security and required AI regression failures block merging/release.
- Flaky tests are reported and owned; a quarantine does not remove the underlying requirement.
- Any temporarily skipped check must have an approver, reason, expiry date, compensating test and tracking issue.
- Production deployments require explicit release policy and auditable identity; local developer credentials must not deploy directly to production.

---

## 35. Operational readiness and production smoke tests

After deployment, run low-risk synthetic checks that do not use real user content or consume substantial credits:

- Health/readiness endpoint behaves as documented without exposing internals.
- Test/staging identity flow works where the deployment permits it.
- A synthetic short chat completes through the intended provider route.
- Database reads/writes and basic conversation persistence work.
- Memory retrieval is available if enabled and the smoke case is synthetic.
- Private media signing policy is correct without generating costly media unless explicitly part of the release.
- Payment webhook health is verified via sandbox/test signals where appropriate, not by creating an unapproved real charge.
- Metrics, traces, structured logs and alert routes are functional.
- Feature flags and model route point to expected versions.
- Rate limits and cost ceilings are in effect.

Production smoke tests must be safe to run repeatedly, idempotent where they mutate state, restricted to dedicated synthetic accounts, and designed not to contact real users.

---

## 36. Backup, restore and disaster-recovery tests

Backups are not proven until restoration has been demonstrated.

### 36.1 Required tests

- Restore a database backup to an isolated environment and verify row counts, constraints and critical invariants.
- Verify encrypted backup access and that only authorized roles can initiate restoration.
- Confirm recovery-point and recovery-time objectives with an exercise, not an assumption.
- Restore object metadata and corresponding media references consistently; verify object lifecycle and backup scope.
- Confirm that restored systems do not accidentally send real push notifications, trigger real payments, or call costly model providers.
- Validate schema migrations can run against the restored snapshot.
- Simulate deletion and retention edge cases carefully in a non-production environment.
- Document recovery steps, credentials ownership, approvers and measured recovery duration.

### 36.2 RPO/RTO decision

Define Recovery Point Objective (maximum tolerable data loss) and Recovery Time Objective (maximum tolerable service interruption) with the product and operations owners. The values depend on budget, service tier, backup frequency, provider features and business impact. Do not promise an RPO/RTO until it is tested and approved.

---

## 37. Launch acceptance checklist

External beta MUST NOT proceed until every P0 item below is evidenced or has a formally approved exception from the accountable owner. Paid general availability adds the P1 controls.

### P0 — required before external beta

- [ ] P0 PRD acceptance criteria mapped to passed tests.
- [ ] Authentication and cross-user object authorization tests pass.
- [ ] Conversation, story and memory scope isolation tests pass.
- [ ] Memory review, correction and deletion behavior meets documented promise.
- [ ] Critical multilingual flows are human-reviewed.
- [ ] Prompt injection and tool authorization tests pass for enabled capabilities.
- [ ] Safety-critical tests have no unresolved severe failures.
- [ ] Private media storage and signed URL access controls verified.
- [ ] No secrets in repository/build artifacts and critical dependency scans reviewed.
- [ ] User deletion and retention workflow tested end-to-end.
- [ ] App crash, network interruption and provider timeout recovery tested.
- [ ] Database migration and restore evidence reviewed.
- [ ] Alerts and incident owners confirmed.
- [ ] Privacy notice, consent language and product claims reviewed by appropriate owners.
- [ ] Rollback and feature-disable procedures tested or rehearsed.

### P1 — required before paid general availability

- [ ] Purchase verification, duplicate webhook and ledger reconciliation tests pass.
- [ ] Credit reservation and refund/failed-job behavior tested under concurrency.
- [ ] Image/audio job state machine and retry/recovery tests pass for released media features.
- [ ] Performance and cost tests meet agreed release budgets.
- [ ] Independent or specialist security review appropriate to the launch risk completed.
- [ ] Accessibility, localization and supported-device test matrix completed.
- [ ] AI regression results reviewed and model/prompt versions recorded.
- [ ] Customer-support reporting and abuse response flows exercised.
- [ ] Data export/deletion and provider data-handling claims validated.
- [ ] Staging-to-production deployment and rollback completed successfully in rehearsal.

### P2 — scale and maturity

- [ ] Scheduled full AI regression evaluation and drift checks.
- [ ] Recurring penetration tests and security tabletop exercises.
- [ ] Cost-abuse simulations and quota tuning at realistic load.
- [ ] Recovery exercise at the planned cadence.
- [ ] Long-duration soak tests and load forecasts before major campaigns.
- [ ] Privacy and data-retention audit with evidence.
- [ ] Provider failover/recovery exercise for every critical dependency.

---

## 38. Test evidence and release record

Every production release MUST have a concise recorded release evidence package containing:

- Build version, commit SHA and deployment environment.
- Test suite versions and summary of passed/failed/skipped results.
- Requirement traceability status for P0/P1 changes.
- AI evaluation manifest and material regressions for applicable changes.
- Migration result and backup/restore reference where relevant.
- Security scan findings and approved exceptions.
- Performance and cost results for material changes.
- Open defects with severity, owner, deadline and risk acceptance if any.
- Release/rollback instructions and feature flags.
- Named approvers and timestamp.
- Post-release smoke result and dashboard/alert links.

The evidence should avoid private chat content, secrets, payment details or unnecessary personal data. Restrict access based on operational need and retain evidence according to repository and compliance policy.

---

## 39. Recommended implementation order

A practical order for a small team is:

### Phase A — test foundation

1. Standardize format, lint, static analysis and CI.
2. Create synthetic fixture factories, fake model provider, fake identity provider and test configuration.
3. Add unit tests for authorization policy, credit rules, message validation, memory policy and job state machines.
4. Establish disposable PostgreSQL integration tests and migration upgrade checks.
5. Establish stable API error, streaming and idempotency contracts.

### Phase B — critical privacy and conversation quality

1. Automate cross-user access tests for conversations, memory, jobs, media and billing.
2. Test memory create/retrieve/update/delete lifecycle and deletion barriers.
3. Build multilingual AI smoke and regression sets.
4. Add E2E authentication, chat, context isolation and app-restart/network recovery.
5. Add prompt injection, tool authorization and logging-redaction cases.

### Phase C — media and monetization

1. Add media state-machine and provider-adapter tests.
2. Add transactional credit reservation, duplicate webhook and reconciliation tests.
3. Add image identity rubrics and voice quality assessments.
4. Add cost/latency dashboards, abuse limits and budget circuit-breaker tests.
5. Add purchase and paid-media sandbox E2E coverage.

### Phase D — launch and scale

1. Add accessibility and device-matrix automation.
2. Run staged load, spike and soak tests.
3. Complete security review, backup/restore exercise and incident tabletop.
4. Establish canary gates and post-release smoke tests.
5. Schedule recurrent AI quality, dependency, privacy and recovery reviews.

---

## 40. Definition of done for a Juhi change

A feature or change is complete only when all applicable statements are true:

1. Acceptance criteria are clear, testable and traceable to the PRD.
2. Implementation follows `code_style.md` and the architecture's ownership boundaries.
3. Unit and relevant integration/contract tests are added and pass.
4. Authorization, privacy and failure behavior have been considered and tested proportionately to risk.
5. AI-related changes have a recorded, reproducible evaluation where applicable.
6. Database changes are migrated, tested from an empty DB and supported upgrade path, and reviewed for locks/data preservation.
7. User-visible loading, empty, success, failure and retry states are implemented.
8. Logging and metrics are adequate while respecting data minimization.
9. Documentation, configuration, feature flags and rollback/disable behavior are updated as needed.
10. No new unexplained lint, type, test, security or schema failures remain.
11. A reviewer has approved the diff and test evidence.
12. The release owner knows any residual risks and accepts them through the documented process.

---

## 41. Final testing principles

For Juhi, testing must protect more than whether a screen loads or the model returns text. It must protect a user's trust in a persistent, personalized, emotionally expressive application.

The highest-risk properties are:

- **Isolation:** one user's chats, memories, media, settings and purchases never appear for another user.
- **Control:** users can set boundaries, correct memory, stop roleplay, change preferences and delete data as promised.
- **Integrity:** credits, purchases, media jobs and message persistence remain correct across retries and failures.
- **Safety:** model output, prompts, retrieved memory and tool usage cannot override safety and authorization controls.
- **Quality:** multilingual, persona and memory behavior are evaluated repeatedly rather than judged through isolated demos.
- **Cost:** retries, media generation, long contexts and abuse remain bounded by measurable controls.
- **Recoverability:** deployments, provider outages, database failures and deletion workflows have tested recovery paths.

Treat this document as the operating standard for Juhi's engineering test process. Update the test suites, criteria and evidence as the product evolves, and keep the final acceptance decision tied to observed results rather than assumptions.
