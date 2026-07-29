// Deterministic verifier — chạy TRƯỚC mọi LLM judge (tối ưu chi phí: máy check được thì không đốt token).
// Fail (exit 1): schema sai, link gãy, level ngoài 1-4, front/back thiếu.
// Warn: body < 100 từ (mục tiêu 300-500), thiếu refs, thiếu categories.
import { readdirSync, readFileSync } from 'node:fs';
import matter from 'gray-matter';

const DIR = 'content/stuff';
const files = readdirSync(DIR).filter((f) => f.endsWith('.md'));
const ids = new Set(files.map((f) => f.replace(/\.md$/, '')));
const errors = [];
const warns = [];

for (const f of files) {
  const id = f.replace(/\.md$/, '');
  let parsed;
  try { parsed = matter(readFileSync(`${DIR}/${f}`, 'utf8')); }
  catch (e) { errors.push(`${id}: YAML không parse được — ${e.message}`); continue; }
  const d = parsed.data;

  for (const k of ['title', 'front', 'back']) {
    if (!d[k] || String(d[k]).trim() === '') errors.push(`${id}: thiếu trường bắt buộc "${k}"`);
  }
  const lvl = d.level ?? 2;
  if (!Number.isInteger(lvl) || lvl < 1 || lvl > 4) errors.push(`${id}: level=${JSON.stringify(d.level)} — phải là số nguyên 1-4`);
  for (const l of d.links ?? []) {
    if (!ids.has(l)) errors.push(`${id}: link gãy → "${l}" không tồn tại trong content/stuff/`);
  }
  for (const r of d.refs ?? []) {
    if (!/^https?:\/\//.test(r)) errors.push(`${id}: ref không phải URL — "${r}"`);
  }
  const words = parsed.content.trim().split(/\s+/).filter(Boolean).length;
  if (words < 100) warns.push(`${id}: body ${words} từ (mục tiêu 300-500)`);
  if (!(d.refs ?? []).length) warns.push(`${id}: chưa có refs`);
  if (!(d.categories ?? []).length) warns.push(`${id}: chưa có categories`);
}

console.log(`Checked ${files.length} cards.`);
if (warns.length) console.log(`\n⚠ ${warns.length} warnings:\n` + warns.slice(0, 40).map((w) => '  - ' + w).join('\n') + (warns.length > 40 ? `\n  ... +${warns.length - 40} more` : ''));
if (errors.length) {
  console.error(`\n✗ ${errors.length} errors:\n` + errors.map((e) => '  - ' + e).join('\n'));
  process.exit(1);
}
console.log('\n✓ Schema + link integrity PASS');
