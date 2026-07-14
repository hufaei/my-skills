# Source-Shaped Prompt Templates Design

## Problem

The six note pages currently present assistant-authored execution summaries as reusable prompt examples. Those summaries are useful as structural interpretations, but they do not preserve the source prompts' writing form, section order, instruction density, exceptions, or runtime layering.

The approved correction is to make each reusable prompt example a parameterized, source-shaped template rather than a newly invented universal workflow.

## Content contract

Every reusable prompt example must:

1. follow the source material's major section order and instruction style;
2. preserve general behavioral rules, gates, exceptions, and completion criteria;
3. replace provider-specific payloads with named slots using `{{FIELD_NAME = ...}}`;
4. leave each slot where the source-specific content originally participates in the prompt;
5. keep enough surrounding prose that a reader can understand how to fill and use the slot;
6. separate model, runtime, tool, skill, and UI layers when a note combines multiple source files;
7. avoid presenting a compressed numbered hierarchy as the primary prompt example.

Named slots cover identity, model/version names, current time/location, personality text, product capabilities, quotas, tool names and schemas, sandbox paths, environment details, render-component syntax, connector registries, and other deployment-specific data.

The templates may minimally paraphrase source wording, but they must preserve the source instruction's function and local context. They must not reproduce large source files verbatim.

## Page-specific shape

### GPT-5.5 Prompt Framework

Preserve the Codex behavior prompt's order: identity and personality slot, `General`, engineering judgment, frontend guidance, editing constraints, special requests, autonomy, working with the user, formatting, final answer, and intermediate updates. Represent consumer-runtime tool catalogs as a reusable runtime-extension slot rather than merging them into a generic request loop.

### Claude Fable 5 / Claude Code

Preserve the runtime order: `Harness`, communication, session guidance, environment, context management, tools, Git, plan/worktree behavior, task tracking, web tools, resume behavior, and write/edit behavior. Replace individual tool implementations with a repeatable tool-registration template containing use conditions, exclusions, parameters, effects, confirmation requirements, and result handling.

### Grok Prompt Evolution

Use the Grok 4.3-style order: base behavior, environment information, context snapshot, available tools, render components, and skills. Keep the older-version evolution in the explanatory note, while the reusable example exposes tool and render-component slots in the source-shaped locations.

### Gemini Prompt Family

Keep the Gemini base assistant instructions, capability-only quarantine, response/format guidance, strict-completion versus expert-guide rules, personalization gates, visual gate, interactive-widget gate, and output/component contracts. Product names, quotas, image models, widget implementations, and component syntax become slots.

### GPT-5.6 / Codex Runtime

Preserve the model behavior prompt's order: personality, writing style, technical communication, working with the user, commentary/final channels, final formatting, visualization rules, work rules, editing constraints, autonomy, and skills. Follow it with explicit runtime-extension slots for app context, environment context, tools, plugins/connectors, and confirmation policies instead of rewriting the whole runtime as a ten-step loop.

### Claude Sonnet 5 / Claude Code 2.1.207

Provide two clearly separated source-shaped layers: the assistant base layer and the coding runtime layer. The base layer retains tone, proactivity, policy gates, artifacts, visual routing, connectors, and tool discovery. The coding layer retains harness, communication, environment, context continuity/compaction, skills, task tracking, configuration/doctor patterns, review effort, and delivery behavior. Product-specific tools and bundled-skill bodies become slots.

## Existing material

- Keep each page's explanatory sections, comparisons, source index, and review questions.
- Keep the current mind maps as structural learning aids.
- Reframe any remaining compressed workflow as `结构解读`; it must not be labeled as the reusable prompt itself.
- Do not change card titles, note slugs, routes, or map assets.

## Verification

Add a site-contract test that extracts the reusable prompt block from every note and asserts:

- named `{{FIELD = ...}}` slots exist in meaningful quantity;
- the block is long enough to be a usable prompt rather than a short outline;
- page-specific source-order markers are present;
- the old disclaimers that explicitly describe the template as a non-source execution-chain abstraction are absent.

Run the full test suite, reproduce the Pages build, inspect all six rendered note pages, deploy to GitHub Pages, and verify the public site.
