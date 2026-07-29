# Seeing the Unseen — Project Rules

Website chia sẻ kiến thức (bias, cognitive behavior, psychology): mỗi concept là một "stuff" — đốm lửa trên bản đồ hang động Plato. Stack: Astro 5 static + content-as-git. Chi tiết: `docs/build-plan.md`.

## Cấu trúc

- `content/stuff/` — 1 file .md = 1 card. **Filename = slug = khoá tham chiếu.** Không đổi tên file tùy tiện (gãy links).
- `content/approaches/` — bài case study/ứng dụng.
- `scripts/content-pipeline/` — pipeline 3 vai (researcher/writer/verifier), backlog, prompts.
- `src/` — Astro. `src/components/map/` — map engine (canvas 2D) + stuff overlay (Phase 2). `src/lib/progress.ts` — fog-of-war progression (localStorage). `maps/` — README mô tả map pipeline (Phase 2). `docs/` — plan + guides.

## Phase 2 — Map & fog-of-war

- Map đọc dữ liệu từ `public/map-data.json` (sinh bởi `npm run mapdata` từ `content/stuff`) — **không đọc content trực tiếp**.
- 4 map + The Sun, khớp `level` 1–4 trong frontmatter. Canvas 2D tự render, không Tiled/Kaplay.
- Tiến trình khám phá (fog-of-war) qua `src/lib/progress.ts` — contract: `getLit/markLit/isLit/litCountByLevel`.

## Schema stuff card (bắt buộc)

```yaml
title: string          # bắt buộc
front: string          # câu hỏi tiếng Việt — bắt buộc
back: string           # định nghĩa 1-2 câu — bắt buộc
level: 1-4             # 1=Imagining, 2=Belief, 3=Thinking, 4=Knowledge
categories: [slug]     # bias | mental-models | fallacy | memory | perception | theory | heuristic | social
links: [slug]          # CHỈ slug tồn tại trong content/stuff/ — không dùng title
refs: [url]            # nguồn tham khảo — bắt buộc có ít nhất 1
strategy: string       # optional — 1 câu actionable
published: true
```

Body: 300-500 từ tự viết. Legacy cards (migrate từ Jekyll) đang ngắn — enrich dần qua pipeline.

## Quy tắc bất biến

1. **Không scrape/copy nội dung** từ nguồn có bản quyền (Coglode, DecisionLab, PsychologyToday). Nguồn chỉ nằm trong `refs`; body phải tự viết.
2. **`npm run verify` phải PASS trước mọi commit** chạm vào `content/`. CI sẽ fail nếu không.
3. `links` dùng slug, không dùng title. Verifier bắt link gãy.
4. Giọng văn: `front` tiếng Việt gợi tò mò (mẫu: `content/stuff/anchoring.md`); `back` ngắn gọn; không học thuật khô.
5. Icon không random — derive theo category trong `src/lib/icons.ts`.
6. Không commit thẳng vào `master`; làm việc trên branch, mở PR.

## Content pipeline (phương án B — model-tiered)

- Researcher = subagent `researcher` (Haiku): refs + level/categories/links.
- Writer = subagent `writer` (Sonnet): viết card.
- Verifier = `npm run verify` (code, $0) — chạy trước mọi LLM judge.
- Commands: `/new-card <concept>`, `/batch-cards <n>` (hard cap 10/run).
- Human review qua PR — pipeline không tự merge.

## Lệnh thường dùng

- `npm run dev` / `npm run build` — dev / build (build tự chạy pagefind).
- `npm run verify` — validate schema + link integrity toàn bộ content.
- `npm run graph` — sinh `public/graph.json` từ frontmatter.
