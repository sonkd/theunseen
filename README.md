# Seeing the Unseen 🔥

Every piece of knowledge is a flame in Plato's cave. A knowledge-sharing site about cognitive biases, mental models, and psychology — structured as a journey through 4 maps (Imagining → Belief → Thinking → Knowledge), rendered as flip cards linked into a knowledge graph.

## Quickstart

```bash
npm install
npm run dev        # http://localhost:4321
npm run verify     # validate content schema + link integrity
npm run build      # static build → dist/ (+ pagefind index)
```

## Docs

- `docs/build-plan.md` — kiến trúc, roadmap, Definition of Done
- `docs/agent-workflow-guide.md` — content pipeline 3-agent (researcher/writer/verifier)
- `CLAUDE.md` — quy tắc dự án cho AI agents

## Deploy

**Netlify là platform production duy nhất.** Cấu hình nằm trong `netlify.toml`
(ghi đè mọi thiết lập trong Netlify UI): build `npm run build`, publish `dist`,
Node 22, `NPM_FLAGS=--include=dev` (pagefind ở devDependencies, chạy ở `postbuild`).

- `public/_headers` — cache rules, Netlify đọc từ publish dir
- `public/_redirects` — URL cũ thời Jekyll → `/library/`

Docker (`docker compose up -d --build`) chỉ dùng để **preview local** và cho
job `daily-content`; không phải đường deploy production.
