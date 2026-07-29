// Build public/graph.json from content/stuff frontmatter (nodes + edges).
import { readdirSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import matter from 'gray-matter';

const DIR = 'content/stuff';
const files = readdirSync(DIR).filter((f) => f.endsWith('.md'));
const nodes = [];
const edges = new Set();
const ids = new Set(files.map((f) => f.replace(/\.md$/, '')));

for (const f of files) {
  const { data } = matter(readFileSync(`${DIR}/${f}`, 'utf8'));
  const id = f.replace(/\.md$/, '');
  if (data.published === false) continue;
  nodes.push({ id, title: data.title, level: data.level ?? 2, categories: data.categories ?? [] });
  for (const l of data.links ?? []) {
    if (!ids.has(l)) continue;
    edges.add([id, l].sort().join('|'));
  }
}
mkdirSync('public', { recursive: true });
writeFileSync('public/graph.json', JSON.stringify({
  nodes,
  edges: [...edges].map((e) => { const [a, b] = e.split('|'); return { source: a, target: b }; }),
}, null, 2));
console.log(`graph.json: ${nodes.length} nodes, ${edges.size} edges`);
