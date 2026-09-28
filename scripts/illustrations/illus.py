#!/usr/bin/env python3
"""Editorial geometric illustration primitives — Seeing the Unseen.

Two artboards:
  * FULL  400x400 (panel 400x440, 545 w/ wordmark) — dùng cho hero/section (Phase B).
  * THUMB 128x128                                   — bản RÚT GỌN riêng, dùng cho stuff card.

THUMB không phải là bản scale của FULL. Theo skill `editorial-geometric-illustration`:
bỏ chi tiết <8px, giảm số phần tử, stroke ~1.2% chiều rộng, bỏ mũi tên và đường chấm.
"""
import math
import itertools

INK = "#111111"
SW_FULL = 2.4       # 0.60% của 400
SW_THUMB = 1.6      # 1.25% của 128

_uid = itertools.count()

PALETTES = {
    "mint":  dict(bg="#8FDDC0", t1="#DCF4E9", t2="#AFE6CF", t3="#7FD6B4", t4="#4FC39A", acc="#2FBF8F"),
    "amber": dict(bg="#F9D18A", t1="#FDF0D6", t2="#FBE1AE", t3="#F7C871", t4="#F0AE3C", acc="#E39B22"),
    "paper": dict(bg="#FFFFFF", t1="#DCF4E9", t2="#AFE6CF", t3="#7FD6B4", t4="#4FC39A", acc="#2FBF8F"),
}


def _pal(hue, paper_bg=False):
    """Lấy palette theo hue; paper_bg=True → nền trắng nhưng giữ nguyên tint ladder của hue."""
    p = dict(PALETTES[hue])
    if paper_bg:
        p["bg"] = "#FFFFFF"
    return p


# --------------------------------------------------------------------------
# FULL artboard 400x400
# --------------------------------------------------------------------------
S = f'stroke="{INK}" stroke-width="{SW_FULL}" stroke-linecap="round" stroke-linejoin="round"'
NOFILL = f'fill="none" {S}'
DOT = f'fill="none" stroke="{INK}" stroke-width="{SW_FULL}" stroke-dasharray="1 9" stroke-linecap="round"'


def arrow(x1, y1, x2, y2, head=13):
    a, w = math.atan2(y2 - y1, x2 - x1), math.radians(26)
    p1 = (x2 - head * math.cos(a - w), y2 - head * math.sin(a - w))
    p2 = (x2 - head * math.cos(a + w), y2 - head * math.sin(a + w))
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {NOFILL}/>'
            f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {x2},{y2} {p2[0]:.1f},{p2[1]:.1f}" {NOFILL}/>')


def donut_seg(cx, cy, r0, r1, a0, a1, fill, s=S):
    ra0, ra1 = math.radians(a0), math.radians(a1)
    big = 1 if (a1 - a0) % 360 > 180 else 0
    xo0, yo0 = cx + r1 * math.cos(ra0), cy + r1 * math.sin(ra0)
    xo1, yo1 = cx + r1 * math.cos(ra1), cy + r1 * math.sin(ra1)
    xi1, yi1 = cx + r0 * math.cos(ra1), cy + r0 * math.sin(ra1)
    xi0, yi0 = cx + r0 * math.cos(ra0), cy + r0 * math.sin(ra0)
    return (f'<path d="M{xo0:.1f},{yo0:.1f} A{r1},{r1} 0 {big} 1 {xo1:.1f},{yo1:.1f} '
            f'L{xi1:.1f},{yi1:.1f} A{r0},{r0} 0 {big} 0 {xi0:.1f},{yi0:.1f} Z" fill="{fill}" {s}/>')


def contrast(p):
    return (f'<path d="M108,248 L148,168 L188,248 Z" fill="{p["t1"]}" {S}/>'
            f'<line x1="196" y1="272" x2="248" y2="150" {NOFILL}/>'
            f'<circle cx="292" cy="212" r="40" fill="{p["t2"]}" {S}/>')


def nested_scope(p):
    o = [f'<circle cx="200" cy="{288-r}" r="{r}" fill="{f}" {S}/>'
         for r, f in ((84, "none"), (66, p["t1"]), (48, p["t2"]), (30, p["t4"]))]
    return "".join(o) + arrow(200, 288, 200, 154)


def overlap_phases(p):
    o = [f'<line x1="72" y1="212" x2="328" y2="212" {DOT}/>']
    o += [f'<ellipse cx="{cx}" cy="212" rx="42" ry="76" fill="{p["acc"]}" fill-opacity="0.30" {S}/>'
          for cx in (148, 200, 252)]
    return "".join(o)


def coverage_sphere(p):
    cx, cy, r = 200, 212, 78
    cid = f"sph{next(_uid)}"
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{p["t1"]}" {S}/>',
         f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>',
         f'<g clip-path="url(#{cid})">']
    o += [f'<ellipse cx="{cx}" cy="{cy}" rx="{abs(k)*22+8}" ry="{r}" {NOFILL} transform="rotate(-32 {cx} {cy})"/>'
          for k in range(-3, 4)]
    return "".join(o) + "</g>" + arrow(cx - 92, cy + 92, cx + 92, cy - 92)


def funnel(p):
    o = [f'<ellipse cx="200" cy="140" rx="76" ry="23" fill="{p["t1"]}" {S}/>',
         f'<path d="M124,140 L200,208 L276,140" {NOFILL}/>']
    o += [f'<ellipse cx="200" cy="{224+i*24}" rx="{24+i*21}" ry="{ry}" fill="{p["acc"]}" '
          f'fill-opacity="{0.30-i*0.06:.2f}" {S}/>' for i, ry in enumerate((8, 12, 16, 20))]
    return "".join(o)


