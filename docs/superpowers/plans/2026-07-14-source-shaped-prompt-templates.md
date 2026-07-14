# Source-Shaped Prompt Templates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the six compressed workflow summaries with source-shaped, parameterized prompt templates that preserve source order and instruction density.

**Architecture:** Keep the existing notes, routes, learning maps, comparisons, and review questions. Add test helpers that extract each reusable prompt block and enforce named slots, minimum density, source-order markers, and removal of the old abstraction disclaimers; then rewrite the six prompt blocks in three source-family batches.

**Tech Stack:** Markdown, Python `unittest`, static HTML/JavaScript, GitHub Pages Actions

## Global Constraints

- Use named slots with the exact syntax `{{FIELD_NAME = ...}}`.
- Preserve source-shaped section order and directive style.
- Parameterize provider-specific identity, versions, capabilities, quotas, tools, schemas, environment data, paths, and component syntax.
- Keep explanatory notes, comparisons, source indexes, review questions, note slugs, routes, and map assets.
- Do not use a compressed `For every request` numbered workflow as the primary reusable prompt.
- Do not reproduce the complete source files verbatim.

---

### Task 1: Add reusable-template contract helpers

**Files:**
- Modify: `tests/test_site.py`

**Interfaces:**
- Produces: `reusable_prompt(slug: str) -> str` and `assert_source_shaped_template(slug, markers, minimum_slots=8)`.
- Consumes: note Markdown under `notes/<slug>/README.md`.

- [ ] **Step 1: Add the extractor and assertion helper**

Add below `png_dimensions`:

```python
def reusable_prompt(slug: str) -> str:
    text = (ROOT / "notes" / slug / "README.md").read_text(encoding="utf-8")
    heading = re.search(
        r"^## .*?(?:FrameworkNote|精华版|可复用模板).*?$", text, re.MULTILINE
    )
    if heading is None:
        raise AssertionError(f"missing reusable prompt heading for {slug}")
    block = re.search(r"```text\n(.*?)\n```", text[heading.end() :], re.DOTALL)
    if block is None:
        raise AssertionError(f"missing reusable prompt block for {slug}")
    return block.group(1)
```

Add inside `SiteContractTests`:

```python
def assert_source_shaped_template(
    self, slug: str, markers: tuple[str, ...], minimum_slots: int = 8
):
    note = (ROOT / "notes" / slug / "README.md").read_text(encoding="utf-8")
    prompt = reusable_prompt(slug)
    slots = re.findall(r"\{\{[A-Z0-9_]+\s*=\s*\.\.\.\}\}", prompt)
    self.assertGreaterEqual(len(prompt), 2200, slug)
    self.assertGreaterEqual(len(slots), minimum_slots, slug)
    for marker in markers:
        self.assertIn(marker, prompt, f"{slug}: missing {marker}")
    for disclaimer in (
        "不是源提示词的逐字内容",
        "不是源提示词逐字内容",
        "不是原 prompt 的逐字结构",
        "不是 Grok 原提示词的逐字模板",
    ):
        self.assertNotIn(disclaimer, note, f"{slug}: stale disclaimer")
```

- [ ] **Step 2: Run the existing suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: existing 9 tests pass because no new family-specific contract test has been added yet.

### Task 2: Rebuild the OpenAI prompt templates

**Files:**
- Modify: `tests/test_site.py`
- Modify: `notes/gpt-5.5-prompt-framework/README.md`
- Modify: `notes/gpt-5.6-codex-runtime/README.md`

**Interfaces:**
- Consumes: `OpenAI/Codex/gpt-5.5.md`, `OpenAI/gpt-5.5-thinking.md`, `OpenAI/gpt-5.5-instant.md`, `OpenAI/gpt-5.5-api.md`, `OpenAI/Codex/gpt-5.6.md`, `OpenAI/Codex/codex-full.md`, and the browser/computer runtime files at snapshot `5c86715f453f0eca188451a48bf5b165831d8b29`.
- Produces: two source-shaped reusable prompt blocks.

- [ ] **Step 1: Write the failing OpenAI contract test**

```python
def test_openai_notes_use_source_shaped_parameterized_prompts(self):
    self.assert_source_shaped_template(
        "gpt-5.5-prompt-framework",
        (
            "# General",
            "## Engineering judgment",
            "## Frontend guidance",
            "## Editing constraints",
            "# Working with the user",
            "## Intermediate updates",
            "# Runtime extension slots",
        ),
        minimum_slots=10,
    )
    self.assert_source_shaped_template(
        "gpt-5.6-codex-runtime",
        (
            "# Personality",
            "# Working with the user",
            "## Intermediate commentary",
            "## Final answer",
            "# Rules for getting work done",
            "# Using skills",
            "# Runtime extension slots",
        ),
        minimum_slots=10,
    )
```

