---
name: jl-engineering-orchestra
description: Use only when the user explicitly invokes $jl-engineering-orchestra or selects it for a repository engineering task that benefits from plan-before-execution control, adaptive inline or multi-agent implementation, optional isolation, selective TDD, review, and evidence-based completion.
---

# JL Engineering Orchestra

## Purpose

Run the complete JL engineering workflow without making it the default for
small or obvious tasks. Keep the current task responsible for scope, dispatch,
review, correction, and final judgment. Default to multi-agent execution, but
handle a simple, well-bounded change inline when delegation would add no value.

Separate discussion from execution. Inspect, reason, and plan first. Do not
modify the repository or start implementation until the user explicitly says
`执行` after seeing the plan.

## Required JL dependencies

Use only the installed `jl-*` dependencies listed below. Never silently fall
back to an unprefixed or separately installed upstream version.

- `jl-dispatching-parallel-agents`
- `jl-test-driven-development`
- `jl-using-git-worktrees`
- `jl-ponytail`
- `jl-test-philosophy`
- `jl-requesting-code-review`
- `jl-receiving-code-review`
- `jl-verification-before-completion`
- `jl-doc-steward`

Before starting, resolve the installed Skill root as the parent directory of
this `jl-engineering-orchestra` directory. Verify that every dependency has a
readable sibling file at `<installed-skill-root>/<dependency>/SKILL.md`.

Do not inspect the source repository's `skills/` and `synced/` directories to
decide what is installed: they distinguish owned and upstream-managed source,
not installation state. Stop only when an installed sibling is actually
missing or unreadable; never substitute an unprefixed Skill.

Before following a dependency's workflow, read that sibling `SKILL.md`
completely, plus each reference it explicitly requires. Do not rely on
implicit Skill invocation to compose this workflow.

## Workflow

### 1. Establish the repository baseline

Read applicable repository instructions, contributor documentation, manifests,
architecture documents, and task runners. Record the current branch, base
branch, `HEAD`, upstream, worktrees, and existing tracked or untracked changes.
Preserve all pre-existing user work.

### 2. Shape the change

Clarify the requirement, boundaries, acceptance criteria, and design in the
conversation. Inspect repository evidence before proposing a solution. Ask the
user only about missing product direction, authority, or material scope; infer
ordinary engineering choices and explain them in the plan. Present alternatives
only when they represent a material trade-off, and lead with a recommendation.

### 3. Select defaults without routine questions

Honor explicit user choices. Otherwise infer execution mode, TDD, and isolation
from the task and repository, record the decisions in the plan, and do not ask
the user to choose among routine engineering preferences.

Default to multi-agent execution. Work inline only when the requirement and
acceptance criteria are clear, the change is localized and low-risk, it does
not alter architecture, authorization, data migration, production boundaries,
or a public contract, and the current task can implement and verify it
directly.

Judge complexity primarily by coupling, uncertainty, contract and operational
risk, reversibility, and verification breadth. Use estimated or actual diff
size, file count, dispersion, and review volume as lower-weight signals. Large
mechanical or generated diffs can remain simple; a small authorization,
migration, or public-contract diff can remain complex.

Treat a task as medium when it may cross several components or layers but has
one coherent outcome, known boundaries, a reversible approach, and a clear
verification path. Treat cross-domain architecture, migrations, security or
authorization, public-contract changes, hard-to-reverse behavior, or
substantial unknowns as complex. Use multi-agent execution for both medium and
complex tasks; scale parallel investigation, implementation isolation, and
review depth to the actual complexity.

Default to TDD only for development of a wholly new feature. Do not default to
TDD for changes to existing features, interfaces, pages, bug fixes,
compatibility work, or refactoring. This changes implementation order, not the
obligation to add useful tests and run verification. The user's explicit TDD
choice always overrides this default.

