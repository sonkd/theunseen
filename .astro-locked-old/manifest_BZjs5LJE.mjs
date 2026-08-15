import '@astrojs/internal-helpers/path';
import '@astrojs/internal-helpers/remote';
import 'piccolore';
import { N as NOOP_MIDDLEWARE_HEADER, q as decodeKey } from './chunks/astro/server_CwOJRIjy.mjs';
import 'clsx';
import 'es-module-lexer';
import 'html-escaper';

const NOOP_MIDDLEWARE_FN = async (_ctx, next) => {
  const response = await next();
  response.headers.set(NOOP_MIDDLEWARE_HEADER, "true");
  return response;
};

const codeToStatusMap = {
  // Implemented from IANA HTTP Status Code Registry
  // https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  PAYMENT_REQUIRED: 402,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  METHOD_NOT_ALLOWED: 405,
  NOT_ACCEPTABLE: 406,
  PROXY_AUTHENTICATION_REQUIRED: 407,
  REQUEST_TIMEOUT: 408,
  CONFLICT: 409,
  GONE: 410,
  LENGTH_REQUIRED: 411,
  PRECONDITION_FAILED: 412,
  CONTENT_TOO_LARGE: 413,
  URI_TOO_LONG: 414,
  UNSUPPORTED_MEDIA_TYPE: 415,
  RANGE_NOT_SATISFIABLE: 416,
  EXPECTATION_FAILED: 417,
  MISDIRECTED_REQUEST: 421,
  UNPROCESSABLE_CONTENT: 422,
  LOCKED: 423,
  FAILED_DEPENDENCY: 424,
  TOO_EARLY: 425,
  UPGRADE_REQUIRED: 426,
  PRECONDITION_REQUIRED: 428,
  TOO_MANY_REQUESTS: 429,
  REQUEST_HEADER_FIELDS_TOO_LARGE: 431,
  UNAVAILABLE_FOR_LEGAL_REASONS: 451,
  INTERNAL_SERVER_ERROR: 500,
  NOT_IMPLEMENTED: 501,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504,
  HTTP_VERSION_NOT_SUPPORTED: 505,
  VARIANT_ALSO_NEGOTIATES: 506,
  INSUFFICIENT_STORAGE: 507,
  LOOP_DETECTED: 508,
  NETWORK_AUTHENTICATION_REQUIRED: 511
};
Object.entries(codeToStatusMap).reduce(
  // reverse the key-value pairs
  (acc, [key, value]) => ({ ...acc, [value]: key }),
  {}
);

