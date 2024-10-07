/// <reference types="vitest" />
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    globals: true, // Enables globals like describe, it, expect
    environment: 'jsdom', // Use jsdom to simulate a browser environment
    // setupFiles: './vitest.setup.js', // Optional setup file for additional configurations
  },
});
