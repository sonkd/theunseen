---
name: daily-content
description: Job nội dung hàng ngày — sync backlog, ưu tiên 2 card map Imagining + 2 card map Thinking mỗi ngày rồi mới lấy đủ 15 theo priority cũ, regenerate graph + map data, cập nhật backlog, commit vào branch new. Dùng cho scheduled task hoặc khi muốn chạy một ngày sản xuất đầy đủ.
---

# Daily content job (15 cards/ngày — ưu tiên 2 Imagining + 2 Thinking/ngày)

Chạy end-to-end. Hard cap 15 card/run. Nếu bất kỳ bước nào fail 2 lần liên tiếp → dừng, báo cáo, KHÔNG commit.

## Bước 1 — Sync backlog

```bash
npm run backlog
```

Script `scripts/content-pipeline/sync-backlog.mjs` quét toàn bộ `content/stuff/`, cập nhật status:

- `needs-enrich` — có file nhưng body < 300 từ (priority 1 = có ≥2 links, 2 = body < 100 từ, 3 = còn lại)
- `todo` — concept chưa có file
- `done` — đủ chuẩn, bỏ qua

Đây là cơ chế chống trùng lặp: card đã đủ chuẩn tự chuyển `done`, không bao giờ được chọn lại.

## Bước 2 — Sản xuất 15 card

Thứ tự chọn (đã cập nhật để cân bằng 2 map đang thiếu nội dung — Imagining 0 card, Thinking 15 card so với Belief 212 card):

1. **Ưu tiên nhóm map trước** — trong các dòng `status=todo`:
   - Lấy 2 dòng có `notes` chứa `map:imagining`, priority thấp nhất (thứ tự curated 41→70, KHÔNG đảo).
   - Lấy 2 dòng có `notes` chứa `map:thinking`, priority thấp nhất (thứ tự curated 81→110, KHÔNG đảo).
   - Nếu một trong hai tag đã hết dòng `todo` (backlog cạn cho nhóm đó), bỏ qua nhóm đó, KHÔNG lấy bù từ nhóm còn lại — để dành slot cho bước 2 dưới.
2. **Phần còn lại của cap 15** (tối đa 11 slot) theo logic cũ, loại trừ 4 dòng đã lấy ở bước 1:
   - Lấy `needs-enrich` priority thấp nhất (1 → 2 → 3) trước.
   - Hết `needs-enrich` thì lấy tiếp `todo` khác (không phân biệt tag) priority thấp nhất cho đủ 15.
3. Với mỗi card, theo quy trình pipeline 3 vai:
   - subagent **researcher** (Haiku): đọc card hiện tại (nếu enrich) hoặc note gợi ý trong backlog (nếu todo) + refs, bổ sung facts, đề xuất 2-4 links (verify slug tồn tại), bổ sung refs nếu yếu.
   - subagent **writer** (Sonnet): viết/mở rộng body lên 300-500 từ theo `scripts/content-pipeline/prompts/writer.md`.
     - Card enrich: giữ nguyên `front`/`back`/`level` cũ trừ khi sai rõ ràng.
     - Card todo tag `map:imagining`: đặt `level: 1`, category chính `perception` (kèm category phụ nếu hợp), giọng văn tập trung vào hiện tượng tri giác/ảo giác — không quy thành judgment bias.
     - Card todo tag `map:thinking`: đặt `level: 3`, category chính `mental-models` (kèm `theory`/`heuristic` nếu hợp), nội dung là framework/mô hình có cấu trúc, có bước áp dụng rõ ràng — không phải một bias đơn lẻ.
   - `npm run verify` sau mỗi card.
4. Brake: 2 card liên tiếp fail verify sau 2 vòng sửa → dừng vòng lặp, sang bước 3 với những card đã xong.

## Bước 3 — Regenerate artifacts

```bash
npm run verify && npm run graph && npm run mapdata && npm run build
```

`npm run build` là smoke test cuối. Fail → KHÔNG commit, báo cáo lỗi.

## Bước 4 — Cập nhật backlog cho ngày mai

```bash
npm run backlog
```

Chạy lại sau khi đã viết xong: card vừa đạt 300+ từ tự chuyển `done` → ngày mai không bị chọn lại.

## Bước 5 — Commit

```bash
git add -A
git commit -m "content: daily batch YYYY-MM-DD — N cards (enrich M, new K)"
```

Commit vào branch `new` (đã được duyệt cho job tự động — xem CLAUDE.md). **Không push, không merge sang master.**

## Bước 6 — Build

**Netlify là platform deploy production duy nhất** — tự chạy khi branch được push
(cấu hình trong `netlify.toml`). Job này KHÔNG push, nên nhắc trong báo cáo rằng cần push
để Netlify deploy.

Docker không có trong môi trường sandbox và cũng không phải đường deploy production
(chỉ dùng preview local) → không build image tại đây. `npm run build` ở bước 3 là smoke test đủ.

## Báo cáo cuối

Bảng: slug | loại (enrich/new/imagining/thinking) | words trước→sau | links thêm | verify.
Kèm: tổng số card, phân bố level sau batch, số node/edge của graph, trạng thái backlog
(todo / needs-enrich / done — tách riêng số dòng todo còn lại theo `map:imagining` /
`map:thinking` để biết còn bao nhiêu ngày sản xuất nữa trước khi backlog nhóm đó cạn),
commit hash. Ước tính chi phí nếu có `/cost`.
