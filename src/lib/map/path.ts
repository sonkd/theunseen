// Đường đi mòn (Catmull-Rom qua khung zig-zag) + grid placement.
// Xem docs/map-layout-spec.md (lưới, đặt stuff) và docs/ui-qa-round2.md R2-2
// (path phải cong/gấp khúc tự nhiên, không phải chevron cơ học lặp lại).

export type PathVertex = { x: number; y: number; dist: number }
export type ZigzagPath = {
  vertices: PathVertex[]
  length: number
  segWidth: number
  zoneCenters: number[]
}

export function hashString(value: string): number {
  let hash = 0
  for (let i = 0; i < value.length; i += 1) {
    hash = (Math.imul(31, hash) + value.charCodeAt(i)) | 0
  }
  return hash >>> 0
}

export function mulberry32(seed: number) {
  let t = seed >>> 0
  return () => {
    t += 0x6d2b79f5
    let r = Math.imul(t ^ (t >>> 15), 1 | t)
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r)
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296
  }
}

export function withSeed(level: number, salt: string) {
  return mulberry32(hashString(`${level}-${salt}`) || 1)
}

function clampInt(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, value))
}

// --- Lưới thiết kế (docs/map-layout-spec.md mục 1) ---
// CELL luôn có nghĩa "64px tại khung tham chiếu REF_W×REF_H". Mọi hàm ở đây
// nhận W,H tuỳ ý (1×1 khi build-map-data cần toạ độ chuẩn hoá 0..1, hoặc kích
// thước canvas thật khi MapCanvas render) — tỉ lệ x/W, y/H luôn bất biến với
// W,H truyền vào nên build-time và render-time luôn cho cùng một hình dạng.
export const CELL = 64
export const REF_W = 1600
export const REF_H = 704
export const ZONES = 3
const CYCLES_PER_ZONE = 1
const SEGMENTS = ZONES * CYCLES_PER_ZONE * 2 // 6 đoạn khung / 7 control point
export const STEP_COLS = 3
export const ROWS_TOTAL = Math.round(REF_H / CELL) // dùng làm biên clamp hàng khi đặt stuff

const SAMPLES_PER_MAP = 240 // docs/ui-qa-round2.md R2-2: sample dày để spline mượt
const MAX_SLOPE_DEG = 35
const MICRO_NOISE_PX = 8 // ở khung tham chiếu REF_H — mép gợn nhẹ, không "vẽ máy"
const BASE_AMPLITUDE_CELL = 2.75 // ~2.5–3×CELL đỉnh<->đáy (mục 3, R2-2 giảm biên độ)

type ControlPoint = { x: number; y: number }

