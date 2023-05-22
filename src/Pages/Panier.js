import React from 'react'
import "./Panier.css"
import ResponsiveMessage from '../component/ResponsiveMessage'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';

import axios from 'axios';
import { useState, useEffect } from 'react';
function Panier() {
  const navigate = useNavigate();

  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  function ajout(product) {
    navigate('/Cart/AddCart/' + product);
    window.location.reload();
  }
  function suppression(product) {
    navigate('/DelCart/' + product);
    window.location.reload();
  }

  useEffect(() => {
    const fetchData = async () => {
        if (isLoading) {
          axios.get("http://127.0.0.1:5000/list_panier").then(res => {
            setData(res.data);
            setIsLoading(false);
          })
        }
    };

    fetchData();
  }, []);

  return (
    <>
      <ResponsiveMessage />

      <div className='Panier Page'>
        <div className='title'>
          <div className="the">THE</div>  
          <div className="french">FRENCH</div> 
          <div className = "flavor">FLAVOR</div>
        </div>


        <div className="content">
          <div className='title-admin'>PANIER</div>


          <div className="container-command">
            {isLoading ? 
              <div>Chargement en cours...</div>
              :
              Object.keys(data.content).map((index, mapIndex) => (
                <div className="ligne">
                  <div className="command-info">
                    <div className='id-product'>Produit : {index}</div>
                    <div className='quantity'>Quantité : {data.content[index]}</div>
                  </div>
                  <div className="button-container">
                    <button onClick={() => ajout(index)}>Ajouter</button>
                    <button onClick={() => suppression(index)}>Suprimer</button>
                  </div>
                </div>
              ))
            }
          </div>

          <div className="ligne-total">
            <div className="command-info">
              <div className='total'>Total : {isLoading ? "load ..." : data.Total} €</div>
            </div>
            <div className="button-container">
              <Link to="/payment">Payer</Link>
            </div>
          </div>
        </div>

      </div>
    </>
  )
}

export default Panier