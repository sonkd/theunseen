---
description: Chạy batch tối đa N card từ backlog (mặc định 5, hard cap 10)
---

Chạy content pipeline theo batch: $ARGUMENTS card (mặc định 5, không bao giờ quá 10 — hard cap chi phí).

Với mỗi concept status=todo trong `scripts/content-pipeline/backlog.csv` (theo priority):
lặp lại quy trình của /new-card. Dừng khi: đủ N card, hoặc backlog hết todo, hoặc 2 card liên tiếp fail verify (no-progress brake).

Kết thúc: chạy `npm run verify` + `npm run graph`, tổng kết bảng (slug | level | words | verify) và nhắc human mở PR review.
