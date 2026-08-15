---
name: batch-cards
description: Chạy batch content pipeline cho N card từ backlog (mặc định 5, hard cap 10). Dùng khi cần sản xuất nhiều stuff cards một lượt, ví dụ "/batch-cards 5" hoặc "chạy batch 5 card".
---

# Batch cards pipeline

Chạy pipeline theo batch: N card (argument sau /batch-cards; mặc định 5; KHÔNG BAO GIỜ quá 10 — hard cap chi phí).

Với mỗi concept status=todo trong `scripts/content-pipeline/backlog.csv` (theo priority tăng dần):
thực hiện đúng quy trình của skill new-card (researcher → writer → verify → cập nhật backlog).

Điều kiện dừng: đủ N card, hoặc backlog hết todo, hoặc 2 card liên tiếp fail verify sau 2 vòng sửa (no-progress brake).

Kết thúc: chạy `npm run verify` + `npm run graph`, tổng kết bảng (slug | level | words | verify) và nhắc human mở PR review. KHÔNG tự commit/merge.
