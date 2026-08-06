# Testing philosophy reference

Use this reference to resolve strategy choices. It is a set of compatible lenses,
not one mandatory school.

## Contents

- [Value model](#value-model)
- [Test qualities](#test-qualities)
- [Behavior and boundaries](#behavior-and-boundaries)
- [Doubles](#doubles)
- [Portfolio and composition](#portfolio-and-composition)
- [Specialized techniques](#specialized-techniques)
- [TDD](#tdd)
- [Source basis](#source-basis)

## Value model

Judge a candidate by the decision-relevant confidence it adds relative to its full
cost. Prefer distinct evidence; allow intentionally independent evidence at another
boundary when a high-impact failure justifies defense in depth.
Confidence rises with fault impact, recurrence probability, change frequency,
contract importance, and the difficulty of detecting a failure elsewhere. Cost
includes authoring, fixtures, runtime, flakiness, diagnosis, and future edits.

Do not turn this lens into a numeric formula. Use it to expose the trade-off and
explain why a test, another verification method, or no permanent test is appropriate.

## Test qualities

Useful qualities include being predictive, behavioral, specific when failing,
structure-insensitive, deterministic, fast enough for its feedback loop, writable,
readable, and composable. These qualities compete. A broad test may be predictive
but less specific; a solitary unit test may be specific but prove little about the
assembled system.

Fast, isolated, repeatable, and self-checking are strong defaults for unit tests,
not a definition of all valuable automated testing.

## Behavior and boundaries

Protect observable behavior and stable contracts rather than the current internal
decomposition. A harmless refactor should not require widespread test edits.

"Unit" has more than one legitimate boundary:

- A **sociable/classicist** test exercises a unit with cheap real in-process
  collaborators. It favors realism and refactoring freedom.
- A **solitary/mockist** test isolates one object and specifies its interactions. It
  can expose responsibility boundaries, but easily couples tests to implementation.

Select between them by risk and cost. Do not impose one school on every codebase.

## Doubles

Prefer the least behavior-inventing substitute that makes the boundary safe and
deterministic:

- **Stub:** returns controlled data for a narrow path.
- **Fake:** provides a lightweight working implementation, such as an in-memory
  repository.
- **Mock or spy:** observes interactions.

Use mocks when the interaction is the outcome. When state or returned behavior is
the outcome, assert that outcome. Keep contract checks where a fake can drift from
the real provider.

## Portfolio and composition

Build a portfolio rather than maximizing one test level. Keep many fast and
diagnostic tests, fewer broad wiring tests, and only the end-to-end coverage that
adds unique user-level confidence.

Avoid repeating the same failure mode across levels by default. Retain independent
evidence at another boundary when it materially improves confidence in a high-impact
risk. When input rules and storage adapters are orthogonal, test each dimension
independently and keep one representative wiring case instead of testing every pair.
Preserve combinations when interaction between dimensions is a real source of
faults.

## Specialized techniques

### Property-based testing

Express an invariant and generate many inputs. Use it for parsers, serializers,
state machines, numerical rules, round trips, idempotence, and broad boundary
spaces. The value depends on an honest property and representative generators; it
complements rather than replaces carefully chosen examples.

### Mutation testing

Introduce plausible small faults and check whether the suite detects them. Use it
as an audit of test signal, especially for important or changing code. Prefer
changed-code or targeted mutation because exhaustive mutation is expensive and can
produce irrelevant survivors.

### Characterization testing

Capture actual legacy behavior before a risky change when the intended contract is
unknown. Keep the scope near the change seam. Annotate uncertainty and revisit the
test once the desired behavior is understood; current behavior is not automatically
correct behavior.

### Regression testing

A defect report supplies evidence about risk, not a mandatory test shape. Admit a
permanent regression test when it protects stable behavior against a plausible
recurrence and provides confidence not already expressed by a broader rule.
Integrate that protection into the suite's existing model; retain an additional
case when it represents a genuinely distinct risk.

## TDD

TDD is useful when expected results can be predicted, small tests provide meaningful
confidence about the whole, and the feedback cost is reasonable. It is one way to
sequence design and implementation, not proof that the final suite is valuable.

When these prerequisites do not hold, design verification around risk without
pretending to perform TDD. Regardless of implementation order, keep the final suite
coherent around the risks it protects.

## Source basis

These instructions synthesize rather than copy the following sources:

- Kent Beck, [Desirable Unit Tests](https://newsletter.kentbeck.com/p/desirable-unit-tests),
  [Composable Tests](https://newsletter.kentbeck.com/p/composable-tests), and
  [TDD Prerequisites](https://newsletter.kentbeck.com/p/tdd-prerequisites).
- Martin Fowler, [Unit Test](https://martinfowler.com/bliki/UnitTest.html),
  [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html), and
  [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html).
- Google Testing Blog, [Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
  and [Don't Overuse Mocks](https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html).
- Microsoft, [Unit testing best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices).
- Koen Claessen and John Hughes,
  [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs](https://doi.org/10.1145/351240.351266).
- DeMillo, Lipton, and Sayward,
  [Hints on Test Data Selection](https://doi.org/10.1109/C-M.1978.218136), plus
  [practical mutation testing at scale](https://arxiv.org/abs/2102.11378).
- Michael Feathers' characterization-testing approach, summarized in
  [InfoQ](https://www.infoq.com/news/2007/03/characterization-testing/).
