// Force parameters shared between the offline bake (scripts/lib/bake-layout.mjs)
// and the browser re-heat (GraphView) so a re-heated layout matches the baked one.
export function sphereRadius(nodeCount) {
  return 4.5 * Math.sqrt(nodeCount);
}

export function configureForces(sim, { forceLink, forceManyBody, forceRadial, forceCenter }, links, degreeById, radius) {
  sim
    .force(
      'link',
      forceLink(links)
        .id((n) => n.id)
        .distance(30)
        .strength((l) => 1 / Math.min(degreeById.get(l.source.id ?? l.source) || 1, degreeById.get(l.target.id ?? l.target) || 1)),
    )
    .force('charge', forceManyBody().strength(-120).theta(0.9).distanceMax(radius * 2))
    .force('radial', forceRadial(radius, 0, 0, 0).strength(0.15))
    .force('center', forceCenter(0, 0, 0).strength(0.05));
  return sim;
}