def network(p):
    cx, cy, R = 200, 212, 76
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in range(-90, 270, 60)]
    o = [f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{pts[(i+1)%6][0]:.1f}" y2="{pts[(i+1)%6][1]:.1f}" {NOFILL}/>'
         for i, a in enumerate(pts)]
    hx = " ".join(f'{cx+22*math.cos(math.radians(a)):.1f},{cy+22*math.sin(math.radians(a)):.1f}'
                  for a in range(-90, 270, 60))
    o.append(f'<polygon points="{hx}" fill="{p["t2"]}" {S}/>')
    o += [f'<line x1="{cx}" y1="{cy}" x2="{a[0]:.1f}" y2="{a[1]:.1f}" {NOFILL}/>' for a in pts]
    o += [f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="13" fill="#FFFFFF" {S}/>' for a in pts]
    return "".join(o)


def cycle(p):
    cx, cy = 200, 212
    o = [f'<circle cx="{cx}" cy="{cy}" r="76" {NOFILL}/>',
         f'<circle cx="{cx}" cy="{cy}" r="46" fill="{p["t1"]}" {S}/>',
         f'<circle cx="{cx}" cy="{cy}" r="11" fill="{INK}" stroke="none"/>']
    for a0, a1 in ((-58, 58), (122, 238)):
        r = 100
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        o.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" {NOFILL}/>')
        ta = math.radians(a1) + math.pi / 2
        o.append(arrow(x1 - 12 * math.cos(ta), y1 - 12 * math.sin(ta), x1, y1, head=12))
    return "".join(o)


def page_structure(p):
    o = [f'<rect x="112" y="140" width="176" height="144" rx="3" fill="#FFFFFF" {S}/>',
         f'<line x1="112" y1="168" x2="288" y2="168" {NOFILL}/>',
         f'<rect x="122" y="178" width="74" height="18" fill="{p["t3"]}" {S}/>',
         f'<rect x="206" y="178" width="72" height="18" fill="{p["t3"]}" {S}/>',
         f'<circle cx="146" cy="238" r="20" fill="{p["t1"]}" {S}/>']
    o += [f'<line x1="{196+i*18}" y1="220" x2="{196+i*18}" y2="258" {NOFILL}/>' for i in range(3)]
    return "".join(o)


def proportion(p):
    cx, cy = 208, 208
    return (f'<circle cx="{cx}" cy="{cy}" r="74" fill="{p["t2"]}" {S}/>'
            + donut_seg(cx, cy, 20, 74, 90, 168, p["t4"])
            + f'<circle cx="{cx}" cy="{cy}" r="20" fill="#FFFFFF" {S}/>'
            + f'<line x1="{cx-14}" y1="{cy+14}" x2="88" y2="322" {NOFILL}/>'
            + f'<line x1="{cx}" y1="{cy+20}" x2="{cx}" y2="322" {NOFILL}/>')


def hierarchy(p):
    return (f'<circle cx="200" cy="152" r="30" fill="{p["t4"]}" {S}/>'
            f'<path d="M200,182 L200,214 M112,246 L112,214 L288,214 L288,246 M200,214 L200,246" {NOFILL}/>'
            f'<circle cx="112" cy="272" r="26" fill="{p["t2"]}" {S}/>'
            f'<rect x="174" y="246" width="52" height="52" fill="{p["t2"]}" {S}/>'
            f'<path d="M288,246 L316,298 L260,298 Z" fill="{p["t2"]}" {S}/>')


def layers(p):
    return "".join(
        f'<ellipse cx="200" cy="{136+i*30}" rx="86" ry="24" '
        f'fill="{"#FFFFFF" if o == 0 else p["acc"]}" fill-opacity="{1 if o == 0 else o}" {S}/>'
        for i, o in enumerate((0.0, 0.18, 0.34, 0.34, 0.18, 0.0)))


def spectrum(p):
    o = [f'<line x1="76" y1="212" x2="324" y2="212" {DOT}/>']
    o += [f'<circle cx="{92+i*54}" cy="212" r="{12+i*9}" fill="{p["acc"]}" '
          f'fill-opacity="{0.12+i*0.15:.2f}" {S}/>' for i in range(5)]
    return "".join(o)


def divergence(p):
    ox, oy = 128, 212
    o = [f'<circle cx="{ox}" cy="{oy}" r="13" fill="{p["t4"]}" {S}/>']
    o += [arrow(ox + 20 * math.cos(math.radians(a)), oy + 20 * math.sin(math.radians(a)),
                ox + 158 * math.cos(math.radians(a)), oy + 158 * math.sin(math.radians(a)))
          for a in (-34, -12, 12, 34)]
    o.append(f'<path d="M300,120 A180,180 0 0 1 300,304" {DOT}/>')
    return "".join(o)


def threshold(p):
    return (f'<line x1="72" y1="212" x2="328" y2="212" {DOT}/>'
            f'<circle cx="132" cy="260" r="26" fill="{p["acc"]}" fill-opacity="0.18" {S}/>'
            f'<circle cx="200" cy="212" r="30" fill="{p["acc"]}" fill-opacity="0.40" {S}/>'
            f'<circle cx="272" cy="160" r="34" fill="{p["acc"]}" fill-opacity="0.66" {S}/>'
            + arrow(112, 292, 300, 128))


REGISTRY = dict(contrast=contrast, nested_scope=nested_scope, overlap_phases=overlap_phases,
                coverage_sphere=coverage_sphere, funnel=funnel, network=network, cycle=cycle,
                page_structure=page_structure, proportion=proportion, hierarchy=hierarchy,
                layers=layers, spectrum=spectrum, divergence=divergence, threshold=threshold)


def panel(name, pal="mint", wordmark=None, w=400, h=None, transparent=False):
    p = PALETTES[pal]
    h = h or (545 if wordmark else 440)
    bg = "" if transparent else f'<rect width="{w}" height="{h}" fill="{p["bg"]}"/>'
    mark = (f'<text x="{w/2}" y="{h-47}" text-anchor="middle" font-family="Helvetica,Arial" '
            f'font-size="27" letter-spacing="0.5" fill="{INK}">{wordmark}</text>') if wordmark else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{bg}{REGISTRY[name](p)}{mark}</svg>')


# --------------------------------------------------------------------------
# THUMB artboard 128x128 — bản rút gọn, KHÔNG scale từ FULL
# Luật: không mũi tên, không đường chấm, ≤4 phần tử chính, lề an toàn ≥12px.
# --------------------------------------------------------------------------
TS = f'stroke="{INK}" stroke-width="{SW_THUMB}" stroke-linecap="round" stroke-linejoin="round"'
TNF = f'fill="none" {TS}'


def t_contrast(p):
    # Hai khối đối lập, hình học trái ngược (góc cạnh vs tròn), tách rời.
    return (f'<path d="M19,86 L41,42 L63,86 Z" fill="{p["t1"]}" {TS}/>'
            f'<circle cx="87" cy="64" r="22" fill="{p["t3"]}" {TS}/>')


def t_nested_scope(p):
    # 3 vòng đồng tâm, đậm dần vào trong = tầng phạm vi.
    return "".join(f'<circle cx="64" cy="64" r="{r}" fill="{f}" {TS}/>'
                   for r, f in ((46, p["t1"]), (30, p["t3"]), (14, p["acc"])))


def t_overlap_phases(p):
    # 2 ellipse chồng nhau; vùng giao tự đậm lên nhờ fill-opacity.
    return "".join(f'<ellipse cx="{cx}" cy="64" rx="26" ry="40" fill="{p["acc"]}" '
                   f'fill-opacity="0.32" {TS}/>' for cx in (50, 78))


def t_coverage_sphere(p):
    # Khối cầu có kinh tuyến xuyên suốt = bao phủ toàn hệ.
    cid = f"tsph{next(_uid)}"
    o = [f'<circle cx="64" cy="64" r="45" fill="{p["t1"]}" {TS}/>',
         f'<clipPath id="{cid}"><circle cx="64" cy="64" r="45"/></clipPath>',
         f'<g clip-path="url(#{cid})">',
         f'<line x1="64" y1="19" x2="64" y2="109" {TNF} transform="rotate(-32 64 64)"/>']
    o += [f'<ellipse cx="64" cy="64" rx="{rx}" ry="45" {TNF} transform="rotate(-32 64 64)"/>'
          for rx in (16, 32)]
    return "".join(o) + "</g>"


def t_funnel(p):
    # Miệng rộng → thắt → mở lại: hội tụ rồi phân kỳ (double diamond).
    # Đĩa dưới đặt sát mũi nón để không đọc thành "ly rượu".
    return (f'<ellipse cx="64" cy="32" rx="40" ry="12" fill="{p["t1"]}" {TS}/>'
            f'<path d="M24,32 L64,70 L104,32" {TNF}/>'
            f'<ellipse cx="64" cy="79" rx="22" ry="9" fill="{p["acc"]}" fill-opacity="0.38" {TS}/>'
            f'<ellipse cx="64" cy="97" rx="38" ry="14" fill="{p["acc"]}" fill-opacity="0.20" {TS}/>')


def t_network(p):
    # 6 node → rút còn 3 node quanh một lõi.
    cx, cy, R = 64, 66, 34
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))
           for a in (-90, 30, 150)]
    o = [f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{pts[(i+1)%3][0]:.1f}" y2="{pts[(i+1)%3][1]:.1f}" {TNF}/>'
         for i, a in enumerate(pts)]
    o += [f'<line x1="{cx}" y1="{cy}" x2="{a[0]:.1f}" y2="{a[1]:.1f}" {TNF}/>' for a in pts]
    o.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{p["t3"]}" {TS}/>')
    o += [f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="9" fill="#FFFFFF" {TS}/>' for a in pts]
    return "".join(o)


def t_cycle(p):
    # 3 cung đứt đoạn quay quanh một lõi (không mũi tên).
    # Cố ý KHÔNG có chấm đen ở tâm — chấm giữa vòng đồng tâm sẽ đọc thành "con mắt".
    cx, cy, r = 64, 64, 45
    o = []
    for a0 in (-96, 24, 144):
        a1 = a0 + 88
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        o.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" {TNF}/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="21" fill="{p["t3"]}" {TS}/>')
    return "".join(o)


def t_page_structure(p):
    # Khung + header + 2 block + 1 dải: bố cục / IA.
    return (f'<rect x="26" y="28" width="76" height="72" rx="2" fill="#FFFFFF" {TS}/>'
            f'<line x1="26" y1="45" x2="102" y2="45" {TNF}/>'
            f'<rect x="34" y="53" width="29" height="13" fill="{p["t3"]}" {TS}/>'
            f'<rect x="68" y="53" width="26" height="13" fill="{p["t3"]}" {TS}/>'
            f'<rect x="34" y="76" width="60" height="14" fill="{p["t1"]}" {TS}/>')


def t_proportion(p):
    # Donut một lát cắt = phần trên tổng.
    cx, cy = 64, 64
    return (f'<circle cx="{cx}" cy="{cy}" r="44" fill="{p["t2"]}" {TS}/>'
            + donut_seg(cx, cy, 17, 44, 90, 172, p["acc"], s=TS)
            + f'<circle cx="{cx}" cy="{cy}" r="17" fill="#FFFFFF" {TS}/>')


def t_hierarchy(p):
    # 1 gốc → 2 nhánh (rút từ 3), hai hình con khác nhau để phân loại đọc được.
    return (f'<circle cx="64" cy="34" r="16" fill="{p["acc"]}" {TS}/>'
            f'<path d="M64,50 L64,66 M34,66 L94,66 M34,66 L34,78 M94,66 L94,78" {TNF}/>'
            f'<circle cx="34" cy="92" r="14" fill="{p["t2"]}" {TS}/>'
            f'<rect x="80" y="78" width="28" height="28" fill="{p["t2"]}" {TS}/>')


def t_layers(p):
    # 4 đĩa dẹt xếp chồng (rút từ 6); độ chồng tạo sắc độ.
    return "".join(
        f'<ellipse cx="64" cy="{40+i*16}" rx="42" ry="13" '
        f'fill="{"#FFFFFF" if o == 0 else p["acc"]}" fill-opacity="{1 if o == 0 else o}" {TS}/>'
        for i, o in enumerate((0.0, 0.22, 0.36, 0.22)))


def t_spectrum(p):
    # 4 nấc tăng dần, bỏ trục chấm.
    specs = ((19, 6, 0.16), (37, 10, 0.32), (63, 14, 0.48), (97, 18, 0.64))
    return "".join(f'<circle cx="{cx}" cy="64" r="{r}" fill="{p["acc"]}" '
                   f'fill-opacity="{op}" {TS}/>' for cx, r, op in specs)


def t_divergence(p):
    # Một điểm rẽ 3 nhánh. Nêm chia thành 3 múi tint khác nhau — ở 64px các
    # đường kẻ mảnh bên trong một nêm đặc sẽ biến mất, nên phải phân múi bằng màu.
    ox, oy = 34, 64
    xr = 108
    ys = (26, 51, 77, 102)          # 3 múi giữa 4 mốc
    tints = (p["t1"], p["t3"], p["t2"])
    o = [f'<path d="M{ox},{oy} L{xr},{ys[i]} L{xr},{ys[i+1]} Z" fill="{tints[i]}" {TS}/>'
         for i in range(3)]
    o.append(f'<circle cx="{ox}" cy="{oy}" r="11" fill="{p["acc"]}" {TS}/>')
    return "".join(o)


def t_threshold(p):
    # Ngưỡng = đường liền; 3 khối vượt qua nó thì đổi trạng thái (đậm dần).
    return (f'<line x1="14" y1="64" x2="114" y2="64" {TNF}/>'
            f'<circle cx="34" cy="88" r="14" fill="{p["acc"]}" fill-opacity="0.18" {TS}/>'
            f'<circle cx="65" cy="64" r="17" fill="{p["acc"]}" fill-opacity="0.44" {TS}/>'
            f'<circle cx="97" cy="40" r="20" fill="{p["acc"]}" fill-opacity="0.70" {TS}/>')


THUMB_REGISTRY = dict(contrast=t_contrast, nested_scope=t_nested_scope,
                      overlap_phases=t_overlap_phases, coverage_sphere=t_coverage_sphere,
                      funnel=t_funnel, network=t_network, cycle=t_cycle,
                      page_structure=t_page_structure, proportion=t_proportion,
                      hierarchy=t_hierarchy, layers=t_layers, spectrum=t_spectrum,
                      divergence=t_divergence, threshold=t_threshold)

# xlsx "Idea shape" -> key trong THUMB_REGISTRY / REGISTRY
SHAPE_MAP = {
    "hierarchy": "hierarchy",
    "branching": "divergence",
    "composition": "page_structure",
    "nesting": "nested_scope",
    "proportion": "proportion",
    "iteration": "cycle",
    "gradation": "spectrum",
    "convergence": "funnel",
    "traversal": "coverage_sphere",
    "contrast": "contrast",
    "system": "network",
    "strata": "layers",
    "tipping point": "threshold",
    "overlap": "overlap_phases",
}


# --------------------------------------------------------------------------
# CONCEPT OBJECTS — hướng B (xem docs/illustration-style-review.md)
#
# Vật thể ẩn dụ dựng BẰNG ĐÚNG primitive hình học. Mục đích: cho thumbnail một
# silhouette đặc trưng để phân biệt được ở 64px — thứ mà 14 idea shape thuần
# không làm nổi khi 230 card chia nhau 14 hình.
#
# Ba test bắt buộc trước khi thêm một concept object mới:
#   1. Nó biểu đạt QUAN HỆ, không phải đồ vật trong ví dụ của card.
#      ("đổi ví dụ trong card → hình có còn đúng không?" Không → loại.)
#   2. Không phải icon sáo bị cấm: người/bộ phận cơ thể, não, bóng đèn,
#      kính lúp, bánh răng, điện thoại.
#   3. Không gắn với trào lưu nhất thời hay chủ đề chế giễu
#      (fidget spinner, UFO, flat-earth) — hình phải sống lâu hơn ví dụ.
# Ngữ pháp không đổi: cùng stroke, một hue, tint ladder, không chữ, không mũi tên.
# --------------------------------------------------------------------------


def t_mirror(p):
    # Gương: cùng một sự việc, hai cách quy kết. Nửa trái nhạt (mình) /
    # nửa phải đậm (người khác) — bất đối xứng chính là nội dung.
    cid = f"tmir{next(_uid)}"
    return (f'<clipPath id="{cid}"><circle cx="64" cy="54" r="38"/></clipPath>'
            f'<circle cx="64" cy="54" r="38" fill="{p["t1"]}" {TS}/>'
            f'<g clip-path="url(#{cid})">'
            f'<rect x="64" y="16" width="38" height="76" fill="{p["t3"]}"/></g>'
            f'<line x1="64" y1="16" x2="64" y2="92" {TNF}/>'
            f'<path d="M64,92 L64,110 M44,110 L84,110" {TNF}/>')


def t_in_out_ring(p):
    # Lõi đặc (in-group) + vành; hai chấm nằm HẲN ngoài vành (out-group).
    return (f'<circle cx="58" cy="64" r="34" {TNF}/>'
            f'<circle cx="58" cy="64" r="19" fill="{p["acc"]}" fill-opacity="0.55" {TS}/>'
            f'<circle cx="108" cy="42" r="8" fill="{p["t2"]}" {TS}/>'
            f'<circle cx="106" cy="92" r="7" fill="{p["t2"]}" {TS}/>')


def t_balance(p):
    # Đòn cân lệch trên trụ tam giác: đánh đổi, thiên lệch có hướng.
    # Thanh dùng rect (không phải line) — ở 64px một line 1.6px gần như biến mất.
    # Đỉnh trụ phải CHẠM thanh, nếu không hình đọc thành cần cẩu chứ không phải cân.
    return (f'<path d="M64,48 L46,104 L82,104 Z" fill="{p["t1"]}" {TS}/>'
            f'<rect x="18" y="40" width="92" height="9" rx="4" fill="{p["t2"]}" {TS}'
            f' transform="rotate(14 64 44.5)"/>'
            f'<circle cx="24" cy="32" r="12" fill="{p["t3"]}" {TS}/>'
            f'<circle cx="104" cy="70" r="19" fill="{p["acc"]}" fill-opacity="0.55" {TS}/>')


def t_beam(p):
    # Nguồn hẹp → chùm mở rộng → một đích duy nhất sáng lên: chú ý dồn vào một điểm.
    # Chùm sáng KHÔNG được khép viền ở đáy — khép lại thì hình đọc thành bình thí nghiệm.
    # Vùng sáng: polygon có fill nhưng KHÔNG stroke; chỉ 2 cạnh xiên mới có nét.
    return (f'<rect x="52" y="14" width="24" height="13" fill="{p["t3"]}" {TS}/>'
            f'<path d="M54,27 L24,100 L104,100 L74,27 Z" fill="{p["acc"]}" '
            f'fill-opacity="0.20" stroke="none"/>'
            f'<path d="M54,27 L24,100 M74,27 L104,100" {TNF}/>'
            f'<circle cx="64" cy="92" r="12" fill="{p["acc"]}" fill-opacity="0.78" {TS}/>')


def t_halo_spill(p):
    # Một lõi đậm, sắc độ lan ra các ô lân cận: ấn tượng tràn sang trait khác.
    return (f'<circle cx="46" cy="64" r="21" fill="{p["acc"]}" fill-opacity="0.72" {TS}/>'
            f'<rect x="70" y="44" width="20" height="20" fill="{p["acc"]}" fill-opacity="0.40" {TS}/>'
            f'<rect x="70" y="70" width="20" height="20" fill="{p["acc"]}" fill-opacity="0.24" {TS}/>'
            f'<rect x="96" y="57" width="16" height="16" fill="{p["acc"]}" fill-opacity="0.12" {TS}/>')


def t_veil(p):
    # Một tấm che phủ mất phần dưới của hình: thông tin bị khuất, không phải không tồn tại.
    return (f'<circle cx="64" cy="58" r="32" fill="{p["t2"]}" {TS}/>'
            f'<rect x="14" y="66" width="100" height="34" rx="3" '
            f'fill="{p["acc"]}" fill-opacity="0.55" {TS}/>')


def t_fracture(p):
    # Một khối bị trượt lệch làm đôi: bất nhất giữa hai phần lẽ ra phải khớp.
    return (f'<rect x="22" y="30" width="42" height="42" fill="{p["t1"]}" {TS}/>'
            f'<rect x="64" y="56" width="42" height="42" fill="{p["t3"]}" {TS}/>')


def t_pull(p):
    # Một khối nặng kéo lệch cả hàng: mỏ neo / lực hút không cân xứng.
    # Vệ tinh CÙNG kích thước nhưng KHOẢNG CÁCH hẹp dần khi lại gần khối nặng —
    # dồn lại mới là dấu hiệu của lực hút. Dùng hình vuông để không bị đọc nhầm
    # thành `spectrum` (vốn là dãy tròn to dần) ở khổ 64px.
    o = [f'<circle cx="36" cy="64" r="25" fill="{p["acc"]}" fill-opacity="0.62" {TS}/>']
    o += [f'<rect x="{x}" y="56" width="16" height="16" fill="{p["t2"]}" {TS}/>'
          for x in (68, 90, 102)]
    return "".join(o)


def t_echo(p):
    # Bản gốc + 3 tiếng vọng nhạt dần cùng hướng: lặp lại làm quen thuộc / khuếch đại.
    return "".join(f'<rect x="{18+i*26}" y="{64-(30-i*5)//2}" width="20" height="{30-i*5}" '
                   f'fill="{p["acc"]}" fill-opacity="{0.68-i*0.17:.2f}" {TS}/>'
                   for i in range(4))


def t_gate(p):
    # Nhiều thứ tới, khe hẹp, ít thứ qua: sàng lọc / rào chắn.
    o = [f'<rect x="56" y="14" width="16" height="40" fill="{p["t3"]}" {TS}/>',
         f'<rect x="56" y="74" width="16" height="40" fill="{p["t3"]}" {TS}/>']
    o += [f'<circle cx="{cx}" cy="{cy}" r="8" fill="{p["t1"]}" {TS}/>'
          for cx, cy in ((20, 40), (20, 64), (20, 88))]
    o.append(f'<circle cx="104" cy="64" r="8" fill="{p["acc"]}" fill-opacity="0.6" {TS}/>')
    return "".join(o)


def t_rebound(p):
    # Một tác động đập vào rào cản rồi bật ngược lại — xa hơn và đậm hơn lúc đầu:
    # kết quả đi NGƯỢC chiều với ý định của người tác động.
    # Tường là một khối liền, KHÔNG có khe ở giữa — có khe là đọc thành `gate`.
    return (f'<rect x="96" y="14" width="16" height="100" rx="3" fill="{p["t1"]}" {TS}/>'
            f'<rect x="72" y="55" width="18" height="18" fill="{p["t3"]}" '
            f'fill-opacity="0.60" {TS}/>'
            f'<rect x="16" y="44" width="34" height="34" fill="{p["acc"]}" '
            f'fill-opacity="0.72" {TS}/>')


def t_odd_one_out(p):
    # Lưới đồng nhất + đúng MỘT ô khác loại. Nền đồng nhất là một phần của nội dung:
    # bỏ nền đi thì tính phân biệt biến mất (đúng như cơ chế distinctiveness).
    # 6 ô nhưng đọc thành 2 nhóm thị giác (nền + điểm lệch) nên vẫn giữ luật khổ nhỏ.
    cells = [(x, y) for y in (36, 70) for x in (18, 55, 92)]
    o = [f'<rect x="{x}" y="{y}" width="22" height="22" fill="{p["t2"]}" {TS}/>'
         for i, (x, y) in enumerate(cells) if i != 4]
    o.append(f'<circle cx="66" cy="81" r="14" fill="{p["acc"]}" '
             f'fill-opacity="0.85" {TS}/>')
    return "".join(o)


def t_tail_event(p):
    # Đuôi phân phối: một dãy biến cố thường xuyên nhưng nhỏ, và MỘT biến cố hiếm
    # có độ lớn áp đảo, nằm tách hẳn ra. Khác `echo` ở chỗ các cột đều nhau và cùng
    # đứng trên một đường đáy — chính cái gai cao mới là nội dung.
    o = [f'<rect x="{x}" y="82" width="14" height="22" fill="{p["t2"]}" {TS}/>'
         for x in (14, 33, 52, 71)]
    o.append(f'<rect x="98" y="20" width="18" height="84" fill="{p["acc"]}" '
             f'fill-opacity="0.80" {TS}/>')
    return "".join(o)


def t_gap_fill(p):
    # Một mạch bị đứt, và một mảnh VÁ bắc qua chỗ đứt làm mạch trông liền lại.
    # Mảnh vá lệch trục và khác chất liệu (accent trong suốt) — nhìn kỹ mới thấy
    # nó không thuộc về mạch gốc. Khác `fracture` ở chỗ fracture để lộ chỗ lệch,
    # còn ở đây chỗ hổng bị che đi nên tổng thể đọc thành liền mạch.
    return (f'<rect x="10" y="58" width="38" height="16" rx="3" fill="{p["t2"]}" {TS}/>'
            f'<rect x="80" y="58" width="38" height="16" rx="3" fill="{p["t2"]}" {TS}/>'
            f'<rect x="42" y="42" width="44" height="22" rx="5" fill="{p["acc"]}" '
            f'fill-opacity="0.70" {TS}/>')


def t_granularity(p):
    # Hai khối CÙNG kích thước: một bên phân giải được thành từng phần riêng biệt,
    # một bên nhoè thành khối đồng nhất. Nội dung nằm ở việc hai bên bằng nhau về
    # lượng nhưng khác nhau về độ phân giải — không phải bên nào lớn hơn.
    cid = f"tgra{next(_uid)}"
    return (f'<clipPath id="{cid}"><circle cx="38" cy="64" r="28"/></clipPath>'
            f'<circle cx="38" cy="64" r="28" fill="{p["t1"]}" {TS}/>'
            f'<g clip-path="url(#{cid})">'
            f'<path d="M38,36 L38,92 M10,54 L66,54 M10,76 L66,76" {TNF}/></g>'
            f'<circle cx="98" cy="64" r="28" fill="{p["acc"]}" fill-opacity="0.55" {TS}/>')


def t_cue_lock(p):
    # Nội dung còn NGUYÊN (khối đặc, không bị che) nhưng có một khuyết ở rìa, và
    # mảnh khớp với khuyết đó nằm tách hẳn ra ngoài. Quên ở đây không phải mất dữ
    # liệu mà là thiếu đúng mảnh để mở ra. Khác `veil` (bị che) và `gate` (bị chặn).
    # Mảnh rời có ĐÚNG bán kính của khuyết (r=11) — chính sự khớp bán kính mới nói
    # được "cái thiếu là mảnh này", chứ không phải một chấm trang trí bất kỳ.
    return (f'<path d="M14,26 H82 V53 A11,11 0 0 0 82,75 V102 H14 Z" '
            f'fill="{p["t2"]}" {TS}/>'
            f'<circle cx="105" cy="64" r="11" fill="{p["acc"]}" fill-opacity="0.75" {TS}/>')


def t_depletion(p):
    # Một nguồn lực hữu hạn bị rút cạn dần BỞI CHÍNH việc sử dụng lặp lại.
    # Khác `spectrum` (dải tĩnh của một biến) và `echo` (lặp lại nhạt dần, căn giữa):
    # ở đây có một VẠCH MỐC nằm ngang = mức đầy ban đầu, và các cột căn ĐÁY để đọc
    # được phần đã mất so với mốc đó. Không dùng fill-opacity — thông điệp nằm ở
    # chiều cao, thêm biến thứ hai sẽ làm loãng.
    o = [f'<rect x="14" y="26" width="100" height="7" rx="3" fill="{p["t1"]}" {TS}/>' ]
    o += [f'<rect x="{x}" y="{106-h}" width="18" height="{h}" fill="{p["t3"]}" {TS}/>'
          for x, h in ((18, 68), (44, 50), (70, 32), (96, 16))]
    return "".join(o)


def t_foil(p):
    # Một phần tử được thêm vào CHỈ để làm phần tử bên cạnh trông vượt trội —
    # bản thân nó không bao giờ được chọn. Dấu hiệu đọc được: khối nhỏ là BẢN THU
    # NHỎ của khối lớn (cùng chất liệu, nhỏ hơn ở CẢ HAI chiều) và đứng sát nó, nên
    # quan hệ áp đảo hiện ra ngay. Khối tròn bên trái là phương án KHÔNG so sánh
    # được — nó phá thế đơn điệu để hình không bị đọc thành `spectrum`.
    return (f'<circle cx="32" cy="68" r="26" fill="{p["t1"]}" {TS}/>'
            f'<rect x="62" y="36" width="32" height="64" fill="{p["acc"]}" '
            f'fill-opacity="0.62" {TS}/>'
            f'<rect x="98" y="64" width="18" height="36" fill="{p["acc"]}" '
            f'fill-opacity="0.62" {TS}/>')


def t_latch(p):
    # Các phương án ngang giá, nhưng một phương án đã được cài sẵn ở phía TRƯỚC
    # bức tường, còn muốn tới các phương án kia thì phải vượt tường. Bất đối xứng
    # nằm ở CÔNG SỨC, không ở giá trị. Khác `gate`: gate có khe hở và dòng chảy
    # xuyên qua (sàng lọc), còn tường ở đây ĐẶC — không ai bị chặn, chỉ là đứng yên
    # thì rẻ hơn.
    o = [f'<rect x="16" y="48" width="32" height="32" rx="4" fill="{p["acc"]}" '
         f'fill-opacity="0.75" {TS}/>',
         f'<rect x="58" y="18" width="8" height="92" rx="4" fill="{p["t2"]}" {TS}/>']
    o += [f'<rect x="78" y="{y}" width="30" height="30" rx="4" fill="{p["t1"]}" {TS}/>'
          for y in (26, 68)]
    return "".join(o)


def t_dilution(p):
    # Cùng MỘT nghĩa vụ: khi một người giữ thì nó đặc; khi chia cho nhiều người thì
    # mỗi phần mờ tới mức không đủ kích hoạt hành động. Tổng diện tích gần như không
    # đổi — đó mới là điểm. Khác `proportion` (lát cắt trên tổng, tĩnh) và
    # `granularity` (độ phân giải tri giác của hai người quan sát).
    o = [f'<rect x="14" y="34" width="100" height="24" rx="5" fill="{p["acc"]}" '
         f'fill-opacity="0.72" {TS}/>' ]
    o += [f'<rect x="{14+i*17}" y="76" width="13" height="24" rx="3" fill="{p["acc"]}" '
          f'fill-opacity="0.16" {TS}/>' for i in range(6)]
    return "".join(o)


def t_reference_kink(p):
    # Một đường mốc, hai độ lệch BẰNG NHAU về độ lớn nhưng bị xử lý ngược nhau:
    # phía trên đã rời khỏi mốc (buông sớm, nhạt), phía dưới vẫn dính chặt vào mốc
    # (giữ lại, nặng). Hai ô cố ý CÙNG kích thước — nếu khác kích thước thì hình
    # đọc thành `contrast` (hai thứ khác nhau) chứ không phải bất đối xứng quanh mốc.
    # Hai ô đẩy về HAI ĐẦU đối diện: bản dựng đầu đặt ô dưới gần tâm nên hình đọc
    # thành cái bàn/đòn cân có trụ đỡ (đụng `balance`). Lệch hẳn về hai góc thì
    # quan hệ đọc đúng là bất đối xứng quanh mốc, không phải một vật có chân đế.
    return (f'<rect x="12" y="61" width="104" height="6" rx="3" fill="{p["t1"]}" {TS}/>'
            f'<rect x="16" y="24" width="28" height="28" fill="{p["acc"]}" '
            f'fill-opacity="0.22" {TS}/>'
            f'<rect x="84" y="67" width="28" height="28" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>')


def t_rosy_tilt(p):
    # Thực tế KHÔNG đổi (4 ô bằng nhau y hệt, cùng đứng trên một vạch phẳng), chỉ
    # có sắc độ đánh giá nhạt dần theo thời gian. Khác `depletion` ở đúng chỗ then
    # chốt: depletion đổi CHIỀU CAO (nguồn lực mất thật), còn ở đây kích thước giữ
    # nguyên và chỉ độ đậm đổi — nghĩa là cái suy giảm nằm trong cách nhìn, không
    # nằm trong sự vật. Khác `echo` vì echo đổi cả chiều cao lẫn độ đậm và không có
    # vạch mốc phẳng bên dưới.
    # Ô cao 44 chứ không phải 22: bản 22 cho bbox chỉ cao 34/128, hình đọc thành một
    # dải mỏng và lạc khỏi mật độ nét của cả bộ.
    o = [f'<rect x="14" y="98" width="100" height="6" rx="3" fill="{p["t1"]}" {TS}/>' ]
    o += [f'<rect x="{x}" y="48" width="22" height="44" fill="{p["acc"]}" '
          f'fill-opacity="{op}" {TS}/>'
          for x, op in ((16, 0.78), (42, 0.55), (68, 0.32), (94, 0.14))]
    return "".join(o)


def t_juxtaposition(p):
    # CÙNG một cặp, vẽ hai lần. Hàng trên: đặt sát nhau, cạnh chung biến chênh lệch
    # thành một bậc thang nhìn thấy được. Hàng dưới: tách xa, mất cạnh chung nên
    # cùng chênh lệch đó không còn đọc ra. Biến duy nhất thay đổi là KHOẢNG CÁCH —
    # kích thước hai khối giữ y nguyên giữa hai hàng, nếu không thì mất luận điểm.
    o = [f'<rect x="34" y="18" width="28" height="34" fill="{p["t3"]}" {TS}/>',
         f'<rect x="62" y="26" width="28" height="26" fill="{p["t3"]}" {TS}/>',
         f'<rect x="14" y="76" width="28" height="34" fill="{p["t1"]}" {TS}/>',
         f'<rect x="86" y="84" width="28" height="26" fill="{p["t1"]}" {TS}/>']
    return "".join(o)


def t_overclaim(p):
    # Khung lớn = phạm vi tự nhận, phần tô đặc ở ĐÁY = phần thực sự có. Khoảng rỗng
    # phía trên chính là nội dung: nó không được vẽ thành một vật thể thứ hai, vì thứ
    # người ta thiếu đúng là thứ họ không nhìn thấy. Khác `proportion` (phần/tổng của
    # một đại lượng có thật) và khác `nested_scope` (nhiều tầng phạm vi lồng nhau —
    # ở đây chỉ có HAI mức và chúng chung đáy).
    return (f'<rect x="30" y="18" width="68" height="92" fill="{p["t1"]}" {TS}/>'
            f'<rect x="30" y="86" width="68" height="24" fill="{p["acc"]}" '
            f'fill-opacity="0.78" {TS}/>')


def t_effort_price(p):
    # Một cột chia thành từng ĐỐT (công sức đã bỏ, đếm được) và ngay cạnh là một
    # khối ĐẶC cùng chiều cao nhưng rộng gấp đôi (giá trị cảm nhận). Nội dung nằm ở
    # chỗ chiều cao khối phải bằng chiều cao cột: giá trị được đọc ra TỪ lượng công
    # sức, không từ bản thân vật. Khác `depletion` (cột thấp dần + vạch mốc, mất mát
    # thật) và khác `proportion` (phần/tổng): ở đây không có tổng nào bị chia cả.
    o = [f'<rect x="20" y="{y}" width="24" height="26" fill="{p["t2"]}" {TS}/>'
         for y in (26, 52, 78)]
    o.append(f'<rect x="56" y="26" width="56" height="78" fill="{p["acc"]}" '
             f'fill-opacity="0.70" {TS}/>')
    return "".join(o)


def t_base_blind(p):
    # HAI lần cùng một khối đặc y hệt (cùng bề rộng, cùng sắc độ) — con số được
    # trưng ra. Cái khác nhau là cái RAY nhạt đứng sau nó: một ray ngắn, một ray
    # dài gấp đôi. Cùng một tử số đọc trên hai mẫu số khác hẳn nhau. Ray vẽ nhạt
    # vì đó đúng là thứ bị bỏ qua chứ không phải thứ không tồn tại.
    # Khác `proportion`: donut cho thấy phần VÀ tổng nên tỉ lệ đọc ra được ngay —
    # ở đây tổng mới là biến, và nó bị nhìn xuyên qua.
    o = [f'<rect x="14" y="28" width="46" height="30" fill="{p["t1"]}" {TS}/>',
         f'<rect x="14" y="72" width="100" height="30" fill="{p["t1"]}" {TS}/>',
         f'<rect x="14" y="28" width="30" height="30" fill="{p["acc"]}" '
         f'fill-opacity="0.80" {TS}/>',
         f'<rect x="14" y="72" width="30" height="30" fill="{p["acc"]}" '
         f'fill-opacity="0.80" {TS}/>']
    return "".join(o)


def t_locus_flip(p):
    # Hai khung VUÔNG y hệt nhau; điểm đặc (động lực) nằm TRONG khung bên trái và
    # NGOÀI khung bên phải. Cùng một hành vi, chỉ khác chỗ ta đặt nguồn thúc đẩy.
    # Khác `mirror` (chia MỘT vật thành hai nửa sắc độ — quy kết bất đối xứng nói
    # chung): ở đây nội dung là VỊ TRÍ trong/ngoài của cái đẩy, không phải sắc độ.
    # Chấm ngoài phải CHẠM cạnh trái của khung phải: thả nó lơ lửng giữa hai khung
    # thì nó đọc thành một phần tử thứ ba, không đọc thành "cái đẩy của khung này".
    return (f'<rect x="14" y="44" width="36" height="38" fill="{p["t1"]}" {TS}/>'
            f'<circle cx="32" cy="63" r="8" fill="{p["acc"]}" fill-opacity="0.85" {TS}/>'
            f'<rect x="76" y="44" width="36" height="38" fill="{p["t1"]}" {TS}/>'
            f'<circle cx="68" cy="63" r="8" fill="{p["acc"]}" fill-opacity="0.85" {TS}/>')


def t_asymmetric_fade(p):
    # HAI dãy cùng xuất phát từ một mốc trái, ô nào cũng bằng nhau về kích thước —
    # chỉ sắc độ đổi. Dãy trên giữ được độ đậm gần như nguyên; dãy dưới rơi gần về 0.
    # Nội dung là TỐC ĐỘ phai khác nhau giữa hai dãy, nên phải có đủ hai dãy.
    # Khác `rosy_tilt` (một dãy phai đều — sự vật không đổi, cách nhìn nhạt dần):
    # ở đây một dãy phai nhanh hơn dãy kia mới là luận điểm.
    o = []
    for y, ops in ((26, (0.80, 0.72, 0.64, 0.56)), (70, (0.74, 0.34, 0.15, 0.06))):
        o += [f'<rect x="{x}" y="{y}" width="22" height="32" fill="{p["acc"]}" '
              f'fill-opacity="{op}" {TS}/>'
              for x, op in zip((14, 40, 66, 92), ops)]
    return "".join(o)


def t_from_primitives(p):
    # ĐÚNG ba primitive đó, vẽ hai lần. Hàng dưới: rời nhau, mỗi cái đứng một mình
    # (thành phần cơ bản đã kiểm chứng). Hàng trên: vẫn ba cái đó nhưng khít trong
    # MỘT khung — lời giải được dựng lại từ chính chúng. Biến đổi duy nhất là việc
    # có khung bao hay không, nên hình đọc thành "tháo ra rồi lắp lại", không phải
    # "cái này biến thành cái khác".
    # Khác `granularity` (hai khối bằng lượng, khác độ phân giải): ở đây hai hàng là
    # cùng một bộ phận tử, khác nhau ở chỗ đã lắp hay chưa.
    return (f'<rect x="16" y="22" width="96" height="38" fill="none" {TS}/>'
            f'<rect x="24" y="30" width="22" height="22" fill="{p["t3"]}" {TS}/>'
            f'<path d="M54,52 L66,30 L78,52 Z" fill="{p["t3"]}" {TS}/>'
            f'<circle cx="98" cy="41" r="11" fill="{p["t3"]}" {TS}/>'
            f'<rect x="18" y="82" width="22" height="22" fill="{p["t1"]}" {TS}/>'
            f'<path d="M52,104 L64,82 L76,104 Z" fill="{p["t1"]}" {TS}/>'
            f'<circle cx="104" cy="93" r="11" fill="{p["t1"]}" {TS}/>')


def t_ratchet(p):
    # Ba bậc cao dần, bậc sau ĐỨNG SÁT vai bậc trước chứ không rời ra — bậc đã
    # nhận (đặc, accent) là thứ đỡ cho bậc kế tiếp. Chính chỗ tiếp giáp mới là nội
    # dung: không có bậc nhỏ thì bậc lớn không có chỗ tựa.
    # Khác `spectrum` (4 vòng lớn dần, rời nhau, chỉ là dải độ lớn — không bậc nào
    # phụ thuộc bậc nào) và khác `threshold` (có một đường mốc để vượt qua).
    return (f'<rect x="16" y="86" width="30" height="24" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>'
            f'<rect x="46" y="62" width="30" height="48" fill="{p["t3"]}" {TS}/>'
            f'<rect x="76" y="30" width="30" height="80" fill="{p["t1"]}" {TS}/>')


def t_salience_pop(p):
    # Một trường 9 chấm ĐỀU NHAU: cùng bán kính, cùng lưới, cùng nét viền — nghĩa là
    # số lượng và vị trí không hề đổi. Chỉ ba chấm được tô đặc. Vì mọi chấm đều còn
    # nguyên đường viền, người xem đếm được rằng phần "mới xuất hiện" vốn đã ở đó.
    # Khác `odd_one_out` (một phần tử LỆCH khỏi nền đồng nhất — khác biệt nằm trong
    # vật) và khác `echo` (số lượng/độ lớn tăng dần — tần suất tăng thật).
    hot = {(56, 30), (22, 64), (90, 98)}
    o = []
    for y in (30, 64, 98):
        for x in (22, 56, 90):
            op = 0.85 if (x, y) in hot else 0.12
            o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{p["acc"]}" '
                     f'fill-opacity="{op}" {TS}/>')
    return "".join(o)


