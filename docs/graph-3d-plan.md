# Kế hoạch: Spherical 3D Graph View cho `/graph/`

> Tài liệu giao việc cho Claude Code. Đọc toàn bộ phần **0. Bối cảnh & Ràng buộc** trước khi bắt đầu bất kỳ task nào.

---

## 0. Bối cảnh & Ràng buộc

### 0.1 Giả định (điều chỉnh nếu sai)

| # | Giả định | Nếu sai thì làm gì |
|---|---|---|
| A1 | Site chạy Astro (port dev 4321), build tĩnh (SSG) | Nếu là SSR/Next → chuyển bước bake layout sang API route có cache |
| A2 | Nội dung nằm trong Astro Content Collections (`src/content/**/*.md(x)`) | Nếu là file phẳng → sửa glob trong `scripts/build-graph.mjs` |
| A3 | Liên kết giữa các note dùng wikilink `[[slug]]` và/hoặc markdown link nội bộ | Bổ sung regex parser tương ứng |
| A4 | Quy mô hiện tại **< 3.000 node** và **< 15.000 link** | Nếu > 5.000 node → xem §5 "Escape hatch" |
| A5 | Trang `/graph/` hiện đang render 2D hoặc chưa có | Nếu đã có code 3D → task T4–T7 chuyển thành refactor |
| A6 | Có thể thêm dependency mới vào `package.json` | — |

### 0.2 Ba điều chỉnh so với tài liệu tham khảo ban đầu

**(1) KHÔNG dùng hard spherical projection (normalize × R).**
Chuẩn hoá cứng toạ độ sau mỗi tick sẽ ép toàn bộ node lên **vỏ cầu rỗng**. Hệ quả: mọi link cắt qua ruột cầu, node mặt sau bị che, và cấu trúc cụm (community) bị bóp méo vì mất một bậc tự do. Đây là hành vi của plugin *spherical-knowledge-graph*, **không phải** của graph view Obsidian.

Thay bằng **soft radial constraint**: `d3-force-3d` đã có sẵn `forceRadial(radius, x, y, z)` — đẩy node về điểm gần nhất trên mặt cầu với cường độ tỉ lệ khoảng cách 1 chiều. Cho `strength` thành tham số 0 → 1:

- `strength = 0` → quả cầu đặc (giống 3D graph plugin của Obsidian)
- `strength ≈ 0.15` → **khuyến nghị mặc định**: hình cầu rõ nét nhưng cụm vẫn phình ra được
- `strength → 1` → vỏ cầu rỗng cứng

**(2) Bake layout ở build time, không tính lực ở runtime.**
Site tĩnh → chạy simulation trong Node lúc build, ghi thẳng `x, y, z` vào JSON. Lợi ích:
- First paint là hình cầu hoàn chỉnh, không có màn "Big Bang" giật lag
- Layout **tất định** → vị trí node giống nhau mọi lần truy cập → người đọc hình thành trí nhớ không gian (spatial memory), đây là giá trị UX lớn nhất của graph view
- Chạy được 600–1.000 tick mà không tốn 1ms nào của main thread

Runtime chỉ re-heat khi user kéo node hoặc bật/tắt filter.

**(3) Ảnh tham khảo là graph view *2D* của Obsidian.**
Screenshot bạn gửi là disc 2D, không phải 3D. Cần chọn có chủ đích: 3D đẹp hơn nhưng **tăng extraneous cognitive load** (xoay, occlusion, mất phương hướng). Khuyến nghị: 3D là default, giữ toggle 2D (`numDimensions(2)`) cho người muốn đọc nhanh.

### 0.3 Stack đề xuất

| Phương án | Thư viện | Ngưỡng node | Chọn khi |
|---|---|---|---|
| **A — Khuyến nghị** | `3d-force-graph` (three.js + d3-force-3d, bundled) | ≤ 3.000 | Time-to-value nhanh nhất, API đầy đủ (fly-to camera, hover, drag, pauseAnimation) |
| B | `three.js` + `d3-force-3d` tự viết renderer | ≤ 50.000 | Cần InstancedMesh/Points, shader custom, kiểm soát bundle |
| C | `@cosmograph/cosmos` (GPU compute) | 100.000+ | Chỉ 2D — dùng như escape hatch nếu graph phình to |

`d3-force-3d` dùng **oct-tree + xấp xỉ Barnes–Hut** cho `forceManyBody`, độ chính xác chỉnh qua `theta` → đã đáp ứng yêu cầu O(N log N) trong tài liệu tham khảo, không cần tự implement.

**Chọn A cho v1.** Ghi chú: `3d-force-graph` mặc định tạo 1 `THREE.Mesh` cho mỗi node — bắt đầu tụt frame từ ~2.000 node. Xem T14.

