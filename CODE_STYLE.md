# Juhi — Engineering Code Style and Quality Standard

**Document type:** Engineering standard  
**Applies to:** Juhi Android app, backend API, data layer, AI orchestration, prompt assets, infrastructure, and developer tooling  
**Status:** Proposed baseline for adoption by the repository maintainers  
**Audience:** Mobile engineers, backend engineers, AI engineers, QA, DevOps, security reviewers, and coding agents

---

## 1. Purpose

This document defines how Juhi code should be written, named, organized, tested, reviewed, and maintained. It exists to keep the product understandable as features expand across multilingual conversation, persistent memory, voice, image generation, subscriptions, and trust-and-safety controls.

The standard is intentionally technology-aware. Juhi's initial architecture is a **Flutter mobile application, a Python/FastAPI modular-monolith backend, PostgreSQL as the durable source of truth, optional `pgvector` for semantic retrieval, private object storage for media, Firebase Authentication, and provider adapters for AI services**. The concrete package versions should be selected and pinned by the repository's dependency-management process; this document does not prescribe unverified version numbers.

### 1.1 Normative language

- **MUST / MUST NOT**: required for correctness, safety, security, or maintainability.
- **SHOULD / SHOULD NOT**: default practice; deviations need a clear reason.
- **MAY**: optional when useful.
- **P0**: release-blocking requirement.

### 1.2 Outcomes

Code conforming to this standard should be:

1. **Readable:** intent is obvious without reverse-engineering clever abstractions.
2. **Safe by default:** authorization, validation, privacy, and failure handling are explicit.
3. **Testable:** business rules can be checked without live model providers, Firebase, or cloud resources.
4. **Observable:** failures and performance can be diagnosed without logging private conversation content.
5. **Modular:** features can be added without circular dependencies or cross-layer shortcuts.
6. **Cost-aware:** expensive model, image, and voice operations are bounded, measured, and idempotent where possible.
7. **Consistent:** formatters and linters—not personal preference—settle mechanical style decisions.

---

## 2. Universal engineering principles

### 2.1 Prefer clarity over cleverness

- Use descriptive names that communicate meaning and units.
- Keep functions focused on one coherent responsibility.
- Prefer simple control flow and early returns over deeply nested branches.
- Avoid abstractions that only remove one short expression or merely rename a library call.
- Do not compress code to minimize line count.
- Explain *why* an unusual decision exists; do not comment on obvious syntax.

### 2.2 Explicit boundaries

- UI code MUST NOT call the database directly.
- HTTP route handlers MUST NOT contain large business workflows or direct provider-specific AI logic.
- Domain services MUST NOT depend on Flutter widgets, HTTP request objects, or ORM session internals.
- AI provider SDK types MUST NOT leak through the domain layer or public API schemas.
- Database persistence models MUST NOT be returned as public API responses without mapping and authorization.
- Infrastructure-specific behavior MUST be isolated behind small interfaces/adapters where swapping or testing it is a realistic requirement.

### 2.3 Fail safely and intentionally

- Validate untrusted data at boundaries.
- Do not use an empty object, empty string, `null`, or a fake success response to conceal a failed operation.
- Use typed errors or explicit result states for expected failures.
- Catch exceptions only when the current layer can recover, translate, add meaningful context, or safely terminate the operation.
- Do not catch an exception merely to log and re-raise it unchanged.
- Never expose stack traces, secret values, internal provider responses, SQL details, or raw exception messages to end users.

### 2.4 Make state changes explicit

- Mutations MUST have clear ownership and authorization checks.
- Paid or costly operations MUST have explicit request identity, status transitions, and idempotency behavior.
- Credit debits, refunds, and entitlement changes MUST be transactional and auditable.
- Memory updates and deletions MUST have documented semantics; a user correction takes precedence over a stale inferred memory.
- Avoid hidden writes from property getters, serializers, model constructors, or UI rendering methods.

### 2.5 Keep privacy in the design

- Do not log raw messages, memory content, images, audio, authentication tokens, payment details, or provider credentials by default.
- Do not put private conversation content in analytics event names or metric labels.
- Use synthetic or redacted fixtures in tests and sample data.
- Collect only data with a clear product, safety, operational, or legal purpose.
- Ensure deletion and retention behavior is reflected in code, not merely in documentation.

---

## 3. Repository organization

Use a monorepo unless there is a documented reason to separate deployable services. Keep clients, backend, prompts, infrastructure, and shared contracts distinct.

Recommended starting layout:

