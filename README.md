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

```bash
docker compose up -d --build   # web (nginx) + umami analytics
```