### 0.4 Tham số khởi điểm

```js
const N = nodes.length;
const R = 4.5 * Math.sqrt(N);        // bán kính cầu; area ∝ R² nên scale theo √N

forceLink(links).distance(30).strength(l => 1 / Math.min(deg[l.source], deg[l.target]))
forceManyBody().strength(-120).theta(0.9).distanceMax(R * 2)  // distanceMax cải thiện perf rõ rệt
forceRadial(R, 0, 0, 0).strength(0.15)
forceCenter(0, 0, 0).strength(0.05)
alphaDecay(0.01)        // build time; runtime dùng mặc định 0.0228
velocityDecay(0.4)
ticks: 600              // build time
```

---

## 1. Phase P0 — Data & Layout Pipeline (build time)

### T1 — Script trích xuất đồ thị
**File:** `scripts/build-graph.mjs`

- Đọc toàn bộ content collection, parse wikilink `[[...]]`, markdown link nội bộ, và `tags`/`category` trong frontmatter.
- Sinh `nodes[]`: `{ id, title, url, tags[], folder, wordCount, createdAt }`
- Sinh `links[]`: `{ source, target }` — **dedupe** cặp trùng, bỏ self-loop.
- Xử lý dangling link (trỏ tới note không tồn tại): mặc định **drop**, có flag `--keep-ghosts` để giữ dưới dạng node `ghost: true`.
- Giữ node orphan (không có link nào) — chúng sẽ nổi ở rìa cầu, đó là tín hiệu hữu ích.

**AC:**
- `npm run graph:build` chạy được, exit 0
- Cùng input → output byte-identical (không dùng `Date.now()`, `Math.random()` không seed)
- In ra console: số node, số link, số orphan, số dangling

---

### T2 — Tính metrics đồ thị
**File:** `scripts/lib/graph-metrics.mjs`
**Deps:** `graphology`, `graphology-metrics`, `graphology-communities-louvain`

- `degree`, `inDegree`, `outDegree` cho mỗi node
- Connected components (đánh `componentId`)
- Louvain community detection → `communityId` (dùng để tô màu, thay vì tô theo folder — cụm màu sẽ trùng với cụm không gian, giảm tải nhận thức)

**AC:** mỗi node có đủ `degree`, `componentId`, `communityId`. Louvain chạy với seed cố định.

---

### T3 — Bake layout 3D offline
**File:** `scripts/lib/bake-layout.mjs`
**Deps:** `d3-force-3d`, `seedrandom` (hoặc tự viết mulberry32)

1. **Init bằng Fibonacci sphere** — phân bố đều, tránh cụm chồng tại gốc:
   ```js
   const phi = Math.PI * (3 - Math.sqrt(5));
   nodes.forEach((n, i) => {
     const y = 1 - (i / (N - 1)) * 2;
     const r = Math.sqrt(1 - y * y);
     const th = phi * i;
     n.x = R * Math.cos(th) * r;
     n.y = R * y;
     n.z = R * Math.sin(th) * r;
   });
   ```
   Shuffle thứ tự node bằng seeded PRNG **trước** khi init, để node cùng cụm không bị đặt cạnh nhau một cách giả tạo.

2. Chạy simulation headless: `sim.stop()` rồi `for (i=0; i<600; i++) sim.tick()`.
3. Recenter + rescale về bbox chuẩn hoá.
4. Ghi `public/graph/graph.json`: node có `x, y, z` đã bake, làm tròn **2 chữ số thập phân** (giảm ~35% dung lượng).

**AC:**
- Layout tất định (chạy 2 lần → diff rỗng)
- `alpha < 0.01` khi kết thúc
- Thời gian bake < 10s ở quy mô hiện tại
- `graph.json` sau gzip < 200KB
- Snapshot test: render preview PNG bằng headless canvas để review bằng mắt (optional nhưng rất đáng)

---

### T4 — Gắn vào Astro build
- Thêm `"graph:build": "node scripts/build-graph.mjs"` vào `package.json`
- Chạy trong `prebuild` **và** ở Astro integration hook `astro:config:setup` cho dev mode (watch `src/content/**`)

**AC:** `npm run dev` và `npm run build` đều tự sinh `graph.json` mới nhất.

---

## 2. Phase P1 — Renderer

### T5 — Astro island
**File:** `src/pages/graph.astro`, `src/components/GraphView.tsx` (hoặc `.svelte`/vanilla)

- `client:only="react"` — three.js không SSR được
- **Dynamic import** `3d-force-graph` bên trong `useEffect` để không lọt vào bundle chính
- Fetch `/graph/graph.json` song song với việc khởi tạo scene
- Skeleton loading: hiển thị wireframe cầu mờ, không dùng spinner

