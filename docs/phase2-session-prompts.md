# Phase 2 — Map & Fog-of-war: 3 session prompts (chạy song song)

Nguồn thiết kế: prototype Claude Design "The Unseen.dc.html" (share link). Nếu đã tải file về `design/The-Unseen.dc.html` thì các session tham khảo trực tiếp; nếu chưa, spec đã đủ trong prompt.

## Quyết định đã chốt (mọi session tuân theo — override docs cũ nếu mâu thuẫn)

1. **4 map + The Sun** (không phải 5 map như prototype): Map 1 Eikasia·Imagining, 2 Pistis·Belief, 3 Dianoia·Thinking, 4 Noesis·Intelligence/Knowledge — khớp `level` 1–4. The Sun là màn kết (không chứa stuff). Palette sáng dần từ map 1 (tối) → map 4 (sáng) → Sun (rực).
2. **Header không có Daily/Favorites**: chỉ brand + search + Library + Graph + About.
3. **Canvas tự render** (như prototype, không Tiled/Kaplay, không dependency mới ngoài những gì đã có). Pixel-art bằng canvas 2D + CSS.
4. Data thật từ `content/stuff` → `public/map-data.json` sinh lúc build.

## Contract chung (3 session phải theo đúng — đây là điểm tích hợp)

```ts
// public/map-data.json (S5b sinh, S5a đọc)
{ maps: [{ level: 1|2|3|4, name: string, greek: string, zones: 3,
  stuff: [{ slug, title, icon, zone: 0|1|2, x: number, y: number }] }] }

// src/lib/progress.ts (S5c viết, S5a + S5b gọi)
getLit(): string[]; markLit(slug: string): void; isLit(slug: string): boolean;
litCountByLevel(): Record<number, number>;

// Sự kiện mở overlay (S5a phát, S5b lắng nghe)
window.dispatchEvent(new CustomEvent('stuff:open', { detail: { slug } }))
// Overlay đóng: CustomEvent('stuff:close')
```

Ràng buộc chung: KHÔNG đụng `content/`, `scripts/content-pipeline/`. Không commit — human review. Kết thúc phải chạy `npm run build` PASS và mô tả cách test.

---

## Prompt S5a — Map engine (canvas, movement, fog)

```
Đọc docs/phase2-session-prompts.md (quyết định + contract), docs/build-plan.md, src/lib/icons.ts.

Task: xây map engine cho trang chủ, thay placeholder trong src/pages/index.astro.

Steps:
1. Tạo src/components/map/MapCanvas.astro (island, <script> vanilla TS, canvas 2D full-viewport dưới header).
2. Render 4 map theo quyết định #1: mỗi map 3 zones nối ngang; nền pixel-art tự vẽ (tile 16px: cỏ/đá/cây đơn giản bằng fillRect + noise có seed); palette mỗi map một tông, sáng dần map 1→4.
3. Đường đi: polyline uốn lượn lên xuống ngẫu nhiên (seeded random theo level — deterministic giữa các lần load). Nhân vật ngọn lửa (sprite 2-frame nhấp nháy tự vẽ) đi dọc đường: phím ←/→ đi bộ 280px/s (lửa tự lên/xuống dốc), phím </> và nút MOVE ◀ ▶ nhảy zone; hết map thì sang map kế; footer breadcrumb 4 map + The Sun, click nhảy map.
4. Fog-of-war: mặt nạ radial gradient bám vị trí lửa, bán kính mặc định 500px (mobile = window.innerWidth); ngoài bán kính tối đen, mép mềm.
5. Đọc /map-data.json (fetch runtime; nếu file chưa có, dựng mock 5 stuff/map đúng schema contract để dev độc lập với S5b). Vẽ icon stuff tại (x,y); hover → tooltip title; click → dispatch CustomEvent 'stuff:open' theo contract. Stuff đã lit (progress.isLit — nếu src/lib/progress.ts chưa có thì stub isLit=false, TODO tích hợp) vẽ sáng hơn.
6. Nút OPTIONS (góc phải dưới, trên nhóm MOVE; MOVE+OPTIONS z-index cao nhất): popup gồm slider bán kính đuốc 500–900px, toggle reveal-all, 5 nút nhảy nhanh (4 map + Sun).
7. The Sun (sau map 4): màn hình sáng rực, hiển thị tổng flames lit / tổng stuff, link tới /graph và /library.
8. Test: npm run build PASS; mô tả các bước test thủ công (đi bộ, nhảy zone, fog, hover, click phát event, options).

Ràng buộc: chỉ tạo/sửa src/components/map/**, src/pages/index.astro. KHÔNG đụng content/, scripts/, src/layouts/, src/components/khác. Không dependency mới. Không commit.
```

## Prompt S5b — Map data + stuff overlay + header

