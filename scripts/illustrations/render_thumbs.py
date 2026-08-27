#!/usr/bin/env python3
"""Render thumbnail 128x128 cho stuff card chưa có ảnh.

Nguồn: docs/theunseen_illustration_prompt_library.xlsx, sheet `Article Index`.
Idempotent: bỏ qua mọi card đã có public/assets/stuff/<slug>.png.

    python3 scripts/illustrations/render_thumbs.py [--limit 10] [--dry-run]
"""
import argparse
import io
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import openpyxl                      # noqa: E402
import cairosvg                      # noqa: E402
from illus import thumb, SHAPE_MAP   # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
XLSX = os.path.join(ROOT, "docs", "theunseen_illustration_prompt_library.xlsx")
ASSETS = os.path.join(ROOT, "public", "assets", "stuff")
CONTENT = os.path.join(ROOT, "content", "stuff")

# Override thủ công khi shape trong xlsx rõ ràng sai với nội dung card.
# Cột Hero shape trong xlsx dồn ~58% corpus vào hierarchy + branching (README của
# chính file ghi đây là "design hypothesis"), nên phải chẩn đoán lại theo `back`
# của từng card. slug -> (metaphor, "lý do")
OVERRIDES = {
    "abilene-paradox": (
        "cycle",
        "vòng phản hồi tự củng cố — im lặng của mỗi người được người kế tiếp đọc thành "
        "đồng thuận; dùng cycle thay network để không trùng hình với apophenia"),
    "actor-observer-bias": (
        "mirror",
        "concept object: cùng MỘT hành vi soi qua hai khung quy kết (mình=hoàn cảnh / "
        "người khác=tính cách). mirror sát nghĩa hơn contrast vì contrast chỉ nói 'hai thứ khác nhau', "
        "còn ở đây phải thấy được là cùng một sự việc"),
    "adverse-selection": (
        "funnel",
        "thị trường bị sàng lọc lệch — nhóm rủi ro cao tự chọn tham gia và đọng lại, "
        "không phải quan hệ cha-con"),
    "affect-heuristic": (
        "coverage_sphere",
        "một tín hiệu cảm xúc duy nhất phủ lên toàn bộ đánh giá rủi ro/lợi ích"),
    "affective-forecasting": (
        "proportion",
        "focalism: cảm xúc hiện tại chiếm tỉ trọng quá lớn trong bức tranh tương lai — "
        "proportion đọc rõ hơn contrast và không trùng với actor-observer-bias"),
    "ambiguity-effect": (
        "spectrum",
        "dải từ biết rõ xác suất tới mù mờ; mức né tăng dần theo độ mơ hồ"),
    "anchoring": (
        "pull",
        "concept object: một khối nặng kéo lệch toàn bộ ước lượng còn lại. divergence chỉ ra "
        "'một điểm rẽ nhiều nhánh' — thiếu mất lực kéo, vốn là bản chất của anchoring"),
    "anthropomorphism": (
        "overlap_phases",
        "ranh giới người / không-người bị chồng lấn, không phải phân loại tầng bậc"),
    "antifragility": (
        "threshold",
        "vượt ngưỡng biến động thì hệ mạnh lên thay vì vỡ — đúng định nghĩa tipping point"),
    "apophenia": (
        "network",
        "áp một mạng liên kết lên các điểm vốn rời rạc"),

    # ---- batch #2 (2026-08-27) — xlsx gán 4 hierarchy + 5 divergence + 1 cycle,
    # tức 9/10 card sẽ nhận đúng 2 hình. Chẩn đoán lại toàn bộ theo `back`.
    "appeal-to-novelty": (
        "balance",
        "concept object: hai thứ giống hệt nhau, khác biệt duy nhất là tuổi, nhưng cán cân "
        "vẫn nghiêng về phía 'mới' — divergence không diễn được sự thiên lệch này"),
    "appeal-to-probability-fallacy": (
        "proportion",
        "khả năng cao bị đọc thành chắc chắn — phải thấy được phần trăm CÒN LẠI bị lờ đi, "
        "đó chính là lát cắt trong donut"),
    "argument-from-fallacy": (
        "hierarchy",
        "kết luận treo dưới lập luận: cắt nút cha thì nhánh con bị coi là rơi theo. "
        "Đây là ca hiếm mà hierarchy của xlsx thực sự đúng"),
    "armchair-fallacy": (
        "veil",
        "concept object: ràng buộc, dữ liệu và trade-off của người trong cuộc bị che khuất — "
        "cái không nhìn thấy mới là nguồn của sự tự tin sai chỗ"),
    "attentional-bias": (
        "beam",
        "concept object: chú ý dồn vào một thứ khiến nó nổi bật lên, phần còn lại tối đi. "
        "Tần suất thật không đổi, chỉ có vùng được rọi sáng thay đổi"),
    "attribute-substitution": (
        "contrast",
        "một câu hỏi khó bị đánh tráo bằng một câu hỏi dễ — hai khối có độ phức tạp hình học "
        "trái ngược, đặt thay chỗ nhau"),
    "authority-bias": (
        "pull",
        "concept object: một nguồn có trọng lượng lớn kéo lệch toàn bộ phán đoán còn lại, "
        "bất kể bằng chứng"),
    "automation-bias": (
        "gate",
        "concept object: chỉ thông tin đến từ hệ thống tự động mới lọt qua cổng; "
        "thông tin trái ngược dù đúng vẫn bị chặn"),
    "availability-cascade": (
        "echo",
        "concept object: chính sự lan truyền lặp lại tạo ra cảm giác đáng tin, không phải bằng chứng. "
        "echo sát hơn cycle vì cascade là khuếch đại một chiều, không phải vòng khép kín"),
    "availability-heuristic": (
        "spectrum",
        "trọng số đánh giá giảm dần theo độ khó nhớ lại: thứ dễ bật ra trong đầu được cho là "
        "phổ biến/nguy hiểm hơn thực tế"),
}


