[![Netlify Status](https://api.netlify.com/api/v1/badges/28704be5-e764-4674-ba56-032d388220dc/deploy-status)](https://app.netlify.com/projects/theunseen/deploys)

# Seeing the Unseen 🔥

Every piece of knowledge is a flame in Plato's cave. A knowledge-sharing site about cognitive biases, mental models, and psychology — structured as a journey through 4 maps (Imagining → Belief → Thinking → Knowledge), rendered as flip cards linked into a knowledge graph.

## Stack

Astro 5 (static output) + MDX, no UI framework — pages ship vanilla `<script>` (dynamic `import()` where a page needs a heavy client-only lib, e.g. `/graph/`'s 3D renderer). Content lives as Markdown files under `content/`, typed via Astro Content Collections (`src/content.config.ts`, Zod schema). Search is a plain GET form that hands the query to `/library?q=…`, where the existing client-side filter (category + level + q) narrows the list — no separate search index.

## Quickstart

```bash
npm install
npm run dev        # http://localhost:4321
npm run verify      # validate content schema + link integrity (content/stuff)
npm run build       # static build → dist/ (mapdata + graph bake + astro build)
```

No environment variables are required to run this project — see `.env.example`.

## Common commands

| Command | What it does |
|---|---|
| `npm run dev` | Astro dev server, port 4321. Also rebuilds `public/graph/graph.json` on start and on any `content/stuff/**` change (see `scripts/graph-dev-integration.mjs`). |
| `npm run build` | `prebuild` (mapdata + graph bake) → `astro build`. |
| `npm run preview` | Serve the built `dist/` locally. |
| `npm run verify` | Validates every `content/stuff/*.md`: required frontmatter fields, `level` in 1–4, no broken `links`, `refs` must be URLs. Warns (non-fatal) on short bodies / missing `refs` / missing `categories`. |
| `npm run graph` / `npm run graph:build` | Same command (`graph` is an alias) — extracts nodes/edges from `content/stuff` frontmatter, computes degree/community/component metrics, bakes a deterministic 3D layout, writes `public/graph/graph.json`. |
| `npm run mapdata` | Generates `public/map-data.json` from `content/stuff` for the 2D map view (`src/components/map/MapCanvas.astro`). |
| `npm run backlog` | Syncs `scripts/content-pipeline/backlog.csv` against what actually exists in `content/stuff/` (todo / needs-enrich / done). |
| `npm run test:progress` | Runs `scripts/test-progress.mjs` (tests for the fog-of-war/localStorage progress logic in `src/lib/progress.ts`). |

Scripts referenced elsewhere (docs, chat history) that do **not** exist in `package.json` — do not assume these work:
- `npm run graph:pipeline`, `npm run content:new`, `npm run test`, `npm run lint`, `npm run typecheck` — none of these are defined. There is no test runner, linter, or type-checker wired up beyond `astro check` (not installed) and the scripts above.

## Content model

Two Astro Content Collections, defined in `src/content.config.ts`:

**`stuff`** — loads `content/stuff/**/*.md`. **Filename = slug = the key every `links` reference uses.**

| Field | Type (Zod) | Required | Notes |
|---|---|---|---|
| `title` | `string` | yes | |
| `front` | `string` (min 1) | yes | Vietnamese hook question |
| `back` | `string` (min 1) | yes | 1–2 sentence definition |
| `level` | `number` int 1–4 | no (default `2`) | 1=Imagining, 2=Belief, 3=Thinking, 4=Knowledge |
| `icon` | `string` | no | |
| `map_position` | `{ x: number, y: number }` | no | |
| `categories` | `string[]` | no (default `[]`) | e.g. `bias`, `mental-models`, `fallacy`, `memory`, `perception`, `theory`, `heuristic`, `social` |
| `tags` | `string[]` | no (default `[]`) | |
| `links` | `string[]` | no (default `[]`) | **Slugs only**, not titles — `npm run verify` fails on broken links |
| `refs` | `string[]` | no (default `[]`) | Must be `http(s)://` URLs |
| `approaches` | `{ title: string, url: string }[]` | no (default `[]`) | |
| `strategy` | `string` | no | Optional actionable one-liner |
| `conundrum` | `string` | no | |
| `published` | `boolean` | no (default `true`) | |
| `image` | `string` (nullish) | no | Internal path only, e.g. `/assets/stuff/<slug>.png` |

**`approaches`** — loads `content/approaches/**/*.md` (empty directory as of this writing — no case-study posts published yet).

| Field | Type (Zod) | Required |
|---|---|---|
| `title` | `string` | yes |
| `stuff` | `string[]` (default `[]`) | no |
| `published` | `boolean` (default `true`) | no |

`npm run verify` enforces a stricter subset of this at build time via plain JS (not Zod) against `content/stuff` only — see `scripts/content-pipeline/verify.mjs`.

## Directory structure

```
content/
  stuff/            230 markdown cards — 1 file = 1 concept, filename = slug
  approaches/        (empty) case-study posts, keyed by `stuff` slugs
docs/                architecture notes, specs, plans (see below)
public/
  graph/graph.json   generated — do not hand-edit, run `npm run graph`
  map-data.json       generated — do not hand-edit, run `npm run mapdata`
  _headers, _redirects  Netlify-specific (cache rules; legacy Jekyll URL redirects)
scripts/
  build-graph.mjs           entry point for `npm run graph`
  build-map-data.mjs        entry point for `npm run mapdata`
  graph-dev-integration.mjs Astro integration: rebuilds graph.json in dev mode
  lib/                      graph-metrics.mjs, bake-layout.mjs, seeded-random.mjs
  content-pipeline/         verify.mjs, sync-backlog.mjs, researcher/writer prompts
src/
  content.config.ts   Zod schemas for the two content collections
  components/          FlipCard.astro, StuffThumb.astro, map/MapCanvas.astro, map/StuffOverlay.astro
  layouts/Base.astro
  lib/                 icons.ts, progress.ts, graph-forces.mjs, map/palette.ts, map/path.ts
  pages/
    index.astro         2D map (Phase 2)
    library.astro        list + search
    about.astro
    graph.astro          3D knowledge-graph view (see docs/graph-pipeline.md)
    stuff/[slug].astro    per-card static page
    stuff-data/[slug].json.ts  JSON endpoint the popup overlay fetches
.claude/               skills + agents used by the content pipeline commands
```

## Docs

- `docs/build-plan.md` — original architecture review, tech-stack rationale, phased roadmap (Phase 0–3)
- `docs/graph-3d-plan.md` — task-by-task spec for the 3D graph view (`/graph/`) and its implementation status
- `docs/graph-pipeline.md` — how `content/stuff` frontmatter becomes `public/graph/graph.json`
- `docs/content-authoring.md` — how to write/verify a stuff card, and the pipeline commands that automate it
- `docs/deploy.md` — Netlify production config, CI, Docker (local-preview only)
- `docs/roadmap.md` — current phase status (pointer into `build-plan.md`, kept short)
- `docs/adr/` — architecture decision records (empty so far; template inside)
- `docs/agent-workflow-guide.md` — content pipeline 3-agent workflow (researcher/writer/verifier)
- `CLAUDE.md` — project rules for AI coding agents

## Deploy

**Netlify is the only production platform.** Config lives in `netlify.toml`
(overrides any setting in the Netlify UI): build `npm run build`, publish `dist`,
Node 22, `NPM_FLAGS=--include=dev` (`gray-matter` is a devDependency, needed by `scripts/` during `prebuild`).

- `public/_headers` — cache rules, read by Netlify from the publish dir
- `public/_redirects` — old Jekyll-era URLs → `/library/`

Docker (`docker compose up -d --build`) is **local preview only**, and what the
`daily-content` job uses; it is not the production deploy path. See `docs/deploy.md` for details.
