---
name: jl-prompt-architect
description: Use when the user is explicitly designing, writing, revising, debugging, or reviewing prompts intended for an AI model, agent, runtime, tool, skill, or AI-powered product. Also use when an agent project explicitly involves system/developer/user prompt hierarchy, prompt assembly, context injection, tool contracts, instruction priority, state recovery, or prompt evaluation. A short, purpose-built instruction that the user will copy into another AI system counts as prompt engineering. Do not trigger for ordinary prose, documentation, UI copy, general coding, casual requests addressed to Codex, or generic brainstorming unless the requested deliverable is itself a prompt.
---

# JL Prompt Architect

## Contract

Design prompts as executable interfaces. Language is part of the interface: it
directs attention, establishes a relationship, and changes how decisions unfold.
Make the intended outcome, decision path, evidence, authority, runtime, output,
and recovery behavior legible. Spend structure where behavior can diverge.

Return a prompt the user can actually place in its target layer. Do not mistake a
long prompt for a complete prompt or compressed jargon for precision.

## Choose the operation

- **Draft:** build for the actual task, reader, and execution surface. Use a small
  purpose prompt when it suffices; choose a complete agent template when the
  relationship, decisions, and tool workflow need to work together.
- **Adapt an exemplar:** choose a source by its work surface, stage, interaction
  pattern, and failure modes. A model name alone is not a selection criterion.
  Learn how the original wording and sequence produce behavior before adapting it.
- **Revise locally:** establish what must stay invariant, then change the smallest
  relevant passage. Preserve language, voice, obligation strength, exceptions,
  schemas, and authority unless the user requests a behavioral change. Distinguish
  expression-only changes from changes to observable decisions or effects.

Review can accompany any operation. Use the relevant lenses rather than treating
every review as a full runtime audit.

## Establish the boundary

Before drafting, determine what can be established from the request or supplied
artifacts:

1. **Consumer:** which model, agent, tool, or product surface will read it?
2. **Outcome:** what observable result should it produce or preserve?
3. **Inputs:** what context, variables, files, messages, or evidence can it receive?
4. **Authority:** may it only answer, or may it call tools, mutate state, publish, or
   affect users?
5. **Output:** what form, schema, destination, or completion evidence is required?
6. **Lifetime:** is this a one-shot instruction, a reusable template, or a stateful
   runtime contract?

Inspect relevant source code, prompt assembly, tool schemas, or runtime
documentation when available. Do not invent capabilities or instruction priority.
Ask one focused question at a time, and continue asking only while a missing
answer changes the architecture; otherwise use a conspicuous placeholder such as
`{{TARGET_MODEL}}`.

Keep three layers distinct: the **product surface** owns interaction and rendering,
the **model prompt** owns stable behavior, and the **runtime** owns injected context,
capabilities, permissions, and state. A shared model does not imply shared memory,
tools, or authority across surfaces.

Also keep three kinds of authority independent: instruction priority decides what
must be obeyed, source authority decides where facts come from, and action authority
decides which effects are permitted. Strong evidence does not grant permission, and
high-priority style instructions do not create facts.

## Choose the smallest fitting shape

| Prompt surface | Minimum useful structure |
| --- | --- |
| One-shot task | outcome → necessary context → constraints → output |
| Reusable template | inputs → decision procedure → quality bar → output → edge behavior |
| Agent behavior | identity → intent → cognition → expression → authority → completion |
| Runtime composition | stable behavior → environment → tools → policy → injected context → state |
| Tool or connector | purpose → use/do not use → inputs → effects → authority → result/failure |
| Skill or workflow | trigger → ordered procedure → resources → gates → verification → resume |
| Creative or media prompt | subject → composition → style → invariants → exclusions → delivery |

Do not inflate a clear one-shot prompt into an agent runtime. Do not compress a
stateful, tool-using agent into a role sentence plus a list of adjectives.

Read references according to the decision being made:

- For learning from source templates, choosing wording or voice, adapting a whole
  agent prompt, or a nuanced local revision, read the relevant sections of
  [prompt-language-and-examples.md](references/prompt-language-and-examples.md).
- For agent/runtime composition, tools, prompt hierarchy, state recovery, or a
  review of those contracts, read
  [prompt-architecture.md](references/prompt-architecture.md).

A tool-using agent adaptation may need both. A short self-contained task or simple
wording fix can use the guidance here without loading either reference.

## Compose in three passes

### 1. Thinking

Define the cognitive architecture through observable decisions and checkpoints:

- State the intent and terminal condition before techniques.
- Route facts to their source of truth before asking the model to infer.
- Order dependent work; permit independent inspection to run together when the
  runtime supports it.
