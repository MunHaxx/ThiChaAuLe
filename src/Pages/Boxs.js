import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

function Boxs() {
  const navigate = useNavigate();

  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  function handleClick(product) {
    navigate('/AddCart/' + product);
  }


  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get('/api/data');
      setData(result.data.stocks);
      setIsLoading(false);
    };
    fetchData();
  }, []);

  if (isLoading) {
    return <div>Chargement en cours...</div>;
  }

  return (
    <div className="Home">
      {Object.keys(data).map((index) => (
        <div key={index}>
          <h2>{data[index].name}</h2>
          <p>Tarif: {data[index].tarifs} €</p>
          <button onClick={() => handleClick(index)}>Ajouter au panier</button>
        </div>
      ))}
    </div>
  );
}

export default Boxs;