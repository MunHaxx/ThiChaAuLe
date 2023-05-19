import React from 'react'
import "./Bienvenue.css";
import imgBienvenue from "../../images/imgBienvenue.png"

function Bienvenue() {
  return (
    <div className="Page Bienvenue">
        <div className='title'>
          <div className="the">THE</div>  
          <div className="french">FRENCH</div> 
          <div className = "flavor">FLAVOR</div>
        </div>
        <div className='subtitle'>
          BOX DE NOURRITURE 
          <br />
          FRANÇAISE
        </div>
        <div className='image'><img alt="" src={imgBienvenue} /></div>
    </div>
  )
}

export default Bienvenue