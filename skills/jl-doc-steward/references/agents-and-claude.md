# AGENTS.md and CLAUDE.md

This reference separates external format semantics from JL authoring policy.
Do not present the JL policy as part of the external standard.

## External semantics to preserve

### Open AGENTS.md format

- The canonical filename is `AGENTS.md`; the file is ordinary Markdown with no
  required headings.
- It complements README by carrying agent-focused project context, commands,
  tests, conventions, and constraints.
- A root file provides repository guidance. Nested files provide more specific
  subtree guidance, and closer guidance takes precedence when instructions
  conflict.
- Treat the file as living documentation.

Source: [AGENTS.md open format](https://agents.md/) and its
[MIT-licensed repository](https://github.com/agentsmd/agents.md).

### Codex discovery behavior

- Codex reads instructions once at the beginning of a run/session.
- At global scope, Codex uses `AGENTS.override.md` when non-empty; otherwise it
  uses `AGENTS.md`.
- At project scope, Codex walks from the project root toward the current working
  directory. In each directory it checks `AGENTS.override.md`, then `AGENTS.md`,
  then configured fallback names, and includes at most one file per directory.
- Files are concatenated root-to-leaf, so guidance nearer the working directory
  appears later and overrides broader guidance.
- Empty files are skipped. The default combined project-instruction limit is 32
  KiB and can be configured with `project_doc_max_bytes`.

Source: [OpenAI: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md).

### Claude Code compatibility

- Claude Code reads `CLAUDE.md`, not `AGENTS.md` directly.
- A `CLAUDE.md` can import `AGENTS.md` with `@AGENTS.md`; relative imports are
  resolved from the importing file.
- A symlink from `CLAUDE.md` to `AGENTS.md` also works when no Claude-specific
  additions are needed, but symlink support is less portable on Windows.
- Claude-specific instructions may follow the import instead of duplicating the
  shared instructions.

Source: [Anthropic: How Claude remembers your project](https://code.claude.com/docs/en/memory#agents-md).

## JL authoring policy

### Investigate

Before creating or updating an instruction file, inspect the actual repository:

- existing `AGENTS.md`, overrides, `CLAUDE.md`, and other agent-rule files;
- README, CONTRIBUTING/DEVELOPMENT, architecture docs, ADRs, and docs indexes;
- package/workspace manifests, task runners, CI workflows, test/lint/type/build
  configuration, and generated-code markers;
- directory boundaries that genuinely use different commands, languages,
  ownership, safety rules, or architectural constraints.

Resolve every command and path from repository evidence. Run only safe checks
needed to confirm syntax or behavior; never deploy, migrate, rotate secrets, or
touch production merely to validate an instruction.

### Write the root AGENTS.md

Use the smallest set of sections that gives an agent executable project context:

1. Brief repository purpose and a map of important entry points
2. Exact setup and development commands when agents need them
3. Relevant lint, type-check, test, build, and documentation gates
4. Architecture or dependency invariants easy for an agent to violate
5. Repository-specific code and test conventions not obvious from tooling
6. Safe change boundaries: always allowed, ask first, and prohibited operations
7. Documentation synchronization rules
8. Links to authoritative README, architecture, API, ADR, and contribution docs

Keep operational guidance direct and verifiable. Explain a prohibition with the
safe path when one exists. Reserve formatter and lint rules for their tools.

Do not include generic engineering advice, personality prompts, temporary task
plans, full architecture explanations, copied README sections, inferred team
process, secrets, or commands that were not verified. Keep the instruction chain
well below the configured byte limit; there is no mandatory line count.

### Add nested guidance conservatively

Create a nested `AGENTS.md` only when its subtree has a real different command,
toolchain, generated-code rule, safety boundary, ownership rule, or architecture
constraint. Write only the differences and additions; do not copy the root file.
Do not generate one mechanically for every package in a monorepo.

Update existing files in place after checking their scope. Preserve valid local
rules, remove contradictions, and link to canonical detail rather than allowing
root and nested files to drift.

### Create the CLAUDE.md compatibility entry

When Claude compatibility is in scope, prefer this portable root entry:

```markdown
@AGENTS.md
```

If an existing `CLAUDE.md` has real Claude-specific guidance, preserve it below
the import. If the repository already standardizes on symlinks and needs no
Claude-only guidance, keep that convention instead. Never maintain a copied
second body.

For every nested `AGENTS.md` that must also govern Claude Code, add an adjacent
thin `CLAUDE.md` import or preserve an equivalent existing compatibility
mechanism. Do not add nested compatibility files when no nested AGENTS guidance
was justified.

### Audit

Confirm that:

- each command and path exists and matches repository tooling;
- root and nested scopes do not conflict unintentionally;
- closer files contain only meaningful local differences;
- `CLAUDE.md` imports or links the intended `AGENTS.md` without duplicate truth;
- durable constraints live here while capabilities and reusable workflows stay
  in Skills;
- no instruction requests unauthorized, destructive, secret-bearing, or
  production actions by default.
