# Homepage Brand Rename Design

## Goal

Rename the site-facing brand from `Prompt Engineering Notes` to `AI Prompt Atlas` so the homepage accurately covers model prompts, agent runtimes, skills, and learning maps.

## Approved copy

- Site name: `AI Prompt Atlas`
- Homepage subtitle: `模型提示词、Agent Runtime 与 Skills 学习图谱`

## Scope

Update every site-brand surface in `docs/index.html`:

- the static HTML `<title>` fallback;
- the sticky navigation brand;
- the homepage `<h1>`;
- the homepage browser title;
- detail-page browser-title suffixes;
- not-found-page browser-title suffixes.

The existing snapshot kicker remains unchanged. The subtitle replaces the current longer homepage description.

## Non-goals

- Do not change `https://hufaei.github.io/my-skills/`.
- Do not rename note routes, folders, Markdown files, map assets, card titles, or note headings.
- Do not change the six-note catalog, visual layout, or Pages workflow.

## Verification and deployment

Add a regression test that asserts the new brand appears on all required surfaces and the old brand is absent from the reader HTML. Run the full site contract suite and local Pages build, then push `main`, wait for the Pages workflow, and verify the live homepage and one detail-page browser title.
