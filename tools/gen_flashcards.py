#!/usr/bin/env python3
"""
gen_flashcards.py — Bơm gợi ý `front` / `back` / `source` / `difficulty`
cho các thẻ trong my_collections/_stuff/*.md

Nguyên tắc AN TOÀN:
- Chỉ điền field ĐANG TRỐNG hoặc THIẾU. Không bao giờ ghi đè nội dung bạn đã viết.
- Idempotent: chạy lại nhiều lần không đổi kết quả.
- Mặc định --dry-run (chỉ xem trước). Thêm --write để thực sự ghi file.
- Giữ nguyên định dạng file: chỉ chèn/sửa đúng dòng cần thiết, không dump lại YAML.

Nguồn dữ liệu tự suy ra từ thân bài:
- back   = đoạn định nghĩa đầu tiên trong body (bỏ dòng "[More information](...)").
- source = link http đầu tiên trong body (thường là Wikipedia).
- front  = câu hỏi mẫu tạo từ title (bạn nên chỉnh tay cho tự nhiên hơn).

Dùng:
    python3 tools/gen_flashcards.py                 # xem trước tất cả
    python3 tools/gen_flashcards.py --show 5        # xem 5 thẻ đầu chi tiết
    python3 tools/gen_flashcards.py --only anchoring
    python3 tools/gen_flashcards.py --write         # áp dụng
"""
import argparse
import os
import re
import sys

STUFF_DIR = os.path.join("my_collections", "_stuff")

# Câu hỏi mặt trước mẫu. {t} = title. Chỉnh cho hợp category của bạn.
FRONT_TEMPLATE = "'{t}' là gì, và nó tác động thế nào đến cách bạn nghĩ hoặc ra quyết định?"

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)
LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)]+)\)")


def split_front_matter(text):
    m = FM_RE.match(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def has_key(fm, key):
    return re.search(r"^%s\s*:" % re.escape(key), fm, re.M) is not None


def key_value_empty(fm, key):
    """True nếu key tồn tại nhưng giá trị rỗng ('' hoặc "" hoặc trống)."""
    m = re.search(r"^%s\s*:\s*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return False
    v = m.group(1).strip()
    return v in ("", '""', "''")


def get_value(fm, key):
    m = re.search(r"^%s\s*:\s*(.*)$" % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else None


def yaml_dq(s):
    """Bọc chuỗi trong dấu nháy kép YAML an toàn."""
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return '"%s"' % s


def derive_from_body(body):
    """Lấy định nghĩa (paragraph đầu) + source url từ body markdown."""
    source = ""
    para = []
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("[") and "More information" in line:
            m = LINK_RE.search(line)
            if m and not source:
                source = m.group(2)
            continue
        if LINK_RE.fullmatch(line or ""):  # dòng chỉ chứa 1 link
            m = LINK_RE.search(line)
            if m and not source:
                source = m.group(2)
            continue
        if line == "":
            if para:  # đã có đoạn đầu -> dừng
                break
            continue
        para.append(line)
    definition = " ".join(para).strip()
    # gỡ markdown link còn sót trong đoạn -> giữ text
    definition = LINK_RE.sub(r"\1", definition)
    if not source:
        m = LINK_RE.search(body)
        if m:
            source = m.group(2)
    return definition, source


def insert_after_title(fm, new_lines):
    lines = fm.splitlines()
    out, inserted = [], False
    for ln in lines:
        out.append(ln)
        if not inserted and re.match(r"^title\s*:", ln):
            out.extend(new_lines)
            inserted = True
    if not inserted:  # không có title -> chèn đầu
        out = new_lines + lines
    return "\n".join(out)


def replace_empty_key(fm, key, value_literal):
    return re.sub(
        r"^(%s\s*:\s*).*$" % re.escape(key),
        lambda m: m.group(1) + value_literal,
        fm,
        count=1,
        flags=re.M,
    )


def process(text):
    fm, body = split_front_matter(text)
    if fm is None:
        return None, {}
    title = get_value(fm, "title") or ""
    title = title.strip().strip('"').strip("'")
    definition, source = derive_from_body(body)

    changes = {}
    new_after_title = []

    def want(key, value):
        """Điền key nếu thiếu, hoặc thay nếu đang rỗng."""
        nonlocal fm
        if value in (None, ""):
            return
        if key_value_empty(fm, key):
            fm = replace_empty_key(fm, key, value)
            changes[key] = "filled-empty"
        elif not has_key(fm, key):
            new_after_title.append("%s: %s" % (key, value))
            changes[key] = "added"
        # else: đã có giá trị -> bỏ qua (không ghi đè)

    want("front", yaml_dq(FRONT_TEMPLATE.format(t=title)) if title else "")
    want("back", yaml_dq(definition) if definition else "")
    want("source", yaml_dq(source) if source else "")
    want("difficulty", "2")

    if new_after_title:
        fm = insert_after_title(fm, new_after_title)

    if not changes:
        return None, {}
    return "---\n%s\n---\n%s" % (fm, body), changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Thực sự ghi file")
    ap.add_argument("--only", help="Chỉ xử lý 1 slug (không .md)")
    ap.add_argument("--show", type=int, default=0, help="In chi tiết N thẻ đầu")
    ap.add_argument("--limit", type=int, default=0, help="Giới hạn số file xử lý")
    args = ap.parse_args()

    if not os.path.isdir(STUFF_DIR):
        print("Không thấy %s — hãy chạy từ thư mục gốc repo." % STUFF_DIR)
        sys.exit(1)

    files = sorted(f for f in os.listdir(STUFF_DIR) if f.endswith(".md"))
    if args.only:
        files = [f for f in files if f[:-3] == args.only]
    if args.limit:
        files = files[: args.limit]

    changed, shown = 0, 0
    for f in files:
        path = os.path.join(STUFF_DIR, f)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        new_text, changes = process(text)
        if not changes:
            continue
        changed += 1
        if args.write:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_text)
        if shown < args.show:
            shown += 1
            print("\n=== %s  (%s) ===" % (f, ", ".join("%s:%s" % (k, v) for k, v in changes.items())))
            print(new_text.split("\n---\n")[0] + "\n---")

    mode = "ĐÃ GHI" if args.write else "DRY-RUN (chưa ghi)"
    print("\n[%s] %d/%d thẻ sẽ được bổ sung field." % (mode, changed, len(files)))
    if not args.write and changed:
        print("→ Chạy lại với --write để áp dụng. Dùng --show 5 để xem trước chi tiết.")


if __name__ == "__main__":
    main()
