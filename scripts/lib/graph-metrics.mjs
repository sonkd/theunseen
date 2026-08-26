// Graph metrics computed offline (build time): degree, connected component, community.
import Graph from 'graphology';
import { connectedComponents } from 'graphology-components';
import louvain from 'graphology-communities-louvain';
import { mulberry32 } from './seeded-random.mjs';

const LOUVAIN_SEED = 1337;

export function computeMetrics(nodes, edges) {
  const graph = new Graph({ type: 'undirected', multi: false, allowSelfLoops: false });
  for (const node of nodes) graph.addNode(node.id);
  for (const edge of edges) {
    if (!graph.hasEdge(edge.source, edge.target)) {
      graph.addEdge(edge.source, edge.target);
    }
  }

  const components = connectedComponents(graph);
  const componentId = new Map();
  components.forEach((component, index) => {
    component.forEach((id) => componentId.set(id, index));
  });

  if (graph.order > 0) {
    louvain.assign(graph, { rng: mulberry32(LOUVAIN_SEED) });
  }

  return nodes.map((node) => ({
    ...node,
    degree: graph.hasNode(node.id) ? graph.degree(node.id) : 0,
    componentId: componentId.get(node.id) ?? -1,
    communityId: graph.hasNode(node.id) ? graph.getNodeAttribute(node.id, 'community') ?? 0 : 0,
  }));
}
