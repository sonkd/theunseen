# Roadmap

The authoritative phased roadmap (with Definition-of-Done per phase) is
**§2.6 "Roadmap theo phase" in `docs/build-plan.md`** — this file is just a
short, current-state pointer into it so it doesn't need duplicating (and
drifting out of sync) here.

## Where things stand

- **Phase 0 — Foundation**: done (per `build-plan.md`).
- **Phase 0.5 — Enrich legacy content**: ongoing, in parallel with later
  phases — see `docs/content-authoring.md` / `/enrich-cards`.
- **Phase 2 — Card & Library**: shipped (`src/pages/library.astro`,
  `src/pages/stuff/[slug].astro`).
- **Phase 2 — Map & fog-of-war**: shipped (`src/components/map/MapCanvas.astro`,
  `src/lib/progress.ts`).
- **Graph view**: originally listed as backlog in `build-plan.md` §1.3; now
  has its own dedicated spec at `docs/graph-3d-plan.md` (3D, `/graph/`),
  implemented through that doc's P0–P2 phases (data pipeline, renderer,
  hover/click interaction) plus the essential P3/P4 items (idle pause,
  reduced-motion, no-WebGL fallback). See that doc for exactly what's done
  vs. explicitly deferred.
- **Phase 3 — Retention & measurement**: not started. No analytics/event
  tracking exists in the codebase as of this writing.

For anything not covered above (spaced repetition, user accounts, community
contributions via PR), see `build-plan.md` §2.6 "Phase sau (backlog)" —
these are explicitly backlog, not committed work.
