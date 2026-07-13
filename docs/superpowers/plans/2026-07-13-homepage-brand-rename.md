# Homepage Brand Rename Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use test-driven-development to implement each task and verification-before-completion before claiming success.

**Goal:** Rename the reader-facing site brand to `AI Prompt Atlas` and replace the homepage subtitle without changing routes, cards, notes, maps, or deployment behavior.

**Architecture:** Keep the current single-file static reader intact. Add one regression test that treats the six brand surfaces and the homepage subtitle as a stable contract, then make the smallest copy-only update in `docs/index.html`.

**Tech Stack:** Static HTML/CSS/JavaScript, Python `unittest`, GitHub Pages Actions

---

### Task 1: Add the brand consistency contract

**Files:**
- Modify: `tests/test_site.py`
- Test: `tests/test_site.py`

**Step 1: Write the failing test**

Add this test to `SiteContractTests`:

```python
def test_site_brand_is_consistent_across_reader_surfaces(self):
    html = INDEX.read_text(encoding="utf-8")
    self.assertEqual(html.count("AI Prompt Atlas"), 6)
    self.assertIn("模型提示词、Agent Runtime 与 Skills 学习图谱", html)
    self.assertNotIn("Prompt Engineering Notes", html)
```

**Step 2: Run the targeted test to verify it fails**

Run: `python3 -m unittest tests.test_site.SiteContractTests.test_site_brand_is_consistent_across_reader_surfaces -v`

Expected: FAIL because `AI Prompt Atlas` is not yet present.

**Step 3: Implement the minimal page copy change**

In `docs/index.html`:

- Replace the six occurrences of `Prompt Engineering Notes` with `AI Prompt Atlas`.
- Replace the homepage description with `模型提示词、Agent Runtime 与 Skills 学习图谱`.
- Do not change links, slugs, catalog entries, styles, note content, or asset paths.

**Step 4: Run the targeted test to verify it passes**

Run: `python3 -m unittest tests.test_site.SiteContractTests.test_site_brand_is_consistent_across_reader_surfaces -v`

Expected: PASS.

**Step 5: Run the complete test suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: 8 tests pass.

**Step 6: Commit**

```bash
git add tests/test_site.py docs/index.html
git commit -m "feat: rename site to AI Prompt Atlas"
```

### Task 2: Build, publish, and verify GitHub Pages

**Files:**
- Verify: `docs/index.html`
- Verify: `.github/workflows/pages.yml`

**Step 1: Reproduce the Pages build locally**

Build `_site` with the same copy rules as `.github/workflows/pages.yml`, then verify all six route files, Markdown payloads, and mind maps exist.

Expected: six detail routes, six Markdown payloads, and six mind maps.

**Step 2: Perform fresh pre-push verification**

Run the full tests again, run `git diff --check origin/main...HEAD`, and confirm the working tree is clean.

Expected: 8 tests pass, no whitespace errors, clean worktree.

**Step 3: Push the approved main branch change**

Run: `git push origin main`

Expected: the new implementation commit is pushed.

**Step 4: Monitor the Pages workflow**

Find the Pages run triggered by the new commit and watch it to completion.

Expected: workflow conclusion `success`.

**Step 5: Verify the deployed reader**

Check `https://hufaei.github.io/my-skills/` and one detail route.

Expected:

- Homepage returns HTTP 200.
- Homepage nav, H1, and browser title show `AI Prompt Atlas`.
- Homepage subtitle shows `模型提示词、Agent Runtime 与 Skills 学习图谱`.
- Detail page returns HTTP 200 and its title ends with `| AI Prompt Atlas`.
- Deployed reader HTML no longer contains `Prompt Engineering Notes`.
