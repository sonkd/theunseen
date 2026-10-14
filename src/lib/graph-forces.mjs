// Force parameters used by the offline bake (scripts/lib/bake-layout.mjs).
export function sphereRadius(nodeCount) {
  return 4.5 * Math.sqrt(nodeCount);
}

// Bán kính đích cho một node theo rank (số cạnh): rank càng cao thì càng gần
// lõi (minR), rank 0 nằm sát vỏ ngoài (radius). log1p để vài hub không kéo
// lệch toàn bộ thang đo so với phần đông node rank thấp.
export function rankRadius(rank, maxRank, radius) {
  const minR = radius * 0.18;
  if (maxRank <= 0) return radius;
  const norm = Math.log1p(rank) / Math.log1p(maxRank);
  return radius - norm * (radius - minR);
}

export function forceCluster(anchors, strength = 0.18, dimensions = 3) {
  let nodes = [];

  function force(alpha) {
    nodes.forEach((node) => {
      const anchor = anchors.get(node.communityId ?? 0);
      if (!anchor) return;

      const dx = node.x - anchor.x;
      const dy = node.y - anchor.y;
      const dz = dimensions === 3 ? node.z - anchor.z : 0;
      const distance = Math.hypot(dx, dy, dz);
      if (distance <= anchor.radius || distance === 0) return;

      const pull = ((distance - anchor.radius) / distance) * strength * alpha;
      node.vx -= dx * pull;
      node.vy -= dy * pull;
      if (dimensions === 3) node.vz -= dz * pull;
    });
  }

  force.initialize = (simulationNodes) => {
    nodes = simulationNodes;
  };
  return force;
}

export function configureForces(
  sim,
  { forceLink, forceManyBody, forceRadial, forceCenter, forceCollide },
  links,
  degreeById,
  radius,
  rankById,
  communityById,
  communityAnchors,
) {
  const maxRank = rankById ? Math.max(1, ...rankById.values()) : 1;
  sim
    .force(
      'link',
      forceLink(links)
        .id((n) => n.id)
        .distance(30)
        .strength((l) => {
          const sourceId = l.source.id ?? l.source;
          const targetId = l.target.id ?? l.target;
          const baseStrength = 1 / Math.min(degreeById.get(sourceId) || 1, degreeById.get(targetId) || 1);
          return baseStrength * (communityById.get(sourceId) === communityById.get(targetId) ? 1 : 0.35);
        }),
    )
    .force('charge', forceManyBody().strength(-120).theta(0.9).distanceMax(radius * 2))
    .force('collide', forceCollide(2.5).strength(0.8).iterations(2))
    .force(
      'radial',
      forceRadial(
        (n) => (rankById ? rankRadius(rankById.get(n.id) ?? 0, maxRank, radius) : radius),
        0,
        0,
        0,
      ).strength(0.6),
    )
    .force('cluster', forceCluster(communityAnchors))
    .force('center', forceCenter(0, 0, 0).strength(0.05));
  return sim;
}
