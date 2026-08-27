# Graph pipeline

How `content/stuff` frontmatter becomes the 3D graph rendered at `/graph/`.
Implementation status and design rationale for the renderer itself live in
`docs/graph-3d-plan.md` — this doc is just the data pipeline.

## Pipeline

```
content/stuff/*.md (frontmatter: links)
        │
        ▼
scripts/build-graph.mjs        — extract nodes/edges, drop self-loops,
        │                         dedupe edges, count dangling links
        ▼
scripts/lib/graph-metrics.mjs  — degree, connected components,
        │                         Louvain community detection (seeded)
        ▼
scripts/lib/bake-layout.mjs    — Fibonacci-sphere init (seeded shuffle)
        │                       + d3-force-3d simulation, run headless
        │                       for 600 ticks, recentered or rescaled
        ▼
public/graph/graph.json        — { nodes: [{id,title,url,level,categories,
                                    degree,componentId,communityId,x,y,z}],
                                    edges: [{source,target}] }
```

Run it directly with `npm run graph` (alias for `npm run graph:build`, i.e.
`node scripts/build-graph.mjs`).

## Why baked, not live

The layout is computed once at build time and the `x/y/z` coordinates are
written straight into `graph.json`, rounded to 2 decimals. The browser never
runs the force simulation — `/graph/`'s client script sets
`cooldownTicks(0)`/`warmupTicks(0)` and just renders the baked positions.

This means:
- First paint is a complete, stable sphere — no "everything flies in from
  the center" animation.
- The layout is **deterministic**: running `npm run graph` twice on the same
  content produces a byte-identical `graph.json` (verified — no
  unseeded `Math.random()` or `Date.now()` anywhere in the pipeline).
- Node positions stay the same across visits, so a reader builds spatial
  memory of where a concept lives in the graph.

`src/lib/graph-forces.mjs` holds the force parameters (`forceLink`,
`forceManyBody`, `forceRadial`, `forceCenter`) as a function shared between
the Node bake script and the browser, so if the client ever needs to
re-heat the simulation (e.g. after a user drags a node), it uses the exact
same physics as the bake.

## Extraction rules (`scripts/build-graph.mjs`)

- A node is created for every published `content/stuff/*.md` file
  (`published: false` is skipped).
- An edge is created for every `links: [slug, ...]` entry that points at
  another *existing* node. Self-loops are dropped. Edges are deduped
  (undirected — `a→b` and `b→a` collapse to one).
- A link pointing at a slug that doesn't exist counts as **dangling** and
  is dropped by default; pass `--keep-ghosts` to keep it as a node with
  `ghost: true` instead.
- A node with degree 0 (no links in or out) is kept as an **orphan** — it
  still renders, just unconnected.

## Regenerating

- `npm run build` regenerates it automatically via `prebuild`.
- `npm run dev` regenerates it once on server start and again on every
  change under `content/stuff/**`, via the `graph-dev-integration.mjs`
  Astro integration (`astro:config:setup` / `astro:server:setup` hooks in
  `astro.config.mjs`).
- Never hand-edit `public/graph/graph.json` — it's generated output.