```
Đọc docs/phase2-session-prompts.md (quyết định + contract), docs/build-plan.md, scripts/build-graph.mjs, src/pages/stuff/[slug].astro, src/lib/icons.ts.

Task: sinh map-data.json từ content thật + overlay stuff card trên map + chỉnh header.

Steps:
1. Tạo scripts/build-map-data.mjs (pattern giống build-graph.mjs, dùng gray-matter): đọc content/stuff published → nhóm theo level (1-4) → chia đều vào 3 zones/map → toạ độ: nếu frontmatter có map_position thì dùng; nếu không, sinh deterministic từ hash slug trong hành lang ±250px quanh đường đi (dùng cùng seeded random theo level như contract — export hàm pathY(level, x) vào src/lib/map/path.ts để S5a dùng chung nếu file chưa tồn tại). Output public/map-data.json đúng schema contract.
2. Thêm script "mapdata" vào package.json, gọi trong CI (.github/workflows/ci.yml, sau npm run graph) và prebuild.
3. Tạo src/components/map/StuffOverlay.astro (island): lắng nghe 'stuff:open' → fetch nội dung đã render sẵn — làm bằng cách xuất JSON tĩnh /stuff-data/<slug>.json (tạo src/pages/stuff-data/[slug].json.ts trả về title/front/back/refs/links/strategy/body-html). Layout overlay theo wireframe: refs bên trái, card giữa (flip 3D: front = câu hỏi; nút FLIP·LẬT lật sang back = nền tối + toàn văn body; ◂ FLIP lật lại), links bên phải (click → mở stuff đó), nút Close + Share (copy URL /stuff/<slug>/). Khi overlay mở: ◀ ▶ duyệt prev/next stuff trong cùng map (S5a giữ MOVE nổi trên overlay — chỉ cần phát 'stuff:open' mới). Khi mở overlay gọi progress.markLit(slug) nếu src/lib/progress.ts tồn tại (nếu chưa: TODO comment).
4. Header (src/layouts/Base.astro): brand + search box (Pagefind — nếu chưa có UI search thì input Enter → /library?q=) + Library + Graph + About. TUYỆT ĐỐI không thêm Daily/Favorites. Tạo src/pages/about.astro ngắn (nội dung từ docs/build-plan.md phần metaphor).
5. Test: npm run mapdata ra file hợp lệ (in số stuff/map); npm run build PASS; mô tả test overlay bằng cách dispatch event thủ công trong console.

Ràng buộc: chỉ tạo/sửa scripts/build-map-data.mjs, package.json, ci.yml, src/components/map/StuffOverlay.astro, src/lib/map/path.ts, src/pages/stuff-data/, src/pages/about.astro, src/layouts/Base.astro. KHÔNG đụng content/, scripts/content-pipeline/, src/pages/index.astro, src/components/map/MapCanvas.astro. Không commit.
```

## Prompt S5c — Progression, đồng bộ docs & design

```
Đọc docs/phase2-session-prompts.md (quyết định + contract), docs/build-plan.md, maps/README.md, CLAUDE.md.

Task: module progression (fog-of-war có trạng thái) + đồng bộ toàn bộ docs theo quyết định Phase 2.

Steps:
1. Tạo src/lib/progress.ts đúng chữ ký contract: lưu localStorage key 'unseen:lit' (mảng slug, dedupe), thêm getExploredPct(level, total). Kèm test nhỏ chạy bằng node (mock localStorage) tại scripts/test-progress.mjs, thêm script "test:progress" vào package.json.
2. Tự lắng nghe 'stuff:open' trong module init (import từ island nào cũng an toàn — idempotent) để markLit, phòng khi S5b chưa gọi trực tiếp.
3. Đồng bộ docs theo 4 quyết định trong docs/phase2-session-prompts.md:
   - docs/build-plan.md Phase 2: canvas tự render thay Tiled/Kaplay; 4 map + Sun; header bỏ Daily/Favorites; cập nhật DoD Phase 2.
   - maps/README.md: viết lại — không còn Tiled JSON; mô tả seeded path + corridor placement + map-data.json.
   - CLAUDE.md: cập nhật mục cấu trúc (src/components/map/, src/lib/progress.ts) và quy tắc "map đọc map-data.json, không đọc content trực tiếp".
   - docs/agent-workflow-guide.md: thêm mục Phase 2 sessions (S5a/S5b/S5c và ranh giới file).
4. Viết docs/design-reconciliation.md: bảng đối chiếu prototype ↔ implementation (những gì giữ: torch 500px, 280px/s, corridor, flip overlay, OPTIONS; những gì đổi: 5 map→4+Sun, bỏ Daily/Favorites, data thật, palette per-map) — để lần sau update bản design trên Claude theo đúng file này.
5. Test: npm run test:progress PASS; npm run build PASS.

Ràng buộc: chỉ tạo/sửa src/lib/progress.ts, scripts/test-progress.mjs, package.json (script test), docs/**, maps/README.md, CLAUDE.md. KHÔNG đụng content/, src/components/, src/pages/. Không commit.
```

---

## Thứ tự merge (sau khi cả 3 xong)

1. Merge S5c trước (docs + progress — không phụ thuộc ai).
2. Merge S5b (data + overlay; gỡ TODO markLit nếu có).
3. Merge S5a cuối (engine; gỡ stub isLit, nối progress thật + map-data thật, xoá mock).
4. Chạy: `npm run verify && npm run graph && npm run mapdata && npm run build` → smoke test đủ luồng: đi bộ → fog → click stuff → flip → prev/next → Sun → reload thấy vùng đã lit còn sáng.

DoD Phase 2: đủ luồng trên desktop + mobile viewport; Lighthouse trang / ≥ 80; 0 dependency mới; các trang Library/Graph/stuff không bị ảnh hưởng.
