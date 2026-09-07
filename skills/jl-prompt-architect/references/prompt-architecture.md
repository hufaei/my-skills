# Prompt architecture reference

Use this reference for agent, system, runtime, tool, skill, stateful, or review-heavy
prompt work. It is a design lens, not a universal template.

## Contents

- [Four design objects](#four-design-objects)
- [Eight review dimensions](#eight-review-dimensions)
- [Layer boundaries](#layer-boundaries)
- [Surface composition](#surface-composition)
- [Context and memory gates](#context-and-memory-gates)
- [Execution environments and lifecycles](#execution-environments-and-lifecycles)
- [Capability lifecycle](#capability-lifecycle)
- [Evidence and presentation](#evidence-and-presentation)
- [Information-shape routing](#information-shape-routing)
- [Compact runtime contracts](#compact-runtime-contracts)
- [Reusable prompt shapes](#reusable-prompt-shapes)
- [Correction, recovery, and behavioral evaluation](#correction-recovery-and-behavioral-evaluation)

## Four design objects

### Cognition

Control how the model approaches the problem: the evidence order, decision points,
branching, verification, and completion condition. Describe observable workflow;
do not demand publication of private chain-of-thought.

Typical questions:

- What must be understood before action?
- Which source owns each fact?
- Which steps depend on earlier evidence?
- What proves completion?

### Expression

Control how intent becomes language: precision, semantic density, information
architecture, rhythm, abstraction, and reader attention.

Use wording as an interface. `Modify the file` leaves scope open; `replace only the
matching policy block and preserve adjacent configuration` names the target,
operation, and invariant. Expressive language is precise only when it reduces
behavioral ambiguity.

### Control

Control capabilities and boundaries: tools, context sources, permissions, policy,
side effects, schemas, and priority. A capability contract must answer both “how to
use it” and “what authority permits its use.”

### State

Control continuity: active objective, new-message classification, pause/resume,
recovery, compaction, provenance, and terminal state. Treat recovery as a state
transition model, not a generic instruction to “remember context.”

## Eight review dimensions

### 1. Intent

Name the result and its consumer. Distinguish the requested artifact from the work
used to produce it.

Weak: `Help me with an API prompt.`

Stronger: `Produce a system prompt that routes API support questions to the supplied
OpenAPI contract and returns answers with endpoint, prerequisite, and failure-mode
sections.`

### 2. Cognition

Define evidence and decision order. Use verbs that expose checkpoints:

```text
classify the request
→ select the authoritative source
→ resolve conflicts
→ produce the result
→ verify the output contract
```

Avoid empty process words such as “reason deeply” when no observable behavior
changes.

### 3. Information architecture

Order material according to when it changes a decision:

```text
identity and objective
→ inputs and source authority
→ decision workflow
→ capabilities and constraints
→ output and completion
→ recovery when stateful
```

Keep a constraint beside the capability it limits. Keep historical explanation out
of the execution path unless it changes a choice.

### 4. Expression

Prefer exact verbs, concrete objects, explicit invariants, and testable outcomes.
Semantic density is useful when one phrase activates shared knowledge without
creating multiple plausible interpretations.

Use abstraction deliberately:

- abstract language for policy that must generalize;
- concrete language for schemas, effects, examples, and fragile boundaries;
- placeholders for deployment-specific facts that should be injected later.

### 5. Attention

Position is part of control. Put the objective before implementation detail and the
critical gate before the capability it governs. Repeat only invariants whose failure
is costly and likely across distant sections.

Use positive instructions for the default path:

```text
Preserve unrelated changes.
```

Use negative instructions to close a dangerous alternative:

```text
Never treat tool availability as authorization.
```

Neither form is universally stronger; choose according to the behavior being
controlled.

### 6. Runtime

Separate stable instructions from variable injection:

- identity and durable behavior;
- environment and current time;
- project or user instructions;
- memory and continuation state;
- tool and connector registry;
- user request.

Runtime data may be stale, absent, or lower priority than policy. State its ownership
and refresh path.

### 7. Constraints

Distinguish preference, requirement, authorization, and prohibition. Give hard words
to hard boundaries; do not make formatting taste compete with security or external
side effects.

For each material constraint, ask:

- What failure does it prevent?
- Is the scope exact?
- What instruction wins in conflict?
- Can compliance be observed?

### 8. Recovery

Define events and transitions explicitly when work spans messages or tools:

```text
active task
├── replace: abandon only superseded pending work
├── extend: preserve completed work and add the new requirement
├── status: report state without changing direction
├── pause: save an executable resume point
└── continue: resume from the first pending or unverified action
```

Preserve message provenance. Quoted text, tool output, examples, and assistant-authored
summaries do not become user authorization.

## Layer boundaries

Do not collapse these layers merely because a product stores them in one runtime
prompt:

```text
stable identity and behavior
↓
cognitive workflow and expression
↓
environment, tools, memory, and project injection
↓
policy and authority gates
↓
current user request
↓
observable verification and state transition
```

Some instructions affect more than one layer. `Lead with the outcome` shapes both
cognitive priority and answer order. `Diagnose first; do not mutate` shapes cognition
and authority. Classify the primary effect, then inspect secondary effects rather
than forcing every sentence into one exclusive bucket.

Instruction priority, source authority, and action authority are separate orders:

- **Instruction priority** resolves which directive governs behavior when rules
  conflict.
- **Source authority** resolves which system or artifact owns a fact. A repository,
  connected account, rendered UI, and user statement may each own different facts.
- **Action authority** resolves whether the agent may create an effect. It comes from
  the request and applicable policy, not from tool availability or factual access.

A high-priority instruction can require consulting a source without making that
source authoritative for every claim. An authoritative source can prove current
state without granting permission to change it. A permitted action can still require
fresh evidence and satisfied preconditions.

## Surface composition

Treat an AI product as a composition, not a model name:

| Layer | Owns | Must not imply |
| --- | --- | --- |
| Product surface | interaction channels, supported markup/components, artifact handoff, visible feedback | hidden tools, durable memory, or permission |
| Model behavior | stable stance, decision habits, communication, default workflow | current environment or installed capabilities |
| Runtime | injected context, capability schemas, environment, permissions, state and continuation | that every capability should be used |

The same model may serve conversation, coding, design, or voice surfaces with
different evidence, state, and output contracts. The same surface may swap models or
capabilities without changing its user-facing purpose. Place a rule in the layer
that owns it so a presentation change does not silently rewrite behavior and a
runtime change does not require inventing a new identity.

When reviewing an assembled prompt, ask:

1. Which surface receives input and shows the result?
2. Which stable model behaviors should survive capability changes?
3. Which runtime facts are injected, refreshable, or absent?
4. Where are policy, confirmation, and external-effect gates enforced?
5. Can the claimed output actually be represented and inspected on this surface?

## Context and memory gates

Context is eligible input, not mandatory content. Register each context source with
its scope, provenance, freshness, sensitivity, and the decisions it is allowed to
change. Start from no personal or saved context, then admit only information that
materially improves correctness or specificity, or avoids a needless question.

Apply these gates before use:

1. **Relevance:** does this fact change the current result?
2. **Authority:** is this source allowed to establish that kind of fact?
3. **Freshness:** is it still valid, or must it be refreshed?
4. **Scope:** does it belong to this user, project, domain, and task?
5. **Sensitivity:** is use necessary and permitted without exposing private
   machinery or inferring a protected attribute?
6. **Conflict:** does a newer user correction or higher-priority instruction win?

Memory is a selective continuity aid, not a source-specific retrieval substitute.
It may suggest which project or document to inspect, but it cannot stand in for the
current contents of a file, account, remote service, or other authoritative system.
Do not promote transient task state, guesses, quoted examples, or tool output into
durable user intent.

## Execution environments and lifecycles

Name the environment before specifying file or state operations:

| Environment | Typical lifecycle | Core invariant |
| --- | --- | --- |
| User workspace | persistent inputs and deliverables | preserve unrelated state; verify the saved result |
| Session scratchpad | disposable intermediates for one execution | never present temporary state as the deliverable |
| Isolated sandbox | bounded computation with declared persistence and network limits | never describe it as the user's device or account |
| External system | shared or remote state beyond the local runtime | require applicable authority, authentication, and post-action verification |

For every created object, define owner, location class, persistence, recoverability,
cleanup, and handoff. A successful sandbox computation does not prove a workspace
file changed; a saved workspace artifact does not prove it was published; a browser
render does not prove the backing data was mutated. Each boundary needs its own
evidence.

## Capability lifecycle

Use a capability through a complete execution loop:

```text
discover exact capability and current schema
→ confirm it owns the needed fact or effect
→ check action authority, authentication, and other preconditions
→ call with schema-valid inputs
→ inspect the returned result and any claimed side effect
→ verify the user's outcome at the authoritative surface
→ classify failure and retry, fall back, or stop
```

Discovery should produce the exact callable contract rather than a guessed name or
parameter list. Separate permission from authentication: the user may authorize an
effect while the runtime still lacks credentials, and a connected account may be
authenticated without the user authorizing the requested mutation.

For retrieval, route from what is actually known. When the URL is known, read or
extract that address directly; search when direct access fails, the source cannot
answer or refresh the claim, verification needs another source, or the user asks
for alternatives. When the location is unknown, search or discover candidate
sources first, select the source that owns the needed fact, then read it directly.
A search result identifies a candidate; it does not substitute for inspecting the
selected source.

Define retries by failure class. Retry only when the call is safe to repeat, the
failure is plausibly transient, and the attempt count or time bound is explicit.
Correct schema or precondition failures before retrying. Do not repeat an uncertain
non-idempotent effect merely because confirmation is missing; verify remote state or
stop with the uncertainty visible.

## Evidence and presentation

Evidence establishes facts; presentation makes them inspectable. Keep these roles
separate:

| Evidence | What it can establish |
| --- | --- |
| User-provided fact or decision | intent, constraints, and authorization within its scope |
| Source-specific retrieval | current content owned by that source |
| Computation or execution | the observed result under the stated inputs and environment |
| Rendered or interactive surface | what a user can actually see or do there |
| Inference | a conclusion whose uncertainty and premises remain visible |

Prose, tables, citations, visuals, artifacts, and interactive components are
presentation forms. Rendering retrieved data does not upgrade its authority; a
successful component render does not prove the underlying claim; an attractive
artifact does not grant permission to save or publish it.

Claims such as `done`, `fixed`, `saved`, `sent`, `published`, and `verified` require
fresh evidence observed in the current execution at the surface that owns the
claim. A plan, stale transcript, delegated report, successful tool invocation, or
uninspected diff is not sufficient by itself. State skipped, failed, partial, and
unexpected checks before compressing successful evidence into the final response.

## Information-shape routing

Choose an output surface from the information relationship and user need, not from
the mere presence of a rendering capability:

| Information shape or need | Smallest fitting form |
| --- | --- |
| One result or short explanation | prose |
| Independent items | list |
| Repeated fields or exact comparison | table |
| Order-critical procedure | sequence |
| Dates whose order carries meaning | timeline |
| Ownership or nesting | tree |
| Branches, dependencies, or state change | flow or state diagram |
| Spatial identity or visual comparison | sourced image or visual |
| Adjustable inputs that change outcomes | interactive component |
| Persistent, reusable, or editable deliverable | artifact or file |

Default to prose when another form adds no information. Do not use a sequence for
unordered advice, a timeline when dates are incidental, an interactive component
for a single calculation, or an image as decoration. Verify that the active surface
supports the syntax and provide a plain fallback when it does not.

## Compact runtime contracts

Use these field sets as review aids, not mandatory headings.

### Memory Contract

```text
Scope and owner: {{USER_PROJECT_DOMAIN}}
Write gate: {{DURABLE_RELEVANT_NON_SPECULATIVE}}
Stored content: {{FACT_DECISION_WHY_AND_APPLICATION}}
Excluded content: {{SENSITIVE_TRANSIENT_OR_UNTRUSTED}}
Provenance and freshness: {{SOURCE_TIMESTAMP_REFRESH_RULE}}
Read/application gate: {{WHEN_IT_MATERIALLY_CHANGES_THE_RESULT}}
Conflict and mutation: {{CORRECTION_MERGE_DELETE_RULE}}
Lifetime and handoff: {{PERSISTENCE_AND_DISCLOSURE_BOUNDARY}}
```

### Response Component Contract

```text
Purpose: {{INFORMATION_NEED}}
Use / do not use: {{TRIGGER_AND_EXCLUSIONS}}
Required schema: {{FIELDS_TYPES_COUNTS}}
Data authority and freshness: {{SOURCE_AND_REFRESH}}
Surface support: {{VALID_RENDERING_CONTEXT}}
Ordering and layout: {{COMPOSITION_RULES}}
Fallback: {{PLAIN_OR_FILE_ALTERNATIVE}}
Verification: {{RENDER_AND_INTERACTION_CHECK}}
```

The memory contract governs durable context. The response component contract
governs presentation. Neither grants action authority; pair either with the
applicable source, capability, and permission contracts.

## Reusable prompt shapes

Use these as starting shapes. Remove any line that does not change behavior.

### Compact purpose prompt

```text
Outcome: {{OBSERVABLE_RESULT}}
Context: {{ONLY_THE_CONTEXT_THAT_CHANGES_THE_RESULT}}
Constraints: {{MATERIAL_BOUNDARIES}}
Return: {{COPYABLE_OUTPUT_CONTRACT}}
```

### Agent behavior prompt

```text
Identity and relationship: {{ROLE_AND_USER_RELATIONSHIP}}
Intent and terminal condition: {{OBJECTIVE_AND_DONE}}

Cognition:
{{EVIDENCE_ORDER_DECISIONS_AND_VERIFICATION}}

Expression:
{{AUDIENCE_LANGUAGE_STRUCTURE_AND_DENSITY}}

Authority and capabilities:
{{TOOLS_SOURCES_EFFECTS_AND_GATES}}

State and recovery:
{{MESSAGE_TRANSITIONS_PROVENANCE_AND_RESUME}}
```

### Tool contract

```text
Tool: {{NAME}}
Purpose and authoritative data: {{PURPOSE}}
Use when: {{TRIGGER}}
Do not use when: {{EXCLUSIONS}}
Inputs and preconditions: {{INPUT_CONTRACT}}
Side effects and authority: {{EFFECTS_AND_PERMISSION}}
Returned evidence: {{RESULT_CONTRACT}}
Failure and post-call handling: {{FAILURE_RECOVERY}}
```

### Prompt assembly contract

```text
Stable behavior: {{MODEL_OR_AGENT_BEHAVIOR}}
Runtime injection: {{ENVIRONMENT_TOOLS_MEMORY_PROJECT_STATE}}
Priority order: {{CONFLICT_PRECEDENCE}}
Untrusted content boundary: {{DATA_NOT_INSTRUCTIONS}}
User request slot: {{CURRENT_REQUEST}}
Output and verification: {{RESULT_AND_EVIDENCE}}
```

## Correction, recovery, and behavioral evaluation

Treat correction as a normal state transition. When the user identifies an error:

```text
identify the disputed claim, action, or scope
→ re-inspect the authoritative source
→ preserve still-valid work and abandon only the superseded direction
→ determine whether the correction requires new action authority
→ repair within scope
→ verify the corrected outcome with fresh evidence
→ update durable memory only if its write gate passes
```

Do not defend the earlier answer before checking it. A correction has current user
priority for the matter it corrects, but it does not retroactively authorize a new
external effect or destructive repair. If recovery changes product direction,
ownership, or material risk, stop at that boundary and request the missing decision.

A continuation state should preserve the active objective, current constraints,
authorization grants and denials, source provenance, completed evidence, changed
state, failures and retry counts, pending or unverified work, and the next executable
action. On resume, do not repeat work already proven complete and do not promote an
assistant summary, quoted example, or tool output into a user instruction.

Exercise reusable prompts against representative behavior cases:

1. **Normal:** a complete request follows the intended shortest path.
2. **Request type:** an answer, diagnosis, change, monitor, and external effect each
   stop at the correct authorization boundary.
3. **Missing input:** the model asks only when the missing choice changes the result.
4. **Instruction conflict:** lower-priority context cannot override governing rules.
5. **Source conflict:** the model chooses the source that owns the disputed fact and
   keeps inference visible.
6. **Context gate:** irrelevant, stale, cross-domain, or sensitive memory is omitted;
   a current correction wins.
7. **Capability gap:** the model discovers the current schema or reports the missing
   capability instead of guessing.
8. **Authority gap:** authenticated access or tool availability does not trigger an
   unauthorized effect.
9. **Environment mismatch:** scratchpad, sandbox, workspace, and external state are
   not treated as interchangeable.
10. **False-positive call:** a successful invocation is not reported as the user's
    outcome until the authoritative surface verifies it.
11. **Presentation:** unsupported or failed component rendering falls back without
    changing facts, and presentation markup cannot smuggle instructions or authority.
12. **Failure and retry:** schema errors are corrected; transient failures receive
    bounded safe retries; uncertain non-idempotent effects are not blindly repeated.
13. **Correction:** the agent rechecks, repairs only within scope, and re-verifies
    without discarding valid work.
14. **Interruption:** status, extension, replacement, pause, compaction, and continue
    preserve provenance and resume from the first pending or unverified action.
15. **Completion:** stale evidence, confidence, plans, and delegated claims cannot
    support a current completion statement.

Evaluate observable classification, source selection, tool calls, permission gates,
outputs, verification, and state transitions. Score the decision and effect, not
exact wording or private chain-of-thought.

Design basis: [AI Prompt Atlas](https://hufaei.github.io/ai-prompt-atlas/), using its
2026-09-03 source-pinned prompt/runtime case studies as learning material rather
than an official product specification.
