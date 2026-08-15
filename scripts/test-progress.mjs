import { strict as assert } from 'assert'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const progressPath = join(__dirname, '../src/lib/progress.ts')

const mockStorage = new Map()

globalThis.window = {
  localStorage: {
    getItem(key) {
      return mockStorage.get(key) ?? null
    },
    setItem(key, value) {
      mockStorage.set(key, String(value))
    },
  },
}

globalThis.document = {
  addEventListener() {},
}

globalThis.addEventListener = () => {}

const { getLit, isLit, markLit, resetExplored, getExploredPct, litCountByLevel, primeMapData } =
  await import(progressPath)

resetExplored()
assert.deepEqual(getLit(), [], 'Initial storage should be empty')
markLit('map-1')
markLit('map-2')
markLit('map-1')
assert.deepEqual(getLit(), ['map-1', 'map-2'], 'Should dedupe slugs')
assert.equal(isLit('map-1'), true, 'isLit should reflect stored slug')
assert.equal(isLit('map-3'), false, 'isLit should be false for unknown slug')
assert.equal(getExploredPct(2, 4), 50, 'Explored percent should be correct')
assert.equal(getExploredPct(5, 4), 100, 'Explored percent clamps at total')
assert.equal(getExploredPct(-1, 4), 0, 'Explored percent clamps at zero')

primeMapData({ maps: [{ level: 1, stuff: [{ slug: 'map-1' }, { slug: 'map-x' }] }, { level: 2, stuff: [{ slug: 'map-2' }] }] })
assert.deepEqual(litCountByLevel(), { 1: 1, 2: 1 }, 'litCountByLevel should count lit slugs per level')

console.log('PASS')
