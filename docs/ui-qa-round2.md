# UI QA Round 2 — test trên dev local (Chrome)

Test bởi Claude qua Claude-in-Chrome trên `http://localhost:4321`, ngày 29/07/2026.

## PASS

- B1 search box — header hiện ô `SEARCH / TÌM KIẾM ⏎`, không còn thông báo "available after build"
- B3 font — nav header + breadcrumb 5 map đã dùng Press Start 2P
- B5 auto-focus — đi tới gần stuff hiện tooltip tên (vd. "Illusory correlation"), không tự mở overlay ✓
- B7/B8 Library — click card mở overlay; phân trang "Showing 50 / 186 cards (page 1 of 4)"; filter category + level hoạt động
- B2 — nút FLIP đã bỏ
- MOVE ◀ ▶ + breadcrumb nhảy map hoạt động; palette 5 map đúng design-spec (tím → xanh → …)

## FAIL / cần sửa

### R2-1 (P0) — Phân bố level hỏng: 182/186 card ở level 2

```
level: 2 → 182 cards      level: 3 → 3      level: 4 → 1      level: 1 → 0
```

Hệ quả: map 1 (Imagining), 4, 5 **trống rỗng**; map 2 (Belief) nhồi 182 stuff → icon chồng lên nhau thành mảng.
Nguyên nhân gốc: migration Jekyll map thẳng `difficulty: 2` → `level: 2` cho toàn bộ.
**Đây là việc của content pipeline, không phải UI** — cần một pass phân loại lại level theo rubric trong CLAUDE.md.
Mục tiêu phân bố: mỗi map 30–60 stuff.

### R2-2 (P0) — Đường đi quá gấp khúc, cơ học

Path hiện là chevron nhọn biên độ lớn (~300px), 3 chevron giống hệt nhau lặp lại → trông như dãy núi, không như đường mòn.
Yêu cầu: cong và gấp khúc **tự nhiên** hơn (xem prompt R2-2 bên dưới).

### R2-3 (P1) — Phím ←/→ không đi bộ được

Bấm ArrowLeft/ArrowRight (kể cả sau khi click vào canvas) — ngọn lửa **không di chuyển chút nào**. Chỉ nút MOVE hoạt động.
Hint dưới màn hình vẫn ghi "PHÍM ← → ĐỂ ĐI BỘ". B6 chưa xong, và vấn đề rộng hơn: canvas không nhận keyboard focus.

### R2-4 (P1) — Overlay chưa thấy mặt sau

Overlay mở ra chỉ thấy mặt trước (câu hỏi + Close/Share). Không thấy tooltip hint "bấm để lật", chưa xác nhận được click-to-flip hoạt động.

### R2-5 (P2) — Icon stuff render thành chấm tròn

Trên map, stuff hiển thị như đốm tròn phát sáng, không thấy glyph (★ ▲ ◼︎ ●) như design. Ở mật độ cao (map 2) chúng dính thành mảng.

### R2-6 (P2) — Library dùng style khác design system

Card Library bo tròn, nền kem, sans-serif — không cùng ngôn ngữ với map (pixel, viền cứng 2px). Cần thống nhất.
