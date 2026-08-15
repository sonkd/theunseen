import { b as createAstro, c as createComponent, m as maybeRenderHead, r as renderComponent, F as Fragment, a as renderTemplate, e as addAttribute, f as renderScript } from '../chunks/astro/server_CwOJRIjy.mjs';
import 'piccolore';
import { $ as $$Base } from '../chunks/Base_zCXmWhgI.mjs';
/* empty css                                 */
import { $ as $$StuffOverlay } from '../chunks/StuffOverlay_w4u6zJAm.mjs';
export { renderers } from '../renderers.mjs';

const MAPS = [
  {
    name: "IMAGINING",
    vn: "Tưởng tượng",
    sub: "EIKASIA",
    cats: ["SHADOW", "IMAGE", "ECHO"],
    gA: "#1e1c3a",
    gB: "#1a1834",
    treeD: "#100e24",
    treeL: "#2a2750",
    treeHi: "#3a366b",
    bush: "#232048",
    path: "#4c4680",
    pathDot: "#3d3868",
    flower: "#8f7fe0",
    rock: "#4a4670",
    icon: "#cfc2ff",
    iconGlow: "rgba(160,130,255,.85)",
    dk: "5,4,16",
    alpha: 0.97
  },
  {
    name: "BELIEF",
    vn: "Niềm tin",
    sub: "PISTIS",
    cats: ["OBJECT", "SENSE", "HABIT"],
    gA: "#17414b",
    gB: "#143a43",
    treeD: "#0c2830",
    treeL: "#20565f",
    treeHi: "#2f6f78",
    bush: "#123640",
    path: "#7e9a94",
    pathDot: "#6b8781",
    flower: "#d8b46a",
    rock: "#4f6a6b",
    icon: "#aef0dd",
    iconGlow: "rgba(90,220,180,.85)",
    dk: "4,16,18",
    alpha: 0.93
  },
  {
    name: "THINKING",
    vn: "Tư duy",
    sub: "DIANOIA",
    cats: ["MATH", "LOGIC", "HYPOTHESIS"],
    gA: "#8ed3ac",
    gB: "#85cba3",
    treeD: "#47927e",
    treeL: "#68b199",
    treeHi: "#83c7ae",
    bush: "#57ad83",
    path: "#f2ecd9",
    pathDot: "#e0d7bd",
    flower: "#f2d24d",
    rock: "#b9c4bb",
    icon: "#0f5140",
    iconGlow: "rgba(255,240,170,.9)",
    dk: "8,32,24",
    alpha: 0.88
  },
  {
    name: "INTELLIGENCE",
    vn: "Lý tính",
    sub: "NOESIS",
    cats: ["FORM", "DIALECTIC", "ESSENCE"],
    gA: "#cfe0a4",
    gB: "#c7d899",
    treeD: "#7c9a54",
    treeL: "#9cba70",
    treeHi: "#b4d086",
    bush: "#a4c476",
    path: "#f7f0da",
    pathDot: "#e7dec2",
    flower: "#e08a4a",
    rock: "#bdb694",
    icon: "#5a4a10",
    iconGlow: "rgba(255,220,120,.9)",
    dk: "40,30,6",
    alpha: 0.8
  },
  {
    name: "KNOWLEDGE",
    vn: "Tri thức",
    sub: "EPISTEME",
    cats: ["SUN", "TRUTH", "GOOD"],
    gA: "#f0e2b2",
    gB: "#ecdca6",
    treeD: "#c49f55",
    treeL: "#dcbd74",
    treeHi: "#ecd694",
    bush: "#dfc98a",
    path: "#fcf7e6",
    pathDot: "#efe6cb",
    flower: "#dd6440",
    rock: "#d3c7a8",
    icon: "#7a4408",
    iconGlow: "rgba(255,200,90,.95)",
    dk: "70,48,4",
    alpha: 0.5
  }
];
const ROMANS = ["I", "II", "III", "IV", "V"];

