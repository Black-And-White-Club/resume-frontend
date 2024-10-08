// vitest.setup.ts
import { vi } from 'vitest';

// Mock the environment variable
vi.stubGlobal('import.meta', {
  env: {
    PUBLIC_API_URL: 'https://mock.api.url', // Use your mock base URL
  },
});