```text
juhi/
├── apps/
│   └── mobile/                    # Flutter Android app (and future platforms)
├── services/
│   └── api/                       # FastAPI modular monolith
├── packages/
│   └── api_contracts/             # Optional generated or shared contract artifacts
├── ai/
│   ├── prompts/                   # Versioned prompt templates and metadata
│   ├── evals/                     # Golden datasets and evaluation definitions
│   └── policies/                  # AI routing and safety configuration
├── database/
│   ├── migrations/                # Authoritative schema migrations
│   ├── seeds/                     # Non-sensitive development reference data
│   └── docs/                      # Schema and data lifecycle notes
├── infra/
│   ├── terraform/                 # Infrastructure as code, if adopted
│   ├── docker/                    # Container assets
│   └── deploy/                    # Environment-specific deployment references
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   ├── database.md
│   ├── security.md
│   └── code_style.md
├── scripts/                       # Safe developer and CI utilities
├── .editorconfig
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

If the existing repository differs, do not perform a large folder migration only to match this example. Record the current structure and converge incrementally.

### 3.1 Ownership by layer

| Layer | Owns | Must not own |
|---|---|---|
| Presentation/UI | Rendering, user input, view state | Direct SQL, secret keys, domain persistence rules |
| Application/use cases | Workflow orchestration, transaction boundaries | Widget layout, provider SDK details |
| Domain | Business rules, entities, policies, domain errors | Framework-specific HTTP and database types |
| Adapters/infrastructure | DB, Firebase, cloud storage, AI SDK, payment gateway | Product decisions that belong in domain services |
| API layer | Auth context, request/response validation, status codes | Long-running provider calls embedded in route handlers |
| Background workers | Durable asynchronous jobs and retries | Unbounded retries or hidden user-facing state changes |

### 3.2 Avoid circular dependencies

Dependencies should point toward stable business concepts. A module may depend on modules below it in the documented dependency direction, but lower-level modules must not import route handlers or UI modules. If A imports B and B imports A, reconsider the boundary before introducing import hacks.

---

## 4. Naming conventions

Names MUST be specific enough to distinguish similar concepts. Avoid ambiguous names such as `data`, `item`, `manager`, `helper`, `process`, `common`, or `utils` when a more precise name is available.

| Item | Convention | Example |
|---|---|---|
| Dart classes, enums, extensions | `UpperCamelCase` | `ConversationRepository` |
| Dart methods and variables | `lowerCamelCase` | `loadConversationPage` |
| Dart constants | `lowerCamelCase` unless repository convention requires otherwise | `defaultPageSize` |
| Python modules, functions, variables | `snake_case` | `create_memory_candidate` |
| Python classes and exceptions | `PascalCase` | `MemoryConflictError` |
| Python constants | `UPPER_SNAKE_CASE` | `MAX_MESSAGE_LENGTH` |
| SQL tables and columns | `snake_case`, plural tables | `conversation_messages` |
| SQL primary keys | `id` | `conversation_id` references `conversations.id` |
| SQL foreign keys | `<referenced_entity>_id` | `user_id`, `persona_version_id` |
| HTTP paths | lowercase nouns, plural resource names | `/v1/conversations` |
| JSON API fields | `snake_case` consistently | `created_at`, `next_cursor` |
| Environment variables | `UPPER_SNAKE_CASE` | `DATABASE_URL` |
| Prompt files | descriptive name plus explicit version or release metadata | `conversation_system_v003.md` |
| Feature flags | namespaced, purpose-oriented | `voice.realtime_calls.enabled` |
| Test files | explicit test subject | `test_memory_service.py` |

Do not mix JSON field styles inside the same API. If a client-facing API already uses camelCase, document that contract and apply it consistently; do not transform casing ad hoc in each handler.

### 4.1 Names should encode units and semantics

Prefer `timeout_seconds`, `duration_ms`, `credit_amount_minor_units`, or `maximum_image_bytes` over vague names like `timeout`, `duration`, or `amount` when unit ambiguity could cause a defect.

Distinguish:

- `user_id`: the authenticated Juhi user ID.
- `provider_user_id`: an external identity identifier.
- `conversation_id`: a durable conversation identifier.
- `request_id`: one request's correlation ID.
- `idempotency_key`: client or server key preventing duplicate side effects.
- `model_run_id`: one specific model invocation.

---

## 5. Formatting and editor settings

Formatting MUST be automated and enforced in CI. Developers should not spend review time debating wrapping, whitespace, or import ordering.

### 5.1 `.editorconfig` baseline

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space

[*.{yml,yaml,json,md,sql,toml,py}]
indent_size = 4

[*.dart]
indent_size = 2

[Makefile]
indent_style = tab
```

If a formatter mandates a different indentation rule for a file type, the formatter takes precedence. The team MUST commit formatter configuration rather than depend on IDE defaults.

### 5.2 General rules

- One statement per line in application code.
- Avoid lines so long they hide conditions or make diffs hard to review; let the language formatter determine most wrapping.
- Keep imports grouped and deterministically sorted.
- Remove unused imports, dead code, commented-out implementations, and temporary debug prints before merge.
- Use trailing commas where required or recommended by the language formatter.
- Do not hand-format generated files. Regenerate them using the documented command.
- Markdown examples MUST be syntactically plausible and should not contain live secrets or personal information.

---

## 6. Flutter and Dart standards

### 6.1 Required toolchain discipline

- Pin the Flutter SDK version through the repository's chosen toolchain mechanism.
- Commit `pubspec.lock` for the application.
- Use a single agreed package-management workflow.
- Run `dart format` and `flutter analyze` before merge.
- Treat new analyzer warnings as defects unless a documented suppression is justified.
- Do not add a dependency for a small utility that can be implemented safely in a few readable lines.

### 6.2 Recommended baseline packages and tools

Use only what the repository has adopted; this is a suggested baseline rather than a requirement to add all packages at once.

- `flutter_lints` for baseline analysis.
- A selected state-management approach, such as Riverpod or Bloc, used consistently across features.
- A typed HTTP client layer with centralized auth and error handling.
- A serialization approach with generated models where it materially reduces drift.
- Mock/fake libraries for unit and widget tests.
- Integration-test tooling for real auth, deep links, media permission, and purchase flows.

