# GitHub Pages Route Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the project Pages site from `/my-skills/` to `/ai-prompt-atlas/` by renaming the existing GitHub repository.

**Architecture:** Keep the static reader and note routes unchanged. Update repository-owned URLs in the README, verify relative routing under the new prefix, rename the repository through GitHub, update the local remote, and redeploy with the existing Pages workflow.

**Tech Stack:** Static HTML/JavaScript, Python `unittest`, Git, GitHub CLI, GitHub Pages Actions

## Global Constraints

- Canonical repository: `https://github.com/hufaei/ai-prompt-atlas`.
- Canonical Pages URL: `https://hufaei.github.io/ai-prompt-atlas/`.
- Preserve repository history, stars, settings, the six-note catalog, and nested note slugs.
- Keep local install script filenames unchanged.

---

### Task 1: Update repository-owned public URLs

**Files:**
- Modify: `README.md`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: the approved repository and Pages URLs.
- Produces: README links that point only to the renamed repository and new Pages route.

- [ ] **Step 1: Write the failing test**

```python
def test_readme_uses_the_canonical_repository_and_pages_route(self):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    self.assertIn("https://hufaei.github.io/ai-prompt-atlas/", readme)
    self.assertIn("https://github.com/hufaei/ai-prompt-atlas/", readme)
    self.assertNotIn("https://hufaei.github.io/my-skills/", readme)
    self.assertNotIn("https://github.com/hufaei/my-skills/", readme)
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run: `python3 -m unittest tests.test_site.SiteContractTests.test_readme_uses_the_canonical_repository_and_pages_route -v`

Expected: FAIL because the new Pages URL is absent.

- [ ] **Step 3: Replace the two canonical links in README**

Replace:

```text
https://hufaei.github.io/my-skills/
https://github.com/hufaei/my-skills/tree/main/skills/prune-merged-worktrees
```

with:

```text
https://hufaei.github.io/ai-prompt-atlas/
https://github.com/hufaei/ai-prompt-atlas/tree/main/skills/prune-merged-worktrees
```

- [ ] **Step 4: Run the targeted and full tests**

Run: `python3 -m unittest tests.test_site.SiteContractTests.test_readme_uses_the_canonical_repository_and_pages_route -v`

Run: `python3 -m unittest discover -s tests -v`

Expected: the targeted test and all 9 tests pass.

- [ ] **Step 5: Commit**

```bash
git add README.md tests/test_site.py
git commit -m "docs: update AI Prompt Atlas routes"
```

### Task 2: Verify and publish the new project route

**Files:**
- Verify: `docs/index.html`
- Verify: `.github/workflows/pages.yml`

**Interfaces:**
- Consumes: the static Pages artifact and GitHub repository settings.
- Produces: a deployed reader at `https://hufaei.github.io/ai-prompt-atlas/`.

- [ ] **Step 1: Build and test under the new local prefix**

Reproduce `.github/workflows/pages.yml`, place the artifact under a local `ai-prompt-atlas/` directory, and open both `/ai-prompt-atlas/` and `/ai-prompt-atlas/notes/gpt-5.6-codex-runtime/`.

Expected: six cards render; the detail page loads Markdown and a 1600-pixel-wide learning map.

- [ ] **Step 2: Push the README and test commit**

Run: `git push origin main`

Expected: the current branch is synchronized before the repository rename.

- [ ] **Step 3: Rename the repository and update origin**

```bash
gh repo rename ai-prompt-atlas --repo hufaei/my-skills --yes
git remote set-url origin https://github.com/hufaei/ai-prompt-atlas.git
```

Expected: `gh repo view hufaei/ai-prompt-atlas` resolves and `origin` uses the new URL.

- [ ] **Step 4: Trigger and monitor Pages**

Run: `gh workflow run pages.yml --repo hufaei/ai-prompt-atlas --ref main`

Watch the new run through completion.

Expected: build and deploy jobs conclude successfully.

- [ ] **Step 5: Verify the public route**

Check the homepage and `notes/gpt-5.6-codex-runtime/` route with HTTP and a real browser.

Expected: both return 200; the homepage renders six cards; the detail page loads its Markdown and learning map; browser titles retain `AI Prompt Atlas`.
