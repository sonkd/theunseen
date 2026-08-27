# Seeing the Unseen — Project Instructions (Claude Code)

Website chia sẻ tri thức (cognitive bias, mental models, psychology): mỗi concept là một **"stuff"** — đốm lửa trên bản đồ hang động Plato. Người đọc "thắp sáng" thẻ khi khám phá (fog-of-war). Stack: **Astro 5 static + content-as-git**. Bối cảnh sâu hơn: `docs/build-plan.md`, `docs/roadmap.md`.

> Đọc file này trước khi chạm code. Quy tắc ở đây **ghi đè** thói quen mặc định.

---

## 1. Quickstart

```bash
nvm use                 # Node 22 (.nvmrc)
npm ci
npm run dev             # astro dev → http://localhost:4321
npm run verify          # BẮT BUỘC pass trước khi commit content/
npm run build           # prebuild: mapdata + graph:build → build → postbuild: pagefind
```

Tất cả script (nguồn: `package.json`):

| Lệnh | Việc |
|---|---|
| `npm run dev` | Astro dev server |
| `npm run build` | `mapdata + graph` → `astro build` → `pagefind` (fail nếu thiếu index) |
| `npm run verify` | Validate schema + link integrity toàn bộ `content/` (`scripts/content-pipeline/verify.mjs`) |
| `npm run graph` | Sinh `public/graph.json` từ frontmatter |
| `npm run mapdata` | Sinh `public/map-data.json` cho map engine |
| `npm run backlog` | Sync `scripts/content-pipeline/backlog.csv` với thực tế `content/stuff/` |
| `npm run test:progress` | Test fog-of-war progression |

---

## 2. Bản đồ thư mục

- `content/stuff/` — **1 file `.md` = 1 card.** Filename = slug = khoá tham chiếu. **Không đổi tên file tùy tiện** (gãy `links`).
- `content/approaches/` — case study/ứng dụng, tham chiếu tới các slug stuff.
- `src/content.config.ts` — **nguồn sự thật của schema** (Zod). Xem mục 4.
- `src/pages/` — routes: `index.astro` (`/`), `about.astro`, `library.astro`, `graph.astro` (đồ thị 3D), `stuff/[slug].astro` (trang thẻ), `stuff-data/[slug].json.ts` (JSON endpoint).
- `src/components/` — `FlipCard.astro` (thẻ lật), `StuffThumb.astro` (thumbnail/fallback), `map/MapCanvas.astro` + `map/StuffOverlay.astro` (Phase 2).
- `src/lib/` — `progress.ts` (fog-of-war, localStorage), `icons.ts` (glyph theo category), `map/palette.ts` (màu theo level), `map/path.ts`, `graph-forces.mjs`.
- `scripts/` — `build-graph.mjs`, `build-map-data.mjs`, `graph-dev-integration.mjs`, `content-pipeline/` (verify, backlog, prompts).
- `.claude/agents/` — subagent `researcher.md`, `writer.md`.
- `docs/` — plan, specs, QA rounds, ADR. `maps/` — README pipeline map.

**Bỏ qua / dọn (không sửa, không commit):** `dist/`, `dist.stale*`, `.astro/`, `.astro-locked-old/`, `.unlink-trash-tmp/`, `__test_*.txt`. Đây là artifact build/rác — không phải nguồn.

---

## 3. Kiến trúc dữ liệu (Phase 2 — Map & fog-of-war)

- Map/graph **không đọc `content/` trực tiếp** → đọc `public/map-data.json` + `public/graph.json` (sinh lúc build từ frontmatter). Sửa content xong phải chạy lại `mapdata`/`graph`.
- 4 map + The Sun, khớp `level` 1–4 trong frontmatter. Canvas 2D tự render (không Tiled/Kaplay).
- Fog-of-war qua `src/lib/progress.ts` — contract ổn định: `getLit / markLit / isLit / litCountByLevel`. Đừng đổi contract này mà không cập nhật cả `test:progress`.

---

## 4. Schema stuff card (khớp `src/content.config.ts`)

```yaml
title: string            # bắt buộc
front: string            # câu hỏi tiếng Việt gợi tò mò — bắt buộc, min 1
back: string             # định nghĩa 1–2 câu — bắt buộc, min 1
level: 1-4               # default 2. 1=Imagining 2=Belief 3=Thinking 4=Knowledge
categories: [slug]       # default []. vd: bias | mental-models | fallacy | memory | perception | theory | heuristic | social
tags: [slug]             # default [] — nhãn tự do phụ trợ
links: [slug]            # default []. CHỈ slug tồn tại trong content/stuff/ — KHÔNG dùng title
refs: [url]              # default []. Nên có ≥1 nguồn (verify khuyến nghị)
strategy: string         # optional — 1 câu actionable
conundrum: string        # optional — tình huống/nghịch lý
approaches: [{title,url}]# optional — liên kết case study
icon: string             # optional — override glyph (mặc định derive theo category)
map_position: {x,y}      # optional — vị trí thủ công trên map
image: string|null       # optional — path nội bộ /assets/stuff/<slug>.png
published: boolean       # default true
```

