# Refine Round 5 — graph tooltip, library chips/meta, deck-style card, search

Test trên `http://localhost:4321` (dev). Phạm vi: cải thiện cái đã có.

---

## P1 — Search box không hoạt động (P0, 2 bug độc lập)

### Bằng chứng

1. Dev mode: `PagefindUI` = `undefined` (đúng — chưa build index), fallback form `/library?q=` hiện ra đúng.
2. Submit form với `q=anchoring` → điều hướng tới `/library`, nhưng **`?q=` biến mất**, `location.search` rỗng.
3. `library.astro` → `getState()` chỉ đọc `cat`, `level`, `page`. **Không đọc `q` bao giờ.**

→ Hai lỗi chồng nhau:

- **P1a** — Library không hề xử lý tham số `q`. Kể cả URL đúng `/library?q=anchoring` cũng không lọc gì.
- **P1b** — Library **xoá** `q` khỏi URL: `applyFilters(getState())` chạy lúc load → `updateUrl()` dựng lại query chỉ từ `cat/level/page` rồi `history.replaceState` → mất `q`. Người dùng thấy URL "sạch" và kết quả đầy đủ 186 card, tưởng search hỏng hoàn toàn.

### Yêu cầu

- `getState()` đọc thêm `q`; `updateUrl()` **giữ nguyên** `q` (không bao giờ tự xoá tham số lạ).
- Lọc theo `q`: khớp không phân biệt hoa thường trên `title` + `front` (dữ liệu đã có sẵn trong DOM/`data-*`). Kết hợp AND với filter category/level đang bật.
- Khi có `q`: hiện chip "Từ khoá: …" có nút ✕ để xoá riêng phần tìm kiếm; `resultCount` nêu rõ đang tìm gì.
- Ô search ở header điền sẵn giá trị `q` khi đang ở `/library?q=…` (recognition over recall).
- Trên trang có Pagefind (bản build), fallback vẫn phải hoạt động — không được để hai cơ chế đá nhau.

---

## P2 — `/graph`: tooltip khi hover node

Tooltip đã có trong code nhưng thực tế khó kích hoạt (vùng bấm node degree-0 chỉ r=8px — xem `docs/ui-audit-library-graph.md` B2).

Yêu cầu: hover node → hiện tooltip tên stuff **giống hệt tooltip ở Home** (nền `--ink`, chữ `--font-pixel` 8px, viền trắng 2px, radius nhỏ, bám con trỏ, không chặn chuột). Thêm hit area trong suốt r ≥ 22px. Rời node → ẩn ngay (không delay). Bàn phím: node focus được bằng Tab → hiện cùng tooltip.

---

## P3 — `/library`: chip tràn dòng + meta nhỏ lại

Hiện trạng đo được: `.chips` có `flex-wrap: nowrap`, `overflow-x: visible` → chip cuối bị cắt ngang ("1 · Ima…" mất chữ), không xuống dòng, không cuộn được.

- `.chips` → `flex-wrap: wrap`, gap 8px. Chip tràn thì xuống dòng, không cắt, không cuộn ngang.
- Meta chip trên card (`<span class="meta">2 · Belief</span>`): **bỏ số thứ tự** → chỉ còn `Belief`. Cỡ chữ nhỏ hơn (10px, letter-spacing .08em), padding gọn, màu `--muted`, viền nhạt — là nhãn phụ, không phải nút.
- Sau khi bỏ số, phải còn phân biệt được level: dùng màu chấm/viền theo level (lấy từ `palette.ts`), không dùng số.

---

## P4 — Popup stuff dạng deck card (theo mẫu Learning Loop)

Thiết kế lại `StuffOverlay` theo cấu trúc thẻ bài 2 mặt. **Không thêm trường mới vào schema** — ánh xạ từ dữ liệu đã có:

### Mặt trước

| Vùng | Nguồn dữ liệu | Style |
|---|---|---|
| Băng đầu thẻ | `categories[0]` viết hoa + dòng phụ `Map N · <tên map>` | nền đậm (màu `icon` của map theo level), chữ `--font-pixel` 8px, canh giữa |
| Khung minh hoạ | `StuffThumb` phóng to (128×128) trên nền nhạt màu map | chiếm ~30% chiều cao thẻ |
| Tiêu đề | `title` | 28px/700, sát lề trái |
| Câu hỏi dẫn | `front` | 18px/600, 2–3 dòng |
| Định nghĩa | `back`, mở đầu bằng nhãn in đậm `ĐỊNH NGHĨA` | 13px, line-height 1.5 |
| Cũng gọi là | *(không có trong schema — bỏ hẳn, không bịa)* | — |
| Loop in | `links` (2–5 slug) | nhãn nhỏ + tên các stuff liên quan, click chuyển thẻ |
| Chân thẻ | `Map N` bên phải | 10px, `--muted` |

### Mặt sau

| Vùng | Nguồn dữ liệu |
|---|---|
| Tiêu đề | `Strategy: <title>` |
| Nội dung | body 300–500 từ, giữ nguyên heading/bullet của Markdown |
| Chiến lược | `strategy` — đặt trong khối nổi bật, nhãn `Strategy` |
| Đọc thêm | `refs` — nhãn `Read more`, chữ nhỏ |
| Chân thẻ | tên site + level |

### Quy tắc hình thức (theo mẫu đính kèm)

- Tỉ lệ thẻ ~ 9:16 dựng đứng, bo góc 24px, viền 2px `--ink`, bóng mềm; mặt sau nền tối hơn (`--dark-bg-2`) để hai mặt phân biệt tức thì.
- Desktop: thẻ cao tối đa 82vh, rộng ~420px, canh giữa; hai cột phụ (refs trái / links phải) như hiện tại **gộp vào trong thẻ** — thẻ là một khối duy nhất, không còn 3 cột rời.
- Mobile: thẻ chiếm gần trọn màn hình, cuộn trong thẻ.
- Lật: click bất kỳ đâu trên thẻ (giữ nguyên hành vi hiện tại), tooltip hint lần đầu.
- Body dài hơn chiều cao thẻ → cuộn **trong mặt sau**, không làm thẻ dài ra.
- Tôn trọng `prefers-reduced-motion`: bỏ animation lật 3D, chuyển bằng fade.

---

## Definition of Done

- [ ] `/library?q=anchoring` lọc đúng; `q` không bị xoá khỏi URL; ô search điền sẵn từ khoá
- [ ] Chip filter xuống dòng, không chip nào bị cắt ở mọi bề rộng ≥ 320px
- [ ] Meta card còn `Belief` (không số), 10px; level phân biệt bằng màu
- [ ] Hover node ở `/graph` ra tooltip tên stuff, style trùng Home; hit area ≥ 22px
- [ ] Popup stuff là thẻ đơn khối 2 mặt theo bảng ánh xạ trên, không thêm trường schema mới
- [ ] `npm run build` PASS; kiểm tra 1512px và 390px
