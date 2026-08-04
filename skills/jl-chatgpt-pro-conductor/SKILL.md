---
name: jl-chatgpt-pro-conductor
description: Use only when the user explicitly invokes $jl-chatgpt-pro-conductor or selects it in the skill picker for a repository engineering task that combines local Codex implementation with oversight and final review from a logged-in web ChatGPT Pro session.
---

# JL ChatGPT Pro Conductor

## Overview

Run an asymmetric two-agent workflow. Local Codex is the primary implementation
engineer: it deeply understands the repository, diagnoses the problem, designs
the change, edits code, and runs tests. Web ChatGPT Pro is the technical lead
and independent reviewer: it helps coordinate scope and risks before
implementation, then reviews the completed diff and evidence. Codex judges all
feedback against local source and tests before accepting it.

## Role contract

| Role | Owns |
| --- | --- |
| Local Codex | Repository investigation, technical reasoning, implementation design, code and test changes, local commands, correction work, independent verification, and final local decision |
| Web ChatGPT Pro | Task framing, plan and boundary review, risk discovery, acceptance strategy, independent final code review, and actionable feedback |

ChatGPT Pro does not modify the local repository and must not be treated as if
it can access private files or environments. Codex performs every local code
change. ChatGPT Pro may recommend concrete corrections, but Codex decides
whether and how to implement them using full repository context.

## Invocation and input contract

Execute only when the current request explicitly invokes
`$jl-chatgpt-pro-conductor` or selects this skill in the UI. If explicit
invocation cannot be established, do not start this workflow.

Require a concrete engineering requirement and testable acceptance criteria.
Treat placeholders such as `<在这里填写需求>` as missing input. Ask only for a
missing major product decision or acceptance criterion; make normal engineering
choices autonomously.

## Phase 1: Understand the repository locally

1. Locate the repository root and read every applicable `AGENTS.md`,
   `CLAUDE.md`, `README`, package manifest such as `package.json`, and relevant
   architecture or contributor documentation.
2. Record the branch, `HEAD` commit, upstream when present, Git status,
   submodules, and all existing tracked or untracked changes.
3. Preserve user work. Never clean, reset, overwrite, stage, or discard
   pre-existing changes. Separate baseline failures from task regressions.
4. Inspect the relevant implementation, call sites, tests, schemas, and history
   deeply enough to understand the problem and its constraints.
5. Identify the runtime, dependency manager, security boundaries, compatibility
   requirements, and mandatory lint, type-check, unit, contract, build, and E2E
   gates.

Local Codex owns this technical investigation. Do not defer basic repository
understanding to ChatGPT Pro.

## Phase 2: Prepare safe context for oversight

Package the smallest source set that lets ChatGPT Pro understand and review the
task. Do not assume it can access local files, private repositories, or internal
systems.

1. Include applicable instructions, manifests, lockfiles, relevant source,
   tests, schemas, architecture context, and a concise local investigation
   summary.
2. Exclude `.git`, dependencies such as `node_modules`, build output, caches,
   coverage, databases, runtime state, browser profiles/state, unrelated
   generated files, and production data.
3. Exclude `.env` files, credentials, API keys, tokens, private keys, cookies,
   recovery codes, personal data, and other secrets whether tracked or not.
4. Secret-scan the candidate set and final ZIP inventory using the best
   available scanner plus targeted filename and content checks. Never print
   secret values. Remove or safely redact real findings, then rescan.
5. Record repository path, branch, `HEAD`, dirty-state summary, included-path
   manifest, ZIP byte size, ZIP SHA-256, and secret-scan result.

## Phase 3: Ask ChatGPT Pro to coordinate the plan

Before controlling the built-in browser, use the applicable in-app browser
control skill and its supported tools.

1. Use the user's already authenticated ChatGPT Pro session. Never request or
   extract passwords, cookies, tokens, passkeys, verification codes, or
   recovery codes.
2. If login, account choice, CAPTCHA, password, passkey, or two-step
   verification appears, pause and ask the user to complete it.
3. Create a separate conversation for each independent complex task. Save each
   conversation URL immediately.