Default to `jl-ponytail` at full intensity for production implementation. Apply
its minimal-solution ladder only after the requirement and real code path are
understood. It may reduce code, files, dependencies, and abstractions; it may not
shrink accepted behavior, architecture boundaries, validation, error handling,
security, accessibility, migration safety, or verification. The user's explicit
choice to disable or change its intensity always overrides this default.

Select a Worktree when the user requests one or isolation is needed to keep
concurrent implementation safe. Otherwise plan to continue an appropriate
existing feature branch or create an ordinary task branch from a clean default
branch. If pre-existing changes make either choice unsafe, explain the exact
state and ask only for the decision needed to preserve the user's work.

### 4. Plan

Write the plan in the conversation without creating a plan file or modifying
the repository. Make tasks independently reviewable, name exact files and
commands when repository evidence supports them, and keep the plan
proportional to the request. Include:

- complexity and the evidence behind it;
- the low-weight estimated diff signal;
- inline or multi-agent execution;
- TDD, Ponytail, and isolation decisions;
- implementation, review, test, documentation, and verification steps;
- authority boundaries and any unresolved blocker.

End the plan by stating that no implementation has started and wait for the
user to say `执行`. Treat approval, agreement, `继续`, or further discussion as
feedback on the plan, not execution authorization.

### 5. Pass the execution gate

Begin implementation only after the user explicitly says `执行` for the
presented plan. Until then, limit work to read-only inspection, discussion,
design, risk analysis, and plan revision. Do not edit files, install
dependencies, create branches or Worktrees, run implementation agents, commit,
push, or open a pull request.

After authorization, prepare the selected branch or Worktree. If the actual
diff later reveals a material scope expansion, stop, reassess complexity and
verification, present a revised plan, and wait for a new `执行` before
continuing outside the approved scope.

### 6. Implement under supervision

For the default multi-agent mode, delegate bounded investigation,
implementation, and review roles while the controller retains the full plan
and final judgment. Use `jl-dispatching-parallel-agents` only for genuinely
independent work that will not edit shared state. Run dependent or overlapping
work sequentially. For a simple change, implement inline without introducing a
delegation ceremony.

Before writing or changing production code, read and apply `jl-ponytail` at the
selected intensity. Use it to find the smallest complete implementation, not to
skip repository inspection or reinterpret the accepted scope.

The controller reviews raw diffs and evidence between tasks. Do not accept a
worker's completion claim without inspection.

If TDD applies under the default above or was explicitly selected, use
`jl-test-driven-development`. Whether or not TDD applies, use
`jl-test-philosophy` to integrate each discovered risk into the existing test
model and choose additions, revisions, consolidation, or omissions by decision
confidence and maintenance cost. `jl-test-philosophy` owns test selection and
suite shape when its guidance differs from Ponytail's bundled check preference.

### 7. Review and correct

Use `jl-requesting-code-review` after substantive implementation. Process
feedback with `jl-receiving-code-review`: verify each finding against source,
requirements, and executable evidence before accepting it. Apply the smallest
complete correction and repeat review when the correction is material.

### 8. Keep durable documentation honest

Update documentation only when the change affects a documented user workflow,
public command, setup step, compatibility promise, or architectural decision.
Route documentation assessment, synchronization, creation, and review through
`jl-doc-steward`. Let it select the appropriate document type and any required
README or ADR sub-skill; do not call those sub-skills directly from this
workflow.

### 9. Prove completion

Use `jl-verification-before-completion`. Run the repository's required gates
unless the user explicitly limits them, distinguish simulated checks from real
integration evidence, and report unverified risks without upgrading them into
success claims.

## Authority boundary

Repository work does not imply permission to commit, push, create or merge a
PR, deploy, migrate data, change production configuration, or touch real user
data. Perform those actions only when explicitly authorized in the current
request.

The final report must state what changed, review corrections, commands and
results, unresolved risks, and whether the work is local, committed, pushed,
opened as a PR, merged, or deployed.
