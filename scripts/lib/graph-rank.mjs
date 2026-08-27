// Rank = degree (số cạnh) của mỗi node, dùng để xếp node nhiều liên kết hơn
// vào gần lõi khối cầu hơn (xem rankRadius trong src/lib/graph-forces.mjs).
//
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

export function computeRank(nodes, edges) {
  const adjacency = buildAdjacency(edges);
  return new Map(nodes.map((n) => [n.id, adjacency.get(n.id)?.size ?? 0]));
}

export function updateRank(prevRankById, nodes, edges, addedIds) {
  const adjacency = buildAdjacency(edges);
  const nodeIds = new Set(nodes.map((n) => n.id));

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
    if (nodeIds.has(id)) rankById.set(id, adjacency.get(id)?.size ?? 0);
  });
  // Node hoàn toàn mới nhưng chưa từng có trong prevRankById (phòng khi addedIds
  // thiếu sót) vẫn cần một giá trị rank thay vì undefined.
  nodes.forEach((n) => {
    if (!rankById.has(n.id)) rankById.set(n.id, adjacency.get(n.id)?.size ?? 0);
  });
  return rankById;
}
