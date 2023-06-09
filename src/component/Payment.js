import React from 'react';
import "./Payment.css";
import { Link } from 'react-router-dom';
import ResponsiveMessage from './ResponsiveMessage';

import axios from 'axios';
import { useState, useEffect } from 'react';

function Payment() {const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

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

      <div className='Payment Page'>
        <div className='title'>
          <div className="the">THE</div>  
          <div className="french">FRENCH</div> 
          <div className = "flavor">FLAVOR</div>
        </div>

        <div className="content">
          <div className='title-paiement'>PAIEMENT</div>

          <div className="payment-container">
            <div className="ligne courte">
              <div className="texte">Nom</div>
              <input type="text" id="name" name="name" placeholder="XXXXXXXXX" required></input>
            </div>

            <div className="ligne courte">
              <div className="texte">Numéro de carte</div>
              <input type="text" id="cb-number" name="cb-number" placeholder="0000 0000 0000 0000" required></input>
            </div>

            <div className="ligne-longue">
              <div className="ligne longue">
                <div className="texte">Date d'expiration</div>
                <input type="text" id="date" name="date" placeholder="MM/AA" minlength="5" maxlength="5" required></input>
              </div>
              <div className="ligne longue">
                <div className="texte">Code de sécurité</div>
                <input type="text" id="cvc" name="cvc" placeholder="000" minlength="5" maxlength="5" required></input>
              </div>
            </div>
          </div>

          <div className="ligne-total">
            <div className="command-info">
              <div className='total'>Total : {isLoading ? "load ..." : data.Total} €</div>
            </div>
            <div className="button-container">
              <Link to="/panier">Annuler</Link>
              <Link to="/paymentsuccess">Payer</Link>
            </div>
          </div>

          <div className="error">Erreur info</div>

        </div>
          
      </div>
    </>
  )
}

export default Payment