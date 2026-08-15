---
name: new-card
description: Tạo stuff card mới qua content pipeline 3 vai (researcher → writer → verify). Dùng khi cần tạo card cho 1 concept, ví dụ "/new-card goodharts-law" hoặc "tạo card cho <concept>". Nếu không truyền concept, lấy từ backlog.
---

# New card pipeline

Tạo stuff card cho concept được truyền vào (argument sau /new-card).

1. Nếu không có concept: đọc `scripts/content-pipeline/backlog.csv`, lấy concept `todo` có priority cao nhất (số nhỏ = cao).
2. Dùng subagent **researcher** tạo research brief theo `scripts/content-pipeline/prompts/researcher.md`.
3. Dùng subagent **writer** viết `content/stuff/<slug>.md` từ brief, theo `scripts/content-pipeline/prompts/writer.md`.
4. Chạy `npm run verify` — nếu fail, yêu cầu writer sửa (tối đa 2 vòng, sau đó dừng và báo lỗi).
5. Cập nhật status trong backlog.csv thành `drafted`.
6. Báo cáo: slug, level, links, word count. KHÔNG tự commit — để human review qua PR.