def t_foreground_swell(p):
    # Một dãy biến cố ĐỀU NHAU chạy suốt trên một vạch đáy, và dãy đó vẫn tiếp tục
    # ở CẢ HAI phía của khối lớn — đời sống không dừng lại vì sự kiện trọng tâm.
    # Khối giữa phình to là cỡ nó chiếm trong dự đoán, không phải cỡ thật của nó.
    # Khác `tail_event` (khối lớn nằm ở RÌA và hiếm — nội dung là độ hiếm) và khác
    # `beam` (nguồn sáng làm phần còn lại tối đi — ở đây phần còn lại vẫn sáng đều).
    o = [f'<rect x="12" y="98" width="104" height="5" rx="2" fill="{p["t1"]}" {TS}/>']
    o += [f'<rect x="{x}" y="78" width="10" height="18" fill="{p["t2"]}" {TS}/>'
          for x in (14, 29, 44, 92, 107)]
    o.append(f'<rect x="58" y="26" width="28" height="70" fill="{p["acc"]}" '
             f'fill-opacity="0.78" {TS}/>')
    return "".join(o)


def t_one_affordance(p):
    # Một khối có BA mấu nối giống hệt nhau ở ba cạnh — ba công dụng đều khả thi.
    # Chỉ một mấu được ghép với vật đối ứng; hai mấu kia vẽ đầy đủ nhưng bỏ trống.
    # Nội dung nằm ở chỗ ba mấu vẽ y như nhau: cái chặn không nằm trong vật, nó nằm
    # trong việc chỉ một mối ghép từng được dùng.
    # Khác `cue_lock` (thiếu đúng mảnh khớp nên KHÔNG mở được) và khác `latch`
    # (các phương án ngang giá, một cái đã cài sẵn): ở đây mảnh khớp không thiếu.
    # Bản đầu dùng MẤU LỒI ra ngoài cộng một vật đối ứng: silhouette đọc thành một
    # cỗ máy (vật thể nhận dạng được — style cấm), và mấu đã ghép dính liền vật đối
    # ứng thành một khối nên không còn thấy "ghép". Đổi sang HỐC lõm nằm trong thân:
    # ba hốc vẽ y hệt nhau, chỉ một hốc được lấp đầy.
    return (f'<rect x="34" y="34" width="60" height="60" fill="{p["t1"]}" {TS}/>'
            f'<rect x="57" y="40" width="14" height="10" fill="#FFFFFF" {TS}/>'
            f'<rect x="40" y="57" width="10" height="14" fill="#FFFFFF" {TS}/>'
            f'<rect x="78" y="57" width="10" height="14" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>')


