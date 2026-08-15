# Design Spec — trích từ Claude Design "The Unseen.dc.html"

> Nguồn: https://claude.ai/design/p/f3202e75-7d70-4ba7-aecd-5d048459ee9d (file `The Unseen.dc.html`).
> Đây là **source of truth cho UI**. Implementation hiện tại lệch bản design → cần align theo file này.
> Token dưới đây trích trực tiếp từ mã nguồn prototype, không phải phỏng đoán.

## 1. Quyết định cập nhật (override docs cũ)

- **5 map** (không phải 4 + Sun riêng): map 5 `KNOWLEDGE · EPISTEME` **chính là** The Sun — palette vàng rực, cats `SUN/TRUTH/GOOD`, alpha fog thấp nhất (.5 = sáng nhất).
- Ánh xạ content: `level` 1→map 1, 2→map 2, 3→map 3, 4→map 4. **Map 5 không chứa stuff** — là màn tổng kết (flames lit, link Graph/Library).
- Header: brand + search + Library + Graph + About. **Không có Daily / Favorites.**

## 2. Palette 5 map (nguyên văn từ prototype)

Mỗi map là object: `{name, vn, sub, cats, gA, gB, treeD, treeL, treeHi, bush, path, pathDot, flower, rock, icon, iconGlow, dk, alpha}`
(`gA/gB` = 2 tông nền cỏ; `treeD/L/Hi` = cây; `bush` = bụi; `path/pathDot` = đường đi; `dk` = màu bóng tối RGB; `alpha` = độ đậm fog — giảm dần → sáng dần)

```js
const MAPS = [
  {name:'IMAGINING',   vn:'Tưởng tượng', sub:'EIKASIA',  cats:['SHADOW','IMAGE','ECHO'],
   gA:'#1e1c3a', gB:'#1a1834', treeD:'#100e24', treeL:'#2a2750', treeHi:'#3a366b', bush:'#232048',
   path:'#4c4680', pathDot:'#3d3868', flower:'#8f7fe0', rock:'#4a4670',
   icon:'#cfc2ff', iconGlow:'rgba(160,130,255,.85)', dk:'5,4,16',   alpha:.97},

  {name:'BELIEF',      vn:'Niềm tin',    sub:'PISTIS',   cats:['OBJECT','SENSE','HABIT'],
   gA:'#17414b', gB:'#143a43', treeD:'#0c2830', treeL:'#20565f', treeHi:'#2f6f78', bush:'#123640',
   path:'#7e9a94', pathDot:'#6b8781', flower:'#d8b46a', rock:'#4f6a6b',
   icon:'#aef0dd', iconGlow:'rgba(90,220,180,.85)',  dk:'4,16,18',  alpha:.93},

  {name:'THINKING',    vn:'Tư duy',      sub:'DIANOIA',  cats:['MATH','LOGIC','HYPOTHESIS'],
   gA:'#8ed3ac', gB:'#85cba3', treeD:'#47927e', treeL:'#68b199', treeHi:'#83c7ae', bush:'#57ad83',
   path:'#f2ecd9', pathDot:'#e0d7bd', flower:'#f2d24d', rock:'#b9c4bb',
   icon:'#0f5140', iconGlow:'rgba(255,240,170,.9)',   dk:'8,32,24',  alpha:.88},

  {name:'INTELLIGENCE',vn:'Lý tính',     sub:'NOESIS',   cats:['FORM','DIALECTIC','ESSENCE'],
   gA:'#cfe0a4', gB:'#c7d899', treeD:'#7c9a54', treeL:'#9cba70', treeHi:'#b4d086', bush:'#a4c476',
   path:'#f7f0da', pathDot:'#e7dec2', flower:'#e08a4a', rock:'#bdb694',
   icon:'#5a4a10', iconGlow:'rgba(255,220,120,.9)',   dk:'40,30,6',  alpha:.8},

  {name:'KNOWLEDGE',   vn:'Tri thức',    sub:'EPISTEME', cats:['SUN','TRUTH','GOOD'],
   gA:'#f0e2b2', gB:'#ecdca6', treeD:'#c49f55', treeL:'#dcbd74', treeHi:'#ecd694', bush:'#dfc98a',
   path:'#fcf7e6', pathDot:'#efe6cb', flower:'#dd6440', rock:'#d3c7a8',
   icon:'#7a4408', iconGlow:'rgba(255,200,90,.95)',   dk:'70,48,4',  alpha:.5},
];
```

## 3. Typography & chrome

- Font pixel: **`'Press Start 2P', monospace`** (Google Fonts) — dùng cho nhãn map, breadcrumb, nút MOVE/OPTIONS, badge "A FIRE".
- Font phụ: `ui-monospace, Menlo, monospace`.
- Nền app ngoài canvas: `#fbfaf7`; chữ tối `#3a372f`; viền/nhạt `#d9d4c6`, `#eee9dc`, `#f6f3ea`; muted `#8a8577` / `#9a958a`.
- Nền tối (overlay mặt sau card): `#0a0910`, `#141310`.

## 4. Layout & hành vi (nguyên bản prototype)

- **Header**: brand `▢ the unseen` trái + ô `SEARCH / TÌM KIẾM ⏎` (Enter → nhảy tới stuff khớp tên) + nav phải.
- **Nhãn map**: badge góc trên trái `I · IMAGINING`, dưới là dòng nhỏ `EIKASIA — Tưởng tượng · VÙNG 1/3`.
- **Breadcrumb** đáy trái: `IMAGINING · BELIEF · THINKING · INTELLIGENCE · KNOWLEDGE`, map hiện tại in đậm, click nhảy map.
- **Hint** đáy phải: `PHÍM ← → ĐỂ ĐI BỘ · < > NHẢY VÙNG · ARROWS TO WALK`.
- **MOVE** ◀ ▶ góc phải dưới; **OPTIONS ▲** ngay trên nó. Cả hai z-index cao nhất, luôn nổi trên overlay. Khi overlay mở, ◀ ▶ chuyển thành duyệt prev/next stuff.
- **OPTIONS popup**: slider torchRadius 500–900px, toggle revealAll, 5 nút nhảy map.
- Ngọn lửa: badge `A FIRE` dưới sprite; tốc độ đi bộ **280px/s**; đường đi uốn lượn seeded theo map; stuff sinh trong hành lang ~500px quanh đường.
- Fog: bán kính mặc định **500px** (mobile = bề rộng màn hình), màu bóng tối = `dk` của map, độ đậm = `alpha`.
- Icon stuff: `['★','▲','◼︎','●','✱','◆','☀︎','✦','☯︎','☾']` — trong repo derive theo category (`src/lib/icons.ts`), không random.
- Mỗi map chia **3 zones** (`VÙNG 1/3`).

## 5. Khác biệt có chủ đích so với prototype (giữ nguyên, không sửa ngược)

| Prototype | Repo | Lý do |
|---|---|---|
| 75 essay mẫu ngẫu nhiên | 182 stuff thật từ `content/stuff` qua `public/map-data.json` | Content thật |
| Header có Daily/Favorites | Bỏ | Quyết định của Núi |
| Icon random | Derive theo category | Build plan V5 |
| Không có progression | `src/lib/progress.ts` (localStorage, flames lit) | Build plan — retention hook |
