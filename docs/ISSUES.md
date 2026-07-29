# QA Issue Backlog — The Stuff Unseen

> Bàn giao cho Claude Code. Fix theo thứ tự P1 → P4. Mỗi issue có: triệu chứng · file · nguyên nhân · cách fix · acceptance.

---

## P1 — Critical

### 1. `share.js` gọi addEventListener trên null
- **Triệu chứng:** Console `TypeError: Cannot read properties of null (reading 'addEventListener')` tại `assets/js/share.js:18` khi mở trang About.
- **File:** `assets/js/share.js` (dòng 1-3, 17-18).
- **Nguyên nhân:** `#copy-btn` / `.share-popup` / `.share-btn` không tồn tại trên trang không có share popup (About/Home dùng `layout: post` theo default nên vẫn load share.js).
- **Fix:** Null-check trước khi dùng: nếu `copyUrl`/`shareOptions`/`shareBtn`/`closeShareBtn` null thì return sớm hoặc bọc `if (el)`.
- **Acceptance:** Không còn exception trong console ở About/Home; share vẫn chạy ở trang `/stuff/:name/`.

### 2. Nút Dark/Light theme không hoạt động
- **Triệu chứng:** Click icon mặt trời → không đổi theme, không đổi class trên `<html>/<body>`, icon sun/moon không đổi. Fail ở Home + About.
- **File:** `assets/js/main.js` (IIFE, dòng 19 và 43).
- **Nguyên nhân (đã đọc source):** `main.js` là 1 IIFE. `line 19 lamp.addEventListener` không null-check; `line 43 $('#modal-container').click()` phụ thuộc cứng jQuery. Nếu bất kỳ dòng nào throw → cả IIFE abort → handler theme không gắn.
  **Lưu ý:** `share.js` và `main.js` là 2 `<script>` riêng → lỗi share.js **không** làm dừng main.js. Đừng coi share.js là nguyên nhân theme.
- **Fix:**
  - Guard `#mode`: `if (lamp) lamp.addEventListener(...)`.
  - Tách phần theme lên đầu, đưa `$('#modal-container')` xuống dưới và bọc `if (window.jQuery && $('#modal-container').length)`.
  - Xác nhận `data-theme` toggle + `localStorage.theme` đồng bộ với inline script trong `_layouts/*.html`.
- **Acceptance:** Toggle đổi theme tức thì mọi trang; reload giữ đúng theme; console sạch lỗi từ main.js.

### 3. Search 404 + tên file JSON không nhất quán
- **Triệu chứng:** SimpleJekyllSearch fetch fail. Categories gọi `/assets/search-stuff.json`, Archive gọi `/assets/search.json` — báo 404.
- **File:** `_includes/footer.html:29,32`; `assets/search.json`, `assets/search-stuff.json`.
- **Nguyên nhân:** Cả 2 file nguồn ĐỀU tồn tại → 404 nhiều khả năng do build/emit hoặc `baseurl`, không phải thiếu file.
- **Fix:** Kiểm tra `_site/assets/` sau `jekyll build` xem 2 file có emit không. Gộp về **1 feed dùng chung** cho mọi trang (có thể tái dùng pattern `assets/decks.json`), sửa `footer.html` trỏ 1 tên duy nhất, prepend `site.baseurl`.
- **Acceptance:** Search chạy ở cả Categories + Archive; Network 200 cho file JSON.

---

## P2 — High

### 4. Menu mobile không có nền che (overlay trong suốt)
- **Triệu chứng:** ~390px, mở hamburger → menu đè lên nội dung, `background: rgba(0,0,0,0)`, `opacity: .8`, không backdrop → khó đọc.
- **File:** SCSS của navbar (`_sass/klise/*` hoặc `_includes/navbar.html`).
- **Fix:** Thêm nền đục cho overlay menu ở breakpoint mobile (solid bg theo theme hoặc `backdrop-filter: blur`) + `z-index` cao hơn nội dung.
- **Acceptance:** Ở ≤430px, menu mở có nền đục, chữ đọc rõ, không lộ nội dung phía sau.

