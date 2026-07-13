# Prompt Notes Snapshot Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a six-card, source-pinned learning snapshot with refreshed existing notes, two new model/runtime notes, and two exact-text learning maps.

**Architecture:** Keep the existing dependency-free static reader in `docs/index.html`. A catalog entry maps each route slug to one Markdown payload and one PNG map; the existing GitHub Actions workflow copies those files into a Pages artifact. Add standard-library structural tests so missing cards, notes, sections, routes, sources, or images fail before deployment.

**Tech Stack:** Static HTML/CSS/JavaScript, Markdown rendered by marked, Python 3 standard-library tests, SVG rendered to PNG by headless Chrome, GitHub Actions Pages.

## Global Constraints

- Source snapshot is `asgeirtj/system_prompts_leaks@5c86715f453f0eca188451a48bf5b165831d8b29` dated 2026-07-12.
- Notes are study summaries, not official model documentation and not verbatim prompt reproductions.
- Preserve every existing note's core thesis, reusable template, comparison material, and review questions.
- Add exactly two new cards: GPT-5.6/Codex Runtime and Claude Sonnet 5/Claude Code 2.1.207.
- Every note must contain a reusable framework, review questions, and immutable source links.
- The two new map PNGs are exactly 1600×900 and use deterministic text rendering.
- Deployment remains the existing `Publish notes to GitHub Pages` workflow on `main`.

---

### Task 1: Add the site content contract

**Files:**
- Create: `tests/test_site.py`
- Read: `docs/index.html`
- Read: `.github/workflows/pages.yml`

**Interfaces:**
- Consumes: note catalog objects embedded in `docs/index.html`.
- Produces: `python3 -m unittest discover -s tests -v`, the repository-wide predeployment contract.

- [ ] **Step 1: Write the failing structural tests**

Create a standard-library `unittest` suite with this exact required slug set:

```python
EXPECTED_SLUGS = {
    "gpt-5.6-codex-runtime",
    "claude-sonnet-5-claude-code-2.1.207",
    "gpt-5.5-prompt-framework",
    "claude-fable-5-claude-code-prompt-framework",
    "grok-prompt-evolution",
    "gemini-prompt-family",
}
```

Extract catalog slugs from `docs/index.html`. For every slug, assert `notes/<slug>/README.md` and `docs/assets/mindmaps/<slug>.png` exist. Assert every note contains `## 一句话核心`, a heading matching `FrameworkNote|精华版|可复用模板`, `## 复习问题`, `## 来源索引`, the snapshot hash, and no `C:\\Users\\` path. Parse PNG IHDR bytes and assert the two new images are 1600×900. Mirror the workflow copy loop in a temporary directory and assert all six route HTML files and content payloads exist.

- [ ] **Step 2: Run the tests and confirm RED**

Run: `python3 -m unittest discover -s tests -v`

Expected: failures identify the two missing catalog slugs/notes/maps and missing snapshot sections in retained notes.

- [ ] **Step 3: Commit the failing contract**

```bash
git add tests/test_site.py
git commit -m "test: define prompt notes snapshot contract"
```

### Task 2: Refresh the catalog and Markdown notes

