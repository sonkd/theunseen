---
title: "Spec — Flashcard layer (Hướng A / Jekyll)"
status: draft
owner: Tiểu Núi
updated: 2026-07-24
---

# Flashcard layer cho The Stuff Unseen — Spec (Hướng A)

> Mục tiêu: biến mỗi `stuff` thành flashcard học được, **không đổi tech stack** (giữ Jekyll + Tailwind + Netlify). Thêm 1 lớp UX + JS client-side, tái dùng toàn bộ nội dung hiện có.

## 1. Nguyên tắc thiết kế

- **Progressive enhancement**: trang `/stuff/:name/` hiện tại vẫn chạy nếu tắt JS. Study mode là lớp thêm.
- **Không backend**: tiến độ học lưu `localStorage`. Không cần tài khoản ở MVP.
- **1 nguồn sự thật**: nội dung thẻ nằm trong front matter của `my_collections/_stuff/*.md`. Study mode đọc qua feed JSON sinh lúc build.
- **Không phá SEO**: card lẻ vẫn được server-render như cũ.

## 2. Content model (schema thẻ)

Mở rộng front matter của `_stuff`, **tương thích ngược** (thiếu field mới thì fallback).

```yaml
---
title: "Anchoring"            # bắt buộc — mặt trước mặc định
front: "Vì sao con số đầu tiên bạn nghe lại 'ghim' phán đoán?"  # optional; fallback: title
back: "Xu hướng dựa quá mức vào thông tin đầu tiên khi ra quyết định."  # optional; fallback: conundrum → 1 đoạn đầu của content
strategy: "Đặt lại mốc; hỏi 'nếu không có con số này thì sao?'"  # optional
connected: ["Contrast effect", "Framing effect"]   # graph liên kết (đã có)
categories: ["Mental Models"]                      # đã có
tags: [decision, bias]                              # optional
difficulty: 2          # 1..3, phục vụ sắp thứ tự ôn; default 2
source: "https://en.wikipedia.org/wiki/Anchoring"  # optional; fallback: link "More information" trong content
image:                 # optional
published: true
---
Nội dung markdown dài (giữ nguyên) — hiển thị ở trang chi tiết.
```

**Quy tắc fallback (JS + Liquid):**

| Field | Nếu trống thì lấy |
|---|---|
| `front` | `title` |
| `back` | `conundrum` → nếu trống, `description` → nếu trống, đoạn text đầu của `content` |
| `strategy` | ẩn |
| `source` | link đầu tiên trong `content` |

> Ưu tiên nội dung: điền `front`/`back`/`strategy` cho ít nhất 1 category hoàn chỉnh trước khi ra mắt. Đây là giá trị lõi, không phải code.

## 3. Kiến trúc lớp flashcard

```
my_collections/_stuff/*.md      # nguồn dữ liệu (mở rộng schema)
        │  (Jekyll build, Liquid)
        ▼
assets/decks.json               # feed: mảng card {title, front, back, strategy, category, tags, connected, url, source, difficulty}
        │  (fetch lúc runtime)
        ▼
_pages/study.md  (/study/)  ──► assets/js/flashcards.js  ──► render flip cards + SRS (localStorage)
_includes/flashcard.html        # markup 1 thẻ (dùng lại cho card-of-the-day server-render)
_sass/articles/flashcards.scss  # style 3D flip (class thuần, tránh bị Tailwind purge)
```

**Vì sao render client-side từ JSON:** study mode cần shuffle, lọc deck, SRS xuyên nhiều thẻ — render động gọn hơn nhiều so với Liquid. Trang chi tiết SEO vẫn server-render nên không ảnh hưởng index.

## 4. Luồng UX

### 4.1 `/study/` — trung tâm học

- **Deck picker**: `All` + mỗi `category` + (tuỳ chọn) tag phổ biến. Đếm số thẻ mỗi deck.
- **Card of the day**: 1 thẻ deterministically theo ngày (hash ngày → index). Server-render để có SEO + share.
- **Study session**: chọn deck → vào chế độ lật thẻ.

### 4.2 Chế độ lật thẻ (study session)

- Mặt trước: `front`. Click / phím `Space` → lật hiện `back` + `strategy` + link nguồn + connected.
- Điều hướng: `←`/`→` hoặc nút Prev/Next; `S` shuffle; `1`=Cần ôn, `2`=Đã thuộc.
- **Progress bar**: đã xem / tổng; badge "Đã thuộc".
- Trạng thái lưu local, phục hồi khi quay lại.

### 4.3 Kết nối (Connect)

- Trong mặt sau, `connected[]` render thành link nhảy sang thẻ khác (trong session hoặc mở trang chi tiết).

## 5. SRS (SM-2 rút gọn) — Phase 1.5

Client-side, đủ dùng, không cần server.

```
mỗi card lưu: { ease: 2.5, interval: 0, due: <timestamp>, reps: 0, box }
- "Đã thuộc" (grade good): reps++; interval = reps==1?1 : reps==2?3 : round(interval*ease); due = now + interval*ngày
- "Cần ôn"  (grade again): reps=0; interval=0; ease = max(1.3, ease-0.2); due = now (ôn lại trong phiên)
Deck "Due today" = card có due <= hôm nay.
```

MVP có thể chỉ dùng 2 hộp `known/review` (Leitner 2-box); nâng lên SM-2 sau.

## 6. Lưu trữ localStorage (schema)

```json
key "su_flashcards_v1": {
  "cards": { "<slug>": { "box": "review|known", "ease": 2.5, "interval": 3, "due": 1690000000000, "reps": 2, "seen": true } },
  "lastDeck": "mental-models",
  "updatedAt": 1690000000000
}
```

- Versioned key để migrate an toàn. Có nút **Reset progress**.

## 7. Không phá vỡ (compat) & rủi ro

- Tailwind purge: markup do JS sinh **không** được Tailwind quét → dùng class thuần trong `flashcards.scss`, không phụ thuộc utility class runtime.
- Trùng dữ liệu codex (`.md` + `.yml`): ngoài phạm vi spec này; đề xuất chọn `.yml` làm nguồn (việc riêng).
- Thẻ chưa có `front/back`: vẫn hiển thị nhờ fallback → an toàn khi triển khai dần.

## 8. Definition of Done (MVP)

- [ ] `assets/decks.json` build ra JSON hợp lệ từ `site.stuff`.
- [ ] `/study/`: deck picker + Card of the day + chế độ lật thẻ chạy offline sau lần tải đầu.
- [ ] Flip (click + phím), shuffle, prev/next, mark Known/Review, progress bar.
- [ ] Trạng thái lưu `localStorage`, phục hồi sau reload; có Reset.
- [ ] `connected[]` click được.
- [ ] Điền `front/back/strategy` đầy đủ cho ≥ 1 category (vd Mental Models).
- [ ] Menu có "Study"; không lỗi layout ở các trang cũ.

## 9. Next steps sau MVP

1. SM-2 đầy đủ + deck "Due today".
2. Thống kê học (streak, số thẻ thuộc) — vẫn local.
3. (Chỉ khi cần tài khoản) đồng bộ đa thiết bị → lúc đó cân nhắc Hướng B/C.

## 10. Cách chạy & build

```bash
# CSS (Tailwind/PostCSS) + Jekyll
npm run dev            # nếu package.json có script build css
bundle exec jekyll serve --livereload
# mở http://localhost:4000/study/
```

> File này là spec sống — cập nhật khi schema/UX đổi.
