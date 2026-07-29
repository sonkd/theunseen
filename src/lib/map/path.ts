export type PathSample = { x: number; y: number; dist: number }
export type PathResult = { samples: PathSample[]; length: number; zoneCenters: number[] }

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

/**
 * Seeded, deterministic corridor path for a map level. Same (level, width, height)
 * always yields the same samples — used identically by the render engine (real
 * viewport px) and by build-map-data (width=1, height=1 normalized) so stuff
 * placement always lines up with the rendered path.
 */
export function buildPath(level: number, width: number, height: number): PathResult {
  const rng = withSeed(level, 'path')
  const anchors = [0, 1, 2, 3, 4].map((i) => {
    const x = (width / 4) * i
    const y = height * (0.28 + rng() * 0.24 + (i % 2 ? 0.03 : 0))
    return { x, y }
  })

  const samples: PathSample[] = []
  let total = 0
  const sampleStep = Math.max(width / 240, 1e-6)
  let previous = { x: anchors[0].x, y: anchors[0].y }

  for (let px = 0; px <= width; px += sampleStep) {
    const t = width === 0 ? 0 : px / width
    const segment = Math.min(3, Math.floor(t * 4))
    const localT = t * 4 - segment
    const a = anchors[segment]
    const b = anchors[segment + 1]
    const baseY = a.y + (b.y - a.y) * localT
    const curve = Math.sin(localT * Math.PI) * height * 0.06 * (1 + 0.2 * (segment % 2))
    const y = baseY + curve * (segment % 2 === 0 ? 1 : -1)
    const dx = px - previous.x
    const dy = y - previous.y
    total += Math.sqrt(dx * dx + dy * dy)
    samples.push({ x: px, y, dist: total })
    previous = { x: px, y }
  }

  const zoneCenters = [0, 1, 2].map((zone) => {
    const targetX = (width * (zone * 2 + 1)) / 6
    const nearest = samples.reduce(
      (best, sample) => {
        const delta = Math.abs(sample.x - targetX)
        return delta < best.delta ? { sample, delta } : best
      },
      { sample: samples[0], delta: Infinity },
    )
    return nearest.sample.dist
  })

  return { samples, length: total, zoneCenters }
}

/**
 * Deterministic corridor position (normalized 0..1) for a stuff card: nearest
 * path sample for its zone, offset by a seeded amount within the corridor.
 */
export function corridorPosition(level: number, slug: string, zone: 0 | 1 | 2) {
  const { samples } = buildPath(level, 1, 1)
  const targetX = (zone * 2 + 1) / 6
  const nearest = samples.reduce(
    (best, sample) => {
      const delta = Math.abs(sample.x - targetX)
      return delta < best.delta ? { sample, delta } : best
    },
    { sample: samples[0], delta: Infinity },
  )

  const rng = withSeed(level, `stuff-${slug}`)
  const corridorWidth = 0.08 // ~ tương đương hành lang ±250px trên khung hình chuẩn
  const offsetX = (rng() - 0.5) * 2 * corridorWidth
  const offsetY = (rng() - 0.5) * 2 * corridorWidth

  return {
    x: Math.min(1, Math.max(0, nearest.sample.x + offsetX)),
    y: Math.min(1, Math.max(0, nearest.sample.y + offsetY)),
  }
}
