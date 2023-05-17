import React from 'react'
import "./Temoignages.css";
import imgQuote from "../../images/imgQuote.png"

function Temoignages() {
  return (
    <div className="Temoignages">
        <div className='tem-title'>TÉMOIGNAGES</div>
        <div className="container">
          <div className='quote'>
            <div className='icon-quote-container'>
              <img className="icon-quote" alt="" src={imgQuote} />
            </div>
            <div className="quote-title">TRANSPORTÉE À PARIS</div>
            <p className='quote-container'>
              Je suis ravi de la qualité des produits français que j'ai reçus<br /> 
              dans ma box. Tout était frais, bien emballé et délicieux !<br /> 
              J'adore découvrir de nouvelles saveurs et ce site a vraiment<br /> 
              su satisfaire mes papilles. La livraison était rapide et le<br /> 
              service client très sympathique. Je recommande vivement<br /> 
              cette box à tous les amateurs de bonne cuisine française !<br />
              <br />
              Teddy, Canada
            </p>
          </div>
          <div className='quote'>
            <div className='icon-quote-container'>
              <img className="icon-quote" alt="" src={imgQuote} />
            </div>
            <div className="quote-title">COMME EN FRANCE</div>
            <p className='quote-container'>
            Je suis originaire de France et j'ai été agréablement surpris<br /> 
            par la qualité et l'authenticité des produits que j'ai reçus dans<br /> 
            ma box. C'était comme si j'avais un petit bout de France chez moi !<br /> 
            Les produits étaient tous de qualité supérieure et très bien choisis.<br /> 
            Le service client était également très réactif et sympathique.<br /> 
            Je recommande cette box à tous les expatriés français en manque<br />
            de saveurs de leur pays natal !<br /> 
            <br />
            Danielle, Etat-Unis
            </p>
          </div>
        </div>
    </div>
  )
}

export default Temoignages