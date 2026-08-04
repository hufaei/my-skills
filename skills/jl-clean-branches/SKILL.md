---
name: jl-clean-branches
description: Use when the user explicitly invokes $jl-clean-branches or asks to clean, prune, audit, or remove local branches, remote-tracking branches, remote branches, or Git worktrees after changes have been merged.
---

# JL Clean Branches

## Safety contract

Scan first, explain candidates, and obtain confirmation before deletion. Never
delete the current branch, the default branch, a branch with unmerged commits,
a dirty Worktree, or a branch whose remote/PR state is uncertain.

## Inventory

1. Resolve the repository root, remotes, remote default branch, current branch,
   upstreams, and worktree registrations.
2. Fetch and prune remote-tracking references without deleting remote branches.
3. List local branches with upstream, ahead/behind state, last commit, and every
   attached Worktree.
4. List remote and remote-tracking branches separately. A vanished tracking
   reference is not proof that a local branch is safe to delete.
5. Determine merge status against the current remote default branch. When a PR
   used squash or rebase merging, use authoritative PR state plus patch or
   commit equivalence instead of relying only on ancestry.

## Classify candidates

Place every branch or Worktree into one of these groups:

- **Safe local cleanup:** merged into the agreed base, no unique commits, not
  current, and not attached to a dirty Worktree.
- **Review required:** PR merged but ancestry differs, remote branch still
  exists, upstream is gone, or patch equivalence needs confirmation.
- **Protected:** unmerged or ahead commits, open PR, unknown remote state,
  default/current branch, dirty Worktree, or externally managed Worktree.

Show the evidence and exact proposed operations. Ask separately before deleting
local branches, Worktrees, or remote branches; remote deletion is never implied
by local cleanup.

## Execute approved cleanup

- Remove only clean Worktrees explicitly selected by the user. Never remove an
  externally managed Worktree solely because it looks stale.
- Use safe local branch deletion; do not force-delete unless the user sees the
  unique commits and explicitly authorizes their loss.
- Delete only the named remote branches the user approved.
- Prune registrations and remote-tracking references after confirmed cleanup.

Finish with retained protected items, removed items, recovery information when
available, and anything that still needs human judgment.
