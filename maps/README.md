# Maps (Phase 2)

4 map chính + 1 map kết, vẽ bằng [Tiled](https://www.mapeditor.org/), export JSON:

1. `imagining.json` — level 1
2. `belief.json` — level 2
3. `thinking.json` — level 3
4. `knowledge.json` — level 4
5. `sun.json` — The Good: màn tổng kết, graph view, không chứa stuff

Engine: Kaplay (island `client:only` trong src/pages/index.astro). Stuff đặt theo `map_position` trong frontmatter; thiếu thì auto-place khi build.