### 5. Logo nav vỡ trên Study & Stats
- **Triệu chứng:** Study/Stats dùng `the-flame.png` (ảnh ngang) nhồi khung 39×40 `object-cover` → crop méo. Home/About dùng `avatar.png` đúng.
- **File:** `_includes/navbar.html` (nhánh `page.id` / `page.image`).
- **Nguyên nhân:** Navbar lấy `post.image` (ảnh header bài) làm logo khi page có image.
- **Fix:** Logo nav luôn dùng `site.logo` (`avatar.png`), không lấy ảnh bài. (Có thể bỏ field `image` khỏi front matter của `study.md`/`stats.md` như giải pháp tạm.)
- **Acceptance:** Logo giống nhau, không méo, trên mọi trang.

---

## P3 — Medium

### 6. Footnote `[3]` ở About trỏ sai anchor
- **Triệu chứng:** `[3]` (cognitive load) có `href="#ref-2"`, đúng phải `#ref-3`.
- **File:** `about.md` (phần thân + Notes).
- **Fix:** Sửa `href` của footnote [3] thành `#ref-3` (id đã tồn tại trong Notes).
- **Acceptance:** Click `[3]` nhảy đúng note 3.

### 7. Hamburger ☰ và close ✕ hiện cùng lúc ở mobile
- **Triệu chứng:** Menu chưa mở nhưng cả ☰ và ✕ cùng hiện góc phải.
- **File:** `_includes/navbar.html` (label icon) + `assets/js/main.js` (cbox change) / CSS `:checked`.
- **Fix:** Chỉ hiện 1 icon theo trạng thái `#menu-trigger`: mặc định ẩn `.close-icon`; khi `:checked` thì ẩn `.menu-icon`, hiện `.close-icon` (ưu tiên CSS thuần để không phụ thuộc JS).
- **Acceptance:** Đóng → chỉ ☰; mở → chỉ ✕.

---

## P4 — Low

### 8. Categories/Decks: 4 nhóm rỗng, 181 bài dồn "Mental Models"
- **Triệu chứng:** Concepts/Tools/Frameworks/People hiện mô tả nhưng 0 bài. Deck ở Study cũng chỉ có "Mental Models".
- **File:** `_data/categories.yml`; front matter `my_collections/_stuff/*.md`; `_data/the-cognitive-bias-codex.yml`.
- **Fix (chọn 1):**
  - (a) Ẩn category/deck rỗng trong template.
  - (b) **Khuyến nghị:** viết script map 181 bias → 4 nhóm Codex (Too Much Info / Not Enough Meaning / Need to Act Fast / What to Remember) từ `the-cognitive-bias-codex.yml`, gán lại `categories`.
- **Acceptance:** Không còn category/deck rỗng; hoặc mỗi bài thuộc đúng nhóm Codex.

### 9. Study: legend phím tắt dễ nhầm với bộ đếm
- **Triệu chứng:** Thanh trên "0 đã thuộc" vs hint dưới "1 cần ôn · 2 đã thuộc" (thực ra là phím tắt).
- **File:** `_pages/study.md` (dòng `.fc-hint`).
- **Fix:** Đổi diễn đạt hint, ví dụ: "Phím tắt: **Space** lật · **←/→** chuyển · **1** = Cần ôn · **2** = Đã thuộc".
- **Acceptance:** Không thể hiểu nhầm hint là bộ đếm.

---

## Đã hoạt động tốt (không cần fix)
Flip flashcard (animation mượt), Đã thuộc/Cần ôn + auto-advance, lưu tiến độ localStorage, trang Stats phản ánh đúng, tab filter Archive, điều hướng menu mobile khi click link.

## Nên test thêm (sau khi fix)
Trang chi tiết `/stuff/:name/` (flip + khối Connects + prev/next) · footer (`/feed.xml`, `/thanks`) · `/study/` + `/stats/` ở 768px & 1024px · empty-state của `/stats/` khi chưa học thẻ nào.