Do not introduce a second state-management framework for a single feature without an architecture decision record (ADR).

### 6.3 `analysis_options.yaml` baseline

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  errors:
    invalid_annotation_target: ignore # Keep only if required by the chosen serializer.
  exclude:
    - build/**
    - '**/*.g.dart'
    - '**/*.freezed.dart'

linter:
  rules:
    avoid_dynamic_calls: true
    avoid_print: true
    cancel_subscriptions: true
    close_sinks: true
    directives_ordering: true
    no_leading_underscores_for_local_identifiers: true
    prefer_const_constructors: true
    prefer_final_locals: true
    require_trailing_commas: true
    unawaited_futures: true
```

Validate each rule against the selected Dart SDK and project packages before enabling the baseline; do not suppress a large set of warnings to get a green build. Keep exceptions narrow and commented.

### 6.4 Dart language rules

- Prefer sound null safety. Do not use `!` unless the invariant has already been established and cannot be represented more safely.
- Avoid `dynamic` at application boundaries. Parse external JSON into validated, typed models.
- Prefer `final` for bindings that are not reassigned and `const` for compile-time constants.
- Use enums or sealed classes for states instead of unrelated strings.
- Use immutable state objects. State updates should produce new state rather than mutate shared state in place.
- Avoid `BuildContext` use after an `await` unless the widget's mounted state is checked and the operation still makes sense.
- Cancel stream subscriptions and dispose controllers, focus nodes, audio players, and animation controllers.
- Do not create expensive service objects or start asynchronous work in `build()`.
- Use keys when preserving identity matters in list rendering; do not add arbitrary keys without a reason.
- Keep widgets focused. Extract a widget when it has a meaningful purpose, reusable behavior, or materially improves readability—not merely to reduce line count.

### 6.5 Mobile architecture convention

A feature-first structure is preferred:

```text
lib/
├── app/
│   ├── app.dart
│   ├── router.dart
│   └── bootstrap.dart
├── core/
│   ├── config/
│   ├── errors/
│   ├── logging/
│   ├── network/
│   ├── security/
│   ├── theme/
│   └── widgets/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── chat/
│   ├── memory/
│   ├── companion_profile/
│   ├── media/
│   ├── billing/
│   └── settings/
└── main.dart
```

Each feature should expose a small public surface. Keep internal data sources private to that feature unless a shared abstraction is deliberately defined.

### 6.6 UI and state rules

- Widgets render state and dispatch user intent; they do not implement billing, memory conflict resolution, or provider routing.
- State classes must model loading, success, empty, partial, retryable error, and unrecoverable error states where relevant.
- Do not render raw backend errors to users. Map typed error codes to clear, localized messages.
- Network requests should have explicit cancellation or stale-response behavior when users navigate away or change selected conversations.
- Long lists should be lazy, paginated, and keyed by stable IDs.
- Animations must respect reduced-motion settings where practical and should not block core controls.
- Avoid sending duplicate requests because the widget rebuilt. Place side effects in a notifier/controller/use case, not `build()`.

### 6.7 Example: typed UI state

```dart
sealed class ConversationLoadState {
  const ConversationLoadState();
}

final class ConversationLoading extends ConversationLoadState {
  const ConversationLoading();
}

final class ConversationLoaded extends ConversationLoadState {
  const ConversationLoaded(this.messages, {this.nextCursor});

  final List<ChatMessage> messages;
  final String? nextCursor;
}

final class ConversationFailed extends ConversationLoadState {
  const ConversationFailed(this.errorCode, {required this.canRetry});

  final String errorCode;
  final bool canRetry;
}
```

Do not represent every state as `isLoading`, `hasError`, `isEmpty`, and `isSuccess` booleans that can accidentally produce contradictory combinations.

---

## 7. Python and FastAPI standards

### 7.1 Python baseline

- Use type hints for all public functions, service methods, and module boundaries.
- Use Python's standard formatter and a fast linter selected by the team. `ruff format` and `ruff check` are a good combined starting point.
- Use `pyproject.toml` as the single home for Python tooling configuration where supported.
- Use a type checker such as mypy or Pyright for application code. Fix errors rather than disabling whole modules.
- Commit lock files or exact dependency constraints according to the selected package manager.
- Keep I/O at explicit boundaries: HTTP, database, queues, files, and model providers.
- Avoid module-level mutable state and import-time network calls.

### 7.2 Suggested Ruff and pytest baseline

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "ASYNC", "S", "SIM"]
ignore = []

[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
testpaths = ["tests"]
asyncio_mode = "auto"
```

Tune lint selections for the project's actual stack. Security-oriented lint rules can produce false positives; suppress findings only after reviewing the specific case and recording the reason. If using a pytest async plugin, pin and configure it consistently.

### 7.3 Python naming and typing

- Functions and variables use `snake_case`.
- Classes use `PascalCase`.
- Constants use `UPPER_SNAKE_CASE`.
- Use `Enum` or `Literal` for constrained values where useful.
- Prefer typed domain objects over dictionaries passed across many layers.
- Use `TypedDict` only when a dictionary shape is genuinely appropriate.
- Use `Protocol` for an interface when structural typing helps tests or alternate adapters.
- Avoid `Any`; if unavoidable at a third-party boundary, narrow it immediately after validation.
- Do not use mutable default arguments (`def f(items: list[str] = [])`).
- Use dataclasses or Pydantic models according to the layer; do not use one type indiscriminately for API schemas, DB models, and domain state.