Body markdown **300–500 từ tự viết** (mẫu chuẩn: `content/stuff/anchoring.md`). Legacy cards migrate từ Jekyll đang ngắn — enrich dần qua pipeline.

### Quy ước `image` (thumbnail 64×64)

- Nếu có, phải là path nội bộ `/assets/stuff/<slug>.png` (file đặt ở `public/assets/stuff/`). Nguồn 128×128, hiển thị 64×64 (nét trên Retina).
- Không có `image` → fallback tự động (glyph `src/lib/icons.ts` + màu level `src/lib/map/palette.ts`) qua `StuffThumb.astro`.
- **Không bịa URL ảnh ngoài** (vd notion.so). Chưa có ảnh nội bộ thì để trống.

---

## 5. Quy tắc bất biến

1. **Không scrape/copy nội dung** từ nguồn có bản quyền (Coglode, DecisionLab, PsychologyToday…). Nguồn chỉ nằm trong `refs`; body **tự viết**.
2. **`npm run verify` phải PASS** trước mọi commit chạm `content/`. CI (`ci.yml`) chạy `verify → graph → mapdata → build`; fail 1 bước là fail build.
3. `links` dùng **slug**, không dùng title. Verifier bắt link gãy.
4. Giọng văn: `front` tiếng Việt gợi tò mò; `back` ngắn gọn, không học thuật khô. Fintech-first khi cho ví dụ.
5. Icon **không random** — derive theo category (`src/lib/icons.ts`).
6. **Không commit thẳng `master`.** Làm trên branch → PR → human review. *Ngoại lệ:* job `daily-content` (scheduled) được commit thẳng vào `new` sau khi `verify + graph + mapdata + build` đều PASS — vẫn không push/merge sang `master`.

---

## 6. Content pipeline (model-tiered)

- **Researcher** = subagent `researcher` (Haiku): tìm `refs`, gợi `level/categories/links`.
- **Writer** = subagent `writer` (Sonnet): viết body + `front/back/strategy`.
- **Verifier** = `npm run verify` (code, $0) — chạy TRƯỚC mọi LLM judge.
- Commands: `/new-card <concept>`, `/batch-cards <n>` (hard cap 10/run), `/enrich-cards <n>`, `/daily-content` (job hàng ngày, 15 card).
- Chạy `npm run backlog` **trước và sau** mỗi batch để chống trùng lặp (đồng bộ `backlog.csv`: todo / needs-enrich / done).
- Pipeline **không tự merge** sang `master` — human review qua PR.

---

## 7. Build · Deploy · CI

- **Deploy production: Netlify** (`netlify.toml` ghi đè UI). Build `npm run build`, publish `dist/`, Node 22, `NPM_FLAGS=--include=dev` (pagefind ở devDeps).
- **CI (`.github/workflows/ci.yml`)** chạy trên push `new|master|dev` + mọi PR: `npm ci → verify → graph → mapdata → build`.
- **Docker (`docker.yml`)** chỉ chạy tay (`workflow_dispatch`) để kiểm Dockerfile — không phải kênh deploy.

---

## 8. Gotchas

- Sửa frontmatter/thêm card mà không chạy lại `mapdata`/`graph` → map/graph hiển thị dữ liệu cũ. `npm run build` tự lo (prebuild).
- `refs`/`links`/`categories` mặc định `[]` trong Zod — thiếu sẽ **không** throw schema, nhưng `verify` mới là cổng chất lượng thật (link gãy, thiếu ref…).
- `front`/`back` `min(1)` → để rỗng sẽ fail build ngay ở content layer.
- `site` trong `astro.config.mjs` đang là placeholder (`theunseen.example.com`) — cập nhật khi đổi domain thật (ảnh hưởng canonical/sitemap).

---

## 9. Definition of Done cho mọi thay đổi

- [ ] `npm run verify` PASS.
- [ ] Nếu chạm content: `npm run graph` + `npm run mapdata` chạy được, `npm run build` xanh.
- [ ] `links` trỏ slug tồn tại; `refs` ≥1; body tự viết 300–500 từ (với card mới).
- [ ] Làm trên branch, mở PR — không đụng `master`.
