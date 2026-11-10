---
name: jl-prompt-architect
description: Use when the user is explicitly designing, writing, revising, debugging, or reviewing prompts intended for an AI model, agent, runtime, tool, skill, or AI-powered product. Also use when an agent project explicitly involves prompt hierarchy, assembly, context injection, tool contracts, instruction priority, state recovery, or prompt evaluation. A short instruction intended for reuse in another AI system counts. Do not trigger for ordinary prose, documentation, UI copy, general coding, casual requests addressed to Codex, or brainstorming unless the deliverable is itself a prompt.
---

# JL Prompt Architect

## Contract

Make prompts usable for their actual task and execution surface. Language directs
attention, establishes the reader relationship, and shapes decisions; it is part
of the interface. Spend structure where behavior can diverge. A clear short task
can be complete without an agent identity, tools, memory, or recovery protocol.

Follow the user's requested operation and delivery format. A review produces
findings and recommendations; it does not authorize rewriting the prompt.

## Establish the task and locate the problem

Start from the desired result or reported failure. Use the request and supplied
artifacts to establish the consumer, necessary inputs, constraints, and output.
For an existing prompt, inspect the affected passage and, when available, the
actual assembled input and observed output. For a clear new task, draft directly;
a failure sample is not a prerequisite.

When debugging, distinguish these possible causes before choosing a rewrite:

- **Prompt:** an ambiguous, missing, conflicting, or misplaced instruction.
- **Input:** missing, stale, irrelevant, or truncated material.
- **Tool:** a schema, source, authentication, effect, or result-handling mismatch.
- **Runtime or surface:** assembly priority, context delivery, state, or visibility.

One symptom may cross boundaries. Make the smallest check that separates plausible
causes. Diagnosis may conclude that the prompt should stay unchanged. Do not fix
a broken context pipeline by adding emphatic prose.

Infer ordinary defaults from context; omit details that do not affect the task.
Ask only when a real gap changes the goal, architecture, or correctness. Use input
slots for genuinely variable, reusable business content. Do not turn every unknown
into a placeholder or make an unnecessary questionnaire.

The target runtime may differ from this Codex session. Inspect its actual contracts
when available. A future interface may be designed as a proposed contract with
explicit implementation prerequisites; unavailable current tools do not prevent
that design. A tool name or slot alone cannot make a prompt deployable.

## Choose the operation

- **Review:** compare the prompt and available evidence with the intended behavior.
  Return supported findings, their consequences, and focused recommendations. Keep
  suggested edits separate; do not supply a replacement unless requested.
- **Draft:** write the smallest complete instruction for the stated task, reader,
  and surface. Add agent or runtime structure only where it changes behavior.
- **Adapt:** study a relevant source module in its original order. Choose faithful
  adaptation, behavioral redesign, or an independent source-inspired draft, and
  identify the mode accurately.
- **Revise:** separate an expression-only edit from an intended behavior change.
  For expression-only work, preserve actor, trigger, scope, obligation strength,
  schema, exception, and observable result, as well as deployment language and
  voice. For behavioral work, name the decision or effect being changed.

Review may support another operation without turning it into a full runtime audit.

## Do the minimum necessary work

For a one-shot prompt, express the outcome, needed context, material constraints,
and output. For a reusable task, add only the decision branches and input slots it
will actually use. For an agent, establish its relationship, evidence order,
authority, completion, and any continuity it needs.

Keep these distinctions even when they share one prompt file:

- **Product surface:** interaction, rendering, and delivery.
- **Stable model behavior:** decisions, stance, and expression.
- **Runtime:** injected environment, context, tools, permissions, and state.

Instruction priority determines what to obey; source authority determines what
establishes a fact; action authority determines which effects are permitted.
Evidence and tool availability do not create permission.

Write instructions in decision order. Put prerequisites before actions and
exceptions beside their rule. Use concrete nouns and active verbs; replace empty
qualities with observable criteria. Retain useful cadence, imagery, and role
framing when they steer attention. Establish the audience before tone: English and
a colleague voice are not universal defaults.

Use a positive normal path and reserve hard wording for hard boundaries. Compress
repeated meaning, not distinct decisions. Keep few, purposeful examples; their
incidental facts or style must not override explicit requirements. Specify
observable checks, not disclosure of private chain-of-thought. Give freedom to
harmless creative choices and precision to schemas, effects, and costly failures.

Read additional material only for a live decision:

- For source-template learning or adaptation, read the complete applicable
  sections on [source reading and adaptation modes](references/prompt-language-and-examples.md#read-the-original-as-an-executable-composition).
  For voice, density, or a worked short/agent/local edit, read the relevant
  complete example and its explanation in that reference.
- For tool, source, context, memory, state, or delivery contracts, read the
  complete applicable sections of [prompt architecture](references/prompt-architecture.md).
  A simple wording edit does not need this reference.
- For a failure investigation, substantive review, or behavioral comparison, read
  the complete applicable sections of [review and evaluation](references/review-and-evaluation.md).
  A clear short draft can be checked with the next section alone.

## Verify proportionately

Check the prompt against the user's goal and output contract. Look for a
contradictory rule, unsupported capability, missing decisive branch, or an example
that changes the meaning. For an expression-only revision, compare the invariants
above, including exceptions and schema.

Select a few cases that discriminate the behavior at risk. An ordinary case and
the affected exception may suffice for a narrow edit; a stateful external-effect
agent may need a failure or recovery case. Do not impose every runtime scenario,
build evaluation infrastructure, or add wording-match tests to ordinary prompt work.

When a baseline exists and execution is available, compare baseline and candidate
under the same relevant conditions. Distinguish a textual review, a designed test,
and an observed run. Without observed runs, do not claim improved model behavior.
Stop when the requested contract is met and the material concern is resolved;
recheck only when new evidence, changes, or failures justify it.

## Deliver what was requested

For drafting or revision, lead with the copyable prompt or requested file. Include
only deployment prerequisites, remaining dependencies, material behavioral changes,
or validation limits the user needs. Do not force architecture fields into the
answer. If the user asks for just the prompt, provide just that prompt; a design
with unmet deployment prerequisites must remain visibly labeled as such.

For review, lead with findings and evidence, or say that no issue was found within
the inspected scope. Separate an observed defect from a plausible risk. Name any
material unverified requirement. A diagnosis can recommend an input, tool, or
runtime fix while leaving the prompt intact.
