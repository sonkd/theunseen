# Deploy

## Production: Netlify

**Netlify is the only production platform.** `netlify.toml` overrides any
setting configured in the Netlify UI:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "22"
  NPM_FLAGS = "--include=dev"   # Pagefind is a devDependency, needed at postbuild
```

`[context.production]`, `[context.deploy-preview]`, and `[context.branch-deploy]`
all run the same `npm run build` — no environment-specific build behavior.

`npm run build` is `prebuild` (mapdata + graph bake) → `astro build` →
`postbuild` (Pagefind indexing; the build **fails** if
`dist/pagefind/pagefind-entry.json` ends up missing or empty).

- `public/_headers` — cache rules, read by Netlify straight from the publish dir.
- `public/_redirects` — old Jekyll-era URLs → `/library/`.

No environment variables are required (see `.env.example`).

## CI

`.github/workflows/ci.yml` runs on push to `new`/`master`/`dev` and on every
PR:

```
npm ci
npm run verify   # content schema + link integrity
npm run graph    # regenerate public/graph/graph.json
npm run mapdata  # regenerate public/map-data.json
npm run build
```

This is a correctness check, not a deploy step — Netlify builds
independently from its own trigger on the connected branch.

## Docker — local preview only

`docker compose up -d --build` builds and runs the site locally via
`Dockerfile`/`docker-compose.yml`. This is **not** the production deploy
path — it exists for:

- Local preview without running `npm run dev` directly.
- The `daily-content` scheduled job (see `docs/content-authoring.md`),
  which needs a consistent environment to write/verify/build content
  before committing to the `new` branch.

There's also `.github/workflows/docker.yml` — manual-only
(`workflow_dispatch`), used to confirm the Dockerfile still builds. It does
not run automatically and does not deploy anywhere.
