import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const stuff = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/stuff' }),
  schema: z.object({
    title: z.string(),
    front: z.string().min(1),
    back: z.string().min(1),
    level: z.number().int().min(1).max(5).default(2),
    icon: z.string().optional(),
    map_position: z.object({ x: z.number(), y: z.number() }).optional(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    links: z.array(z.string()).default([]),
    refs: z.array(z.string()).default([]),
    approaches: z.array(z.object({ title: z.string(), url: z.string() })).default([]),
    strategy: z.string().optional(),
    conundrum: z.string().optional(),
    published: z.boolean().default(true),
    image: z.string().nullish(),
  }),
});

const approaches = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/approaches' }),
  schema: z.object({
    title: z.string(),
    stuff: z.array(z.string()).default([]),
    published: z.boolean().default(true),
  }),
});

export const collections = { stuff, approaches };
