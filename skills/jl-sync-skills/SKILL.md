---
name: jl-sync-skills
description: Use when the user explicitly invokes $jl-sync-skills or asks to check, compare, update, or synchronize the upstream-managed skills stored in this my-skills repository.
---

# JL Sync Skills

## Contract

Treat every directory under `synced/` as generated, upstream-managed content.
Never edit it by hand. Update it only through the repository sync script and
keep every change reviewable in Git.

## Workflow

1. Resolve the `my-skills` repository root from this installed Skill's real
   path. Read `sources.yaml` and the current Git status.
2. Run `python3 scripts/sync_skills.py check --json` from the repository root.
   Stop if a synced directory has local modifications relative to its recorded
   generated hash.
3. For each changed upstream, inspect the source diff between the recorded and
   latest commits. Summarize in plain language:
   - source link and commit movement;
   - added, removed, renamed, or moved files;
   - behavior and trigger changes;
   - dependency-reference changes;
   - likely compatibility or migration impact.
4. Present grouped choices: sync all changed Skills, select a subset, or skip.
   Do not apply anything before the user chooses.
5. Run `python3 scripts/sync_skills.py apply <skill...>` for the selected names.
   The script copies the upstream directory, adds only the configured `jl-`
   namespace and dependency transforms, generates UI metadata from the declared
   invocation policy, updates source commits and hashes, and refuses unmanaged
   local edits.
6. Review the resulting Git diff. Call out any unexpected content or transform
   failure instead of repairing a synced directory manually.
7. Ask whether to leave changes in the working tree, create commits, or create
   commits plus an annotated tag. Never push by default.

If a synced Skill needs behavior customization, create a new owned Skill or
explicitly change its management policy; do not hide a permanent patch inside
the generated directory.
