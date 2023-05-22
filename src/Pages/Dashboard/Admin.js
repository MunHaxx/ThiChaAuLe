import React from 'react'
import "./Admin.css";
import Couronne from "../../images/couronne.webp"
import ResponsiveMessage from '../../component/ResponsiveMessage'

import axios from 'axios';
import { useState, useEffect } from 'react';

function Admin() {
  const [enCours, setEnCours] = useState([]);
  const [isLoadingEnCours, setIsLoadingEnCours] = useState(true);

  const [terminer, setTerminer] = useState([]);
  const [isLoadingTerminer, setIsLoadingTerminer] = useState(true);

  const [users, setUsers] = useState([]);
  const [isLoadingUsers, setIsLoadingUsers] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
        if (isLoadingEnCours) {
            axios.get("http://127.0.0.1:5000/list_cmd_encours").then(res => {
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
        if (isLoadingUsers) {
            axios.get("http://127.0.0.1:5000/...").then(res => {
                setUsers(res.data);
                setIsLoadingUsers(false);
            })
        }


      //Est ce qu'on a un truc aussi pour les stats
    };

    fetchData();
  }, []);

  return (
    <>
      <ResponsiveMessage />

      <div className='Admin Page'>
        <div className='title'>
          <div className="the">THE</div>  
          <div className="french">FRENCH</div> 
          <div className = "flavor">FLAVOR</div>
        </div>

        <div className="container-stats">
          <div className="title-stats">STATISTIQUES</div>
          <div className="box-sells">30 BOXS VENDUES</div>
          <div className="title-stats">150 USERS</div>
        </div>

        <div className="content">
          <div className='title-admin'>ADMIN</div>

          <div className='container-ligne'>
            <div className="sub-title">Commandes</div>

            <div className="container-command">
              {setIsLoadingEnCours ?
                <div>Chargement en cours...</div>
                :
                Object.keys(enCours).map((index, mapIndex) => (
                  <div className="ligne">
                    <div className="command-info">
                      <div className='id-command'>Id : {index}</div>
                      <div className='date'>Etat : {enCours[index].status}</div>
                    </div>
                    <div className="button-container">
                      <button>Préparé</button>
                      <button>Suprimer</button>
                    </div>
                  </div>
                ))
              }
              {setIsLoadingTerminer ?
                <div>Chargement en cours...</div>
                :
                Object.keys(terminer).map((index, mapIndex) => (
                  <div className="ligne">
                    <div className="command-info">
                      <div className='id-command'>Id : {index}</div>
                      <div className='date'>Etat : {terminer[index].status}</div>
                    </div>
                    <div className="button-container">
                      <button>Préparé</button>
                      <button>Suprimer</button>
                    </div>
                  </div>
                ))
              }
            </div>
          </div>

          <div className='container-ligne'>
            <div className="sub-title">Gestion utilisateurs</div>

            <div className="container-command">
              {isLoadingUsers ?
                <div>Chargement en cours...</div>
                :
                Object.keys(users).map((role, mapIndex) => (
                  Object.keys(users[role]).map((index, newMapIndex) => (
                    <div className="ligne">
                      <div className="command-info">
                        <div className='id-user'>Id : {users[role][index].id}</div>
                        {role === "admin" ?
                          <img alt="" src={Couronne} />
                          :
                          undefined
                        }
                      </div>
                      <div className="button-container">
                        <button>Rendre {role === "admin" ? "user" : "admin"}</button>
                        <button>Suprimer</button>
                      </div>
                    </div>
                  )) 
                ))
              }
              {/* Fin container command */}
            </div>
            {/* Fin container ligne */}
          </div>
          {/* Fin content */}
        </div>
      </div>
    </>
  )
}

export default Admin