def t_two_frames(p):
    # Hai khung y hệt nhau, mực nước ở ĐÚNG cùng một độ cao (y=64) — sự thật không
    # đổi. Khung trái tô phần DƯỚI mức, khung phải tô phần TRÊN mức: cùng một mốc,
    # một bên đọc thành "được bấy nhiêu", bên kia thành "mất bấy nhiêu".
    # Khác `contrast` (hai khối khác hình, khác chất — đối lập có thật) và khác
    # `reference_kink` (hai độ lệch quanh mốc bị xử lý ngược): ở đây chỉ có MỘT mốc
    # và không có độ lệch nào cả, chỉ có phía nào được tô.
    return (f'<rect x="16" y="30" width="42" height="68" fill="none" {TS}/>'
            f'<rect x="16" y="64" width="42" height="34" fill="{p["acc"]}" '
            f'fill-opacity="0.55" {TS}/>'
            f'<rect x="70" y="30" width="42" height="68" fill="none" {TS}/>'
            f'<rect x="70" y="30" width="42" height="34" fill="{p["acc"]}" '
            f'fill-opacity="0.55" {TS}/>')


def t_owed_reversal(p):
    # Một dãy 4 ô Y HỆT NHAU nằm CÙNG một phía của đường mốc = chuỗi kết quả đã xảy
    # ra thật. Ô thứ 5 nằm phía đối diện nhưng để RỖNG: cái "phải đến để cân bằng
    # lại" chưa hề tồn tại, và không có gì trong chuỗi sinh ra nó. Chỗ rỗng chính là
    # nội dung — quá khứ không nợ tương lai điều gì.
    # Khác `reference_kink` (hai độ lệch CÓ THẬT, bằng nhau, bị xử lý ngược nhau):
    # ở đây phía dưới không có độ lệch nào, chỉ có kỳ vọng. Ô rỗng phải CÙNG kích
    # thước với 4 ô kia — nhỏ hơn thì hình đọc thành `spectrum`.
    o = [f'<line x1="12" y1="64" x2="116" y2="64" {TNF}/>']
    o += [f'<rect x="{x}" y="34" width="17" height="26" fill="{p["acc"]}" '
          f'fill-opacity="0.78" {TS}/>' for x in (14, 35, 56, 77)]
    o.append(f'<rect x="98" y="68" width="17" height="26" fill="none" {TS}/>')
    return "".join(o)


