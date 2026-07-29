# Content pipeline — Phương án B (3 vai, model-tiered)

Researcher (Haiku) → Writer (Sonnet) → Verifier (code, $0) → PR review (human).

- `backlog.csv` — hàng đợi concept. Cột status: todo → drafted → published.
- `prompts/` — prompt template cho 2 vai LLM.
- `verify.mjs` — verifier deterministic: schema, link integrity, word count. Chạy: `npm run verify`.

Quy trình chi tiết + tự động hóa: xem `docs/agent-workflow-guide.md`.
Nguyên tắc chi phí: model rẻ cho extraction, model mạnh chỉ để viết, verify bằng code trước khi bất kỳ LLM judge nào, hard cap 10 card/run.
