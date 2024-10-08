import { render, screen, waitFor } from '@testing-library/preact';
import Counter from 'src/components/common/Counter';
import { vi, expect, test } from 'vitest';

describe('Counter Component', () => {
  beforeEach(() => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ visits: 42 }),
      });
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test('renders initial visit count as loading', () => {
    render(<Counter />);
    const countValueElement = screen.getByTestId('count-value');
    expect(countValueElement.textContent).toBe('...');
  });

  test('fetches visit count 42 and displays it', async () => {
    render(<Counter />);
    const countElement = await screen.findByText('You are visitor number 42! Hi there!');
    expect(countElement).toBeInTheDocument();
  });

  test('handles fetch error gracefully', async () => {
    global.fetch.mockImplementationOnce(() => Promise.reject(new Error('Fetch failed')));
    render(<Counter />);

    // Wait for the potential error message to appear
    await waitFor(() => {
      // Assert that the specific error message is displayed
      expect(screen.getByText('Failed to fetch visit count')).toBeInTheDocument();

      // Optionally assert that the count is not displayed, or any other relevant behavior
      // For instance:
      // expect(screen.queryByText('You are visitor number 42! Hi there!')).not.toBeInTheDocument();
    });
  });
});
