# Seeing the Unseen — Đánh giá ý tưởng & Build Plan

> Website chia sẻ kiến thức (bias, cognitive behavior, psychology) dưới dạng "stuff" — mỗi stuff là một đốm lửa trên bản đồ hang động Plato, mở bằng flip card.

**English summary:** A knowledge-sharing site where each concept ("stuff") is a flame on a Pokémon-style map structured after Plato's Cave. Cards flip front/back, link into a knowledge graph, and the fog-of-war reveals content as the reader explores. Recommended stack: Astro + MDX (content-as-git) + Kaplay map engine + Obsidian as CMS, fully static, Docker/nginx deploy.

---

## Phần 1 — Đánh giá ý tưởng

### 1.1 Điểm mạnh (giữ nguyên)

- **Metaphor nhất quán từ đầu đến cuối**: hang động Plato → 4 chặng nhận thức → nhân vật ngọn lửa → fog-of-war. Đây là điểm khác biệt lớn nhất so với các site liệt kê bias (thedecisionlab, coglode) — họ có nội dung tốt nhưng trải nghiệm là "danh mục", còn đây là "hành trình".
- **Flip card khớp cơ chế học**: mặt trước là câu hỏi, mặt sau là khái niệm — đúng cấu trúc active recall / retrieval practice, hiệu quả hơn đọc thụ động.
- **Graph qua `links` + `categories`**: nội dung mental models vốn liên kết chằng chịt; cấu trúc graph phản ánh đúng bản chất domain.
- **Content-as-Markdown + Obsidian làm CMS**: chi phí vận hành bằng 0, versioning qua git, không vendor lock-in.

### 1.2 Vấn đề cần sửa (theo mức độ ảnh hưởng)

**V1. "5 Map chính" nhưng chỉ liệt kê 4.**
Divided Line của Plato có 4 phân đoạn: Imagining → Belief → Thinking → Intelligence/Knowledge, cộng đích đến là **The Good (Mặt trời)**. Đề xuất: 4 map chính + 1 map kết "The Sun" — không chứa stuff, là màn hình tổng kết hành trình (% khám phá, graph toàn cảnh). Vừa đúng triết học, vừa có "ending" như game.

**V2. Trường `level` đang neo vào figure "Level of mind" — rubric chưa vận hành được.**
Figure đính kèm (Perception/Thinking/Emotion) là trục cảm xúc–tốc độ, khó map 1-1 sang độ khó nội dung. Đề xuất rubric 4 mức khớp luôn với 4 map — một trường phục vụ cả phân loại lẫn vị trí trên bản đồ:

| Level | Map | Loại nội dung | Ví dụ |
|---|---|---|---|
| 1 | Imagining | Hiện tượng bề mặt, ảo giác tri giác | Optical illusions, priming |
| 2 | Belief | Bias & heuristics cá nhân/nhóm | Abilene paradox, anchoring |
| 3 | Thinking | Framework, mental models có cấu trúc | Cognitive load, Bayes thinking |
| 4 | Knowledge | Meta-cognition, lý thuyết nền | Dual-process theory, epistemology |

**V3. Map-first navigation gây rủi ro findability và SEO.**
Nếu map là cách duy nhất tiếp cận nội dung: người quay lại tìm 1 card cụ thể sẽ khó, Google không index được nội dung render trong canvas, mobile khó thao tác. Wireframe của bạn đã có Search / Daily / Favorites — đúng hướng. Chốt kiến trúc **dual-mode**:

- *Explore mode* (map, canvas): trải nghiệm chính, discovery.
- *Library mode* (list + search + filter category/level): mỗi stuff là một **trang HTML tĩnh có URL riêng** (`/stuff/abilene-paradox`). Map chỉ là lớp trình diễn phía trên; SEO, share link, accessibility đều chạy trên trang tĩnh.

**V4. Bản quyền nội dung.**
The Decision Lab, Coglode, Psychology Today là nội dung có bản quyền (Coglode là sản phẩm trả phí). Wikipedia là CC BY-SA. Quy tắc: chỉ dùng các nguồn làm **tài liệu tham khảo trong `refs`**, phần mô tả 300–500 từ phải là bản viết lại của bạn. Không scrape. Đây là điều kiện để site tồn tại lâu dài.

**V5. Icon random làm mất khả năng scan.**
Icon nên mang nghĩa: map theo `categories` (ví dụ ▲ = Bias, ● = Mental Model, ✦ = Theory, ☾ = Perception...). Người dùng học được ngôn ngữ hình ảnh sau vài phút thay vì nhiễu ngẫu nhiên.

### 1.3 Cải thiện đề xuất thêm (giá trị cao, chi phí thấp)

