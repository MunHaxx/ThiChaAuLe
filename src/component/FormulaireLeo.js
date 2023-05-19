import React from "react";
import "./FormulaireLeo.css"
import imgLogin from "../images/imgLogin.jpg"
import { Link } from 'react-router-dom'

function Formulaire() {

    return (
      <div className="containerFormulaire">
        <div className="imgLogin"><img alt="" src={imgLogin} /></div>

        <div className="inputContainer">
          <form method="post">
            <input id="id" type="text" name="id" placeholder="ID"/>
            <input id="password" type="password" name="password" placeholder="Password"/>
            <button type="submit" value="valider">Valider</button>
          </form>
        </div>
      </div>
    );
  }
  
  export default Formulaire;
  