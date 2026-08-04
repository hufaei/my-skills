# Writing principles

## Source-backed principles

Apply these principles without turning them into claims about a repository:

- Prefer a small, fresh documentation set over a large stale one. Update docs
  with the code change and remove known-dead documentation.
- Write for the reader's immediate need. Separate task instructions, factual
  reference, and conceptual explanation when mixing them would bury the answer.
- State facts directly and plainly. Put prerequisites before instructions, lead
  with the simplest successful path, and use consistent terminology.
- Keep reference material authoritative, neutral, structured like the system it
  describes, and easy to consult rather than read end to end.
- Avoid duplicated truth. Link to the canonical contract, decision, or detailed
  explanation instead of maintaining parallel copies.
- Use one H1, descriptive headings, fenced code blocks with language labels,
  informative link text, and tables only for genuinely tabular comparisons.

These principles come from:

- [Google documentation best practices](https://google.github.io/styleguide/docguide/best_practices.html)
- [Google Markdown style guide](https://google.github.io/styleguide/docguide/style.html)
- [Diátaxis documentation system](https://diataxis.fr/)
- [Diátaxis reference guidance](https://diataxis.fr/reference/)

## JL authoring policy

Use the source-backed principles through these repository-writing rules:

1. Identify the audience and the question the document must answer.
2. Find a repository artifact for every project-specific factual claim.
3. Match the existing project's terminology and formatting before introducing a
   new convention.
4. Prefer concrete nouns and active verbs. Define unavoidable acronyms on first
   use.
5. Put commands in copyable code blocks and identify the directory or
   prerequisites when execution context matters.
6. Use examples that are valid, safe, minimal, and consistent with the current
   contract. Never place real credentials or production identifiers in examples.
7. Describe limitations and failure behavior next to the capability they
   constrain.
8. Use diagrams only when relationships or flows are materially clearer than in
   prose. Label nodes and relationships, declare scope, and keep diagram source
   reviewable when the repository supports diagrams as code.
9. Do not add badges, screenshots, tables of contents, boilerplate sections, or
   speculative roadmaps unless they improve this repository's actual document.
10. If only wording changes, preserve semantics. If semantics must change,
    identify the supporting code, contract, or accepted decision.

## Document quality check

A document is ready when a reader can identify:

- what the document governs and who it is for;
- where its factual claims come from;
- what action or understanding it enables;
- which linked document owns deeper detail;
- what remains unknown, proposed, deprecated, or unverified.