function catmullRom(p0: ControlPoint, p1: ControlPoint, p2: ControlPoint, p3: ControlPoint, t: number): ControlPoint {
  const t2 = t * t
  const t3 = t2 * t
  const x = 0.5 * (2 * p1.x + (-p0.x + p2.x) * t + (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 + (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3)
  const y = 0.5 * (2 * p1.y + (-p0.y + p2.y) * t + (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 + (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3)
  return { x, y }
}

/**
 * Khung control point zig-zag cho map `level`: đỉnh/đáy xen kẽ, nhưng mỗi
 * điểm được seed riêng — biên độ 60–100% biên độ gốc, x lệch ±15% so với
 * chia đều — để 3 "chu kỳ" trong 1 map không lặp lại y hệt nhau (R2-2).
 * Độ dốc giữa 2 control point liên tiếp bị giới hạn ~35°, vượt thì nới x.
 */
function buildControlPoints(level: number, W: number, H: number): ControlPoint[] {
  const cellY = (CELL / REF_H) * H
  const segWidth = W / SEGMENTS
  const centerY = H / 2
  const baseHalfAmp = (BASE_AMPLITUDE_CELL * cellY) / 2

  const ampRng = withSeed(level, 'amp')
  const xRng = withSeed(level, 'xoffset')

  const controls: ControlPoint[] = []
  for (let i = 0; i <= SEGMENTS; i += 1) {
    const idealX = i * segWidth
    const xJitter = i > 0 && i < SEGMENTS ? (xRng() - 0.5) * 2 * 0.15 * segWidth : 0
    const ampFactor = 0.6 + ampRng() * 0.4 // 60–100% biên độ gốc mỗi chu kỳ
    const half = baseHalfAmp * ampFactor
    const y = i % 2 === 0 ? centerY + half : centerY - half // chẵn = đáy, lẻ = đỉnh
    controls.push({ x: idealX + xJitter, y })
  }

  const maxSlopeRad = (MAX_SLOPE_DEG * Math.PI) / 180
  for (let i = 1; i < controls.length; i += 1) {
    const a = controls[i - 1]
    const b = controls[i]
    const dy = Math.abs(b.y - a.y)
    const dx = b.x - a.x
    const minDx = dy / Math.tan(maxSlopeRad)
    if (dx < minDx) {
      const shift = minDx - dx
      for (let k = i; k < controls.length; k += 1) controls[k].x += shift
    }
  }

  // Rescale x để điểm cuối luôn đúng W (giữ zoneWidth/placement bất biến dù đã nới độ dốc).
  const span = controls[controls.length - 1].x - controls[0].x
  const scaleX = span > 0 ? W / span : 1
  const originX = controls[0].x
  controls.forEach((c) => {
    c.x = (c.x - originX) * scaleX
  })

  return controls
}

/**
 * Đường đi mòn cho map `level`, trải trên chiều rộng W và cao H (đơn vị bất
 * kỳ — fraction 0..1 hoặc pixel thật). Catmull-Rom qua khung zig-zag ở trên,
 * sample dày (≥240 điểm/map) rồi rắc thêm nhiễu tần số cao nhỏ (±8px ở khung
 * tham chiếu) để mép đường hơi gợn tự nhiên, không như polyline máy móc.
 */
export function buildZigzagPath(level: number, W: number, H: number): ZigzagPath {
  const controls = buildControlPoints(level, W, H)
  const extended = [controls[0], ...controls, controls[controls.length - 1]]
  const samplesPerSeg = Math.max(4, Math.round(Math.max(SAMPLES_PER_MAP, controls.length * 40) / SEGMENTS))

  const raw: ControlPoint[] = []
  for (let seg = 0; seg < SEGMENTS; seg += 1) {
    const p0 = extended[seg]
    const p1 = extended[seg + 1]
    const p2 = extended[seg + 2]
    const p3 = extended[seg + 3]
    const steps = seg === SEGMENTS - 1 ? samplesPerSeg + 1 : samplesPerSeg
    for (let s = 0; s < steps; s += 1) {
      raw.push(catmullRom(p0, p1, p2, p3, s / samplesPerSeg))
    }
  }

  const noiseRng = withSeed(level, 'microjitter')
  const noiseAmp = (MICRO_NOISE_PX / REF_H) * H
  raw.forEach((p) => {
    p.y += (noiseRng() - 0.5) * 2 * noiseAmp
  })

  const vertices: PathVertex[] = []
  let total = 0
  raw.forEach((v, i) => {
    if (i > 0) total += Math.hypot(v.x - raw[i - 1].x, v.y - raw[i - 1].y)
    vertices.push({ x: v.x, y: v.y, dist: total })
  })

  const zoneWidth = W / ZONES
  const zoneCenters = [0, 1, 2].map((zone) => distanceAtX(vertices, zoneWidth * (zone + 0.5)))

  return { vertices, length: total, segWidth: W / SEGMENTS, zoneCenters }
}

function segmentAtX(vertices: PathVertex[], x: number) {
  for (let i = 1; i < vertices.length; i += 1) {
    if (x <= vertices[i].x || i === vertices.length - 1) return { a: vertices[i - 1], b: vertices[i] }
  }
  return { a: vertices[0], b: vertices[1] }
}

function distanceAtX(vertices: PathVertex[], x: number) {
  const { a, b } = segmentAtX(vertices, x)
  const t = (x - a.x) / Math.max(1e-6, b.x - a.x)
  return a.dist + (b.dist - a.dist) * t
}

/** Điểm {x,y} trên path tại hoành độ x (cùng đơn vị với path.vertices). */
export function pointAtX(path: ZigzagPath, x: number) {
  const { a, b } = segmentAtX(path.vertices, x)
  const t = (x - a.x) / Math.max(1e-6, b.x - a.x)
  return { x, y: a.y + (b.y - a.y) * t }
}

/** Điểm {x,y} trên path tại quãng đường đã đi (arc-length) `distance`. */
export function pointAtDistance(path: ZigzagPath, distance: number) {
  const vertices = path.vertices
  if (!vertices.length) return { x: 0, y: 0 }
  const clamped = clampInt(distance, 0, path.length)
  let index = vertices.findIndex((v) => v.dist >= clamped)
  if (index === -1) index = vertices.length - 1
  if (index === 0) return { x: vertices[0].x, y: vertices[0].y }
  const prev = vertices[index - 1]
  const current = vertices[index]
  const t = (clamped - prev.dist) / Math.max(1e-6, current.dist - prev.dist)
  return {
    x: prev.x + (current.x - prev.x) * t,
    y: prev.y + (current.y - prev.y) * t,
  }
}

/** Góc nghiêng (radian) của đoạn path tại quãng đường đã đi `distance`. */
export function angleAtDistance(path: ZigzagPath, distance: number) {
  const vertices = path.vertices
  if (vertices.length < 2) return 0
  const clamped = clampInt(distance, 0, path.length)
  let index = vertices.findIndex((v) => v.dist >= clamped)
  if (index <= 0) index = 1
  if (index >= vertices.length) index = vertices.length - 1
  const a = vertices[index - 1]
  const b = vertices[index]
  return Math.atan2(b.y - a.y, b.x - a.x)
}

/**
 * Convenience: y (pixel tham chiếu REF_W×REF_H) của path map `level` tại
 * hoành độ x (cũng trong hệ tham chiếu đó). `build-map-data.mjs` dùng
 * buildZigzagPath trực tiếp với world width động khi 1 zone cần nhiều cột
 * hơn REF_W cung cấp — tỉ lệ x/W, y/H bất biến nên vẫn cùng hình dạng.
 */
export function pathYAt(level: number, x: number): number {
  const path = buildZigzagPath(level, REF_W, REF_H)
  const clampedX = clampInt(x, 0, REF_W)
  return pointAtX(path, clampedX).y
}

/** Snap toạ độ (pixel tham chiếu) về giao điểm lưới CELL gần nhất. */
export function gridSnap(x: number, y: number): { x: number; y: number } {
  return { x: Math.round(x / CELL) * CELL, y: Math.round(y / CELL) * CELL }
}
