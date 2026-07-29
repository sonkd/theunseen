// Đồng bộ backlog.csv với thực tế content/stuff/ — idempotent, chạy được nhiều lần.
// Cột: concept,priority,status,notes
//   status: todo (chưa có file) | needs-enrich (có file, body < 300 từ) | done (đủ chuẩn)
// Giữ nguyên các dòng todo do người thêm tay; chỉ cập nhật status/notes của card đã tồn tại.
import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs'
import matter from 'gray-matter'

const DIR = 'content/stuff'
const CSV = 'scripts/content-pipeline/backlog.csv'
const TARGET_WORDS = 300

const files = readdirSync(DIR).filter((f) => f.endsWith('.md'))
const stats = new Map()
for (const f of files) {
  const slug = f.replace(/\.md$/, '')
  const parsed = matter(readFileSync(`${DIR}/${f}`, 'utf8'))
  const words = parsed.content.trim().split(/\s+/).filter(Boolean).length
  const links = (parsed.data.links ?? []).length
  const refs = (parsed.data.refs ?? []).length
  stats.set(slug, { words, links, refs, level: parsed.data.level ?? 2 })
}

// đọc backlog cũ để giữ dòng todo thủ công + priority
const previous = new Map()
if (existsSync(CSV)) {
  const lines = readFileSync(CSV, 'utf8').trim().split('\n').slice(1)
  for (const line of lines) {
    const m = line.match(/^([^,]+),([^,]*),([^,]*),"?(.*?)"?$/)
    if (m) previous.set(m[1], { priority: m[2], status: m[3], notes: m[4] })
  }
}

const rows = []

// 1) card đã tồn tại
for (const [slug, s] of [...stats].sort((a, b) => a[0].localeCompare(b[0]))) {
  const needsEnrich = s.words < TARGET_WORDS
  const status = needsEnrich ? 'needs-enrich' : 'done'
  // ưu tiên: card ít chữ + nhiều links (hub node) làm trước
  const priority = !needsEnrich ? 5 : s.links >= 2 ? 1 : s.words < 100 ? 2 : 3
  rows.push({
    concept: slug,
    priority,
    status,
    notes: `L${s.level} · ${s.words}w · ${s.links} links · ${s.refs} refs`,
  })
}

// 2) concept chưa có file (giữ nguyên dòng cũ, status todo)
for (const [concept, p] of previous) {
  if (stats.has(concept)) continue
  rows.push({ concept, priority: p.priority || 3, status: 'todo', notes: p.notes || '' })
}

rows.sort((a, b) => a.priority - b.priority || a.concept.localeCompare(b.concept))
const out = ['concept,priority,status,notes', ...rows.map((r) => `${r.concept},${r.priority},${r.status},"${r.notes}"`)].join('\n')
writeFileSync(CSV, out + '\n')

const count = (s) => rows.filter((r) => r.status === s).length
console.log(`backlog.csv synced: ${rows.length} rows — todo ${count('todo')} · needs-enrich ${count('needs-enrich')} · done ${count('done')}`)
