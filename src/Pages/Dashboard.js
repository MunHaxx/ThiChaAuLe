import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';

function Dashboard() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get('/api/data');
      setData(result.data);
      setIsLoading(false);
    };
    fetchData();
  }, []);

  if (isLoading) {
    return <div>Chargement en cours...</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>

      <hr />

      <h1>Données de l'API Flask :</h1>
      {/* <p>{JSON.stringify(data)}</p> */}
      {data.map(item => (
        <div key={item.id}>
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;

