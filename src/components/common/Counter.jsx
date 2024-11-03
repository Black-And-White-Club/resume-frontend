import { useEffect, useState } from 'preact/hooks';
// import { PUBLIC_API_URL } from 'astro:env/client';

const Counter = () => {
  const [count, setCount] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVisitCount = async () => {
      // local add ${PUBLIC_API_URL} in fron of /api/count
      const url = '/api/count';

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setCount(data.visits);
      } catch (error) {
        console.error('Error fetching visit count:', error);
        setError('Failed to fetch visit count');
      }
    };

    fetchVisitCount();
  }, []);

  return (
    <div className="counter">
      <p id="visit-count">
        You are visitor number <span data-testid="count-value">{count === null ? '...' : count}</span>! Hi there!
      </p>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Counter;