function sanitizeParams(params) {
  return Object.fromEntries(
    Object.entries(params).map(([key, value]) => {
      if (typeof value === "string") {
        return [key, value.normalize().replace(/#/g, "%23").replace(/\?/g, "%3F")];
      }
      return [key, value];
    })
  );
}
function getParameter(part, params) {
  if (part.spread) {
    return params[part.content.slice(3)] || "";
  }
  if (part.dynamic) {
    if (!params[part.content]) {
      throw new TypeError(`Missing parameter: ${part.content}`);
    }
    return params[part.content];
  }
  return part.content.normalize().replace(/\?/g, "%3F").replace(/#/g, "%23").replace(/%5B/g, "[").replace(/%5D/g, "]");
}
function getSegment(segment, params) {
  const segmentPath = segment.map((part) => getParameter(part, params)).join("");
  return segmentPath ? "/" + segmentPath : "";
}
function getRouteGenerator(segments, addTrailingSlash) {
  return (params) => {
    const sanitizedParams = sanitizeParams(params);
    let trailing = "";
    if (addTrailingSlash === "always" && segments.length) {
      trailing = "/";
    }
    const path = segments.map((segment) => getSegment(segment, sanitizedParams)).join("") + trailing;
    return path || "/";
  };
}

function deserializeRouteData(rawRouteData) {
  return {
    route: rawRouteData.route,
    type: rawRouteData.type,
    pattern: new RegExp(rawRouteData.pattern),
    params: rawRouteData.params,
    component: rawRouteData.component,
    generate: getRouteGenerator(rawRouteData.segments, rawRouteData._meta.trailingSlash),
    pathname: rawRouteData.pathname || void 0,
    segments: rawRouteData.segments,
    prerender: rawRouteData.prerender,
    redirect: rawRouteData.redirect,
    redirectRoute: rawRouteData.redirectRoute ? deserializeRouteData(rawRouteData.redirectRoute) : void 0,
    fallbackRoutes: rawRouteData.fallbackRoutes.map((fallback) => {
      return deserializeRouteData(fallback);
    }),
    isIndex: rawRouteData.isIndex,
    origin: rawRouteData.origin
  };
}

function deserializeManifest(serializedManifest) {
  const routes = [];
  for (const serializedRoute of serializedManifest.routes) {
    routes.push({
      ...serializedRoute,
      routeData: deserializeRouteData(serializedRoute.routeData)
    });
    const route = serializedRoute;
    route.routeData = deserializeRouteData(serializedRoute.routeData);
  }
  const assets = new Set(serializedManifest.assets);
  const componentMetadata = new Map(serializedManifest.componentMetadata);
  const inlinedScripts = new Map(serializedManifest.inlinedScripts);
  const clientDirectives = new Map(serializedManifest.clientDirectives);
  const serverIslandNameMap = new Map(serializedManifest.serverIslandNameMap);
  const key = decodeKey(serializedManifest.key);
  return {
    // in case user middleware exists, this no-op middleware will be reassigned (see plugin-ssr.ts)
    middleware() {
      return { onRequest: NOOP_MIDDLEWARE_FN };
    },
    ...serializedManifest,
    assets,
    componentMetadata,
    inlinedScripts,
    clientDirectives,
    routes,
    serverIslandNameMap,
    key
  };
}

const manifest = deserializeManifest({"hrefRoot":"file:///sessions/funny-exciting-shannon/mnt/theunseen/","cacheDir":"file:///sessions/funny-exciting-shannon/mnt/theunseen/node_modules/.astro/","outDir":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/","srcDir":"file:///sessions/funny-exciting-shannon/mnt/theunseen/src/","publicDir":"file:///sessions/funny-exciting-shannon/mnt/theunseen/public/","buildClientDir":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/client/","buildServerDir":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/server/","adapterName":"","routes":[{"file":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/about/index.html","links":[],"scripts":[],"styles":[{"type":"inline","content":":root{--bg: #fbfaf7;--surface: #f6f3ea;--text: #3a372f;--ink: #111114;--muted: #8a8577;--muted-2: #9a958a;--border: #d9d4c6;--border-soft: #eee9dc;--flame: #f0a343;--accent: #c9563c;--dark-bg: #0a0910;--dark-bg-2: #141310;--font-pixel: \"Press Start 2P\", monospace;--font-mono: ui-monospace, Menlo, monospace}*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 system-ui,sans-serif;display:flex;flex-direction:column;min-height:100vh}a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}main{flex:1 1 auto;max-width:880px;margin:0 auto;padding:2rem 1rem 4rem;width:100%}main.full-bleed{max-width:none;margin:0;padding:0;display:flex;overflow:hidden}header.site{flex:none;display:flex;gap:1rem;flex-wrap:wrap;align-items:center;padding:0 20px;height:56px;background:var(--bg);border-bottom:2px solid var(--ink);position:relative;z-index:10}header.site a{text-decoration:none;color:var(--text);font-family:var(--font-pixel);font-size:9px;letter-spacing:.1em}header.site a.brand{color:var(--ink);font-weight:700;font-size:16px;letter-spacing:-.01em;font-family:system-ui,sans-serif}.search-shell{display:flex;flex-direction:column;gap:.5rem;flex:1 1 270px;min-width:220px;max-width:340px}.search-fallback{width:100%}.search-fallback input,[data-pagefind-ui] input{width:100%;height:32px;padding:0 12px;border:2px solid var(--ink);border-radius:7px;background:#fff;color:var(--ink);outline:none;font-size:11px;letter-spacing:.08em}.search-fallback input::placeholder,[data-pagefind-ui] input::placeholder{color:var(--muted)}[data-pagefind-ui]{width:100%}.site-nav{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}\n.about[data-astro-cid-kh7btl4r] p[data-astro-cid-kh7btl4r]{color:var(--text)}\n"}],"routeData":{"route":"/about","isIndex":false,"type":"page","pattern":"^\\/about\\/?$","segments":[[{"content":"about","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/about.astro","pathname":"/about","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/graph/index.html","links":[],"scripts":[],"styles":[{"type":"inline","content":":root{--bg: #fbfaf7;--surface: #f6f3ea;--text: #3a372f;--ink: #111114;--muted: #8a8577;--muted-2: #9a958a;--border: #d9d4c6;--border-soft: #eee9dc;--flame: #f0a343;--accent: #c9563c;--dark-bg: #0a0910;--dark-bg-2: #141310;--font-pixel: \"Press Start 2P\", monospace;--font-mono: ui-monospace, Menlo, monospace}*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 system-ui,sans-serif;display:flex;flex-direction:column;min-height:100vh}a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}main{flex:1 1 auto;max-width:880px;margin:0 auto;padding:2rem 1rem 4rem;width:100%}main.full-bleed{max-width:none;margin:0;padding:0;display:flex;overflow:hidden}header.site{flex:none;display:flex;gap:1rem;flex-wrap:wrap;align-items:center;padding:0 20px;height:56px;background:var(--bg);border-bottom:2px solid var(--ink);position:relative;z-index:10}header.site a{text-decoration:none;color:var(--text);font-family:var(--font-pixel);font-size:9px;letter-spacing:.1em}header.site a.brand{color:var(--ink);font-weight:700;font-size:16px;letter-spacing:-.01em;font-family:system-ui,sans-serif}.search-shell{display:flex;flex-direction:column;gap:.5rem;flex:1 1 270px;min-width:220px;max-width:340px}.search-fallback{width:100%}.search-fallback input,[data-pagefind-ui] input{width:100%;height:32px;padding:0 12px;border:2px solid var(--ink);border-radius:7px;background:#fff;color:var(--ink);outline:none;font-size:11px;letter-spacing:.08em}.search-fallback input::placeholder,[data-pagefind-ui] input::placeholder{color:var(--muted)}[data-pagefind-ui]{width:100%}.site-nav{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}\n"},{"type":"external","src":"/_astro/graph.CUI7AN6C.css"},{"type":"inline","content":".intro[data-astro-cid-oy34yelw]{margin-top:0;color:var(--muted)}.graph-container[data-astro-cid-oy34yelw]{width:100%;min-height:80vh;border:1px solid var(--border);border-radius:24px;background:radial-gradient(circle at top,rgba(240,163,67,.1),transparent 38%),var(--surface);overflow:hidden;position:relative}.graph-tooltip[data-astro-cid-oy34yelw]{position:absolute;pointer-events:none;background:var(--ink);color:#fff;border:2px solid #fff;border-radius:12px;padding:.6rem .85rem;font-family:var(--font-pixel);font-size:8px;z-index:10;white-space:nowrap;box-shadow:0 12px 40px #00000040}.graph-link[data-astro-cid-oy34yelw]{display:inline-block;margin-top:1.25rem;color:var(--flame);text-decoration:none}\n"}],"routeData":{"route":"/graph","isIndex":false,"type":"page","pattern":"^\\/graph\\/?$","segments":[[{"content":"graph","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/graph.astro","pathname":"/graph","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/library/index.html","links":[],"scripts":[],"styles":[{"type":"inline","content":":root{--bg: #fbfaf7;--surface: #f6f3ea;--text: #3a372f;--ink: #111114;--muted: #8a8577;--muted-2: #9a958a;--border: #d9d4c6;--border-soft: #eee9dc;--flame: #f0a343;--accent: #c9563c;--dark-bg: #0a0910;--dark-bg-2: #141310;--font-pixel: \"Press Start 2P\", monospace;--font-mono: ui-monospace, Menlo, monospace}*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 system-ui,sans-serif;display:flex;flex-direction:column;min-height:100vh}a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}main{flex:1 1 auto;max-width:880px;margin:0 auto;padding:2rem 1rem 4rem;width:100%}main.full-bleed{max-width:none;margin:0;padding:0;display:flex;overflow:hidden}header.site{flex:none;display:flex;gap:1rem;flex-wrap:wrap;align-items:center;padding:0 20px;height:56px;background:var(--bg);border-bottom:2px solid var(--ink);position:relative;z-index:10}header.site a{text-decoration:none;color:var(--text);font-family:var(--font-pixel);font-size:9px;letter-spacing:.1em}header.site a.brand{color:var(--ink);font-weight:700;font-size:16px;letter-spacing:-.01em;font-family:system-ui,sans-serif}.search-shell{display:flex;flex-direction:column;gap:.5rem;flex:1 1 270px;min-width:220px;max-width:340px}.search-fallback{width:100%}.search-fallback input,[data-pagefind-ui] input{width:100%;height:32px;padding:0 12px;border:2px solid var(--ink);border-radius:7px;background:#fff;color:var(--ink);outline:none;font-size:11px;letter-spacing:.08em}.search-fallback input::placeholder,[data-pagefind-ui] input::placeholder{color:var(--muted)}[data-pagefind-ui]{width:100%}.site-nav{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}\n"},{"type":"external","src":"/_astro/graph.CUI7AN6C.css"},{"type":"inline","content":".filters[data-astro-cid-hofbs6tv]{border:1px solid var(--border);background:var(--surface);padding:1rem 1.25rem;border-radius:18px;margin-bottom:1.5rem}.filter-header[data-astro-cid-hofbs6tv]{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;align-items:center}.filter-copy[data-astro-cid-hofbs6tv]{margin:.35rem 0 0;color:var(--muted)}.filter-group[data-astro-cid-hofbs6tv]{margin-top:1rem}.filter-label[data-astro-cid-hofbs6tv]{text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;color:var(--muted);margin-bottom:.4rem}.chips[data-astro-cid-hofbs6tv]{display:flex;flex-wrap:wrap;gap:.5rem}.chip[data-astro-cid-hofbs6tv]{appearance:none;border:1px solid var(--border);background:#fff;color:var(--text);border-radius:999px;padding:.55rem .85rem;cursor:pointer;transition:transform .15s ease,background .15s ease,border-color .15s ease}.chip[data-astro-cid-hofbs6tv]:hover{transform:translateY(-1px);border-color:var(--flame)}.chip[data-astro-cid-hofbs6tv].active{background:#f0a34326;border-color:var(--flame);color:var(--flame)}.clear-button[data-astro-cid-hofbs6tv]{margin-top:1rem;appearance:none;border:1px solid var(--border);background:transparent;color:var(--text);border-radius:999px;padding:.7rem 1rem;cursor:pointer}.clear-button[data-astro-cid-hofbs6tv]:hover{border-color:var(--flame);color:var(--flame)}.result-count[data-astro-cid-hofbs6tv]{color:var(--muted);font-size:.95rem}.grid[data-astro-cid-hofbs6tv]{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.75rem;margin:0}.grid[data-astro-cid-hofbs6tv] a[data-astro-cid-hofbs6tv]{text-decoration:none;color:var(--text);display:grid;grid-template-columns:auto 1fr;gap:.75rem;padding:.85rem 1rem;border:1px solid var(--border);border-radius:16px;align-items:center}.grid[data-astro-cid-hofbs6tv] a[data-astro-cid-hofbs6tv]:hover{border-color:var(--flame)}.card[data-astro-cid-hofbs6tv]{transition:opacity .2s ease,transform .2s ease}.card[data-astro-cid-hofbs6tv][hidden]{display:none!important}.icon[data-astro-cid-hofbs6tv]{color:var(--flame);font-size:1.1rem;line-height:1}.meta[data-astro-cid-hofbs6tv]{color:var(--muted);font-size:.85rem;display:block;grid-column:2}.pagination[data-astro-cid-hofbs6tv]{display:flex;align-items:center;justify-content:center;gap:.75rem;margin-top:2rem}.pagination[data-astro-cid-hofbs6tv].hidden{display:none}.page-nav[data-astro-cid-hofbs6tv]{appearance:none;border:1px solid var(--border);background:#fff;color:var(--text);border-radius:999px;padding:.55rem 1rem;cursor:pointer;font-size:.9rem}.page-nav[data-astro-cid-hofbs6tv]:hover:not(:disabled){border-color:var(--flame);color:var(--flame)}.page-nav[data-astro-cid-hofbs6tv]:disabled{opacity:.4;cursor:default}.page-numbers[data-astro-cid-hofbs6tv]{display:flex;gap:.35rem}.page-numbers[data-astro-cid-hofbs6tv] button[data-astro-cid-hofbs6tv]{appearance:none;border:1px solid var(--border);background:#fff;color:var(--text);border-radius:999px;width:2.2rem;height:2.2rem;cursor:pointer;font-size:.85rem}.page-numbers[data-astro-cid-hofbs6tv] button[data-astro-cid-hofbs6tv].active{background:var(--ink);color:#fff;border-color:var(--ink)}.page-numbers[data-astro-cid-hofbs6tv] button[data-astro-cid-hofbs6tv]:hover:not(.active){border-color:var(--flame);color:var(--flame)}\n"}],"routeData":{"route":"/library","isIndex":false,"type":"page","pattern":"^\\/library\\/?$","segments":[[{"content":"library","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/library.astro","pathname":"/library","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/index.html","links":[],"scripts":[],"styles":[{"type":"inline","content":":root{--bg: #fbfaf7;--surface: #f6f3ea;--text: #3a372f;--ink: #111114;--muted: #8a8577;--muted-2: #9a958a;--border: #d9d4c6;--border-soft: #eee9dc;--flame: #f0a343;--accent: #c9563c;--dark-bg: #0a0910;--dark-bg-2: #141310;--font-pixel: \"Press Start 2P\", monospace;--font-mono: ui-monospace, Menlo, monospace}*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 system-ui,sans-serif;display:flex;flex-direction:column;min-height:100vh}a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}main{flex:1 1 auto;max-width:880px;margin:0 auto;padding:2rem 1rem 4rem;width:100%}main.full-bleed{max-width:none;margin:0;padding:0;display:flex;overflow:hidden}header.site{flex:none;display:flex;gap:1rem;flex-wrap:wrap;align-items:center;padding:0 20px;height:56px;background:var(--bg);border-bottom:2px solid var(--ink);position:relative;z-index:10}header.site a{text-decoration:none;color:var(--text);font-family:var(--font-pixel);font-size:9px;letter-spacing:.1em}header.site a.brand{color:var(--ink);font-weight:700;font-size:16px;letter-spacing:-.01em;font-family:system-ui,sans-serif}.search-shell{display:flex;flex-direction:column;gap:.5rem;flex:1 1 270px;min-width:220px;max-width:340px}.search-fallback{width:100%}.search-fallback input,[data-pagefind-ui] input{width:100%;height:32px;padding:0 12px;border:2px solid var(--ink);border-radius:7px;background:#fff;color:var(--ink);outline:none;font-size:11px;letter-spacing:.08em}.search-fallback input::placeholder,[data-pagefind-ui] input::placeholder{color:var(--muted)}[data-pagefind-ui]{width:100%}.site-nav{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}\n"},{"type":"external","src":"/_astro/graph.CUI7AN6C.css"},{"type":"external","src":"/_astro/index.DFsLT5Kk.css"}],"routeData":{"route":"/","isIndex":true,"type":"page","pattern":"^\\/$","segments":[],"params":[],"component":"src/pages/index.astro","pathname":"/","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}}],"site":"https://theunseen.example.com","base":"/","trailingSlash":"ignore","compressHTML":true,"componentMetadata":[["\u0000astro:content",{"propagation":"in-tree","containsHead":false}],["/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/library.astro",{"propagation":"in-tree","containsHead":true}],["\u0000@astro-page:src/pages/library@_@astro",{"propagation":"in-tree","containsHead":false}],["/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/stuff/[slug].astro",{"propagation":"in-tree","containsHead":true}],["\u0000@astro-page:src/pages/stuff/[slug]@_@astro",{"propagation":"in-tree","containsHead":false}],["/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/about.astro",{"propagation":"none","containsHead":true}],["/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/graph.astro",{"propagation":"none","containsHead":true}],["/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/index.astro",{"propagation":"none","containsHead":true}]],"renderers":[],"clientDirectives":[["idle","(()=>{var l=(n,t)=>{let i=async()=>{await(await n())()},e=typeof t.value==\"object\"?t.value:void 0,s={timeout:e==null?void 0:e.timeout};\"requestIdleCallback\"in window?window.requestIdleCallback(i,s):setTimeout(i,s.timeout||200)};(self.Astro||(self.Astro={})).idle=l;window.dispatchEvent(new Event(\"astro:idle\"));})();"],["load","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).load=e;window.dispatchEvent(new Event(\"astro:load\"));})();"],["media","(()=>{var n=(a,t)=>{let i=async()=>{await(await a())()};if(t.value){let e=matchMedia(t.value);e.matches?i():e.addEventListener(\"change\",i,{once:!0})}};(self.Astro||(self.Astro={})).media=n;window.dispatchEvent(new Event(\"astro:media\"));})();"],["only","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).only=e;window.dispatchEvent(new Event(\"astro:only\"));})();"],["visible","(()=>{var a=(s,i,o)=>{let r=async()=>{await(await s())()},t=typeof i.value==\"object\"?i.value:void 0,c={rootMargin:t==null?void 0:t.rootMargin},n=new IntersectionObserver(e=>{for(let l of e)if(l.isIntersecting){n.disconnect(),r();break}},c);for(let e of o.children)n.observe(e)};(self.Astro||(self.Astro={})).visible=a;window.dispatchEvent(new Event(\"astro:visible\"));})();"]],"entryModules":{"\u0000@astro-page:src/pages/about@_@astro":"pages/about.astro.mjs","\u0000@astro-page:src/pages/graph@_@astro":"pages/graph.astro.mjs","\u0000@astro-page:src/pages/index@_@astro":"pages/index.astro.mjs","\u0000@astro-page:src/pages/library@_@astro":"pages/library.astro.mjs","\u0000@astro-page:src/pages/stuff-data/[slug].json@_@ts":"pages/stuff-data/_slug_.json.astro.mjs","\u0000@astro-page:src/pages/stuff/[slug]@_@astro":"pages/stuff/_slug_.astro.mjs","\u0000@astro-renderers":"renderers.mjs","\u0000noop-middleware":"_noop-middleware.mjs","\u0000virtual:astro:actions/noop-entrypoint":"noop-entrypoint.mjs","\u0000@astrojs-manifest":"manifest_BZjs5LJE.mjs","/sessions/funny-exciting-shannon/mnt/theunseen/.astro/content-assets.mjs":"chunks/content-assets_DleWbedO.mjs","/sessions/funny-exciting-shannon/mnt/theunseen/.astro/content-modules.mjs":"chunks/content-modules_Dz-S_Wwv.mjs","\u0000astro:data-layer-content":"chunks/_astro_data-layer-content_BiE-S2Q2.mjs","/sessions/funny-exciting-shannon/mnt/theunseen/node_modules/astro/dist/assets/services/sharp.js":"chunks/sharp_DTXwykK0.mjs","/sessions/funny-exciting-shannon/mnt/theunseen/src/components/FlipCard.astro?astro&type=script&index=0&lang.ts":"_astro/FlipCard.astro_astro_type_script_index_0_lang.WpWg-W0c.js","/sessions/funny-exciting-shannon/mnt/theunseen/src/components/map/MapCanvas.astro?astro&type=script&index=0&lang.ts":"_astro/MapCanvas.astro_astro_type_script_index_0_lang.BnlkcXbp.js","/sessions/funny-exciting-shannon/mnt/theunseen/src/components/map/StuffOverlay.astro?astro&type=script&index=0&lang.ts":"_astro/StuffOverlay.astro_astro_type_script_index_0_lang.DNCORV9z.js","/sessions/funny-exciting-shannon/mnt/theunseen/src/layouts/Base.astro?astro&type=script&index=0&lang.ts":"_astro/Base.astro_astro_type_script_index_0_lang.Z60JBQSu.js","/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/library.astro?astro&type=script&index=0&lang.ts":"_astro/library.astro_astro_type_script_index_0_lang.DFD10snM.js","astro:scripts/before-hydration.js":""},"inlinedScripts":[["/sessions/funny-exciting-shannon/mnt/theunseen/src/components/FlipCard.astro?astro&type=script&index=0&lang.ts","document.querySelectorAll(\".flip\").forEach(e=>e.addEventListener(\"click\",()=>e.classList.toggle(\"flipped\")));"],["/sessions/funny-exciting-shannon/mnt/theunseen/src/layouts/Base.astro?astro&type=script&index=0&lang.ts","document.addEventListener(\"DOMContentLoaded\",()=>{const n=document.querySelector(\"[data-pagefind-ui-wrapper]\");if(!n)return;const t=n.querySelector(\"[data-pagefind-ui]\"),r=n.querySelector(\".search-fallback\"),d=(i,a)=>new Promise((o,c)=>{const e=document.createElement(i);Object.entries(a).forEach(([l,s])=>e.setAttribute(l,s)),e.onload=()=>o(e),e.onerror=()=>c(new Error(`Failed to load ${a.href||a.src}`)),document.head.appendChild(e)});Promise.all([d(\"link\",{rel:\"stylesheet\",href:\"/pagefind/pagefind-ui.css\"}),d(\"script\",{src:\"/pagefind/pagefind-ui.js\",type:\"text/javascript\",async:\"false\"})]).then(()=>{typeof window.PagefindUI==\"function\"&&(new window.PagefindUI({element:t,bundlePath:\"/pagefind/\"}),t&&(t.hidden=!1),r&&(r.hidden=!0))}).catch(()=>{})});"],["/sessions/funny-exciting-shannon/mnt/theunseen/src/pages/library.astro?astro&type=script&index=0&lang.ts","const E=Array.from(document.querySelectorAll('[data-filter-type=\"category\"]')),S=Array.from(document.querySelectorAll('[data-filter-type=\"level\"]')),k=document.getElementById(\"clearFilters\"),M=document.getElementById(\"resultCount\"),P=document.getElementById(\"cardGrid\"),m=Array.from(document.querySelectorAll(\".card\")),N=Array.from(document.querySelectorAll(\".card a[data-slug]\")),$=document.getElementById(\"pagination\"),w=document.getElementById(\"pagePrev\"),L=document.getElementById(\"pageNext\"),h=document.getElementById(\"pageNumbers\"),g=Number(P.dataset.pageSize)||50,f=e=>e?e.split(\",\").map(t=>t.trim()).filter(Boolean):[],o=()=>{const e=new URLSearchParams(window.location.search),t=Math.max(1,parseInt(e.get(\"page\"),10)||1);return{categories:f(e.get(\"cat\")),levels:f(e.get(\"level\")),page:t}},y=(e,t)=>{e.forEach(a=>{const n=a.dataset.filterValue,c=t.includes(n);a.classList.toggle(\"active\",c),a.setAttribute(\"aria-pressed\",String(c))})},q=e=>{const t=new URLSearchParams;e.categories.length&&t.set(\"cat\",e.categories.join(\",\")),e.levels.length&&t.set(\"level\",e.levels.join(\",\")),e.page>1&&t.set(\"page\",String(e.page));const a=t.toString(),n=a?`${window.location.pathname}?${a}`:window.location.pathname;window.history.replaceState({},\"\",n)},K=(e,t)=>{h.innerHTML=\"\";for(let a=1;a<=t;a+=1){const n=document.createElement(\"button\");n.type=\"button\",n.textContent=String(a),a===e&&n.classList.add(\"active\"),n.addEventListener(\"click\",()=>r({...o(),page:a})),h.appendChild(n)}},r=e=>{y(E,e.categories),y(S,e.levels);const t=new Set(e.categories),a=new Set(e.levels),n=m.filter(l=>{const i=l.dataset.categories.split(\" \").filter(Boolean),d=l.dataset.level,C=t.size===0||i.some(I=>t.has(I)),A=a.size===0||a.has(d);return C&&A}),c=Math.max(1,Math.ceil(n.length/g)),s=Math.min(Math.max(1,e.page),c),p=(s-1)*g,B=p+g,b=new Set(n);let u=0;m.forEach(l=>{const i=n.indexOf(l),d=b.has(l)&&i>=p&&i<B;l.hidden=!d,d&&(u+=1)}),M.textContent=`Showing ${u} / ${n.length} cards (page ${s} of ${c})`,$.classList.toggle(\"hidden\",c<=1),w.disabled=s<=1,L.disabled=s>=c,K(s,c),q({...e,page:s})},v=(e,t)=>{const a=e.indexOf(t);a===-1?e.push(t):e.splice(a,1)},x=e=>{const t=e.currentTarget,a=t.dataset.filterType,n=t.dataset.filterValue,c=o();a===\"category\"&&v(c.categories,n),a===\"level\"&&v(c.levels,n),r({...c,page:1})};E.forEach(e=>e.addEventListener(\"click\",x));S.forEach(e=>e.addEventListener(\"click\",x));k.addEventListener(\"click\",()=>r({categories:[],levels:[],page:1}));w.addEventListener(\"click\",()=>r({...o(),page:o().page-1}));L.addEventListener(\"click\",()=>r({...o(),page:o().page+1}));N.forEach(e=>{e.addEventListener(\"click\",t=>{t.button!==0||t.metaKey||t.ctrlKey||t.shiftKey||t.altKey||(t.preventDefault(),window.dispatchEvent(new CustomEvent(\"stuff:open\",{detail:{slug:e.dataset.slug}})))})});r(o());"]],"assets":["/file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/about/index.html","/file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/graph/index.html","/file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/library/index.html","/file:///sessions/funny-exciting-shannon/mnt/outputs/dist-tmp/index.html"],"buildFormat":"directory","checkOrigin":false,"allowedDomains":[],"actionBodySizeLimit":1048576,"serverIslandNameMap":[],"key":"Hw3uhYFP4QEPqJeshdxFtWxwha3s2JstGyVottoArgI="});
if (manifest.sessionConfig) manifest.sessionConfig.driverModule = null;

export { manifest };
