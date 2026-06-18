---
name: prune-merged-worktrees
description: Use when cleaning local Git branches or linked worktrees, especially stale branches with gone upstreams, many worktrees under .worktrees, Windows cleanup failures like Filename too long or Directory not empty, or requests to delete everything already merged into dev/main while preserving unmerged work.
---

# Prune Merged Worktrees

## Overview

Clean local Git branches by reachability from an explicit base branch. Preserve anything not merged into the base, protect the current branch and long-lived branches, and remove clean linked worktrees before deleting their branches only after explicit confirmation.

## Workflow

1. State the success rule before deleting: branches not merged into the base are kept; the current branch and protected branches are kept.
2. Run `git fetch --all --prune`.
3. Inspect status, branch tracking, merge state, and worktrees:

```powershell
git status --short --branch
git branch --format "%(refname:short)|%(upstream:short)|%(upstream:track)|%(committerdate:iso8601)|%(objectname:short)|%(subject)" --sort=-committerdate
git branch --merged origin/dev
git branch --no-merged origin/dev
git worktree list --porcelain
```

4. Classify branches:

| Class | Action |
| --- | --- |
| Current branch | Keep |
| `dev`, `main`, release or other user-protected branch | Keep |
| Not merged into base | Keep |
| Merged into base and not protected | Candidate |
| Candidate checked out by linked worktree | Remove that worktree first, then delete branch |
| Dirty linked worktree | Stop and ask |
| Windows `Filename too long` or `Directory not empty` cleanup failure | Re-run the helper; it removes clean repo-local `.worktrees` directories with long-path-safe PowerShell and then prunes metadata |
| Unregistered directory under `.worktrees` | Report it; do not delete it unless it is verified as stale |

5. Show the candidate list and ask for confirmation unless the user already gave an explicit deletion rule.
6. Delete candidates with `git branch -d`, not `-D`, unless the user explicitly asks to force delete.
7. Re-run the audit and summarize what remains.

## Helper Script

Use `scripts/audit-git-worktree-branches.ps1` for repeatable audits and optional cleanup:

```powershell
powershell -ExecutionPolicy Bypass -File path\to\scripts\audit-git-worktree-branches.ps1 -Repo C:\path\repo -Base origin/dev -FetchPrune
```

Dry-run is the default. To delete merged candidates:

```powershell
powershell -ExecutionPolicy Bypass -File path\to\scripts\audit-git-worktree-branches.ps1 -Repo C:\path\repo -Base origin/dev -Delete -RemoveWorktrees
```

The script only treats branches reachable from `-Base` as deletion candidates. It refuses to delete the primary worktree branch, protected branch names, branches not merged into the base, and dirty worktrees. For clean worktrees under the repository's `.worktrees` directory, it uses long-path-safe PowerShell deletion and `git worktree prune` instead of relying on `git worktree remove`, which is fragile on Windows with ignored dependency trees.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Using upstream `[gone]` as the only delete signal | Check merge reachability from the base first |
| Deleting a branch still checked out in `.worktrees` | Remove the clean linked worktree first |
| Treating `git branch --merged` without a base as enough | Pass the intended base, usually `origin/dev` |
| Using `git branch -D` for convenience | Use `-d`; force delete only on explicit request |
| Cleaning before checking dirty status | Run status for every worktree first |
| Trusting `git worktree remove` on Windows dependency trees | Prefer the helper script's long-path-safe cleanup for repo-local `.worktrees` |
| Ignoring half-removed worktrees | Re-run the audit; prune metadata and report unregistered directories before deleting branch refs |
