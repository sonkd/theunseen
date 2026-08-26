// Astro integration: (re)build public/graph/graph.json on dev server start and
// whenever content/stuff changes, so `npm run dev` never serves a stale graph.
import { exec } from 'node:child_process';

export default function graphDevIntegration() {
  return {
    name: 'graph-dev-integration',
    hooks: {
      'astro:config:setup': ({ command, addWatchFile, logger }) => {
        if (command !== 'dev') return;
        const rebuild = () => {
          exec('node scripts/build-graph.mjs', (error, stdout, stderr) => {
            if (error) logger.error(`graph:build failed: ${stderr || error.message}`);
            else logger.info(stdout.trim());
          });
        };
        rebuild();
        addWatchFile(new URL('../content/stuff/', import.meta.url));
      },
      'astro:server:setup': ({ server, logger }) => {
        server.watcher.on('all', (_event, path) => {
          if (!path.includes('/content/stuff/')) return;
          exec('node scripts/build-graph.mjs', (error, stdout, stderr) => {
            if (error) logger.error(`graph:build failed: ${stderr || error.message}`);
            else logger.info(stdout.trim());
          });
        });
      },
    },
  };
}
