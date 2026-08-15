# UX/UI Audit — /library và /graph

Test trên `http://localhost:8080` (docker preview), viewport 1512×734.
Phạm vi: **chỉ cải thiện những gì đã có** — không thêm tính năng hay nội dung mới.

## Người dùng & bối cảnh (nền cho mọi quyết định)

- **Ai:** người tò mò về bias/mental models, phần lớn là khách mới đến từ link chia sẻ hoặc search.
- **Cảm xúc:** tò mò nhưng thiếu kiên nhẫn — họ đến để "hiểu một khái niệm", không phải để duyệt danh mục.
- **Bối cảnh:** desktop lẫn mobile, đọc lướt 3 giây rồi quyết định ở lại hay thoát.
- **Vai trò 2 trang:** Home (map) là trải nghiệm khám phá; **Library = tra cứu có chủ đích**; **Graph = thấy được mối liên hệ**. Cả hai là "library mode" — phải nhanh, quét được, không cần chơi.

---

# A. /library — Score 6/10

Chức năng đủ và đúng (filter, phân trang, overlay), nhưng thứ bậc thị giác đặt sai trọng tâm và ngôn ngữ thiết kế lệch khỏi phần còn lại của site.

## Critical

**A1. Filter panel chiếm trọn màn hình đầu tiên**
Panel filter cao ~380px đẩy nội dung xuống dưới; ở 1512×734 chỉ thấy **2 hàng card**. Nội dung mới là hero của trang, không phải bộ lọc.
→ Thu gọn: hàng chip category cuộn ngang một dòng, level thành 4 chip cùng hàng, bỏ dòng mô tả "Filter by category and level, then share the URL." (không ai đọc). Mục tiêu: panel ≤ 120px, thấy ≥ 4 hàng card above the fold.

**A2. Không có empty state**
Lọc ra 0 kết quả → lưới trắng trơn, pagination biến mất, chỉ còn dòng "Showing 0 / 0 cards". Người dùng không biết phải làm gì.
→ Empty state: nêu bộ lọc đang áp dụng + nút "Bỏ lọc" (dùng lại `#clearFilters`).

**A3. Pagination render bằng `createElement` → mất CSS scoped**
Cùng lớp bug với breadcrumb ở Home: nút số trang không mang `data-astro-cid-*` nên `.page-numbers button {...}` không áp dụng. Trong ảnh chụp, nút `1 2 3 4` là ô vuông mặc định của trình duyệt, trong khi `‹ Prev` / `Next ›` là pill bo tròn — hai style cạnh nhau.
→ Render sẵn tối đa N nút trong markup rồi toggle, hoặc dùng `<style is:global>` giới hạn trong `.page-numbers`.

**A4. Đổi trang không đưa người dùng về đầu danh sách**
Bấm "2" ở cuối trang → nội dung đổi nhưng scroll vẫn ở đáy; người dùng nhìn thấy cuối danh sách mới, tưởng chưa đổi.
→ `scrollIntoView` lên đầu lưới sau khi đổi trang.

## Important

**A5. Meta line không mang thông tin**
182/186 card hiện đúng một chuỗi "Mental models · Map 2 — Belief". Dòng meta chiếm 40% chiều cao card mà giá trị bằng 0.
(Gốc rễ là phân bố level — xem `docs/ui-qa-round2.md` R2-1 — nhưng UI đang khuếch đại nó.)
→ Rút gọn còn nhãn map dạng chip nhỏ; nếu category trùng với filter đang bật thì ẩn đi.

**A6. Chip level chỉ là số trần**
"1 2 3 4" không nói lên điều gì với người mới. Trang khác gọi là "Map 2 — Belief".
→ Đổi nhãn thành `1 · Imagining`, `2 · Belief`… (dữ liệu đã có sẵn trong `LEVEL_MAPS`).

**A7. Không có tín hiệu "bấm sẽ mở overlay"**
Card là `<a href="/stuff/...">` nhưng click lại mở overlay. Hover chỉ đổi màu viền — không đủ affordance, và người dùng có thể kỳ vọng rời trang.
→ Hover nâng nhẹ (translateY -1px) + đổi nền; giữ href cho ctrl-click và SEO.

**A8. Hai ngôn ngữ thiết kế trên cùng một site**
Header/map: pixel, viền cứng 2px, góc vuông. Library: nền kem, viền 1px, bo 16–18px, sans-serif.
→ Thống nhất về hệ đã chốt trong `docs/design-spec.md`: viền cứng hơn (2px `--ink` cho phần tử tương tác chính), bo nhỏ lại (8–12px), nhãn/chip dùng `--font-pixel` ở cỡ nhỏ.

## Polish

**A9. Radius và spacing không theo hệ**
Radius: panel 18px, card 16px, chip 999px, page-number 0 (do A3). Padding card `.85rem 1rem` = 13.6/16px — không nằm trên lưới 8pt; gap lưới 12px ≈ padding trong card, vi phạm "internal ≤ external".
→ Chuẩn hoá: radius {8, 12, 999}; padding card 16px; gap lưới 24px.

**A10. Không có thang typography**
`h1` là mặc định trình duyệt; title card 16px; meta 13.6px. Chênh lệch chỉ nhờ màu.
→ Áp thang 1.2: 12 / 14 / 16 / 20 / 24px; `h1` 24px; title card 16px/600; meta 12px.

