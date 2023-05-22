import React from 'react';
import "./User.css";
import ResponsiveMessage from '../../component/ResponsiveMessage'

import axios from 'axios';
import { useState, useEffect } from 'react';

function User() {

  const [enCours, setEnCours] = useState([]);
  const [isLoadingEnCours, setIsLoadingEnCours] = useState(true);

  const [terminer, setTerminer] = useState([]);
  const [isLoadingTerminer, setIsLoadingTerminer] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
        if (isLoadingEnCours) {
          axios.get("http://127.0.0.1:5000/...").then(res => {
            setEnCours(res.data);
            setIsLoadingEnCours(false);
          })
        }
        if (isLoadingTerminer) {
            axios.get("http://127.0.0.1:5000/...").then(res => {
                setTerminer(res.data);
                setIsLoadingTerminer(false);
            })
        }

    };

    fetchData();
  }, []);

  return (
    <>
      <ResponsiveMessage />

      <div className='User Page'>
        <div className='title'>
          <div className="the">THE</div>  
          <div className="french">FRENCH</div> 
          <div className = "flavor">FLAVOR</div>
        </div>

        <div className="content">
          <div className='title-command'>MES COMMANDES</div>

          <div className='container-ligne'>
            <div className="sub-title">En cours</div>

            <div className="container-command">
              {isLoadingEnCours ?
                <div>Chargement en cours...</div>
                :
                Object.keys(enCours).map((index, mapIndex) => (
                  <div className="ligne">
                    <div className='num-command'>{index}</div>
                    <div className='date'>Le {enCours[index].date}</div>
                    <div className="total">Total : {enCours[index].prix} €</div>
                    <div className="etat">Etat : {enCours[index].status}</div>
                  </div>
                ))
              }
            </div>
          </div>

          <div className='container-ligne'>
            <div className="sub-title">Terminer</div>

            <div className="container-command">
              {isLoadingTerminer ?
                <div>Chargement en cours...</div>
                :
                Object.keys(terminer).map((index, mapIndex) => (
                  <div className="ligne">
                    <div className='num-command'>{index}</div>
                    <div className='date'>Le {terminer[index].date}</div>
                    <div className="total">Total : {terminer[index].prix} €</div>
                    <div className="etat">Etat : {terminer[index].status}</div>
                  </div>
                ))
              }
            </div>
          </div>
        </div>

      </div>
    </>
  )
}

export default User
