import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig, envField } from 'astro/config';
import dotenv from 'dotenv';
import { existsSync } from 'fs';

import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import partytown from '@astrojs/partytown';
import icon from 'astro-icon';
import compress from 'astro-compress';
import type { AstroIntegration } from 'astro';

import astrowind from './vendor/integration';
import { readingTimeRemarkPlugin, responsiveTablesRehypePlugin, lazyImagesRehypePlugin } from './src/utils/frontmatter';

import preact from '@astrojs/preact';

// Resolve the directory name (for using with aliases)
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Determine which environment file to load based on NODE_ENV
const envFile =
  process.env.NODE_ENV === 'docker' ? '.env.docker' : process.env.NODE_ENV === 'k8s' ? '.env.k8s' : '.env'; // Default to `.env` for local development

// Load the appropriate .env file if it exists
if (existsSync(envFile)) {
  dotenv.config({ path: envFile });
}

const hasExternalScripts = false;
const whenExternalScripts = (items: (() => AstroIntegration) | (() => AstroIntegration)[] = []) =>
  hasExternalScripts ? (Array.isArray(items) ? items.map((item) => item()) : [items()]) : [];

export default defineConfig({
  output: 'static',

  experimental: {
    env: {
      schema: {
        PUBLIC_API_URL: envField.string({
          context: 'client', // Expose it to the client
          access: 'public', // Make it public
          optional: true, // Ensure it's required
        }),
      },
    },
  },

  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap(),
    mdx(),
    icon({
      include: {
        tabler: ['*'],
        'flat-color-icons': [
          'template',
          'gallery',
          'approval',
          'document',
          'advertising',
          'currency-exchange',
          'voice-presentation',
          'business-contact',
          'database',
        ],
      },
    }),
    ...whenExternalScripts(() =>
      partytown({
        config: { forward: ['dataLayer.push'] },
      })
    ),
    compress({
      CSS: true,
      HTML: {
        'html-minifier-terser': {
          removeAttributeQuotes: false,
        },
      },
      Image: false,
      JavaScript: true,
      SVG: false,
      Logger: 1,
    }),
    astrowind({
      config: './src/config.yaml',
    }),
    preact(),
  ],

  image: {
    domains: ['cdn.pixabay.com'],
  },

  markdown: {
    remarkPlugins: [readingTimeRemarkPlugin],
    rehypePlugins: [responsiveTablesRehypePlugin, lazyImagesRehypePlugin],
  },

  vite: {
    resolve: {
      alias: {
        '~': path.resolve(__dirname, './src'),
      },
    },
  },
});
