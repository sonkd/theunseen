# design/ — bản thiết kế gốc (reference, không build)

Thư mục chứa file thiết kế nguồn để các session UI tham chiếu pixel-chính-xác.
Astro KHÔNG build thư mục này (nằm ngoài src/ và public/).

## Cần có

- `The-Unseen.dc.html` — prototype từ Claude Design
  (https://claude.ai/design/p/f3202e75-7d70-4ba7-aecd-5d048459ee9d, file `The Unseen.dc.html`)

## Cách lấy file

1. Mở link design ở trên.
2. Menu file (dropdown cạnh tên project "The Unseen") → **Download** / hoặc **Share → Download code**.
3. Lưu vào thư mục này, đổi tên thành `The-Unseen.dc.html`.

Nếu chưa có file: dùng `docs/design-spec.md` — đã trích sẵn toàn bộ token quan trọng
(5 palette map nguyên văn, typography, layout, hằng số hành vi) từ prototype.
Spec đó đủ để implement; file HTML chỉ giúp đối chiếu chi tiết render.

## Quy tắc

- File trong đây là **read-only reference**. Không import vào src/.
- Khi bản design trên Claude được cập nhật: tải lại file, đồng thời cập nhật
  `docs/design-spec.md` và `docs/design-reconciliation.md`.