- [ ] **Step 2: Run the OpenAI test and verify RED**

Run: `python3 -m unittest tests.test_site.SiteContractTests.test_openai_notes_use_source_shaped_parameterized_prompts -v`

Expected: FAIL because both current blocks contain no named slots and do not preserve the source headings.

- [ ] **Step 3: Replace the GPT-5.5 reusable block**

Use this exact source-order inventory:

```text
You are {{AGENT_NAME = ...}}, a {{AGENT_ROLE = ...}} based on {{MODEL_FAMILY = ...}}.
{{PERSONALITY = ...}}
# General
## Engineering judgment
## Frontend guidance
### Build with empathy
### Design instructions
## Editing constraints
## Special user requests
## Autonomy and persistence
# Working with the user
## Formatting rules
## Final answer instructions
## Intermediate updates
# Runtime extension slots
## Environment and artifact layer
## Tool registry template
## Retrieval and source-of-truth layer
## Model response controls
```

Fill each section with source-faithful directives. Use named slots for frontend domain rules, user-request exceptions, completion condition, progress cadence, environment, artifact contract, tool name/purpose/parameters/return contract, retrieval sources, citation syntax, output channels, and oververbosity.

- [ ] **Step 4: Replace the GPT-5.6 reusable block**

Use this exact source-order inventory:

```text
You are {{AGENT_NAME = ...}}, an agent based on {{MODEL_FAMILY = ...}}.
# Personality
## Writing style
## Technical communication
# Working with the user
## Intermediate commentary
## Final answer
### Formatting rules
### Visualizations
# Rules for getting work done
## File editing constraints
## Autonomy and persistence
# Using skills
### How to use skills
# Runtime extension slots
## App and environment context
## Tool and connector registry
## UI control and confirmation policy
```

Fill each section with source-faithful directives. Use named slots for personality, collaboration surface, status cadence, requested terminal condition, link syntax, visualization threshold, search command, edit method, destructive-operation policy, instruction files, skill catalog, app context, environment context, tools, plugins/connectors, UI surface, and confirmation rules.

- [ ] **Step 5: Run the OpenAI test and full suite**

Run the targeted test, then `python3 -m unittest discover -s tests -v`.

Expected: targeted test and all 10 tests pass.

- [ ] **Step 6: Commit the OpenAI batch**

```bash
git add tests/test_site.py notes/gpt-5.5-prompt-framework/README.md notes/gpt-5.6-codex-runtime/README.md
git commit -m "docs: restore source-shaped OpenAI prompt templates"
```

### Task 3: Rebuild the Anthropic prompt templates

**Files:**
- Modify: `tests/test_site.py`
- Modify: `notes/claude-fable-5-claude-code-prompt-framework/README.md`
- Modify: `notes/claude-sonnet-5-claude-code-2.1.207/README.md`

**Interfaces:**
- Consumes: Claude Code Fable/Opus runtime files, Claude Sonnet 5, bundled skills, and 2.1.207 compact files at the fixed snapshot.
- Produces: two layered, source-shaped reusable prompt blocks.

- [ ] **Step 1: Add and run the failing Anthropic contract test**

Require Fable markers `# Harness`, `# Communicating with the user`, `# Context management`, `# Tools`, `## {{TOOL_NAME = ...}}`, `## Git`, `# Task tracking`, and `# Resume and delivery` with at least 12 slots.

Require Sonnet markers `# Assistant base layer`, `<tone_and_formatting>`, `<proactivity>`, `## Artifact routing`, `## Connector and tool discovery`, `# Coding runtime layer`, `## Context management and compaction`, `## Bundled skill template`, and `# Delivery` with at least 14 slots.

Expected: FAIL against the current compressed blocks.

- [ ] **Step 2: Replace the Fable reusable block**

Preserve the source order `Harness` → communication → session guidance → environment → context management → tools. Represent each concrete tool through a repeated `## {{TOOL_NAME = ...}}` registration containing purpose, when-to-use, when-not-to-use, parameters, state effects, confirmation gate, result contract, and failure recovery. Retain separate Git, plan/worktree, task-tracking, web, resume, and write/edit sections.

