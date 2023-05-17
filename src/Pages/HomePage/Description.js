import React from 'react';
import "./Description.css";
import imgDescription from "../../images/imgDescription.jpeg";
import { Link } from 'react-router-dom';

function Description() {
  return (
    <div className="Description">
        <img alt="" src={imgDescription} />
        <div className="right-part-container">
          <div className='in-a-box'>Qu'y a-t-il à l'intérieur de chaque Box ?</div>
          <ul>
            <li>Des produits issus de producteurs français</li>
            <li>Des explications sur les produits</li>
            <li>La France a porté de main</li>
            <li>Délicieux repas garantis !</li>
          </ul>
          <Link to = "/boxs"><button id='parcourir' type='search' value='parcourir'>PARCOURIR LES BOXS !</button></Link>
        </div>
    </div>
  )
}

export default Description