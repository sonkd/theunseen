[![Netlify Status](https://api.netlify.com/api/v1/badges/28704be5-e764-4674-ba56-032d388220dc/deploy-status)](https://app.netlify.com/sites/theunseen/deploys)

---

# The Stuff Unseen
> The seen is the changing, the unseen is the unchanging. Plato.

### 1. Install Postcss and Tailwind

```bash
$ npm install tailwindcss @tailwindcss/typography cssnano postcss postcss-import autoprefixer --save-dev
```

Only postcss:
```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

#### Import Tailwind CSS**
Add an @import to your CSS file that imports Tailwind CSS.
```css
@import "tailwindcss";
```

#### Start your build process
Run your build process with npm run dev or whatever command is configured in your package.json file.
```bash
npm run dev
```


### 2. Build Jekyll site
To build and serve your Jekyll site locally with live reload, use the following command:

```bash
bundle exec jekyll serve --livereload
```

### 3. Sync stuff from Notion

```bash
python3 theunseen_notion_sync.py
```