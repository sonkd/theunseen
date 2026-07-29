import fs from 'fs/promises'
import path from 'path'
import matter from 'gray-matter'
import { corridorPosition } from '../src/lib/map/path.ts'
import { iconFor } from '../src/lib/icons.ts'

const CONTENT_DIR = path.resolve('./content/stuff')
const OUTPUT_FILE = path.resolve('./public/map-data.json')

const MAP_META = {
  1: { name: 'Eikasia · Imagining' },
  2: { name: 'Pistis · Belief' },
  3: { name: 'Dianoia · Thinking' },
  4: { name: 'Noesis · Intelligence/Knowledge' },
}

async function collectFiles(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true })
  const files = []
  for (const entry of entries) {
    const resolved = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      files.push(...(await collectFiles(resolved)))
    } else if (entry.isFile() && resolved.endsWith('.md')) {
      files.push(resolved)
    }
  }
  return files
}

function normalizeLevel(raw) {
  const level = Number(raw)
  if (!Number.isFinite(level) || level < 1) return 1
  if (level > 4) return 4
  return Math.floor(level)
}

async function buildMapData() {
  const files = await collectFiles(CONTENT_DIR)
  const published = []

  for (const file of files) {
    const raw = await fs.readFile(file, 'utf-8')
    const { data } = matter(raw)
    if (data.published === false) continue

    const slug = path.basename(file, '.md')
    const level = normalizeLevel(data.level)
    const categories = Array.isArray(data.categories) ? data.categories : []

    published.push({
      slug,
      title: data.title || slug,
      icon: iconFor(slug, categories, data.icon),
      level,
      map_position: data.map_position && typeof data.map_position === 'object' ? data.map_position : null,
    })
  }

  published.sort((a, b) => a.level - b.level || a.slug.localeCompare(b.slug))

  const levelGroups = { 1: [], 2: [], 3: [], 4: [] }
  for (const item of published) {
    levelGroups[item.level].push(item)
  }

  const maps = [1, 2, 3, 4].map((level) => {
    const stuff = levelGroups[level].map((item, index) => {
      const zone = index % 3
      const position = item.map_position
        ? { x: Number(item.map_position.x) || 0, y: Number(item.map_position.y) || 0 }
        : corridorPosition(level, item.slug, zone)

      return {
        slug: item.slug,
        title: item.title,
        icon: item.icon,
        zone,
        x: position.x,
        y: position.y,
      }
    })

    return {
      level,
      name: MAP_META[level].name.split(' · ')[1],
      greek: MAP_META[level].name.split(' · ')[0],
      zones: 3,
      stuff,
    }
  })

  const output = { maps }

  await fs.mkdir(path.dirname(OUTPUT_FILE), { recursive: true })
  await fs.writeFile(OUTPUT_FILE, JSON.stringify(output, null, 2), 'utf-8')
  const total = maps.reduce((sum, m) => sum + m.stuff.length, 0)
  console.log(`Wrote ${total} stuff entries across ${maps.length} maps to ${OUTPUT_FILE}`)
}

buildMapData().catch((error) => {
  console.error(error)
  process.exit(1)
})
