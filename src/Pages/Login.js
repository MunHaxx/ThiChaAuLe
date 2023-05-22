import React from 'react';
import Formulaire from '../component/Formulaire';
import { Link } from 'react-router-dom'

import "./Login.css";

function Login() {

  return (
    <div className="Login Page">
        <div className="login-and-register">
          <div className="title">
            <div className="the">THE</div>  
            <div className="french">FRENCH</div> 
            <div className="flavor">FLAVOR</div>
          </div>
          <div className="login-connecter-title">SE CONNECTER</div>
          <div className="Formulaire-Login"><Formulaire /></div>
            <div className="other-register">
              <div className="oublie-mdp" ><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley">Mot de passe oublié ?</a></div>
              <div className="pas-de-compte">Vous n'avez pas de compte ?</div>
              <div className="inscrivez-vous" ><Link to="/register">Inscrivez-vous !</Link></div>
            </div>
        </div>
    </div>
  );
}

export default Login;