- Separate diagnosis from mutation, observation from inference, and a delegated
  result from verified evidence.
- Specify what must be checked, not private chain-of-thought that must be exposed.
- Classify the request before acting: answer, review, and status requests authorize
  inspection and reporting; diagnosis does not imply repair; change requests cover
  normal in-scope implementation; monitoring authorizes observation, not new effects.
- Ground `done`, `fixed`, `saved`, `sent`, and `verified` in fresh evidence observed
  during the current execution. Report skipped, failed, or partial checks plainly.

Prefer `inspect → diagnose → change → verify` over “think carefully.” Prefer a
concrete completion test over “provide the best answer.”

### 2. Expression

Make the language carry behavior:

- Read a useful exemplar as a sequence: what does each sentence make the model
  attend to, why does it come here, and which misreading does an example resolve?
  Transfer that mechanism into the target task; retain useful original phrasing
  when it performs the same function in the target.
- Use concrete nouns and active verbs for actions and boundaries. Replace empty
  qualities with observable criteria; retain a useful image, cadence, or role
  framing when it steers the intended work.
- Establish the audience and relationship before choosing tone. Preserve the
  existing deployment language unless change is requested or the target contract
  requires it; English and a colleague voice are not universal defaults.
- Order instructions by decision time. Put prerequisites before actions and
  exceptions beside the rule they qualify.
- Use a positive default to establish the normal path; reserve `never`, `must`, and
  `do not` for hard boundaries.
- Compress repeated meaning, not distinct decisions. Expand only where ambiguity is
  expensive.
- Keep examples few and purposeful. A contrast can clarify a fragile boundary; a
  complete worked example can teach voice, sequence, and density. Let explicit
  requirements govern when incidental example details conflict with them.
- Match the target surface's language, markup, and tool-call contract. Select a
  coherent clarification default and place its exceptions nearby; do not combine
  contradictory defaults from different source templates.
- Treat prose, tables, visuals, artifacts, and response components as presentation.
  They may expose evidence, but cannot manufacture facts or broaden permission.

Let rhythm reveal hierarchy: a default, a reason when useful, and an example where
it changes interpretation. This is a useful pattern, not a required paragraph form.
For local revisions, check actor, trigger, scope, obligation, exception, and result
before claiming that meaning is unchanged.

### 3. Runtime and state

For tool-using or stateful prompts, keep stable behavior separate from injected
state. Skip runtime machinery when the target task does not need it:

- Treat current time, environment, memory, project instructions, tool registries,
  and user context as runtime inputs, not timeless identity.
- Register each capability with its source authority, inputs, side effects,
  confirmation boundary, returned evidence, and failure handling.
- Never let tool availability imply permission.
- Define how new messages replace, extend, pause, resume, or request status from the
  active task when continuity matters.
- Preserve objective, decisions, authorization, completed evidence, pending work,
  and provenance across recovery or compaction.

## Control freedom

Match instruction strength to failure cost:

- Use **high freedom** for taste, synthesis, and open-ended generation.
- Use **medium freedom** for preferred patterns with legitimate variation.
- Use **low freedom** for schemas, destructive effects, authorization, protocol
  order, and recovery invariants.

Do not over-specify harmless choices. Do not leave irreversible or externally
visible behavior to implication.

## Review the prompt

Review from eight lenses: intent, cognition, information architecture, expression,
attention, runtime, constraints, and recovery. Treat them as diagnostic lenses, not
mandatory headings.

Check that:

- the strongest wording protects the highest-cost failure rather than stylistic
  preferences;
- later instructions do not silently contradict earlier ones;
- every tool, memory, and context source has a distinct authority;
- output requirements can be verified without guessing hidden reasoning;
- simple inputs remain simple, edge inputs take the intended branch, and interrupted
  work resumes from the correct state;
- examples generalize to a new input without importing their facts, product
  capabilities, or incidental style as requirements;
- an expression-only revision preserves the original decision boundaries and
  output contract, while an intended behavior change is identified.

For a reusable or high-impact prompt, exercise representative normal, boundary,
conflict, and recovery cases. Evaluate observable decisions and outputs. Do not ask
the model to reveal private reasoning.

## Deliver

Lead with the copyable prompt in a fenced block or the requested target file. When
deployment depends on them, state the architecture choice, unresolved placeholders,
and material trade-offs the user needs to deploy or revise it. When revising an
existing prompt, explain the behavioral change rather than narrating every wording
edit.

When source adaptation matters, identify the source and distinguish faithful
parameterization, behavioral adaptation, and an independently written template.
Explain the borrowed expression mechanism only when it helps the user apply or
review the result. Do not present an adapted template as a verbatim original.

If the user asks for “just the prompt,” provide just the deployable prompt.
