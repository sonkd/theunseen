# Refine Round 4 — search hỏng, thumbnail, layout card Library

Test trên `http://localhost:8080` (docker preview).

---

## S1 — Search hoàn toàn không hoạt động (P0)

### Bằng chứng thu được

- Gõ vào ô search → panel hiện `Đang tìm kiếm cho anchoring...` và **đứng im vĩnh viễn**, 0 kết quả.
- Console lặp lại 4 lần:
  ```
  Error: Failed to load Pagefind metadata
      at Worker.<anonymous> (/pagefind/pagefind.js)
  ```
- `PagefindUI` là function (script tải được), nhưng `/pagefind/pagefind-entry.json` **không lấy được**.

→ Kết luận: `pagefind-ui.js/css` có trong image, nhưng **index (entry json + wasm + chunk) thiếu hoặc không serve được**. Search chưa từng chạy trên bản docker này.

### Nghi vấn cần kiểm chứng (theo thứ tự)

1. `postbuild: pagefind --site dist` có thực sự chạy trong Docker không? Binary `pagefind` tải lúc `npm ci` là bản glibc; base image là `node:22-alpine` (musl) → nhiều khả năng không chạy được hoặc thoát sớm.
2. `.dockerignore` (36 byte) có loại `node_modules` không — nếu không, `COPY . .` ghi đè `node_modules` alpine bằng bản macOS.
3. Thư mục `dist/pagefind/` sau build có đủ: `pagefind-entry.json`, `wasm.*.pagefind`, `*.pf_index`, `fragment/` không.
4. nginx có serve đúng MIME cho `.pagefind` / `.pf_index` / `.wasm` không.

### Yêu cầu sửa

- Build phải **fail lớn** nếu index không sinh ra — thêm bước kiểm tra sau `pagefind`: không tồn tại `dist/pagefind/pagefind-entry.json` → `exit 1`. Không bao giờ để image chạy với search chết.
- **Lỗi phải rơi về fallback:** hiện code chỉ ẩn form dự phòng khi `new PagefindUI()` khởi tạo thành công — nhưng khởi tạo thành công ≠ index chạy. Thêm timeout ~2.5s: nếu chưa có kết quả/lỗi metadata → ẩn UI Pagefind, hiện lại form `/library?q=`. Người dùng không bao giờ nhìn spinner vô hạn.
- Đảm bảo chạy được cả 3 môi trường: `npm run dev` (không index — dùng fallback), `npm run preview` (có index), docker (có index).

---

## S2 — Trường `image`: thumbnail 64×64 cho mỗi stuff

### Hiện trạng

- Schema đã có `image: z.string().nullish()` nhưng **không trang nào render**.
- Chỉ **3/186** card có `image`, và cả 3 đều trỏ `notion.so/images/page-cover/...` — hotlink sang Notion: dễ chết link, chậm, không kiểm soát được.

### Quyết định

- `image` = **đường dẫn nội bộ** `/assets/stuff/<slug>.png`, kích thước hiển thị **64×64** (file nguồn 128×128 để nét trên màn Retina).
- Không có `image` → **fallback là ô icon**: nền `--surface`, glyph từ `src/lib/icons.ts` màu theo level (dùng `icon` trong `src/lib/map/palette.ts`). Fallback là mặc định cho 183 card hiện tại, nên nó phải trông cố ý, không như "ảnh lỗi".
- Bỏ 3 URL Notion hiện có (xoá giá trị, để trống → dùng fallback) — tránh phụ thuộc bên ngoài.
- Ảnh dùng `loading="lazy"`, `width/height` cố định để không gây layout shift, `alt` = title.

### Nơi hiển thị

| Chỗ | Kích thước | Ghi chú |
|---|---|---|
| Card ở `/library` | 64×64 | thay vị trí chấm icon hiện tại |
| Overlay stuff | 64×64 | cạnh title |
| Trang `/stuff/<slug>` | 64×64 | cạnh h1 |
| Map, graph | **không dùng** | giữ glyph/node như hiện tại |

Cập nhật `CLAUDE.md` (mục schema) và `scripts/content-pipeline/prompts/writer.md`: `image` optional, nếu có phải là path nội bộ.

---

## S3 — Layout card `/library` xô lệch

### Chẩn đoán

- `.grid a` dùng `align-items: center` + `grid-template-columns: auto 1fr`; card nào title dài (vd. *Defensive attribution hypothesis*) xuống 2 dòng thì cao hơn hẳn card cùng hàng → hàng lởm chởm, mắt không quét được theo cột.
- Card quá thấp (~64px) so với mật độ nội dung; padding `.85rem 1rem` (13.6/16px) không nằm trên lưới 8pt.
- Gap lưới 12px ≈ padding trong card → vi phạm "internal ≤ external", card dính vào nhau.

### Yêu cầu

- **Chiều cao đồng nhất**: mọi card cùng `min-height` (đề xuất **112px**, đủ chứa thumbnail 64 + padding 16×2 + lề), nội dung căn trên (`align-items: start`), title `-webkit-line-clamp: 2` để title dài không phá layout.
- Layout card: thumbnail 64×64 bên trái, cột phải gồm title (16px/600, tối đa 2 dòng) → meta chip (12px). Khoảng cách thumbnail ↔ text 16px.
- Padding card 16px; gap lưới 24px; radius 12px; `minmax(280px, 1fr)`.
- Hover: `translateY(-1px)` + đổi nền, transition 150ms ease-out.
- Mobile 390px: 1 cột, thumbnail giữ 64×64.

---

## Definition of Done

- [ ] Gõ vào ô search ra kết quả trên bản docker; không còn "Failed to load Pagefind metadata"
- [ ] Build fail nếu `dist/pagefind/pagefind-entry.json` không tồn tại
- [ ] Search lỗi/không có index → tự rơi về form `/library?q=` trong ≤ 2.5s, không có spinner vô hạn
- [ ] Card Library cao đều nhau (đo 3 hàng đầu, chênh lệch 0px), title 2 dòng không phá layout
- [ ] Thumbnail 64×64 hiển thị ở library / overlay / trang stuff; card không có `image` dùng ô icon fallback
- [ ] Không còn URL Notion trong `content/stuff/`
- [ ] `npm run verify && npm run build` PASS; kiểm tra 1512px và 390px