### 7.4 FastAPI route handler rules

Routes are thin transport adapters. They should authenticate, validate, invoke a use case, and map the result to an API response.

```python
@router.post(
    "/v1/conversations/{conversation_id}/messages",
    response_model=CreateMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    conversation_id: UUID,
    payload: CreateMessageRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
) -> CreateMessageResponse:
    result = await service.create_message(
        actor_user_id=current_user.user_id,
        conversation_id=conversation_id,
        text=payload.text,
        client_request_id=payload.client_request_id,
    )
    return CreateMessageResponse.from_result(result)
```

This is an illustration, not a drop-in implementation. Adapt dependency injection, type definitions, and transaction management to the project's actual modules. The route must not trust a user ID supplied in the request body as the authorization identity.

### 7.5 Service layer rules

- Put business logic in explicit application/domain services.
- Pass authenticated actor identity to operations that read or mutate user-owned records.
- Do not accept a bare conversation ID and assume it belongs to the current user; enforce ownership in the query or service policy.
- Keep database transactions short. Do not hold a transaction open while waiting for an LLM, image provider, payment provider, or slow network request.
- Model long-running work as a durable job and use explicit status transitions.
- Use idempotency keys for repeatable requests with costly or irreversible effects.
- Return typed domain results and raise domain-specific errors for expected failure modes.

### 7.6 Async rules

- Use asynchronous clients for I/O inside async handlers and workers.
- Never perform long blocking file, network, CPU-bound, or synchronous provider work on the event loop.
- Offload CPU-heavy tasks to an appropriate worker or process pool.
- Use timeouts for every outbound network call.
- Use bounded retries with exponential backoff and jitter for transient failures only.
- Do not retry validation errors, authorization failures, or payment declines as though they were transient.
- Avoid unbounded `asyncio.gather` fan-out. Set concurrency limits and cancellation behavior.
- Do not swallow `CancelledError` or prevent task cancellation unless shutdown semantics require a carefully documented exception.

### 7.7 Error handling

Create a small, documented application error vocabulary, such as:

- `authentication_required`
- `permission_denied`
- `resource_not_found`
- `validation_failed`
- `rate_limited`
- `insufficient_credits`
- `provider_unavailable`
- `operation_in_progress`
- `internal_error`

Map these to stable API error codes and appropriate HTTP statuses. Do not expose raw exception messages, internal hostnames, table names, SDK payloads, or stack traces. A stable public error code is part of the API contract and should not change arbitrarily.

---

## 8. API and contract conventions

### 8.1 HTTP API rules

- Prefix public APIs with a version such as `/v1`.
- Use nouns for resource paths and HTTP verbs for intent.
- Use cursor pagination for message histories and other potentially large lists.
- Include a request/correlation ID in logs and appropriate response metadata.
- Define request and response schemas explicitly.
- Apply maximum lengths and size limits to text, URLs, uploaded metadata, and pagination parameters.
- Use consistent timestamps in ISO 8601 UTC format.
- Return a stable envelope or standard response shape consistently across endpoints.
- Keep internal-only endpoints inaccessible from the public network or protected by explicit service authentication.

### 8.2 Example error shape

```json
{
  "error": {
    "code": "provider_unavailable",
    "message": "Juhi could not complete this request right now.",
    "request_id": "req_example_123",
    "retryable": true
  }
}
```

The request ID is illustrative, not an authentication credential. End-user messages should be localized by the client where practical; internal diagnostics belong in protected logs.

### 8.3 Schema changes

- Public API changes must be reviewed for backward compatibility.
- Generate OpenAPI and client models through one documented source of truth where feasible.
- Avoid duplicating field definitions by hand in several places.
- If a response field must be deprecated, document the transition period and consumer impact.
- Add contract tests for endpoints used by the mobile application.

### 8.4 Idempotency

For message submission, media generation, payment processing, credit purchases, and other repeatable side effects:

1. Define the idempotency-key scope and expiry.
2. Persist the key with the authenticated user and operation.
3. Store the terminal result or operation ID.
4. On retry, return the original result rather than repeat the charge or provider operation.
5. Reject re-use of a key with a materially different request body.

---

## 9. PostgreSQL and SQL standards

### 9.1 SQL style

- Use lowercase `snake_case` for identifiers.
- Prefer plural table names and singular column names.
- Name primary keys `id`; name foreign keys `<entity>_id`.
- Use explicit constraint names, such as `fk_messages_conversation_id` and `uq_user_external_identity`.
- Explicitly list columns in queries and inserts; avoid `SELECT *` in production code.
- Prefer parameterized statements or the ORM's parameter binding; never concatenate untrusted values into SQL.
- Use transactions for invariants spanning multiple rows.
- Keep migrations small enough to reason about and roll forward safely.
- Use UTC timestamps and document the storage semantics.
- Use the database to enforce invariants that must hold under concurrency, not just application-level pre-checks.

### 9.2 PostgreSQL usage

- Use UUID or another deliberately selected immutable identifier scheme consistently.
- Use foreign keys and appropriate delete behavior for owned data.
- Use check constraints for bounded values where beneficial.
- Use partial and composite indexes only where access patterns justify them.
- Avoid over-indexing write-heavy tables. Every index has write, storage, and maintenance cost.
- Use `JSONB` for genuinely flexible metadata, not as a replacement for relational modeling of core business concepts.
- Use `pgvector` only for vector-retrieval use cases; preserve source metadata, ownership, deletion behavior, and embedding-model/version information.
- Keep media bytes in private object storage; store metadata and controlled object references in PostgreSQL.

