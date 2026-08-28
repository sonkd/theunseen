# Scheduled task — "Vẽ illustration cho các stuff"

Nguồn dữ liệu: `docs/theunseen_illustration_prompt_library.xlsx` · Skill: `editorial-geometric-illustration`
· Code: `scripts/illustrations/` (`illus.py` + `render_thumbs.py`).

**Cập nhật 2026-08-28** — đã chạy batch #3. Tiến độ 30/230. Xem mục F: nhật ký chạy.

---

## A. Prompt để dán vào scheduled task

> Vẽ illustration cho các stuff card chưa có ảnh trong repo `theunseen`, dùng skill
> `editorial-geometric-illustration` và thư viện prompt `docs/theunseen_illustration_prompt_library.xlsx`.
>
> **Bước 0 — preflight (bắt buộc, dừng ngay nếu fail):**
> 1. Xác nhận repo có mặt: `docs/theunseen_illustration_prompt_library.xlsx` và `scripts/illustrations/illus.py` phải tồn tại.
>    Nếu không → dừng, báo "repo chưa được mount", KHÔNG tạo file/commit nào.
> 2. Dependency: `pip install openpyxl cairosvg --break-system-packages` và `convert`/`montage` (ImageMagick).
>
> **Chọn batch (idempotent — bắt buộc):**
> 1. Đọc sheet `Article Index` (230 bài, mỗi bài đã gán sẵn `Hero shape`, `Hue`).
> 2. Bỏ qua mọi card đã có `public/assets/stuff/<slug>.png`. Lấy **10 card đầu tiên chưa có ảnh** theo cột `#`.
> 3. Không còn card nào thiếu ảnh → dừng, báo "đã phủ 100%", không commit.
>
> **Chẩn đoán metaphor trước khi vẽ (bắt buộc — đây là bước dễ bỏ nhất):**
> - Đọc field `back` của cả 10 card. Đối chiếu với bảng chẩn đoán idea shape ở Step 2 của skill.
> - Cột `Hero shape` trong xlsx **chỉ là điểm khởi đầu**, không phải kết luận: nó dồn ~58% corpus
>   vào `hierarchy` + `branching`. Batch #1 phải override 9/10. Coi việc override là mặc định, không phải ngoại lệ.
> - **Trong cùng một batch không được lặp metaphor.** 10 card cùng lúc mà 4 cái giống hệt nhau thì
>   thumbnail mất hết chức năng phân biệt. Trùng → chẩn đoán lại card yếu hơn.
> - Ghi override vào dict `OVERRIDES` trong `scripts/illustrations/render_thumbs.py` kèm **lý do**, rồi mới render.
>
> **Ưu tiên concept object (hướng B — xem mục G):** sau khi chẩn đoán idea shape, hỏi thêm
> *"có concept object nào biểu đạt đúng quan hệ này không?"*. Có → **dùng concept object**, vì nó cho
> silhouette đặc trưng, phân biệt tốt hơn hẳn ở 64px. Không → dùng idea shape rút gọn.
>
> **Vẽ (mỗi card 1 ảnh, artboard 128 → xuất PNG 512):**
> - `python3 scripts/illustrations/render_thumbs.py --limit 10`
> - Script dùng `THUMB_REGISTRY` trong `illus.py` (14 idea shape + 10 concept object = 24 hình) —
>   bản **rút gọn riêng cho khổ nhỏ**, không scale từ 400×400: ≤4 phần tử, stroke 1.6 (1.25% chiều rộng),
>   không mũi tên, không đường chấm, lề an toàn ≥12px.
> - Nền `paper` (trắng), tint ladder theo `Hue` của card (mint/amber). Không wordmark, không chữ.
> - Export `public/assets/stuff/<slug>.png` **512×512** (render 1024 → Lanczos 512) **và** `<slug>.svg`.
>   Ảnh này vừa là thumbnail 64px vừa là **ảnh minh hoạ chính của card** → 128 sẽ vỡ ở khổ lớn.
>   Đổi khổ: `--png-size N`.
> - Sửa metaphor sau khi đã render: `--only slug-a,slug-b` để render lại đúng các card đó.
>
> **Cập nhật content:** script tự set `image: /assets/stuff/<slug>.png` vào frontmatter, chèn ngay trước
> `published:`. Không đụng field nào khác.
>
> **Kiểm tra trước khi giao (bắt buộc):**
> - Contact sheet ở **cả hai** khổ, rồi **Read và thực sự nhìn**:
>   ```bash
>   cd public/assets/stuff
>   montage *.png -tile 5x -geometry +6+6 -background '#DDDDDD' /tmp/_contact.png
>   mkdir -p /tmp/r64 && for f in *.png; do convert "$f" -resize 64x64 /tmp/r64/"$f"; done
>   montage /tmp/r64/*.png -tile 5x -geometry +8+8 -background '#F5F5F5' /tmp/_contact64.png
>   ```
>   Khổ 64 mới là khổ hiển thị thật (`StuffThumb.astro`). Lỗi "hình bết" và "hai card trông giống nhau"
>   chỉ lộ ra ở khổ 64.
> - `npm run verify` PASS → `npm run graph && npm run mapdata && npm run build` xanh.
> - Checklist: không vật thể của *ví dụ* · concept object (nếu dùng) qua đủ 3 test ở mục G ·
>   stroke đồng đều · đúng 1 hue/card · không gradient/shadow/blur · không chữ ·
>   10 hình phân biệt được với nhau ở 64px.
>
> **Git:** branch `illustrations/<YYYY-MM-DD>`, commit, mở PR. **Không commit thẳng `master`.**
>
> **Báo cáo cuối:** bảng `slug | xlsx shape | metaphor dùng | hue | override?`, số card đã xử lý,
> số còn lại, link PR.

