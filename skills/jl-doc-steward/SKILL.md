---
name: jl-doc-steward
description: Use only when the user explicitly invokes $jl-doc-steward or explicitly asks JL Docs Steward to create, update, synchronize, audit, or restructure repository documentation, including README, ADR, API, architecture, design/RFC, CHANGELOG, CONTRIBUTING/DEVELOPMENT, AGENTS.md, or CLAUDE.md.
---

# JL Docs Steward

## Contract

Maintain a small, accurate documentation set whose claims can be traced to the
repository, an accepted decision, or user-provided facts. Treat source code,
machine-readable contracts, configuration, CI, and accepted decisions as
evidence; never turn a plausible guess into project truth.

Operate only after explicit invocation. An audit-only request is read-only.
Creating, synchronizing, or refining documentation authorizes edits to the
requested documentation scope, not unrelated code or configuration.

## Select the operation

- **Create:** add a missing document only when the user requested that document
  or its need follows directly from the requested scope.
- **Synchronize:** start from the code/configuration diff and update only the
  documents whose durable claims changed.
- **Audit:** report unsupported, stale, duplicated, conflicting, or missing
  documentation without editing files.
- **Refine:** improve structure and expression without silently changing the
  documented contract or decision.

## Inspect before writing

1. Read repository-level instructions and the existing documentation index or
   conventions. Inspect `AGENTS.md`, `CLAUDE.md`, `README*`, `docs/`, package
   manifests, build files, CI workflows, and documentation tooling when present.
2. For synchronization, inspect the relevant Git diff, source, tests, schemas,
   generated artifacts, and accepted decision records. Do not infer the change
   from a commit title alone.
3. Identify the source of truth for each claim. Keep an internal ledger of:
   claim, evidence path, affected document, and confidence gap.
4. Preserve the repository's language, filenames, directory layout, Markdown
   conventions, and generated/manual ownership boundaries.
5. If a material fact cannot be established, omit it from authoritative text
   and report the gap. Do not fill the gap with generic content or invented
   commands.

Read [writing-principles.md](references/writing-principles.md) before authoring
or restructuring any document.

## Route by document type

Update only the types whose purpose matches the requested information:

| Document | Durable purpose | Use when |
| --- | --- | --- |
| README | Human orientation and fastest successful start | Public purpose, setup, entry points, or basic usage changed |
| ADR | Why an important decision was made | A consequential choice and its actual alternatives need a durable record |
| API docs | Consumer-visible contract | Endpoints, schemas, authentication, errors, compatibility, or examples changed |
| Architecture docs | Current enduring system structure | Boundaries, responsibilities, dependencies, runtime flows, or deployment changed |
| Design doc/RFC | A proposal for review | A significant change needs goals, options, trade-offs, and validation before implementation |
| CHANGELOG | Curated notable release history | A user-visible or compatibility-relevant released/unreleased change occurred |
| CONTRIBUTING/DEVELOPMENT | Human development workflow | Setup, contribution process, commands, or quality gates changed |
| AGENTS/CLAUDE | Durable agent instructions | Agent-relevant commands, constraints, boundaries, or verification rules changed |

For README work, use **REQUIRED SUB-SKILL:** `jl-readme-blueprint-generator`.
Treat its output as a draft and verify every retained statement against the
actual repository; its assumptions never override repository evidence.

For ADR work, use **REQUIRED SUB-SKILL:**
`jl-architecture-decision-records`. Preserve its confirmation and lifecycle
rules. Do not create an ADR for a trivial implementation choice or invent
alternatives that were never considered.

For API, architecture, design/RFC, CHANGELOG, or
CONTRIBUTING/DEVELOPMENT work, read
[document-types.md](references/document-types.md).

For `AGENTS.md` or `CLAUDE.md`, read
[agents-and-claude.md](references/agents-and-claude.md). Keep the external
format semantics separate from JL authoring policy as marked there.

## Keep one source of truth

- Link instead of copying detailed material between README, architecture docs,
  RFCs, ADRs, API references, and agent instructions.
- Update a generator input or machine-readable contract before its generated
  output. Never hand-edit a generated document unless the repository explicitly
  treats it as editable.
- Keep current-state documentation factual. Keep proposals and historical
  rationale in RFCs and ADRs with an explicit status.
- Preserve useful existing content and links. Remove or replace text only when
  evidence shows it is stale, duplicated, or in the wrong document type.
- Never expose credentials, private endpoints, production data, or internal
  operational details that the repository does not intentionally document.

## Verify and report

1. Re-read the changed documents against their evidence and the document-type
   contract.
2. Check referenced paths, anchors, links, examples, version names, and commands.
   Run existing documentation linters, generators, or contract checks when they
   are safe and relevant. Do not run deployment, migration, destructive, or
   production commands merely to validate prose.
3. Review the final Git diff for unrelated rewrites, duplicated truth, generated
   files edited by hand, precise prose assertions, and unsupported claims.
4. Report documents created or changed, evidence used, checks actually run, and
   unresolved gaps. Distinguish a rendered/linted document from a production-
   verified procedure.
