#!/usr/bin/env python3
"""Render thumbnail 128x128 cho stuff card chưa có ảnh.

Nguồn: docs/theunseen_illustration_prompt_library.xlsx, sheet `Article Index`.
Idempotent: bỏ qua mọi card đã có public/assets/stuff/<slug>.png.

    python3 scripts/illustrations/render_thumbs.py [--limit 10] [--dry-run]
"""
import argparse
import hashlib
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
        # sửa ở batch #3: bản proportion trùng byte với base-rate-fallacy (cùng hue amber),
        # mà base-rate-fallacy mới là card phần/tổng đúng nghĩa. threshold cũng sát nghĩa hơn.
        "threshold",
        "một xác suất chưa tới 100% bị làm tròn thành 'chắc chắn' khi vượt qua một ngưỡng chủ "
        "quan — đúng nghĩa tipping point. amber ở đây phân biệt được với antifragility (mint)"),
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
        "contrast",
        "một nguồn quyền lực đứng như một khối nặng đối lập với toàn bộ bằng chứng còn lại — "
        "đổi từ pull sang contrast vì pull+mint đã trùng byte với anchoring (anchoring giữ pull, "
        "đúng nghĩa 'kéo lệch ước lượng' hơn vì có một con số neo cụ thể, còn ở đây là trọng "
        "lượng của nguồn phát ngôn, không phải một điểm neo)"),
    "automation-bias": (
        "gate",
        "concept object: chỉ thông tin đến từ hệ thống tự động mới lọt qua cổng; "
        "thông tin trái ngược dù đúng vẫn bị chặn"),
    "availability-cascade": (
        "echo",
        "concept object: chính sự lan truyền lặp lại tạo ra cảm giác đáng tin, không phải bằng chứng. "
        "echo sát hơn cycle vì cascade là khuếch đại một chiều, không phải vòng khép kín"),
    "availability-heuristic": (
        "funnel",
        "rất nhiều ký ức tồn tại, nhưng chỉ những thứ dễ bật ra trong đầu mới lọt qua để trở "
        "thành phán đoán về tần suất/nguy hiểm — đổi từ spectrum sang funnel vì spectrum+amber "
        "đã trùng byte với ambiguity-effect (ambiguity-effect giữ spectrum, đúng nghĩa 'dải liên "
        "tục từ biết rõ tới mù mờ' hơn, còn ở đây bản chất là một phễu lọc theo độ dễ nhớ)"),

    # ---- batch #3 (2026-08-28) — xlsx gán 5 hierarchy + 4 branching + 1 proportion.
    # Chỉ 1/10 (base-rate-fallacy) là đúng. Thêm 2 concept object mới: `rebound`, `odd_one_out`
    # (registry 24 -> 26) vì không hình nào trong 24 hình cũ diễn được hai quan hệ đó.
    "backfire-effect": (
        "rebound",
        "concept object MỚI: đính chính đập vào rào cản bản sắc rồi bật ngược — niềm tin sai "
        "chẳng những không giảm mà còn đậm hơn. Không hình nào trong registry cũ diễn được "
        "'kết quả đi ngược ý định'; divergence chỉ nói 'một điểm rẽ nhiều nhánh'"),
    "bandwagon-effect": (
        "pull",
        "concept object: đám đông là một khối có trọng lực — càng đông thì lực hút càng mạnh, "
        "cá nhân bị kéo vào vì khối lượng chứ không vì bằng chứng. hierarchy của xlsx sai hẳn: "
        "ở đây không có quan hệ cha-con nào"),
    "barnum-effect": (
        "nested_scope",
        "một mô tả phủ được gần như mọi người nhưng được đọc thành cái lõi riêng của một người: "
        "vòng ngoài = ai cũng đúng, lõi = 'đúng với riêng tôi'"),
    "base-rate-fallacy": (
        "proportion",
        "giữ nguyên xlsx — ca hiếm mà cột Hero shape đúng: cả bài là quan hệ phần/tổng, "
        "lát cắt dương tính thật quá nhỏ so với khối dương tính giả"),
    "belief-bias": (
        "fracture",
        "concept object: cấu trúc lập luận và kết luận lẽ ra phải khớp theo logic, nhưng ở đây "
        "lệch nhau — và ta vẫn chấp nhận vì kết luận nghe đúng. hierarchy đã dùng cho "
        "argument-from-fallacy với đúng nghĩa cha-con nên không dùng lại ở đây"),
    "bias-blind-spot": (
        "balance",
        "concept object: chuẩn kép — cùng một loại bằng chứng, cân về phía người khác thì nặng "
        "trịch, về phía mình thì nhẹ tênh. Đã loại 2 phương án trước vì render ra ảnh TRÙNG BYTE "
        "với card cũ cùng hue amber: veil đụng armchair-fallacy, mirror đụng actor-observer-bias"),
    "bizarreness-effect": (
        "odd_one_out",
        "concept object MỚI: nền đồng nhất là MỘT PHẦN của cơ chế — card nói rõ hiệu ứng biến "
        "mất nếu cả danh sách đều kỳ lạ. contrast chỉ nói 'hai thứ khác nhau', không có nền"),
    "black-swan-theory": (
        "tail_event",
        "concept object MỚI: đuôi phân phối — chuỗi biến cố thường xuyên nhưng nhỏ, và một biến "
        "cố hiếm có độ lớn áp đảo nằm tách hẳn. spectrum (thử đầu) bị loại vì đã có ambiguity-effect "
        "và availability-heuristic dùng, cả ba cùng hue amber sẽ ra ba thumbnail giống hệt nhau; "
        "threshold thì đụng antifragility — card anh em của Taleb"),
    "bucket-error": (
        "overlap_phases",
        "các mệnh đề lẽ ra độc lập bị chồng vào chung một vùng — chạm vào vùng giao thì cả hai "
        "cùng bị đụng, nên sửa một mảnh nhỏ bị cảm nhận như phủ nhận cả khối"),
    "bystander-effect": (
        "divergence",
        "khuếch tán trách nhiệm: một tình huống cần giúp bị chia thành nhiều phần cho nhiều "
        "người, càng nhiều nhánh mỗi nhánh càng loãng cho tới khi không ai hành động"),
    "cathedral-effect": (
        "halo_spill",
        "concept object: chiều cao trần là một ấn tượng không gian mồi (prime) rồi lan sang "
        "cách xử lý những vấn đề không liên quan gì tới không gian — đúng nghĩa 'ấn tượng lan "
        "sang đánh giá lân cận', không phải quan hệ cha-con của hierarchy"),
    "change-blindness": (
        "beam",
        "concept object: chú ý dồn hết vào việc đếm đường chuyền (điểm sáng), còn phần thay đổi "
        "thực sự xảy ra trong vùng đang tối đi — beam đúng nghĩa hơn hierarchy vì đây không phải "
        "quan hệ phân tầng mà là hệ quả của việc chú ý chỉ rọi được một điểm"),
    "cheerleader-effect": (
        "coverage_sphere",
        "khuôn mặt trung bình của cả nhóm phủ lên nhận thức về từng khuôn mặt riêng lẻ, kéo "
        "đánh giá về gần mức trung bình dễ nhìn hơn — không phải quan hệ lồng nhau (nesting) như "
        "xlsx gán, vì không có 'lõi' nào bị bao bọc, chỉ có một lớp phủ đè lên toàn bộ"),
    "chestertons-fence": (
        "layers",
        "hàng rào là một lớp trầm tích lịch sử — lý do dựng lên nằm ở tầng dưới, phải đào tới đó "
        "trước khi gỡ lớp trên; layers sát nghĩa hơn hierarchy vì đây không phải quan hệ cha-con "
        "mà là quan hệ tích tụ theo thời gian"),
    "choice-overload": (
        "spectrum",
        "24 loại mứt là một dải gần như liên tục, càng dày đặc trên dải đó càng khó phân biệt và "
        "khó chọn — spectrum đúng nghĩa hơn divergence vì đây không phải một điểm rẽ nhánh, mà là "
        "mật độ lựa chọn dọc theo một dải"),
    "choice-supportive-bias": (
        "echo",
        "concept object: mỗi lần nhớ lại, câu chuyện về lựa chọn đã chọn được kể lại và khuếch đại "
        "thêm một chút theo hướng tích cực — đúng nghĩa lặp lại làm khuếch đại của echo, không "
        "phải một điểm rẽ nhánh (divergence)"),
    "circle-of-competence": (
        "in_out_ring",
        "concept object: đúng nghĩa đen tên gọi — có một vòng tròn, bên trong là phạm vi hiểu biết "
        "đủ sâu để quyết định, bên ngoài là chỉ biết bề mặt; in_out_ring sát hơn hẳn hierarchy vì "
        "đây không phải quan hệ cha-con mà là ranh giới thuộc về"),
    "clustering-illusion": (
        "cycle",
        "một khi não bộ 'thấy' cụm trong dữ liệu ngẫu nhiên, mỗi điểm dữ liệu tiếp theo lại được "
        "diễn giải để củng cố thêm cho cụm đó — vòng tự củng cố (cycle) đúng hơn network vì không "
        "có liên kết thật giữa các điểm, chỉ có vòng lặp diễn giải; cũng tránh trùng hình với "
        "apophenia (network) vốn diễn tả cùng một nhóm hiện tượng thấy-quy-luật-trong-nhiễu"),
    "cognitive-dissonance": (
        "mirror",
        "concept object: cùng một con người soi qua hai khung — niềm tin đang giữ và hành vi đã "
        "làm — lệch nhau, buộc phải chỉnh một trong hai để khớp lại; mirror đúng hơn hierarchy vì "
        "đây không phải quan hệ phân tầng mà là cùng một sự việc nhìn qua hai lăng kính mâu thuẫn"),
    "cognitive-load-theory": (
        "threshold",
        "bộ nhớ làm việc có một sức chứa cố định — vượt ngưỡng đó, chất lượng xử lý sập nhanh "
        "chứ không suy giảm từ từ; threshold đúng nghĩa hơn hierarchy vì đây là một giới hạn dung "
        "lượng, không phải quan hệ cha-con"),
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

    if not args.dry_run:
        dupes = {}
        for c in index:
            f = os.path.join(ASSETS, f"{c['slug']}.png")
            if os.path.exists(f):
                dupes.setdefault(hashlib.md5(open(f, "rb").read()).hexdigest(),
                                 []).append(c["slug"])
        clashes = [v for v in dupes.values() if len(v) > 1]
        if clashes:
            print("\n!! TRÙNG BYTE — các card dưới đây render ra ĐÚNG một ảnh:", file=sys.stderr)
            for v in clashes:
                print("   " + " == ".join(v), file=sys.stderr)
            print("   (đổi metaphor hoặc hue cho một trong hai, xem mục C của "
                  "docs/scheduled-task-illustrations.md)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