### 9.3 ORM usage

- Keep ORM models close to the persistence layer.
- Do not use ORM entities as public response models.
- Avoid implicit lazy loading in request serialization.
- Use explicit query plans for complex reads and paginate large results.
- Avoid N+1 query patterns; use eager loading or purpose-built queries where justified.
- Keep session lifetimes short and scoped to a request or background unit of work.
- Do not share one ORM session concurrently across unrelated async tasks.

### 9.4 Migration rules

- Every schema change must be represented in a versioned migration.
- Never rely on a developer's local database state as proof that a migration works.
- Test upgrade paths against a disposable database in CI.
- Use expand-and-contract for potentially breaking changes: add compatible structures, deploy dual-compatible code, backfill, switch reads/writes, then remove old structures later.
- Large backfills should be resumable, observable, and run as controlled jobs rather than one long schema migration.
- Review locks and table-rewrite risks for large tables.
- Keep migrations forward-only in routine production practice; rollback should be planned, not assumed to be safe automatically.

---

## 10. AI, prompts, memory, and provider adapters

AI-specific code requires stronger discipline because the same request may be affected by prompt versions, model behavior, user memory, provider outages, and safety policy.

### 10.1 Provider-independent domain types

- Domain services MUST NOT return provider SDK response objects.
- Define internal request/response types for chat completion, image generation, speech recognition, speech synthesis, embeddings, and moderation.
- Keep provider-specific configuration in adapters.
- Add a capability registry describing which provider/model supports which operation, language, streaming behavior, content policy, and maximum payload.
- Provider routing must be explicit and observable. Do not silently send sensitive data to a new provider without a documented policy review.
- A provider fallback must preserve safety checks, privacy constraints, and user-visible behavior.

### 10.2 Prompt files are versioned artifacts

- Store prompts in version control, with an owner, stable identifier, version, intent, required inputs, output contract, safety notes, and evaluation coverage.
- Do not build large system prompts through scattered string concatenation across routes and utility files.
- Keep system policy, developer instructions, persona definition, retrieved memory, current conversation, and user message as clearly identified sections.
- Treat user messages, retrieved memories, uploaded documents, and tool results as untrusted data. They must not override system-level policies.
- Use structured output schemas for machine-consumed results instead of parsing free-form prose where feasible.
- Do not place secrets, hidden internal reasoning, private provider data, or instructions to bypass safety in prompts.
- Do not modify a production prompt without versioning it and running its applicable regression evaluations.

### 10.3 Prompt composition order

A conceptual composition order is:

1. System policy and non-negotiable safety constraints.
2. Product/application behavior and allowed tools.
3. Versioned companion persona and user-selected settings.
4. Retrieved memory and relationship context, labeled as contextual data.
5. Recent conversation context.
6. Current user message.

The final arrangement must comply with the selected model API's role semantics and limits. Retrieved data does not become trusted instructions merely because it is inserted into a prompt.

### 10.4 Memory code rules

- Do not store every message automatically as durable memory.
- Separate episodic, semantic, preference, relationship, and user-corrected memory types where product requirements need them.
- Persist source/provenance, confidence where applicable, created/updated timestamps, and user-visibility/deletion state.
- Give explicit user corrections precedence over inferred or stale facts.
- Apply ownership filters before semantic similarity ranking.
- Do not log full memories during retrieval debugging.
- Ensure deleted memories cannot reappear from summaries, caches, vector indexes, or derived artifacts.
- Use deterministic unit tests for memory selection and policy decisions; use evaluation datasets for model-dependent quality.

### 10.5 AI output parsing

- Validate structured output against a schema.
- Bound maximum response length and tool-call count.
- Reject unknown tool names and unauthorized arguments.
- Validate any URL, media reference, object ID, or identifier returned by a model before use.
- Treat model output as untrusted. It must not directly become SQL, shell commands, HTML, or privileged tool input.
- On parse failure, use a controlled repair attempt only if cost and safety policies permit; otherwise return a typed failure or safe fallback.

### 10.6 Model evaluation

Every meaningful prompt, routing, model, or memory retrieval change SHOULD run relevant evaluations for:

- Language quality in English, Hindi, Tamil, Tanglish, and Hinglish, with explicit coverage gaps documented.
- Persona consistency without overriding user preferences or safety.
- Factual memory correctness and correction handling.
- Prompt injection and tool misuse.
- Crisis and self-harm response behavior where applicable.
- Disallowed content and image-generation boundaries.
- Latency, token cost, provider failure, and retry behavior.

Use anonymized, synthetic, or consented evaluation data. Avoid copying production private conversations into permanent test fixtures.

---

## 11. Security-related coding rules

`security.md` is authoritative for the detailed threat model and release gates. This section defines day-to-day implementation requirements.

