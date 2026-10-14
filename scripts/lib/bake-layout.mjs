// Offline 3D layout bake: Fibonacci-sphere init + d3-force-3d simulation run
// headless in Node, so the browser only ever paints a finished sphere.
import { forceSimulation, forceLink, forceManyBody, forceRadial, forceCenter, forceCollide } from 'd3-force-3d';
import { mulberry32, seededShuffle } from './seeded-random.mjs';
import { sphereRadius, configureForces } from '../../src/lib/graph-forces.mjs';

const SHUFFLE_SEED = 42;
const TICKS = 600;
const COMMUNITY_TICKS = 240;
const TWO_D_TICKS = 480;

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

function communityLayout(nodes, edges, radius) {
  const membersByCommunity = new Map();
  const communityById = new Map();

  nodes.forEach((node) => {
    const communityId = node.communityId ?? 0;
    communityById.set(node.id, communityId);
    const members = membersByCommunity.get(communityId) ?? [];
    members.push(node.id);
    membersByCommunity.set(communityId, members);
  });

  const communities = [...membersByCommunity.entries()]
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(([id, memberIds]) => {
      const clusterRadius = Math.min(radius * 0.48, 7 + Math.sqrt(memberIds.length) * 3);
      return { id: String(id), communityId: id, size: memberIds.length, radius: clusterRadius };
    });

  if (communities.length === 1) {
    const community = communities[0];
    return {
      communityById,
      anchors: new Map([[community.communityId, { x: 0, y: 0, z: 0, radius: community.radius }]]),
    };
  }

  fibonacciSphereInit(communities, radius * 0.7);

  const betweenCommunityEdges = new Map();
  edges.forEach((edge) => {
    const sourceCommunity = communityById.get(edge.source);
    const targetCommunity = communityById.get(edge.target);
    if (sourceCommunity === undefined || targetCommunity === undefined || sourceCommunity === targetCommunity) return;

    const [first, second] = [String(sourceCommunity), String(targetCommunity)].sort();
    const key = `${first}\u0000${second}`;
    betweenCommunityEdges.set(key, (betweenCommunityEdges.get(key) ?? 0) + 1);
  });

  const communityLinks = [...betweenCommunityEdges.entries()]
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(([key, weight]) => {
      const [source, target] = key.split('\u0000');
      return { source, target, weight };
    });
  const anchorSimulation = forceSimulation(communities, 3)
    .randomSource(mulberry32(SHUFFLE_SEED + 1))
    .alphaDecay(0.02)
    .velocityDecay(0.4)
    .force(
      'link',
      forceLink(communityLinks)
        .id((community) => community.id)
        .distance((link) => {
          const baseDistance = link.source.radius + link.target.radius + 12;
          return baseDistance / Math.min(1.5, Math.sqrt(link.weight));
        })
        .strength((link) => Math.min(0.7, 0.3 + Math.log1p(link.weight) * 0.08)),
    )
    .force('charge', forceManyBody().strength(-radius * 0.8).distanceMax(radius * 3))
    .force('collide', forceCollide((community) => community.radius + 4).strength(0.9).iterations(2))
    .force('center', forceCenter(0, 0, 0).strength(0.08))
    .stop();

  for (let i = 0; i < COMMUNITY_TICKS; i += 1) anchorSimulation.tick();

  const center = communities.reduce(
    (sum, community) => [sum[0] + community.x, sum[1] + community.y, sum[2] + community.z],
    [0, 0, 0],
  ).map((coordinate) => coordinate / communities.length);

  const anchors = new Map(
    communities.map((community) => [
      community.communityId,
      {
        x: community.x - center[0],
        y: community.y - center[1],
        z: community.z - center[2],
        radius: community.radius,
      },
    ]),
  );
  return { communityById, anchors };
}

