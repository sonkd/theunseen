import fs from 'fs/promises'
import path from 'path'
import matter from 'gray-matter'
import { buildZigzagPath, pointAtX, gridSnap, CELL, STEP_COLS, ZONES, ROWS_TOTAL, REF_W, REF_H } from '../src/lib/map/path.ts'
import { iconFor } from '../src/lib/icons.ts'
import { MAPS } from '../src/lib/map/palette.ts'

const CONTENT_DIR = path.resolve('./content/stuff')
const OUTPUT_FILE = path.resolve('./public/map-data.json')

const GRID_TOP = 1
const GRID_BOTTOM = ROWS_TOTAL - 1

function titleCase(value) {
  return value.charAt(0) + value.slice(1).toLowerCase()
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

// Bề rộng zone mặc định (docs/map-layout-spec.md mục 1) — nới ra nếu zone bận
// nhất trong map cần nhiều slot cột hơn mức này (mục 3: "tăng zoneWidth").
function computeMapLayout(level, zoneGroups) {
  const maxCount = Math.max(1, ...zoneGroups.map((g) => g.length))
  const neededWidthPx = (maxCount + 1) * STEP_COLS * CELL
  const baseZoneWidthPx = REF_W / ZONES
  const zoneWidthPx = Math.max(baseZoneWidthPx, neededWidthPx)
  const worldW = zoneWidthPx * ZONES
  const path2d = buildZigzagPath(level, worldW, REF_H)
  return { zoneWidthPx, worldW, path: path2d }
}

// Đặt stuff trong 1 zone theo lưới: slot cột đều STEP_COLS, xen kẽ trên/dưới
// đường đi, collision-free, snap về tâm ô lưới (docs/map-layout-spec.md mục 3).
function placeZoneStuff(zone, group, zoneWidthPx, path2d) {
  const zoneStartCol = Math.round((zone * zoneWidthPx) / CELL)
  const occupied = new Set()
  const placements = []
  let slotIndex = 1

  group.forEach((item, i) => {
    if (item.map_position) {
      const snapped = gridSnap(Number(item.map_position.x) * CELL || 0, Number(item.map_position.y) * CELL || 0)
      const col = Math.round(snapped.x / CELL)
      const row = Math.round(snapped.y / CELL)
      occupied.add(`${col}:${row}`)
      placements.push({ item, col, row, x: snapped.x, y: snapped.y })
      return
    }

    let offset = i % 2 === 0 ? -1 : 1
    if (i % 4 === 0) offset = -2

    let col = 0
    let row = 0
    for (;;) {
      const localCol = slotIndex * STEP_COLS
      const globalCol = zoneStartCol + localCol
      const x = globalCol * CELL
      const trueY = pointAtX(path2d, x).y
      const pathRow = Math.round(trueY / CELL)
      // Đảm bảo |row*CELL - trueY| <= 2*CELL thật sự (không chỉ so với pathRow
      // đã làm tròn) — thu hẹp offset dần về 0 nếu path cong khiến lệch quá.
      let appliedOffset = offset
      while (appliedOffset !== 0 && Math.abs((pathRow + appliedOffset) * CELL - trueY) > 2 * CELL) {
        appliedOffset += appliedOffset > 0 ? -1 : 1
      }
      const candidateRow = Math.max(GRID_TOP, Math.min(GRID_BOTTOM, pathRow + appliedOffset))
      const key = `${globalCol}:${candidateRow}`
      slotIndex += 1
      if (occupied.has(key)) continue
      occupied.add(key)
      col = globalCol
      row = candidateRow
      break
    }
    placements.push({ item, col, row, x: col * CELL, y: row * CELL })
  })

  return placements
}

function columnGapStats(placements) {
  const cols = placements.map((p) => p.col).sort((a, b) => a - b)
  const gaps = []
  for (let i = 1; i < cols.length; i += 1) gaps.push(cols[i] - cols[i - 1])
  return gaps
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

  const report = []
  let globalMinGap = Infinity
  let globalMaxGap = -Infinity

  // 5 maps theo docs/design-spec.md: content level 1-4 -> map index 0-3;
  // map index 4 (KNOWLEDGE · EPISTEME) là màn kết, không chứa stuff.
  const maps = MAPS.map((palette, index) => {
    const level = index + 1
    const zoneGroups = [[], [], []]
    if (level <= 4) {
      levelGroups[level].forEach((item, i) => zoneGroups[i % 3].push(item))
    }

    const { zoneWidthPx, worldW, path: mapPath } = computeMapLayout(level, zoneGroups)
    const zoneCounts = []
    const allGaps = []

    const stuff = zoneGroups.flatMap((group, zone) => {
      const placements = placeZoneStuff(zone, group, zoneWidthPx, mapPath)
      zoneCounts.push(placements.length)
      allGaps.push(...columnGapStats(placements))

      return placements.map(({ item, col, x, y }) => ({
        slug: item.slug,
        title: item.title,
        icon: item.icon,
        zone,
        col,
        x: x / worldW,
        y: y / REF_H,
      }))
    })

    const minGap = allGaps.length ? Math.min(...allGaps) : null
    const maxGap = allGaps.length ? Math.max(...allGaps) : null
    if (minGap != null) globalMinGap = Math.min(globalMinGap, minGap)
    if (maxGap != null) globalMaxGap = Math.max(globalMaxGap, maxGap)

    report.push({
      level,
      name: titleCase(palette.name),
      total: stuff.length,
      zoneCounts,
      minGap,
      maxGap,
    })

    return {
      level,
      name: titleCase(palette.name),
      greek: titleCase(palette.sub),
      vn: palette.vn,
      zones: 3,
      stuff: stuff.map(({ col, ...rest }) => rest), // col chỉ dùng nội bộ để đo khoảng cách
    }
  })

  const output = { maps }

  await fs.mkdir(path.dirname(OUTPUT_FILE), { recursive: true })
  await fs.writeFile(OUTPUT_FILE, JSON.stringify(output, null, 2), 'utf-8')

  const total = maps.reduce((sum, m) => sum + m.stuff.length, 0)
  console.log(`Wrote ${total} stuff entries across ${maps.length} maps to ${OUTPUT_FILE}`)
  console.log('')
  console.log('Map layout report (docs/map-layout-spec.md):')
  for (const row of report) {
    console.log(
      `  Map ${row.level} ${row.name}: ${row.total} stuff — zones [${row.zoneCounts.join(', ')}] — ` +
        `col gap min=${row.minGap ?? 'n/a'} max=${row.maxGap ?? 'n/a'} (STEP_COLS=${STEP_COLS})`,
    )
  }
  console.log(
    `  Global col gap: min=${Number.isFinite(globalMinGap) ? globalMinGap : 'n/a'} max=${Number.isFinite(globalMaxGap) ? globalMaxGap : 'n/a'}`,
  )
}

buildMapData().catch((error) => {
  console.error(error)
  process.exit(1)
})
