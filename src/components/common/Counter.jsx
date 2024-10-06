// Counter.jsx
import { useEffect, useState } from 'preact/hooks';
import { PUBLIC_API_URL } from 'astro:env/client';

const Counter = () => {
  // Declare count using useState hook
  const [count, setCount] = useState(0);

  // Function to fetch the visit count from the API
  const fetchVisitCount = async () => {
    try {
      console.log('PUBLIC_API_URL:', PUBLIC_API_URL);
      const origin = window.location.origin;

      // Create a Headers object and set the Origin header
      const headers = new Headers();
      headers.set('Origin', origin);
      const response = await fetch(`${PUBLIC_API_URL}/api/count`, {
        headers: headers,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setCount(data.visits); // Update count with the fetched visit count
      console.log('API Response:', data);
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
        This page has been visited <span className="font-bold">{count}</span> times.
      </p>
    </div>
  );
};

export default Counter;