---

## B. Assumptions

- **A1 — Thumbnail-first.** Chỉ sinh **thumbnail 128×128** — đó là thứ site Astro thực sự render
  (`StuffThumb.astro` hiển thị 64×64, `object-fit: cover`, bo góc 8px). Hero 1200×630 + section 800×800
  trong xlsx là chuẩn blog/Substack, repo chưa có slot render → mục D.
- **A2 — Batch 10 card/lần.** 230 card → 23 lần chạy.
- **A3 — Branch + PR.** Không dùng ngoại lệ commit thẳng `new` (ngoại lệ đó chỉ cấp cho `daily-content`).
- **A4 — Hue theo xlsx** (mint 115 / amber 115). Không tự đổi.
- **A5 — Idempotent theo sự tồn tại của file PNG**, không theo frontmatter.
- **A6 — Metaphor KHÔNG theo xlsx một cách máy móc.** Xem mục C.
- **A7 — Môi trường chạy.** Task cần git branch + `npm run build` → chạy trong repo checkout
  (Claude Code / CI). Nếu chạy ở Cowork thì folder `theunseen` phải được kết nối trước; session
  scheduled không tương tác nên không xin quyền folder giữa chừng được.

---

## C. `Idea shape` (xlsx) → `metaphor` — và tại sao không được tin cột này

Ánh xạ tên 1-1 (xlsx dùng tên idea shape, `illus.py` dùng key REGISTRY):

| Idea shape (xlsx) | metaphor trong `illus.py` | Số lần dùng trong corpus |
|---|---|---|
| `hierarchy` | `hierarchy` | 201 |
| `branching` | `divergence` | 200 |
| `composition` | `page_structure` | 55 |
| `nesting` | `nested_scope` | 54 |
| `proportion` | `proportion` | 49 |
| `iteration` | `cycle` | 34 |
| `gradation` | `spectrum` | 27 |
| `convergence` | `funnel` | 19 |
| `traversal` | `coverage_sphere` | 15 |
| `contrast` | `contrast` | 14 |
| `system` | `network` | 12 |
| `strata` | `layers` | 5 |
| `tipping point` | `threshold` | 3 |
| `overlap` | `overlap_phases` | 2 |

Bảng này nằm sẵn trong `SHAPE_MAP` của `illus.py`.