**AC:** bundle của các trang khác **không tăng** một byte nào (kiểm bằng `npm run build -- --verbose` hoặc `rollup-plugin-visualizer`).

---

### T6 — Khởi tạo với layout đã bake
```js
Graph
  .graphData(data)              // node đã có x,y,z
  .cooldownTicks(0)             // KHÔNG chạy sim khi load
  .numDimensions(3)
```
Chỉ gọi `d3ReheatSimulation()` khi user kéo node hoặc đổi filter/tham số lực.
Khi re-heat, cấu hình lực **phải khớp hệt** file bake (T3) — tách config ra `src/lib/graph-forces.js` dùng chung cho cả Node và browser.

**AC:** first paint hiển thị hình cầu ổn định, 0 frame nhảy vị trí.

---

### T7 — Mã hoá thị giác
| Kênh | Ánh xạ | Ghi chú |
|---|---|---|
| Kích thước node | `4 * Math.sqrt(degree + 1)` | Diện tích tuyến tính theo degree, đúng tri giác |
| Màu node | `communityId` → palette | Tối đa 8 màu + xám cho phần còn lại |
| Độ mờ link | `0.08 – 0.15` | Hairball phải đọc như *texture*, không phải nhiễu |
| Độ sâu | `THREE.FogExp2` + `depthWrite` | **Bắt buộc** — không có depth cue thì 3D vô nghĩa |
| Node hiện tại | Ring/glow | Khi vào từ một note cụ thể |

- Nền và palette lấy từ CSS custom properties của site để đồng bộ dark/light mode.

**AC:** kiểm 3 mức zoom (xa/vừa/gần), node mặt sau phải mờ rõ rệt so với mặt trước.

---

### T8 — Label với LOD
- Mặc định chỉ hiện label cho node có `degree ≥ P90`
- Hover → hiện label node đó + 1-hop neighbors
- Zoom gần (`camera.position.length() < R`) → hiện thêm label theo khoảng cách
- Dùng `THREE.Sprite` với canvas texture atlas, **không** dùng `CSS2DRenderer` (reflow DOM mỗi frame)

**AC:** ≤ 40 label hiển thị đồng thời ở mọi thời điểm.

---

## 3. Phase P2 — Tương tác

### T9 — Hover: highlight 1-hop *(giá trị cao nhất, ưu tiên trước T10–T12)*
- Hover node → node đó + neighbors giữ nguyên opacity, phần còn lại giảm còn 0.1
- Link liên quan đổi màu + tăng width
- Throttle raycast xuống 30fps

**AC:** độ trễ hover < 50ms ở quy mô hiện tại.

---

### T10 — Click: focus + điều hướng
- Click 1 lần → `cameraPosition()` bay tới node (transition 800ms, ease-out), mở side panel với title + excerpt + danh sách backlink
- Click nút trong panel hoặc double-click node → điều hướng tới note
- ESC → thoát focus, camera về vị trí cũ

---

### T11 — Search & filter
- Input search: fuzzy match title → highlight kết quả, mờ phần còn lại (**không** xoá node khỏi scene → giữ ổn định không gian)
- Filter theo tag/folder: node bị loại chuyển sang xám + opacity 0.05, **không** re-layout
- Slider "Depth": chỉ hiện subgraph N-hop quanh node đang focus

> **Nguyên tắc:** filter thay đổi *độ nổi bật*, không thay đổi *vị trí*. Node nhảy chỗ là nguyên nhân số một phá vỡ spatial memory.

---

### T12 — Panel điều khiển
Collapsible, mặc định đóng, lưu state vào `localStorage`:

- `Sphericity` (0 → 1) — map trực tiếp vào `forceRadial().strength()`, **đây là slider chính**
- `Link distance`, `Repulsion`
- `Show labels` / `Auto-rotate` / `2D ↔ 3D` (`numDimensions(2|3)` có animate transition)
- `Reset layout` → nạp lại toạ độ bake gốc

---

### T13 — Deep link
- `/graph/?focus=<slug>` → camera bay thẳng tới node đó khi load
- Thêm link "Xem trong graph" ở cuối mỗi note, trỏ tới URL trên

---

## 4. Phase P3 — Hiệu năng

### T14 — Ngưỡng chuyển renderer
- Nếu `N > 2000`: thay `nodeThreeObject` bằng một `THREE.Points` duy nhất với custom shader (size attribute + circular alpha mask), hoặc `THREE.InstancedMesh`
- Link: gộp thành **một** `THREE.LineSegments` với `BufferGeometry` chung — tuyệt đối không tạo 1 object/link
- Đặt feature flag `RENDER_MODE = 'mesh' | 'points'`, tự chọn theo `N`

