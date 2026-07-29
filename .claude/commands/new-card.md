---
description: Tạo stuff card mới qua pipeline 3 vai (researcher → writer → verify)
---

Tạo stuff card cho concept: $ARGUMENTS

1. Nếu $ARGUMENTS trống: đọc `scripts/content-pipeline/backlog.csv`, lấy concept `todo` có priority cao nhất.
2. Dùng subagent **researcher** tạo research brief cho concept.
3. Dùng subagent **writer** viết `content/stuff/<slug>.md` từ brief.
4. Chạy `npm run verify` — nếu fail, yêu cầu writer sửa (tối đa 2 vòng).
5. Cập nhật status trong backlog.csv thành `drafted`.
6. Báo cáo: slug, level, links, word count, chi phí ước tính. KHÔNG tự commit — để human review.