- **Fog-of-war = progression có trạng thái**: stuff đã mở lưu vào `localStorage` → vùng đó "sáng vĩnh viễn". Hang động sáng dần theo hành trình người đọc — đây là retention hook chính, đúng metaphor "flames". Hiển thị "12/58 flames lit" mỗi map.
- **Daily flame**: mỗi ngày highlight 1 stuff (đã có trong wireframe) — lý do quay lại hằng ngày, về sau có thể nâng thành spaced repetition.
- **Graph view** (Obsidian-style, dùng d3-force) ở The Sun map hoặc trang riêng — biến `links` thành trải nghiệm nhìn thấy được.
- **Đo lường từ ngày 1** (self-host, không cookie): cards flipped/session, % explored, return rate, search queries không có kết quả (= content gap). *Giả định các chỉ số này là KPI; nếu bạn có mục tiêu khác (newsletter, cộng đồng) cần bổ sung.*

---

## Phần 2 — Build Plan

### 2.1 Giả định (nếu sai, điều chỉnh plan)

- Solo builder, làm ngoài giờ; ưu tiên chi phí vận hành ~0 và ship sớm.
- Giai đoạn 1 không cần tài khoản người dùng, comment, hay backend động (progress lưu localStorage là đủ).
- Nội dung song ngữ kiểu hiện tại (câu hỏi tiếng Việt, định nghĩa tiếng Anh), chưa cần i18n framework.
- Bạn thoải mái với git + Markdown (đã dùng Obsidian). Doc gốc có syntax Jekyll (`{{site.baseurl}}`) — giả định site Jekyll cũ sẽ được migrate, không duy trì song song.

### 2.2 Chọn tech stack — 3 phương án

| | A. Astro static (khuyến nghị) | B. Next.js + Payload CMS | C. Jekyll (giữ nền cũ) |
|---|---|---|---|
| Content | MDX + Content Collections (schema validate bằng Zod) | Postgres + Payload admin UI | Markdown + Liquid |
| CMS | Obsidian vault = source of truth, commit qua git | Web admin UI | Obsidian + git |
| Database | Không cần (graph build-time) | Postgres | Không |
| Map engine | Kaplay (island component) | Kaplay | Khó nhúng sạch |
| Search | Pagefind (static, build-time) | API route | Lunr.js |
| Hosting | Static — Cloudflare Pages/nginx, ~$0 | VPS ~$5–10/tháng | GitHub Pages |
| Phù hợp khi | Solo, content-driven, ship nhanh | Cần accounts/sync progress cross-device | Muốn đổi ít nhất |

**Khuyến nghị: Phương án A.** Lý do: toàn bộ tính năng giai đoạn 1 không cần server; Astro cho phép trang tĩnh SEO-friendly + "island" canvas tương tác trong cùng một trang — đúng kiến trúc dual-mode ở V3; frontmatter của bạn gần như dùng được nguyên trạng. Phương án B chỉ đáng giá khi cần user accounts — có thể migrate sau vì content vẫn là Markdown. Phương án C loại vì nhúng map engine và validate schema đều khó.

**Stack chi tiết (toàn bộ open-source):**

- **Astro 5** — static site, content collections, MDX
- **Kaplay** (kế thừa Kaboom.js, MIT) — map engine 2D tile-based; đủ cho tilemap + sprite + input, nhẹ hơn Phaser
- **Tiled Map Editor** — vẽ 4 map, export JSON
- **Pagefind** — full-text search tĩnh
- **d3-force** — graph view
- **Zod** — validate frontmatter khi build (fail CI nếu `links` trỏ tới stuff không tồn tại)
- **Umami** (self-host) hoặc **Plausible CE** — analytics không cookie
- **Docker + nginx** — serve static build; Umami chạy container riêng

### 2.3 Content schema (chuẩn hoá từ template của bạn)

```yaml
---
title: "Abilene paradox"
slug: "abilene-paradox"          # URL + id để links tham chiếu
front: "'Abilene paradox' là gì, và nó tác động thế nào đến quyết định của bạn?"
back: "A group collectively decides on a course of action counter to the preferences of most members."
level: 2                          # 1-4, rubric ở V2 — quyết định stuff nằm ở map nào
map_position: { x: 12, y: 34 }   # tile coords; bỏ trống = auto-place khi build
icon: "▲"                        # derive từ category chính nếu bỏ trống
categories: ["mental-models", "bias"]
links: ["groupthink", "conformity-bias"]   # slug, không phải title — tránh gãy khi đổi tên
refs:
  - "https://en.wikipedia.org/wiki/Abilene_paradox"
approaches:                       # đổi từ URL rời → object có title để render đẹp
  - { title: "Case study: sprint planning", url: "..." }
published: true
image: "..."
---

Đoạn giới thiệu 300–500 từ...
```

Thay đổi so với template gốc: thêm `slug` làm khoá tham chiếu; `links` dùng slug thay vì title; `level` theo rubric 1–4; thêm `map_position` (optional); `approaches` thành object. Build script sẽ generate `graph.json` (nodes + edges) và `map-data.json` cho Kaplay từ toàn bộ frontmatter.

### 2.4 Cấu trúc repo

