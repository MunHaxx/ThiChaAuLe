import React from 'react'
import "./Admin.css";
import Couronne from "../../images/couronne.webp"
import ResponsiveMessage from '../../component/ResponsiveMessage'

import axios from 'axios';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Admin() {
  const navigate = useNavigate();

  function suppression(number) {
    navigate('/suppr_cmd/' + number);
    window.location.reload();
  }

  function terminerCommand(number) {
    navigate('/terminer_cmd/' + number);
    window.location.reload();
  }

  function enCoursCommand(number) {
    navigate('/encours_cmd/' + number);
    window.location.reload();
  }

  function switchRole(user, role) {
    if (role === "admin") {
      navigate('/admin_to_user/' + user);
      window.location.reload();
    } else {
      navigate('/user_to_admin/' + user);
      window.location.reload();
    }
    
  }

  function deleteUser(user) {
    navigate('/delete_user/' + user);
    window.location.reload();
    
  }

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
                console.log(res.data);
                console.log(isLoadingEnCours);
            })
        }
        if (isLoadingTerminer) {
            axios.get("http://127.0.0.1:5000/list_cmd_term").then(res => {
                setTerminer(res.data);
                setIsLoadingTerminer(false);
                console.log(res.data);
                console.log(isLoadingTerminer);
            })
        }
        if (isLoadingUsers) {
            axios.get("http://127.0.0.1:5000/list_users").then(res => {
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
              {isLoadingEnCours ?
                <div>Chargement en cours...</div>
                :
                (Object.keys(enCours).length === 0) ?
                  <div>Il n'y a pas de commande en cours</div> // Ou tout autre rendu que vous souhaitez pour indiquer que les données sont vides
                :
                  Object.keys(enCours).map((index, mapIndex) => (
                    <div className="ligne">
                      <div className="command-info">
                        <div className='id-command'>Id : {index}</div>
                        <div className='date'>Etat : {enCours[index].status}</div>
                      </div>
                      <div className="button-container">
                        <button onClick={() => terminerCommand(index)}>Terminé</button>
                        <button onClick={() => suppression(index)}>Supprimer</button>
                      </div>
                    </div>
                ))
              }
              {isLoadingTerminer ?
                <div>Chargement en cours...</div>
                :
                (Object.keys(terminer).length === 0) ?
                  <div>Il n'y a pas de commande terminer</div> // Ou tout autre rendu que vous souhaitez pour indiquer que les données sont vides
                :
                  Object.keys(terminer).map((index, mapIndex) => (
                    <div className="ligne">
                      <div className="command-info">
                        <div className='id-command'>Id : {index}</div>
                        <div className='date'>Etat : {terminer[index].status}</div>
                      </div>
                      <div className="button-container">
                        <button onClick={() => enCoursCommand(index)}>En cours</button>
                        <button onClick={() => suppression(index)}>Supprimer</button>
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
                        <button onClick={() => switchRole(index, role)}>Rendre {role === "admin" ? "user" : "admin"}</button>
                        <button onClick={() => deleteUser(index)}>Suprimer</button>
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