def t_self_built(p):
    # Hai khối CÙNG kích thước = cùng một nội dung. Khối trái tô đặc và có mối ghép
    # bên trong: thứ do chính mình dựng lên từng phần. Khối phải liền một mảng, tô
    # nhạt: thứ nhận nguyên si. Dấu vết của việc TỰ TẠO là cái quyết định độ đậm.
    # Khác `granularity` (hai hình TRÒN, và bên phân giải được lại là bên NHẠT — nói
    # về độ phân giải của một lượng) và khác `effort_price` (cột đốt + khối giá trị
    # rộng gấp đôi — nói về định giá, không nói về lưu giữ).
    return (f'<rect x="16" y="34" width="44" height="60" fill="{p["acc"]}" '
            f'fill-opacity="0.72" {TS}/>'
            f'<path d="M16,54 L60,54 M16,74 L60,74 M38,34 L38,54" {TNF}/>'
            f'<rect x="70" y="34" width="44" height="60" fill="{p["t1"]}" {TS}/>')


def t_proxy_inflates(p):
    # Hai cặp cột trên cùng một đáy. Cặp trái: phép đo và mục tiêu CAO BẰNG NHAU —
    # phép đo còn là chỉ báo trung thực. Cặp phải: cột phép đo vọt lên, cột mục tiêu
    # tụt xuống. Nội dung nằm ở chỗ hai đại lượng TỪNG trùng nhau rồi tách ra đúng
    # lúc bị tối ưu — nên bắt buộc phải có trạng thái "trước".
    # Khác `ratchet` (ba bậc cao dần, bậc sau tựa bậc trước, không có trạng thái
    # trước) và khác `contrast` (hai khối khác chất, không chung mốc nào).
    return (f'<rect x="14" y="56" width="18" height="50" fill="{p["t3"]}" {TS}/>'
            f'<rect x="35" y="56" width="18" height="50" fill="{p["t1"]}" {TS}/>'
            f'<rect x="75" y="24" width="18" height="82" fill="{p["acc"]}" '
            f'fill-opacity="0.78" {TS}/>'
            f'<rect x="96" y="86" width="18" height="20" fill="{p["t1"]}" {TS}/>')


def t_one_for_all(p):
    # Một vùng = ranh giới nhóm, bên trong là các cá thể RỜI NHAU. Đúng MỘT cá thể
    # được quan sát (tô đặc); cả vùng bên trong lấy luôn sắc độ của cá thể đó.
    # Nội dung: tính chất của một mẫu bị sơn lên toàn bộ tập.
    # Khác `in_out_ring` (có chấm nằm HẲN ngoài vành — nói về ranh giới thuộc về,
    # không có gì lan ra) và khác `odd_one_out` (nền đồng nhất + một phần tử lệch:
    # cái lệch là nội dung, và nó không nhuộm ai cả).
    o = [f'<circle cx="64" cy="66" r="48" fill="{p["acc"]}" fill-opacity="0.16" {TS}/>']
    o += [f'<circle cx="{x}" cy="{y}" r="11" fill="#FFFFFF" {TS}/>'
          for x, y in ((84, 46), (44, 86), (84, 86))]
    o.append(f'<circle cx="44" cy="46" r="11" fill="{p["acc"]}" '
             f'fill-opacity="0.88" {TS}/>')
    return "".join(o)


def t_consensus_merge(p):
    # Ba vòng chồng lên nhau tới mức gần thành MỘT khối, cùng một sắc độ: các quan
    # điểm đã nhập lại làm một. Vòng thứ tư tách hẳn ra và để RỖNG — ý kiến khác
    # không bao giờ được tô vào khối đồng thuận.
    # Khác `overlap_phases` (các ellipse chồng nhau đều, không ai bị bỏ lại — nói về
    # giao thoa giai đoạn) và khác `in_out_ring` (có vành ranh giới rõ, và cái ngoài
    # vành là người ngoài nhóm chứ không phải ý kiến bị loại).
    o = [f'<circle cx="{x}" cy="{y}" r="24" fill="{p["acc"]}" fill-opacity="0.34" {TS}/>'
         for x, y in ((48, 46), (72, 46), (60, 68))]
    o.append(f'<circle cx="101" cy="97" r="13" fill="none" {TS}/>')
    return "".join(o)


def t_tint_carryover(p):
    # Bốn ô đánh giá rời nhau, TÔ CÙNG một sắc độ, không ô nào nhạt hơn ô nào. Chỉ ô
    # đầu có chấm đặc bên trong = tiêu chí duy nhất thực sự có bằng chứng. Ba ô còn
    # lại được chấm điểm y hệt mà trong ruột không có gì.
    # Khác `halo_spill` (sắc độ NHẠT DẦN khi lan ra): ở đây không nhạt đi chút nào,
    # và chính chỗ "không nhạt" mới là nội dung. Khác `salience_pop` (lưới 9 chấm,
    # vài chấm được tô — nói về độ nhìn thấy, không về suy diễn phẩm chất).
    o = [f'<rect x="{x}" y="{y}" width="34" height="34" fill="{p["acc"]}" '
         f'fill-opacity="0.42" {TS}/>'
         for x, y in ((22, 22), (72, 22), (22, 72), (72, 72))]
    o.append(f'<circle cx="39" cy="39" r="9" fill="{p["acc"]}" '
             f'fill-opacity="0.95" {TS}/>')
    return "".join(o)


def t_parsimony(p):
    # Cùng MỘT hành vi quan sát được (khối phải), hai lối giải thích dẫn tới nó: lối
    # trên phải đi qua ba mắt xích rỗng (cố ý + có động cơ + nhắm vào mình), lối dưới
    # chỉ cần một mắt xích đặc (vô tâm). Nội dung là CHÊNH LỆCH số giả định, nên hai
    # chuỗi bắt buộc phải khác hẳn nhau về số mắt.
    # Khác `divergence` (một điểm rẽ ra nhiều nhánh — chiều ngược lại) và khác
    # `funnel` (nhiều đầu vào bị một cái phễu thu hẹp, không phải hai lối song song).
    o = [f'<path d="M18,30 L96,30 L96,60 M26,92 L96,92 L96,74" {TNF}/>']
    o += [f'<circle cx="{x}" cy="30" r="8" fill="#FFFFFF" {TS}/>' for x in (18, 44, 70)]
    o.append(f'<circle cx="26" cy="92" r="9" fill="{p["acc"]}" '
             f'fill-opacity="0.82" {TS}/>')
    o.append(f'<rect x="82" y="53" width="28" height="28" fill="{p["t3"]}" {TS}/>')
    return "".join(o)


def t_regression_crossing(p):
    # Đường DỐC = năng lực thật, chạy từ việc dễ (trái, cao) xuống việc khó (phải,
    # thấp). Đường PHẲNG = mức tự đánh giá, gần như không đổi theo độ khó. Hai đường
    # cắt nhau nên hai nêm giữa chúng ĐỔI DẤU: phía dễ tự đánh giá thấp hơn thật,
    # phía khó tự đánh giá cao hơn thật. Chỗ cắt nhau là nội dung.
    # Khác `overclaim` (chỉ lệch một chiều, phần tự nhận luôn lớn hơn phần thật) và
    # khác `reference_kink` (một mốc ngang + hai ô lệch RỜI nhau, không có đường thứ
    # hai cắt qua).
    return (f'<path d="M16,30 L64,64 L16,64 Z" fill="{p["t1"]}" {TS}/>'
            f'<path d="M64,64 L112,98 L112,64 Z" fill="{p["acc"]}" '
            f'fill-opacity="0.55" {TS}/>'
            f'<path d="M16,30 L112,98" {TNF}/>'
            f'<path d="M16,64 L112,64" {TNF}/>')


