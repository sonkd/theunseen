# Maps (Phase 2)

4 map chính + The Sun — khớp `level` 1–4 trong frontmatter stuff card:

1. Eikasia · Imagining — level 1
2. Pistis · Belief — level 2
3. Dianoia · Thinking — level 3
4. Noesis · Intelligence/Knowledge — level 4
5. The Sun — màn kết, không chứa stuff, hiển thị tổng flames lit + link /graph, /library

## Phase 2 map pipeline

- Không dùng Tiled JSON hay tilemap runtime. Map do canvas 2D tự vẽ (pixel-art bằng `fillRect` + noise có seed).
- `scripts/build-map-data.mjs` đọc `content/stuff` published, nhóm theo `level`, chia đều vào 3 zones/map, sinh toạ độ (`map_position` nếu có, hoặc deterministic từ seeded path quanh hành lang) → xuất `public/map-data.json`.
- Đường đi (path) mỗi map dùng seeded random theo `level` — deterministic giữa các lần load, export qua `src/lib/map/path.ts` để cả build script và engine dùng chung một seed (vị trí stuff luôn khớp đường đi).
- `src/components/map/MapCanvas.astro` fetch `/map-data.json` lúc runtime để render — không đọc content trực tiếp.

## Map data flow

- `public/map-data.json` là nguồn dữ liệu chính cho map (sinh lúc build bởi `npm run mapdata`, chạy trước `astro build` qua `prebuild`).
- `src/components/map/` chỉ đọc `/map-data.json`, không import `content/stuff`.
- Corridor placement: stuff được đặt trong hành lang ±250px quanh đường đi seeded, tính theo cùng logic với `path.ts`.

## Ghi chú

- File này giải thích cách module map hoạt động trong Phase 2 — xem `docs/phase2-session-prompts.md` cho contract đầy đủ và `docs/design-reconciliation.md` cho đối chiếu prototype ↔ implementation.
- Không đọc nội dung map từ `content/` trực tiếp; mọi thay đổi dữ liệu map phải qua `scripts/build-map-data.mjs`.
