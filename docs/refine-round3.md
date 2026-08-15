# Refine Round 3 — motion trên Home, search panel, trang About

Phạm vi: tinh chỉnh cái đã có. Không thêm tính năng mới.

## Ghi chú thuật ngữ (motion)

Yêu cầu "ease-in-out, vào nhanh — ra chậm" thực chất mô tả **ease-out**: tăng tốc tức thì rồi giảm dần khi về đích. Đây là curve đúng cho phần tử **xuất hiện**.

| Mục đích | Curve | Thời lượng |
|---|---|---|
| Stuff hiện ra (scale-in) | `cubic-bezier(0.16, 1, 0.3, 1)` — ease-out mạnh | 320ms |
| Stuff mờ đi (rời vùng sáng) | `cubic-bezier(0.4, 0, 1, 1)` — ease-in | 220ms (thoát luôn nhanh hơn vào) |
| Focus khi lửa tới sát | `cubic-bezier(0.34, 1.56, 0.64, 1)` — nảy nhẹ | 240ms |
| Ánh sáng ngọn lửa nhấp nháy | `ease-in-out` lặp | 1600–2200ms |

Stagger 40–60ms giữa các stuff cùng lộ ra → cảm giác ánh sáng "quét" qua thay vì bật đồng loạt.
Tôn trọng `prefers-reduced-motion`: bỏ scale + stagger, chỉ đổi opacity.

---

## R3-1 — Home: motion cho stuff, path, ngọn lửa

**Trạng thái stuff (3 mức, theo khoảng cách `d` tới ngọn lửa, `R` = bán kính đuốc):**

| Trạng thái | Điều kiện | Scale | Opacity |
|---|---|---|---|
| hidden | `d > R` | 0.4 | 0 |
| revealed | `d ≤ R` | 1.0 | 0.85 |
| focused | `d ≤ 90px` | 1.15 | 1.0 + glow |
| lit (đã mở) | progress.isLit | 1.0 | 1.0, giữ sáng cả khi `d > R` |

- Chuyển hidden → revealed: scale 0.4 → 1.0 + opacity 0 → 0.85, curve ease-out 320ms, stagger theo khoảng cách (gần lửa hiện trước).
- Chuyển revealed → hidden: ease-in 220ms, **không** scale về 0.4 hoàn toàn (dừng ở 0.85) để tránh giật khi lửa đi qua đi lại.
- Vì đây là canvas: nội suy `scale`/`alpha` trong render loop bằng hàm easing thủ công, không dùng CSS transition. Lưu `t` (0→1) cho mỗi stuff, cập nhật theo `deltaTime`, áp easing khi vẽ.

**Ngọn lửa:**

- Kích thước sprite tăng ~1.4× so với hiện tại.
- Quầng sáng: 3 lớp radial-gradient chồng nhau (lõi trắng ấm → `--flame` → tắt dần), thay vì một vòng cứng. Bán kính quầng ≈ 2.5× chiều cao sprite.
- Nhấp nháy: bán kính + alpha dao động ±6% chu kỳ ~1.8s, `ease-in-out`. Đủ để "sống", không gây phân tán.
- Viền/bóng đổ: bỏ viền cứng nếu có; dùng bóng mềm màu `iconGlow` của map hiện tại.

**Đường đi:**

- Bo tròn các góc: tại mỗi control point, thay góc nhọn bằng cung quadratic bán kính 40–60px (hoặc Catmull-Rom tension ~0.5). Vẫn giữ nhịp lên-xuống rõ ràng — chỉ mềm góc, không làm phẳng đường.
- Giới hạn độ dốc tối đa ~35°.
- Vẽ đường bằng 2 lớp: lớp dưới rộng hơn màu `path`, lớp trên hẹp hơn màu `pathDot` → cảm giác lối mòn có chiều sâu.

**File:** `src/components/map/MapCanvas.astro`, `src/lib/map/path.ts`.

---

## R3-2 — Search: panel kết quả đọc được