**AC:** ≥ 50 FPS khi xoay liên tục, đo trên MacBook Air M-series ở `N` hiện tại.

---

### T15 — Vòng đời render
- `IntersectionObserver` → `pauseAnimation()` khi canvas ra khỏi viewport
- `document.visibilitychange` → pause khi chuyển tab
- Dừng rAF khi simulation đã nguội **và** camera đứng yên **và** auto-rotate tắt
- Giới hạn `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`

**AC:** CPU về ~0% khi trang idle 5 giây (kiểm bằng Chrome Performance Monitor).

---

### T16 — Ngân sách bundle
- three.js + 3d-force-graph ≈ 600KB gzip → **phải** lazy load
- Prefetch chunk khi hover link `/graph/` trên nav
- Đặt budget trong CI: JS của trang `/graph/` ≤ 900KB gzip; các trang khác không đổi

---

## 5. Phase P4 — A11y & Fallback

### T17 — `prefers-reduced-motion`
- Tắt auto-rotate, tắt camera fly-to (nhảy thẳng), tắt mọi transition layout

### T18 — Fallback không WebGL
- Detect qua `canvas.getContext('webgl2')`
- Fallback: danh sách note nhóm theo `communityId`, sắp xếp theo degree giảm dần

### T19 — Bàn phím & screen reader
- `<div role="application" aria-label="...">` bọc canvas
- Tab qua top-50 node theo degree; Enter → mở note
- Kèm `<nav hidden>` chứa danh sách đầy đủ node + backlink dạng `<ul>` cho screen reader và cho SEO crawl

### T20 — Mobile
- `N > 500` → chỉ render node `degree ≥ 2`, tắt label mặc định
- Touch: 1 ngón xoay, 2 ngón zoom, tap = hover, double-tap = mở note
- Cấm auto-rotate trên mobile (tốn pin)

---

## 6. Escape hatch — nếu đồ thị vượt 5.000 node

1. Chuyển sang `@cosmograph/cosmos` (2D, GPU compute) — hy sinh 3D, đổi lấy 100k+ node ở 60fps
2. Hoặc giữ 3D nhưng **prune** ở build time: chỉ render node có `degree ≥ 2`, gộp phần đuôi thành node "cluster" bung ra khi click

---

## 7. Definition of Done

### Kỹ thuật
- [ ] `npm run build` sinh `graph.json` tất định, layout không đổi giữa hai lần build
- [ ] `/graph/` first contentful paint hiển thị hình cầu ổn định, không có giai đoạn "nổ tung"
- [ ] ≥ 50 FPS khi xoay liên tục; CPU ~0% khi idle
- [ ] Bundle các trang khác không tăng
- [ ] Hoạt động trên Safari iOS + Chrome Android
- [ ] Có fallback không WebGL và tôn trọng `prefers-reduced-motion`

### Trải nghiệm
- [ ] Nhìn 3 giây là nhận ra "đây là bản đồ ghi chú", không cần chú thích
- [ ] Hover bất kỳ node nào → hiểu ngay nó nối với gì
- [ ] Từ graph tới được note trong ≤ 2 thao tác
- [ ] Vị trí node giống hệt nhau giữa hai lần truy cập

### Đo lường (thêm event vào analytics)
| Sự kiện | Ý nghĩa |
|---|---|
| `graph_view_loaded` | Baseline lưu lượng |
| `graph_node_hover` (unique nodes/session) | Độ sâu khám phá |
| `graph_node_navigate` | **Metric chính** — graph có thực sự dẫn tới đọc bài không |
| `graph_search_used`, `graph_control_changed` | Tính năng nào đáng giữ |
| `time_on_graph` | Chỉ có ý nghĩa khi đi kèm `graph_node_navigate` — nếu time cao mà navigate thấp thì đó là *lạc lối*, không phải *hấp dẫn* |

> Chỉ số thành công đề xuất: **≥ 25% session vào `/graph/` kết thúc bằng ít nhất một `graph_node_navigate`**. Dưới ngưỡng này, graph đang là đồ trang trí chứ không phải công cụ điều hướng.

---

## 8. Thứ tự thực thi khuyến nghị

```
T1 → T2 → T3 → T4        (P0 — làm xong mới thấy được gì)
      ↓
T5 → T6 → T7             (P1 — có hình cầu tĩnh, đẹp)
      ↓
T9 → T10                 (P2 — hai tương tác giá trị nhất)
      ↓
T15 → T17 → T18          (chống hồi quy về perf/a11y)
      ↓
T8, T11, T12, T13, T14, T16, T19, T20   (theo nhu cầu thực tế)
```

**Ship được sau T10.** Mọi thứ sau đó là tối ưu tăng dần.