**Vấn đề đã xác nhận bằng dữ liệu (batch #1):** `hierarchy` + `branching` chiếm ~58% corpus.
Trong 10 card đầu tiên, xlsx gán 5 `branching` + 4 `hierarchy` + 1 `system` — tức 9/10 card sẽ nhận
đúng 2 hình. Sau khi đọc `back` của từng card, **9/10 phải override**; không card nào trong batch
thực sự là quan hệ cha–con.

Kết luận: cột `Hero shape` là *design hypothesis* (README của chính xlsx ghi vậy), không phải kết quả
chẩn đoán. Coi nó như gợi ý hạng hai.

**Khuyến nghị (chưa làm):** sinh lại cột `Hero shape` bằng một pass đọc `back` + `categories` của
cả 230 card, ép phân bố về mức hợp lý hơn (không shape nào >15% corpus). Việc này bỏ được bước
override thủ công ở 22 batch còn lại. Ước tính: 1 lần chạy, ~230 lượt phân loại ngắn.

**Rủi ro còn lại — đụng hình ở cấp corpus.** 14 primitive cho 230 card → trung bình 16 card/hình.
Trên trang library/map, 16 thumbnail giống hệt nhau sẽ trông như lỗi. Hai hướng xử lý, chưa quyết:

1. Thêm biến thể xác định theo slug (xoay tam giác `network`, đổi góc lát cắt `proportion`,
   đổi số nấc `spectrum`) — giữ nguyên ngữ pháp, phá được sự trùng khít. Rẻ.
2. Mở rộng bộ primitive từ 14 lên ~24 bằng cách ghép đôi (`hierarchy` + `cycle`…) như Step 2 của skill
   cho phép. Đắt hơn, nhưng đúng hơn về mặt ngữ nghĩa.

---

## G. Concept object — hướng B (áp dụng từ 2026-08-27)

Bối cảnh & lý do: `docs/illustration-style-review.md`. Vấn đề gốc: 230 card chia nhau 14 idea shape
→ ~16 card dùng chung một hình, trên trang library trông như lỗi render.

**Nguyên tắc phân vai:** ảnh của card **không phải nơi dạy khái niệm** (không ai học được cơ chế từ
ô 64px) — nhiệm vụ của nó là **phân biệt & gợi nhớ**. Vì vậy lớp này được dùng *concept object*:
vật thể ẩn dụ nhưng **dựng bằng đúng bộ primitive hình học**, cùng stroke, một hue.

13 concept object hiện có (`CONCEPT_OBJECTS` trong `illus.py`, `CONCEPT_MEANING` giữ nghĩa từng cái):

| key | quan hệ nó biểu đạt |
|---|---|
| `mirror` | cùng một sự việc, hai cách quy kết (mình ↔ người khác) |
| `in_out_ring` | trong nhóm ↔ ngoài nhóm; ranh giới thuộc về |
| `balance` | đánh đổi, cán cân lệch có hướng |
| `beam` | chú ý dồn vào một điểm, phần còn lại tối đi |
| `halo_spill` | một ấn tượng lan sang các đánh giá lân cận |
| `veil` | thông tin bị che khuất chứ không phải không tồn tại |
| `fracture` | hai phần lẽ ra khớp nhau nhưng lệch — bất nhất |
| `pull` | một khối nặng kéo lệch toàn bộ phần còn lại |
| `echo` | lặp lại làm quen thuộc / khuếch đại dần |
| `gate` | sàng lọc: nhiều thứ tới, ít thứ qua |
| `rebound` | tác động bật ngược lại, kết quả đi ngược ý định ban đầu *(thêm ở batch #3)* |
| `odd_one_out` | một phần tử lệch khỏi nền đồng nhất — phân biệt nhờ tương phản *(thêm ở batch #3)* |
| `tail_event` | biến cố hiếm nhưng độ lớn áp đảo, nằm ngoài dải quen thuộc *(thêm ở batch #3)* |

**Ba test bắt buộc trước khi thêm concept object mới** — trượt một là loại:

1. **Quan hệ:** biểu đạt *quan hệ*, không phải đồ vật trong ví dụ. Hỏi: *"đổi ví dụ trong card →
   hình có còn đúng không?"* Không → loại.
2. **Icon sáo:** không người/bộ phận cơ thể, não, bóng đèn, kính lúp, bánh răng, điện thoại.
3. **Tuổi thọ:** không gắn trào lưu nhất thời hay chủ đề chế giễu (fidget spinner, UFO, flat-earth).

**Ba bẫy kỹ thuật đã gặp thật khi dựng — kiểm ngay:**

- *Nét mảnh biến mất ở 64px.* `<line>` 1.6px gần như tàng hình → thanh/trục phải dùng `<rect>` bo góc.
  (`balance` đã phải sửa vì lý do này.)
- *Bộ phận không chạm nhau đọc sai nghĩa.* Trụ cân không chạm đòn cân → hình đọc thành cần cẩu.
- *Trùng chất liệu với idea shape khác.* `pull` bản đầu là dãy tròn to dần → nhầm với `spectrum` ở 64px;
  phải đổi vệ tinh sang hình vuông và biến thiên theo *khoảng cách* thay vì *kích thước*.

**Đã áp dụng cho batch #1:** `actor-observer-bias` chuyển `contrast` → `mirror` (contrast chỉ nói
"hai thứ khác nhau", mirror nói được "cùng một sự việc, hai khung nhìn"); `anchoring` chuyển
`divergence` → `pull` (divergence thiếu mất *lực kéo*, vốn là bản chất của anchoring).

---

## D. Phase B (tuỳ chọn — chỉ chạy khi cần OG/social)

Repo chưa render hero/section. Khi cần OG image cho `/stuff/<slug>`:

- Sinh `public/assets/stuff/<slug>/hero.png` (1200×630, nền tint theo hue) từ `REGISTRY` (bản FULL 400×400)
  trong `illus.py`, dịch hình vào tâm khổ mới.
- Section 800×800 chỉ có nghĩa nếu xuất bản bản dài trên Substack/blog — Astro không dùng.
- Sheet `Image Prompts` có sẵn prompt từng dòng (690 dòng) nếu muốn dùng image-gen thay `illus.py`.

---

## E. Definition of Done (mỗi lần chạy)

- [ ] Đúng 10 card mới có `<slug>.png` + `<slug>.svg` trong `public/assets/stuff/` (không dôi ra).
- [ ] Mỗi card đã được chẩn đoán metaphor theo `back`, override ghi kèm lý do trong `OVERRIDES`.
- [ ] Không hai card nào trong batch dùng cùng một metaphor.
- [ ] Frontmatter `image` set đúng path nội bộ, không đụng field khác.
- [ ] Đã render contact sheet ở **cả 128 và 64** và **nhìn bằng mắt**.
- [ ] `npm run verify` PASS; `graph + mapdata` xanh; `build` xanh ở container/CI (không chạy được trong VM Cowork).
- [ ] Guard `!! TRÙNG BYTE` không báo cặp mới nào do batch này tạo ra.
- [ ] PR mở trên branch riêng kèm bảng báo cáo; `master` không bị chạm.

---

## F. Nhật ký chạy

| Batch | Ngày | Card | Branch | Ghi chú |
|---|---|---|---|---|
| #1 | 2026-08-26 | `abilene-paradox` → `apophenia` (10) | `illustrations/2026-08-26` | Dựng `scripts/illustrations/`. Override 9/10 khỏi xlsx. Sửa 3 thumb primitive: `cycle` (bản cũ đọc thành "con mắt"), `divergence` (kẻ mảnh biến mất ở 64px → chuyển sang phân múi bằng tint), `funnel` (đọc thành "ly rượu"). |
| #1b | 2026-08-27 | re-render 10 card | — | Áp hướng B: thêm 10 concept object (registry 14 → 24), PNG 128 → **512** (ảnh giờ kiêm ảnh minh hoạ chính). Đổi 2 metaphor: `actor-observer-bias` `contrast`→`mirror`, `anchoring` `divergence`→`pull`. |
| #2 | 2026-08-27 | `appeal-to-novelty` → `availability-heuristic` (10) | `illustrations/2026-08-27` | **Override 10/10.** xlsx gán 4 `hierarchy` + 5 `divergence` + 1 `cycle` — chỉ 1 ca (`argument-from-fallacy`) thực sự là hierarchy. Dùng 6 concept object + 4 idea shape, không lặp metaphor. Sửa `beam`: viền khép kín ở đáy khiến hình đọc thành **bình thí nghiệm** → bỏ nét đáy, chỉ giữ 2 cạnh xiên. |

| #3 | 2026-08-28 | `backfire-effect` → `bystander-effect` (10) | `illustrations/2026-08-28` | **Override 9/10** (chỉ `base-rate-fallacy` giữ xlsx). Thêm 3 concept object: `rebound`, `odd_one_out`, `tail_event` (registry 24 → 27). Thêm **guard trùng byte** vào `render_thumbs.py`. Sửa 1 card của batch #2: `appeal-to-probability-fallacy` `proportion` → `threshold`. |

**Tiến độ: 30/230 (13.0%) — còn 200 card.**

### Metaphor batch #3

| slug | xlsx shape | dùng | loại |
|---|---|---|---|
| backfire-effect | branching | `rebound` | concept object *(mới)* |
| bandwagon-effect | hierarchy | `pull` | concept object |
| barnum-effect | branching | `nested_scope` | idea shape |
| base-rate-fallacy | proportion | `proportion` | idea shape *(ca hiếm xlsx đúng)* |
| belief-bias | hierarchy | `fracture` | concept object |
| bias-blind-spot | branching | `balance` | concept object |
| bizarreness-effect | branching | `odd_one_out` | concept object *(mới)* |
| black-swan-theory | hierarchy | `tail_event` | concept object *(mới)* |
| bucket-error | hierarchy | `overlap_phases` | idea shape |
| bystander-effect | hierarchy | `divergence` | idea shape |

### Vấn đề trùng hình ở cấp corpus — đã đo được, chưa xử lý hết

Contact sheet 30 card ở khổ 64 cho thấy **4 cặp render ra ảnh trùng byte** (cùng metaphor + cùng hue):

| cặp | xử lý |
|---|---|
| `bias-blind-spot` == `actor-observer-bias` (mirror/amber) | đã đổi → `balance` |
| `bias-blind-spot` == `armchair-fallacy` (veil/amber, phương án trước đó) | đã đổi → `balance` |
| `base-rate-fallacy` == `appeal-to-probability-fallacy` (proportion/amber) | đã đổi card batch #2 → `threshold` |
| `ambiguity-effect` == `availability-heuristic` (spectrum/amber) | **còn tồn** |
| `anchoring` == `authority-bias` (pull/mint) | **còn tồn** |

Hue chỉ có 2 giá trị nên nó chỉ chia đôi không gian: với 27 hình, trần lý thuyết là 54 ảnh
phân biệt cho 230 card. Hai cặp còn tồn không có metaphor thay thế nào đủ sát ở hue tương ứng —
đây là bằng chứng thực nghiệm cho việc **phải chọn một trong hai hướng ở mục C** (biến thể theo
slug, hoặc mở rộng primitive) trước khi tới batch ~#8, chứ không thể xử lý từng ca một mãi.

Guard mới trong `render_thumbs.py` in cảnh báo `!! TRÙNG BYTE` sau mỗi lần render — không fail
build, nhưng không được bỏ qua khi mở PR.

### Metaphor batch #2

| slug | xlsx shape | dùng | loại |
|---|---|---|---|
| appeal-to-novelty | branching | `balance` | concept object |
| appeal-to-probability-fallacy | hierarchy | `proportion` | idea shape |
| argument-from-fallacy | hierarchy | `hierarchy` | idea shape *(ca hiếm xlsx đúng)* |
| armchair-fallacy | branching | `veil` | concept object |
| attentional-bias | hierarchy | `beam` | concept object |
| attribute-substitution | branching | `contrast` | idea shape |
| authority-bias | branching | `pull` | concept object |
| automation-bias | hierarchy | `gate` | concept object |
| availability-cascade | iteration | `echo` | concept object |
| availability-heuristic | branching | `spectrum` | idea shape |

Concept object đã giải đúng bài toán phân biệt: 6/10 card batch này dùng concept object, và
10/10 metaphor khác nhau — điều gần như không thể nếu chỉ có 14 idea shape.

### Bẫy đã gặp, đừng dẫm lại

- `--limit 10` đếm theo *card còn thiếu ảnh*, nên nếu render lại một card đã có ảnh thì batch sẽ
  kéo thêm card mới vào cho đủ 10. Muốn sửa metaphor của card đã render → dùng `--only`, đừng dùng `--limit`.
- Thư mục mount của Cowork có thể chặn `unlink`. File tạm phải ghi ra `/tmp`, không ghi vào `public/`.
- `npm run build` **không chạy được qua `device_bash` của Cowork**. Nguyên nhân thật (xác định ở
  batch #3): `device_bash` chạy trong một VM **Linux**, còn `node_modules` trong repo là bản cài
  trên **macOS** → `Cannot find module '@rolldown/binding-wasm32-wasi'`. Đừng chạy `npm install`
  trong VM đó để "sửa" — nó sẽ ghi đè `node_modules` của máy thật bằng binary Linux.
  Cách kiểm tra build đúng: clone repo vào container/CI, `npm ci`, `npm run build`.
  `verify` + `graph` + `mapdata` chạy bình thường trong VM.
- **Frontmatter `image:` từng bị revert ngoài phiên** (cả `CLAUDE.md` và docs cũng vậy). Sau mỗi batch
  phải kiểm: `grep -h "^image:" content/stuff/*.md | wc -l` bằng đúng số PNG trong `public/assets/stuff/`.
  Lệch → chạy lại `set_frontmatter_image` cho các slug thiếu.
- **Trùng byte giữa các card là lỗi im lặng.** Hai card cùng metaphor + cùng hue cho ra ĐÚNG một
  file PNG. Không nhìn ra được nếu chỉ soi contact sheet của riêng batch — phải chạy guard md5 trên
  toàn bộ `public/assets/stuff/`. Sửa bằng cách đổi metaphor, không đổi hue (hue do xlsx quy định).
- Hình khép viền kín dễ bị đọc thành **đồ vật** ngoài ý muốn (`beam` → bình thí nghiệm,
  `funnel` → ly rượu). Khi hình mô tả *luồng/tia*, để hở đầu mở — đừng đóng path bằng `Z` có stroke.
