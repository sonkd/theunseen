import { b as createAstro, c as createComponent, m as maybeRenderHead, f as renderScript, a as renderTemplate, r as renderComponent, e as addAttribute } from '../../chunks/astro/server_CwOJRIjy.mjs';
import 'piccolore';
import { $ as $$Base } from '../../chunks/Base_zCXmWhgI.mjs';
import 'clsx';
/* empty css                                     */
import { r as renderEntry, g as getCollection, i as iconFor, L as LEVEL_MAPS } from '../../chunks/icons_B8eSqVC-.mjs';
export { renderers } from '../../renderers.mjs';

const $$Astro$1 = createAstro("https://theunseen.example.com");
const $$FlipCard = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$FlipCard;
  const { front, back, icon } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<button class="flip" aria-label="Flip card" data-astro-cid-mmspuptz> <span class="face front" data-astro-cid-mmspuptz><span class="icon" data-astro-cid-mmspuptz>${icon}</span><span data-astro-cid-mmspuptz>${front}</span></span> <span class="face back" data-astro-cid-mmspuptz>${back}</span> </button>  ${renderScript($$result, "/sessions/funny-exciting-shannon/mnt/theunseen/src/components/FlipCard.astro?astro&type=script&index=0&lang.ts")}`;
}, "/sessions/funny-exciting-shannon/mnt/theunseen/src/components/FlipCard.astro", void 0);

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(cooked.slice()) }));
var _a;
const $$Astro = createAstro("https://theunseen.example.com");
async function getStaticPaths() {
  const all = await getCollection("stuff", ({ data }) => data.published);
  return all.map((s) => ({ params: { slug: s.id }, props: { s, all } }));
}
const $$slug = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$slug;
  const { s, all } = Astro2.props;
  const { Content } = await renderEntry(s);
  const related = s.data.links.map((slug) => all.find((x) => x.id === slug)).filter(Boolean);
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": s.data.title, "description": s.data.back, "data-astro-cid-tpy6nfu7": true }, { "default": async ($$result2) => renderTemplate(_a || (_a = __template([" ", '<article data-pagefind-body data-pagefind-meta data-astro-cid-tpy6nfu7> <script type="application/json" data-pagefind-meta>\n      {JSON.stringify({ title: s.data.title })}\n    <\/script> <p class="meta" data-astro-cid-tpy6nfu7>Map ', " \u2014 ", " \xB7 ", "</p> <h1 data-astro-cid-tpy6nfu7>", "</h1> ", " ", " ", " ", " ", " ", " </article> "])), maybeRenderHead(), s.data.level, LEVEL_MAPS[s.data.level], s.data.categories.join(", "), s.data.title, renderComponent($$result2, "FlipCard", $$FlipCard, { "front": s.data.front, "back": s.data.back, "icon": iconFor(s.id, s.data.categories, s.data.icon), "data-astro-cid-tpy6nfu7": true }), s.data.strategy && renderTemplate`<p data-astro-cid-tpy6nfu7><strong data-astro-cid-tpy6nfu7>Strategy:</strong> ${s.data.strategy}</p>`, renderComponent($$result2, "Content", Content, { "data-astro-cid-tpy6nfu7": true }), s.data.approaches.length > 0 && renderTemplate`<section data-astro-cid-tpy6nfu7><h2 data-astro-cid-tpy6nfu7>Approaches</h2> <ul data-astro-cid-tpy6nfu7>${s.data.approaches.map((a) => renderTemplate`<li data-astro-cid-tpy6nfu7><a${addAttribute(a.url, "href")} data-astro-cid-tpy6nfu7>${a.title}</a></li>`)}</ul> </section>`, related.length > 0 && renderTemplate`<section data-astro-cid-tpy6nfu7><h2 data-astro-cid-tpy6nfu7>Connected flames</h2> <ul data-astro-cid-tpy6nfu7>${related.map((r) => r && renderTemplate`<li data-astro-cid-tpy6nfu7><a${addAttribute(`/stuff/${r.id}/`, "href")} data-astro-cid-tpy6nfu7>${r.data.title}</a></li>`)}</ul> </section>`, s.data.refs.length > 0 && renderTemplate`<section data-astro-cid-tpy6nfu7><h2 data-astro-cid-tpy6nfu7>References</h2> <ul data-astro-cid-tpy6nfu7>${s.data.refs.map((r) => renderTemplate`<li data-astro-cid-tpy6nfu7><a${addAttribute(r, "href")} rel="nofollow noopener" data-astro-cid-tpy6nfu7>${r}</a></li>`)}</ul> </section>`) })} `;
}, "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/stuff/[slug].astro", void 0);

const $$file = "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/stuff/[slug].astro";
const $$url = "/stuff/[slug]";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$slug,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
