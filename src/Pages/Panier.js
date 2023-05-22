import React from 'react'
import "./Panier.css"
import ResponsiveMessage from '../component/ResponsiveMessage'
import { Link } from 'react-router-dom'

function Panier() {
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
            <div className="ligne">
              <div className="command-info">
                <div className='id-product'>Produit : xxxx</div>
                <div className='quantity'>Quantité : xxxx</div>
                <div className='price'>Prix : xxx</div>
              </div>
              <div className="button-container">
                <button>Ajouter</button>
                <button>Suprimer</button>
              </div>
            </div>

            <div className="ligne">
              <div className="command-info">
                <div className='id-product'>Produit : xxxx</div>
                <div className='quantity'>Quantité : xxxx</div>
                <div className='price'>Prix : xxx</div>
              </div>
              <div className="button-container">
                <button>Ajouter</button>
                <button>Suprimer</button>
              </div>
            </div>
          </div>

          <div className="ligne-total">
            <div className="command-info">
              <div className='total'>Total : xxxx €</div>
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