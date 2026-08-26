// Build public/graph/graph.json: extract nodes/edges from content/stuff frontmatter,
// compute graph metrics (degree/component/community), bake a deterministic 3D layout.
import { readdirSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import matter from 'gray-matter';
import { computeMetrics } from './lib/graph-metrics.mjs';
import { bakeLayout } from './lib/bake-layout.mjs';

const DIR = 'content/stuff';
const KEEP_GHOSTS = process.argv.includes('--keep-ghosts');

const files = readdirSync(DIR).filter((f) => f.endsWith('.md'));
const ids = new Set(files.map((f) => f.replace(/\.md$/, '')));

const rawNodes = [];
const edgeSet = new Set();
let danglingCount = 0;

for (const f of files) {
  const { data } = matter(readFileSync(`${DIR}/${f}`, 'utf8'));
  const id = f.replace(/\.md$/, '');
  if (data.published === false) continue;
  rawNodes.push({
    id,
    title: data.title,
    url: `/stuff/${id}/`,
    level: data.level ?? 2,
    categories: data.categories ?? [],
  });
  for (const link of data.links ?? []) {
    if (link === id) continue; // drop self-loop
    if (!ids.has(link)) {
      danglingCount += 1;
      if (!KEEP_GHOSTS) continue;
    }
    edgeSet.add([id, link].sort().join('|'));
  }
}

if (KEEP_GHOSTS) {
  const known = new Set(rawNodes.map((n) => n.id));
  for (const key of edgeSet) {
    for (const id of key.split('|')) {
      if (!known.has(id)) {
        known.add(id);
        rawNodes.push({ id, title: id, url: null, level: null, categories: [], ghost: true });
      }
    }
  }
}

const edges = [...edgeSet].map((e) => {
  const [source, target] = e.split('|');
  return { source, target };
});

const orphanCount = rawNodes.filter((n) => !edges.some((e) => e.source === n.id || e.target === n.id)).length;

const withMetrics = computeMetrics(rawNodes, edges);
const baked = bakeLayout(withMetrics, edges);

mkdirSync('public/graph', { recursive: true });
writeFileSync(
  'public/graph/graph.json',
  JSON.stringify({ nodes: baked, edges }),
);

console.log(
  `graph.json: ${baked.length} nodes, ${edges.length} edges, ${orphanCount} orphan, ${danglingCount} dangling`,
);