- [ ] **Step 3: Replace the Sonnet/2.1.207 reusable block**

Create an `Assistant base layer` followed by a `Coding runtime layer`. Preserve XML-style behavioral/policy tags in the base layer. Retain separate artifact, visual, connector/tool-discovery, harness, communication, environment, compaction/provenance, bundled-skill, task/review-effort, configuration/doctor, and delivery sections. Parameterize the product/tool implementations rather than converting them to a universal task loop.

- [ ] **Step 4: Run the Anthropic test and full suite**

Expected: targeted test and all 11 tests pass.

- [ ] **Step 5: Commit the Anthropic batch**

```bash
git add tests/test_site.py notes/claude-fable-5-claude-code-prompt-framework/README.md notes/claude-sonnet-5-claude-code-2.1.207/README.md
git commit -m "docs: restore source-shaped Anthropic prompt templates"
```

### Task 4: Rebuild the Grok and Gemini prompt templates

**Files:**
- Modify: `tests/test_site.py`
- Modify: `notes/grok-prompt-evolution/README.md`
- Modify: `notes/gemini-prompt-family/README.md`

**Interfaces:**
- Consumes: Grok 3–4.3, Gemini 3.1 Pro, Gemini 3.5 Flash, and Nano Banana 2 API files at the fixed snapshot.
- Produces: source-shaped product/tool and web-assistant templates.

- [ ] **Step 1: Add and run the failing Grok/Gemini contract test**

Require Grok markers `## Environment Info`, `## Context Info`, `## Available Tools`, `## {{TOOL_NAME = ...}}`, `## Available Render Components`, `## {{RENDER_COMPONENT = ...}}`, and `## Skills` with at least 12 slots.

Require Gemini markers `# Assistant identity`, `# Capability-only information`, `# Response guiding principles`, `# Follow-up rules`, `# Personalization gate`, `# Visual support gate`, `# Interactive output gate`, `# Image execution contract`, and `# Output component contracts` with at least 14 slots.

Expected: FAIL against the current compressed blocks.

- [ ] **Step 2: Replace the Grok reusable block**

Preserve base behavior followed by environment, context, tools, render components, and skills. Keep a reusable tool definition in the original location with purpose, parameter schema, execution boundary, returned data, and post-call behavior slots. Keep a parallel render-component definition with trigger, schema, and fallback slots.

- [ ] **Step 3: Replace the Gemini reusable block**

Preserve assistant identity and formatting guidance, quarantine capability data, retain strict-completion/expert-guide branching, personalization gates, visual relevance gate, interactive widget gate, image execution contract, and component output contracts. Parameterize model/tier/quota/capability facts, user-data sources, component names/syntax, image model, tool call schema, and fallback behavior.

- [ ] **Step 4: Run the Grok/Gemini test and full suite**

Expected: targeted test and all 12 tests pass.

- [ ] **Step 5: Commit the Grok/Gemini batch**

```bash
git add tests/test_site.py notes/grok-prompt-evolution/README.md notes/gemini-prompt-family/README.md
git commit -m "docs: restore source-shaped Grok and Gemini templates"
```

### Task 5: Build, render, deploy, and verify

**Files:**
- Verify: `.github/workflows/pages.yml`
- Verify: `docs/index.html`
- Verify: all six note Markdown files

**Interfaces:**
- Consumes: the twelve-test site contract and the existing Pages workflow.
- Produces: updated public note pages at `https://hufaei.github.io/ai-prompt-atlas/`.

- [ ] **Step 1: Run fresh verification**

Run all 12 tests, `git diff --check origin/main...HEAD`, and confirm a clean worktree after commits.

- [ ] **Step 2: Reproduce the Pages build**

Build `_site` exactly as `.github/workflows/pages.yml` and verify six routes, six Markdown payloads, and six mind maps.

- [ ] **Step 3: Inspect all six rendered prompt blocks locally**

Use a real browser to open each note route. Verify the reusable heading is present, the rendered prompt block is at least 2200 characters, named slots are visible, and the page remains within the mobile viewport.

- [ ] **Step 4: Push and monitor Pages**

Push `main`, watch the Pages workflow to `success`, and verify the deployed commit SHA.

- [ ] **Step 5: Verify the public site**

Check the homepage and all six note routes over HTTP. In a browser, inspect at least one page from each source family and confirm the source-shaped headings, visible named slots, Markdown content, and learning map.
