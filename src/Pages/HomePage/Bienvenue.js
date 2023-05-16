import React from 'react'
import "./Bienvenue.css";
import imgBienvenue from "../../images/imgBienvenue.png"

function Bienvenue() {
  return (
    <div className="Bienvenue">
        <div className='title'>
          <span class="the">THE</span>  
          FRENCH 
          <span class = "flavor">FLAVOR</span>
        </div>
        <div className='subtitle'>
          BOX DE NOURRITURE <br />
          FRANÇAISE
        </div>
        <div className='image'><img alt="" src={imgBienvenue} /></div>
    </div>
  )
}

export default Bienvenue