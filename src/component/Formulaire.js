import React from "react";
import "./Formulaire.css"
import { Link } from 'react-router-dom'

function Formulaire() {

    return (
      <div className="containerFormulaire">

        <div className="inputContainer">
          <form method="post">
            <input id="id" type="text" name="id" placeholder="ID"/>
            <input id="password" type="password" name="password" placeholder="Password"/>
            <button type="submit" value="valider">Valider</button>
            <button><Link to="/register">Créer un compte</Link></button>
          </form>
        </div>
      </div>
    );
  }
  
  export default Formulaire;
  