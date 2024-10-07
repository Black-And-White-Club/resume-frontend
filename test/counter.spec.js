import { render, screen, waitFor } from '@testing-library/preact';
import Counter from 'src/components/common/Counter';
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mocking fetch before tests
beforeEach(() => {
  vi.spyOn(global, 'fetch').mockImplementation((url) => {
    if (url === `${import.meta.env.PUBLIC_API_URL}/api/count`) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ visits: 42 }),
      });
    }
    return Promise.reject(new Error('Unknown endpoint'));
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('Counter Component', () => {
  // Unit Test: Verifying initial rendering
  test('renders initial visit count as 0', () => {
    render(<Counter />);
    expect(screen.getByText(/You are visitor number/i)).toBeInTheDocument();
    expect(screen.getByText(/0/i)).toBeInTheDocument();
  });

  // Component Test: Verifying data fetching and display
  test('fetches visit count and displays it', async () => {
    render(<Counter />);
    await waitFor(() => {
      expect(screen.getByText(/You are visitor number/i)).toBeInTheDocument();
      expect(screen.getByText(/42/i)).toBeInTheDocument();
    });
  });

  // Component Test: Verifying error handling
  test('handles fetch error gracefully', async () => {
    global.fetch.mockImplementationOnce(() => Promise.reject(new Error('Fetch failed')));

    render(<Counter />);
    await waitFor(() => {
      expect(screen.getByText(/You are visitor number/i)).toBeInTheDocument();
      expect(screen.getByText(/0/i)).toBeInTheDocument();
    });
  });
});
