# Prompt Notes Snapshot Refresh Design

## Goal

Refresh `hufaei.github.io/my-skills` as a current learning snapshot, not a branch history or changelog. Preserve the existing card-to-detail reading experience and the high-value structure of every note while adding two new model families selected by the user: GPT-5.6/Codex Runtime and Claude Sonnet 5/Claude Code 2.1.207.

## Source boundary

- Source repository: `asgeirtj/system_prompts_leaks` at commit `5c86715f453f0eca188451a48bf5b165831d8b29` dated 2026-07-12.
- The notes are study summaries, not official product documentation and not verbatim reproductions of the source prompts.
- Source links point to immutable commit URLs so the learning snapshot remains reproducible.
- Existing claims are retained unless the current source snapshot disproves them. New material is integrated as current understanding rather than presented as a commit-by-commit narrative.

## Information architecture

The home page remains a responsive card grid. It will contain six cards:

1. GPT-5.6 / Codex Runtime — new, marked as a current snapshot.
2. Claude Sonnet 5 / Claude Code 2.1.207 — new, marked as a current snapshot.
3. GPT-5.5 Prompt Framework — retained and expanded with source attribution and its relationship to the newer Codex runtime.
4. Claude Fable 5 / Claude Code — retained as the earlier engineering-agent baseline and linked forward to the Sonnet 5 note.
5. Grok Prompt Evolution — retained, with portable source links replacing machine-local paths.
6. Gemini Prompt Family — retained, with portable source links replacing machine-local paths.

Each detail page preserves the current core sequence:

1. title and compact learning focus;
2. large overview learning map;
3. Markdown note with a one-sentence thesis;
4. model/runtime decomposition and comparisons;
5. a reusable `FrameworkNote` template in a dark code block;
6. review questions;
7. immutable source index and snapshot metadata.

## New note: GPT-5.6 / Codex Runtime

The note teaches GPT-5.6 as one layer inside a larger Codex runtime, rather than treating the model prompt as the whole agent. It separates:

- model personality and communication contract;
- commentary/final channel protocol;
- workspace and file-editing rules;
- autonomy, persistence, and authorization boundaries;
- skill discovery and routing;
- full runtime tool contracts;
- browser/computer-use layers;
- evidence gathering, side effects, verification, and delivery.

Its reusable `FrameworkNote: For Every Codex Runtime Request` follows a practical execution chain: classify, locate source of truth, load instructions, define authority, decide ask/proceed, route the narrowest capability, preserve workspace state, communicate progress, verify, and deliver.

## New note: Claude Sonnet 5 / Claude Code 2.1.207

The note separates the Sonnet 5 general assistant prompt from the Claude Code capability layer. It teaches:

- assistant identity, style, safety, and artifact behavior;
- code-workspace autonomy and evidence;
- reusable skills as operational playbooks;
- settings/hooks/permissions through `update-config`;
- environment diagnosis through `doctor`;
- review effort levels and structured findings;
- visualization and artifact-production skills;
- compact, rewind, continuation, and fake-user-turn resistance in 2.1.207;
- Git, side-effect, verification, and delivery boundaries.

Its reusable `FrameworkNote: For Every Claude Code Task` follows: classify, inspect workspace, discover instructions/skills, choose effort, preserve authorization boundaries, execute conservatively, manage context continuity, verify, inspect Git state, and report.

## Visual design

The visual language stays close to the current site: warm off-white background, white panels, dark text, restrained blue accent, thin borders, and generous reading width. Changes are limited to scanability:

- two-column desktop card grid so six cards read as a catalog rather than a single sparse row;
- compact family and “latest snapshot” badges;
- snapshot date/source line on detail pages;
- clearer focus/hover states and mobile stacking;
- improved typography and table/code overflow without changing the core layout.

The two new learning maps are deterministic 1600×900 PNGs generated from SVG. This is deliberate: generative image tools are useful for illustrative covers, but these diagrams contain exact Chinese and English labels that must remain correct and legible. Each map uses six numbered modules, a central request-to-delivery flow, principle callouts, and a one-line memory hook, matching the existing infographic role while improving text accuracy.

## Implementation boundaries

- Keep the one-file static reader architecture in `docs/index.html`; do not add a framework or package dependency.
- Add one Markdown file and one PNG per new note.
- Update the existing four Markdown notes in place; do not replace them with changelogs.
- Keep the GitHub Actions Pages workflow unless validation shows it cannot publish the new files.
- Add a lightweight repository validation script and tests for card metadata, note structure, assets, and build output.

## Data flow and failure handling

The Pages workflow copies every `notes/*/README.md` into `_site/content`, copies the mind-map assets, and creates a route directory for each slug. The browser reads the route, resolves the note metadata from the static catalog, fetches its Markdown with `cache: no-store`, and renders it with `marked`.

Validation fails before deployment when a card has no note, image, required `FrameworkNote`, review section, or source index. At runtime, Markdown fetch failures remain visible as a readable error panel. Missing or unknown routes return the existing note chooser rather than a blank screen.

## Verification and deployment

Before pushing:

- run the validation tests once in a failing state before implementation and again after implementation;
- build `_site` using the same copy logic as GitHub Actions;
- verify six cards, six routes, six Markdown payloads, six mind maps, required note sections, and 1600×900 dimensions for the two new maps;
- serve the built site locally and inspect the home page and both new detail pages at desktop and mobile widths;
- review `git diff` and repository status.

After pushing `main`, monitor the `Publish notes to GitHub Pages` workflow to completion, then open the public home page and both new routes to confirm the deployed snapshot.