**Bug hiện tại (đã chụp màn hình xác nhận):** kết quả Pagefind render **trong suốt đè lên bản đồ tối** → chữ không đọc nổi. Kèm theo lỗi nội dung: chuỗi kỹ thuật `___END_PAGEFIND_WEIGHT___` lọt vào excerpt, và sub-result đổ nguyên body của card ra màn hình.

**Yêu cầu:**

- Panel kết quả có **nền đặc** (`--bg`), viền 2px `--ink`, radius 12px, đổ bóng mềm; nổi trên map với z-index cao hơn canvas nhưng thấp hơn nhóm MOVE/OPTIONS.
- Desktop: panel neo dưới ô search, rộng bằng ô search (min 340px), cao tối đa 60vh, cuộn trong panel.
- Mobile (< 768px): **overlay toàn màn hình** — nền `--bg`, có nút đóng, ô search cố định trên đỉnh, danh sách cuộn bên dưới. Không để panel nhỏ đè lên map.
- Mỗi kết quả chỉ hiển thị: **title** (đậm) → **description = trường `front`** (2 dòng, cắt bằng ellipsis) → **tags** (chip nhỏ: categories + `Map N`). Bỏ excerpt tự động của Pagefind và bỏ sub-results.
- Lọc sạch mọi chuỗi `___END_PAGEFIND_WEIGHT___` khỏi nội dung hiển thị.
- Trạng thái: đang tìm (skeleton 3 dòng), không có kết quả (nêu từ khoá + gợi ý mở Library), lỗi tải Pagefind (fallback form `/library?q=` như hiện tại).
- Bấm kết quả → `stuff:open` (overlay dùng chung), không điều hướng.
- Bàn phím: `↓`/`↑` di chuyển giữa kết quả, `Enter` mở, `Esc` đóng panel. Focus trap trên mobile overlay.

**Ghi chú kỹ thuật:** để có `front` + tags cho từng kết quả, dùng `data-pagefind-meta` trên trang stuff (`title`, `front`, `categories`, `level`) rồi đọc từ `result.meta` — không cần API mới.

**File:** `src/layouts/Base.astro`, `src/pages/stuff/[slug].astro` (chỉ thêm thuộc tính `data-pagefind-meta`).

---

## R3-3 — About: nội dung từ branch master

Lấy nguyên văn nội dung `about.md` trên branch `master` (tác giả: Núi) và chuyển sang Astro:

- Nội dung: đoạn Plato / Allegory of the Cave, đoạn prism, mục **Flames 🔥**, mục **Notes** với 3 chú thích có anchor qua lại (`#ref-1` ↔ `#plato-says`, v.v.).
- 2 hình: `assets/img/stuff/prism.png` và `assets/img/the-flame.png` — lấy từ branch master bằng `git show master:<path> > public/assets/img/<...>` (đừng tải lại từ web).
- Bỏ cú pháp Jekyll: `{{site.baseurl}}/category/` → `/library/`; `{:target="_blank"}` → `target="_blank" rel="noopener"`.
- Giữ `<figure>` + `<figcaption>` cho cả 2 hình.
- Style theo design system: chiều rộng đọc ~680px, thang chữ đã chuẩn hoá, chú thích `<small>` màu `--muted`, hình bo 12px + viền `--border`.

**File:** `src/pages/about.astro`, `public/assets/img/`.

---

## Definition of Done

- [ ] Stuff scale-in ease-out 320ms có stagger; mờ đi ease-in 220ms; `prefers-reduced-motion` chỉ đổi opacity
- [ ] Ngọn lửa to hơn ~1.4×, quầng sáng 3 lớp, nhấp nháy ±6%
- [ ] Không còn góc nhọn trên đường đi; nhịp lên-xuống vẫn rõ
- [ ] Panel search có nền đặc, đọc được trên map tối; mobile là overlay toàn màn hình
- [ ] Kết quả chỉ có title + front + tags; không còn `___END_PAGEFIND_WEIGHT___`
- [ ] `/about` khớp nội dung master, 2 hình hiển thị, anchor chú thích nhảy đúng
- [ ] `npm run build` PASS; kiểm tra ở 1512px và 390px
