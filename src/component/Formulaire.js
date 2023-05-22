import React from "react";
import "./Formulaire.css"

function Formulaire() {

    return (
      <div className="containerFormulaire">
        <div className="inputContainer">
          <form method="post">
            <input className="id-password-login" type="text" name="id" placeholder="nom d'utilisateur"/>
            <input className="id-password-login" type="password" name="password" placeholder="mot de passe"/>
            <button className="connect-login" type="submit" value="valider">Connexion</button>
          </form>
        </div>
      </div>
    );
  }
  
  export default Formulaire;
  