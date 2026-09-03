---
name: daily-content
description: Job nội dung hàng ngày — sync backlog, sản xuất ĐÚNG 3 card cho mỗi map trong 5 map (Imagining, Belief, Thinking, Intelligence, Knowledge) = 15 card/ngày, regenerate graph + map data, cập nhật backlog, commit vào branch new. Dùng cho scheduled task hoặc khi muốn chạy một ngày sản xuất đầy đủ.
---

# Daily content job (15 cards/ngày — hạn ngạch cứng 3 card × 5 map)

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

## Bước 2 — Sản xuất 15 card = 3 card × 5 map

**Hạn ngạch theo map là RÀNG BUỘC CỨNG, không phải gợi ý.** Mỗi map lấy đúng 3 card, không hơn.
Tuyệt đối KHÔNG dùng priority toàn cục để chọn card — priority chỉ dùng để sắp thứ tự curated
*bên trong* một map. Đây là lỗi của phiên bản rule cũ: vì priority của Imagining (41–70) luôn
nhỏ hơn Thinking (81–110), mọi slot dư đều rơi vào Imagining và batch 2026-08-27 ra 13 Imagining
+ 2 Thinking dù rule tự mô tả là "cân bằng".

### 2.1 — Hạn ngạch cơ bản

Với **từng** tag dưới đây, lọc `status=todo` rồi lấy **3 dòng priority thấp nhất trong chính tag đó**
(thứ tự curated, KHÔNG đảo, KHÔNG trộn giữa các tag):

| Map | tag trong `notes` | level bắt buộc | dải priority curated |
|---|---|---|---|
| 1 Imagining | `map:imagining` | `level: 1` | 41–70 |
| 2 Belief | `map:belief` | `level: 2` | (chưa seed) |
| 3 Thinking | `map:thinking` | `level: 3` | 81–110 |
| 4 Intelligence | `map:intelligence` | `level: 4` | 121–150 |
| 5 Knowledge | `map:knowledge` | `level: 5` | 161–190 |

### 2.2 — Khi một map cạn backlog

Nếu một map có ít hơn 3 dòng `todo`, lấy hết phần còn lại của map đó, rồi **chia lại số slot thiếu
theo vòng tròn (round-robin)** cho các map vẫn còn `todo`, theo thứ tự map 1 → 2 → 3 → 4 → 5,
mỗi vòng cấp thêm 1 slot cho một map. Cách này giữ tổng 15 mà không để map nào nuốt hết phần dư.

Nếu tổng số dòng `todo` toàn backlog < 15 thì làm hết số có và báo cáo — KHÔNG bịa concept mới,
KHÔNG hạ chuẩn để lấp cho đủ 15.

### 2.3 — Enrich

`needs-enrich` (body < 300 từ) KHÔNG còn nằm trong cap 15. Nếu có dòng `needs-enrich`, báo cáo số
lượng ở cuối và đề xuất chạy `/enrich-cards` riêng — không trộn vào hạn ngạch map, vì trộn vào
chính là thứ làm hỏng phân bổ trước đây.

### 2.4 — Pipeline cho từng card

Với mỗi card, theo quy trình pipeline 3 vai:
   - subagent **researcher** (Haiku): đọc card hiện tại (nếu enrich) hoặc note gợi ý trong backlog (nếu todo) + refs, bổ sung facts, đề xuất 2-4 links (verify slug tồn tại), bổ sung refs nếu yếu.
   - subagent **writer** (Sonnet): viết/mở rộng body lên 300-500 từ theo `scripts/content-pipeline/prompts/writer.md`.
     - Card enrich: giữ nguyên `front`/`back`/`level` cũ trừ khi sai rõ ràng.
     - Card tag `map:imagining`: `level: 1`, category chính `perception`. Nội dung là hiện tượng tri giác/ảo giác/priming — KHÔNG quy thành judgment bias.
     - Card tag `map:belief`: `level: 2`, category chính `bias` (kèm `social`/`memory` nếu hợp). Nội dung là thiên lệch ở cấp cá nhân/nhóm.
     - Card tag `map:thinking`: `level: 3`, category chính `mental-models` (kèm `theory`/`heuristic` nếu hợp). Nội dung là framework/mô hình có cấu trúc, có bước áp dụng rõ ràng — không phải một bias đơn lẻ.
     - Card tag `map:intelligence`: `level: 4`, category chính `theory` (kèm `mental-models` nếu hợp). Nội dung là **siêu nhận thức và nhận thức luận ứng dụng** — cách kiểm tra, hiệu chỉnh, cập nhật chính tư duy của mình (biết mình biết gì, độ tự tin có khớp thực tế không, bằng chứng nào đủ mạnh). KHÔNG phải một framework ra quyết định (đó là Thinking), cũng KHÔNG phải một lý thuyết nền mô tả cách trí óc vận hành (đó là Knowledge).
     - Card tag `map:knowledge`: `level: 5`, category chính `theory`. Nội dung là **lý thuyết nền mô tả cơ chế của nhận thức/quyết định** — thứ mà các bias và framework tầng dưới đứng trên (mẫu chuẩn: `dual-process-theory`, `prospect-theory`, `map-is-not-the-territory`). Viết ở tầng giải thích cơ chế, không phải mẹo áp dụng.
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

