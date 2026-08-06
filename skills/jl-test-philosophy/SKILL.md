---
name: jl-test-philosophy
description: Use when the user asks to design, write, revise, simplify, or review automated tests or test strategy, or when $jl-engineering-orchestra routes test decisions here. Shape a coherent, maintainable suite that buys decision-relevant confidence in meaningful behavior, risk, and contracts. Do not trigger for ordinary implementation that neither requests nor routes test work.
---

# JL Test Philosophy

## Contract

Treat tests as evidence for engineering decisions, not inventory for code. Shape
the suite as a coherent model of meaningful behavior and risk. Let stable contracts
and distinct risks determine its structure; let development history supply evidence,
not a prescribed list of permanent tests.

Optimize for **decision confidence per maintenance cost**. Each test should add
distinct evidence about a material behavior, invariant, boundary, or risky change.
Independent evidence at another boundary may overlap when a high-impact failure
justifies defense in depth. Growth is justified when it adds meaningful confidence.

Honor the caller's mode and authority. Design and review requests return analysis
without modifying files. Write or revise tests only when implementation is requested,
and do not reshape production code merely to make testing convenient.

## Decide before writing

Inspect the changed behavior and existing suite first. For every proposed test,
establish:

1. **Confidence:** what engineering decision will this evidence support?
2. **Risk:** what plausible fault, regression, or misunderstanding could it expose,
   and what would the consequence be?
3. **Contract:** what stable, observable behavior or invariant should remain true?
4. **Contribution:** what confidence does this add beyond existing coverage, or why
   does a high-impact risk need independent evidence at another boundary?
5. **Surface:** where is the least costly stable boundary that still observes the
   real behavior faithfully?

Then choose deliberately among:

- run an existing test unchanged;
- strengthen or generalize an existing test;
- replace several examples with one table, invariant, or property;
- add a genuinely new test;
- merge or delete redundant tests;
- use a temporary characterization test around uncertain legacy behavior;
- verify another way and add no permanent test.

Review feedback, a production-code edit, or a bug fix does not automatically earn
a new regression test.

## Match the test to the change

### New behavior

Protect acceptance behavior, core rules, important partitions, and stable public
contracts. Do not mirror every implementation unit. TDD is an execution-order
choice owned by the user or calling workflow; this Skill neither forces nor
forbids it.

### Bug fix or review correction

First ask why the current suite did not provide the needed signal. Add a regression
test only when the defect escaped useful coverage, represents a plausible recurring
fault, violates an intentionally stable contract, and is not subsumed by a clearer
existing test. Otherwise strengthen, replace, consolidate, or omit.

### Existing behavior change

Update tests that express the old contract. Do not preserve obsolete behavior with
new negative assertions or leave contradictory historical tests behind.

### Refactor or unfamiliar legacy code

Prefer existing observable-contract tests. Add narrowly scoped characterization
tests only where current behavior must be understood or held stable during a risky
change. Treat captured behavior as evidence of what exists, not proof of what is
correct; remove or rewrite temporary protection once the intended contract is
clear.

### Security, authorization, data, and compatibility boundaries

Test both permitted and forbidden outcomes when absence or rejection is itself the
contract. Give these high-impact boundaries stronger and sometimes deliberately
redundant protection when failures would be difficult to detect or recover from.

## Choose a faithful boundary

Choose the closest stable contract with the lowest **total** cost across fidelity,
diagnostic clarity, runtime, setup, flakiness, and maintenance. The smallest unit is
not automatically the best surface.

- Prefer real in-process collaborators when they are fast and deterministic.
- Use fakes or stubs at slow, remote, nondeterministic, or destructive boundaries.
- Verify mock interactions only when the interaction itself is the contract, such
  as committing a transaction, emitting an audit event, or suppressing a forbidden
  side effect.
- Keep a broader integration or end-to-end test only when it proves wiring or user
  behavior that lower-level tests cannot establish.

Derive expected results independently of the implementation. Do not add production
hooks solely to make tests convenient.

## Compose the risk model

- Partition behavior by meaningful equivalence classes instead of collecting one
  example per review round.
- Use table-driven tests for the same rule across representative cases.
- Use property-based tests when an invariant spans a large input space and the
  generators can model that space honestly.
- Test orthogonal dimensions separately, then keep the smallest useful wiring test;
  avoid their full Cartesian product unless interactions are themselves risky.
- Let one strong test replace several weaker near-duplicates.
- Use mutation testing selectively on important or changing code to audit whether
  tests detect plausible faults; do not make repository-wide mutation scores a
  ritual.

Read [testing-philosophy.md](references/testing-philosophy.md) when choosing among
competing test boundaries, doubles, characterization, property-based testing,
mutation testing, or TDD.

## Keep ordinary copy out of the test contract

Do not add or revise automated tests solely because ordinary UI, prompt, error,
empty-state, heading, help, or explanatory copy was added, changed, or removed.
Test the state, permission, action, navigation, or business outcome behind the copy.
Prefer stable semantic queries and outcomes over exact strings or snapshots that
must be updated whenever wording is polished.

Assert wording only when the wording itself is an intentional contract, such as
legal or regulatory text, localization behavior, a protocol token, or explicitly
versioned public output. Test only the contractual portion, not surrounding prose.

## Reject low-signal tests

Usually do not add tests for:

- private methods, internal call order, source layout, symbol names, or harmless
  refactoring structure;
- mock calls that merely restate the implementation;
- coverage targets without a named risk;
- trivial accessors, generated code, framework behavior, or type-system guarantees;
- broad regression cases already covered by a stronger rule or invariant;
- `not.toHave...` assertions that only memorialize removed implementation.

An absence assertion is valuable when absence is observable and contractually
important: a secret must not leak, an unauthorized action must not occur, or a
forbidden protocol field must not be emitted.

## Review and finish

Before completion, review the suite as a whole rather than only the newest tests:

1. Confirm each changed test adds distinct confidence or justified independent
   protection, and survives harmless refactoring.
2. Where practical, confirm high-value tests fail for the actual defect or a
   meaningful mutation. Do not require mutation evidence from every test.
3. Confirm review-driven changes remain coherent. Consolidate tests that protect the
   same failure mode at the same boundary; preserve distinct risks and justified
   independent evidence for high-impact failures.
4. Evaluate setup, runtime, flakiness, and change amplification as maintenance costs.
5. Run the relevant test levels and distinguish unit evidence from integration or
   production evidence.

Report tests added, strengthened, merged, replaced, deleted, and intentionally not
added. State the confidence each decision buys and any residual risk left to other
verification.
