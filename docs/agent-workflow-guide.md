# Agent Workflow Guide — Content Pipeline 3 vai (Phương án B)

> Hướng dẫn thiết lập và tự động hóa sản xuất stuff cards bằng 3 agent trong VS Code Agent Sessions (Claude Code), tối ưu chi phí bằng model tiering + verifier bằng code.

**English summary:** Three-role content pipeline for VS Code agent sessions: Researcher (Haiku) gathers refs and proposes graph placement, Writer (Sonnet) drafts the card, and a deterministic code Verifier gates quality at zero token cost. Humans review via PR. Hard caps and minimal context keep each card under a few cents.

---

## 1. Kiến trúc

```
backlog.csv ──▶ [Researcher · Haiku] ──▶ research brief (YAML)
                       │                        │
              WebSearch/WebFetch          [Writer · Sonnet]
              Grep graph hiện có                │
                                        content/stuff/<slug>.md
                                                │
                                    [Verifier · verify.mjs · $0]
                                       schema ✓ links ✓ words ✓
                                                │
                                         PR ──▶ Human review ──▶ merge
```

Nguyên tắc (theo 4 layer Prompt/Context/Harness/Loop):

| Layer | Thiết lập trong repo |
|---|---|
| Prompt | `scripts/content-pipeline/prompts/*.md` — template cố định cho 2 vai |
| Context | Chỉ nạp: brief + 3–5 card liên quan. Không bao giờ nạp cả `content/` |
| Harness | `/new-card` = Gather → Act → Verify một vòng; verifier là code |
| Loop | `/batch-cards` = lặp có hard cap 10, no-progress brake, completion = verify PASS |

## 2. Thiết lập một lần

Các file đã có sẵn trong repo — VS Code Agent Sessions tự nhận:

- `.claude/agents/researcher.md` — subagent Researcher, `model: haiku`, chỉ có tools đọc + web. Xuất hiện trong tab **Agents** của panel Customizations.
- `.claude/agents/writer.md` — subagent Writer, `model: sonnet`, có quyền Write + Bash (để chạy verify).
- `.claude/commands/new-card.md` — slash command `/new-card <concept>`.
- `.claude/commands/batch-cards.md` — slash command `/batch-cards <n>`.
- `CLAUDE.md` — quy tắc chung, mọi session tự động load.

Kiểm tra: mở session mới trong folder `theunseen`, gõ `/` — thấy `new-card` và `batch-cards`; panel Agents hiển thị `researcher`, `writer`.

## 3. Vận hành

### Tạo 1 card

```
/new-card goodharts-law
```

Session chính (orchestrator) sẽ: gọi subagent researcher → nhận brief → gọi subagent writer → chạy `npm run verify` → cập nhật backlog → báo cáo. Không tự commit.

### Chạy batch

```
/batch-cards 5
```

Lấy 5 concept `todo` ưu tiên cao nhất từ `scripts/content-pipeline/backlog.csv`. Dừng sớm nếu 2 card liên tiếp fail verify (no-progress brake — tránh đốt token vào ngõ cụt).

### Enrich 181 legacy cards

Cards migrate từ Jekyll có body ngắn (verify hiện báo warning `< 100 từ`). Dùng chính pipeline này:

```
/batch-cards 5 — thay vì backlog, lấy 5 card có warning word-count từ npm run verify,
researcher bổ sung facts từ refs có sẵn, writer mở rộng body lên 300-500 từ, giữ nguyên front/back.
```

(Có thể lưu thành command riêng `.claude/commands/enrich-cards.md` khi quy trình ổn định.)

### Review & merge

1. Kết thúc mỗi batch: `git diff` xem cards mới, sửa giọng văn nếu cần.
2. `npm run verify && npm run graph` lần cuối.
3. Commit lên branch làm việc, mở PR. **Pipeline không bao giờ tự merge** — human là quality gate cuối.

## 4. Kiểm soát chi phí

| Đòn bẩy | Thiết lập | Tiết kiệm |
|---|---|---|
| Model tiering | Researcher = Haiku, Writer = Sonnet, orchestrator không tự viết | ~70% so với dùng 1 model mạnh cho cả pipeline |
| Verifier bằng code | `verify.mjs` chạy trước, LLM không bao giờ được nhờ "check schema" | ~1 lượt LLM/card |
| Context tối thiểu | Writer chỉ đọc brief + 3–5 card liên quan | Token input giảm ~10x so với nạp cả vault |
| Hard cap | `/batch-cards` tối đa 10/run | Chặn runaway loop |
| No-progress brake | 2 fail liên tiếp → dừng | Chặn retry vô hạn |

Ước tính: ~15–25k token/card → **vài cent/card**; 60 card mới < $10. Theo dõi thực tế bằng `/cost` sau mỗi batch, ghi vào cột notes của backlog nếu lệch.

## 5. Tự động hóa thêm (tùy chọn, khi pipeline đã ổn định)

- **Hook verify tự động**: thêm PostToolUse hook (panel **Hooks**) chạy `npm run verify` mỗi khi có Write/Edit vào `content/stuff/` — lỗi schema bị chặn ngay tại chỗ, không đợi đến cuối.
- **Headless batch định kỳ**: `claude -p "/batch-cards 5" --allowedTools "Read,Write,Edit,Grep,Glob,Bash(npm run verify),Bash(npm run graph)"` chạy qua cron/CI, output là branch chờ PR. Chỉ bật khi tỉ lệ pass-verify-lần-đầu ≥ 80%.
- **CI làm verifier thứ 2**: `.github/workflows/ci.yml` đã chạy verify + build trên mọi PR — không merge được card lỗi.

## 6. Definition of Done (mỗi card)

- [ ] `npm run verify` PASS, không error
- [ ] Body 300–500 từ, tự viết, không copy nguồn
- [ ] `links` ≥ 2 slug tồn tại và liên quan thật
- [ ] `refs` ≥ 1 URL đáng tin
- [ ] Human đã đọc và approve qua PR
