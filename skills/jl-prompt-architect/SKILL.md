---
name: jl-prompt-architect
description: Use when the user is explicitly designing, writing, revising, debugging, or reviewing prompts intended for an AI model, agent, runtime, tool, skill, or AI-powered product. Also use when an agent project explicitly involves system/developer/user prompt hierarchy, prompt assembly, context injection, tool contracts, instruction priority, state recovery, or prompt evaluation. A short, purpose-built instruction that the user will copy into another AI system counts as prompt engineering. Do not trigger for ordinary prose, documentation, UI copy, general coding, casual requests addressed to Codex, or generic brainstorming unless the requested deliverable is itself a prompt.
---

# JL Prompt Architect

## Contract

Design prompts as executable interfaces, not decorated prose. Make the intended
outcome, decision path, evidence, authority, runtime, output, and recovery behavior
legible. Spend structure only where behavior can diverge.

Return a prompt the user can actually place in its target layer. Do not mistake a
long prompt for a complete prompt or compressed jargon for precision.

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

For agent/system/runtime prompts, tool contracts, prompt hierarchy, state recovery,
or a formal prompt review, read
[prompt-architecture.md](references/prompt-architecture.md). Skip it when the
one-shot shape above already resolves the task.

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

- Use concrete nouns and active verbs. Replace vague qualities with observable
  criteria.
- Order instructions by decision time. Put prerequisites before actions and
  exceptions beside the rule they qualify.
- Use a positive default to establish the normal path; reserve `never`, `must`, and
  `do not` for hard boundaries.
- Compress repeated meaning, not distinct decisions. Expand only where ambiguity is
  expensive.
- Keep examples few and contrastive. Use them to resolve a fragile boundary, not to
  restate the rule.
- Match the target model's language, markup, and tool-call contract. Do not add
  decorative headings or ceremonial roles.
- Treat prose, tables, visuals, artifacts, and response components as presentation.
  They may expose evidence, but cannot manufacture facts or broaden permission.

Let rhythm reveal hierarchy: rule, reason when non-obvious, then the smallest
example that disambiguates it.

### 3. Runtime and state

Keep stable behavior separate from injected state:

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
  work resumes from the correct state.

For a reusable or high-impact prompt, exercise representative normal, boundary,
conflict, and recovery cases. Evaluate observable decisions and outputs. Do not ask
the model to reveal private reasoning.

## Deliver

Lead with the copyable prompt in a fenced block or the requested target file. When
deployment depends on them, state the architecture choice, unresolved placeholders,
and material trade-offs the user needs to deploy or revise it. When revising an
existing prompt, explain the behavioral change rather than narrating every wording
edit.

If the user asks for “just the prompt,” provide just the deployable prompt.
