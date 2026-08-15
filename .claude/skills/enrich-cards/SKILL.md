---
name: enrich-cards
description: Enrich N legacy cards có body ngắn (mặc định 5, hard cap 10) - mở rộng body lên 300-500 từ, thêm links. Dùng khi cần nâng cấp cards migrate từ Jekyll, ví dụ "/enrich-cards 5" hoặc "/enrich-cards 5 bias" (lọc theo category).
---

# Enrich legacy cards

Enrich N card (argument 1; mặc định 5, KHÔNG quá 10). Argument 2 (optional): lọc theo category.

1. Chạy `npm run verify`, lấy danh sách card có warning word-count. Nếu có filter category: chỉ giữ card thuộc category đó. Ưu tiên card đang có nhiều links nhất (hub nodes trước).
2. Với mỗi card:
   - Subagent **researcher**: đọc card hiện tại + refs có sẵn, bổ sung facts (thí nghiệm gốc, tác giả, tranh cãi/replication nếu có), đề xuất 2-4 links mới từ graph (verify slug tồn tại), bổ sung refs nếu nguồn hiện tại yếu.
   - Subagent **writer**: mở rộng body lên 300-500 từ theo cấu trúc trong prompts/writer.md. GIỮ NGUYÊN front/back/level hiện có (chỉ sửa nếu sai rõ ràng — báo cáo lại). Thêm `strategy` nếu chưa có.
3. `npm run verify` sau mỗi card; 2 card liên tiếp fail → dừng (no-progress brake).
4. Kết thúc: `npm run graph`, tổng kết bảng (slug | words trước→sau | links thêm | verify). KHÔNG tự commit.
