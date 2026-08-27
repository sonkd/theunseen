// Offline 3D layout bake: Fibonacci-sphere init + d3-force-3d simulation run
// headless in Node, so the browser only ever paints a finished sphere.
import { forceSimulation, forceLink, forceManyBody, forceRadial, forceCenter } from 'd3-force-3d';
import { mulberry32, seededShuffle } from './seeded-random.mjs';
import { sphereRadius, configureForces } from '../../src/lib/graph-forces.mjs';

const SHUFFLE_SEED = 42;
const TICKS = 600;

function fibonacciSphereInit(nodes, radius) {
  const n = nodes.length;
  const phi = Math.PI * (3 - Math.sqrt(5));
  nodes.forEach((node, i) => {
    const y = n === 1 ? 0 : 1 - (i / (n - 1)) * 2;
    const r = Math.sqrt(Math.max(0, 1 - y * y));
    const theta = phi * i;
    node.x = radius * Math.cos(theta) * r;
    node.y = radius * y;
    node.z = radius * Math.sin(theta) * r;
  });
}

export function bakeLayout(nodes, edges) {
  const radius = sphereRadius(nodes.length || 1);
  const rng = mulberry32(SHUFFLE_SEED);
  const ordered = seededShuffle(nodes, rng);
  fibonacciSphereInit(ordered, radius);

  const degreeById = new Map(nodes.map((n) => [n.id, n.degree || 1]));
  const rankById = new Map(nodes.map((n) => [n.id, n.rank ?? n.degree ?? 0]));
  const links = edges.map((e) => ({ source: e.source, target: e.target }));

  const sim = forceSimulation(ordered, 3)
    .alphaDecay(0.01)
    .velocityDecay(0.4)
    .stop();
  configureForces(sim, { forceLink, forceManyBody, forceRadial, forceCenter }, links, degreeById, radius, rankById);

  for (let i = 0; i < TICKS; i += 1) sim.tick();

  // Recenter + rescale to a normalized bbox so the sphere is centered at origin.
  const byId = new Map(ordered.map((n) => [n.id, n]));
  let cx = 0;
  let cy = 0;
  let cz = 0;
  ordered.forEach((n) => { cx += n.x; cy += n.y; cz += n.z; });
  cx /= ordered.length || 1;
  cy /= ordered.length || 1;
  cz /= ordered.length || 1;

  return nodes.map((node) => {
    const n = byId.get(node.id);
    return {
      ...node,
      x: Math.round((n.x - cx) * 100) / 100,
      y: Math.round((n.y - cy) * 100) / 100,
      z: Math.round((n.z - cz) * 100) / 100,
    };
  });
}
