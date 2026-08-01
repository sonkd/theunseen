import { c as createComponent, r as renderComponent, a as renderTemplate, m as maybeRenderHead } from '../chunks/astro/server_CwOJRIjy.mjs';
import 'piccolore';
import { $ as $$Base } from '../chunks/Base_zCXmWhgI.mjs';
/* empty css                                 */
export { renderers } from '../renderers.mjs';

const $$About = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "About", "description": "What Seeing the Unseen is and how the map metaphor works.", "data-astro-cid-kh7btl4r": true }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<article class="about" data-astro-cid-kh7btl4r> <h1 data-astro-cid-kh7btl4r>About</h1> <p data-astro-cid-kh7btl4r>This project is built like a hidden map made of stories. Each piece of content is a waypoint, a question, or a strategy inside a larger landscape.</p> <p data-astro-cid-kh7btl4r>Instead of a linear library, the site lets you move through levels and zones. The map, graph, and library are three ways to explore the same world.</p> <p data-astro-cid-kh7btl4r>The metaphor is simple: ideas travel through corridors, and the site is a space where connections become visible, not just listed.</p> </article> ` })} `;
}, "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/about.astro", void 0);

const $$file = "/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/about.astro";
const $$url = "/about";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$About,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
