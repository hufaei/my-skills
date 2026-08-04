---
name: jl-engineering-orchestra
description: Use only when the user explicitly invokes $jl-engineering-orchestra or selects it for a repository engineering task that benefits from deliberate design, optional isolation and TDD, delegated implementation, review, and evidence-based completion.
---

# JL Engineering Orchestra

## Purpose

Run the complete JL engineering workflow without making it the default for
small or obvious tasks. Keep the current task responsible for scope, dispatch,
review, correction, and final judgment. Delegate implementation when useful.

## Required JL dependencies

Use only the installed `jl-*` dependencies listed below. Never silently fall
back to an unprefixed or separately installed upstream version.

- `jl-brainstorming`
- `jl-writing-plans`
- `jl-executing-plans`
- `jl-dispatching-parallel-agents`
- `jl-subagent-driven-development`
- `jl-test-driven-development`
- `jl-using-git-worktrees`
- `jl-lean-tests`
- `jl-requesting-code-review`
- `jl-receiving-code-review`
- `jl-verification-before-completion`
- `jl-readme-blueprint-generator`
- `jl-architecture-decision-records`

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

Use `jl-brainstorming` to clarify the requirement, boundaries, acceptance
criteria, and design. Keep ordinary engineering choices inside the team; ask
the user only about missing product direction, authority, or material scope.

### 3. Ask the three execution choices once

Unless already specified, ask the user to choose:

1. TDD: yes or no.
2. Isolation: Worktree or ordinary branch/current branch.
3. Execution: subagents, visible tasks, or inline execution when delegation is
   unavailable or unnecessary.

If Worktree is selected, use `jl-using-git-worktrees`. Otherwise:

- Continue an appropriate existing feature branch.
- From a clean default branch, create a task branch from the agreed base.
- If the working tree is dirty, do not move changes automatically; present the
  current state and request a choice.

### 4. Plan

Use `jl-writing-plans`. Make tasks independently reviewable, name exact files
and commands, and keep the plan proportional to the request.

### 5. Implement under supervision

For independent tasks, use `jl-dispatching-parallel-agents`. For a plan with
separable implementation tasks, prefer `jl-subagent-driven-development`; use
`jl-executing-plans` when inline execution is the chosen mode.

The controller reviews raw diffs and evidence between tasks. Do not accept a
worker's completion claim without inspection.

If TDD was selected, use `jl-test-driven-development`. Whether or not TDD is
selected, use `jl-lean-tests` to keep the suite focused on meaningful failures
and stable contracts.

### 6. Review and correct

Use `jl-requesting-code-review` after substantive implementation. Process
feedback with `jl-receiving-code-review`: verify each finding against source,
requirements, and executable evidence before accepting it. Apply the smallest
complete correction and repeat review when the correction is material.

### 7. Keep durable documentation honest

Update documentation only when the change affects a documented user workflow,
public command, setup step, compatibility promise, or architectural decision.

- Use `jl-readme-blueprint-generator` for README creation or material updates.
- Use `jl-architecture-decision-records` only for long-lived architectural
  choices, never routine implementation details.

### 8. Prove completion

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
