# Personal Codex Skills

Installable personal Codex skills. This repository is private and stores reusable skills that can be installed globally or into a project.

## Skills

- `prune-merged-worktrees`: audit and clean local Git branches and linked worktrees while preserving branches not merged into a base branch.

## Notes

- `notes/gpt-5.5-prompt-framework`: GPT-5.5-style system prompt framework notes for reviewing task routing, source-of-truth mapping, safety boundaries, tool contracts, and final-response shaping.
- `notes/claude-fable-5-claude-code-prompt-framework`: Claude Fable 5 / Claude Code-style prompt framework notes for reviewing workspace evidence, coding-agent autonomy, tool routing, verification, Git boundaries, and differences from GPT-5.5.
- `notes/grok-prompt-evolution`: Grok prompt evolution notes for reviewing X/web-first routing, tool schemas, render components, multi-agent experiments, remote sandbox behavior, and differences from GPT-5.5 and Claude Code.
- `notes/gemini-prompt-family`: Gemini prompt family notes for reviewing Gemini Pro orchestration gates, Gemini Flash Web UI rendering, Nano Banana image tool contracts, and differences from GPT-5.5, Claude/Fable, and Grok.

## Install From GitHub

In Codex, install any skill path from this repository:

```text
https://github.com/hufaei/my-skills/tree/main/skills/prune-merged-worktrees
```

After installation, restart Codex so the new skills are discovered.

## One-Step Local Install

From a checkout of this repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-my-skills.ps1
```

```bash
chmod +x ./install-my-skills.sh
./install-my-skills.sh
```

Defaults:

- installs every directory under `skills/`
- installs to the current project's `.codex/skills`
- targets Codex only
