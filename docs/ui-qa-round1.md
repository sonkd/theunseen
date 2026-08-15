# UI QA Round 1 — bug list & acceptance criteria

Nguồn: test thủ công của Núi sau khi merge Phase 2 + align design.
Đối chiếu: `docs/design-spec.md` (source of truth UI), `design/The-Unseen.dc.html`.

## Quyết định UX mới (phát sinh từ round này)

1. **Overlay stuff dùng chung toàn site** — Home / Library / Graph đều mở cùng một `StuffOverlay` qua event `stuff:open`. Trang tĩnh `/stuff/<slug>/` vẫn giữ (SEO + share link), nhưng không còn là đích click trong app.
2. **Bỏ nút FLIP** — card lật khi click bất kỳ đâu trên card; gợi ý bằng tooltip "Bấm để lật" hiện lần đầu + khi hover.
3. **Stuff phân bố đều dọc đường đi** (theo arc-length), không cụm.
4. **Auto-focus khi ngọn lửa tới stuff**: chỉ hiện tooltip tên, KHÔNG tự mở overlay.

## Bug list

| # | Trang | Hiện trạng | Kỳ vọng | File |
|---|---|---|---|---|
| B1 | Home | Header hiện "Search available after build." | Dev mode: input search bình thường, Enter → `/library?q=`. Không bao giờ hiện thông báo lỗi cho người dùng | `src/layouts/Base.astro` |
| B2 | Home | Overlay có nút `FLIP · LẬT` | Bỏ nút; click bất kỳ đâu trên card để lật; tooltip hint lần đầu + on hover | `src/components/map/StuffOverlay.astro` |
| B3 | Home | Font breadcrumb 5 map + nav header chưa đúng design system | Cả hai dùng `--font-pixel` ('Press Start 2P') theo design-spec mục 3 | `MapCanvas.astro` (breadcrumb), `Base.astro` (nav) |
| B4 | Home | Stuff co cụm (vị trí theo hash slug) | Zig-zag path + grid placement — xem `docs/map-layout-spec.md` | `scripts/build-map-data.mjs`, `src/lib/map/path.ts` |
| B5 | Home | Đi qua stuff không có phản hồi | Ngọn lửa vào bán kính stuff → auto focus + tooltip tên (không mở overlay) | `MapCanvas.astro` |
| B6 | Home | Cuối map, phím ←/→ không nhảy vùng | Ở cuối/đầu map, phím ←/→ hành xử như nút MOVE ◀ ▶ (nhảy zone/map) | `MapCanvas.astro` |
| B7 | Library | Click card → điều hướng `/stuff/<slug>/` | Mở overlay như Home | `library.astro` |
| B8 | Library | Liệt kê toàn bộ 182 card một trang | Phân trang tối đa 50 stuff/trang | `library.astro` |
| B9 | Graph | Click node → điều hướng trang riêng | Mở overlay như Home | `graph.astro` |
| B10 | Graph | Hover node không có tooltip | Tooltip tên stuff, cùng style với Home | `graph.astro` |

## Acceptance criteria (dùng để verify sau khi fix)

- [ ] Dev mode (`npm run dev`) không hiện bất kỳ thông báo "unavailable/after build" nào ở header
- [ ] Overlay mở được từ cả 3 trang; nội dung + prev/next giống nhau
- [ ] Card lật khi click vào vùng bất kỳ (không phải chỉ nút); tooltip hint xuất hiện lần đầu và khi hover
- [ ] Breadcrumb + nav header dùng Press Start 2P
- [ ] Khoảng cách giữa 2 stuff liên tiếp trên cùng zone lệch nhau < 15%
- [ ] Đi bộ qua stuff → tooltip hiện, overlay KHÔNG mở
- [ ] Cuối map: phím ←/→ nhảy zone/map đúng như nút MOVE
- [ ] Library: 50 card/trang, có điều hướng trang, URL giữ `?page=`
- [ ] Graph: hover tooltip + click mở overlay
- [ ] `npm run build` PASS; `/stuff/<slug>/` vẫn render bình thường
