import React from "react";
import "./Formulaire.css"
import { Link } from 'react-router-dom'

function Formulaire() {

    return (
      <div className="containerFormulaire">
        <div className="inputContainer">
          <form method="post">
            <input className="id-password-login" type="text" name="id" placeholder="nom d'utilisateur"/>
            <input className="id-password-login" type="password" name="password" placeholder="mot de passe"/>
            <button className="connect-login" type="submit" value="valider">Connexion</button>
            <div className="other-register">
              <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"><button className="oublie-mdp" >Mot de passe oublié ?</button></a> 
              <div className="pas-de-compte">Vous n'avez pas de compte ?</div>
              <Link to="/register"><button className="inscrivez-vous" >Inscrivez-vous !</button></Link>
            </div>
          </form>
        </div>
      </div>
    );
  }
  
  export default Formulaire;
  