function communityLayout2D(nodes, edges, radius) {
  const membersByCommunity = new Map();
  const communityById = new Map();

  nodes.forEach((node) => {
    const communityId = node.communityId ?? 0;
    communityById.set(node.id, communityId);
    const members = membersByCommunity.get(communityId) ?? [];
    members.push(node.id);
    membersByCommunity.set(communityId, members);
  });

  const communities = [...membersByCommunity.entries()]
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(([id, memberIds]) => ({
      id: String(id),
      communityId: id,
      size: memberIds.length,
      radius: Math.min(radius * 0.48, 7 + Math.sqrt(memberIds.length) * 3),
    }));

  if (communities.length === 1) {
    const community = communities[0];
    return {
      communityById,
      anchors: new Map([[community.communityId, { x: 0, y: 0, radius: community.radius }]]),
    };
  }

  const anchorRadius = radius * Math.max(1, Math.sqrt(communities.length / 4));
  const angleStep = (Math.PI * 2) / communities.length;
  communities.forEach((community, index) => {
    const angle = angleStep * index - Math.PI / 2;
    community.x = Math.cos(angle) * anchorRadius;
    community.y = Math.sin(angle) * anchorRadius;
  });

  const betweenCommunityEdges = new Map();
  edges.forEach((edge) => {
    const sourceCommunity = communityById.get(edge.source);
    const targetCommunity = communityById.get(edge.target);
    if (sourceCommunity === undefined || targetCommunity === undefined || sourceCommunity === targetCommunity) return;

    const [first, second] = [String(sourceCommunity), String(targetCommunity)].sort();
    const key = `${first}\u0000${second}`;
    betweenCommunityEdges.set(key, (betweenCommunityEdges.get(key) ?? 0) + 1);
  });

  const communityLinks = [...betweenCommunityEdges.entries()]
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(([key, weight]) => {
      const [source, target] = key.split('\u0000');
      return { source, target, weight };
    });
  const anchorSimulation = forceSimulation(communities, 2)
    .randomSource(mulberry32(SHUFFLE_SEED + 2))
    .alphaDecay(0.025)
    .velocityDecay(0.4)
    .force(
      'link',
      forceLink(communityLinks)
        .id((community) => community.id)
        .distance((link) => {
          const baseDistance = link.source.radius + link.target.radius + 18;
          return baseDistance / Math.min(1.5, Math.sqrt(link.weight));
        })
        .strength((link) => Math.min(0.7, 0.3 + Math.log1p(link.weight) * 0.08)),
    )
    .force('charge', forceManyBody().strength(-radius * 0.8).distanceMax(radius * 3))
    .force('collide', forceCollide((community) => community.radius + 8).strength(0.9).iterations(2))
    .force('center', forceCenter(0, 0).strength(0.08))
    .stop();

  for (let i = 0; i < COMMUNITY_TICKS; i += 1) anchorSimulation.tick();

  const center = communities.reduce(
    (sum, community) => [sum[0] + community.x, sum[1] + community.y],
    [0, 0],
  ).map((coordinate) => coordinate / communities.length);
  const anchors = new Map(
    communities.map((community) => [
      community.communityId,
      {
        x: community.x - center[0],
        y: community.y - center[1],
        radius: community.radius,
      },
    ]),
  );
  return { communityById, anchors };
}

function bake2DPositions(nodes, edges, radius) {
  const { communityById, anchors } = communityLayout2D(nodes, edges, radius);
  const memberIndexByCommunity = new Map();
  const memberCountByCommunity = new Map();
  nodes.forEach((node) => {
    const communityId = node.communityId ?? 0;
    memberCountByCommunity.set(communityId, (memberCountByCommunity.get(communityId) ?? 0) + 1);
  });

  const ordered = nodes
    .slice()
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0))
    .map((node) => ({ ...node }));
  ordered.forEach((node) => {
    const communityId = node.communityId ?? 0;
    const memberIndex = memberIndexByCommunity.get(communityId) ?? 0;
    memberIndexByCommunity.set(communityId, memberIndex + 1);

    const count = memberCountByCommunity.get(communityId);
    const angle = memberIndex * Math.PI * (3 - Math.sqrt(5));
    const localRadius = anchors.get(communityId).radius * 0.72 * Math.sqrt((memberIndex + 0.5) / count);
    node.x = anchors.get(communityId).x + Math.cos(angle) * localRadius;
    node.y = anchors.get(communityId).y + Math.sin(angle) * localRadius;
  });

  const links = edges
    .map((edge) => ({ source: edge.source, target: edge.target }))
    .sort((a, b) => (
      a.source < b.source ? -1 : a.source > b.source ? 1
        : a.target < b.target ? -1 : a.target > b.target ? 1 : 0
    ));
  const simulation = forceSimulation(ordered, 2)
    .randomSource(mulberry32(SHUFFLE_SEED + 3))
    .alphaDecay(0.012)
    .velocityDecay(0.4)
    .force(
      'link',
      forceLink(links)
        .id((node) => node.id)
        .distance(16)
        .strength((link) => {
          const sourceId = link.source.id ?? link.source;
          const targetId = link.target.id ?? link.target;
          const sameCommunity = communityById.get(sourceId) === communityById.get(targetId);
          return sameCommunity ? 0.18 : 0.04;
        }),
    )
    .force('charge', forceManyBody().strength(-32).distanceMax(radius * 2))
    .force('collide', forceCollide(2.5).strength(0.9).iterations(2))
    .force('cluster', forceCluster2D(anchors))
    .force('center', forceCenter(0, 0).strength(0.025))
    .stop();

  for (let i = 0; i < TWO_D_TICKS; i += 1) simulation.tick();

  const center = ordered.reduce(
    (sum, node) => [sum[0] + node.x, sum[1] + node.y],
    [0, 0],
  ).map((coordinate) => coordinate / ordered.length);
  const byId = new Map(ordered.map((node) => [node.id, node]));

  return nodes.map((node) => {
    const positioned = byId.get(node.id);
    return {
      x2d: Math.round((positioned.x - center[0]) * 100) / 100,
      y2d: Math.round((positioned.y - center[1]) * 100) / 100,
    };
  });
}

