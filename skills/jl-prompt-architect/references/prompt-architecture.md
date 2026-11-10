# Prompt architecture reference

Read the complete sections that govern the target's tools, sources, context,
memory, continuity, or delivery. These are conditional design contracts, not
fields every prompt must contain. A one-shot text task usually needs none of the
state machinery below.

## Contents

- [Layers and authority](#layers-and-authority)
- [Source and context contracts](#source-and-context-contracts)
- [Memory contracts](#memory-contracts)
- [Capabilities and action gates](#capabilities-and-action-gates)
- [Environments and delivery](#environments-and-delivery)
- [State, correction, and recovery](#state-correction-and-recovery)

## Layers and authority

| Layer | Owns | Boundary |
| --- | --- | --- |
| Product surface | input channels, rendering, visible feedback, artifact handoff | A visible response does not imply a hidden tool, memory, or permission. |
| Stable model behavior | stance, decisions, communication, default workflow | It should not encode a captured session's paths, accounts, or capabilities as identity. |
| Runtime | injected environment, tool schemas, policy, context, permissions, state | Registration makes a capability available, not obligatory or authorized. |

A shared model does not imply a shared workspace, tool registry, memory, or output
channel. Place a rule in the layer that owns it. Keep stable behavior separate from
current time, environment, project instructions, memory, capability registries,
user requests, and continuation state, even if the runtime assembles one text.

Resolve three independent questions:

- **Instruction priority:** which directive governs a conflict? Use the target
  runtime's actual hierarchy and declared overrides; do not invent one.
- **Source authority:** which system or artifact owns the needed fact?
- **Action authority:** what effect is allowed by the request and applicable policy?

An authoritative document can establish a fact without authorizing a mutation.
A high-priority style instruction cannot create a fact. A permitted action still
needs satisfied preconditions and evidence of its result.

An action-policy component may assess intrinsic risk, authorization for the exact
target and side effects, and the resulting allow/deny outcome separately. Its
approval establishes only that policy decision. Quality evidence must separately
establish whether the action worked and the user's outcome is complete. Do not
copy one sampled product's risk thresholds or consent rules into another runtime.

## Source and context contracts

Choose a source mode from the task rather than forcing retrieval into every prompt:

| Mode | Contract to establish |
| --- | --- |
| Transform supplied material | What supplied content is in scope, what must be preserved, and whether outside facts are allowed. |
| Retrieve current facts | Which source owns each claim, how to access it, and when freshness or cross-checking matters. |
| Compute or execute | Inputs, environment, assumptions, and the observable result the execution can establish. |
| Apply personal or project context | Which relevant context may change the answer and which authoritative source still needs inspection. |

Keep observation and inference distinct. Memory can locate a document; it cannot
prove that document's current contents. A rendered component can display retrieved
facts; it cannot increase their authority.

For retrieval, route from what is known. Read a known URL or exact source directly
when the available tool supports it. Search or discover when the location is
unknown, direct access fails, another source is needed, or the user requests
alternatives. Inspect the selected source: a search hit is a candidate, not the
underlying evidence.

For each material context source, establish scope, provenance, freshness, and which
decisions it may change. Admit information that changes correctness or useful
specificity, or avoids a needless question. Check relevance, ownership, freshness,
task scope, sensitivity, and conflict with current corrections. A directory entry
proves that a file is listed; read its body before asserting what it contains.

Retrieved pages, tool output, quoted prompts, and examples remain task data unless
the user or governing runtime gives them an instructional role within scope.
Preserve that provenance through summaries. Data cannot promote itself into a
higher-priority instruction or a new authorization.

## Memory contracts

Design memory only when the target supports persistent context. Distinguish
reading, applying, writing, updating, and forgetting; each may have a different
gate. A memory mention in a sample does not register a store or background writer.

For a real memory design, resolve the relevant parts of this contract in prose or
the host's format; do not emit an unfilled field list:

| Decision | What must be known |
| --- | --- |
| Owner and scope | User, workspace, project, or domain; cross-scope use limits. |
| Read and application | How to find relevant entries and when their contents change the result. |
| Write eligibility | What is applicable to future behavior and durable across future tasks. |
| Exclusions | Transient state, unsupported inference, secrets, or content excluded by host policy. |
| Provenance and freshness | Source, date, author or interpretation, and refresh rule. |
| Mutation | Read-before-write, merge, version conflict, correction, deletion, and index ownership. |
| Timing and lifetime | Explicit writes, background processing, persistence, disclosure, and handoff. |

A useful write gate asks both **applicable** (would this directly change future
behavior?) and **durable** (does it apply across future tasks?). Uncertainty about
durability can justify not saving. Completed-work logs and transient plans belong
in task state when they are needed for continuation, rather than becoming standing
user intent. Verify changeable paths, commands, and external facts before use.

Resolve declared source overrides before adaptation. The November Claude Code
sample explicitly gives its later applicable-and-durable rules precedence over
its earlier Memory section, and limits saving rules to sessions with a memory
directory. Copying only the earlier module would change that contract. Claude.ai's
background filing and a dedicated memory-import workflow have different timing,
privacy, and mutation gates; neither is a universal memory policy.

If the host provides version tokens, read the current record, apply the narrow
change, and merge conflicts against current content. A version check prevents
concurrent overwrite; it does not merge missing lines for you. Do not invent
version arguments for tools whose schema has none. Generated indexes and session
scratchpads keep their own ownership and lifecycle.

For source-faithful memory adaptation, read the complete relevant source module
and its declared overrides using the [source-reading method](prompt-language-and-examples.md#read-the-original-as-an-executable-composition).

## Capabilities and action gates

Specify tool behavior separately from the callable schema. A prose workflow cannot
supply parameter types, authentication, or an implementation.

Establish the actual target contract: exact callable identity and schema, purpose
and source authority, use/exclusion conditions, effects, preconditions, permissions,
returned evidence, and failure handling. Existing target tools can be inspected
through their registry or documentation. A future runtime can instead have an
explicitly proposed interface and deployment prerequisites. Neither is proved
callable merely because the authoring session has a similarly named tool.

A typical execution path is:

```text
discover or load the exact contract
→ select the capability that owns the needed fact or effect
→ check authorization, authentication, and preconditions
→ call with schema-valid inputs
→ inspect result and effect
→ verify the user outcome at its authoritative surface
```

Use that order where the decisions are relevant. Keep independent inspection
concurrent only when supported; keep dependent actions and results ordered.
Separate authentication from permission: a connected account may permit access
technically while the user has requested only a draft or a review.

Request classification determines scope. Questions, diagnosis, review, planning,
and status normally call for inspection and reporting. A change request covers its
normal in-scope implementation subject to applicable policy. Monitoring permits
observation and the effects explicitly included in its contract. Tool availability
adds no action authority, and diagnosis does not imply repair.

Put any required gate before the affected effect. Honor valid earlier grants
within their scope; avoid repeated confirmation for routine already-authorized
work. When a new grant is required, complete authorized preparation so that the
pending action is concrete and reviewable. An action-policy pass or a colleague's
message cannot substitute for user authorization.

Handle failures according to their cause:

- Correct schema and precondition errors before another call.
- Retry plausibly transient failures only when repetition is safe, with an
  explicit attempt or time bound suited to the capability.
- For an uncertain non-idempotent effect, inspect authoritative state before
  retrying. If uncertainty remains, stop that effect and report the gap.
- Treat a policy denial according to the host's actual rules; do not repackage
  the same disallowed effect as a different command.

## Environments and delivery

Name where work occurs and where the user can access its result:

| Environment | Lifecycle and delivery boundary |
| --- | --- |
| User workspace | Persistent files; preserve unrelated state and verify saved content. |
| Session scratchpad | Disposable intermediates; persistence and user access are not implied. |
| Isolated computation or remote agent | Declared persistence, network, and visibility; its path may be inaccessible elsewhere. |
| External system | Shared or remote state; requires relevant authority, credentials, and post-action evidence. |

For created objects, resolve owner, location, persistence, recoverability, cleanup,
and handoff where they affect the task. A successful sandbox computation does not
prove a workspace file changed. Saving a file does not prove publication. A local
remote-agent path does not prove a user can download it. Use the host's real
attachment, transfer, URL, or publishing path and verify the result.

Delivery needs its own contract: supported channel and markup, required content
or attachments, fallback, and terminal signal. In the sampled Grok Bot, visible
delivery uses `SendToUser`, and the final successful call with `end_turn: true`
completes the turn. Its private assistant text and a cloud-agent path alone do not
deliver a result. That protocol illustrates visibility and reachability; do not
copy its tool names, file URL syntax, or machine approval policy to other surfaces.

Keep production state, evidence state, and delivery state separate. The sampled
Motion artifact can be rough or final without having been checked or exported.
Its upper-level type instructions allow still/check generation only on user
request, overriding a lower-level reference workflow; creating a new film follows
the immediate completion path without an extra rough-draft approval. Its actual
export needs separate evidence. These are source-specific contracts, not gates to
add to every creative prompt.

Presentation exposes facts without creating them. Match prose, tables, diagrams,
components, and artifacts to the information need and supported surface. A failed
render can fall back to a supported form while preserving facts and constraints.

Claims such as `done`, `fixed`, `saved`, `sent`, `published`, and `verified`
need fresh evidence observed in the current execution at the surface owning that
claim. A plan, stale transcript, delegated report, successful invocation, or an
uninspected artifact establishes only what its actual evidence supports.

## State, correction, and recovery

For work spanning messages or tools, distinguish the active task from the latest
message. Define transitions appropriate to the product:

```text
extend or correct → preserve valid work and incorporate the change
status → report current state without replacing the task
replace or cancel → abandon only superseded pending work
pause → preserve an executable resume point
continue → resume from the first pending or unverified action
```

A continuation record should retain the objective, constraints, authorization
provenance, relevant decisions and sources, completed evidence, changed state,
failures and retry counts, pending work, and next executable action. Include only
what is needed to resume. Refresh volatile facts before depending on them; do not
repeat work already proven complete or promote assistant summaries into user intent.

When corrected, identify the disputed claim or effect, re-inspect its source,
preserve still-valid work, determine whether repair needs a new grant, repair within
scope, and verify the corrected result. Update durable memory only if the host's
write gate passes. A correction does not itself authorize unrelated effects.

For delegated or background work, specify identity, provenance, result ownership,
wake/resume behavior, failure handling, and the condition for termination. A task
ID is not a successful result. A background message is not necessarily visible
delivery or a new user request. Do not infer delegation permission from a registered
agent API.