**Files:**
- Modify: `docs/index.html`
- Create: `notes/gpt-5.6-codex-runtime/README.md`
- Create: `notes/claude-sonnet-5-claude-code-2.1.207/README.md`
- Modify: `notes/gpt-5.5-prompt-framework/README.md`
- Modify: `notes/claude-fable-5-claude-code-prompt-framework/README.md`
- Modify: `notes/grok-prompt-evolution/README.md`
- Modify: `notes/gemini-prompt-family/README.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the six-slug contract from Task 1 and immutable GitHub blob URLs at the source snapshot.
- Produces: six complete catalog entries and six study notes sharing the required learning skeleton.

- [ ] **Step 1: Add the two catalog entries and scanability metadata**

Add `family`, `badge`, and `snapshot` fields to catalog entries. Render a compact eyebrow row above each card title, display snapshot metadata below the title on detail pages, and place new entries first. Keep `note.file` and `note.image` as the only content dependencies.

- [ ] **Step 2: Apply the restrained visual refresh**

Keep the existing warm palette and panel structure. Change the grid to `repeat(auto-fit, minmax(min(100%, 340px), 1fr))`, constrain the catalog to two columns, add `.card-topline`, `.family-tag`, `.status-badge`, `.snapshot-line`, `:focus-visible`, reduced-motion handling, and mobile behavior. Preserve the existing large mind map and Markdown article order.

- [ ] **Step 3: Write the GPT-5.6/Codex Runtime note**

Use these sections in order: snapshot boundary, one-sentence thesis, runtime layer model, model prompt, communication protocol, workspace/autonomy, skills, full runtime/tool contracts, browser/computer layers, side effects, reusable `FrameworkNote: For Every Codex Runtime Request`, comparisons, review questions, source index. The framework contains ten numbered phases from classification through verified delivery.

- [ ] **Step 4: Write the Claude Sonnet 5/Claude Code 2.1.207 note**

Use these sections in order: snapshot boundary, one-sentence thesis, two-layer model, Sonnet 5 assistant layer, Claude Code skill/runtime layer, `update-config`, `doctor`, code-review effort, dataviz/artifact design, compact/rewind/continuation, reusable `FrameworkNote: For Every Claude Code Task`, comparisons, review questions, source index. State explicitly that 2.1.207 is represented by compaction-layer additions in the snapshot, not a full replacement base prompt.

- [ ] **Step 5: Refresh retained notes without deleting core content**

Add snapshot metadata, one-sentence thesis where absent, immutable source links, and forward links between old and new notes. Replace machine-local source paths in Grok and Gemini. Keep existing reusable templates, comparisons, and review questions intact.

- [ ] **Step 6: Update repository documentation**

List all six notes, explain the source-pinned snapshot convention, and keep the Pages URL and deployment instructions.

- [ ] **Step 7: Run tests to isolate remaining work**

Run: `python3 -m unittest discover -s tests -v`

Expected: all content/catalog/source assertions pass; only the two missing map assertions fail.

- [ ] **Step 8: Commit the content refresh**

```bash
git add docs/index.html notes README.md
git commit -m "feat: refresh prompt engineering notes snapshot"
```

### Task 3: Produce exact-text learning maps

**Files:**
- Create: `docs/assets/mindmaps/source/gpt-5.6-codex-runtime.svg`
- Create: `docs/assets/mindmaps/source/claude-sonnet-5-claude-code-2.1.207.svg`
- Create: `docs/assets/mindmaps/gpt-5.6-codex-runtime.png`
- Create: `docs/assets/mindmaps/claude-sonnet-5-claude-code-2.1.207.png`

**Interfaces:**
- Consumes: the six learning modules and memory hook from each new Markdown note.
- Produces: two 1600×900 browser-safe PNGs referenced directly by the catalog.

- [ ] **Step 1: Create the GPT-5.6 SVG learning map**

Build a 1600×900 SVG titled `GPT-5.6 / Codex Runtime 学习图谱`, six numbered modules, the flow `用户请求 → 事实来源 → 指令/技能 → 能力路由 → 执行验证 → 交付`, and the memory hook `模型定行为，Runtime 给能力，证据与授权决定动作，验证决定完成。` Use system CJK fonts and avoid text smaller than 22 px.

- [ ] **Step 2: Create the Claude SVG learning map**

Build a matching SVG titled `Claude Sonnet 5 / Claude Code 2.1.207 学习图谱`, six modules covering assistant base, workspace, skills, config/doctor, review/artifacts, and compact continuity. Use the flow `用户任务 → 工作区证据 → 技能/努力级别 → 保守执行 → 上下文续作 → 验证交付` and memory hook `Sonnet 定助手底座，Claude Code 用技能扩展执行，Compact 保证长任务不断线。`

- [ ] **Step 3: Render both sources to PNG**

Run headless Chrome once per SVG with `--window-size=1600,900 --force-device-scale-factor=1 --screenshot=<absolute-png-path> file://<absolute-svg-path>` and verify Chrome exits zero.

- [ ] **Step 4: Run tests and confirm GREEN**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass with zero failures.

- [ ] **Step 5: Visually inspect the maps**

Open both PNGs at original resolution and confirm every label is legible, no text clips, the flow is visually dominant, and each memory hook is present exactly once.

- [ ] **Step 6: Commit the maps**

```bash
git add docs/assets/mindmaps
git commit -m "feat: add runtime learning maps"
```

### Task 4: Verify, publish, and inspect the live Pages site

**Files:**
- Verify: all tracked changes
- Publish: `main`

**Interfaces:**
- Consumes: the green repository state from Tasks 1–3.
- Produces: the deployed site at `https://hufaei.github.io/my-skills/`.

- [ ] **Step 1: Build the Pages artifact locally**

Run the exact shell body from `.github/workflows/pages.yml` and assert `_site/index.html`, six `_site/content/*.md` files, six `_site/notes/*/index.html` routes, and both new map PNGs exist.

- [ ] **Step 2: Serve and inspect locally**

Serve `_site` on localhost. Inspect the home page, both new detail pages, and one retained page at 1440×900 and 390×844. Confirm six cards, badges, snapshot line, readable maps, Markdown sections, horizontal table/code overflow, and working home navigation.

- [ ] **Step 3: Run the completion gate**

```bash
python3 -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

Expected: tests pass, diff check exits zero, and status contains no uncommitted files.

- [ ] **Step 4: Push and monitor Pages**

Run `git push origin main`, identify the triggered `Publish notes to GitHub Pages` run, and wait until its conclusion is `success`.

- [ ] **Step 5: Verify the deployed snapshot**

Request the public home URL and both new route URLs with cache-busting query strings. Assert HTTP 200, verify the live HTML contains both new slugs, then inspect the live home and new detail pages visually.