**Repo này có nhiều worktree.** Branch đang được checkout KHÔNG chắc là `new` — nó phụ thuộc vào
phiên làm việc trước đó. Commit thẳng mà không kiểm tra sẽ rơi vào `master`, vi phạm CLAUDE.md §5
quy tắc 6. Sự cố 2026-09-03: batch 25 card commit nhầm vào `master`, và chuỗi lệnh khắc phục
(`git branch -f new HEAD` → fail vì branch đang checkout → các lệnh sau vẫn chạy) đã amend nhầm lên
tip của `origin/new` rồi tua `new` lùi 1 commit. Không mất dữ liệu nhưng mất một buổi để gỡ.

### 5.1 — Gate bắt buộc: phải đứng trên `new` mới được commit

Chạy nguyên khối này. Mỗi lệnh tự dừng nếu fail — KHÔNG bỏ qua lỗi để chạy tiếp lệnh sau.

```bash
git worktree list                      # ghi vào báo cáo: có worktree nào khác đang giữ branch nào
git rev-parse --verify new >/dev/null || { echo "FAIL: branch new không tồn tại"; exit 1; }
git switch new                         || { echo "FAIL: không chuyển được sang new"; exit 1; }
[ "$(git branch --show-current)" = "new" ] || { echo "FAIL: không ở trên new"; exit 1; }
```

Nếu bất kỳ dòng nào in `FAIL` → **DỪNG, KHÔNG commit**, báo cáo nguyên văn output và trạng thái
`git status` + `git branch -vv`. Nguyên nhân thường gặp: một worktree khác đang giữ `new`
(`git switch` sẽ từ chối), hoặc working tree bẩn.

### 5.2 — Commit

```bash
git add -A
git commit -m "content: daily batch $(date +%F) — N cards (enrich M, new K)"
git log --oneline -1                   # xác nhận commit nằm đúng trên new
git branch -vv | grep -E '^\* new'     # xác nhận new ahead, master không đổi
```

`N` phải là số card THỰC TẾ sản xuất, đếm bằng
`git show --stat --oneline HEAD | grep -c 'content/stuff'` — không ghi theo hạn ngạch dự kiến.

**Không push, không merge sang master.** Nếu phát hiện commit đã lỡ vào nhánh sai, KHÔNG tự khắc
phục bằng `git branch -f` hay `git reset --hard`: báo cáo và để người thật xử lý, vì cả hai lệnh đó
hành xử khác nhau tùy worktree đang giữ branch nào.

## Bước 6 — Build

**Netlify là platform deploy production duy nhất** — tự chạy khi branch được push
(cấu hình trong `netlify.toml`). Job này KHÔNG push, nên nhắc trong báo cáo rằng cần push
để Netlify deploy.

Docker không có trong môi trường sandbox và cũng không phải đường deploy production
(chỉ dùng preview local) → không build image tại đây. `npm run build` ở bước 3 là smoke test đủ.

## Báo cáo cuối

**Dòng đầu tiên của báo cáo, bắt buộc:** branch đã commit (`git branch --show-current`), commit hash,
và output `git worktree list`. Nếu không commit được thì nêu rõ lý do ở đúng chỗ này thay vì chôn
xuống cuối. Đây là chốt kiểm để phát hiện ngay commit rơi nhầm nhánh.

Bảng: slug | map (imagining/belief/thinking/intelligence/knowledge) | words | links | verify.

**Bảng kiểm hạn ngạch — bắt buộc có trong mọi báo cáo:** liệt kê số card thực tế sản xuất cho từng
map trong 5 map. Nếu map nào khác 3, phải nêu rõ lý do (cạn backlog → đã chia lại bao nhiêu slot cho
map nào). Đây là chốt kiểm để phát hiện ngay lệch phân bổ, thay vì để lệch âm thầm tích lũy.

Kèm: tổng số card, phân bố level 1–5 sau batch, số node/edge của graph, trạng thái backlog
(todo / needs-enrich / done — **tách riêng số dòng `todo` còn lại theo từng tag map**, kèm ước tính
số ngày sản xuất còn lại của mỗi map ở nhịp 3 card/ngày, để thấy sớm map nào sắp cạn), commit hash.
Ước tính chi phí nếu có `/cost`.
