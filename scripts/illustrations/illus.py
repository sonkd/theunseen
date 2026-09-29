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


def t_unattended_object(p):
    # Một vòng LỚN, chiếm gần hết khung, vẽ RỖNG hoàn toàn: vật thể hiện diện đầy đủ
    # trong tầm mắt, kích thước không thể bỏ sót, nhưng không nhận được một nét mực nào.
    # Cụm ô nhỏ đặc nằm BÊN TRONG vòng đó = nhiệm vụ đang được đếm. Nội dung nằm ở chỗ
    # cả hai ở CÙNG một trường nhìn: cái lớn không bị che, không nằm ngoài rìa, nó chỉ
    # không được chú ý tới.
    # Khác `beam` (attentional-bias mint / change-blindness amber) vốn vẽ nón sáng từ một
    # nguồn — ở đó có hướng chiếu; tại đây không có nguồn nào, chỉ có phần được tô và
    # phần không. Khác `veil` (có tấm che thật) và khác `nested_scope` (nhiều vòng đồng tâm).
    o = [f'<circle cx="64" cy="64" r="46" fill="none" {TS}/>']
    o += [f'<rect x="{x}" y="82" width="15" height="15" fill="{p["acc"]}" '
          f'fill-opacity="0.85" {TS}/>' for x in (40, 58, 76)]
    return "".join(o)


def t_inert_input(p):
    # Hai cột đầu vào CHÊNH LỆCH hẳn về khối lượng, nhưng hai ô kết quả phía trên thì
    # y hệt nhau về cỡ VÀ nằm đúng cùng một độ cao. Đường mốc ngang khoá hai ô đó lại
    # để thấy rõ chúng không hề xê dịch. Nội dung: đổ thêm bao nhiêu thông tin vào cũng
    # không làm kết luận nhích đi một milimet.
    # Khác `depletion` (nguồn lực vơi dần) và khác `echo` (dãy nhạt dần): ở đây cái
    # KHÔNG đổi mới là điểm, nên hai ô kết quả bắt buộc phải vẽ giống hệt nhau.
    return (f'<line x1="14" y1="32" x2="114" y2="32" {TNF}/>'
            f'<rect x="28" y="24" width="17" height="17" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="83" y="24" width="17" height="17" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="24" y="72" width="25" height="36" fill="{p["t2"]}" {TS}/>'
            f'<rect x="79" y="52" width="25" height="56" fill="{p["t2"]}" {TS}/>')


def t_spread_by_n(p):
    # Một trục dọc = giá trị thật. Hàng trên: BA chấm, văng xa trục về cả hai phía.
    # Hàng dưới: NĂM chấm nhỏ hơn, bám sát trục. Cùng một hiện tượng, chỉ khác cỡ mẫu —
    # mẫu nhỏ dao động rộng hơn hẳn mẫu lớn. Nội dung là chỗ ta đọc hai hàng như nhau.
    # Số chấm mỗi hàng phải khác nhau và ĐỘ VĂNG phải khác nhau; nếu chỉ khác số lượng
    # thì hình đọc thành `granularity` (phân giải thô/mịn) chứ không thành phương sai.
    o = [f'<line x1="64" y1="16" x2="64" y2="112" {TNF}/>']
    o += [f'<circle cx="{x}" cy="36" r="8" fill="{p["acc"]}" fill-opacity="0.80" {TS}/>'
          for x in (20, 66, 108)]
    o += [f'<circle cx="{x}" cy="92" r="6" fill="{p["acc"]}" fill-opacity="0.80" {TS}/>'
          for x in (38, 51, 64, 77, 90)]
    return "".join(o)


def t_negative_space(p):
    # Khung = không gian phương án. Ba khối đặc ÁP SÁT mép khung = các kết cục phải
    # tránh, thứ duy nhất được vẽ ra. Lời giải là khoảng rỗng hình chữ L còn lại —
    # cố ý KHÔNG vẽ, vì phương pháp này không đi tìm nó, nó chỉ loại trừ phần còn lại.
    # Các khối bắt buộc dính mép khung: rời ra khỏi mép thì hình đọc thành
    # `page_structure` (khối nội dung có lề trong một bố cục) thay vì vùng cấm.
    o = [f'<rect x="18" y="18" width="92" height="92" fill="none" {TS}/>']
    o += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{p["acc"]}" '
          f'fill-opacity="0.78" {TS}/>'
          for x, y, w, h in ((18, 18, 44, 34), (76, 18, 34, 50), (18, 74, 52, 36))]
    return "".join(o)


def t_deserved_backfill(p):
    # Cột PHẢI: hai khối đặc = cái thực sự quan sát được (ai bị phạt, ai được thưởng).
    # Cột TRÁI: hai ô RỖNG, cỡ khớp chính xác từng khối bên phải = phẩm chất đạo đức
    # được suy ngược ra từ kết cục. Vẽ rỗng vì nó chưa từng được quan sát: thế giới
    # công bằng đòi mỗi kết cục phải có một mức xứng đáng đi kèm, nên ô đó luôn được
    # lấp cho vừa. Không cặp nào lệch — chính sự khít tuyệt đối là cái sai.
    # Khác `mirror` (cùng một sự việc soi qua hai khung quy kết) vì ở đây hai cột là
    # hai THỨ khác nhau: một cái đo được, một cái suy ra. Rỗng = chưa quan sát, đúng
    # idiom đã dùng ở `unseen_cushion` và `group_tint_applied`.
    o = []
    for y in (24, 74):
        o.append(f'<rect x="18" y="{y}" width="34" height="30" fill="none" {TS}/>')
        o.append(f'<rect x="76" y="{y}" width="34" height="30" fill="{p["acc"]}" '
                 f'fill-opacity="0.82" {TS}/>')
        o.append(f'<line x1="52" y1="{y+15}" x2="76" y2="{y+15}" {TNF}/>')
    return "".join(o)


def t_narrative_tilt(p):
    # Một khối nặng ở mép trái = câu chuyện đã được chấp nhận. Ba thanh bên phải có
    # CÙNG cỡ và CÙNG khoảng cách, chỉ khác góc nghiêng: càng gần khối nặng càng ngả
    # về phía nó. Sự kiện mới không bị kéo dịch chỗ, nó bị xoay CÁCH DIỄN GIẢI.
    # Khác `pull` (anchoring mint / bandwagon amber) vốn giữ nguyên hướng các vệ tinh
    # và bóp hẹp KHOẢNG CÁCH — ở đó cái lệch là vị trí ước lượng; ở đây vị trí không
    # đổi chút nào, cái lệch là phương hướng.
    o = [f'<circle cx="32" cy="64" r="24" fill="{p["acc"]}" fill-opacity="0.68" {TS}/>']
    o += [f'<rect x="{x}" y="47" width="10" height="34" fill="{p["t2"]}" '
          f'transform="rotate({a} {x + 5} 64)" {TS}/>'
          for x, a in ((66, -38), (86, -22), (104, -8))]
    return "".join(o)


def t_forced_fit(p):
    # Trên trái: một vòng tròn nhỏ vẽ rỗng = bài toán ở hình dạng vốn có của nó.
    # Giữa: khung VUÔNG = công cụ quen tay. Khối bên trong là chính vòng tròn đó, phóng
    # to rồi CẮT PHẲNG bốn cạnh theo khung — bốn cạnh thẳng, bốn góc còn cong, dấu vết
    # của việc bị ép. Vấn đề bị bẻ cho vừa công cụ, không phải công cụ được chọn cho vừa
    # vấn đề.
    # Khác `one_affordance` (functional-fixedness amber) vốn nói về vật có nhiều mấu nối
    # mà chỉ một mối từng dùng — ở đó vật không hề biến dạng. Khác `gate` (lọc bớt số
    # lượng): tại đây không có gì bị chặn lại, chỉ có hình dạng bị đổi.
    cid = f"tfit{next(_uid)}"
    return (f'<circle cx="23" cy="23" r="10" fill="none" {TS}/>'
            f'<clipPath id="{cid}"><rect x="36" y="36" width="56" height="56"/></clipPath>'
            f'<circle cx="64" cy="64" r="34" fill="{p["acc"]}" fill-opacity="0.72" '
            f'clip-path="url(#{cid})"/>'
            f'<rect x="36" y="36" width="56" height="56" fill="none" {TS}/>')


def t_inverse_weight(p):
    # Đường mốc ngang chia hai đại lượng. TRÊN mốc = tầm quan trọng thật. DƯỚI mốc =
    # thời gian đem ra bàn. Cặp trái: quan trọng lớn — bàn một tí. Cặp phải: quan trọng
    # tí xíu — bàn rất lâu. Hai cặp bắt chéo nhau về cỡ; chính thế bắt chéo là nội dung.
    # Hai khối trên bắt buộc chạm đúng đường mốc để so chiều cao đọc được ngay.
    # Khác `contrast` (hai khối đối lập rời nhau, không có đại lượng nào được đo) và
    # khác `proportion` (phần trên tổng, một vòng donut).
    # Hai khối trên dùng chung mép đáy y=58, hai khối dưới dùng chung mép trên y=70:
    # chung mép mới so chiều cao được. Chừa 6px hai bên đường mốc — bản đầu để khối
    # dính sát đường, ở khổ 64px cả cụm dính thành một vệt đen liền.
    return (f'<line x1="14" y1="64" x2="114" y2="64" {TNF}/>'
            f'<rect x="20" y="18" width="40" height="40" fill="{p["acc"]}" '
            f'fill-opacity="0.75" {TS}/>'
            f'<rect x="20" y="70" width="40" height="14" fill="{p["t2"]}" {TS}/>'
            f'<rect x="70" y="44" width="38" height="14" fill="{p["acc"]}" '
            f'fill-opacity="0.75" {TS}/>'
            f'<rect x="70" y="70" width="38" height="40" fill="{p["t2"]}" {TS}/>')


def t_unused_exit(p):
    # Một vùng kín, nhưng tường phải có một KHOẢNG HỞ vẽ rõ ràng — lối ra có thật và
    # đang mở. Khối đặc nằm nép sát tường đối diện, xa lối ra nhất có thể. Không có gì
    # chặn nó lại; cái chặn đã chuyển vào bên trong sau chuỗi lần thử vô ích.
    # Khoảng hở bắt buộc nằm trên tường, không phải ở góc: hở ở góc thì đọc thành khung
    # vẽ dở. Khác `gate` (khe hẹp, nhiều tới ít qua — ở đó việc đi qua vẫn đang diễn ra)
    # và khác `nested_scope` (vòng chứa vòng, không có lối ra nào).
    return (f'<path d="M98,50 L98,26 L30,26 L30,102 L98,102 L98,78" fill="none" {TS}/>'
            f'<circle cx="49" cy="64" r="14" fill="{p["acc"]}" fill-opacity="0.82" {TS}/>')


CONCEPT_OBJECTS_20260917 = dict(
    unattended_object=t_unattended_object, inert_input=t_inert_input,
    spread_by_n=t_spread_by_n, negative_space=t_negative_space,
    deserved_backfill=t_deserved_backfill, narrative_tilt=t_narrative_tilt,
    forced_fit=t_forced_fit, inverse_weight=t_inverse_weight,
    unused_exit=t_unused_exit,
)