```
theunseen/                    # branch "new" — đã scaffold
├── CLAUDE.md                 # quy tắc dự án cho AI agents (schema, giọng văn, no-scrape, verify-trước-commit)
├── .claude/
│   ├── agents/               # researcher.md (Haiku), writer.md (Sonnet)
│   └── commands/             # /new-card, /batch-cards
├── content/                  # Obsidian vault — mở trực tiếp bằng Obsidian
│   ├── stuff/                # 181 cards migrate từ Jekyll + cards mới; filename = slug
│   └── approaches/           # bài case study/ứng dụng
├── scripts/
│   ├── build-graph.mjs       # frontmatter → public/graph.json
│   └── content-pipeline/     # phương án B: backlog.csv, prompts/, verify.mjs
├── src/
│   ├── content.config.ts     # Zod schema (astro:content)
│   ├── pages/                # index (map Phase 2), library, stuff/[slug]
│   ├── components/           # FlipCard.astro; MapCanvas Phase 2
│   └── lib/icons.ts          # icon theo category — không random
├── maps/                     # Tiled JSON: imagining, belief, thinking, knowledge, sun (Phase 2)
├── docs/                     # build-plan.md, agent-workflow-guide.md
├── Dockerfile                # build Astro → nginx:alpine
├── docker-compose.yml        # web + umami + umami-db
└── .github/workflows/ci.yml  # verify → graph → build
```

`docker-compose.yml` tối giản: service `web` (nginx serve `dist/`), `umami` + `postgres` cho analytics. Dev không cần Docker — `npm run dev` là đủ; Docker phục vụ deploy VPS hoặc self-host.

### 2.5 Content pipeline — Phương án B (đã chốt, nằm trong Phase 0)

Pipeline 3 vai model-tiered, chi tiết vận hành trong `docs/agent-workflow-guide.md`:

- **Researcher** (subagent Haiku): fetch refs, đề xuất level/categories, link prediction từ graph hiện có
- **Writer** (subagent Sonnet): viết card từ brief + 3–5 card liên quan làm context
- **Verifier** (`scripts/content-pipeline/verify.mjs`, code, $0): schema, link integrity, word count — chạy trước mọi LLM judge
- Commands: `/new-card`, `/batch-cards` (hard cap 10/run, no-progress brake); human review qua PR
- Chi phí mục tiêu: vài cent/card; 60 card mới < $10

### 2.6 Roadmap theo phase

**Phase 0 — Nền móng (✅ hoàn thành)**
Checkpoint Jekyll vào git history; migrate **181 stuff cards** sang schema mới (0 link gãy); scaffold Astro 5 + content collections + Zod; `scripts/content-pipeline/` + `.claude/` agents/commands + CLAUDE.md; CI verify→graph→build; Dockerfile + docker-compose (web + Umami).
*DoD đạt: verify PASS trên 181 cards; build render 181 trang stuff có URL riêng.*

**Phase 0.5 — Enrich legacy content (song song các phase sau)**
181 cards migrate có body ngắn (warning < 100 từ). Dùng `/batch-cards` enrich dần lên 300–500 từ, ưu tiên cards có nhiều links.
*DoD: 0 warning word-count; mỗi card ≥ 1 ref thật.*

**Phase 1 — Card & Library (tuần 2–3)**
FlipCard component (flip 2 mặt, refs, approaches, related links), library view + filter category/level, Pagefind search, layout theo wireframe 2 của bạn.
*DoD: đủ luồng đọc hoàn chỉnh trên mobile + desktop không cần map; Lighthouse ≥ 90.*

**Phase 2 — Map & Fog-of-war (tuần 4–6)**
Vẽ 4 map bằng Tiled (style Pokemon như ảnh 3), Kaplay island: nhân vật ngọn lửa, di chuyển bằng nút ◀ ▶ + phím, fog-of-war theo bán kính đuốc, click stuff → mở FlipCard modal, localStorage progression, map "The Sun" + graph view.
*DoD: đi hết 4 map, mở card từ map, vùng đã khám phá sáng vĩnh viễn sau reload; map degrade về library trên thiết bị không hỗ trợ.*

**Phase 3 — Retention & đo lường (tuần 7–8)**
Daily flame, favorites, Umami events (card_flip, map_explore_pct, search_no_result), OG image cho share, RSS.
*DoD: dashboard trả lời được "bao nhiêu % khách flip ≥ 3 card/session".*

**Phase sau (backlog):** spaced repetition, user accounts + sync progress (lúc đó cân nhắc lại phương án B), đóng góp cộng đồng qua PR.

### 2.7 Bước tiếp theo ngay

1. `npm install && npm run dev` — kiểm tra site chạy local với 181 cards.
2. Mở session mới trong VS Code Agents, chạy thử `/new-card goodharts-law` — kiểm tra pipeline end-to-end.
3. Review PR đầu tiên, đo chi phí thực tế/card, hiệu chỉnh prompts nếu cần.

---

## Definition of Done (toàn dự án, giai đoạn 1)

- [ ] 40–60 stuff published, phủ đều 4 level
- [ ] Dual-mode hoạt động: map (explore) + library (search/SEO)
- [ ] Mỗi stuff có URL tĩnh, index được, share được
- [ ] Progression lưu local, hang động sáng dần theo người đọc
- [ ] Analytics tự host, đo được flip rate và % explored
- [ ] 100% nội dung là bản viết lại có refs, không scrape
