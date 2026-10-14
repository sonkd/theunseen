import assert from 'node:assert/strict';
import test from 'node:test';
import { computeMetrics } from './lib/graph-metrics.mjs';
import { bakeLayout } from './lib/bake-layout.mjs';

function twoCliques() {
  const nodes = Array.from({ length: 12 }, (_, index) => ({ id: `node-${String(index).padStart(2, '0')}` }));
  const edges = [];
  for (let group = 0; group < 2; group += 1) {
    const start = group * 6;
    for (let i = start; i < start + 6; i += 1) {
      for (let j = i + 1; j < start + 6; j += 1) {
        edges.push({ source: nodes[i].id, target: nodes[j].id });
      }
    }
  }
  edges.push({ source: nodes[5].id, target: nodes[6].id });
  return { nodes, edges };
}

function averagePairDistance(nodes, condition) {
  const distances = [];
  for (let i = 0; i < nodes.length; i += 1) {
    for (let j = i + 1; j < nodes.length; j += 1) {
      if (condition(nodes[i], nodes[j])) {
        distances.push(Math.hypot(
          nodes[i].x - nodes[j].x,
          nodes[i].y - nodes[j].y,
          nodes[i].z - nodes[j].z,
        ));
      }
    }
  }
  return distances.reduce((sum, distance) => sum + distance, 0) / distances.length;
}

test('computes stable community IDs for connected groups and isolated nodes', () => {
  const { nodes, edges } = twoCliques();
  nodes.push({ id: 'isolated' });

  const first = computeMetrics(nodes, edges);
  const second = computeMetrics(nodes.slice().reverse(), edges.slice().reverse());
  const ids = new Map(first.map((node) => [node.id, node.communityId]));

  assert.equal(new Set(first.map((node) => node.communityId)).size, 3);
  assert.equal(ids.get('node-00'), ids.get('node-05'));
  assert.equal(ids.get('node-06'), ids.get('node-11'));
  assert.notEqual(ids.get('node-00'), ids.get('node-06'));
  assert.equal(ids.get('isolated'), 0);
  assert.deepEqual(
    new Map(second.map((node) => [node.id, node.communityId])),
    ids,
  );
});

test('bakes deterministic 3D cluster spacing without dropping isolated nodes', () => {
  const { nodes, edges } = twoCliques();
  nodes.push({ id: 'isolated', communityId: 2, degree: 0, rank: 0 });
  const metrics = computeMetrics(nodes, edges);
  const first = bakeLayout(metrics, edges);
  const second = bakeLayout(metrics, edges);
  const reordered = bakeLayout(metrics.slice().reverse(), edges.slice().reverse());

  assert.equal(first.length, nodes.length);
  assert.deepEqual(
    first.map(({ id, x, y, z, x2d, y2d }) => ({ id, x, y, z, x2d, y2d })),
    second.map(({ id, x, y, z, x2d, y2d }) => ({ id, x, y, z, x2d, y2d })),
  );
  assert.deepEqual(
    new Map(first.map(({ id, x2d, y2d }) => [id, [x2d, y2d]])),
    new Map(reordered.map(({ id, x2d, y2d }) => [id, [x2d, y2d]])),
  );
  const averageInside = averagePairDistance(
    first,
    (a, b) => a.communityId === b.communityId,
  );
  const averageAcross = averagePairDistance(
    first,
    (a, b) => a.communityId !== b.communityId,
  );
  assert.ok(averageInside < averageAcross, `expected within-community distance ${averageInside} < between-community distance ${averageAcross}`);
  assert.ok(first.some((node) => node.id === 'isolated'));
  assert.ok(first.every((node) => [node.x, node.y, node.z].every(Number.isFinite)));
  const positions2D = first.map((node) => ({ ...node, x: node.x2d, y: node.y2d, z: 0 }));
  const averageInside2D = averagePairDistance(
    positions2D,
    (a, b) => a.communityId === b.communityId,
  );
  const averageAcross2D = averagePairDistance(
    positions2D,
    (a, b) => a.communityId !== b.communityId,
  );
  assert.ok(averageInside2D < averageAcross2D, `expected 2D within-community distance ${averageInside2D} < between-community distance ${averageAcross2D}`);
  assert.ok(first.every((node) => [node.x2d, node.y2d].every(Number.isFinite)));
});

test('handles an empty graph and rejects edges with missing endpoints', () => {
  assert.deepEqual(bakeLayout([], []), []);
  assert.deepEqual(computeMetrics([], []), []);
  assert.throws(
    () => computeMetrics([{ id: 'present' }], [{ source: 'present', target: 'missing' }]),
  );
});