CONCEPT_MEANING.update({
    "unattended_object": "một vật lớn hiện diện đầy đủ trong khung nhưng vẽ rỗng, cạnh "
                         "cụm nhỏ đặc đang được đếm — không bị che, chỉ không được chú ý",
    "inert_input": "hai khối đầu vào chênh lệch hẳn nhưng hai ô kết quả y hệt nhau và "
                   "cùng một độ cao — thêm thông tin không làm kết luận xê dịch",
    "spread_by_n": "cùng một trục, hàng ít phần tử thì văng rộng, hàng nhiều phần tử thì "
                   "bám sát — dao động phụ thuộc cỡ mẫu",
    "negative_space": "các vùng phải tránh được tô đặc áp sát mép khung, lời giải là "
                      "khoảng rỗng còn lại và cố ý không được vẽ",
    "deserved_backfill": "cột kết cục quan sát được thì đặc, cột phẩm chất suy ngược ra "
                         "thì rỗng nhưng khít từng cặp — sự khít tuyệt đối mới là cái sai",
    "narrative_tilt": "một khối nặng và dãy thanh cùng cỡ cùng khoảng cách, chỉ góc nghiêng "
                      "tăng dần khi lại gần — cái bị kéo là cách diễn giải, không phải vị trí",
    "forced_fit": "một hình tròn bị cắt phẳng bốn cạnh theo khung vuông bao quanh nó — "
                  "vấn đề bị bẻ cho vừa công cụ",
    "inverse_weight": "hai cặp đại lượng bắt chéo quanh một đường mốc: quan trọng lớn ứng "
                      "với bàn ít, quan trọng nhỏ ứng với bàn nhiều",
    "unused_exit": "một vùng kín có khoảng hở rõ ràng trên tường và khối đặc nép ở tường "
                   "đối diện — lối ra mở nhưng không được dùng",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260917)


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


# --------------------------------------------------------------------------
# batch 2026-09-18 — mười card L/M. xlsx gán 6/10 là `hierarchy`; không card nào
# trong batch có quan hệ cha–con. Mọi hình sát nghĩa sẵn có đều đã kín cả hai hue
# (chi tiết trong OVERRIDES của render_thumbs.py), nên viết mười hình mới.
# --------------------------------------------------------------------------

def t_rank_reversal(p):
    # Đường dọc chia hai CHẾ ĐỘ đánh giá. Cùng một cặp (vòng nhỏ / vòng lớn), cỡ giữ
    # y nguyên ở cả hai bên. Chiều cao = mức được đánh giá; tô đặc = bên thắng.
    # Trái (đánh giá riêng lẻ): vòng NHỎ ở trên và đặc. Phải (so cạnh nhau): vòng LỚN
    # ở trên và đặc. Thứ hạng lật hẳn dù không có gì về hai lựa chọn thay đổi.
    # Khác `juxtaposition` (distinction-bias amber / empathy-gap mint) vốn giữ nguyên
    # chiều cao và chỉ đổi KHOẢNG CÁCH — ở đó cái hiện ra là chênh lệch, không phải
    # sự đảo ngôi. Khác `contrast` (hai khối khác chất, không có ai hơn ai).
    return (f'<line x1="64" y1="16" x2="64" y2="112" {TNF}/>'
            f'<circle cx="34" cy="38" r="12" fill="{p["acc"]}" fill-opacity="0.82" {TS}/>'
            f'<circle cx="34" cy="88" r="19" fill="none" {TS}/>'
            f'<circle cx="95" cy="44" r="19" fill="{p["acc"]}" fill-opacity="0.82" {TS}/>'
            f'<circle cx="95" cy="95" r="12" fill="none" {TS}/>')


def t_fewer_louder(p):
    # Hàng trên: NĂM thanh bằng nhau = bộ chi tiết của bản gốc. Hàng dưới: chỉ còn HAI
    # thanh, và thanh cao nhất vượt hẳn mọi thanh ở hàng trên. Hai chiều biến đổi cùng
    # lúc trong một lần kể lại: số chi tiết rụng đi (leveling) và vài chi tiết bị đẩy
    # cao lên (sharpening). Thiếu một trong hai thì mất nửa luận điểm.
    # Khác `asymmetric_fade` (hai dãy CÙNG số ô, chỉ sắc độ phai khác nhau) và khác
    # `foreground_swell` (một dãy đều liên tục ở CẢ HAI phía khối lớn — ở đó dãy nền
    # không hề rụng bớt). Khác `depletion`: ở đây có thứ CAO LÊN, không chỉ vơi đi.
    # Khe giữa hai hàng phải ≥14px: bản đầu để thanh cao bắt đầu ở y=48 trong khi hàng
    # trên kết ở y=44, ở khổ 64px hai hàng dính thành một cụm và mất hẳn nhịp "kể lại".
    o = [f'<rect x="{x}" y="18" width="14" height="20" fill="{p["t2"]}" {TS}/>'
         for x in (14, 34, 54, 74, 94)]
    o.append(f'<rect x="30" y="82" width="24" height="30" fill="{p["t2"]}" {TS}/>')
    o.append(f'<rect x="66" y="54" width="24" height="58" fill="{p["acc"]}" '
             f'fill-opacity="0.80" {TS}/>')
    return "".join(o)


def t_encoding_depth(p):
    # Đường ngang trên cùng = mặt tiếp nhận. BA ô RỖNG y hệt nhau nằm ngay dưới mặt,
    # không ô nào đi sâu hơn ô nào: đọc lại ba lần vẫn là ba lần ở cùng một tầng.
    # Một khối ĐẶC duy nhất bên phải đâm xuống hết khung. Biến nhìn thấy được là SỐ
    # LẦN (3) đối lại ĐỘ SÂU (1) — đúng điều card phủ định: lặp lại không mua được
    # độ sâu.
    # Khác `flagged_transient` cùng batch (hai vật cùng cỡ, khác nhau ở dấu hiệu, không
    # có trục sâu nào) và khác `layers` (các đĩa dẹt xếp chồng, không có gì đâm xuyên).
    o = [f'<line x1="14" y1="34" x2="114" y2="34" {TNF}/>']
    o += [f'<rect x="{x}" y="34" width="16" height="16" fill="none" {TS}/>'
          for x in (16, 38, 60)]
    o.append(f'<rect x="88" y="34" width="24" height="72" fill="{p["acc"]}" '
             f'fill-opacity="0.82" {TS}/>')
    return "".join(o)


def t_age_forecast(p):
    # Ba hàng, hàng nào cũng gồm một đoạn ĐẶC (tuổi đã sống, quan sát được) nối tiếp
    # một đoạn RỖNG DÀI ĐÚNG BẰNG nó (tuổi còn lại, chưa xảy ra). Càng xuống dưới cặp
    # càng dài, nhưng tỉ lệ 1:1 giữa hai nửa không đổi — đó chính là phát biểu của
    # Lindy: kỳ vọng sống thêm tỉ lệ thuận với đã sống được bao lâu.
    # Nửa rỗng bắt buộc bằng nửa đặc; vẽ lệch tỉ lệ là nói sai định luật. Khác
    # `ratchet` (bậc thang tựa lên nhau, không có phần chưa xảy ra) và khác
    # `streak_projection` (dãy dọc trên một vạch đáy + đúng MỘT ô rỗng vượt cao).
    o = []
    for y, w in ((26, 20), (58, 34), (90, 46)):
        o.append(f'<rect x="14" y="{y}" width="{w}" height="22" fill="{p["acc"]}" '
                 f'fill-opacity="0.78" {TS}/>')
        o.append(f'<rect x="{14+w}" y="{y}" width="{w}" height="22" fill="none" {TS}/>')
    return "".join(o)


def t_steeper_below(p):
    # Một mốc tham chiếu (vạch ngang + gạch dọc ngắn tại gốc). Hai phía cách gốc ĐÚNG
    # cùng một khoảng — 48px mỗi bên, tức hai lượng bằng nhau. Nhưng vùng phía dưới
    # (mất) sâu gấp hơn hai lần vùng phía trên (được), và dốc hẳn ngay sát gốc.
    # Khoảng cách bằng nhau là điều kiện để đọc ra bất đối xứng; lệch khoảng thì hình
    # chỉ còn nói "hai thứ khác cỡ".
    # Khác `reference_kink` (endowment amber / disposition mint) vốn CỐ Ý cho hai ô
    # bằng nhau và nói về việc xử lý ngược chiều; ở đây độ lớn cảm nhận mới là nội
    # dung. Khác `two_frames` (hai khung rời, một mực nước, chỉ khác phía được tô) và
    # khác `setpoint_return` (hai gò ngược chiều CÙNG cỡ và đều quay về nền).
    return (f'<line x1="14" y1="64" x2="114" y2="64" {TNF}/>'
            f'<line x1="64" y1="52" x2="64" y2="76" {TNF}/>'
            f'<path d="M64,64 Q88,58 112,48 L112,64 Z" fill="{p["t2"]}" {TS}/>'
            f'<path d="M64,64 Q46,98 16,106 L16,64 Z" fill="{p["acc"]}" '
            f'fill-opacity="0.72" {TS}/>')


def t_holding_capacity(p):
    # Khung = số chỗ giữ được cùng lúc, và nó có kích thước CỐ ĐỊNH. Ba ô đặc nằm gọn
    # bên trong. Hai ô cùng cỡ nằm HẲN ngoài khung, vẽ rỗng: chúng vẫn tồn tại, chỉ là
    # không được giữ. Giới hạn nằm ở cái khung, không ở số lượng thứ đang chờ.
    # Các ô trong khung phải có lề với mép khung — dính mép thì hình đọc thành
    # `negative_space` (vùng phải tránh, áp sát mép). Khác `gate` (khe hẹp, có dòng
    # chảy xuyên qua: ở đó việc sàng lọc đang diễn ra, còn đây là một sức chứa tĩnh).
    o = [f'<rect x="14" y="36" width="62" height="56" fill="none" {TS}/>']
    o += [f'<rect x="{x}" y="57" width="14" height="14" fill="{p["acc"]}" '
          f'fill-opacity="0.82" {TS}/>' for x in (20, 38, 56)]
    o += [f'<rect x="88" y="{y}" width="14" height="14" fill="none" {TS}/>'
          for y in (48, 72)]
    return "".join(o)


def t_map_remainder(p):
    # Đường bao MÉO, vẽ rỗng = lãnh thổ, với đủ chỗ lồi chỗ lõm không quy về hình học
    # đơn giản nào. Bên trong là một tứ giác ĐẶC, bốn cạnh thẳng, nhỏ hơn hẳn = bản đồ.
    # Các múi rỗng giữa hai đường bao là phần thực tại bị lược đi: có mặt trong hình
    # nhưng không được tô, và không bao giờ khép lại được.
    # Bản đồ bắt buộc là đa giác CẠNH THẲNG nằm trong một bao CONG méo — cùng chất
    # liệu thì hình đọc thành `nested_scope` (các vòng đồng tâm, quan hệ bao hàm thuần
    # tuý). Khác `forced_fit` (hình bị khung CẮT phẳng — ở đó lãnh thổ bị bẻ; ở đây
    # lãnh thổ nguyên vẹn, chỉ có bản đồ là thiếu).
    return (f'<path d="M62,14 C90,12 114,34 108,58 C102,82 116,98 92,110 '
            f'C68,120 34,110 22,88 C10,66 18,32 62,14 Z" fill="none" {TS}/>'
            f'<path d="M48,40 L92,50 L84,88 L42,80 Z" fill="{p["acc"]}" '
            f'fill-opacity="0.72" {TS}/>')


def t_split_identity(p):
    # MỘT khối đặc liền mạch ở dưới = đối tượng, và nó không bị chia ở bất cứ đâu.
    # Hai ô rỗng phía trên = hai tên gọi, mỗi ô có một cuống nối xuống đúng khối đó.
    # Đường dọc giữa hai tên DỪNG LẠI trước khi tới khối: sự chia tách chỉ tồn tại ở
    # tầng tên gọi và tầng niềm tin, không tồn tại ở tầng đối tượng.
    # Đường dọc bắt buộc không chạm khối — chạm vào là hình đọc thành `latch` (bức
    # tường đặc chia hẳn hai phía) hoặc thành `fracture` (khối thật sự bị tách).
    # Khác `mirror` (cùng một sự việc soi qua hai khung quy kết, taken cả hai hue):
    # ở đó hai ảnh đều là ảnh; ở đây một bên là tên, một bên là vật.
    o = [f'<rect x="20" y="74" width="88" height="32" rx="4" fill="{p["acc"]}" '
         f'fill-opacity="0.72" {TS}/>']
    o += [f'<rect x="{x}" y="24" width="30" height="30" fill="none" {TS}/>'
          for x in (24, 74)]
    o += [f'<line x1="{x}" y1="54" x2="{x}" y2="74" {TNF}/>' for x in (39, 89)]
    o.append(f'<line x1="64" y1="20" x2="64" y2="66" {TNF}/>')
    return "".join(o)


def t_flagged_transient(p):
    # Hai vật CÙNG KÍCH THƯỚC. Vật trái nguyên vẹn và được tô đặc = thông tin được
    # mã hoá sâu. Vật phải khác đúng một điểm: một góc bị vát — dấu "tạm thời" — và vì
    # có dấu đó nên nó không nhận được một nét mực nào. Cái quyết định không phải nội
    # dung hay số lần gặp, mà là một phán định gắn ở đầu vào.
    # Dấu hiệu phải ở mức SILHOUETTE (góc vát 14px, còn ~7px ở khổ hiển thị thật) —
    # một nhãn nhỏ bên trong sẽ tàng hình ở 64px. Khác `encoding_depth` cùng batch (có
    # trục sâu và đếm số lần lặp) và khác `cue_lock` (khối nguyên + mảnh khớp nằm rời:
    # ở đó dữ liệu còn đủ, chỉ thiếu chìa; ở đây dữ liệu chưa từng được ghi).
    return (f'<rect x="22" y="44" width="40" height="40" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>'
            f'<path d="M70,44 L96,44 L110,58 L110,84 L70,84 Z" fill="none" {TS}/>')


def t_sealed_bins(p):
    # MỘT dải liền = tổng số tiền, bị chia hết bề ngang thành ba ngăn chạm nhau. Mỗi
    # ngăn một sắc độ riêng và một bề rộng riêng: tiền trong ngăn này không còn đọc
    # được là cùng loại với tiền ngăn kia, dù trên thực tế chúng thay thế nhau hoàn
    # toàn. Vách ngăn là hai nét trùng tại mép chung — đặc và không đi qua được.
    # Sắc độ cố ý KHÔNG tăng dần và bề rộng cố ý không đều: xếp tăng dần thì hình đọc
    # thành `spectrum` (một dải liên tục) chứ không thành các ngăn tách biệt. Không
    # chừa lề trong khung như `page_structure` — chia hết bề ngang mới là "toàn bộ số
    # tiền", còn lề sẽ đọc thành bố cục trang.
    # Ngăn nhạt nhất KHÔNG được nằm giữa: đặt ở giữa thì nó đọc thành khoảng trống chia
    # đôi dải, tức mất luôn nghĩa "ba ngăn". Thứ tự nhạt–đậm–vừa vừa phá được cả nhịp
    # tăng dần lẫn cái đọc-thành-khoảng-trống.
    return (f'<rect x="14" y="40" width="36" height="48" fill="{p["t1"]}" {TS}/>'
            f'<rect x="50" y="40" width="26" height="48" fill="{p["acc"]}" '
            f'fill-opacity="0.62" {TS}/>'
            f'<rect x="76" y="40" width="38" height="48" fill="{p["t3"]}" {TS}/>')


CONCEPT_OBJECTS_20260918 = dict(
    rank_reversal=t_rank_reversal, fewer_louder=t_fewer_louder,
    encoding_depth=t_encoding_depth, age_forecast=t_age_forecast,
    steeper_below=t_steeper_below, holding_capacity=t_holding_capacity,
    map_remainder=t_map_remainder, split_identity=t_split_identity,
    flagged_transient=t_flagged_transient, sealed_bins=t_sealed_bins,
)

CONCEPT_MEANING.update({
    "rank_reversal": "cùng một cặp, cỡ không đổi, nhưng bên nào được tô đặc và bên nào "
                     "ở trên thì lật ngược khi chuyển từ đánh giá riêng lẻ sang so cạnh nhau",
    "fewer_louder": "hàng sau ít phần tử hơn hàng trước nhưng phần tử cao nhất lại vượt "
                    "mọi phần tử hàng trước — vừa rụng chi tiết vừa phóng đại chi tiết",
    "encoding_depth": "ba ô rỗng nằm cùng một tầng nông đối lại một khối đặc đâm sâu — "
                      "số lần lặp lại không mua được độ sâu xử lý",
    "age_forecast": "ba cặp dài dần, cặp nào cũng gồm một nửa đặc đã sống và một nửa rỗng "
                    "dài đúng bằng nó — sống thêm tỉ lệ thuận với đã sống",
    "steeper_below": "hai phía cách mốc đúng cùng một khoảng, nhưng vùng phía mất sâu gấp "
                     "hơn hai lần vùng phía được",
    "holding_capacity": "một khung cỡ cố định giữ được ba ô, hai ô cùng cỡ nằm hẳn ngoài "
                        "khung và vẽ rỗng — vẫn tồn tại, chỉ là không được giữ",
    "map_remainder": "một đường bao méo vẽ rỗng và một đa giác cạnh thẳng đặc nằm trong nó; "
                     "các múi rỗng ở giữa là phần thực tại bản đồ lược đi",
    "split_identity": "một khối liền mạch với hai tên gọi rỗng phía trên, và đường chia giữa "
                      "hai tên dừng lại trước khi tới khối",
    "flagged_transient": "hai vật cùng cỡ, vật bị vát một góc thì không nhận nét mực nào — "
                         "một phán định ở đầu vào quyết định có được ghi hay không",
    "sealed_bins": "một dải bị chia hết bề ngang thành ba ngăn chạm nhau, mỗi ngăn một sắc "
                   "độ và một bề rộng riêng — cùng một nguồn lực bị đọc thành ba loại",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260918)


# --------------------------------------------------------------------------
# Batch 2026-09-19 — mere-exposure → naive-realism
# xlsx gán 6/10 card thành `hierarchy` và 4/10 thành `branching`; không card nào
# trong lô này là quan hệ cha–con hay rẽ nhánh, nên toàn bộ đều override.
# --------------------------------------------------------------------------


def t_familiarity_fill(p):
    # Ba phần tử Y HỆT NHAU về hình và KÍCH THƯỚC — vật không hề đổi, không có
    # thông tin nào được thêm vào. Biến duy nhất là sắc độ, tăng theo số lần gặp:
    # mức ưa thích dâng lên trong khi đối tượng đứng yên.
    # Cỡ bắt buộc không đổi. Vẽ to dần là đã nói "có thêm giá trị thật", tức phủ
    # định đúng luận điểm của card.
    # Khác `stacked_copies` (illusory-truth, amber: ba bản CHỒNG lên nhau, cùng một
    # sắc độ nhạt, chỗ giao mới đậm — nói về niềm tin sinh từ số lần gặp) vì ở đây
    # ba bản tách rời và chính từng bản đậm dần. Khác `echo` (cột thấp dần VÀ nhạt
    # dần — biên độ tắt) và khác `spectrum` (bán kính lớn dần).
    specs = ((16, 0.16), (50, 0.46), (84, 0.82))
    return "".join(f'<rect x="{x}" y="50" width="28" height="28" fill="{p["acc"]}" '
                   f'fill-opacity="{op}" {TS}/>' for x, op in specs)


def t_source_swap(p):
    # Hai nguồn khác hẳn nhau về hình: tam giác (trái) và tròn (phải), cả hai vẽ rỗng.
    # Khối nội dung phía dưới được tô ĐẶC — ký ức còn nguyên vẹn, không mất mát gì — và
    # nó đội một mái TAM GIÁC: dấu của nguồn đã sinh ra nó. Nhưng đường dẫn duy nhất lại
    # chạy sang hình TRÒN. Sai ở chỗ quy nguồn, không ở chỗ nội dung.
    # Mái phải nằm ở mức silhouette (cao 18px, còn 9px ở khổ hiển thị thật); một nhãn
    # nhỏ trong lòng khối sẽ tàng hình ở 64px.
    # Khác `cue_lock` (khuyết bán nguyệt + mảnh khớp rời: dữ liệu đủ, thiếu chìa để mở)
    # và khác `fracture` (hai nửa lệch khớp — bất nhất lộ ra ngoài): ở đây không có gì
    # lệch hay thiếu, chỉ có một mối nối chỉ nhầm địa chỉ.
    return (f'<path d="M30,18 L46,44 L14,44 Z" fill="none" {TS}/>'
            f'<circle cx="98" cy="31" r="15" fill="none" {TS}/>'
            f'<path d="M24,80 L46,62 L68,80 L68,106 L24,106 Z" fill="{p["t3"]}" {TS}/>'
            f'<line x1="68" y1="88" x2="86" y2="43" {TNF}/>')


def t_overwrite_seam(p):
    # Khối ký ức gốc có MỘT đường bao liền, không đứt ở đâu cả. Phần bên phải bên trong
    # nó đã bị thay bằng vật liệu khác (accent trong suốt) nhưng KHÔNG có nét mực nào
    # ngăn giữa hai phần — nhìn từ ngoài vẫn là một khối liền mạch, không có mối ghép
    # nào để lần ra chỗ bị viết đè. Mẩu rời phía trên cùng bề rộng, cùng chất liệu: đó
    # là thông tin đến sau, và nó vừa khít đúng phần đã chiếm chỗ.
    # Đường bao ngoài phải vẽ SAU phần tô để mép trên/dưới của vùng tô không cắt qua nét.
    # Khác `gap_fill` (mảnh vá nổi lên, lệch trục, nhìn ra được là đồ lạ) vì ở đây chỗ
    # ghép phẳng lì; khác `veil` (tấm che nằm ĐÈ lên, phần bị che vẫn còn nguyên phía
    # sau) vì ở đây phần gốc đã mất chỗ thật sự.
    return (f'<rect x="70" y="62" width="44" height="44" fill="{p["acc"]}" '
            f'fill-opacity="0.62" stroke="none"/>'
            f'<rect x="14" y="62" width="100" height="44" fill="none" {TS}/>'
            f'<rect x="70" y="16" width="44" height="28" fill="{p["acc"]}" '
            f'fill-opacity="0.62" {TS}/>')


def t_tail_advantage(p):
    # Hai hàng = hai kênh giác quan, cùng một chuỗi, cùng số phần tử, ba phần tử ĐẦU
    # giống hệt nhau ở cả hai hàng. Khác biệt dồn hết vào phần tử CUỐI: hàng trên nó
    # cao hơn và tô đặc, hàng dưới nó rỗng. Nội dung nằm ở chỗ ưu thế chỉ xuất hiện ở
    # ĐUÔI chuỗi chứ không trải đều — đúng điểm phân biệt modality effect khỏi recency
    # thông thường.
    # Ba phần tử đầu bắt buộc giống hệt nhau giữa hai hàng; cho chúng lệch nhau là đã
    # nói "kênh này nhớ tốt hơn ở mọi vị trí", tức sai luận điểm.
    o = []
    for x in (14, 40, 66):
        o.append(f'<rect x="{x}" y="26" width="20" height="20" fill="{p["t2"]}" {TS}/>')
        o.append(f'<rect x="{x}" y="76" width="20" height="20" fill="{p["t2"]}" {TS}/>')
    o.append(f'<rect x="92" y="16" width="20" height="30" fill="{p["acc"]}" '
             f'fill-opacity="0.85" {TS}/>')
    o.append(f'<rect x="92" y="76" width="20" height="20" fill="none" {TS}/>')
    return "".join(o)


def t_nominal_real(p):
    # Ba mốc thời gian. Cái VỎ rỗng cao dần = con số danh nghĩa, năm sau to hơn năm
    # trước. Cái LÕI đặc bên trong teo dần = sức mua thực. Hai chiều biến thiên ngược
    # nhau trong cùng một vật chính là toàn bộ nội dung: nhìn vỏ thì thấy đi lên.
    # Lõi phải nằm HẲN trong vỏ và cùng căn đáy với vỏ, nếu không mất quan hệ
    # "cùng một thứ, đo hai cách".
    # Khác `two_frames` (framing-effect, amber: hai khung Y HỆT nhau, cùng một mốc, chỉ
    # khác phía nào được tô) vì ở đây các khung khác chiều cao và có biến thiên theo
    # thời gian. Khác `depletion` (cột đặc thấp dần dưới một vạch mốc) vì ở đó không có
    # vỏ rỗng nào lớn lên.
    specs = ((18, 42, 24, 36), (51, 60, 57, 26), (84, 78, 90, 16))
    o = []
    for fx, fh, cx_, ch in specs:
        o.append(f'<rect x="{fx}" y="{106-fh}" width="26" height="{fh}" fill="none" {TS}/>')
        o.append(f'<rect x="{cx_}" y="{106-ch}" width="14" height="{ch}" '
                 f'fill="{p["acc"]}" fill-opacity="0.82" {TS}/>')
    return "".join(o)


def t_shielded_downside(p):
    # Hai khối RỦI RO CÙNG KÍCH THƯỚC, cùng sắc độ — cùng một lượng rủi ro được nhận.
    # Khối trái không chạm đất vì bên dưới nó có một trụ đỡ vẽ RỖNG: cơ chế bảo vệ có
    # tồn tại nhưng không hấp thụ gì cả, nó chỉ nâng bên chọn rủi ro lên khỏi hậu quả.
    # Khối phải đứng thẳng trên đường đáy — cùng một rủi ro đó, đáp xuống bên không được
    # nâng. Nội dung là chỗ tách rời giữa nơi rủi ro được CHỌN và nơi nó được GÁNH.
    # Hai khối bắt buộc cùng cỡ; vẽ khối chạm đất nhỏ hơn là đã nói "có bảo hiểm thì tổn
    # thất ít đi", tức phủ định đúng điều card khẳng định.
    # Trụ phải vẽ rỗng và phải ĐỨNG TRÊN đường đáy. Bản đầu dùng một thanh ngang mảnh
    # lơ lửng: ở 64px cả cụm đọc thành "vật đặt trên bàn", mất sạch quan hệ chống-đỡ.
    # Khác `unseen_cushion` (khối rơi + dải đệm rỗng + đường dự báo, bố cục dọc căn giữa,
    # nói về cái đệm bị BỎ QUÊN khỏi dự báo) vì ở đây ai cũng biết trụ có mặt — biết nên
    # mới dám nhận thêm rủi ro.
    return (f'<line x1="12" y1="106" x2="116" y2="106" {TNF}/>'
            f'<rect x="16" y="70" width="48" height="36" fill="none" {TS}/>'
            f'<rect x="24" y="34" width="32" height="32" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>'
            f'<rect x="76" y="74" width="32" height="32" fill="{p["acc"]}" '
            f'fill-opacity="0.82" {TS}/>')


def t_outcome_weighted(p):
    # Hàng trên: hai hành vi Y HỆT NHAU — cùng hình, cùng cỡ, cùng sắc độ. Đây là điều
    # kiện bắt buộc: chất lượng quyết định của hai bên không khác nhau chút nào.
    # Hàng dưới: hai kết quả lệch hẳn về sức nặng, do may rủi. Nét mực (mức lên án) bám
    # theo KẾT QUẢ chứ không theo hành vi — đó là toàn bộ nghịch lý.
    # Nếu vẽ hai khối trên khác nhau dù chỉ một chút thì hình mất nghĩa: người xem sẽ
    # đọc thành "quyết định tệ hơn thì hậu quả nặng hơn", đúng cái mà card bác bỏ.
    # Khác `divergence` (MỘT điểm rẽ thành nhiều nhánh) vì ở đây có hai gốc độc lập, và
    # khác `outward_credit` (bố cục dọc một cột, chấm đặc trong khối nối lên vòng rỗng).
    o = []
    for x in (20, 74):
        o.append(f'<rect x="{x}" y="18" width="34" height="28" fill="{p["t3"]}" {TS}/>')
        o.append(f'<line x1="{x+17}" y1="46" x2="{x+17}" y2="60" {TNF}/>')
    o.append(f'<circle cx="37" cy="72" r="12" fill="{p["acc"]}" fill-opacity="0.22" {TS}/>')
    o.append(f'<circle cx="91" cy="84" r="22" fill="{p["acc"]}" fill-opacity="0.85" {TS}/>')
    return "".join(o)


def t_recorded_few(p):
    # Hai DẢI cùng chiều cao và cùng cỡ ô, chỉ khác chiều dài. Dải dưới = những gì thật
    # sự xảy ra: sáu ô, chỉ hai ô đi sai được tô. Dải trên = bản ghi còn lại trong trí
    # nhớ: ngắn hơn hẳn và đậm KÍN, vì ba phần tư số lần mọi thứ suôn sẻ không để lại
    # dấu nào. Tỉ lệ đậm trong hai dải lệch nhau — đó là toàn bộ nội dung: câu ngạn ngữ
    # sống nhờ khoảng chênh đó chứ không nhờ tần suất thật.
    # Phải vẽ thành DẢI LIỀN chia ô, không phải các ô rời. Bản đầu dùng hai hàng ô tách
    # rời cạnh 16px: ở 64px chúng rụng xuống 8px và cả hình đọc thành mấy chấm vung vãi,
    # không còn tỉ lệ nào đọc được.
    # Khác `sealed_bins` (mental-accounting, amber: MỘT dải chia hết bề ngang thành ba
    # ngăn KHÁC bề rộng và ba sắc độ khác nhau) vì ở đây có hai dải, ô đều nhau tuyệt
    # đối, và biến duy nhất là chiều dài dải cùng việc ô nào được tô.
    o = []
    for x0, w, n, hits in ((14, 34, 2, (0, 1)), (14, 102, 6, (1, 4))):
        cw = w / n
        o.append(f'<rect x="{x0}" y="{32 if n == 2 else 78}" width="{w}" height="22" '
                 f'fill="none" {TS}/>')
        for i in range(n):
            if i in hits:
                o.append(f'<rect x="{x0 + i * cw:.1f}" y="{32 if n == 2 else 78}" '
                         f'width="{cw:.1f}" height="22" fill="{p["acc"]}" '
                         f'fill-opacity="0.85" {TS}/>')
            elif i:
                o.append(f'<line x1="{x0 + i * cw:.1f}" y1="{32 if n == 2 else 78}" '
                         f'x2="{x0 + i * cw:.1f}" y2="{54 if n == 2 else 100}" {TNF}/>')
    return "".join(o)


def t_opaque_other(p):
    # Hai vật CÙNG LOẠI, cùng cỡ. Vật bên trái vẽ rỗng nên nhìn thấu được vào trong, và
    # cái thấy được là một lõi nhỏ: động cơ của chính mình, đã soi và thấy vừa phải.
    # Vật bên phải bị tô kín đặc — không nhìn vào được, nên toàn bộ phần không thấy bị
    # điền bằng suy đoán. Bất đối xứng nằm ở ĐỘ TRONG SUỐT, không ở hình dạng: hai bên
    # vốn là cùng một loại vật.
    # Dùng hình TRÒN là có chủ ý — `locus_flip` (fundamental-attribution-error, mint) đã
    # chiếm thế "hai khung VUÔNG cạnh nhau, chấm trong / chấm ngoài"; đổi chất tròn↔vuông
    # để hai card không nhầm nhau ở 64px. Ở đó nội dung là VỊ TRÍ trong/ngoài của cái đẩy,
    # ở đây là việc có nhìn vào được hay không.
    return (f'<circle cx="40" cy="64" r="24" fill="none" {TS}/>'
            f'<circle cx="40" cy="64" r="9" fill="{p["acc"]}" fill-opacity="0.80" {TS}/>'
            f'<circle cx="90" cy="64" r="24" fill="{p["acc"]}" fill-opacity="0.88" {TS}/>')


def t_coincident_view(p):
    # Khối đặc = sự việc. Khung rỗng gần như TRÙNG KHÍT lên nó, chỉ lệch vài pixel = cách
    # mình nhìn, sát tới mức tự cảm thấy không có lăng kính nào ở giữa. Khung rỗng bên
    # phải cùng cỡ nhưng XOAY hẳn đi = cách người khác nhìn, lệch thấy rõ.
    # Đây là hình của NIỀM TIN chứ không phải của sự thật: card nói về việc người ta tin
    # cái mình thấy trùng với thực tại, nên vẽ đúng thế mới trung thực với luận điểm.
    # Khung "cách mình nhìn" phải ĐỒNG TÂM với khối đặc, không lệch chéo. Bản đầu cho nó
    # lệch 4px theo đường chéo: ở 64px cặp đó đọc thành một khối có đổ bóng — đúng thứ
    # phong cách này cấm — chứ không đọc thành hai vật trùng khít. Đồng tâm thì quan hệ
    # là sự KHỚP CHỒNG, không thể nhầm sang hiệu ứng.
    # Hai khung rỗng phải cùng kích thước để so sánh được: khác biệt duy nhất giữa chúng
    # là một cái trùng tâm với sự việc, một cái xoay lệch khỏi nó.
    # Góc xoay phải đủ lớn (18°) để cạnh nghiêng đọc được ở 64px; xoay nhỏ hơn sẽ bị
    # nhầm thành lỗi render. Khác `stacked_copies` (illusory-truth, amber: ba bản cùng cỡ
    # TỊNH TIẾN đều) chính nhờ phép xoay, và khác `fracture` (hai nửa đặc lệch khớp).
    return (f'<rect x="22" y="50" width="32" height="32" fill="{p["t3"]}" {TS}/>'
            f'<rect x="18" y="46" width="40" height="40" fill="none" {TS}/>'
            f'<rect x="70" y="46" width="40" height="40" fill="none" {TS} '
            f'transform="rotate(18 90 66)"/>')


CONCEPT_OBJECTS_20260919 = dict(
    familiarity_fill=t_familiarity_fill, source_swap=t_source_swap,
    overwrite_seam=t_overwrite_seam, tail_advantage=t_tail_advantage,
    nominal_real=t_nominal_real, shielded_downside=t_shielded_downside,
    outcome_weighted=t_outcome_weighted, recorded_few=t_recorded_few,
    opaque_other=t_opaque_other, coincident_view=t_coincident_view,
)

CONCEPT_MEANING.update({
    "familiarity_fill": "ba vật y hệt nhau về cỡ, chỉ sắc độ đậm dần — mức ưa thích dâng "
                        "lên trong khi đối tượng không đổi chút nào",
    "source_swap": "khối nội dung còn nguyên và đội mái tam giác của nguồn đã sinh ra nó, "
                   "nhưng đường dẫn duy nhất lại chạy sang hình tròn",
    "overwrite_seam": "một khối có đường bao liền, phần bên trong bị thay bằng vật liệu khác "
                      "mà không có nét ngăn nào — mẩu rời phía trên vừa khít chỗ đã chiếm",
    "tail_advantage": "hai hàng cùng chuỗi, ba phần tử đầu giống hệt nhau, khác biệt dồn hết "
                      "vào phần tử cuối: một bên đặc và cao hơn, một bên rỗng",
    "nominal_real": "vỏ rỗng cao dần bọc lấy lõi đặc teo dần — cùng một thứ, hai cách đo đi "
                    "ngược chiều nhau",
    "shielded_downside": "hai khối rủi ro cùng cỡ: khối đứng trên tấm chắn không chạm đáy, "
                         "khối ngoài rìa tấm chắn rơi hẳn xuống đường đáy",
    "outcome_weighted": "hai hành vi y hệt nhau ở trên, hai kết quả lệch hẳn sức nặng ở dưới "
                        "— nét mực bám theo kết quả chứ không theo hành vi",
    "recorded_few": "năm sự việc cùng cỡ ở hàng dưới chỉ hai cái đặc, và hàng trên — bản ghi "
                    "— chỉ gồm đúng hai cái đặc đó",
    "opaque_other": "hai vật cùng loại cùng cỡ: một cái rỗng nhìn thấu vào lõi nhỏ bên trong, "
                    "một cái tô kín nên phần không thấy được điền đặc bằng suy đoán",
    "coincident_view": "khung rỗng gần như trùng khít lên khối đặc, và một khung cùng cỡ xoay "
                       "hẳn đi bên cạnh",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260919)


# --------------------------------------------------------------------------
# Batch 2026-09-20 — concept object cho 10 card #141-150
# --------------------------------------------------------------------------

def t_one_sours_sum(p):
    # Hàng trên: bốn sự việc CÙNG CỠ — ba cái nhạt (tích cực/trung tính), một cái đậm
    # (tiêu cực). Tỉ lệ thật là 3:1. Thanh tổng ở dưới — ấn tượng đọng lại — lại đậm
    # KÍN như thể cả bốn đều tiêu cực. Khoảng chênh giữa tỉ lệ thật và sắc độ của thanh
    # tổng chính là trọng số dư mà card nói tới, và cũng đúng phần `strategy` bảo đi đếm
    # lại tỉ lệ thực.
    # Bốn ô phải cùng cỡ tuyệt đối: to nhỏ khác nhau thì hình đọc thành "cái tiêu cực
    # vốn lớn hơn", tức là bác bỏ chính luận điểm.
    # Khác `odd_one_out` (bizarreness-effect): ở đó chỉ có một hàng và cái khác biệt
    # đáng nhớ vì khác, không có thanh tổng nào bị nó kéo theo.
    o = []
    for i in range(4):
        paint = (f'fill="{p["acc"]}" fill-opacity="0.9"' if i == 2
                 else f'fill="{p["t2"]}"')
        o.append(f'<rect x="{16+i*26}" y="30" width="18" height="18" {paint} {TS}/>')
    o.append(f'<rect x="16" y="78" width="96" height="22" fill="{p["acc"]}" '
             f'fill-opacity="0.9" {TS}/>')
    return "".join(o)


def t_ramp_to_step(p):
    # Trái: một dốc LIÊN TỤC — xác suất thật đi từ thấp tới cao không đứt đoạn.
    # Phải: đúng dải đó sau khi qua đầu đọc của não — chỉ còn HAI mức, thấp tịt và cao
    # kịch, không có nấc trung gian nào. Cùng đứng trên một đường đáy để so được.
    # Phần giữa của dốc (vùng não bỏ qua) chính là chỗ bị nuốt mất khi sang bên phải.
    # Khác `spectrum` (dãy tròn to dần, không có bản đối chiếu) và khác `steep_then_flat`
    # (một đường cong duy nhất, nói về thời gian chứ không phải độ phân giải).
    return (f'<path d="M18,96 L58,96 L58,36 Z" fill="{p["t2"]}" {TS}/>'
            f'<rect x="70" y="82" width="20" height="14" fill="{p["t3"]}" {TS}/>'
            f'<rect x="92" y="42" width="20" height="54" fill="{p["t3"]}" {TS}/>'
            f'<line x1="14" y1="100" x2="116" y2="100" {TNF}/>')


def t_gap_before_self(p):
    # Một hàng lượt: ba lượt đầu được ghi lại (đặc), lượt NGAY TRƯỚC mình rỗng hoàn
    # toàn, và lượt của mình vống hẳn lên vì toàn bộ chú ý đã dồn vào đó.
    # Vị trí của ô rỗng là điều kiện bắt buộc: nó phải kề sát ô vống. Đặt ô rỗng ở giữa
    # hàng thì hình đọc thành "quên ngẫu nhiên một chỗ", mất hẳn quan hệ nhân quả giữa
    # sự chuẩn bị cho lượt mình và lỗ hổng ngay trước đó.
    # Khác `gap_fill` (confabulation): ở đó lỗ hổng được ĐIỀN bằng vật liệu khác; ở đây
    # nó để trống, và nguyên nhân nằm ở ô bên cạnh chứ không ở bản thân lỗ hổng.
    o = [f'<rect x="{12+i*22}" y="68" width="16" height="22" fill="{p["t3"]}" {TS}/>'
         for i in range(3)]
    o.append(f'<rect x="78" y="68" width="16" height="22" fill="none" {TS}/>')
    o.append(f'<rect x="100" y="44" width="16" height="46" fill="{p["acc"]}" '
             f'fill-opacity="0.9" {TS}/>')
    return "".join(o)


def t_expected_flat(p):
    # Thanh ngang chạy suốt khung, cao độ không đổi từ đầu tới cuối = giả định "mọi thứ
    # vẫn bình thường". Khối dựng đứng cắt ngang qua nó = biến cố hiếm, thật, đang xảy
    # ra. Thanh KHÔNG hề chệch hướng ở chỗ giao — nó đi thẳng qua như không có gì.
    # Chỗ giao tự đậm lên nhờ fill-opacity: đó là vùng duy nhất trong hình nơi hai sự
    # thật cùng tồn tại, và cũng là vùng người ta không nhìn.
    # Thanh phải chạy HẾT chiều rộng, không dừng trước khối: dừng lại là đã thừa nhận
    # biến cố, tức mất nghĩa. Khác `tail_event` (black-swan) vốn là một phân bố có đuôi,
    # ở đó biến cố nằm ngoài rìa; ở đây nó nằm ngay giữa mà vẫn không được tính vào.
    return (f'<rect x="60" y="26" width="34" height="72" fill="{p["acc"]}" '
            f'fill-opacity="0.32" {TS}/>'
            f'<rect x="14" y="72" width="100" height="14" fill="{p["acc"]}" '
            f'fill-opacity="0.32" {TS}/>'
            f'<line x1="14" y1="102" x2="114" y2="102" {TNF}/>')


def t_own_side_premium(p):
    # Một bức tường đặc chia khung làm hai. Cùng MỘT loại vật thể (hình vuông) nằm hai
    # bên: bên ngoài vẽ rỗng và nhỏ, bên trong vẽ đặc và to. Không có khác biệt nào
    # khác giữa chúng ngoài việc đứng ở phía nào của tường — toàn bộ chênh lệch giá trị
    # sinh ra từ đường ranh giới, đúng câu hỏi trong `strategy`.
    # Phải dùng cùng một primitive cho cả hai. Đổi hình (vuông vs tròn) là rơi sang
    # `contrast` và mất nghĩa: khi đó hai thứ khác nhau thật, không còn nghịch lý.
    # Khác `in_out_ring` (in-group-bias): ở đó ranh giới là vòng kín và nội dung hai bên
    # là các cá thể rời; ở đây ranh giới là tường thẳng và vật thể là một, chỉ đổi cỡ.
    return (f'<rect x="22" y="50" width="30" height="30" fill="none" {TS}/>'
            f'<rect x="61" y="20" width="7" height="88" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="74" y="44" width="40" height="40" fill="{p["t3"]}" {TS}/>')


def t_tilted_floor(p):
    # Ba cửa Y HỆT NHAU, cả ba đều MỞ — không cửa nào bị bịt, đó là điều kiện sống còn
    # của nudge (không cấm đoán). Cái thay đổi là mặt sàn: nó nghiêng, nên khối tự lăn
    # về phía một cửa. Kiến trúc lựa chọn nằm ở độ nghiêng, không nằm ở số cửa.
    # Ba cửa phải cùng bề rộng và cùng chiều cao: làm cửa "tốt" to hơn là đã can thiệp
    # vào lợi ích của lựa chọn, tức không còn là nudge mà là ưu đãi.
    # Khác `unused_exit` (learned-helplessness): ở đó có đúng một lối ra và khối đứng
    # yên xa nó; ở đây có ba lối và khối đang ở phía thấp nhất do trọng lực bố cục.
    # Sàn vẽ thành BẬC THANG chứ không phải dốc nghiêng: bản dốc đầu tiên khiến ba cửa
    # (vốn là rect thẳng đứng) chỉ chạm sàn ở một điểm, hai góc đáy hở ra 3-4px và ở
    # 64px cả ba đọc thành mấy ô vuông trôi lơ lửng cạnh một gạch chéo. Bậc thang cho
    # mỗi cửa một mặt phẳng nằm ngang để đứng, mọi cạnh trùng trục nên nét sắc ở khổ nhỏ,
    # mà chiều đi xuống — tức phía ít lực cản — vẫn đọc nguyên.
    o = [f'<polyline points="16,70 44,70 44,82 72,82 72,94 114,94" fill="none" {TS}/>']
    for x, y in ((20, 70), (48, 82), (83, 94)):
        o.append(f'<rect x="{x}" y="{y-24}" width="20" height="24" fill="none" {TS}/>')
    o.append(f'<circle cx="93" cy="85" r="8" fill="{p["acc"]}" fill-opacity="0.9" {TS}/>')
    return "".join(o)


def t_prior_passthrough(p):
    # Một hình dạng đặc trưng đi VÀO bộ máy đo ở đầu này, và đúng hình dạng đó — cùng
    # cỡ, cùng hướng, cùng sắc độ — đi RA ở đầu kia. Bộ máy vẽ rỗng và trung tính, vì
    # nó trông như một quy trình khách quan; cái đã quyết định kết quả là thứ được đưa
    # vào, không phải thứ nó làm.
    # Hai tam giác bắt buộc phải khớp nhau tuyệt đối. Vẽ cái ra hơi khác cái vào là
    # thành "quy trình có tác động chút ít" — mất hẳn ý rò rỉ kỳ vọng.
    # Khác `forced_fit` (law-of-the-instrument): ở đó công cụ ÉP vật liệu vào khuôn của
    # nó; ở đây công cụ không làm gì cả, kỳ vọng chỉ đơn giản đi xuyên qua.
    return (f'<polygon points="18,38 40,38 29,18" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="38" y="50" width="52" height="30" fill="none" {TS}/>'
            f'<line x1="31" y1="40" x2="44" y2="50" {TNF}/>'
            f'<line x1="86" y1="80" x2="97" y2="90" {TNF}/>'
            f'<polygon points="88,112 110,112 99,92" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>')


def t_fewer_supports(p):
    # Hai cột cùng đội MỘT tấm nóc y hệt nhau — cùng một hiện tượng được giải thích.
    # Khác biệt duy nhất nằm ở số khối kê bên dưới: một bên cần một khối, bên kia cần
    # bốn. Cả hai đều đứng được; hình không nói bên nào ĐÚNG, chỉ nói bên nào phải giả
    # định nhiều hơn — đúng phạm vi của Occam (ưu tiên xem xét trước, không phải chân lý).
    # Tấm nóc hai bên bắt buộc cùng cỡ. Nóc khác cỡ thì thành "giải thích nhiều hơn",
    # mà tiền đề của dao cạo là hai giả thuyết giải thích được như nhau.
    # Khác `stacked_copies` (illusory-truth): ở đó các bản sao cùng cỡ tịnh tiến đều và
    # không có gì đội lên; ở đây chồng khối là phần MÓNG, và điểm so sánh là chiều cao
    # chồng giữa hai bên. Khác `parsimony` (hanlons-razor) vốn là hình một-lối-đơn-giản
    # cạnh một lối vòng vèo.
    # Hai cột phải TÁCH hẳn nhau và tấm nóc phải NHÔ RA khỏi chồng móng. Bản đầu để hai
    # cột cách nhau 4px và nóc bằng đúng bề rộng móng: ở 64px khe 2px biến mất, hai cột
    # dính thành một khối bậc thang duy nhất và hình mất sạch nghĩa so sánh. Khe 14px
    # cộng phần nhô 6px mỗi bên cho mỗi cột một hình bóng riêng đọc được ở khổ thật.
    o = [f'<rect x="12" y="20" width="44" height="12" fill="{p["t3"]}" {TS}/>',
         f'<rect x="70" y="20" width="44" height="12" fill="{p["t3"]}" {TS}/>',
         f'<rect x="18" y="38" width="32" height="14" fill="{p["t2"]}" {TS}/>']
    o += [f'<rect x="76" y="{38+i*18}" width="32" height="14" fill="{p["t2"]}" {TS}/>'
          for i in range(4)]
    return "".join(o)


def t_visible_hand(p):
    # Hai tổn hại Y HỆT NHAU ở hàng dưới — cùng cỡ, cùng sắc độ. Hàng trên là hai tác
    # nhân cũng cùng cỡ. Khác biệt duy nhất: bên trái có một nét nối tác nhân với hậu
    # quả và tác nhân đó được tô đặc (bị quy trách nhiệm); bên phải không có nét nối
    # nào và tác nhân để rỗng. Không-hành-động không để lại đường dẫn nào để lần theo,
    # nên nó thoát khỏi phán xét dù hậu quả bằng nhau.
    # Hai khối dưới phải bằng nhau tuyệt đối — đó là tiền đề. Vẽ lệch cỡ là biến hình
    # thành "hành động gây hại nhiều hơn", tức bác bỏ card.
    # Khác `outcome_weighted` (moral-luck): ở đó hành vi giống nhau và KẾT QUẢ lệch;
    # ở đây kết quả giống nhau và sự QUY KẾT lệch — bố cục đảo ngược đúng trục.
    return (f'<rect x="22" y="80" width="30" height="30" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="76" y="80" width="30" height="30" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<circle cx="37" cy="32" r="14" fill="{p["acc"]}" fill-opacity="0.9" {TS}/>'
            f'<circle cx="91" cy="32" r="14" fill="none" {TS}/>'
            f'<line x1="37" y1="46" x2="37" y2="80" {TNF}/>')


def t_forgone_stack(p):
    # Hai cột đứng trên cùng một đường đáy. Phần đặc của hai cột BẰNG NHAU — đó là số
    # tiền/công sức thực sự bỏ ra, thứ duy nhất người ta thường đem ra so. Cột phải đội
    # thêm một khối RỖNG cùng cỡ: phương án tốt nhất đã bị từ bỏ. Nó rỗng vì không ai
    # xuất hoá đơn cho nó, nhưng nó chiếm đúng chỗ trong chi phí thật.
    # Khối rỗng phải dính liền mép trên của khối đặc, không tách rời: tách ra thì nó
    # đọc thành một vật khác đặt gần đó, chứ không phải phần cộng thêm của cùng một chi phí.
    # Khác `nominal_real` (money-illusion): ở đó vỏ rỗng BỌC lấy lõi và hai thứ đi
    # ngược chiều nhau; ở đây hai khối xếp chồng, cùng chiều, và phần rỗng là phần bị bỏ sót.
    return (f'<rect x="24" y="68" width="32" height="36" fill="{p["t3"]}" {TS}/>'
            f'<rect x="72" y="68" width="32" height="36" fill="{p["t3"]}" {TS}/>'
            f'<rect x="72" y="30" width="32" height="38" fill="none" {TS}/>'
            f'<line x1="16" y1="108" x2="112" y2="108" {TNF}/>')


CONCEPT_OBJECTS_20260920 = dict(
    one_sours_sum=t_one_sours_sum, ramp_to_step=t_ramp_to_step,
    gap_before_self=t_gap_before_self, expected_flat=t_expected_flat,
    own_side_premium=t_own_side_premium, tilted_floor=t_tilted_floor,
    prior_passthrough=t_prior_passthrough, fewer_supports=t_fewer_supports,
    visible_hand=t_visible_hand, forgone_stack=t_forgone_stack,
)

CONCEPT_MEANING.update({
    "one_sours_sum": "bốn ô cùng cỡ chỉ một ô đậm, nhưng thanh tổng bên dưới đậm kín như "
                     "thể cả bốn đều vậy",
    "ramp_to_step": "một dốc liên tục cạnh chính nó sau khi bị đọc lại thành đúng hai mức, "
                    "mất sạch nấc giữa",
    "gap_before_self": "hàng lượt có ba ô đặc, một ô rỗng, và ô kề ngay sau đó vống cao hẳn "
                       "— chỗ chú ý đã dồn vào",
    "expected_flat": "thanh ngang chạy suốt ở một cao độ không đổi, xuyên qua khối biến cố "
                     "dựng đứng mà không chệch chút nào",
    "own_side_premium": "cùng một hình vuông ở hai bên bức tường: bên ngoài nhỏ và rỗng, "
                        "bên trong to và đặc",
    "tilted_floor": "ba cửa y hệt nhau đều đang mở, mặt sàn nghiêng, khối nằm ở cửa thấp nhất",
    "prior_passthrough": "một tam giác đi vào bộ máy rỗng ở đầu này và đúng tam giác đó đi ra "
                         "ở đầu kia",
    "fewer_supports": "hai tấm nóc cùng cỡ, một bên kê một khối, bên kia kê bốn khối chồng lên",
    "visible_hand": "hai tổn hại bằng nhau, chỉ bên có nét nối lên tác nhân mới có tác nhân "
                    "được tô đặc",
    "forgone_stack": "hai cột đặc bằng nhau, cột phải đội thêm một khối rỗng cùng cỡ dính liền "
                     "mép trên",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260920)


def thumb(name, hue="mint"):
    """SVG 128x128, nền paper (trắng), tint ladder theo hue của card."""
    p = _pal(hue, paper_bg=True)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" '
            'width="128" height="128">'
            f'<rect width="128" height="128" fill="#FFFFFF"/>'
            f'{THUMB_REGISTRY[name](p)}</svg>')


# --------------------------------------------------------------------------
# Batch 2026-09-24 — optimism-bias → part-list-cueing-effect
# --------------------------------------------------------------------------

def t_self_exempt(p):
    # Một đường mức rủi ro KHÁCH QUAN chạy ngang suốt khung, đi qua cả hai cột. Cột
    # "người khác" dựng đúng tới đường đó. Cột "mình" thấp hẳn, và khoảng hở phía trên
    # nó để rỗng — rủi ro không biến mất, chỉ là phần tự-ước-lượng không chạm tới.
    # Đường mức bắt buộc phải là MỘT nét liền chạy qua cả hai cột. Vẽ hai đường mức
    # riêng cho mỗi cột là thành "hai mức rủi ro khác nhau", tức bác bỏ card: tiền đề
    # của optimism bias là mức rủi ro khách quan NHƯ NHAU.
    # Khác `all_above_median` (illusory-superiority): ở đó mọi phần tử đều vượt đường
    # trung vị và nửa dưới bỏ trống — một phân bố bất khả. Ở đây chỉ có đúng một phần
    # tử tụt xuống, và nó tụt vì nó là phần tử "mình".
    # Khác `overclaim` (dunning-kruger): overclaim là phạm vi tự nhận LỚN hơn phần
    # thực; ở đây đại lượng tự nhận NHỎ hơn mức thực, ngược chiều.
    return (f'<line x1="14" y1="34" x2="114" y2="34" {TNF}/>'
            f'<rect x="76" y="34" width="32" height="72" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="22" y="78" width="32" height="28" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<line x1="14" y1="106" x2="114" y2="106" {TNF}/>')


def t_averted_gaze(p):
    # Khối thông tin bên phải vẽ ĐẶC và không bị gì che: nó hiện diện đầy đủ, nhìn là
    # thấy. Cái nón nhìn bên trái mở về phía ngược lại, trùm lên một vùng rỗng không có
    # gì. Cái thiếu là hành vi nhìn, không phải khả năng nhìn.
    # Khối thông tin tuyệt đối không được phủ hatch, mờ hay viền đứt. Chỉ cần một lớp
    # che là hình rơi ngay về `veil` (thông tin bị che khuất) — đúng cái mà ostrich
    # effect KHÔNG phải: ở đây không ai giấu gì cả.
    # Khác `veil` (curse-of-knowledge, chestertons-fence): ở đó rào cản nằm giữa người
    # xem và vật; ở đây không có rào cản nào, chỉ có hướng nhìn quay đi.
    # Nón nhìn vẽ bằng hai tia tách rộng (42° mở) chứ không phải một mũi tên: mũi tên
    # ở 64px đọc thành "dòng chảy", còn hai tia mở từ một đỉnh giữ được nghĩa "trường
    # nhìn" và thấy rõ là trong đó rỗng.
    return (f'<rect x="76" y="42" width="36" height="44" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<circle cx="62" cy="64" r="9" fill="none" {TS}/>'
            f'<line x1="54" y1="60" x2="16" y2="34" {TNF}/>'
            f'<line x1="54" y1="68" x2="16" y2="94" {TNF}/>')


def t_near_side_detail(p):
    # Một đường ranh giới nhóm chạy dọc giữa khung. Phía gần (nhóm mình): ba phần tử
    # RIÊNG BIỆT, khác cỡ khác dạng, mỗi cái một đường bao. Phía xa (nhóm ngoài): đúng
    # một khối liền, không có nét chia nào bên trong. Cùng một vùng diện tích, chỉ khác
    # ở chỗ bên nào được phân giải thành cá thể.
    # Khối bên phải bắt buộc KHÔNG có nét chia trong. Thêm vào một nét là thành "nhóm
    # ngoài có 2-3 loại", mất hẳn nghĩa đồng nhất hoá.
    # Đường ranh giới là biến nhân quả, phải vẽ rõ và chạy hết chiều cao: bỏ nó đi thì
    # hình chỉ còn là `granularity` chung chung (cross-race-effect, denomination-effect),
    # vốn nói về độ phân giải mà không nói vì sao — ở đây lý do là bạn đứng bên nào.
    o = [f'<line x1="64" y1="14" x2="64" y2="114" {TNF}/>',
         f'<circle cx="30" cy="32" r="11" fill="none" {TS}/>',
         f'<rect x="16" y="54" width="30" height="16" fill="none" {TS}/>',
         f'<circle cx="34" cy="92" r="14" fill="none" {TS}/>',
         f'<rect x="76" y="32" width="36" height="64" fill="{p["t3"]}" {TS}/>']
    return "".join(o)


def t_ex_post_grade(p):
    # Hàng trên là hai quyết định với RUỘT Y HỆT NHAU — cùng số chứng cứ, cùng vị trí,
    # cùng sắc độ. Đó là tiền đề: tại thời điểm ra quyết định, hai bên có chung một cơ
    # sở. Hàng dưới là hai kết cục, một đặc một rỗng. Sắc độ của khung quyết định phía
    # trên sao chép đúng sắc độ của kết cục phía dưới nó, dù ruột hai bên không khác gì.
    # Hai chấm chứng cứ trong hai khung phải đặt cùng toạ độ tương đối. Lệch đi một
    # chấm là hình tự trả lời "quyết định trái tốt hơn thật", tức không còn là bias.
    # Khác `outcome_weighted` (moral-luck): ở đó hàng trên là HÀNH VI và cái lệch là
    # sức nặng đạo đức. Ở đây hàng trên là quyết định có chứng cứ NHÌN THẤY ĐƯỢC bên
    # trong, và cái bị sao chép là nhãn chấm điểm — trục của outcome bias là thông tin
    # sẵn có lúc quyết, nên nó phải hiện ra trong hình.
    o = [f'<rect x="14" y="16" width="44" height="36" fill="{p["t3"]}" {TS}/>',
         f'<rect x="70" y="16" width="44" height="36" fill="none" {TS}/>']
    for bx in (14, 70):
        o.append(f'<circle cx="{bx+14}" cy="34" r="5" fill="{p["acc"]}" '
                 f'fill-opacity="0.9" {TS}/>')
        o.append(f'<circle cx="{bx+30}" cy="34" r="5" fill="{p["acc"]}" '
                 f'fill-opacity="0.9" {TS}/>')
    o += [f'<line x1="36" y1="52" x2="36" y2="80" {TNF}/>',
          f'<line x1="92" y1="52" x2="92" y2="80" {TNF}/>',
          f'<rect x="22" y="80" width="28" height="28" fill="{p["t3"]}" {TS}/>',
          f'<rect x="78" y="80" width="28" height="28" fill="none" {TS}/>']
    return "".join(o)


def t_narrow_interval(p):
    # Dải rộng vẽ rỗng là độ bất định THẬT. Thanh đặc ngắn nằm gọn bên trong là khoảng
    # tin cậy tự nhận. Chấm đặc là giá trị thật — nó rơi RA NGOÀI thanh tự nhận nhưng
    # vẫn nằm trong dải thật. Sai không nằm ở chỗ đoán trượt, mà ở bề rộng của khoảng.
    # Chấm bắt buộc nằm ngoài thanh đặc và trong dải rỗng. Kéo nó vào trong thanh là
    # hình thành "đoán đúng", ra ngoài cả dải là thành "mô hình sai" — cả hai đều không
    # phải overconfidence.
    # Khác `overclaim` (dunning-kruger, false-consensus): ở đó phạm vi tự nhận LỚN hơn
    # phần thực. Ở đây ngược hẳn chiều — phạm vi tự nhận HẸP hơn dải thực, và chính độ
    # hẹp đó sinh ra lỗi.
    # Dải thật vẽ bằng TRỤC có hai nút chặn hai đầu chứ không phải một khung chữ nhật:
    # bản đầu dùng rect nên thanh đặc bên trong đọc thành "một vật nằm trong hộp", mất
    # nghĩa khoảng-trên-thang-đo. Có trục thì cả thanh tự nhận lẫn chấm giá trị thật
    # cùng nằm trên một đường, và chuyện chấm rơi ngoài thanh mới đọc ra được.
    return (f'<line x1="16" y1="64" x2="112" y2="64" {TNF}/>'
            f'<line x1="16" y1="46" x2="16" y2="82" {TNF}/>'
            f'<line x1="112" y1="46" x2="112" y2="82" {TNF}/>'
            f'<rect x="34" y="52" width="34" height="24" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<circle cx="94" cy="64" r="7" fill="{p["acc"]}" fill-opacity="0.9" {TS}/>')


def t_crowd_out(p):
    # Trên: một khung, bên trong đúng một lõi ĐẶC lớn — động lực vốn có. Dưới: cùng
    # khung đó, một khối thưởng RỖNG được cắm vào từ bên ngoài, và lõi đặc teo lại nhỏ
    # hơn hẳn phần được thêm. Tổng phần đặc sau khi thêm thưởng THẤP hơn trước khi thêm.
    # Lõi dưới bắt buộc phải nhỏ hơn lõi trên nhiều hơn là bề rộng khối thưởng. Vẽ lõi
    # giữ nguyên cỡ là thành "thưởng cộng thêm vào", đúng trực giác thông thường mà
    # card này bác bỏ.
    # Khối thưởng để RỖNG có chủ đích: nó chiếm chỗ trong khung nhưng không phải là
    # động lực — nó là cái giá phải trả, không phải cái được thêm.
    # Khác `locus_flip` (fundamental-attribution-error, extrinsic-incentive-error): ở
    # đó nguồn thúc đẩy chỉ ĐỔI CHỖ trong/ngoài mà tổng không đổi. Ở đây tổng giảm —
    # đó chính là chữ "over" trong overjustification.
    return (f'<rect x="18" y="14" width="92" height="36" fill="none" {TS}/>'
            f'<rect x="24" y="20" width="64" height="24" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="18" y="74" width="92" height="36" fill="none" {TS}/>'
            f'<rect x="24" y="80" width="24" height="24" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="56" y="80" width="30" height="24" fill="none" {TS}/>'
            f'<line x1="118" y1="92" x2="84" y2="92" {TNF}/>')


def t_figure_in_noise(p):
    # Một vệt chấm rải ngẫu nhiên, mọi chấm cùng cỡ và đều RỖNG — dữ liệu không có cấu
    # trúc. Ba chấm được tô đặc và nối thành một hình khép kín quen thuộc. Nét nối là
    # thứ người xem thêm vào; trong đám chấm không có gì tương ứng với nó.
    # Các chấm nền phải đặt LỆCH NHAU, không theo lưới. Xếp thành hàng đều là hình tự
    # sinh ra cấu trúc thật, và pareidolia mất nghĩa: cái sai phải nằm ở người nhìn.
    # Ba chấm được chọn cũng không được nằm ở vị trí đặc biệt nào so với phần còn lại.
    # Khác `network` (apophenia): ở đó các liên kết là một mạng thật đang tồn tại. Ở
    # đây chỉ có đúng một hình đóng, và nó phủ lên ba chấm không khác gì các chấm khác.
    # Khác `unlinked_control` (illusion-of-control): ở đó nét nối hụt qua một khoảng
    # trống; ở đây nét nối liền mạch — ảo giác là hình, không phải quan hệ nhân quả.
    noise = [(22, 30), (96, 22), (18, 78), (108, 62), (74, 108), (40, 66), (104, 100)]
    o = [f'<circle cx="{x}" cy="{y}" r="5" fill="none" {TS}/>' for x, y in noise]
    tri = [(44, 42), (88, 50), (62, 88)]
    o.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in tri) +
             f'" fill="none" {TS}/>')
    o += [f'<circle cx="{x}" cy="{y}" r="5" fill="{p["acc"]}" fill-opacity="0.9" {TS}/>'
          for x, y in tri]
    return "".join(o)


def t_vital_few(p):
    # Hai dải CÙNG BỀ RỘNG, cùng gốc trái. Dải trên là nguyên nhân: phần đặc chỉ chiếm
    # một mẩu đầu. Dải dưới là kết quả: phần đặc chiếm gần hết. Hai phần đặc cùng bắt
    # đầu từ mép trái nên đọc được ngay là mẩu nhỏ phía trên ứng với khối lớn phía dưới.
    # Hai dải bắt buộc bằng nhau tuyệt đối về bề rộng — đó là "100%" ở cả hai vế. Vẽ
    # lệch bề rộng là mất trục so sánh và hình thành hai đại lượng rời nhau.
    # Không vẽ nét nối giữa hai phần đặc: căn lề trái đã đủ, thêm nét nối ở 64px thành
    # một vệt đen chen giữa hai dải và làm nhoè cả hai.
    # Khác `proportion` (affective-forecasting, base-rate-fallacy) vốn là một hình duy
    # nhất chia phần: ở đây phải có HAI dải thì mới nói được quan hệ bắt chéo ít→nhiều.
    return (f'<rect x="14" y="32" width="100" height="26" fill="none" {TS}/>'
            f'<rect x="14" y="32" width="20" height="26" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="14" y="74" width="100" height="26" fill="none" {TS}/>'
            f'<rect x="14" y="74" width="80" height="26" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>')


def t_fill_to_frame(p):
    # Hai khung rộng hẹp khác hẳn nhau. Trong mỗi khung, khối việc giãn ra CHẠM cả hai
    # mép. Nhưng cái lõi đặc bên trong — phần việc thật sự phải làm — thì hai bên bằng
    # nhau chằn chặn. Bề rộng khối việc do khung quyết định, không do lõi.
    # Hai lõi bắt buộc cùng cỡ và cùng khoảng cách tới mép trái khung. Cho lõi dưới to
    # hơn là thành "việc nhiều hơn nên lâu hơn" — đúng cái cách đọc mà Parkinson's law
    # bác bỏ.
    # Khối việc phải chạm sát mép trong của khung ở CẢ HAI phía. Chừa lại khe là hình
    # thành "việc chưa lấp đầy", mất chữ "luôn giãn nở".
    # Khác `coverage_sphere` (affect-heuristic): ở đó một thứ phủ lên toàn bộ phần còn
    # lại. Ở đây có hai khung đối chiếu, và ý nghĩa nằm ở chỗ khối giãn KHÁC NHAU trong
    # khi lõi thì không.
    return (f'<rect x="12" y="24" width="48" height="36" fill="none" {TS}/>'
            f'<rect x="16" y="28" width="40" height="28" fill="{p["t3"]}" {TS}/>'
            f'<rect x="22" y="34" width="18" height="16" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>'
            f'<rect x="12" y="74" width="104" height="36" fill="none" {TS}/>'
            f'<rect x="16" y="78" width="96" height="28" fill="{p["t3"]}" {TS}/>'
            f'<rect x="22" y="84" width="18" height="16" fill="{p["acc"]}" '
            f'fill-opacity="0.9" {TS}/>')


def t_cue_crowds_out(p):
    # Hàng trên là đối chứng: năm ô nhớ được, cao bằng nhau, đều rỗng — không ai gợi ý
    # gì cả. Hàng dưới là khi ĐƯỢC gợi ý: hai ô đầu được cho sẵn nên tô đặc và cao
    # nguyên; ba ô còn lại tụt hẳn xuống so với chính chúng ở hàng trên. Đường mức đứt
    # nối từ đỉnh ô được gợi ý chạy sang cho thấy chúng đáng lẽ cao tới đâu.
    # Ba ô sau bắt buộc phải THẤP HƠN hàng đối chứng, không phải biến mất. Xoá hẳn là
    # thành "quên sạch"; part-list cueing chỉ nói nhớ TỆ HƠN, và phần hụt phải nhìn thấy.
    # Hàng trên bắt buộc giữ nguyên năm ô đều nhau — bỏ nó đi thì không còn gì để nói
    # ba ô kia "thấp hơn" so với cái gì.
    # Khác `cue_lock` (cue-dependent-forgetting): ở đó nội dung còn nguyên nhưng THIẾU
    # mảnh khớp để mở. Ở đây mảnh khớp đã được ĐƯA cho, và chính nó làm hụt phần còn
    # lại — nguyên nhân đảo ngược.
    o = [f'<rect x="{14+i*20}" y="20" width="16" height="26" fill="none" {TS}/>'
         for i in range(5)]
    o += [f'<rect x="14" y="80" width="16" height="26" fill="{p["acc"]}" '
          f'fill-opacity="0.9" {TS}/>',
          f'<rect x="34" y="80" width="16" height="26" fill="{p["acc"]}" '
          f'fill-opacity="0.9" {TS}/>']
    o += [f'<rect x="{54+i*20}" y="94" width="16" height="12" fill="none" {TS}/>'
          for i in range(3)]
    o.append(f'<line x1="54" y1="80" x2="110" y2="80" fill="none" stroke="{INK}" '
             f'stroke-width="{SW_THUMB}" stroke-dasharray="3 4" stroke-linecap="round"/>')
    return "".join(o)


CONCEPT_OBJECTS_20260924 = dict(
    self_exempt=t_self_exempt, averted_gaze=t_averted_gaze,
    near_side_detail=t_near_side_detail, ex_post_grade=t_ex_post_grade,
    narrow_interval=t_narrow_interval, crowd_out=t_crowd_out,
    figure_in_noise=t_figure_in_noise, vital_few=t_vital_few,
    fill_to_frame=t_fill_to_frame, cue_crowds_out=t_cue_crowds_out,
)

CONCEPT_MEANING.update({
    "self_exempt": "một đường mức chạy qua cả hai cột, cột 'người khác' chạm tới còn cột "
                   "'mình' thấp hẳn và khoảng hở phía trên để rỗng",
    "averted_gaze": "khối thông tin vẽ đặc và không bị che, nón nhìn mở về phía ngược lại "
                    "trùm lên vùng rỗng",
    "near_side_detail": "một đường ranh giới: phía gần là bốn phần tử riêng biệt khác cỡ, "
                        "phía xa là một khối liền không có nét chia nào",
    "ex_post_grade": "hai khung quyết định ruột y hệt nhau, sắc độ mỗi khung sao chép đúng "
                     "sắc độ của kết cục nằm dưới nó",
    "narrow_interval": "một dải rỗng rộng, một thanh đặc hẹp nằm trong, và điểm giá trị thật "
                       "rơi ra ngoài thanh nhưng vẫn trong dải",
    "crowd_out": "cùng một khung: lõi đặc lớn khi đứng một mình, lõi teo hẳn khi có thêm một "
                 "khối rỗng cắm vào từ ngoài",
    "figure_in_noise": "chấm rải lệch nhau đều rỗng, ba chấm được tô đặc và nối thành một "
                       "hình khép kín",
    "vital_few": "hai dải cùng bề rộng cùng gốc trái: mẩu đặc nhỏ ở dải trên nằm đúng trên "
                 "khối đặc lớn ở dải dưới",
    "fill_to_frame": "hai khung rộng hẹp khác nhau, khối việc chạm hai mép trong cả hai, "
                     "nhưng lõi đặc bên trong bằng nhau",
    "cue_crowds_out": "hàng đối chứng năm ô đều nhau; hàng có gợi ý thì hai ô đầu đặc cao "
                      "nguyên còn ba ô sau tụt hẳn dưới đường mức đứt",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260924)


# --------------------------------------------------------------------------
# Batch 2026-09-29 — peak-end-rule → prejudice (card #161-170).
# xlsx gán 5 hierarchy + 4 branching + 1 contrast cho batch này, tức 9/10 card sẽ
# nhận đúng 2 hình. Không card nào là "một điểm rẽ nhiều nhánh" hay "quan hệ cha-con".
# Sau khi chẩn đoán lại theo `back`, cả 10 quan hệ cần vẽ (chỉ giữ đỉnh và điểm kết ·
# xác suất cảm thấy đặt lệch trên thang · thăng tới bậc không còn vừa · hai kênh mã hoá
# đối một · nguyên nhân rỗng vẫn sinh phản hồi thật · dữ liệu cùng lớp có sẵn mà không
# nhìn · lớp ngoài đồng nhất che lớp trong đồng nhất · mức yêu thích quyết định hành vi
# nào được đọc to · tin tưởng nhích lên qua mốc trả tiền mà chứng cứ không đổi · một dải
# cảm xúc đắp ngang lên các cá thể vốn khác nhau) đều không có trong 122 hình sẵn có, và
# các hình gần nghĩa nhất (fewer_louder, narrow_interval, ratchet, encoding_depth,
# inert_input, over_scaled_forecast, opaque_other, locus_flip, ex_post_grade,
# group_tint_applied) đều đã bị chiếm ở hue cần dùng hoặc sai trục nội dung.
# --------------------------------------------------------------------------


def t_peak_end_kept(p):
    # Sáu thanh trên MỘT đường nền = sáu khoảnh khắc của cùng một trải nghiệm, cao thấp
    # khác nhau. Chỉ hai thanh được tô đặc: thanh CAO NHẤT và thanh CUỐI CÙNG. Bốn thanh
    # còn lại để rỗng — chúng đã xảy ra thật, chỉ là không còn trong bản ghi.
    # Hai thanh đặc bắt buộc là đỉnh và thanh cuối, và thanh cuối KHÔNG được là thanh cao
    # nhất: nếu trùng nhau thì hình chỉ còn nói "cái to nhất được nhớ", tức mất hẳn nửa
    # luận điểm (end được giữ vì nó là end, không vì nó lớn).
    # Số thanh phải đủ nhiều (6) để thấy độ DÀI bị bỏ qua — đó là duration-neglect, hệ
    # quả trực tiếp của card. Rút xuống 3 thanh là mất trục thời lượng.
    # Khác `fewer_louder` (hai HÀNG, hàng dưới rụng bớt thanh và có thanh vượt cao hơn mọi
    # thanh hàng trên): ở đây chỉ một hàng, không thanh nào cao lên, chỉ có việc được tô
    # hay không. Khác `salience_pop` (lưới chấm ĐỀU NHAU, vài chấm được tô) vì ở đây các
    # thanh cao thấp khác nhau và vị trí thứ tự mới là nội dung.
    bars = ((14, 26, 0), (31, 44, 0), (48, 72, 1), (65, 38, 0), (82, 22, 0), (99, 50, 1))
    o = []
    for x, h, keep in bars:
        fill = (f'fill="{p["acc"]}" fill-opacity="0.85"' if keep else 'fill="none"')
        o.append(f'<rect x="{x}" y="{106 - h}" width="14" height="{h}" {fill} {TS}/>')
    o.append(f'<line x1="12" y1="106" x2="115" y2="106" {TNF}/>')
    return "".join(o)


def t_felt_likelihood(p):
    # MỘT thang đo nằm ngang, hai đầu có nút chặn = dải xác suất từ thấp tới cao. Trên
    # thang có hai ô CÙNG KÍCH THƯỚC, cùng hình: cùng một biến cố, đọc ở hai chỗ. Ô ĐẶC
    # nằm gần đầu thấp = tần suất lấy từ dữ liệu, quan sát được. Ô RỖNG nằm gần đầu cao =
    # mức "chắc sẽ tệ" cảm thấy, chưa từng được quan sát. Khoảng hở giữa hai ô chính là
    # thiên kiến.
    # Hai ô bắt buộc bằng nhau tuyệt đối. Vẽ ô bên phải to hơn là đổi trục sang ĐỘ LỚN
    # của hậu quả, tức rơi sang loss-aversion/negativity — còn card này chỉ nói về XÁC
    # SUẤT. Cũng vì vậy cả hai phải nằm trên cùng một thang, không phải hai cột cạnh nhau.
    # Khác `narrow_interval` (một dải rỗng rộng + thanh đặc hẹp bên trong + điểm thật rơi
    # ra ngoài): ở đây không có khoảng tin cậy nào, chỉ có hai điểm trên thang. Khác `pull`
    # (anchoring) vì không có khối nặng nào kéo, hai ô không nối với nhau.
    return (f'<line x1="16" y1="64" x2="112" y2="64" {TNF}/>'
            f'<line x1="16" y1="50" x2="16" y2="78" {TNF}/>'
            f'<line x1="112" y1="50" x2="112" y2="78" {TNF}/>'
            f'<rect x="26" y="54" width="20" height="20" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="82" y="54" width="20" height="20" fill="none" {TS}/>')


def t_promoted_past_fit(p):
    # Ba KHUNG rỗng cao dần trên một đường nền = ba bậc vị trí, yêu cầu mỗi bậc một lớn
    # hơn. Trong khung 1 và khung 2, khối đặc lấp KÍN khung: năng lực đã được chứng minh
    # ở đúng bậc đó. Khung 3 cao thêm nhưng khối đặc bên trong GIỮ NGUYÊN cỡ của khung 2,
    # để hở một vùng rỗng phía trên. Không có khung thứ tư: chuỗi thăng tiến dừng lại
    # đúng ở chỗ khối ngừng lớn.
    # Khối ở khung 3 phải bằng ĐÚNG khối ở khung 2. Cho nó nhỏ lại là thành "người kém
    # đi", còn card nói người không đổi — chỉ có yêu cầu của vị trí là đổi.
    # Khác `ratchet` (foot-in-the-door, mint: ba bậc ĐẶC KÍN tựa vai nhau, không có khung
    # nào) — ở đây mỗi bậc là một khung rỗng và nội dung nằm ở phần khung KHÔNG được lấp.
    # Khác `fill_to_frame` (parkinsons-law: hai khung rộng hẹp khác nhau, khối chạm hai mép
    # trong CẢ HAI) vì ở đây đúng một khung không được chạm tới, và các khung xếp bậc thang.
    return (f'<rect x="14" y="88" width="30" height="20" fill="none" {TS}/>'
            f'<rect x="17" y="91" width="24" height="14" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="48" y="66" width="30" height="42" fill="none" {TS}/>'
            f'<rect x="51" y="69" width="24" height="36" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="82" y="30" width="30" height="78" fill="none" {TS}/>'
            f'<rect x="85" y="69" width="24" height="36" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<line x1="12" y1="108" x2="116" y2="108" {TNF}/>')


def t_dual_route(p):
    # Đường ngang trên = mặt tiếp nhận, chung cho cả hai bên. Bên trái: một ô nhạt (từ
    # ngữ) và ĐÚNG MỘT đường dẫn xuống một dấu vết nhỏ, nhạt. Bên phải: một ô đậm (hình
    # ảnh) và HAI đường dẫn song song xuống một dấu vết to hơn, đậm. Biến duy nhất là SỐ
    # ĐƯỜNG DẪN (1 đối 2); độ lớn của dấu vết phía dưới là hệ quả, không phải tiền đề.
    # Hai đường bên phải phải song song và cách nhau ≥20px (ở 64px là ≥10px). Vẽ chúng
    # chụm về một điểm là thành `funnel` (gộp lại), còn card nói hai kênh chạy ĐỘC LẬP
    # và cùng tồn tại; để chúng sát nhau thì ở 64px hai làn nhập thành một nét dày và
    # hình mất đúng cái biến duy nhất của nó.
    # Khác `encoding_depth` (levels-of-processing, mint: ba ô rỗng nông y hệt nhau đối lại
    # một khối đặc đâm sâu — trục là ĐỘ SÂU đối lại SỐ LẦN LẶP). Ở đây không có trục sâu
    # nào: cả hai bên đều chạy hết cùng một khoảng, chỉ khác số làn.
    return (f'<line x1="14" y1="34" x2="114" y2="34" {TNF}/>'
            f'<rect x="22" y="16" width="24" height="18" fill="{p["t2"]}" {TS}/>'
            f'<line x1="34" y1="34" x2="34" y2="84" {TNF}/>'
            f'<rect x="24" y="84" width="20" height="20" fill="{p["t2"]}" {TS}/>'
            f'<rect x="74" y="16" width="36" height="18" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<line x1="82" y1="34" x2="82" y2="76" {TNF}/>'
            f'<line x1="104" y1="34" x2="104" y2="76" {TNF}/>'
            f'<rect x="76" y="76" width="32" height="28" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>')


def t_sham_response(p):
    # Dưới đường phân cách: hai nguyên nhân CÙNG CỠ, cùng hình — bên trái tô đặc (có
    # hoạt chất), bên phải để RỖNG (viên giả, bên trong không có gì). Trên đường: hai
    # thanh phản hồi, CẢ HAI đều tô đặc và cao gần bằng nhau. Phản hồi bên phải là thật
    # và đo được, dù thứ sinh ra nó thì rỗng.
    # Thanh phản hồi bên phải tuyệt đối không được vẽ rỗng hay mờ. Chỉ cần làm nó nhạt đi
    # là hình tự bác bỏ card: placebo không phải "phản hồi giả", nó là phản hồi thật từ
    # nguyên nhân rỗng. Hai nguyên nhân cũng phải bằng nhau tuyệt đối — khác cỡ là đổi
    # trục sang liều lượng.
    # Khác `inert_input` (information-bias, amber: hai cột đầu vào CHÊNH LỆCH khối lượng
    # và hai ô kết quả y hệt nhau — điểm là kết quả KHÔNG nhích). Ở đây ngược hẳn: đầu
    # vào bằng nhau về cỡ mà khác nhau ở ruột, và kết quả thì CÓ, ở cả hai bên.
    return (f'<rect x="24" y="24" width="26" height="60" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="78" y="36" width="26" height="48" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<line x1="14" y1="84" x2="114" y2="84" {TNF}/>'
            f'<rect x="21" y="88" width="32" height="22" fill="{p["acc"]}" '
            f'fill-opacity="0.85" {TS}/>'
            f'<rect x="75" y="88" width="32" height="22" fill="none" {TS}/>')


def t_outside_view_ignored(p):
    # Một trục dọc bên trái = mốc khởi đầu, chung cho mọi thanh: tất cả đều là dự án cùng
    # lớp, xuất phát từ cùng một chỗ. Ba thanh RỖNG dài BẰNG NHAU = các dự án tương tự đã
    # hoàn thành; rỗng vì dữ liệu có sẵn nhưng không ai mở ra xem. Thanh ĐẶC trên cùng,
    # cùng gốc, ngắn hơn hẳn cả ba = ước lượng mới, dựng từ inside view.
    # Ba thanh tham chiếu phải dài BẰNG NHAU tuyệt đối: lệch nhau là thành một phân bố,
    # tức hình chuyển nghĩa sang "rủi ro đuôi". Ở đây điểm mấu chốt là chúng nhất quán
    # với nhau và nhất quán bác bỏ ước lượng kia.
    # Khác `over_scaled_forecast` (affective forecasting: MỘT khung rỗng lớn và một khối
    # đặc nhỏ ở góc, lệch trên cả hai trục, và chiều lệch là dự báo LỚN hơn thực). Ở đây
    # lệch một trục duy nhất (thời lượng) và ngược chiều: ước lượng NHỎ hơn thực. Khác
    # `vital_few` (hai dải cùng gốc trái, mẩu đặc nằm đúng trên khối đặc lớn) vì ở đây có
    # ba thanh tham chiếu và chúng để rỗng.
    o = [f'<line x1="16" y1="20" x2="16" y2="110" {TNF}/>',
         f'<rect x="16" y="24" width="34" height="18" fill="{p["acc"]}" '
         f'fill-opacity="0.85" {TS}/>']
    o += [f'<rect x="16" y="{y}" width="92" height="16" fill="none" {TS}/>'
          for y in (54, 74, 94)]
    return "".join(o)


def t_unvoiced_row(p):
    # Một đường ngang = mặt nhìn thấy được. TRÊN đường: bốn ô ĐẶC giống hệt nhau — hành
    # vi bên ngoài, ai cũng như ai. DƯỚI đường: bốn ô RỖNG cũng giống hệt nhau, đặt đúng
    # dưới từng ô trên — suy nghĩ thật, và cả bốn đều giống nhau y như thế. Rỗng vì không
    # ai trong hình quan sát được chúng.
    # Hai hàng bắt buộc ĐỀU TUYỆT ĐỐI trong nội bộ mỗi hàng: chỉ cần một ô khác cỡ là
    # hình đọc thành "có một người khác biệt", tức đúng điều card phủ định — nghịch lý ở
    # đây là ai cũng nghĩ mình là ngoại lệ trong khi không ai là ngoại lệ.
    # Khác `veil` (curse-of-knowledge: rào cản nằm giữa NGƯỜI XEM và vật) — ở đây đường
    # ngang không che gì với người xem, nó chia cái các cá thể thấy của NHAU. Khác
    # `tint_carryover` (lưới 2x2 cùng sắc độ, nói về chấm điểm lây lan) và khác
    # `deserved_backfill` (hai cột đối nhau, ô rỗng suy ra từ kết cục) vì ở đây hai hàng
    # là hai LỚP của cùng những cá thể đó, không phải hai thứ khác nhau.
    o = [f'<rect x="{x}" y="26" width="22" height="22" fill="{p["acc"]}" '
         f'fill-opacity="0.8" {TS}/>' for x in (14, 40, 66, 92)]
    o.append(f'<line x1="12" y1="64" x2="116" y2="64" {TNF}/>')
    o += [f'<rect x="{x}" y="82" width="22" height="22" fill="none" {TS}/>'
          for x in (14, 40, 66, 92)]
    return "".join(o)


def t_liking_flip(p):
    # Hàng trên là hai đối tượng cùng loại, chỉ khác ĐỘ ĐẬM: vòng đặc = người được yêu
    # thích, vòng rỗng = người ít được yêu thích. Đó là biến điều tiết, và nó phải hiện
    # ra trong hình vì nó mới là thứ phân biệt card này với các card quy kết khác.
    # Hàng dưới, mỗi bên có ĐÚNG hai hành vi cùng loại với bên kia: ô tô nhạt = hành vi
    # tốt, ô rỗng = hành vi xấu. Cỡ của chúng ĐẢO NHAU giữa hai bên: bên được yêu thích
    # thì hành vi tốt to (đọc thành bản chất) và hành vi xấu nhỏ; bên ít được yêu thích
    # thì ngược lại. Loại hành vi không đổi, chỉ có cái nào được đọc to.
    # Bốn ô phải giữ đúng hai loại tô ở cả hai bên. Đổi luôn kiểu tô theo bên là thành
    # "hai bên làm hai việc khác nhau", tức mất tiền đề cùng-một-hành-vi.
    # Máng giữa hai cặp phải RỘNG HƠN khe trong mỗi cặp (12px đối 2px). Bản dựng đầu để
    # máng 2px còn khe trong 4px: ở 64px bốn ô dính thành một dãy liền và mất hẳn việc
    # mỗi cặp thuộc về vòng nào phía trên.
    # Khác `locus_flip` (fundamental-attribution-error, mint: hai khung vuông cạnh nhau,
    # một chấm TRONG / một chấm NGOÀI) — ở đó biến là vị trí trong/ngoài và không có biến
    # điều tiết nào; ở đây không có chấm trong/ngoài, biến là CỠ, và có thêm token yêu
    # thích ở hàng trên. Khác `mirror` (actor-observer: một vòng bị chia đôi bởi trục
    # gương) vì ở đây là hai đối tượng rời, không phải một sự việc soi hai lần.
    return (f'<circle cx="34" cy="26" r="13" fill="{p["acc"]}" fill-opacity="0.85" {TS}/>'
            f'<circle cx="94" cy="26" r="13" fill="none" {TS}/>'
            f'<rect x="14" y="76" width="28" height="28" fill="{p["t3"]}" {TS}/>'
            f'<rect x="44" y="90" width="14" height="14" fill="none" {TS}/>'
            f'<rect x="70" y="90" width="14" height="14" fill="{p["t3"]}" {TS}/>'
            f'<rect x="86" y="76" width="28" height="28" fill="none" {TS}/>'
            f'<line x1="12" y1="104" x2="116" y2="104" {TNF}/>')


def t_commit_lift(p):
    # Một trục dọc giữa khung = mốc đã trả tiền. Hai bên trục là CÙNG MỘT đại lượng đo
    # hai lần: thanh bên phải cao hơn hẳn thanh bên trái, cùng bề rộng, cùng đường nền.
    # Dưới đường nền, hai chùm chấm rỗng CÙNG SỐ LƯỢNG, cùng cỡ, đặt đối xứng: chứng cứ
    # không thêm một mẩu nào giữa hai lần đo. Toàn bộ nội dung nằm ở chênh lệch chiều cao
    # trong khi chùm chấm thì không đổi.
    # Hai thanh chứng cứ bắt buộc dài BẰNG NHAU. Kéo dài thanh bên phải là hình tự trả
    # lời "có thông tin mới", tức không còn là rationalization mà thành cập nhật hợp lý.
    # Bản dựng đầu vẽ chứng cứ thành hai chùm ba chấm r=5: ở 64px mỗi chấm còn 5px, dưới
    # ngưỡng đọc được, nên phần "chứng cứ không đổi" biến mất và hình chỉ còn hai cột.
    # Khác `ex_post_grade` (outcome-bias, amber: hai khung quyết định ruột y hệt nhau, sắc
    # độ sao chép từ kết cục nằm dưới) — ở đó biến là NHÃN chấm điểm và có kết cục tham
    # gia; ở đây chưa có kết cục nào, chỉ có hành động chi tiền, và biến là chiều cao.
    # Khác `threshold` (một đường mốc để vượt qua) vì trục ở đây là một MỐC THỜI GIAN, đi
    # theo chiều dọc, và không có gì "vượt" nó.
    o = [f'<line x1="14" y1="88" x2="114" y2="88" {TNF}/>',
         f'<line x1="64" y1="16" x2="64" y2="110" {TNF}/>',
         f'<rect x="28" y="58" width="26" height="30" fill="{p["acc"]}" '
         f'fill-opacity="0.85" {TS}/>',
         f'<rect x="74" y="30" width="26" height="58" fill="{p["acc"]}" '
         f'fill-opacity="0.85" {TS}/>']
    o += [f'<rect x="{x}" y="94" width="34" height="14" fill="none" {TS}/>'
          for x in (26, 72)]
    return "".join(o)


def t_blanket_affect(p):
    # Bốn cá thể vẽ RỖNG, cao thấp và rộng hẹp KHÁC NHAU — biến thiên cá nhân có thật và
    # còn nguyên trong hình. Một dải ĐẶC duy nhất, dày, đắp ngang qua cả bốn ở đúng cùng
    # một độ cao và cùng một sắc độ: cảm xúc gán theo tư cách thành viên, không đọc gì
    # bên trong từng người. Dải chạy luôn qua các khoảng trống giữa họ, vì nó dính vào
    # phạm trù chứ không dính vào cá nhân.
    # Dải phải là MỘT khối liền. Cắt thành bốn mẩu trên bốn cá thể là thành bốn phán xét
    # riêng, tức mất nghĩa "chỉ dựa trên việc họ thuộc nhóm nào".
    # Dải vẽ TRƯỚC, bốn cá thể vẽ SAU để nét viền của họ không bị dải phủ mất — cái phải
    # đọc được là sự khác nhau giữa họ vẫn còn đó bên dưới lớp cảm xúc.
    # Khác `group_tint_applied` (implicit-stereotypes, mint: một cụm phần tử ĐỒNG NHẤT
    # sắc độ, nối sang một cá thể lớn nhận đúng sắc độ đó) — ở đó các phần tử vốn đã
    # giống nhau và có mối nối chỉ rõ chiều lan; ở đây các cá thể khác nhau rõ rệt, không
    # có mối nối nào, và cái phủ lên là một dải có BỀ DÀY cắt xuyên qua họ.
    o = [f'<rect x="10" y="78" width="108" height="16" fill="{p["acc"]}" '
         f'fill-opacity="0.55" {TS}/>']
    o += [f'<rect x="{x}" y="{106 - h}" width="{w}" height="{h}" fill="none" {TS}/>'
          for x, w, h in ((14, 20, 44), (40, 22, 66), (68, 18, 32), (92, 20, 56))]
    return "".join(o)


CONCEPT_OBJECTS_20260929 = dict(
    peak_end_kept=t_peak_end_kept, felt_likelihood=t_felt_likelihood,
    promoted_past_fit=t_promoted_past_fit, dual_route=t_dual_route,
    sham_response=t_sham_response, outside_view_ignored=t_outside_view_ignored,
    unvoiced_row=t_unvoiced_row, liking_flip=t_liking_flip,
    commit_lift=t_commit_lift, blanket_affect=t_blanket_affect,
)

CONCEPT_MEANING.update({
    "peak_end_kept": "sáu thanh cao thấp khác nhau trên một đường nền, chỉ thanh cao nhất "
                     "và thanh cuối cùng được tô đặc",
    "felt_likelihood": "một thang đo có hai nút chặn, hai ô bằng nhau trên đó: ô đặc gần "
                       "đầu thấp, ô rỗng đẩy xa về đầu cao",
    "promoted_past_fit": "ba khung rỗng cao dần, khối đặc lấp kín hai khung đầu rồi giữ "
                         "nguyên cỡ ở khung ba nên để hở phần trên",
    "dual_route": "cùng một mặt tiếp nhận: bên trái một đường dẫn xuống dấu vết nhạt nhỏ, "
                  "bên phải hai đường song song xuống dấu vết đậm to",
    "sham_response": "hai nguyên nhân cùng cỡ một đặc một rỗng, nhưng hai thanh phản hồi "
                     "phía trên đều đặc và cao gần bằng nhau",
    "outside_view_ignored": "cùng một gốc trái: ba thanh rỗng dài bằng nhau và một thanh "
                            "đặc ngắn hơn hẳn cả ba",
    "unvoiced_row": "một đường ngang chia hai hàng bốn ô đều tuyệt đối: hàng trên đặc, "
                    "hàng dưới rỗng, đặt đúng dưới từng ô trên",
    "liking_flip": "hai vòng một đặc một rỗng ở hàng trên; hàng dưới mỗi bên hai ô cùng "
                   "hai kiểu tô, cỡ của chúng đảo nhau giữa hai bên",
    "commit_lift": "một trục dọc chia hai thanh cùng bề rộng khác chiều cao, dưới đường "
                   "nền là hai thanh chứng cứ rỗng dài bằng nhau",
    "blanket_affect": "bốn khung rỗng khác cỡ bị một dải đặc dày duy nhất đắp ngang ở "
                      "cùng một độ cao",
})

THUMB_REGISTRY.update(CONCEPT_OBJECTS_20260929)