- Never hardcode API keys, provider secrets, signing keys, passwords, or production tokens.
- Never put privileged provider keys in a Flutter app, remote configuration readable by clients, or public repository.
- Verify authentication tokens using the supported server-side library and verify issuer, audience, signature, expiry, and relevant claims.
- Apply object-level authorization on every user-owned read and write. Knowing a UUID is not authorization.
- Use least-privilege service identities and separate development, test, staging, and production credentials.
- Validate all external input, including AI outputs, webhook bodies, uploaded files, client metadata, and callback URLs.
- Use TLS for transport and managed encryption for persisted data; document exceptions and key ownership.
- Redact logs and telemetry. Never log raw auth headers, session tokens, full conversation content, or image/audio payloads by default.
- Use allowlists for outbound network requests when URL fetching or web tools exist, to reduce SSRF risk.
- Protect payment webhooks with provider signature verification and replay/idempotency controls.
- Make account deletion and data export workflows authorization-checked and auditable.
- Dependency, container, secret, and static security scans MUST be part of CI before production release.

### 11.1 Unsafe example

```python
# UNSAFE: user-controlled SQL and no ownership condition.
query = f"SELECT * FROM conversations WHERE id = '{conversation_id}'"
```

### 11.2 Safer example

```python
# Illustrative SQLAlchemy-style code: bind parameters and scope to the actor.
statement = select(Conversation).where(
    Conversation.id == conversation_id,
    Conversation.user_id == actor_user_id,
)
conversation = await session.scalar(statement)
```

The actual ORM syntax may vary. The invariant is that the query itself scopes the resource to the authenticated owner, and user data is passed through parameter binding rather than string interpolation.

---

## 12. Logging, metrics, and observability

### 12.1 Structured logging

- Emit structured logs with timestamp, severity, service, environment, request ID, trace ID where available, and stable error code.
- Include user ID only as a controlled internal identifier where operationally justified; do not use it as a metric label.
- Keep high-cardinality or private values out of metric labels.
- Do not log complete prompt contents, memories, messages, transcripts, or media.
- Use a dedicated redaction layer for provider errors and request metadata.
- Logs should help answer: what failed, which operation was involved, whether it is retryable, and where to look next—without exposing private content.

### 12.2 Metrics

Prefer low-cardinality metrics such as:

- Request latency and error rate by route template and status class.
- Model latency, provider failure rate, token usage, and estimated cost by approved provider/model category.
- Image and voice job duration, success, retry, and abandonment rate.
- Credit reservations, confirmed charges, releases, and reconciliation mismatches.
- Memory retrieval latency and empty-result rate.
- Queue depth, age of oldest job, worker saturation, and retry count.

Do not create labels from arbitrary user content, conversation IDs, user IDs, raw exception strings, or complete model names if their cardinality is unbounded. Use safe dimensions and sampling.

### 12.3 Tracing

- Propagate correlation and trace context across API, worker, and provider adapter boundaries where supported.
- Do not put message text or other sensitive payloads into trace attributes.
- Record provider/model identifiers as bounded labels according to the routing registry.
- Ensure instrumentation respects consent and data handling policy.

---

## 13. Testing standards

Testing is part of the implementation, not a later activity. Select test scope based on risk and behavior rather than only on code coverage percentage.

### 13.1 Test layers

| Layer | Purpose | Examples |
|---|---|---|
| Static checks | Detect style/type/security issues early | Formatter, linter, type checker, secret scanner |
| Unit tests | Verify isolated rules | Memory ranking, entitlement checks, credit math |
| Component tests | Verify module behavior with fakes | Conversation service and provider adapter mapping |
| Integration tests | Verify real boundaries | PostgreSQL transactions, migrations, object storage permissions |
| Contract tests | Protect client/server compatibility | API schemas, error codes, pagination cursor |
| End-to-end tests | Validate important user journeys | Sign-in, send message, retry generation, delete memory |
| Security tests | Verify attack resistance | IDOR, prompt injection, SSRF, webhook replay |
| AI evaluations | Compare model-dependent quality and safety | Multilingual responses, memory accuracy, persona consistency |
| Load/resilience tests | Validate operational limits | Concurrent chat, queue spikes, provider outage |

### 13.2 Unit test rules

- Test observable behavior rather than private implementation details.
- Use deterministic inputs and fixed clocks/IDs where appropriate.
- Mock network/provider boundaries, not every internal function.
- Include negative cases and boundary conditions, not just the happy path.
- Test authorization with both valid owner and non-owner actor.
- Avoid depending on execution order or shared mutable fixtures.
- Do not use real user data in test fixtures.

### 13.3 AI-specific test rules

- Do not assert exact model wording unless testing a strict schema or deterministic transformation.
- Use criteria-based evaluation for model-dependent quality.
- Keep safety regression cases versioned and reviewed.
- Test both malicious instructions in direct user prompts and injection inside retrieved memory or uploaded content.
- Verify that provider failures never bypass moderation or tool authorization.
- Keep test datasets private when they contain sensitive examples and record their purpose and retention.

### 13.4 Coverage policy

Coverage metrics may help identify untested modules, but they are not proof of correctness. Set thresholds appropriate to the chosen toolchain and enforce critical path coverage for authentication, authorization, credit accounting, data deletion, and memory ownership. Require direct tests for high-risk invariants even when aggregate coverage is high.

---

## 14. Git, branches, commits, and pull requests

### 14.1 Branch names

Use short, searchable branch names:

```text
feat/memory-edit-controls
fix/duplicate-credit-charge
refactor/provider-adapter
docs/security-release-gate
chore/flutter-toolchain
```

Avoid including customer data, secrets, or sensitive incident details in branch names.