function forceCluster2D(anchors, strength = 0.2) {
  let nodes = [];
  function force(alpha) {
    nodes.forEach((node) => {
      const anchor = anchors.get(node.communityId ?? 0);
      if (!anchor) return;
      const dx = node.x - anchor.x;
      const dy = node.y - anchor.y;
      const distance = Math.hypot(dx, dy);
      if (distance <= anchor.radius * 0.72 || distance === 0) return;
      const pull = ((distance - anchor.radius * 0.72) / distance) * strength * alpha;
      node.vx -= dx * pull;
      node.vy -= dy * pull;
    });
  }
  force.initialize = (simulationNodes) => {
    nodes = simulationNodes;
  };
  return force;
}

export function bakeLayout(nodes, edges) {
  if (nodes.length === 0) return [];

  const radius = sphereRadius(nodes.length || 1);
  const twoDPositions = bake2DPositions(nodes, edges, radius);
  const { communityById, anchors } = communityLayout(nodes, edges, radius);
  const rng = mulberry32(SHUFFLE_SEED);
  const ordered = seededShuffle(
    nodes
      .slice()
      .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0))
      .map((node) => ({ ...node })),
    rng,
  );
  const memberIndexByCommunity = new Map();
  const memberCountByCommunity = new Map();
  nodes.forEach((node) => {
    const communityId = node.communityId ?? 0;
    memberCountByCommunity.set(communityId, (memberCountByCommunity.get(communityId) ?? 0) + 1);
  });
  ordered.forEach((node) => {
    const communityId = node.communityId ?? 0;
    const memberIndex = memberIndexByCommunity.get(communityId) ?? 0;
    memberIndexByCommunity.set(communityId, memberIndex + 1);

    const count = memberCountByCommunity.get(communityId);
    const phi = Math.PI * (3 - Math.sqrt(5));
    const y = count === 1 ? 0 : 1 - (memberIndex / (count - 1)) * 2;
    const radial = Math.sqrt(Math.max(0, 1 - y * y));
    const theta = phi * memberIndex;
    const anchor = anchors.get(communityId);
    const localRadius = anchor.radius * 0.75;
    node.x = anchor.x + localRadius * Math.cos(theta) * radial;
    node.y = anchor.y + localRadius * y;
    node.z = anchor.z + localRadius * Math.sin(theta) * radial;
  });

  const degreeById = new Map(nodes.map((n) => [n.id, n.degree || 1]));
  const rankById = new Map(nodes.map((n) => [n.id, n.rank ?? n.degree ?? 0]));
  const links = edges
    .map((edge) => ({ source: edge.source, target: edge.target }))
    .sort((a, b) => (
      a.source < b.source ? -1 : a.source > b.source ? 1
        : a.target < b.target ? -1 : a.target > b.target ? 1 : 0
    ));

  const sim = forceSimulation(ordered, 3)
    .randomSource(mulberry32(SHUFFLE_SEED))
    .alphaDecay(0.01)
    .velocityDecay(0.4)
    .stop();
  configureForces(
    sim,
    { forceLink, forceManyBody, forceRadial, forceCenter, forceCollide },
    links,
    degreeById,
    radius,
    rankById,
    communityById,
    anchors,
  );

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

  return nodes.map((node, index) => {
    const n = byId.get(node.id);
    return {
      ...node,
      x: Math.round((n.x - cx) * 100) / 100,
      y: Math.round((n.y - cy) * 100) / 100,
      z: Math.round((n.z - cz) * 100) / 100,
      ...twoDPositions[index],
    };
  });
}
