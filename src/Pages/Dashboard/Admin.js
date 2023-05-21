import React from 'react'
import "./Admin.css";
import Couronne from "../../images/couronne.webp"

function Admin() {
  return (
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
          <div className="ligne">
              <div className="command-info">
                <div className='id-command'>Id : xxxx</div>
                <div className='date'>Etat : A remettre au relais</div>
              </div>
              <div className="button-container">
                <button>Préparé</button>
                <button>Suprimer</button>
              </div>
            </div>

            <div className="ligne">
              <div className="command-info">
                <div className='id-command'>Id : xxxx</div>
                <div className='date'>Etat : A préparer</div>
              </div>
              <div className="button-container">
                <button>Préparé</button>
                <button>Suprimer</button>
              </div>
            </div>
          </div>
        </div>

        <div className='container-ligne'>
          <div className="sub-title">Gestion utilisateurs</div>

          <div className="container-command">
          <div className="ligne">
              <div className="command-info">
                <div className='id-user'>Id : xxxx</div>
              </div>
              <div className="button-container">
                <button>Rendre Admin</button>
                <button>Suprimer</button>
              </div>
            </div>

            <div className="ligne">
              <div className="command-info">
                <div className='id-user'>Id : xxxx</div>
                <img alt="" src={Couronne} />
              </div>
              <div className="button-container">
                <button>Rendre User</button>
                <button>Suprimer</button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}

export default Admin