const $$Astro = createAstro("https://theunseen.example.com");
const $$MapCanvas = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$MapCanvas;
  const mapLabelsSSR = MAPS.map((m) => m.name.charAt(0) + m.name.slice(1).toLowerCase());
  return renderTemplate`${maybeRenderHead()}<div class="map-shell" data-astro-cid-exfwc5f3> <div class="map-viewport" id="mapViewport" data-astro-cid-exfwc5f3> <canvas id="mapCanvas" aria-label="Map exploration canvas" tabindex="0" autofocus data-astro-cid-exfwc5f3></canvas> <div class="map-badge-group" data-astro-cid-exfwc5f3> <div id="mapBadge" class="map-badge" data-astro-cid-exfwc5f3></div> <div id="mapBadgeSub" class="map-badge-sub" data-astro-cid-exfwc5f3></div> </div> <div id="fireBadge" class="fire-badge hidden" data-astro-cid-exfwc5f3>A FIRE</div> <div id="tooltip" class="map-tooltip hidden" data-astro-cid-exfwc5f3></div> <div id="finalePanel" class="finale-panel hidden" data-astro-cid-exfwc5f3> <div class="finale-title" data-astro-cid-exfwc5f3>V · KNOWLEDGE</div> <div id="finaleCount" class="finale-count" data-astro-cid-exfwc5f3></div> <div class="finale-links" data-astro-cid-exfwc5f3> <a href="/library/" data-astro-cid-exfwc5f3>LIBRARY · THƯ VIỆN</a> <a href="/graph/" data-astro-cid-exfwc5f3>GRAPH · SƠ ĐỒ</a> </div> </div> </div> <div class="chrome-bottom" data-astro-cid-exfwc5f3> <div class="breadcrumb" id="breadcrumb" data-astro-cid-exfwc5f3> ${mapLabelsSSR.map((label, index) => renderTemplate`${renderComponent($$result, "Fragment", Fragment, { "data-astro-cid-exfwc5f3": true }, { "default": async ($$result2) => renderTemplate` <button type="button" class="breadcrumb-btn"${addAttribute(index, "data-map-index")} data-astro-cid-exfwc5f3>${label.toUpperCase()}</button> ${index < mapLabelsSSR.length - 1 && renderTemplate`<span class="sep" data-astro-cid-exfwc5f3>›</span>`}` })}`)} </div> <div class="chrome-spacer" data-astro-cid-exfwc5f3></div> <div class="hint" data-astro-cid-exfwc5f3>PHÍM ← → ĐỂ ĐI BỘ · &lt; &gt; NHẢY VÙNG · ARROWS TO WALK</div> </div> </div> <div class="hud-corner" data-astro-cid-exfwc5f3> <div id="optionsPanel" class="options-panel hidden" role="dialog" aria-modal="true" data-astro-cid-exfwc5f3> <div class="options-header" data-astro-cid-exfwc5f3>OPTIONS · TUỲ CHỌN</div> <div class="options-row" data-astro-cid-exfwc5f3> <span data-astro-cid-exfwc5f3>TORCH · BÁN KÍNH ĐUỐC</span><span id="radiusValue" data-astro-cid-exfwc5f3>500PX</span> </div> <input id="radiusRange" type="range" min="500" max="900" step="10" value="500" data-astro-cid-exfwc5f3> <label class="toggle-row" data-astro-cid-exfwc5f3> <input id="revealAll" type="checkbox" data-astro-cid-exfwc5f3> REVEAL MAP · HIỆN BẢN ĐỒ
</label> <div class="options-row-label" data-astro-cid-exfwc5f3>JUMP TO MAP · NHẢY MAP</div> <div class="quick-nav" id="quickNav" data-astro-cid-exfwc5f3> ${ROMANS.map((roman, index) => renderTemplate`<button type="button" class="quick-nav-btn"${addAttribute(index, "data-map-index")} data-astro-cid-exfwc5f3>${roman}</button>`)} </div> </div> <button id="optionsButton" class="options-button" data-astro-cid-exfwc5f3>OPTIONS ▴</button> <div class="move-row" data-astro-cid-exfwc5f3> <button id="zonePrev" class="control-button" aria-label="Previous" data-astro-cid-exfwc5f3> <svg width="20" height="20" viewBox="0 0 26 26" data-astro-cid-exfwc5f3><polygon points="19,3 6,13 19,23" fill="#111" data-astro-cid-exfwc5f3></polygon></svg> </button> <div class="move-label" data-astro-cid-exfwc5f3>MOVE</div> <button id="zoneNext" class="control-button" aria-label="Next" data-astro-cid-exfwc5f3> <svg width="20" height="20" viewBox="0 0 26 26" data-astro-cid-exfwc5f3><polygon points="7,3 20,13 7,23" fill="#111" data-astro-cid-exfwc5f3></polygon></svg> </button> </div> </div>  ${renderScript($$result, "/sessions/funny-exciting-shannon/mnt/theunseen/src/components/map/MapCanvas.astro?astro&type=script&index=0&lang.ts")}`;
}, "/sessions/funny-exciting-shannon/mnt/theunseen/src/components/map/MapCanvas.astro", void 0);

const $$Index = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Home", "fullBleed": true }, { "default": ($$result2) => renderTemplate` ${renderComponent($$result2, "MapCanvas", $$MapCanvas, {})} ${renderComponent($$result2, "StuffOverlay", $$StuffOverlay, {})} ` })}`;
}, "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/index.astro", void 0);

const $$file = "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/index.astro";
const $$url = "";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
