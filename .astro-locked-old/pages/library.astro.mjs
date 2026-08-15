import { c as createComponent, r as renderComponent, f as renderScript, a as renderTemplate, m as maybeRenderHead, e as addAttribute } from '../chunks/astro/server_CwOJRIjy.mjs';
import 'piccolore';
import { $ as $$Base } from '../chunks/Base_zCXmWhgI.mjs';
import { $ as $$StuffOverlay } from '../chunks/StuffOverlay_w4u6zJAm.mjs';
import { g as getCollection, L as LEVEL_MAPS, i as iconFor } from '../chunks/icons_B8eSqVC-.mjs';
/* empty css                                   */
export { renderers } from '../renderers.mjs';

const $$Library = createComponent(async ($$result, $$props, $$slots) => {
  const stuff = (await getCollection("stuff", ({ data }) => data.published)).sort((a, b) => a.data.title.localeCompare(b.data.title));
  const levels = [1, 2, 3, 4];
  const categories = ["bias", "mental-models", "fallacy", "memory", "perception", "theory", "heuristic", "social"];
  const CATEGORY_LABELS = {
    "bias": "Bias",
    "mental-models": "Mental models",
    "fallacy": "Fallacy",
    "memory": "Memory",
    "perception": "Perception",
    "theory": "Theory",
    "heuristic": "Heuristic",
    "social": "Social"
  };
  const cardCount = stuff.length;
  const PAGE_SIZE = 50;
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Library", "data-astro-cid-hofbs6tv": true }, { "default": async ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="filters" data-astro-cid-hofbs6tv> <div class="filter-header" data-astro-cid-hofbs6tv> <div data-astro-cid-hofbs6tv> <h1 data-astro-cid-hofbs6tv>Library</h1> <p class="filter-copy" data-astro-cid-hofbs6tv>Filter by category and level, then share the URL.</p> </div> <div class="result-count" id="resultCount" data-astro-cid-hofbs6tv>Showing ${cardCount} cards</div> </div> <div class="filter-group" data-astro-cid-hofbs6tv> <div class="filter-label" data-astro-cid-hofbs6tv>Category</div> <div class="chips" id="categoryChips" data-astro-cid-hofbs6tv> ${categories.map((cat) => renderTemplate`<button type="button" class="chip" data-filter-type="category"${addAttribute(cat, "data-filter-value")} aria-pressed="false" data-astro-cid-hofbs6tv> ${CATEGORY_LABELS[cat]} </button>`)} </div> </div> <div class="filter-group" data-astro-cid-hofbs6tv> <div class="filter-label" data-astro-cid-hofbs6tv>Level</div> <div class="chips" id="levelChips" data-astro-cid-hofbs6tv> ${levels.map((l) => renderTemplate`<button type="button" class="chip" data-filter-type="level"${addAttribute(l.toString(), "data-filter-value")} aria-pressed="false" data-astro-cid-hofbs6tv> ${l} </button>`)} </div> </div> <button type="button" class="clear-button" id="clearFilters" data-astro-cid-hofbs6tv>Clear filters</button> </div> <ul class="grid" id="cardGrid"${addAttribute(PAGE_SIZE, "data-page-size")} data-astro-cid-hofbs6tv> ${stuff.map((s) => renderTemplate`<li class="card"${addAttribute(s.id, "data-slug")}${addAttribute(s.data.level.toString(), "data-level")}${addAttribute(s.data.categories.join(" "), "data-categories")} data-astro-cid-hofbs6tv> <a${addAttribute(`/stuff/${s.id}/`, "href")}${addAttribute(s.id, "data-slug")} data-astro-cid-hofbs6tv> <span class="icon" data-astro-cid-hofbs6tv>${iconFor(s.id, s.data.categories, s.data.icon)}</span> <span data-astro-cid-hofbs6tv>${s.data.title}</span> <span class="meta" data-astro-cid-hofbs6tv>${CATEGORY_LABELS[s.data.categories[0]] ?? s.data.categories[0]} · Map ${s.data.level} — ${LEVEL_MAPS[s.data.level]}</span> </a> </li>`)} </ul> <nav class="pagination hidden" id="pagination" aria-label="Library pagination" data-astro-cid-hofbs6tv> <button type="button" id="pagePrev" class="page-nav" data-astro-cid-hofbs6tv>‹ Prev</button> <div class="page-numbers" id="pageNumbers" data-astro-cid-hofbs6tv></div> <button type="button" id="pageNext" class="page-nav" data-astro-cid-hofbs6tv>Next ›</button> </nav> ${renderComponent($$result2, "StuffOverlay", $$StuffOverlay, { "data-astro-cid-hofbs6tv": true })} ` })}  ${renderScript($$result, "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/library.astro?astro&type=script&index=0&lang.ts")}`;
}, "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/library.astro", void 0);

const $$file = "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/library.astro";
const $$url = "/library";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Library,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