### 14.2 Commit messages

Use a consistent format such as Conventional Commits:

```text
feat(chat): add paginated message history
fix(billing): prevent duplicate credit settlement
refactor(ai): isolate provider-specific response types
test(memory): cover user correction precedence
docs(security): clarify media retention
```

A commit should represent one logical change where practical. Do not bundle unrelated formatting, behavior, and infrastructure changes when separate commits would improve reviewability.

### 14.3 Pull request requirements

Every PR should state:

- What changed and why.
- User or operational impact.
- How it was tested (specific commands or CI jobs).
- API, schema, prompt, migration, and configuration impact.
- Security/privacy considerations.
- Cost and latency implications if AI, image, voice, or storage usage changes.
- Rollback or feature-flag approach for risky changes.

Attach screenshots or short recordings for meaningful UI changes, and representative sanitized logs for complex operational changes. Never attach credentials or private conversation content.

### 14.4 Review checklist

Reviewers should verify:

- The code fits the documented architecture and has a clear owner.
- Naming and error handling are consistent.
- Authenticated identity is used for authorization; IDs from payloads are not trusted as proof of ownership.
- Inputs and model outputs are validated.
- Expensive calls have timeouts, limits, retries, and idempotency where required.
- Database transactions and migrations preserve invariants.
- Logs and analytics do not leak private content.
- Tests cover the important success and failure paths.
- Dependencies and public APIs have a clear reason for change.
- Documentation and operational playbooks are updated if behavior changed.

---

## 15. Dependency and configuration management

- Pin or lock dependency versions using the chosen package manager and commit its lock file where appropriate.
- Prefer maintained, widely adopted libraries with clear licensing and active security updates.
- Record why a new dependency is needed, especially for crypto, auth, storage, AI routing, and payment handling.
- Review transitive dependency risks; do not assume a popular package is automatically safe.
- Separate defaults from environment-specific configuration.
- Validate required configuration at startup and fail fast with a safe, actionable message if essential settings are missing.
- Do not make production startup silently fall back to insecure defaults.
- Keep feature flags typed, documented, and measurable. Avoid flags that remain forever without an owner or removal date.
- Never store secrets in `.env.example`; use placeholder values that are clearly invalid.
- Keep local development easy without weakening production authorization or skipping important validation.

### 15.1 Configuration rules

Each setting should document its name, purpose, required environments, default behavior, sensitivity, and validation. Prefer typed settings objects over scattered direct environment reads throughout the codebase.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        case_sensitive=True,
    )

    environment: str
    database_url: str
    firebase_project_id: str
    model_provider_timeout_seconds: float = 30.0
    max_user_message_characters: int = 8_000
```

Illustrative only: configure secret sources, required fields, validation bounds, and environment-specific behavior according to the actual deployment. Avoid reading environment variables in every route or provider adapter.

---

## 16. Performance and cost-conscious coding

Juhi's AI and media workloads can generate variable external cost. Code MUST put explicit bounds on operations likely to multiply latency, load, or spend.

- Define maximum input/output lengths, tool-call count, retrieval count, image size, audio duration, and concurrent jobs.
- Add timeouts to each provider request and propagate cancellation where safe.
- Use bounded retries with jitter; do not retry indefinitely.
- Use queues for image generation, transcription, and other work that may outlive a request.
- Reserve credits transactionally before costly operations, settle based on provider outcome and pricing rules, and release reservations on recoverable failure.
- Use caching only for data that is safe to cache, with explicit ownership and invalidation rules. Never use a shared cache key that allows one user's private memory or response to leak to another user.
- Paginate message history and memory search results.
- Avoid N+1 queries and repeated model calls for data already available in the request context.
- Use circuit breakers or provider health policies where appropriate to avoid cascading failure.
- Measure latency and cost before optimizing; keep optimizations backed by tests.

### 16.1 Avoid hidden duplicate AI calls

Each generation request should carry a unique operation ID. Record a bounded metadata row for each provider attempt. Retry only under a documented policy. Do not call the model once to classify a request and again to generate the response unless the quality gain justifies the latency and cost and the decision is measurable.

---

## 17. Documentation standards

- Public functions and non-obvious modules should have concise docstrings or documentation comments.
- Explain invariants, data lifecycle, and trade-offs—not line-by-line paraphrases of the code.
- Architecture decisions that are costly to reverse SHOULD be documented as ADRs with context, decision, alternatives, and consequences.
- Update relevant Markdown docs when APIs, schema, security controls, prompts, deployment, or operational procedures change.
- Keep examples executable or explicitly label them as illustrative.
- Mark TODOs with an owner or issue reference where possible. Do not leave vague `TODO fix later` notes in high-risk code.
- Avoid giant README files that duplicate every detail; use a concise root README and linked focused documents.

Suggested ADR format:

```markdown
# ADR-00X: <Decision title>

## Status
Proposed | Accepted | Superseded

## Context
What problem needs a decision?

## Decision
What will we do?

## Alternatives considered
What viable options were evaluated?

