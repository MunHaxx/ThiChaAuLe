import React from 'react'
import "./Bienvenue.css";
import imgBienvenue from "../../images/imgBienvenue.png"

function Bienvenue() {
  return (
    <div className="Page Bienvenue">
        <div className='title'>
          <span className="the">THE</span>  
          <span className="french">FRENCH</span> 
          <span className = "flavor">FLAVOR</span>
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