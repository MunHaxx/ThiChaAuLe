// import React from 'react';
// import Formulaire from '../component/Formulaire';
// import axios from 'axios';
// import { useState, useEffect } from 'react';

// import { useNavigate } from 'react-router-dom';

// function Home() {
//   const navigate = useNavigate();

//   const [data, setData] = useState([]);
//   const [isLoading, setIsLoading] = useState(true);

//   function handleClick(product) {
//     navigate('/' + product);
//   }

//   useEffect(() => {
//     const fetchData = async () => {
//       const result = await axios.get('/api/data');
//       setData(result.data);
//       setIsLoading(false);
//     };
//     fetchData();
//   }, []);

//   if (isLoading) {
//     return <div>Chargement en cours...</div>;
//   }

//   return (
//     <div className="Home">
//         <div className="bonjour">Bonjour à tous</div>
//       <div className="containerBulbizarre">
//         <div className='carréDansLaxe'>
//           <img alt="" className="bulbizarre" src='https://www.pokepedia.fr/images/thumb/e/ef/Bulbizarre-RFVF.png/250px-Bulbizarre-RFVF.png' />
//         </div>

//         <div className="descriptionBulbizarre">
//           <h1>HELLO WORLD</h1>
//           <p>Bulbizarre est un pokémon de la première gen de type plante</p> 
//         </div>
//       </div>
//       <a href="https://eu.shop.battle.net/fr-fr">Battle net</a>
//       <button onClick={() => handleClick("hello")}>Changer l'URL</button>

//       <br />
//       <br />
//       <br />
//       <br />
    

//       {data.map((index) => (
//         <div></div>
//       ))}
//     </div>
//   );
// }

// export default Home;

import React from 'react';
import Formulaire from '../component/Formulaire';
import axios from 'axios';
import { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

function Home() {
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

export default Home;
