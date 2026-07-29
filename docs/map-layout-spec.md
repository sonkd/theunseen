# Map Layout Spec — zig-zag path + grid placement

> Thay thế cách sinh path cong (spline) và đặt stuff theo hash slug hiện tại.
> Mục tiêu: đường đi zig-zag lên/xuống rõ ràng, stuff bám lưới, phân bố đều — theo sketch của Núi.

## 1. Hệ toạ độ & lưới

- **World**: mỗi map rộng `W = zones × zoneWidth` (zones = 3). Toạ độ chuẩn hoá 0..1 khi lưu vào `map-data.json`; nhân với kích thước viewport khi render.
- **Grid**: `CELL = 64px` (bội số của tile 16px). Cột `col = round(x / CELL)`, hàng `row = round(y / CELL)`.
- Mọi stuff **snap vào tâm ô lưới** — không đặt toạ độ tự do.
- Nền vẽ chấm lưới mờ tại mỗi giao điểm (như sketch): dot 2px, `rgba(ink, .06)` — chỉ hiện trong bán kính đuốc.

## 2. Đường đi zig-zag

Thay spline bằng **polyline gấp khúc thẳng**, đỉnh/đáy nằm trên lưới:

```
cyclesPerZone = 1          // 1 chu kỳ lên-xuống mỗi zone → 3 chu kỳ/map
segments      = zones × cyclesPerZone × 2      // = 6 đoạn/map
segWidth      = W / segments
yTop          = rowTop × CELL                 // đỉnh (giá trị y nhỏ)
yBottom       = rowBottom × CELL              // đáy
amplitude     = yBottom - yTop ≈ 4 × CELL     // ~256px

vertex[i] = { x: i × segWidth,
              y: (i % 2 === 0) ? yBottom : yTop }   // i chẵn = đáy, lẻ = đỉnh
```

- Kết quả: **đi lên → xuống → lên → xuống** liên tục khi ngọn lửa đi từ trái sang phải, đúng như sketch (chevron nhọn, không bo cong).
- `rowTop`/`rowBottom` lệch nhẹ theo map (seeded ±1 hàng) để 5 map không giống hệt nhau, nhưng **luôn snap lưới** và **luôn giữ đúng nhịp lên-xuống**.
- Ngọn lửa đi dọc polyline này (nội suy tuyến tính giữa 2 đỉnh), góc nghiêng sprite theo hướng đoạn đang đi.

## 3. Đặt stuff trên lưới

```
STEP_COLS = 3                                  // khoảng cách tối thiểu giữa 2 stuff (cột)
slots     = các cột col = STEP_COLS, 2×STEP_COLS, ... trong zone
```

Với stuff thứ `i` (thứ tự ổn định theo alphabet slug) trong zone:

1. `col = slotCols[i]` — lấy tuần tự, **phân bố đều theo cột**, không dùng hash.
2. `pathRow = round(pathY(col × CELL) / CELL)` — hàng của đường đi tại cột đó.
3. `offset = (i % 2 === 0) ? -1 : +1` — xen kẽ **trên / dưới** đường đi (như sketch).
   Nếu `i % 4 === 0` dùng `offset = -2` để tạo nhịp thị giác (hàng cao hơn).
4. `row = clamp(pathRow + offset, gridTop, gridBottom)`.
5. Toạ độ cuối = tâm ô `(col × CELL, row × CELL)`.
6. Nếu ô đã bị chiếm → lấy slot cột kế tiếp (collision-free đảm bảo bằng vòng lặp).

Ràng buộc:

- Mọi stuff nằm trong hành lang `|y - pathY(x)| ≤ 2 × CELL` → luôn lọt bán kính đuốc 500px.
- `map_position` trong frontmatter **vẫn override**, nhưng cũng bị snap về tâm ô lưới gần nhất.
- Deterministic: cùng input → cùng output; không random ở bước đặt.
- Nếu số stuff của zone > số slot khả dụng → tăng `zoneWidth` (nới world) thay vì nhồi thêm vào ô đã có.

## 4. Chia stuff vào zone

Giữ nguyên: `level` quyết định map (1–4 → map 1–4, map 5 KNOWLEDGE không chứa stuff).
Trong map, chia đều theo thứ tự alphabet: `zone = floor(index × zones / total)` — chênh lệch giữa các zone ≤ 1.

## 5. Definition of Done

- [ ] Đường đi là polyline gấp khúc, nhịp lên-xuống-lên-xuống thấy rõ khi đi hết map
- [ ] Đỉnh/đáy path và mọi stuff đều nằm trên giao điểm lưới `CELL = 64`
- [ ] Khoảng cách cột giữa 2 stuff liên tiếp = `STEP_COLS` (đều tuyệt đối), không cụm
- [ ] Stuff xen kẽ trên/dưới đường đi
- [ ] Không có 2 stuff trùng ô
- [ ] Chấm lưới mờ hiện trong vùng sáng của đuốc
- [ ] `npm run mapdata` in ra: số stuff/map, số stuff/zone, min/max khoảng cách cột
