#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# linux-build.sh — build shim cho Linux sandbox của Cowork
#
# VẤN ĐỀ
#   `node_modules/` trong repo được cài trên macOS (darwin-arm64). `device_bash`
#   của Cowork chạy trong một VM Linux (aarch64) mount repo qua ~/mnt/. Astro 7
#   dùng rolldown với native binding theo platform → trong VM nó không tìm thấy
#   binding Linux và fallback sang WASI cũng không có:
#       Cannot find module '@rolldown/binding-wasm32-wasi'
#   => `npm run build` LUÔN fail trong sandbox, và vì daily-content / illustration
#   job coi build là smoke test bắt buộc trước khi commit nên cả hai job dừng ở đó.
#
#   KHÔNG chạy `npm install` / `npm ci` thẳng trong ~/mnt/theunseen để "sửa":
#   nó ghi đè node_modules của máy thật bằng binary Linux và làm hỏng dev trên macOS.
#
# CÁCH XỬ LÝ
#   Dựng một workspace riêng trong scratch của VM ($HOME, NGOÀI ~/mnt/, macOS không
#   nhìn thấy) với node_modules Linux đúng platform, rồi build ở đó. Repo thật chỉ
#   được đọc, không bị đụng vào.
#
# DÙNG
#   bash scripts/linux-build.sh setup    # cài node_modules Linux (nền, ~2-5 phút)
#   bash scripts/linux-build.sh status   # tiến độ setup/build
#   bash scripts/linux-build.sh build    # sync source + npm run build (nền)
#   bash scripts/linux-build.sh log      # 60 dòng log cuối
#   bash scripts/linux-build.sh clean    # xoá workspace
#
#   Mỗi lệnh trả về ngay (job chạy nền) vì device_bash có giới hạn ~180s/lần.
#   Poll bằng `status` cho tới khi thấy DONE hoặc FAILED.
#
# PHẠM VI
#   Chỉ dành cho `npm run build`. `verify`, `graph`, `mapdata`, `backlog` là JS
#   thuần (chỉ cần gray-matter/graphology) nên chạy thẳng trong repo được — đã
#   xác nhận PASS trong VM.
# ---------------------------------------------------------------------------
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${TU_LINUX_WORK:-$HOME/.tu-linux-build}"
LOG="$WORK/last.log"
STATE="$WORK/state"

if [ "$(uname -s)" != "Linux" ]; then
  echo "Script này chỉ dùng trong VM Linux của Cowork."
  echo "Trên macOS chạy 'npm run build' bình thường."
  exit 1
fi

mark() { mkdir -p "$WORK"; printf '%s %s\n' "$(date -u +%FT%TZ)" "$1" > "$STATE"; }

sync_src() {
  mkdir -p "$WORK"
  tar -C "$REPO" -cf - \
      --exclude='./node_modules*' \
      --exclude='./.git' \
      --exclude='./dist*' \
      --exclude='./.astro*' \
      --exclude='./.unlink-trash-tmp' \
      --exclude='*.log' \
      . | tar -C "$WORK" -xf -
}

cmd_setup() {
  mkdir -p "$WORK"
  sync_src
  mark "SETUP_RUNNING"
  nohup bash -c "
    cd '$WORK'
    node --version
    npm ci --no-audit --no-fund
  " > "$LOG" 2>&1 &
  disown || true
  # đánh dấu kết quả khi tiến trình nền kết thúc
  nohup bash -c "
    while pgrep -f 'npm ci --no-audit' >/dev/null 2>&1; do sleep 5; done
    if [ -d '$WORK/node_modules/astro' ]; then
      printf '%s SETUP_DONE\n' \"\$(date -u +%FT%TZ)\" > '$STATE'
    else
      printf '%s SETUP_FAILED\n' \"\$(date -u +%FT%TZ)\" > '$STATE'
    fi
  " >/dev/null 2>&1 &
  disown || true
  echo "setup đã chạy nền. Workspace: $WORK"
  echo "Poll: bash scripts/linux-build.sh status"
}

cmd_build() {
  if [ ! -d "$WORK/node_modules/astro" ]; then
    echo "Chưa có node_modules Linux. Chạy 'setup' trước."
    exit 1
  fi
  # giữ lại node_modules, chỉ sync source
  sync_src
  mark "BUILD_RUNNING"
  nohup bash -c "
    cd '$WORK'
    if npm run build; then
      printf '%s BUILD_DONE\n' \"\$(date -u +%FT%TZ)\" > '$STATE'
    else
      printf '%s BUILD_FAILED\n' \"\$(date -u +%FT%TZ)\" > '$STATE'
    fi
  " > "$LOG" 2>&1 &
  disown || true
  echo "build đã chạy nền. Poll: bash scripts/linux-build.sh status"
}

cmd_status() {
  [ -f "$STATE" ] && cat "$STATE" || echo "chưa chạy lần nào"
  [ -f "$LOG" ] && { echo "--- 15 dòng log cuối ---"; tail -15 "$LOG"; }
}

cmd_log() { [ -f "$LOG" ] && tail -60 "$LOG" || echo "chưa có log"; }

cmd_clean() { rm -rf "$WORK"; echo "đã xoá $WORK"; }

case "${1:-}" in
  setup)  cmd_setup ;;
  build)  cmd_build ;;
  status) cmd_status ;;
  log)    cmd_log ;;
  clean)  cmd_clean ;;
  *) sed -n '2,40p' "${BASH_SOURCE[0]}"; exit 1 ;;
esac
