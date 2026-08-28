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


CONCEPT_OBJECTS = dict(mirror=t_mirror, in_out_ring=t_in_out_ring, balance=t_balance,
                       beam=t_beam, halo_spill=t_halo_spill, veil=t_veil,
                       fracture=t_fracture, pull=t_pull, echo=t_echo, gate=t_gate,
                       rebound=t_rebound, odd_one_out=t_odd_one_out,
                       tail_event=t_tail_event)

# Quan hệ mà mỗi concept object biểu đạt — dùng khi chẩn đoán metaphor cho card.
CONCEPT_MEANING = {
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
}

THUMB_REGISTRY.update(CONCEPT_OBJECTS)


def thumb(name, hue="mint"):
    """SVG 128x128, nền paper (trắng), tint ladder theo hue của card."""
    p = _pal(hue, paper_bg=True)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" '
            'width="128" height="128">'
            f'<rect width="128" height="128" fill="#FFFFFF"/>'
            f'{THUMB_REGISTRY[name](p)}</svg>')