def t_observed_lift(p):
    # Một dãy cột đều nhau = hành vi nền. Cung phía trên phủ đúng hai cột giữa: đó là
    # phạm vi đang bị quan sát. Hai cột nằm dưới cung cao hẳn lên và tô đặc, dù không
    # có điều kiện nào khác thay đổi. Nội dung: mức đo tăng do PHẠM VI QUAN SÁT.
    # Cung phải hở hai đầu — khép lại thành vòng thì đọc thành con mắt, đúng thứ
    # phong cách này cấm.
    # Khác `beam` (chùm dồn vào một điểm, phần còn lại tối đi — nói về chú ý của
    # chính chủ thể) và khác `ratchet`/`spectrum` (dãy tăng đơn điệu, không có mốc
    # nào đánh dấu phạm vi).
    o = [f'<path d="M40,40 A30,26 0 0 1 88,40" {TNF}/>']
    for x, h, fill, opa in ((14, 30, p["t1"], ""), (42, 52, p["acc"], ' fill-opacity="0.78"'),
                            (70, 52, p["acc"], ' fill-opacity="0.78"'), (98, 30, p["t1"], "")):
        o.append(f'<rect x="{x}" y="{106-h}" width="16" height="{h}" '
                 f'fill="{fill}"{opa} {TS}/>')
    return "".join(o)


def t_setpoint_return(p):
    # Một MỨC NỀN nằm ngang, và hai độ lệch — một lên, một xuống — đều dựng lên rất
    # dốc rồi thoải dần về đúng đường nền đó. Nội dung là cái ĐUÔI: biến cố không bị
    # xoá, nó chỉ hết tác dụng. Hai độ lệch phải NGƯỢC CHIỀU và cùng cỡ để đọc được
    # rằng cơ chế thích nghi không phân biệt tin tốt với tin xấu.
    # Khác `threshold` (đường ngang + các khối VƯỢT qua nó và ở luôn trạng thái mới):
    # ở đây không có gì vượt qua, mọi thứ quay về. Khác `rebound` (bật ngược lại phía
    # người tác động) và khác `rosy_tilt` (sự vật không đổi, chỉ sắc độ trôi theo thời
    # gian — không có mức nền nào để quay về).
    return (f'<line x1="14" y1="64" x2="114" y2="64" {TNF}/>'
            f'<path d="M26,64 L38,22 Q45,20 49,33 Q57,58 70,64 Z" '
            f'fill="{p["t3"]}" {TS}/>'
            f'<path d="M72,64 L84,106 Q91,108 95,95 Q103,70 116,64 Z" '
            f'fill="{p["t2"]}" {TS}/>')


def t_retrofit_path(p):
    # Nhiều kết cục khả dĩ đứng RỜI NHAU và CÙNG CỠ ở phía phải = trước khi biết, không
    # cái nào nổi trội. Chỉ đúng một cái được tô đặc và được nối vào một đường liền về
    # điểm khởi đầu. Nội dung: đường đó chỉ vẽ được SAU khi đã biết, nhưng vẽ rồi thì
    # trông như nó vốn là con đường duy nhất.
    # Khác `divergence` (các nêm đặc toả ra từ một điểm — nói về việc rẽ nhánh, tất cả
    # nhánh đều có thật và đều được vẽ): ở đây ba kết cục kia để RỖNG, và cái rỗng đó
    # mới là điều ta quên mất. Khác `salience_pop` (lưới đều, vài phần tử được tô — nói
    # về độ nhìn thấy) vì ở đây có một ĐƯỜNG NỐI, tức một lời giải thích nhân quả.
    o = [f'<line x1="31" y1="63" x2="88" y2="52" {TNF}/>',
         f'<circle cx="22" cy="64" r="9" fill="{p["acc"]}" fill-opacity="0.78" {TS}/>']
    o += [f'<circle cx="100" cy="{cy}" r="11" fill="none" {TS}/>'
          for cy in (22, 78, 106)]
    o.append(f'<circle cx="100" cy="50" r="11" fill="{p["acc"]}" '
             f'fill-opacity="0.78" {TS}/>')
    return "".join(o)


def t_asymmetric_probe(p):
    # Hai khối Y HỆT NHAU — cùng cỡ, cùng sắc độ — nên thực tế là đối xứng: không ai có
    # lợi thế thông tin nào. Chỉ có hai mũi thăm dò là lệch: mũi từ trái cắm sâu tới
    # tâm khối phải, mũi từ phải đứng lại giữa khoảng trống. Nội dung là ĐỘ SÂU TỰ
    # NHẬN, không phải độ sâu thật — và vì hai khối giống nhau, người xem tự thấy mũi
    # ngắn kia đáng ra phải dài bằng mũi dài.
    # Khác `mirror` (cùng MỘT sự việc soi qua hai khung quy kết — chỉ có một đối tượng):
    # ở đây có HAI chủ thể, mỗi bên tự nhận về phía bên kia. Khác `overclaim` (phạm vi
    # tự nhận lớn hơn phần thực có — một chiều, một chủ thể).
    return (f'<circle cx="34" cy="64" r="22" fill="{p["t1"]}" {TS}/>'
            f'<circle cx="94" cy="64" r="22" fill="{p["t1"]}" {TS}/>'
            f'<line x1="34" y1="54" x2="94" y2="54" {TNF}/>'
            f'<line x1="94" y1="76" x2="66" y2="76" {TNF}/>'
            f'<circle cx="34" cy="64" r="4" fill="{p["acc"]}" {TS}/>'
            f'<circle cx="94" cy="64" r="4" fill="{p["acc"]}" {TS}/>')


def t_unlinked_control(p):
    # Bên trái: một khối đặc, có thứ tự, có một mấu nối chìa ra = cái ta thao tác.
    # Bên phải: một vùng chỉ chứa các chấm nằm rải rác không theo trật tự nào = kết quả
    # ngẫu nhiên. Giữa hai thứ là một KHOẢNG TRỐNG không có gì băng qua. Nội dung nằm ở
    # chỗ thiếu: mấu nối chỉ đúng hướng, nên cảm giác điều khiển được là có thật, còn
    # mối liên kết thì không.
    # Khác `fracture` (hai phần CÓ nối nhưng lệch khớp — bất nhất): ở đây không có khớp
    # nào cả. Khác `veil` (thông tin bị che, vẫn tồn tại sau tấm che): ở đây không có gì
    # bị che, liên kết vốn không tồn tại.
    o = [f'<rect x="14" y="46" width="28" height="36" fill="{p["t3"]}" {TS}/>',
         f'<line x1="42" y1="64" x2="56" y2="64" {TNF}/>',
         f'<circle cx="92" cy="64" r="24" fill="none" {TS}/>']
    o += [f'<circle cx="{cx}" cy="{cy}" r="5" fill="{p["acc"]}" '
          f'fill-opacity="0.78" {TS}/>'
          for cx, cy in ((83, 52), (101, 57), (85, 77), (100, 74))]
    return "".join(o)


def t_hollow_chain(p):
    # Một KHUNG liền vây quanh cả dãy = lời tự nhận "tôi hiểu cơ chế này từ đầu tới
    # cuối". Bên trong, chỉ mắt đầu và mắt cuối được tô đặc; hai mắt giữa để rỗng.
    # Nội dung: cái biết được là hai đầu — hiện tượng vào và kết quả ra — còn các mắt
    # trung gian chưa bao giờ được kiểm, và chính cái khung mới khiến nó đọc thành liền
    # mạch. Bốn mắt phải CÙNG KÍCH THƯỚC, nếu không hình sẽ đọc thành `spectrum`.
    # Khác `gap_fill` (chỗ hổng được VÁ bằng vật liệu lạ): ở đây không ai vá, lỗ vẫn
    # nguyên — chỉ là không ai nhìn vào. Khác `tint_carryover` (lưới 2x2 tô cùng sắc độ,
    # nói về việc chấm điểm lây lan) vì đây là một CHUỖI có thứ tự trước–sau.
    o = [f'<rect x="14" y="38" width="100" height="52" rx="6" fill="none" {TS}/>']
    o += [f'<rect x="{x}" y="52" width="18" height="24" '
          f'fill="{p["acc"]}" fill-opacity="0.78" {TS}/>' for x in (20, 92)]
    o += [f'<rect x="{x}" y="52" width="18" height="24" fill="none" {TS}/>'
          for x in (44, 68)]
    return "".join(o)


def t_streak_projection(p):
    # Bốn kết quả CÙNG CỠ nằm trên một vạch đáy = chuỗi thắng có thật, và chúng bằng
    # nhau vì mỗi lần thử là độc lập và giống hệt nhau. Ô thứ năm để RỖNG và CAO HƠN
    # hẳn: cái được kỳ vọng ở lần tới, vừa chưa tồn tại vừa bị thổi lên quá mức. Nội
    # dung nằm ở chỗ không có gì trong bốn ô kia sinh ra chiều cao của ô thứ năm.
    # Khác `owed_reversal` (ô rỗng nằm phía ĐỐI DIỆN một đường mốc — kỳ vọng đảo chiều,
    # tức gambler's fallacy): ở đây ô rỗng nằm CÙNG phía và cao hơn, tức kỳ vọng nối
    # dài. Khác `ratchet` (các bậc cao dần và tựa lên nhau — ở đó quan hệ phụ thuộc là
    # CÓ THẬT): bốn ô ở đây phải bằng nhau tuyệt đối, nếu vẽ cao dần là đã khẳng định
    # cái mà card phủ định. Khác `echo` (nhạt và thấp dần — khuếch đại một chiều rồi
    # tắt), vì hot-hand đi lên chứ không tắt.
    o = [f'<line x1="12" y1="98" x2="116" y2="98" {TNF}/>']
    o += [f'<rect x="{x}" y="62" width="15" height="34" fill="{p["acc"]}" '
          f'fill-opacity="0.78" {TS}/>' for x in (14, 34, 54, 74)]
    o.append(f'<rect x="97" y="38" width="15" height="58" fill="none" {TS}/>')
    return "".join(o)


def t_steep_then_flat(p):
    # Năm cột trên một đường mốc, nhưng mức SỤT giữa cột 1 và cột 2 lớn hơn tổng ba
    # mức sụt còn lại. Nội dung là ĐỘ CONG: giá trị không giảm đều theo khoảng cách —
    # nó đổ sập ở đoạn gần rồi gần như nằm ngang ở đoạn xa. Chính chỗ "gần như nằm
    # ngang" giải thích được nghịch lý đảo chiều ưu tiên: dịch cả hai mốc ra xa thì
    # chênh lệch gần như biến mất, nên lựa chọn lật ngược.
    # Không dùng ramp sắc độ: thông điệp nằm ở chiều cao, thêm biến thứ hai sẽ làm
    # loãng. Khác `depletion` (có vạch mốc "mức đầy" ở trên và các cột tụt gần như ĐỀU
    # nhau — mất mát do sử dụng): ở đây không có mức đầy nào bị rút, và nhịp sụt là
    # không đều một cách có chủ ý. Khác `spectrum` (dải tròn nhạt dần, tăng/giảm ĐỀU).
    o = [f'<line x1="12" y1="102" x2="116" y2="102" {TNF}/>']
    o += [f'<rect x="{x}" y="{102-h}" width="16" height="{h}" fill="{p["acc"]}" '
          f'fill-opacity="0.72" {TS}/>'
          for x, h in ((16, 64), (38, 27), (60, 18), (82, 14), (104, 12))]
    return "".join(o)


CONCEPT_OBJECTS = dict(effort_price=t_effort_price, overclaim=t_overclaim,
                       owed_reversal=t_owed_reversal, self_built=t_self_built,
                       proxy_inflates=t_proxy_inflates, one_for_all=t_one_for_all,
                       consensus_merge=t_consensus_merge,
                       tint_carryover=t_tint_carryover, parsimony=t_parsimony,
                       regression_crossing=t_regression_crossing,
                       observed_lift=t_observed_lift,
                       base_blind=t_base_blind, locus_flip=t_locus_flip,
                       asymmetric_fade=t_asymmetric_fade,
                       from_primitives=t_from_primitives, ratchet=t_ratchet,
                       salience_pop=t_salience_pop,
                       foreground_swell=t_foreground_swell,
                       one_affordance=t_one_affordance, two_frames=t_two_frames,
                       mirror=t_mirror, in_out_ring=t_in_out_ring, balance=t_balance,
                       beam=t_beam, halo_spill=t_halo_spill, veil=t_veil,
                       fracture=t_fracture, pull=t_pull, echo=t_echo, gate=t_gate,
                       rebound=t_rebound, odd_one_out=t_odd_one_out,
                       tail_event=t_tail_event, gap_fill=t_gap_fill,
                       granularity=t_granularity, cue_lock=t_cue_lock,
                       depletion=t_depletion, foil=t_foil, latch=t_latch,
                       dilution=t_dilution, reference_kink=t_reference_kink,
                       juxtaposition=t_juxtaposition, rosy_tilt=t_rosy_tilt,
                       setpoint_return=t_setpoint_return,
                       retrofit_path=t_retrofit_path,
                       asymmetric_probe=t_asymmetric_probe,
                       unlinked_control=t_unlinked_control,
                       hollow_chain=t_hollow_chain,
                       streak_projection=t_streak_projection,
                       steep_then_flat=t_steep_then_flat)

