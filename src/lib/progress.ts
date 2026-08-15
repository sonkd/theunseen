export type ProgressStorage = {
  explored: string[]
}

export type MapDataForProgress = {
  maps: { level: number; stuff: { slug: string }[] }[]
}

const STORAGE_KEY = 'unseen:lit'

function getStoredSlugs(): string[] {
  if (typeof window === 'undefined' || !window.localStorage) {
    return []
  }

  const next = window.localStorage.getItem(STORAGE_KEY)
  if (!next) {
    return []
  }

  try {
    const parsed = JSON.parse(next)
    if (!Array.isArray(parsed)) {
      return []
    }

    return parsed.filter((item) => typeof item === 'string')
  } catch {
    return []
  }
}

function saveSlugs(slugs: string[]) {
  if (typeof window === 'undefined' || !window.localStorage) {
    return
  }

  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(slugs))
}

export function getExploredSlugs(): string[] {
  return getStoredSlugs()
}

export function getLit(): string[] {
  return getStoredSlugs()
}

export function isLit(slug: string): boolean {
  if (!slug || typeof slug !== 'string') {
    return false
  }
  return getStoredSlugs().includes(slug.trim())
}

export function markLit(slug: string) {
  if (!slug || typeof slug !== 'string') {
    return
  }

  const normalizedSlug = slug.trim()
  if (normalizedSlug.length === 0) {
    return
  }

  const slugs = getStoredSlugs()
  if (!slugs.includes(normalizedSlug)) {
    saveSlugs([...slugs, normalizedSlug])
  }
}

export function resetExplored() {
  saveSlugs([])
}

let cachedMapData: MapDataForProgress | null = null

export function primeMapData(data: MapDataForProgress) {
  cachedMapData = data
}

export function litCountByLevel(): Record<number, number> {
  const lit = new Set(getStoredSlugs())
  const counts: Record<number, number> = {}
  if (!cachedMapData) {
    return counts
  }

  for (const map of cachedMapData.maps) {
    counts[map.level] = map.stuff.filter((s) => lit.has(s.slug)).length
  }

  return counts
}

export function getExploredPct(level: number, total: number): number {
  if (typeof level !== 'number' || typeof total !== 'number' || total <= 0) {
    return 0
  }

  const clamped = Math.min(Math.max(level, 0), total)
  return Math.round((clamped / total) * 100)
}

let hasSetupOpenListener = false

function getSlugFromEvent(event: Event | CustomEvent): string | null {
  const anyEvent = event as any
  const detail = anyEvent.detail
  if (detail == null) {
    return null
  }

  if (typeof detail === 'string') {
    return detail
  }

  if (typeof detail === 'object' && detail !== null) {
    if (typeof detail.slug === 'string') {
      return detail.slug
    }
    if (typeof detail.id === 'string') {
      return detail.id
    }
  }

  return null
}

function setupStuffOpenListener() {
  if (hasSetupOpenListener) {
    return
  }

  if (typeof globalThis === 'undefined' || typeof (globalThis as any).addEventListener !== 'function') {
    return
  }

  hasSetupOpenListener = true
  ;(globalThis as any).addEventListener('stuff:open', (event: Event) => {
    const slug = getSlugFromEvent(event)
    if (slug) {
      markLit(slug)
    }
  })
}

setupStuffOpenListener()