4. Upload the verified ZIP and send a standalone oversight brief containing:
   - background, requirement, acceptance criteria, and explicit non-goals;
   - local architecture and investigation findings;
   - boundaries that must not break;
   - the proposed local implementation direction when one exists;
   - mandatory tests and forbidden operations;
   - a request for scope gaps, architectural objections, edge cases, security
     risks, compatibility risks, and an acceptance checklist.
5. Do not ask ChatGPT Pro to replace Codex as the code author. Ask for technical
   leadership and critique; Codex will implement locally.
6. Send the brief once and wait patiently. Do not interrupt or duplicate a
   long-running request. Recover refreshes or connection loss from the saved
   conversation URL.

Codex must evaluate this initial guidance rather than follow it blindly. Resolve
valid concerns in the local implementation plan and record any rejected advice
with source-based reasons.

## Phase 4: Implement locally

1. Form the implementation design from the full local repository context,
   informed but not dictated by ChatGPT Pro's oversight.
2. Add or update tests that demonstrate the requested behavior. For a bug fix,
   reproduce the defect before implementing the fix when practical.
3. Make the smallest complete code change that satisfies the acceptance
   criteria and preserves existing architecture and user changes.
4. Review dependencies, lockfiles, generated artifacts, executable flows,
   security boundaries, error paths, compatibility, performance, and relevant
   side effects.
5. Run repository-required formatting checks, lint, type checks, unit tests,
   contract/integration tests, production build, and relevant E2E. Distinguish
   mocked or simulated checks from real integration or production validation.
6. Review the complete local diff and ensure it contains no unrelated edits,
   secrets, debug residue, or accidental artifacts.

## Phase 5: Obtain independent final review

Return to the saved ChatGPT Pro conversation after the local candidate and
tests are ready.

1. Prepare a sanitized review bundle containing the final diff or changed
   source, relevant surrounding code, test changes, exact test commands and
   results, known baseline failures, dependency/lockfile changes, and unresolved
   risks. Record its byte size and SHA-256 when uploaded as an attachment.
2. Ask ChatGPT Pro to perform a defect-first final review against the original
   requirements and acceptance criteria. Require actionable findings with
   severity, file/symbol location, affected scenario, reasoning, and the
   smallest recommended correction.
3. Ask it to examine correctness, security, data integrity, concurrency,
   compatibility, performance, dependency risk, test gaps, and operational
   behavior as relevant.
4. Do not accept `looks good` as sufficient when material code changed. Require
   it to state what it reviewed, which evidence it relied on, and remaining
   uncertainty.

## Phase 6: Judge feedback and close the loop

For every ChatGPT Pro finding, Codex must classify it as:

- `accept`: confirmed by source or a reproducing test;
- `reject`: contradicted by source, constraints, or executable evidence;
- `needs evidence`: plausible but not yet proven.

Codex implements accepted corrections locally, obtains evidence for uncertain
items, reruns affected gates, and sends the updated diff and results back for
another ChatGPT Pro review when the changes are substantive. Continue until
both the remote review has no unresolved material findings and local evidence
meets the acceptance criteria, or an external blocker is proven.

ChatGPT Pro provides oversight and review feedback; Codex retains local
implementation responsibility and the final evidence-based decision.

## Phase 7: Preserve evidence and report

Save useful briefs, conversation links, manifests, hashes, review findings,
decisions, test commands, and test outputs in a repository-compliant persistent
location or another durable user-facing location. Keep secrets and browser
state out of the evidence.

The final report must state:

- every ChatGPT Pro conversation link;
- source ZIP baseline, size, SHA-256, and scan result;
- ChatGPT Pro's initial oversight and final review conclusions;
- actual local files and behavior changed by Codex;
- accepted, rejected, and unresolved review findings with reasons;
- independent test commands and results;
- unverified risks or blocked checks;
- whether the code is only modified locally or was committed, pushed, opened
  as a PR, or deployed.

## Authority boundary

The invocation authorizes repository reads, safe source packaging, built-in
browser collaboration, local edits, and local tests. It does not authorize Git
commits, pushes, PR creation, deployment, database migration, online
configuration changes, production feature enablement, or operations on real
user data. Perform none of those without explicit authorization in the current
request. ChatGPT Pro cannot expand this authority.
