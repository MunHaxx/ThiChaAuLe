import React from 'react'
import "./Temoignages.css";
import imgQuote from "../../images/imgQuote.png"

function Temoignages() {
  return (
    <div className="Page Temoignages">
        <div className='title'>TÉMOIGNAGES</div>
        <div className="quotes-container">
          <div className='quote'>
            <div className='icon-quote-container'>
              <img className="icon-quote" alt="" src={imgQuote} />
            </div>

            <div className="quote-title">TRANSPORTÉE À PARIS</div>

            <div className='info-container'>
              <div className="quote-text">
                Je suis ravi de la qualité des produits français que j'ai reçus
                dans ma box. Tout était frais, bien emballé et délicieux !<br /> 
                J'adore découvrir de nouvelles saveurs et ce site a vraiment
                su satisfaire mes papilles. La livraison était rapide et le
                service client très sympathique. Je recommande vivement
                cette box à tous les amateurs de bonne cuisine française !
              </div>
              <div className="quote-author">
                Teddy, Canada
              </div>
            </div>
          </div>
          <div className='quote'>
            <div className='icon-quote-container'>
              <img className="icon-quote" alt="" src={imgQuote} />
            </div>

            <div className="quote-title">COMME EN FRANCE</div>

            <div className='info-container'>
              <div className="quote-text">
                Je suis originaire de France et j'ai été agréablement surpris
                par la qualité et l'authenticité des produits que j'ai reçus dans
                ma box. C'était comme si j'avais un petit bout de France chez moi !
                Les produits étaient tous de qualité supérieure et très bien choisis.
                Le service client était également très réactif et sympathique.<br /> 
                Je recommande cette box à tous les expatriés français en manque
                de saveurs de leur pays natal !<br /> 
              </div>
              <div className="quote-author">
                Danielle, Etat-Unis
              </div>
            </div>
          </div>
        </div>
    </div>
  )
}

export default Temoignages