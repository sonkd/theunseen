import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import graphDevIntegration from './scripts/graph-dev-integration.mjs';

export default defineConfig({
  site: 'https://theunseen.example.com',
  integrations: [mdx(), graphDevIntegration()],
});
