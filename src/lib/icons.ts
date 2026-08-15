// Icon mang nghĩa theo category chính — không random (build plan V5).
const CATEGORY_ICONS: Record<string, string> = {
  'bias': '▲',
  'mental-models': '●',
  'fallacy': '✱',
  'memory': '☾',
  'perception': '☀︎',
  'theory': '✦',
  'heuristic': '◆',
  'social': '☯︎',
};
const FALLBACK = ['★', '◼︎', '✦', '◆'];

export function iconFor(slug: string, categories: string[], explicit?: string): string {
  if (explicit) return explicit;
  for (const c of categories) if (CATEGORY_ICONS[c]) return CATEGORY_ICONS[c];
  let h = 0;
  for (const ch of slug) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return FALLBACK[h % FALLBACK.length];
}

export const LEVEL_MAPS = ['', 'Imagining', 'Belief', 'Thinking', 'Knowledge'] as const;
