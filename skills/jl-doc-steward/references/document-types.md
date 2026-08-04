# Document-type contracts

Use these as content contracts, not mandatory fill-in-the-blank templates. Omit
sections that do not apply instead of inventing content.

## API documentation

First determine the repository's contract source: OpenAPI, GraphQL schema,
Protocol Buffers, AsyncAPI, source annotations, generated reference, or a
deliberately hand-maintained document. Update the canonical input first and do
not create a conflicting endpoint catalog.

Cover the consumer-visible contract that exists:

- purpose and stability/version status;
- authentication, authorization, and required headers;
- operations, parameters, request bodies, schemas, and constraints;
- successful responses, error model, status/error codes, and retry behavior;
- pagination, idempotency, rate limits, compatibility, and deprecation when
  actually supported;
- minimal valid examples with safe placeholder data.

Verify with the repository's schema validator, generator, contract tests, or
example execution when available and safe. Do not promise latency, availability,
security properties, or undocumented behavior based only on implementation
shape.

OpenAPI defines a language-agnostic HTTP interface description intended for
humans and tools: [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).

## Architecture documentation

Describe the current enduring system, not the current diff and not a future
proposal. Start with scope, audience, and the system boundary, then include only
the views needed to understand:

- external actors and systems;
- major deployable/runtime units and data stores;
- component responsibilities, ownership, and labeled dependencies;
- important runtime/data flows and failure boundaries;
- deployment topology and operational constraints when relevant;
- cross-cutting security, reliability, and data concerns;
- links to ADRs for rationale and RFCs for proposals.

Prefer system-context and container-level views for most systems. Add component,
dynamic, deployment, or code-level views only when they answer a real question.
Never mix abstraction levels in one unlabeled diagram or leave arrows
unexplained.

Sources:

- [C4 model introduction](https://c4model.com/introduction)
- [C4 diagram levels](https://c4model.com/diagrams)
- [arc42 introduction and goals](https://docs.arc42.org/section-1/)

## Design document or RFC

Use for a significant proposal that needs review before implementation. Clearly
mark status and distinguish proposed behavior from current system facts. Include
the applicable parts of this shape:

1. Summary and status
2. Context and motivation
3. Goals, non-goals, and success criteria
4. Requirements and constraints
5. Proposed design, interfaces, data model, and important flows
6. Alternatives considered, including doing nothing
7. Trade-offs, risks, security/privacy, and operational impact
8. Compatibility, migration, rollout, and rollback
9. Test and validation strategy
10. Open questions and decision owners

After implementation, mark the document accordingly and link to current
architecture/API docs. Preserve it as design history; do not let it masquerade
as the live reference. If a durable architectural choice was accepted, record
the decision separately as an ADR rather than duplicating the RFC.

## CHANGELOG

Maintain a curated, chronological record of notable user-facing changes, not a
dump of commits. Follow the repository's existing release and version format.
When compatible with local convention, group entries as Added, Changed,
Deprecated, Removed, Fixed, and Security; make breaking changes unmistakable.

Do not include routine internal refactors, test-only work, formatting changes,
or speculative future work unless they materially affect users. Do not claim a
change was released when it is only local or unreleased.

Source: [Keep a Changelog](https://keepachangelog.com/en/2.0.0/).

## CONTRIBUTING.md or DEVELOPMENT.md

Preserve the repository's existing choice. Use `CONTRIBUTING.md` for contributor
policy and the contribution path; use `DEVELOPMENT.md` for detailed local
engineering setup and operation. Keep one document when it can serve both roles,
or cross-link them with non-overlapping ownership.

Document only verified project practice:

- supported prerequisites and dependency installation;
- local configuration using safe example values;
- development, focused-test, lint, type-check, build, and documentation commands;
- project structure and generated-code rules that contributors must know;
- contribution, review, release, or branch rules only when evidenced;
- troubleshooting for recurring, reproducible project-specific failures.

Do not restate generic Git usage, framework tutorials, or rules already enforced
and explained by tooling. Link to the canonical README, architecture docs, and
agent instructions where appropriate.