## Điểm tốt

- Filter multi-select + sync URL `?cat=&level=&page=` — chia sẻ được trạng thái lọc, đúng nhu cầu tra cứu.
- `aria-pressed` trên chip, card là `<a>` thật → keyboard và screen reader dùng được.
- Giữ `href` gốc và tôn trọng ctrl/cmd-click — chi tiết nhỏ mà nhiều người bỏ qua.

---

# B. /graph — Score 4/10

Thuật toán lực chạy được và click node mở overlay đúng, nhưng trang chưa kể được câu chuyện "mạng lưới ý tưởng" và vi phạm vài nguyên tắc cơ bản.

## Critical

**B1. ~150 node mồ côi bao quanh viền, che mất mạng lưới thật**
Chỉ ~20 node có liên kết; số còn lại (degree 0) bị lực đẩy dồn thành viền chấm quanh khung. Nhìn vào không thấy "graph", chỉ thấy nhiễu.
→ Xử lý ở tầng UI (gốc rễ content đã ghi ở R2-1): node degree 0 mờ đi (opacity .35, bán kính nhỏ nhất) và **gom lại một khu vực riêng** thay vì trộn vào cụm chính. Cụm có liên kết được ưu tiên ở giữa.

**B2. Vùng bấm quá nhỏ**
Node degree 0 có `r = 8px` → mục tiêu 16px, thấp hơn nhiều mức tối thiểu 44px. Tôi hover trượt node ở lần thử đầu; tooltip không hiện.
→ Thêm `<circle>` trong suốt bán kính ≥ 22px làm hit area, hoặc `stroke-width` lớn + `pointer-events: all`. Trên mobile bắt buộc.

**B3. Màu mã hoá level nhưng không có chú giải**
4 màu = 4 level, nhưng không chỗ nào giải thích. Thông tin truyền tải **chỉ bằng màu** — vi phạm WCAG.
→ Legend nhỏ (4 dòng: chấm màu + `1 · Imagining`…) đặt góc khung; tooltip thêm tên map.

**B4. Màu node không thuộc design system**
`#bcb7ff`, `#53c6d2`, `#8dcc6b` là màu tự chế, không có trong `docs/design-spec.md`.
→ Lấy `icon`/`iconGlow` của 4 map trong `src/lib/map/palette.ts` → graph và map nói cùng một ngôn ngữ màu, người dùng học một lần dùng cả hai nơi.

## Important

**B5. Bố cục cuộn hai lần**
`h1` + đoạn intro đẩy khung graph xuống dưới fold; khung lại cao 80vh → phải cuộn để thấy graph, rồi cuộn tiếp để thấy hết.
→ Cho graph chiếm phần còn lại của viewport (như map ở Home): header + tiêu đề gọn trên một dòng, khung `height: calc(100vh - header - title)`.

**B6. Không có trạng thái nghỉ / rỗng**
`graph.json` rỗng hoặc lỗi fetch → hộp trắng, không thông báo. Trong lúc mô phỏng chạy cũng không có tín hiệu gì.
→ Empty state ngắn + skeleton mờ trong ~300ms đầu.

**B7. Mô phỏng đóng băng, không tương tác lại được**
`alpha` tắt dần rồi `return` — node đứng im, có thể đang chồng nhau, và không kéo được để xem rõ.
→ Cho phép kéo node (pointerdown/move/up) và hâm nóng lại `alpha` khi kéo. Đây là hành vi cơ bản của graph view, không phải tính năng mới.

**B8. Intro tiếng Anh giữa site song ngữ**
"Explore the network of ideas in an Obsidian-style graph…" — các trang khác dùng VN hoặc VN/EN.
→ Viết lại song ngữ ngắn, hoặc bỏ hẳn (canvas tự nói lên nó).

## Polish

**B9. Cạnh liên kết gần như vô hình** — `rgba(58,55,47,0.18)` 1px. Tăng lên .35 và làm đậm cạnh của node đang hover.
**B10. Radius khung 24px** lớn hơn mọi thành phần khác; gradient nền trang trí không phục vụ mục đích. Đưa về 12px, bỏ gradient hoặc đổi thành tín hiệu (sáng ở cụm dày đặc).
**B11. `O(n²)` mỗi frame** — 186 node = ~17k phép tính/frame. Chạy được bây giờ, sẽ chậm ở ~500 node. Ít nhất giới hạn số vòng lặp khi `alpha` nhỏ.

## Điểm tốt

- Click node → `stuff:open` dùng chung overlay với Home/Library — nhất quán, đúng kiến trúc đã chốt.
- Bán kính node theo degree — hub node tự nổi bật, đúng nguyên tắc mã hoá dữ liệu.
- Tooltip đã dùng `--font-pixel`, đúng design system.

---

## Nên kiểm chứng gì

1. **5-second test** trên /library: cho xem 5 giây rồi hỏi "trang này để làm gì, bạn làm gì tiếp theo?" — nếu họ nói "để lọc" thay vì "để đọc các khái niệm" thì A1 chưa được giải quyết.
2. **Task test** trên /graph: "tìm một khái niệm liên quan tới confirmation bias" — đo xem có ai làm được không khi 150 node mồ côi còn ở đó.
3. Cả hai trang ở viewport 390px — hiện chưa test mobile lần nào.
