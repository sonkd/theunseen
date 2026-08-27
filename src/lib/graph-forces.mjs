// Force parameters shared between the offline bake (scripts/lib/bake-layout.mjs)
// and the browser re-heat (GraphView) so a re-heated layout matches the baked one.
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

export function configureForces(sim, { forceLink, forceManyBody, forceRadial, forceCenter }, links, degreeById, radius, rankById) {
  const maxRank = rankById ? Math.max(1, ...rankById.values()) : 1;
  sim
    .force(
      'link',
      forceLink(links)
        .id((n) => n.id)
        .distance(30)
        .strength((l) => 1 / Math.min(degreeById.get(l.source.id ?? l.source) || 1, degreeById.get(l.target.id ?? l.target) || 1)),
    )
    .force('charge', forceManyBody().strength(-120).theta(0.9).distanceMax(radius * 2))
    .force(
      'radial',
      forceRadial(
        (n) => (rankById ? rankRadius(rankById.get(n.id) ?? 0, maxRank, radius) : radius),
        0,
        0,
        0,
      ).strength(0.6),
    )
    .force('center', forceCenter(0, 0, 0).strength(0.05));
  return sim;
}
