---
name: daily-content
description: Job nội dung hàng ngày — sync backlog, viết/enrich 15 stuff card, regenerate graph + map data, cập nhật backlog, commit vào branch new. Dùng cho scheduled task hoặc khi muốn chạy một ngày sản xuất đầy đủ.
---

# Daily content job (15 cards/ngày)

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

Ưu tiên **enrich trước, card mới sau**:

1. Lấy 15 dòng `needs-enrich` priority thấp nhất (1 → 2 → 3), theo thứ tự trong backlog.
2. Nếu hết `needs-enrich`, lấy tiếp các dòng `todo` cho đủ 15.
3. Với mỗi card, theo quy trình pipeline 3 vai:
   - subagent **researcher** (Haiku): đọc card hiện tại + refs, bổ sung facts, đề xuất 2-4 links (verify slug tồn tại), bổ sung refs nếu yếu
   - subagent **writer** (Sonnet): viết/mở rộng body lên 300-500 từ theo `scripts/content-pipeline/prompts/writer.md`; giữ nguyên `front`/`back`/`level` của card cũ trừ khi sai rõ ràng
   - `npm run verify` sau mỗi card
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

Docker **không có** trong môi trường sandbox → không build image tại đây.
Thay vào đó: `npm run build` ở bước 3 đã xác nhận site build được; image Docker do CI dựng
(`.github/workflows/docker.yml`) khi branch `new` được push.
Nếu Docker khả dụng (chạy trên máy Núi), có thể chạy thêm: `docker compose build web`.

## Báo cáo cuối

Bảng: slug | loại (enrich/new) | words trước→sau | links thêm | verify.
Kèm: tổng số card, phân bố level sau batch, số node/edge của graph, trạng thái backlog
(todo / needs-enrich / done), commit hash. Ước tính chi phí nếu có `/cost`.