# Quan hệ mà mỗi concept object biểu đạt — dùng khi chẩn đoán metaphor cho card.
CONCEPT_MEANING = {
    "effort_price": "công sức đã bỏ ra được đọc thành giá trị của vật — cột đốt đếm được "
                    "quyết định chiều cao khối giá trị bên cạnh",
    "overclaim":   "phạm vi tự nhận lớn hơn hẳn phần thực có, và khoảng chênh để rỗng "
                   "vì chính người trong cuộc không nhìn thấy nó",
    "mirror":      "cùng một sự việc, hai cách quy kết (mình ↔ người khác)",
    "in_out_ring": "trong nhóm ↔ ngoài nhóm; ranh giới thuộc về",
    "balance":     "đánh đổi, cán cân lệch có hướng",
    "beam":        "chú ý dồn vào một điểm, phần còn lại tối đi",
    "halo_spill":  "một ấn tượng lan sang các đánh giá lân cận",
    "veil":        "thông tin bị che khuất chứ không phải không tồn tại",
    "fracture":    "hai phần lẽ ra khớp nhau nhưng lệch — bất nhất",
    "pull":        "một khối nặng kéo lệch toàn bộ phần còn lại",
    "echo":        "lặp lại làm quen thuộc / khuếch đại dần",
    "gate":        "sàng lọc: nhiều thứ tới, ít thứ qua",
    "rebound":     "tác động bật ngược lại, kết quả đi ngược ý định ban đầu",
    "odd_one_out": "một phần tử lệch khỏi nền đồng nhất — phân biệt nhờ tương phản với phần còn lại",
    "tail_event":  "biến cố hiếm nhưng độ lớn áp đảo, nằm ngoài dải quen thuộc (đuôi phân phối)",
    "gap_fill":    "một chỗ hổng được vá bằng vật liệu lạ, khiến tổng thể đọc thành liền mạch",
    "granularity": "cùng một lượng, nhưng một bên phân giải được thành từng cá thể còn bên kia nhoè thành khối",
    "cue_lock":    "nội dung còn nguyên nhưng thiếu đúng mảnh khớp để mở ra được",
    "depletion":   "một nguồn lực hữu hạn bị rút cạn dần bởi chính việc sử dụng lặp lại",
    "foil":        "một phần tử thêm vào chỉ để làm phần tử bên cạnh trông vượt trội",
    "latch":       "các phương án ngang giá nhưng một phương án đã cài sẵn — đứng yên rẻ hơn đổi",
    "dilution":    "cùng một nghĩa vụ chia cho nhiều người, mỗi phần loãng tới mức không đủ kích hoạt",
    "reference_kink": "hai độ lệch bằng nhau quanh một đường mốc nhưng bị xử lý ngược nhau",
    "juxtaposition":  "cùng một cặp: đặt sát nhau thì chênh lệch đọc ra, tách xa thì biến mất",
    "rosy_tilt":   "sự vật không đổi, chỉ có sắc độ đánh giá nhạt/đậm dần theo trục thời gian",
    "base_blind":  "cùng một tử số đọc trên hai mẫu số khác hẳn nhau — cái nền quyết định "
                   "ý nghĩa con số lại là thứ bị nhìn xuyên qua",
    "locus_flip":  "cùng một hành vi, nguồn thúc đẩy được đặt bên trong hay bên ngoài vật",
    "asymmetric_fade": "hai dãy cùng xuất phát, một dãy phai nhanh hơn hẳn dãy kia — "
                       "chênh lệch nằm ở tốc độ phai, không ở điểm bắt đầu",
    "from_primitives": "cùng một bộ phần tử cơ bản: rời ra khi tháo, khít trong một khung "
                       "khi dựng lại — lời giải xây từ thành phần đã kiểm chứng",
    "ratchet":     "các bậc cao dần và bậc sau tựa lên vai bậc trước — bậc nhỏ đã nhận là "
                   "chỗ đứng cho bậc lớn kế tiếp",
    "salience_pop": "số lượng và vị trí không đổi, chỉ vài phần tử được tô đặc — cái tăng "
                    "lên là độ nhìn thấy, không phải tần suất",
    "foreground_swell": "một phần tử phình to trong khi dãy đều đặn vẫn chạy tiếp ở cả hai "
                        "phía — cỡ nó chiếm trong dự đoán, không phải cỡ thật",
    "one_affordance": "một vật có nhiều mấu nối như nhau nhưng chỉ một mối ghép từng được "
                      "dùng — cái chặn nằm trong thói quen, không trong vật",
    "two_frames":  "cùng một mốc, một bên tô phần dưới, bên kia tô phần trên — được hay mất "
                   "chỉ là phía nào được kể",
    "owed_reversal": "một chuỗi kết quả có thật dồn về một phía của mốc, và một ô rỗng ở phía "
                     "đối diện — cái 'đến lượt phải đổi chiều' chưa hề tồn tại",
    "self_built":  "cùng một nội dung qua hai lối: thứ tự mình dựng lên từng phần giữ được "
                   "dấu vết, thứ nhận nguyên si thì nhạt",
    "proxy_inflates": "phép đo và mục tiêu từng cao bằng nhau, rồi tách hẳn ra khi phép đo bị "
                      "lấy làm đích — chỉ số vọt lên trong lúc mục tiêu tụt xuống",
    "one_for_all": "tính chất của đúng một cá thể được quan sát bị sơn lên toàn bộ vùng chứa "
                   "nó — mẫu một người, kết luận cả nhóm",
    "consensus_merge": "nhiều quan điểm chồng lên nhau tới mức thành một khối đồng sắc, và "
                       "phần tử không nhập vào thì bị bỏ rỗng ngoài rìa",
    "tint_carryover": "nhiều ô đánh giá cùng một sắc độ nhưng chỉ một ô có bằng chứng bên "
                      "trong — các ô kia được chấm điểm y hệt mà ruột rỗng",
    "parsimony":   "cùng một hệ quả, hai lối giải thích khác hẳn nhau về số mắt xích giả định",
    "regression_crossing": "hai đường cắt nhau nên độ lệch đổi dấu qua điểm cắt — một phía "
                           "đánh giá cao hơn thật, phía kia thấp hơn thật",
    "observed_lift": "một dãy đều nhau, riêng phần nằm trong phạm vi được quan sát thì cao "
                     "hẳn lên — mức đo đổi vì bị nhìn, không vì điều kiện đổi",
    "setpoint_return": "hai độ lệch ngược chiều quanh một mức nền, cả hai đều dốc lên rồi "
                       "thoải về đúng mức nền — biến cố hết tác dụng chứ không bị xoá",
    "retrofit_path": "nhiều kết cục khả dĩ cùng cỡ, chỉ cái đã xảy ra được tô đặc và nối vào "
                     "một đường liền về điểm đầu — đường chỉ vẽ được sau khi đã biết",
    "asymmetric_probe": "hai chủ thể y hệt nhau, nhưng mũi thăm dò một bên cắm sâu hơn hẳn "
                        "bên kia — chênh lệch nằm ở độ sâu tự nhận, không ở thực tế",
    "unlinked_control": "một mấu nối chỉ đúng hướng vào vùng kết quả ngẫu nhiên nhưng không "
                        "có gì băng qua khoảng trống — liên kết vốn không tồn tại",
    "hollow_chain": "một khung liền vây quanh cả chuỗi nhưng chỉ hai mắt đầu–cuối được tô, "
                    "các mắt giữa để rỗng — cái khung khiến nó đọc thành liền mạch",
    "streak_projection": "một chuỗi kết quả bằng nhau và một ô rỗng CÙNG phía nhưng cao hơn "
                         "hẳn — kỳ vọng nối dài chuỗi, mà không gì trong chuỗi sinh ra nó",
    "steep_then_flat": "mức sụt ở đoạn gần lớn hơn tổng các mức sụt còn lại, rồi gần như nằm "
                       "ngang ở đoạn xa — độ cong, không phải độ giảm",
}

THUMB_REGISTRY.update(CONCEPT_OBJECTS)


# --------------------------------------------------------------------------
# Batch 2026-09-16 — 9 concept object mới.
# Lý do phải mở thêm nhiều: xlsx gán 9/10 card của batch này là `branching`
# (-> divergence) và 1 là `nesting`. Không card nào là "một điểm rẽ nhiều nhánh".
# Sau khi chẩn đoán lại theo `back`, các quan hệ cần vẽ (tự sinh nhưng gán ra
# ngoài · rò rỉ tín hiệu qua một ranh giới · ngoại suy vượt dữ liệu · chỉ đếm một
# ô của bảng 2x2 · tất cả đều trên mức trung bình · lặp lại bản sao rỗng · tấm đệm
# không được tính · dự báo phóng đại trên CẢ hai trục · sắc độ nhóm sơn lên cá thể)
# đều không có trong 62 hình sẵn có, và các hình gần nghĩa nhất (locus_flip, veil,
# overclaim, echo, base_blind, one_for_all) đã kín cả hai hue.
# --------------------------------------------------------------------------


def t_outward_credit(p):
    # Một khối = bản thân, và chấm ĐẶC nằm BÊN TRONG nó: cảm giác/lựa chọn thực sự
    # do chính mình sinh ra. Mối nối chạy LÊN TRÊN tới một vòng RỖNG = tác nhân bên
    # ngoài được ghi công. Nội dung nằm ở sự lệch pha giữa hai chỗ: chỗ đặc là nguồn
    # thật, chỗ rỗng là nơi nhận công.
    # Bố cục DỌC là có chủ ý — `locus_flip` (hai khung vuông cạnh nhau, chấm trong /
    # chấm ngoài) nói cùng một hành vi được quy nguồn vào trong hay ra ngoài; ở đây
    # nguồn đã xác định là bên trong, và cái được thêm vào là một tác nhân KHÔNG CÓ
    # THẬT. Khác `unlinked_control` (khoảng trống không ai băng qua): ở đây mối nối
    # có thật, chỉ có phía nhận là rỗng.
    # Vòng rỗng đặt CHÉO lên góc trên-phải, không đặt thẳng trục: bản dựng đầu để nó
    # ngay trên đỉnh khối và nối bằng một đoạn dọc — ở khổ lớn hình đó đọc thành cái
    # kẹo mút / một dáng người có đầu, tức vật thể nhận dạng được (vi phạm Step 6).
    return (f'<rect x="16" y="58" width="62" height="48" fill="{p["t1"]}" {TS}/>'
            f'<circle cx="47" cy="82" r="13" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<line x1="70" y1="62" x2="88" y2="44" {TNF}/>'
            f'<circle cx="99" cy="33" r="16" fill="none" {TS}/>')


def t_signal_leak(p):
    # Trái: khối tô ĐẶC = cường độ nội tâm cảm nhận được, đầy. Đường dọc giữa khung
    # = ranh giới trong–ngoài (da mặt, giọng nói). Phải: khung RỖNG lớn = lượng mà ta
    # tin là người khác đọc được, với một chấm nhỏ ở giữa = lượng thực sự lọt ra.
    # Nội dung là khoảng rỗng giữa chấm nhỏ và khung lớn, và nó nằm ở PHÍA BÊN KIA
    # một ranh giới — đó là thứ phân biệt card này với overclaim thuần tuý.
    # Khác `veil` (thông tin bị che khỏi NGƯỜI KHÁC nhìn vào): ở đây không ai che gì,
    # vấn đề là ta ước lượng sai độ trong suốt của chính mình. Khác `over_scaled_forecast`
    # (không có ranh giới, và phần thật nằm ở GÓC vì lệch trên cả hai trục).
    return (f'<rect x="12" y="34" width="34" height="60" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>'
            f'<line x1="56" y1="20" x2="56" y2="108" {TNF}/>'
            f'<rect x="68" y="34" width="46" height="60" fill="none" {TS}/>'
            f'<circle cx="91" cy="64" r="7" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>')


