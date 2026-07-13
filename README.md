# Personal Codex Skills

Installable personal Codex skills. This repository is private and stores reusable skills that can be installed globally or into a project.

## Skills

- `prune-merged-worktrees`: audit and clean local Git branches and linked worktrees while preserving branches not merged into a base branch.

## Notes

- `notes/gpt-5.6-codex-runtime`: GPT-5.6/Codex runtime notes for reviewing model behavior, workspace rules, skills, tool routing, authorization, browser/computer layers, verification, and delivery.
- `notes/claude-sonnet-5-claude-code-2.1.207`: Claude Sonnet 5 and Claude Code 2.1.207 snapshot notes for reviewing assistant behavior, bundled skills, configuration/doctor workflows, review effort, artifacts, and compact continuity.
- `notes/gpt-5.5-prompt-framework`: GPT-5.5-style system prompt framework notes for reviewing task routing, source-of-truth mapping, safety boundaries, tool contracts, and final-response shaping.
- `notes/claude-fable-5-claude-code-prompt-framework`: Claude Fable 5 / Claude Code-style prompt framework notes for reviewing workspace evidence, coding-agent autonomy, tool routing, verification, Git boundaries, and differences from GPT-5.5.
- `notes/grok-prompt-evolution`: Grok prompt evolution notes for reviewing X/web-first routing, tool schemas, render components, multi-agent experiments, remote sandbox behavior, and differences from GPT-5.5 and Claude Code.
- `notes/gemini-prompt-family`: Gemini prompt family notes for reviewing Gemini Pro orchestration gates, Gemini Flash Web UI rendering, Nano Banana image tool contracts, and differences from GPT-5.5, Claude/Fable, and Grok.

All six notes are maintained as a current learning snapshot rather than a repository changelog. The current source boundary is `asgeirtj/system_prompts_leaks@5c86715f453f0eca188451a48bf5b165831d8b29` (2026-07-12); each note links to immutable source files at that commit.

## GitHub Pages Notes Site

The prompt engineering notes can be published as a static GitHub Pages reader. The workflow in `.github/workflows/pages.yml` builds `docs/index.html` and copies every `notes/*/README.md` into the Pages artifact.

Public notes URL:

```text
https://hufaei.github.io/ai-prompt-atlas/
```

In repository settings, set Pages source to **GitHub Actions**. For private repositories, GitHub Pages availability and private site visibility depend on the GitHub plan and organization/enterprise settings.

## Install From GitHub

In Codex, install any skill path from this repository:

```text
https://github.com/hufaei/ai-prompt-atlas/tree/main/skills/prune-merged-worktrees
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
