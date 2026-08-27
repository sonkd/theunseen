# Review: bộ card tham chiếu vs `editorial-geometric-illustration`

Phân tích 10 flashcard bias (line-art) do người dùng cung cấp, đối chiếu với skill hiện tại và `scripts/illustrations/illus.py` (14 primitive, batch #1 đã render 10 thumbnail).

**Kết luận ngắn:** bộ card đó **vi phạm gần như toàn bộ mục NEVER** của skill — nhưng nó dễ hiểu hơn vì giải một bài toán khác: *nhận diện & gợi nhớ*, không phải *giải thích cơ chế*. Hướng update đúng không phải "bỏ hình học để vẽ đồ vật", mà là **tách vai trò theo kích thước** và **mở rộng ngữ pháp để chống đụng hình**.

---

## 1. Ba chiến lược đang trộn lẫn trong bộ card

| Nhóm | Card | Hình vẽ | Vẽ cái gì |
|---|---|---|---|
| **(1) Literal-name** — vẽ đúng nghĩa đen của tên gọi | Halo Effect · Spotlight Effect | hào quang thiên thần · đèn sân khấu chiếu người | *Cái tên*, không phải cơ chế |
| **(2) Example-object** — vẽ đồ vật trong dòng ví dụ | Bandwagon (fidget spinner) · Confirmation (UFO) · Backfire (bản đồ phẳng) | đồ vật cụ thể của ví dụ | *Ví dụ*, không phải khái niệm |
| **(3) Conceptual metaphor** — vẽ quan hệ | FAE (gương) · In-Group (Stonehenge) · Naïve Cynicism (tay đưa quà / tay chìa ra) · Self-Serving (huy chương) | quan hệ self↔other, trong↔ngoài, cho↔nhận | *Cơ chế* |

**Đánh giá theo mức độ sát nghĩa:**

- Nhóm (3) là nhóm duy nhất thực sự dạy được. Stonehenge đặc biệt tốt: 5 cột dính nhau có xà ngang + 2 cột rời hai bên = in-group/out-group **nhìn phát hiểu**, không cần caption. Gương của FAE cũng vậy — mặt phản chiếu = phán xét bản thân, mặt kia = phán xét người khác.
- Nhóm (1) rất dễ nhớ nhưng **rỗng nội dung**: hào quang không giải thích tại sao ấn tượng tốt lan sang các trait khác. Nó là mnemonic, không phải explanation.
- Nhóm (2) là nhóm **yếu nhất và nên tránh**. Ba lý do:
  - *Lỗi thời*: fidget spinner là hiện tượng 2017; 5 năm nữa người đọc không nhận ra.
  - *Phụ thuộc ví dụ*: đổi ví dụ là hình vô nghĩa. Hình lẽ ra phải sống lâu hơn ví dụ.
  - *Thiên kiến văn hoá / châm biếm*: UFO và flat-earth gắn với conspiracy kiểu Mỹ, và mang giọng chế giễu — lệch tone "Seeing the Unseen".
- **Groupthink** là ca thất bại rõ nhất: mặt người nhìn nghiêng ghép từ mảng địa hình — phải nhìn rất lâu mới ra, và ra rồi vẫn không hiểu liên quan gì tới "conformity". Ở 64px thì thành nhiễu hoàn toàn.

---

## 2. Vì sao chúng "dễ hiểu" hơn hình học thuần

Ba cơ chế thật sự đứng sau, tách khỏi chuyện literal hay không:

1. **Silhouette đặc trưng.** Mỗi card một bóng hình riêng → phân biệt được ngay cả khi thu nhỏ. Đây đúng là điểm yếu đã ghi trong `docs/scheduled-task-illustrations.md` mục C: 230 card / 14 primitive = **~16 card dùng chung một hình**. Trên trang library, 16 thumbnail giống hệt nhau trông như lỗi render.
2. **Neo vào tri thức có sẵn.** Người đọc đã biết "hào quang", "spotlight" → không tốn chi phí giải mã.
3. **Có nhân vật/hành động.** Tay đưa quà kể một *câu chuyện nhỏ*; hình học chỉ nêu một *quan hệ*.

Nhưng đổi lại: mất tính hệ thống, phụ thuộc văn hoá, và không scale (mỗi card phải vẽ tay riêng — 230 card là bất khả thi cho pipeline tự động).

---

## 3. Ba hướng update — kèm khuyến nghị

### Hướng A — Giữ nguyên hình học, chỉ thêm biến thể *(rẻ, không giải quyết gốc)*
Thêm variation xác định theo slug (xoay, đổi số nấc, đổi góc lát cắt). Phá được sự trùng khít nhưng 16 card vẫn cùng "họ hình" → ở 64px vẫn khó phân biệt.

### Hướng B — Hệ lai 2 tầng theo kích thước ✅ **Khuyến nghị**
Tách rõ vai trò, vì hai kích thước phục vụ hai mục đích khác nhau:

| Lớp | Kích thước | Nhiệm vụ | Ngữ pháp |
|---|---|---|---|
| **Thumbnail** | 64/128px | *Nhận diện & gợi nhớ* — giúp phân biệt card này với card kia | Cho phép **concept object**: 1 vật thể ẩn dụ, dựng **bằng đúng bộ primitive hình học**, stroke/hue không đổi |
| **Hero / section** | 800–1200px | *Giải thích cơ chế* | Giữ nguyên idea-shape trừu tượng như hiện tại |

Điểm mấu chốt: **thumbnail 64px không phải nơi dạy khái niệm** — không ai học được cơ chế từ một ô 64px. Ép nó mang nhiệm vụ giải thích là lý do khiến hình vừa trừu tượng vừa trùng nhau. Đổi nhiệm vụ của nó thành *phân biệt*, mọi thứ hợp lý trở lại.

"Concept object" ở đây **không phải** vẽ đồ vật tuỳ tiện. Ràng buộc chặt:
- Chỉ nhận vật thể thuộc **nhóm (3)** — biểu đạt *quan hệ*, không phải đồ vật trong ví dụ.
- Dựng từ đúng primitive (tròn/ellipse/tam giác/vuông/lục giác/đường/cung), stroke 1.6 @128, một hue.
- **Vẫn cấm tuyệt đối:** người có mặt/tay/cơ thể, não, bóng đèn, kính lúp, bánh răng, điện thoại — tức các icon sáo đã cấm.
- Test bắt buộc: *hình này còn đúng không nếu đổi ví dụ trong card?* Không → loại.

### Hướng C — Mở bộ primitive 14 → ~24 bằng ghép đôi *(đắt, đúng ngữ nghĩa nhất)*
`hierarchy`+`cycle`, `contrast`+`threshold`… Skill đã cho phép ở Step 2. Giảm đụng hình xuống ~10 card/hình nhưng chưa đủ, và tăng chi phí chẩn đoán mỗi card.

> **Khuyến nghị: B, kèm A làm lớp phụ.** C để dành nếu sau 5–6 batch vẫn thấy trùng.

---

## 4. Cụ thể: sửa gì trong skill

**Step 1 — bảng deliverable:** tách dòng thumbnail thành vai trò riêng, ghi rõ *"nhiệm vụ: phân biệt & gợi nhớ, KHÔNG phải giải thích"*.

**Step 2 — thêm nhánh chẩn đoán cho thumbnail:**
> Với thumbnail ≤128px: sau khi chẩn đoán idea shape, hỏi thêm — *có concept object nào biểu đạt đúng quan hệ này không?* Có → ưu tiên, vì nó phân biệt tốt hơn ở khổ nhỏ. Không → dùng idea shape rút gọn.

**Step 3 — thêm mục "Concept object grammar":** vật thể phải dựng từ primitive, một hue, stroke đồng đều; kèm 3 test loại trừ (đổi ví dụ có hỏng không · có phải icon sáo không · có nhận ra ở 64px không).

**Mục NEVER — nới có điều kiện, không xoá:**
- Sửa: ~~NEVER vẽ vật thể mô tả~~ → **NEVER vẽ vật thể *của ví dụ*; vật thể *của quan hệ* được phép ở lớp thumbnail, với ràng buộc ở Step 3.**
- **Giữ nguyên** lệnh cấm: người/bộ phận cơ thể, não, bóng đèn, kính lúp, bánh răng — đây vẫn là icon sáo.
- **Thêm mới:** NEVER vẽ đồ vật gắn với trào lưu nhất thời hoặc chủ đề chế giễu (fidget spinner, UFO, flat-earth) — hình phải sống lâu hơn ví dụ và giữ giọng trung tính.

**Step 7 — thêm 2 mục checklist:**
- [ ] Ở khổ 64px, không hai thumbnail nào trong cùng batch bị nhầm với nhau.
- [ ] Mỗi thumbnail vẫn đúng nếu ví dụ trong card bị thay.

---

## 5. Lưu ý bản quyền

Bộ card đính kèm là tài sản của tác giả gốc. Ta **học nguyên tắc** (silhouette đặc trưng, neo tri thức sẵn có, vẽ quan hệ chứ không vẽ ví dụ) — **không sao chép hình**. Skill đã có sẵn dòng NEVER copy; giữ nguyên.

---

## 6. Definition of Done / next steps

- [ ] Cập nhật skill: Step 1 (bảng vai trò), Step 2 (nhánh thumbnail), Step 3 (concept object grammar), NEVER (nới có điều kiện + cấm đồ vật trend), Step 7 (2 mục checklist).
- [ ] Bổ sung `illus.py`: nhóm `CONCEPT_OBJECTS` cho các quan hệ hay gặp — self↔other (gương), in↔out (vòng trong/ngoài), give↔take, up↔down.
- [ ] Render lại 10 thumbnail batch #1 theo ngữ pháp mới, đặt cạnh bản cũ ở **khổ 64** để so.
- [ ] Nếu bản mới phân biệt tốt hơn rõ rệt → áp cho 22 batch còn lại; nếu không → quay về hướng A.

**Quyết định cần bạn chốt:** có mở "concept object" cho lớp thumbnail không (hướng B), hay giữ thuần hình học và chấp nhận đụng hình (hướng A)?
