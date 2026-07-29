// Trích nguyên văn từ prototype "The Unseen.dc.html" (design/The Unseen.dc.html)
// và docs/design-spec.md mục 2 — đây là SOURCE OF TRUTH cho màu map, không tự chế.
export type MapPalette = {
  name: string
  vn: string
  sub: string
  cats: [string, string, string]
  gA: string
  gB: string
  treeD: string
  treeL: string
  treeHi: string
  bush: string
  path: string
  pathDot: string
  flower: string
  rock: string
  icon: string
  iconGlow: string
  dk: string
  alpha: number
}

export const MAPS: MapPalette[] = [
  {
    name: 'IMAGINING', vn: 'Tưởng tượng', sub: 'EIKASIA', cats: ['SHADOW', 'IMAGE', 'ECHO'],
    gA: '#1e1c3a', gB: '#1a1834', treeD: '#100e24', treeL: '#2a2750', treeHi: '#3a366b', bush: '#232048',
    path: '#4c4680', pathDot: '#3d3868', flower: '#8f7fe0', rock: '#4a4670',
    icon: '#cfc2ff', iconGlow: 'rgba(160,130,255,.85)', dk: '5,4,16', alpha: .97,
  },
  {
    name: 'BELIEF', vn: 'Niềm tin', sub: 'PISTIS', cats: ['OBJECT', 'SENSE', 'HABIT'],
    gA: '#17414b', gB: '#143a43', treeD: '#0c2830', treeL: '#20565f', treeHi: '#2f6f78', bush: '#123640',
    path: '#7e9a94', pathDot: '#6b8781', flower: '#d8b46a', rock: '#4f6a6b',
    icon: '#aef0dd', iconGlow: 'rgba(90,220,180,.85)', dk: '4,16,18', alpha: .93,
  },
  {
    name: 'THINKING', vn: 'Tư duy', sub: 'DIANOIA', cats: ['MATH', 'LOGIC', 'HYPOTHESIS'],
    gA: '#8ed3ac', gB: '#85cba3', treeD: '#47927e', treeL: '#68b199', treeHi: '#83c7ae', bush: '#57ad83',
    path: '#f2ecd9', pathDot: '#e0d7bd', flower: '#f2d24d', rock: '#b9c4bb',
    icon: '#0f5140', iconGlow: 'rgba(255,240,170,.9)', dk: '8,32,24', alpha: .88,
  },
  {
    name: 'INTELLIGENCE', vn: 'Lý tính', sub: 'NOESIS', cats: ['FORM', 'DIALECTIC', 'ESSENCE'],
    gA: '#cfe0a4', gB: '#c7d899', treeD: '#7c9a54', treeL: '#9cba70', treeHi: '#b4d086', bush: '#a4c476',
    path: '#f7f0da', pathDot: '#e7dec2', flower: '#e08a4a', rock: '#bdb694',
    icon: '#5a4a10', iconGlow: 'rgba(255,220,120,.9)', dk: '40,30,6', alpha: .8,
  },
  {
    name: 'KNOWLEDGE', vn: 'Tri thức', sub: 'EPISTEME', cats: ['SUN', 'TRUTH', 'GOOD'],
    gA: '#f0e2b2', gB: '#ecdca6', treeD: '#c49f55', treeL: '#dcbd74', treeHi: '#ecd694', bush: '#dfc98a',
    path: '#fcf7e6', pathDot: '#efe6cb', flower: '#dd6440', rock: '#d3c7a8',
    icon: '#7a4408', iconGlow: 'rgba(255,200,90,.95)', dk: '70,48,4', alpha: .5,
  },
]

export const ROMANS = ['I', 'II', 'III', 'IV', 'V'] as const
