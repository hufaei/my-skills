# Review and evaluation

Use this reference for a reported failure, a substantive prompt review, or a
comparison of changed behavior. Read the complete applicable sections. Select the
checks that could change the decision; this is not a checklist to run in full.

## Contents

- [Diagnose at the current stage](#diagnose-at-the-current-stage)
- [Turn a concern into a discriminating check](#turn-a-concern-into-a-discriminating-check)
- [Return a useful review](#return-a-useful-review)
- [Compare a baseline and candidate](#compare-a-baseline-and-candidate)
- [Select cases by the change at risk](#select-cases-by-the-change-at-risk)
- [Stop and report evidence honestly](#stop-and-report-evidence-honestly)

## Diagnose at the current stage

For a clear new task, establish its intended result and draft it. Do not require
a failure sample, transcript, or baseline that does not exist.

For an existing prompt, begin with the user's goal or symptom and inspect the
smallest relevant record: affected instruction, actual input, observed output,
and tool or runtime evidence where available. These are diagnostic inputs, not
mandatory fields to demand from the user. If evidence is missing, distinguish
what the text proves from what would need a run or runtime inspection.

| Stage | Useful intervention | Avoid |
| --- | --- | --- |
| Starting | Identify the outcome, decisive constraints, and source or interface facts that must be established. | A generic architecture inventory for a clear small task. |
| Stuck | Locate the failing transition in actual attempts and results; propose a check that separates the remaining causes. | Repeating exhausted attempts or replacing diagnosis with another broad plan. |
| Reviewing a result | Compare the result with the requested contract and examine what existing checks did not exercise. | Treating an unrelated passing check as resolution of a known mismatch. |
| Choosing candidates | Use a constraint or observation that distinguishes the candidates already under consideration. | Inventing a more elaborate interpretation without evidence or repeating a preference as proof. |

Revisit earlier advice against evidence obtained since it was given. Withdraw a
recommendation when a result defeats its premise. A reviewer statement is advice,
not a source of truth merely because it appears earlier in the transcript.

Locate the cause before choosing the change:

| Possible cause | Evidence to inspect | Likely intervention |
| --- | --- | --- |
| Prompt | Conflicting defaults, vague actor or scope, misplaced exception, output ambiguity. | Clarify the affected instruction or decision branch. |
| Input | Missing source, stale facts, irrelevant context, truncation, or a lost user correction. | Repair selection, freshness, or input delivery. |
| Tool | Wrong schema, wrong source, absent credentials, misunderstood effect, or uninspected result. | Correct the capability contract or call handling. |
| Runtime or surface | Wrong priority, unloaded module, state loss, unsupported rendering, inaccessible artifact, or invisible final message. | Repair assembly, state, or delivery. |

Causes may combine. If the prompt already states the intended rule but that rule
was not loaded, adding stronger wording is not the primary fix. If evidence
cannot distinguish instruction interpretation from missing context, report that
uncertainty and propose the smallest separating check. A valid diagnosis may
recommend no prompt edit.

For a tool, memory, source, state, or delivery defect, read the complete applicable
contract in [prompt architecture](prompt-architecture.md) before recommending it.
For disputed wording or exemplar transfer, read the relevant complete section of
[prompt language and examples](prompt-language-and-examples.md).

## Turn a concern into a discriminating check

Ground each material concern in a concrete situation:

1. Identify the relevant input or event and its source.
2. State the expected observable behavior from the user requirement, accepted
   contract, or source-faithful invariant.
3. Record the actual behavior or, for a textual review, the competing readings
   enabled by the instruction.
4. Name the check or minimal change that would separate the causes.

Use these relationships in analysis; do not force a form into the user's answer.

For example: the user asks only for review, the prompt tells the agent to
“inspect and fix,” and the trace shows a file write. Expected behavior is findings
without mutation. The instruction and trace support a scope defect. Narrowing
the review branch is a focused candidate; adding a general “be careful” rule is not.

A different case: the prompt already requires citing the supplied policy, but
the assembled request omitted that policy. Expected behavior depends on receiving
the source. Inspecting the assembly can establish an input defect; rewriting
the citation instruction cannot restore an absent document.

Preserve the distinction between a known defect, a plausible failure path, and
an unsupported preference. A source-based expected result must be independent of
the candidate's wording; do not invent an oracle that repeats its assumptions.
Evaluate visible decisions, calls, effects, outputs, and state transitions rather
than exact phrasing or private chain-of-thought.

## Return a useful review

A review-only request returns findings and recommendations. Do not silently
replace the prompt, write files, or implement runtime changes. A small suggested
phrase can illustrate a recommendation when useful; label it as a suggestion.

Lead with the most consequential supported issue. For each material finding,
give the affected passage or artifact, the input or event that exposes it, the
expected behavior, the consequence, and a focused recommendation. Cite an actual
location or trace when available. Keep severity proportional to the failure and
say whether the issue blocks the requested outcome.

Separate observed failures from risks inferred from the text. State material
evidence gaps without presenting them as defects. If no issue is found, say so
within the inspected scope and name any important untested requirement. Do not
add speculative defensive work merely to populate a review.

For expression-only edits, check actor, trigger, scope, obligation strength,
schema, exception, and observable result. A mandatory consultation changed to
optional self-review is behavioral redesign; a similar sentence count does not
make it a faithful wording edit.

## Compare a baseline and candidate

When an existing prompt and a runnable target are available, retain the baseline.
Use the same relevant input, model/runtime settings, tool schemas, context, and
output criteria for both. Record differences that prevent a controlled comparison.
Do not attribute a runtime fix, newly supplied evidence, or model change to prose.

Choose a small set of cases tied to the actual concern. Include the affected
failure or branch, and an ordinary case whose behavior should remain valid.
Establish the expected result before judging either output. When model variability
could change the decision, use enough repeated observations to distinguish a
pattern from an isolated result; do not impose a universal trial count.

For each case, compare:

- whether each version made the intended observable decision;
- whether the candidate resolved the targeted issue;
- whether it changed an invariant or introduced a relevant regression.

For a new prompt, evaluate against its contract; do not fabricate a baseline.
When execution is unavailable or outside scope, provide a textual assessment or
proposed cases and label them as unrun. A review can identify an ambiguous branch
without proving how often a model will take it.

No custom evaluator, grader service, telemetry pipeline, or automated harness is
required for ordinary work. Use existing relevant evaluation machinery when the
task calls for it. Avoid regex or snapshot tests of ordinary wording; exact tests
belong to actual machine-readable schemas and protocols.

## Select cases by the change at risk

Use the smallest subset that could reveal a consequential mistake:

| Change or concern | Discriminating cases and observable result |
| --- | --- |
| Narrow wording or format edit | Normal input plus the affected exception; preserve obligation, fields, and output boundary. |
| Clarification default | Complete input, an inferable omission, and a gap that changes correctness; proceed or ask at the intended boundary. |
| Source or context routing | Supplied material versus outside facts, or relevant versus stale context; use the source that owns the claim. |
| Exemplar adaptation | A normal path and an exception from the source; preserve intended mechanisms without importing its environment or incidental examples. |
| Review versus implementation | A review-only request and an authorized change request; report or mutate according to scope. |
| Capability or action contract | Valid call plus the actual missing-schema, permission, or uncertain-effect condition at risk; discover, stop, or retry correctly. |
| State or delivery contract | The relevant correction, status, resume, or remote artifact case; preserve provenance and complete the real handoff. |

A short text prompt does not need authorization or recovery cases. A change to
retry behavior does not need every presentation case. Broaden coverage when the
change affects shared decisions, external effects, or failures that current cases
cannot discriminate.

## Stop and report evidence honestly

Stop when the requested artifact or review is complete, relevant checks meet the
contract, and no unresolved material finding justifies more work. New failures,
changed instructions, or an unexplained mismatch may require another iteration.
A stylistic preference or a long unused checklist does not.

Report the kind and limits of evidence: textual inspection, contract check,
proposed case, observed run, or baseline/candidate comparison. A passing YAML or
link check establishes file integrity; it does not establish model behavior.
A designed test is not an executed test. One observed success does not establish
general improvement.

If a known defect remains, name it and whether it blocks use. If an unavailable
runtime prevents execution, deliver the useful requested work with that limit
visible; do not claim verified deployment or improved behavior. Respect the user's
requested format, including a request for just the prompt.
