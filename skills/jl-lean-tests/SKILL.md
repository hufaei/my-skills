---
name: jl-lean-tests
description: Use when the user asks to design, add, simplify, or review tests, or when $jl-engineering-orchestra routes test work here. Keep tests focused on meaningful failures and stable contracts; do not trigger for ordinary implementation that does not request test work.
---

# JL Lean Tests

## Core rule

Every test must name the production failure it would catch. If that failure is
not meaningful, probable, or contractually important, do not add the test.

## Select the smallest useful test surface

1. State the behavior or contract at risk.
2. Name the realistic production change that would make the test fail.
3. Choose the lowest-cost test level that observes the real behavior.
4. Derive expected values independently of the implementation.
5. Prefer one strong test over several near-duplicates.

## Write tests for

- Core business rules and externally observable behavior.
- Bug reproductions that fail for the actual defect.
- Security and data-integrity boundaries.
- Stable API, protocol, schema, compatibility, and workflow contracts.
- Error paths whose mishandling causes a meaningful user or operational
  failure.

## Usually do not write tests for

- Exact prose, punctuation, headings, or formatting unless the text itself is
  a legal, protocol, localization, snapshot, or public API contract.
- Private methods, internal call order, source layout, grep results, or symbol
  names.
- Assertions that mocks were called instead of assertions on real behavior.
- Coverage targets without an identified failure.
- Trivial getters, framework behavior, or generated code.
- Broad regression tests that repeat stronger existing coverage.
- `not.toHave...` or other absence assertions merely proving removed code stays
  removed.

An absence assertion is justified only when absence is itself the security or
business contract, such as not exposing a secret, not granting unauthorized
access, or not emitting a forbidden protocol field.

## Review existing tests

Reject or simplify a test when it survives a meaningful mutation, depends on
the implementation to calculate its expected value, breaks on harmless
refactoring, or protects no named failure. Keep test utilities in the test
surface rather than adding production hooks solely for tests.

Report what was intentionally left untested and why when the omission carries
residual risk.
