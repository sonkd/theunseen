import { b as createAstro, c as createComponent, e as addAttribute, j as renderHead, k as renderSlot, f as renderScript, a as renderTemplate } from './astro/server_CwOJRIjy.mjs';
import 'piccolore';
import 'clsx';
/* empty css                         */

const $$Astro = createAstro("https://theunseen.example.com");
const $$Base = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Base;
  const { title, description = "Seeing the Unseen \u2014 flames of knowledge in Plato's cave.", fullBleed = false } = Astro2.props;
  return renderTemplate`<html lang="vi"> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description"${addAttribute(description, "content")}><title>${title} · Seeing the Unseen</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">${renderHead()}</head> <body> <header class="site"> <a class="brand" href="/">🔥 the unseen</a> <div class="search-shell" data-pagefind-ui-wrapper> <div data-pagefind-ui hidden></div> <form class="search-fallback" action="/library" method="get"> <input name="q" type="search" placeholder="SEARCH / TÌM KIẾM ⏎" aria-label="Search"> </form> </div> <div style="flex:1"></div> <a href="/library/">Library</a> <a href="/graph/">Graph</a> <a href="/about/">About</a> </header> <main${addAttribute(fullBleed ? "full-bleed" : "", "class")}>${renderSlot($$result, $$slots["default"])}</main> ${renderScript($$result, "/sessions/funny-charming-lovelace/mnt/theunseen/src/layouts/Base.astro?astro&type=script&index=0&lang.ts")} </body> </html>`;
}, "/sessions/funny-charming-lovelace/mnt/theunseen/src/layouts/Base.astro", void 0);

export { $$Base as $ };
