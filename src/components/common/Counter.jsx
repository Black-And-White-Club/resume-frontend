import { useEffect, useState } from 'preact/hooks';
import { PUBLIC_API_URL } from 'astro:env/client';

const Counter = () => {
  // Declare count using useState hook
  const [count, setCount] = useState(0);

  // Function to fetch the visit count from the API
  const fetchVisitCount = async () => {
    try {
      const response = await fetch(`${PUBLIC_API_URL}/api/count`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setCount(data.visits); // Update count with the fetched visit count
    } catch (error) {
      console.error('Error fetching visit count:', error);
      setCount(0); // Reset count to 0 on error
    }
  };

  // Fetch visit count on component mount
  useEffect(() => {
    fetchVisitCount();
  }, []); // Empty dependency array ensures this runs once on mount

  return (
    <div className="counter">
      <p id="visit-count">
        You are visitor number <span className="font-bold">{count}</span>! Hi there!
      </p>
    </div>
  );
};

export default Counter;
