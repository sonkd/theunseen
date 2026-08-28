// Rank quyết định node nào nằm gần lõi khối cầu hơn (rankRadius trong
// src/lib/graph-forces.mjs: rank càng cao thì bán kính càng nhỏ).
//
// Rule: map càng gần "The Sun" trong ẩn dụ hang động Plato thì càng SÂU vào
// bóng tối tri thức — level 1 (Imagining) gần trung tâm nhất, level 5
// (Knowledge) xa nhất: Imagining < Belief < Thinking < Intelligence <
// Knowledge (thứ tự xa dần trung tâm). Trong cùng 1 level, node nhiều liên
// kết hơn (degree) vẫn gần trung tâm hơn — nhưng chỉ là tie-breaker phụ,
// level luôn áp đảo nhờ LEVEL_WEIGHT >> degree tối đa thực tế.
const NUM_LEVELS = 5;
const LEVEL_WEIGHT = 1000;

function levelRankBase(level) {
  const clamped = Math.min(NUM_LEVELS, Math.max(1, level ?? NUM_LEVELS));
  return (NUM_LEVELS - clamped) * LEVEL_WEIGHT;
}

// updateRank cập nhật đệ quy: chỉ tính lại rank cho các node vừa được thêm
// (addedIds) và neighbor trực tiếp của chúng — rank của node khác không đổi
// vì rank chỉ dịch chuyển khi có cạnh mới chạm vào node đó.
function buildAdjacency(edges) {
  const adjacency = new Map();
  const touch = (id) => {
    if (!adjacency.has(id)) adjacency.set(id, new Set());
    return adjacency.get(id);
  };
  for (const e of edges) {
    touch(e.source).add(e.target);
    touch(e.target).add(e.source);
  }
  return adjacency;
}

function nodeRank(node, adjacency) {
  const degree = adjacency.get(node.id)?.size ?? 0;
  return levelRankBase(node.level) + degree;
}

export function computeRank(nodes, edges) {
  const adjacency = buildAdjacency(edges);
  return new Map(nodes.map((n) => [n.id, nodeRank(n, adjacency)]));
}

export function updateRank(prevRankById, nodes, edges, addedIds) {
  const adjacency = buildAdjacency(edges);
  const nodesById = new Map(nodes.map((n) => [n.id, n]));

  // Đệ quy 1 hop: mỗi node vừa thêm tự "lan" dirty sang neighbor trực tiếp
  // của nó, nhưng neighbor đó không lan tiếp — rank chỉ dịch chuyển ở nơi
  // một cạnh mới thực sự chạm vào.
  const dirty = new Set();
  const markDirty = (id) => {
    dirty.add(id);
    adjacency.get(id)?.forEach((neighborId) => dirty.add(neighborId));
  };
  addedIds.forEach(markDirty);

  const rankById = new Map(prevRankById);
  dirty.forEach((id) => {
    const node = nodesById.get(id);
    if (node) rankById.set(id, nodeRank(node, adjacency));
  });
  // Node hoàn toàn mới nhưng chưa từng có trong prevRankById (phòng khi addedIds
  // thiếu sót) vẫn cần một giá trị rank thay vì undefined.
  nodes.forEach((n) => {
    if (!rankById.has(n.id)) rankById.set(n.id, nodeRank(n, adjacency));
  });
  return rankById;
}