def t_fitted_overreach(p):
    # Năm điểm nằm trên một đường THẲNG HOÀN HẢO — độ mạch lạc của dữ liệu, chính là
    # thứ sinh ra cảm giác tự tin. Đường khớp qua chúng KHÔNG dừng ở điểm cuối mà chạy
    # tiếp tới mép khung, và đoạn chạy tiếp đó không có điểm nào bên dưới. Nội dung:
    # sự tự tin kéo dài ra ngoài phạm vi mà mẫu hình bảo chứng, và nó tự tin ĐƯỢC chính
    # vì mẫu hình quá gọn.
    # Các điểm phải thẳng tuyệt đối — vẽ lệch một chút là mất luận điểm "dễ kể thành
    # câu chuyện". Khác `regression_crossing` (hai đường cắt nhau, độ lệch đổi dấu) và
    # khác `ratchet` (các bậc rời, bậc sau tựa bậc trước).
    # Đường khớp bắt đầu ĐÚNG ở điểm đầu tiên và chỉ kéo dài về PHÍA TRƯỚC. Bản dựng
    # đầu cho nó thò ra cả hai đầu, làm đoạn thừa phía sau đọc thành nhiễu và loãng
    # mất luận điểm (chỉ đoạn vượt quá điểm cuối mới là phần không có dữ liệu đỡ).
    # Điểm vẽ SAU đường để đường không cắt ngang qua giữa chấm.
    o = [f'<line x1="20" y1="96" x2="118" y2="20" {TNF}/>']
    o += [f'<circle cx="{x}" cy="{y}" r="6" fill="{p["acc"]}" '
          f'fill-opacity="0.82" {TS}/>'
          for x, y in ((20, 96), (38, 82), (56, 69), (74, 55), (92, 42))]
    return "".join(o)


def t_one_cell_counted(p):
    # Bảng 2x2 đủ bốn ô, bốn ô BẰNG NHAU vì cả bốn đều xảy ra thật. Chỉ ô "có X và có
    # Y" được tô; ba ô còn lại để rỗng vì chưa bao giờ được đếm. Hai vạch đậm ở mép
    # trên và mép trái đánh dấu đúng hàng/cột đã được chú ý.
    # Nội dung nằm ở BA ô rỗng: mối liên hệ chỉ tồn tại khi bỏ qua chúng — đúng phần
    # `strategy` của card ("đếm cả những lần X xảy ra mà KHÔNG có Y").
    # Khác `tint_carryover` (lưới 2x2 tô CÙNG sắc độ cả bốn ô — nói về chấm điểm lây
    # lan) và khác `odd_one_out` (một DÃY đồng nhất với một phần tử lệch).
    o = [f'<rect x="{x}" y="{y}" width="40" height="40" fill="none" {TS}/>'
         for x, y in ((20, 24), (70, 24), (20, 74), (70, 74))]
    o.append(f'<rect x="20" y="24" width="40" height="40" fill="{p["acc"]}" '
             f'fill-opacity="0.82" {TS}/>')
    # Bản dựng đầu có thêm hai vạch đánh dấu hàng/cột đã được chú ý; ở khổ lớn chúng
    # đọc thành vệt thừa chứ không thành nhãn, nên bỏ. Lưới 2x2 với ĐÚNG một ô được
    # tô đã là chữ ký riêng — không hình nào khác trong registry có dạng này.
    return "".join(o)


def t_all_above_median(p):
    # Một đường mốc = mức trung bình. TẤT CẢ các chấm đều nằm phía trên nó, và nửa
    # dưới để trống hoàn toàn. Nội dung là chỗ trống đó: nếu mọi người đều tự chấm
    # mình trên trung bình thì phân bố này không thể tồn tại — bất khả về mặt thống kê
    # chứ không phải chỉ là "hơi lạc quan".
    # Chiều cao các chấm phải KHÁC nhau (người ta không tự cho mình bằng nhau), nhưng
    # không chấm nào được chạm hay vượt xuống dưới đường mốc.
    # Khác `salience_pop` (lưới 9 chấm, vài chấm được tô — nói về độ nhìn thấy) và
    # khác `owed_reversal` (dãy ô một phía + MỘT ô rỗng phía đối diện).
    o = [f'<line x1="12" y1="76" x2="116" y2="76" {TNF}/>']
    o += [f'<circle cx="{x}" cy="{y}" r="8" fill="{p["acc"]}" '
          f'fill-opacity="0.80" {TS}/>'
          for x, y in ((20, 56), (42, 40), (64, 54), (86, 38), (108, 50))]
    return "".join(o)


def t_stacked_copies(p):
    # Ba bản sao Y HỆT NHAU về kích thước và sắc độ, lệch nhau một quãng đều. Mỗi bản
    # tô rất nhạt — tự nó không mang thêm bằng chứng nào. Chỗ cả ba chồng lên nhau thì
    # đậm hẳn: cảm giác "đúng" sinh ra từ SỐ LẦN gặp lại, không từ nội dung của bất kỳ
    # lần nào. Ba hình bắt buộc phải cùng cỡ; vẽ to dần là đã khẳng định có thêm thông
    # tin, tức phủ định đúng điểm của card.
    # Khác `echo` (nhạt và thấp dần — khuếch đại một chiều rồi tắt) và khác
    # `consensus_merge` (các vòng nhập thành một khối + một phần tử bị bỏ rỗng ngoài
    # rìa, nói về áp lực nhóm chứ không về sự lặp lại).
    return "".join(f'<rect x="{x}" y="{x}" width="56" height="56" fill="{p["acc"]}" '
                   f'fill-opacity="0.30" {TS}/>' for x in (20, 36, 52))


def t_unseen_cushion(p):
    # Khối đặc ở trên = cú sốc đang rơi. Dải RỖNG ở giữa = cơ chế đối phó/hợp lý hoá,
    # có thật và sẽ đỡ lấy cú rơi, nhưng vẽ rỗng vì nó không có mặt trong dự báo. Đường
    # dưới cùng = mức mà ta dự đoán mình sẽ chạm tới. Nội dung là khoảng cách giữa đáy
    # dải đệm và đường đó: phần dự báo sai, đúng bằng phần bị bỏ quên.
    # Khác `threshold` (vượt mốc thì đổi trạng thái) và khác `latch` (bức tường công
    # sức chặn việc ĐỔI): ở đây không có gì bị chặn, chỉ có một lực đỡ không được tính.
    # Khác `setpoint_return` (hedonic-treadmill, mint) vốn vẽ đường hồi về mức nền —
    # ở đó sự hồi phục được vẽ ra, còn ở đây cái phải thấy là nó bị BỎ QUA.
    return (f'<rect x="44" y="18" width="40" height="30" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>'
            f'<rect x="20" y="62" width="88" height="20" fill="none" {TS}/>'
            f'<line x1="14" y1="104" x2="114" y2="104" {TNF}/>')


def t_over_scaled_forecast(p):
    # Khung RỖNG lớn = cảm xúc được dự báo, phóng đại trên CẢ hai trục: rộng (kéo dài
    # bao lâu) và cao (mạnh tới đâu). Khối đặc nhỏ nằm ở GÓC, chung đúng góc gốc với
    # khung = trải nghiệm thật. Chung gốc là bắt buộc: hai thứ xuất phát từ cùng một
    # sự kiện, chỉ khác nhau ở quy mô được gán.
    # Khác `overclaim` (phần đặc trải HẾT bề ngang ở đáy — chỉ lệch trên MỘT trục,
    # dùng cho Dunning-Kruger và false-consensus): ở đây lệch trên hai trục vì card
    # nói rõ cả "length" lẫn "intensity". Khác `signal_leak` (có ranh giới dọc và chấm
    # nằm giữa khung, nói về cái lọt ra ngoài chứ không về quy mô dự báo).
    return (f'<rect x="16" y="22" width="96" height="84" fill="none" {TS}/>'
            f'<rect x="16" y="80" width="30" height="26" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>')


def t_group_tint_applied(p):
    # Trái: một cụm phần tử nhỏ, tất cả cùng một sắc độ = phẩm chất được gán cho cả
    # nhóm. Phải: MỘT phần tử lớn hơn, tô CHÍNH sắc độ đó, nhưng ruột là một ô rỗng —
    # không có quan sát nào về riêng người này. Mối nối chạy từ cụm sang cá thể để chỉ
    # rõ sắc độ đến từ đâu.
    # Đây là chiều NGƯỢC của `one_for_all` (mint, group-attribution-error): ở đó một cá
    # thể được quan sát rồi sơn lên cả vùng; ở đây cả vùng chưa chắc được quan sát mà
    # sắc độ của nó vẫn chảy ngược vào một cá thể. Khác `halo_spill` (sắc độ nhạt dần
    # khi lan): ở đây sắc độ sang tới cá thể KHÔNG nhạt đi chút nào.
    o = [f'<rect x="{x}" y="{y}" width="18" height="18" fill="{p["acc"]}" '
         f'fill-opacity="0.55" {TS}/>'
         for x, y in ((14, 32), (36, 32), (14, 56), (36, 56))]
    o.append(f'<line x1="58" y1="51" x2="76" y2="51" {TNF}/>')
    o.append(f'<rect x="78" y="30" width="36" height="42" fill="{p["acc"]}" '
             f'fill-opacity="0.55" {TS}/>')
    o.append(f'<rect x="88" y="40" width="16" height="22" fill="#FFFFFF" {TS}/>')
    return "".join(o)


CONCEPT_OBJECTS_20260916 = dict(
    outward_credit=t_outward_credit, signal_leak=t_signal_leak,
    fitted_overreach=t_fitted_overreach, one_cell_counted=t_one_cell_counted,
    all_above_median=t_all_above_median, stacked_copies=t_stacked_copies,
    unseen_cushion=t_unseen_cushion,
    over_scaled_forecast=t_over_scaled_forecast,
    group_tint_applied=t_group_tint_applied,
)

CONCEPT_MEANING.update({
    "outward_credit": "cảm giác sinh ra bên trong nhưng công được ghi cho một tác nhân "
                      "bên ngoài vốn rỗng",
    "signal_leak": "nội tâm đầy, phần lọt qua ranh giới thì nhỏ xíu, nhưng phạm vi tự "
                   "cho là người khác đọc được lại lớn",
    "fitted_overreach": "các điểm thẳng hàng hoàn hảo và đường khớp chạy tiếp ra ngoài "
                        "vùng có dữ liệu — mạch lạc sinh ra tự tin, không sinh ra độ chính xác",
    "one_cell_counted": "bảng 2x2 đủ bốn ô nhưng chỉ ô đồng xuất hiện được tô — liên hệ "
                        "chỉ tồn tại khi ba ô kia không được đếm",
    "all_above_median": "mọi phần tử đều nằm trên đường trung bình và nửa dưới bỏ trống — "
                        "một phân bố không thể tồn tại",
    "stacked_copies": "nhiều bản sao y hệt, mỗi bản rỗng như nhau, chỗ chồng lên nhau thì "
                      "đậm — độ tin đến từ số lần gặp lại",
    "unseen_cushion": "một lực đỡ có thật nằm giữa cú rơi và mức dự đoán, nhưng vẽ rỗng vì "
                      "nó không có mặt trong dự báo",
    "over_scaled_forecast": "khung dự báo phóng đại trên cả hai trục (kéo dài bao lâu và "
                            "mạnh tới đâu) so với khối trải nghiệm thật chung gốc",
    "group_tint_applied": "sắc độ của cả nhóm chảy nguyên vẹn vào một cá thể mà ruột cá thể "
                          "đó không có quan sát nào",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260916)


def thumb(name, hue="mint"):
    """SVG 128x128, nền paper (trắng), tint ladder theo hue của card."""
    p = _pal(hue, paper_bg=True)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" '
            'width="128" height="128">'
            f'<rect width="128" height="128" fill="#FFFFFF"/>'
            f'{THUMB_REGISTRY[name](p)}</svg>')