## Consequences
Benefits, limitations, security/cost impact, and migration needs.
```

---

## 18. Automation and CI quality gates

CI should run the same deterministic checks developers can run locally. Required jobs should be fast enough to run consistently and should not need production secrets for normal pull requests.

### 18.1 Suggested PR pipeline

1. Check formatting.
2. Run linters and type checkers.
3. Run unit tests.
4. Run integration tests requiring disposable databases/services.
5. Validate migrations and API contracts.
6. Scan for secrets and prohibited artifacts.
7. Run dependency and container scans.
8. Build the mobile application and backend container.
9. Run selected security tests for changes to auth, billing, storage, memory, or provider tools.
10. Publish test results and relevant coverage summaries.

### 18.2 Local commands (illustrative)

```bash
# Flutter app
cd apps/mobile
dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test

# Python API
cd ../../services/api
ruff format --check .
ruff check .
mypy app
pytest -q

# Database migrations
# Use the exact command supported by the chosen migration framework.
# Run migration tests against a clean, disposable PostgreSQL database.
```

Adjust paths, configured commands, and type checker options to the actual repository. Once adopted, these commands must be documented in the root README or CONTRIBUTING guide and match CI behavior.

### 18.3 Release gates

A release SHOULD NOT proceed if any of the following is true:

- Formatting, linting, type checks, or required tests fail.
- A schema migration has not been tested against a clean database.
- Security checks reveal an unresolved critical or high-severity issue without approved risk acceptance.
- Authentication or ownership tests are missing for new user-owned resources.
- Billing/credit flows lack idempotency and reconciliation coverage.
- A prompt/model-routing change has no relevant safety and quality evaluation.
- A production configuration change has not been validated in staging.
- A release introduces unbounded provider spend or an unobservable background job.

---

## 19. Code review: common anti-patterns to reject

Reject or request redesign when code:

- Adds business rules to widgets or route handlers.
- Uses broad `except Exception` blocks to hide failed operations.
- Swallows errors and reports success to the UI.
- Uses global mutable state for user-specific data.
- Relies on client-supplied role, price, user ID, or credit balance as authoritative.
- Loads an arbitrary object by ID without a user-ownership constraint.
- Uses `SELECT *` or dynamically interpolates untrusted SQL.
- Stores generated media publicly by default.
- Makes an LLM output trigger privileged tool execution without validation and authorization.
- Logs raw prompt, transcript, user memory, authentication token, or payment payload.
- Adds unbounded retries, unbounded queue concurrency, or unbounded chat history to context.
- Adds a new provider SDK throughout the codebase instead of one adapter.
- Places prompt instructions in many unrelated files with no versioning or evaluation.
- Changes production behavior through an undocumented environment variable.
- Adds a new abstraction with no clear consumer or testability benefit.
- Disables a linter globally to avoid fixing local issues.

---

## 20. Definition of Done

A change is ready to merge when the relevant items below are satisfied.

### Correctness and design

- [ ] The change meets the agreed acceptance criteria.
- [ ] Code is in the correct layer and does not introduce circular dependencies.
- [ ] Names, types, boundaries, and error states are clear.
- [ ] Public API and data model changes are backward-compatible or have a migration plan.

### Quality and tests

- [ ] Formatter, linter, and type checker pass.
- [ ] Tests cover successful behavior, failures, and relevant edge cases.
- [ ] Concurrency/idempotency behavior is tested for operations with side effects.
- [ ] AI changes have relevant evaluation cases.
- [ ] Migrations run against a clean disposable database.

### Security and privacy

- [ ] Authentication and resource ownership are enforced server-side.
- [ ] Inputs and external/model outputs are validated.
- [ ] No secrets or sensitive content are added to logs, fixtures, or repository history.
- [ ] Retention and deletion behavior is covered when data lifecycle changes.
- [ ] New provider/data sharing is reviewed against privacy policy.

### Operations and documentation

- [ ] Timeouts, retries, limits, and idempotency are defined for external operations.
- [ ] Metrics/logs can diagnose failure without revealing user content.
- [ ] Cost and latency implications are reviewed for AI/media changes.
- [ ] Relevant docs, runbooks, and configuration examples are updated.
- [ ] Rollback or feature-flag strategy exists for risky changes.

---

## 21. Adoption strategy

Do not attempt to rewrite the entire codebase to meet this standard in one large change. Adopt it incrementally:

### Phase 1 — Establish the baseline

- Commit formatter and linter configuration for Flutter, Python, and SQL.
- Add basic CI checks and document local commands.
- Define folder boundaries and error conventions.
- Block secrets and private user content in fixtures and logs.

### Phase 2 — Protect high-risk behavior

- Add object-level authorization tests for every user-owned resource.
- Add idempotency and transactional tests for paid generation and credits.
- Add data deletion, memory correction, and retention tests.
- Add prompt injection and tool-authorization evaluation cases.

### Phase 3 — Improve operational maturity

- Add contract tests, migration tests, bounded load tests, and provider failure simulation.
- Make observability and cost controls consistent across model adapters.
- Add dependency policy and staged security release gates.
- Revisit style deviations and remove unnecessary suppressions.

### Phase 4 — Maintain the standard

- Revisit the document when the stack changes materially.
- Use ADRs for significant exceptions.
- Remove obsolete rules and unsupported examples.
- Track repeat review findings and automate frequent checks.

---

## 22. Final engineering rule

**Write code so another engineer can safely change it six months later without needing the original author.** The style system should support a dependable AI companion: one that preserves user trust, handles personal data carefully, behaves consistently across languages, and grows without turning every new feature into a risky rewrite.

When a project-specific decision conflicts with this guide, follow the approved architecture and security documents, record the reason for deviation, and update this guide if the exception becomes the new standard.
