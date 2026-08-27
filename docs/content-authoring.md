# Content authoring

How to write a stuff card, by hand or through the content pipeline.

## Schema

Type-checked by Astro Content Collections at `src/content.config.ts` (Zod).
Full field-by-field table is in the root `README.md` under **Content model** —
this doc covers the writing conventions instead.

- **Filename = slug = the key every other card's `links` uses to reference
  it.** Don't rename a published file — it breaks every card linking to it.
- `front`: a Vietnamese hook question. See `content/stuff/anchoring.md` for
  the target tone — curious, not academic.
- `back`: 1–2 sentence definition, kept short (it's the flip-card back face).
- `links`: **slugs, not titles.** `npm run verify` fails the build on any
  link pointing at a slug that doesn't exist in `content/stuff/`.
- `refs`: at least one, must be an `http(s)://` URL. Sources go here only —
  see the copyright rule below.
- `image` (optional): must be an internal path, `/assets/stuff/<slug>.png`,
  with the file placed in `public/assets/stuff/`. Never a URL to an external
  site (e.g. notion.so). No `image` field → `StuffThumb.astro` renders a
  fallback glyph from `src/lib/icons.ts`, colored by `level` via
  `src/lib/map/palette.ts`. Icons are derived from `categories`, never
  picked at random.
- Body: 300–500 words, written by hand. Legacy cards migrated from the old
  Jekyll site are often short — `npm run verify` warns (doesn't fail) on
  bodies under 100 words; enriching these is ongoing work (`/enrich-cards`).

## Invariant rules (from `CLAUDE.md`)

1. **No scraping/copying** from copyrighted sources (Coglode, DecisionLab,
   PsychologyToday). Sources belong in `refs` only — the body must be
   written from scratch.
2. **`npm run verify` must PASS** before any commit touching `content/`. CI
   runs this too and fails the build otherwise.
3. `links` uses slugs, never titles — the verifier catches broken links.
4. Don't commit straight to `master`; work on a branch, open a PR. The one
   exception is the scheduled `daily-content` job, which may commit
   directly to the `new` branch after `verify + graph + mapdata + build`
   all pass — it still never pushes/merges to `master`.

## Commands

```bash
npm run verify    # schema + link integrity check — run this before every content commit
npm run graph     # regenerate public/graph/graph.json after adding/editing links
npm run mapdata   # regenerate public/map-data.json (2D map view reads this, not content/ directly)
npm run backlog   # sync scripts/content-pipeline/backlog.csv against content/stuff/ (todo / needs-enrich / done)
```

## Pipeline commands (Claude Code slash commands, see `.claude/skills/`)

- `/new-card <concept>` — full researcher → writer → verify pipeline for
  one concept. Researcher is a Haiku subagent (refs + level/categories/links),
  writer is a Sonnet subagent (writes the card), verifier is
  `npm run verify` (runs before any LLM judge, since it's free and
  deterministic).
- `/batch-cards <n>` — same pipeline for N concepts pulled from the backlog
  (hard cap 10 per run).
- `/enrich-cards <n>` — expand legacy short-body cards to 300–500 words,
  optionally filtered by category.
- `/daily-content` — the scheduled job: syncs the backlog, writes/enriches
  15 cards, regenerates graph + map data, commits to `new` (see rule 4
  above).

Run `npm run backlog` before and after a batch to avoid duplicate work.
