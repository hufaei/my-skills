# GitHub Pages Route Rename Design

## Goal

Change the project Pages route from `/my-skills/` to `/ai-prompt-atlas/`, matching the approved `AI Prompt Atlas` site name.

## Chosen approach

Rename the existing GitHub repository from `hufaei/my-skills` to `hufaei/ai-prompt-atlas`. For a GitHub Pages project site, the repository name owns the first URL path segment, so this produces `https://hufaei.github.io/ai-prompt-atlas/` while preserving repository history, stars, settings, and the existing Pages workflow.

The alternatives are rejected:

- A client-side redirect would leave the official Pages route unchanged.
- A new repository would duplicate history and require migrating settings and Pages configuration.
- A custom domain is outside the requested route-only change and would require DNS ownership.

## Repository updates

- Update the public Pages URL in `README.md`.
- Update the repository installation link in `README.md`.
- Keep local install script names unchanged because they are executable filenames, not public routes.
- Keep the visible site name `AI Prompt Atlas` and the existing note/card routes unchanged beneath the new project prefix.

## Deployment flow

1. Confirm `hufaei/ai-prompt-atlas` is available and the current Pages site uses GitHub Actions.
2. Verify the built reader under a local `/ai-prompt-atlas/` prefix.
3. Rename the GitHub repository and update the local `origin` URL.
4. Trigger the existing Pages workflow in the renamed repository.
5. Verify the new homepage and one detail route over HTTP and in a browser.
6. Record the old route response without depending on it as the canonical URL.

## Success criteria

- The canonical repository is `https://github.com/hufaei/ai-prompt-atlas`.
- The canonical Pages homepage is `https://hufaei.github.io/ai-prompt-atlas/`.
- The homepage and a note detail route both return HTTP 200.
- The browser renders six cards on the homepage and loads Markdown plus the learning map on the detail page.
- `README.md` contains no canonical `hufaei/my-skills` or `/my-skills/` links.
