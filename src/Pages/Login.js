import React from 'react';
import Formulaire from '../component/Formulaire';

import "./Login.css";

function Login() {

  return (
    <div className="Login">
        <div className="login-titles">
          <div className="login-site-title">
            <span className="the">THE</span>  
            <span className="french">FRENCH</span> 
            <span className = "flavor">FLAVOR</span>
          </div>
          <div className="login-connecter-title">SE CONNECTER</div>
        </div>
        <Formulaire />

    </div>
  );
}

export default Login;
