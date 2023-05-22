import React from 'react';
import "./User.css";
import ResponsiveMessage from '../../component/ResponsiveMessage'

function User() {
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
              <div className="ligne">
                <div className='num-command'>1</div>
                <div className='date'>Le xx/xx/xxx</div>
                <div className="nombre-articles">Nombre articles : x</div>
                <div className="total">Total : x euros</div>
                <div className="etat">Etat : En cours de livraison</div>
              </div>

              <div className="ligne">
                <div className='num-command'>2</div>
                <div className='date'>Le xx/xx/xxx</div>
                <div className="nombre-articles">Nombre articles : x</div>
                <div className="total">Total : x euros</div>
                <div className="etat">Etat : En cours de livraison</div>
              </div>
            </div>
          </div>

          <div className='container-ligne'>
            <div className="sub-title">Terminer</div>

            <div className="container-command">
              <div className="ligne">
                <div className='num-command'>3</div>
                <div className='date'>Le xx/xx/xxx</div>
                <div className="nombre-articles">Nombre articles : x</div>
                <div className="total">Total : x euros</div>
                <div className="etat">Etat : En cours de livraison</div>
              </div>

              <div className="ligne">
                <div className='num-command'>4</div>
                <div className='date'>Le xx/xx/xxx</div>
                <div className="nombre-articles">Nombre articles : x</div>
                <div className="total">Total : x euros</div>
                <div className="etat">Etat : En cours de livraison</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </>
  )
}

export default User