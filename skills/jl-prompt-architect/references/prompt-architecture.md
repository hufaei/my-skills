# Prompt architecture reference

Use this reference for agent, system, runtime, tool, skill, stateful, or review-heavy
prompt work. It is a design lens, not a universal template.

## Contents

- [Four design objects](#four-design-objects)
- [Eight review dimensions](#eight-review-dimensions)
- [Layer boundaries](#layer-boundaries)
- [Reusable prompt shapes](#reusable-prompt-shapes)
- [Conflict and recovery checks](#conflict-and-recovery-checks)

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

## Conflict and recovery checks

Exercise a reusable prompt against a small case set:

1. **Normal:** a complete request follows the intended shortest path.
2. **Missing input:** the model asks only when the missing choice changes the result.
3. **Conflict:** lower-priority context cannot override policy or authority.
4. **Capability gap:** the model reports the missing capability instead of pretending.
5. **Side effect:** execution waits at the correct authorization gate.
6. **Interruption:** status, extension, replacement, pause, and continuation preserve
   the right state.
7. **Completion:** the model relies on fresh observable evidence, not confidence or a
   delegated claim.

Evaluate decisions, tool calls, outputs, and state transitions. Do not require or
score private chain-of-thought.

Design basis: [AI Prompt Atlas](https://hufaei.github.io/ai-prompt-atlas/), used as
a source-pinned collection of prompt/runtime case studies rather than an official
product specification.