def read_index():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Article Index"]
    rows = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h else "" for h in next(rows)]
    ix = {name: header.index(name) for name in
          ("#", "File", "Title", "Hero shape", "Hue")}
    out = []
    for r in rows:
        if not r or r[ix["File"]] is None:
            continue
        out.append(dict(
            n=r[ix["#"]],
            slug=str(r[ix["File"]]).removesuffix(".md"),
            title=r[ix["Title"]],
            shape=str(r[ix["Hero shape"]]).strip().lower(),
            hue=str(r[ix["Hue"]]).strip().lower(),
        ))
    out.sort(key=lambda d: d["n"])
    return out


def set_frontmatter_image(slug):
    """Set `image:` trong frontmatter. Không đụng field nào khác. True nếu có thay đổi."""
    path = os.path.join(CONTENT, f"{slug}.md")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
    if not m:
        return None
    fm, rest = m.group(1), text[m.end():]
    line = f"image: /assets/stuff/{slug}.png"
    lines = fm.rstrip("\n").split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("image:"):
            if ln.strip() == line:
                return False
            lines[i] = line
            break
    else:
        pub = next((i for i, ln in enumerate(lines) if ln.startswith("published:")), None)
        lines.insert(pub if pub is not None else len(lines), line)
    open(path, "w", encoding="utf-8").write("---\n" + "\n".join(lines) + "\n---\n" + rest)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default=None,
                    help="danh sách slug ngăn cách bằng dấu phẩy — render lại đúng các card này "
                         "(bỏ qua luật idempotent), dùng khi sửa metaphor")
    ap.add_argument("--png-size", type=int, default=512,
                    help="cạnh PNG xuất ra (mặc định 512). Ảnh này vừa là thumbnail 64px vừa là "
                         "ảnh minh hoạ chính của card, nên cần đủ lớn để không vỡ ở khổ lớn; "
                         "SVG đi kèm mới là nguồn scale vô hạn.")
    args = ap.parse_args()

    os.makedirs(ASSETS, exist_ok=True)
    index = read_index()
    if args.only:
        want = [s.strip() for s in args.only.split(",") if s.strip()]
        pending = [c for c in index if c["slug"] in want]
        args.limit = len(pending)
    else:
        pending = [c for c in index if not os.path.exists(os.path.join(ASSETS, f"{c['slug']}.png"))]

    if not pending:
        print("COVERAGE 100% — không còn card nào thiếu ảnh.")
        return 0

    batch = pending[:args.limit]
    print(f"total={len(index)} missing={len(pending)} batch={len(batch)}\n")
    print(f"{'slug':<40} {'idea shape':<14} {'metaphor':<16} hue")

    for c in batch:
        metaphor, reason = OVERRIDES.get(c["slug"], (None, None))
        if metaphor is None:
            metaphor = SHAPE_MAP.get(c["shape"])
        if metaphor is None:
            print(f"  !! shape lạ: {c['slug']} -> {c['shape']}", file=sys.stderr)
            return 1
        hue = c["hue"] if c["hue"] in ("mint", "amber") else "mint"
        print(f"{c['slug']:<40} {c['shape']:<14} {metaphor:<16} {hue}"
              + (f"   [override: {reason}]" if reason else ""))
        if args.dry_run:
            continue

        svg = thumb(metaphor, hue)
        open(os.path.join(ASSETS, f"{c['slug']}.svg"), "w", encoding="utf-8").write(svg)
        # render 2x kích thước đích rồi hạ xuống bằng Lanczos để có antialias sạch
        size = args.png_size
        buf = io.BytesIO()
        cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                         output_width=size * 2, output_height=size * 2)
        # temp ra ngoài repo: thư mục mount có thể không cho unlink
        big = os.path.join(tempfile.gettempdir(), f"{c['slug']}.tmp.png")
        open(big, "wb").write(buf.getvalue())
        subprocess.run(["convert", big, "-filter", "Lanczos", "-resize", f"{size}x{size}",
                        "-strip", os.path.join(ASSETS, f"{c['slug']}.png")], check=True)
        os.remove(big)
        set_frontmatter_image(c["slug"])

    print(f"\nremaining after batch = {len(pending) - (0 if args.dry_run else len(batch))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
